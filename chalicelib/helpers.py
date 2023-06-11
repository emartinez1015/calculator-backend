import math
from chalice import ChaliceViewError
#helper functions

def generate_random_url(is_numeric):
    base_url = 'https://www.random.org/strings/'
    if is_numeric == 'true':
        url = base_url + '?num=2&len=3&digits=on&loweralpha=off&unique=on&format=plain&rnd=new'
    else:
        url = base_url + '?num=1&len=20&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new'
    return url


def perform_operation(num1, num2, symbol):

    if not num1.isnumeric():
        return num1
    try:
        expression = f"math.sqrt({num1})" if symbol == "√" else f"{int(num1)} {symbol} {int(num2)}"
        result = eval(expression)
        return result
    except (ValueError, SyntaxError) as e:
        return f"Error: Invalid input or expression: {str(e)}"
    except ZeroDivisionError as e:
        raise ChaliceViewError("Divisor can't be zero. Try other ramdon number.")
