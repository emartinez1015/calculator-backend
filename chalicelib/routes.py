import boto3
import requests
from chalice import BadRequestError, Blueprint, ChaliceViewError, Response
from chalicelib.authorizers import cognito_auth
from chalicelib.helpers import generate_random_url, perform_operation
from chalicelib.models import Operation, Record, User
from datetime import datetime
from peewee import fn
from playhouse.shortcuts import model_to_dict
from chalicelib.config import USER_POOL_REGION, COGNITO_CLIENT_ID

routes = Blueprint(__name__)
api_version = 'v1'
base_path = f'/{api_version}'

@routes.authorizer()
def cognito_auth_wrapper(auth_request):
    return cognito_auth(auth_request)


@routes.route(f'{base_path}/operations', methods=['GET'], authorizer=cognito_auth_wrapper)
def get_operations():
    operations = Operation.select().execute()
    serialized_data = [model_to_dict(op) for op in operations]
    return Response(
        body={'data': serialized_data},
        status_code=200
    )


@routes.route(f'{base_path}/records', methods=['GET'], authorizer=cognito_auth_wrapper)
def get_records():
    page = int(routes.current_request.query_params.get('page', 1))
    per_page = int(routes.current_request.query_params.get('per_page', 10))
    operation_type = routes.current_request.query_params.get('operation_type')
    cognito_user_id = routes.current_request.context['authorizer']['username']

    query = (
        Record.select()
        .join(Operation)
        .join(User, on=(Record.user_id == User.id))
        .where(
            (User.cognito_user_id == cognito_user_id) &
            fn.lower(Operation.type).contains(operation_type.lower()) &
            (Record.active == True)
        )
    )

    offset = (page - 1) * per_page
    limit = per_page

    paginated_results = query.offset(offset).limit(limit)
    total_count = query.count()

    serialized_data = [record.to_dict() for record in paginated_results]

    return Response(
        body={
            'data': serialized_data,
            'total_records': total_count
        },
        status_code=200
    )


@routes.route(f'{base_path}/records', methods=['POST'], authorizer=cognito_auth_wrapper)
def create_record():
    request_data = routes.current_request.json_body
    operation_id = request_data['operation_id']
    num1 = request_data['num1']
    num2 = request_data['num2']
    cognito_user_id = routes.current_request.context['authorizer']['username']

    try:
        operation = Operation.get(Operation.id == operation_id)
        amount = operation.cost
        user = User.get(User.cognito_user_id == cognito_user_id)
        operation_response = perform_operation(num1, num2, operation.symbol)

        new_record = Record.create(
            operation=operation_id,
            user_id=user,
            amount=amount,
            operation_response=operation_response,
            date=datetime.now()
        )

        return Response(
            body={
                'message': 'Record created successfully',
                'data': new_record.to_dict()
            },
            status_code=200
        )
    except (ChaliceViewError, Operation.DoesNotExist, User.DoesNotExist, ZeroDivisionError) as e:
        return Response(
            body={
                'error': str(e),
                'message': 'Failed to create record'
            },
            status_code=400
        )


@routes.route(f'{base_path}/records/{{record_id}}', methods=['DELETE'], authorizer=cognito_auth_wrapper)
def soft_delete_record(record_id):
    try:
        record = Record.get(Record.id == record_id)
        record.active = False
        record.save()

        return Response(
            body={'message': f'Record {record_id} was deleted successfully'}
        )
    except Record.DoesNotExist:
        return Response(
            body={'message': f'Record {record_id} not found'},
            status_code=404
        )


@routes.route(f'{base_path}/random-string', methods=['GET'], authorizer=cognito_auth_wrapper)
def random_string():
    query_params = routes.current_request.query_params
    is_numeric = query_params.get('numeric')

    if is_numeric is None:
        raise BadRequestError('Missing required parameter: numeric')

    url = generate_random_url(is_numeric.lower())
    response = requests.get(url)

    if response.ok:
        strings = response.text.split('\n')[:-1]
        return Response(body={'data': strings})
    else:
        return Response(body={'error': 'Failed to generate random strings'}, status_code=response.status_code)


@routes.route(f'{base_path}/signup', methods=['POST'])
def signup():
    request_body = routes.current_request.json_body
    username = request_body['username']
    password = request_body['password']
    client = boto3.client('cognito-idp', region_name=USER_POOL_REGION)

    try:
        response = client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=username,
            Password=password
        )
        user = User.create(
            username=username,
            status=True,
            cognito_user_id=response['UserSub']
        )
        user.save()
        return Response(
            body={'message': 'Sign up successful', 'data': response},
            status_code=200
        )
    except client.exceptions.UsernameExistsException:
        return Response(
            body={'message': 'Username already exists'},
            status_code=400
        )
    except Exception as e:
        return Response(
            body={'message': f'Sign up failed {e}'},
            status_code=500
        )


@routes.route(f'{base_path}/signin', methods=['POST'])
def signin():
    request_body = routes.current_request.json_body
    username = request_body['username']
    password = request_body['password']
    client = boto3.client('cognito-idp', region_name=USER_POOL_REGION)

    try:
        response = client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        user = User.get(User.username == username)

        return Response(
            body={
                'message': 'Sign in successful',
                'access_token': response['AuthenticationResult']['AccessToken'],
                'user': user.to_dict()
            },
            status_code=200
        )
    except client.exceptions.NotAuthorizedException:
        return Response(
            body={'message': 'Invalid username or password'},
            status_code=401
        )
    except client.exceptions.UserNotConfirmedException:
        return Response(
            body={'message': 'User is not confirmed. Please confirm your account.'},
            status_code=401
        )
    except Exception as e:
        return Response(
            body={'message': f'Sign in failed: {e}'},
            status_code=500
        )



@routes.route(f'{base_path}/signout', methods=['POST'], authorizer=cognito_auth_wrapper)
def signout():
    access_token = routes.current_request.json_body['access_token']
    client = boto3.client('cognito-idp', region_name=USER_POOL_REGION)
    
    try:
        response = client.global_sign_out(
            AccessToken=access_token
        )
        
        return Response(
            body={'message': 'Sign out successful'},
            status_code=200
        )
    except Exception as e:
        return Response(
            body={'message': 'Sign out failed'},
            status_code=500
        )


@routes.route(f'{base_path}/confirm', methods=['POST'])
def confirm():
    request_body = routes.current_request.json_body
    username = request_body['username']
    confirmation_code = request_body['confirmation_code']
    client = boto3.client('cognito-idp', region_name=USER_POOL_REGION)

    try:
        response = client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code
        )

        return Response(
            body={'message': 'User confirmed successfully. You can now sign in.'},
            status_code=200
        )
    except client.exceptions.UserNotFoundException:
        return Response(
            body={'message': 'User not found.'},
            status_code=400
        )
    except client.exceptions.CodeMismatchException:
        return Response(
            body={'message': 'Invalid confirmation code.'},
            status_code=400
        )
    except client.exceptions.NotAuthorizedException:
        return Response(
            body={'message': 'User is already confirmed.'},
            status_code=400
        )
    except Exception as e:
        return Response(
            body={'message': 'Confirmation failed'},
            status_code=500
        )
