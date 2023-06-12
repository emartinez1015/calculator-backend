# Calculator Backend

This repository contains the backend code for a calculator application. It provides the necessary functionality for performing basic arithmetic operations.

## How to Run Locally

To run the calculator backend locally, follow these steps:

1. Clone the repository to your local machine using the following command:

   ```shell
   git clone https://github.com/emartinez1015/calculator-backend.git
    
2. Navigate to the project directory:
    ```shell
    cd calculator-backend

3. Create a Python virtual environment:
    ```shell
    python3 -m venv venv

4. Activate the virtual environment:
    ```shell
    source venv/bin/activate

5. Install the required dependencies using pip:
    ```shell
    pip install -r requirements.txt

6. Start the Chalice server by executing the following command:
    ```shell
    chalice local
    
The server will start running on http://localhost:8000.


## How to Run Tests

The calculator backend comes with a set of tests to ensure its functionality. To run the tests, follow these steps:

1. Ensure that you have completed the initial setup steps mentioned in the "How to Run Locally" section.

2. Open a terminal and navigate to the project directory.

3. Run the following command to execute the test suite inside tests folder:

   ```shell
   pytest


## Live Demo API Backend
[Calculator Backend API](https://ky23idqdol.execute-api.us-east-2.amazonaws.com/api/)
