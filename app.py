from chalice import Chalice, CORSConfig
from chalicelib.routes import routes


cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type'],
    max_age=600,
    expose_headers=['X-Amz-Date']
)

app = Chalice(app_name='calculator-backend')

app.api.cors = cors_config
app.register_blueprint(routes)


@app.route('/', methods=['GET'])
def index():
    return {'message': 'Welcome to the calculator backend API.'}


# Run the Chalice app
if __name__ == '__main__':
    app.debug = True
    app.run()
