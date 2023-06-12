import math
from chalice import ChaliceViewError
from chalicelib.config import RAMDON_ORG_URL


def generate_random_url(is_numeric):
    """
    Generates a URL for requesting random strings from a random.org API.
    The URL format depends on the value of the 'is_numeric' parameter.
    If 'is_numeric' is 'true', the URL will request numeric strings.
    If 'is_numeric' is any other value, the URL will request alphanumeric strings.
    Returns the generated URL.
    """
    base_url = RAMDON_ORG_URL
    if is_numeric == 'true':
        url = base_url + '?num=2&len=3&digits=on&loweralpha=off&unique=on&format=plain&rnd=new'
    else:
        url = base_url + '?num=1&len=20&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new'
    return url


def perform_operation(num1, num2, symbol):
    """
    Performs a mathematical operation based on the given inputs.
    The operation can be addition, subtraction, multiplication, division, square root or ramdon string generation.
    Returns the result of the operation.
    If an error occurs during the evaluation, returns an error message.
    """
    if not num1.isnumeric():
        return num1
    try:
        expression = f"math.sqrt({num1})" if symbol == "√" else f"{int(num1)} {symbol} {int(num2)}"
        result = eval(expression)
        return result
    except (ValueError, SyntaxError) as e:
        return f"Error: Invalid input or expression: {str(e)}"
    except ZeroDivisionError as e:
        raise ChaliceViewError("Divisor can't be zero. Try other random number.")
