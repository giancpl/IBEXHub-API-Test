# IBEXHub-API-Test

## Introduction

**IBEXHub** is an API service designed to integrate Bitcoin and Lightning Network functionalities into applications. The service manages a cluster of Lightning nodes, liquidity, and channels to ensure proper operation. The focus of this project is to implement and test five of IBEXHub's APIs, alongside thorough documentation to support the testing process. This includes testing account creation, Bitcoin and Lightning address generation, fee estimation, invoice generation, and payment splits.

## Initial Setup

This project is implemented using **Python**, with the key functionality relying on HTTP requests made using the `requests` library. The project is structured with different Python files for each API's functionality and test cases. Each test function is isolated in its own script to make it easy to test and execute individually.

### Requirements

- Python 3.x
- `requests` library (for making HTTP requests)
  
If `requests` is not installed, use the following command to install it:

```bash
pip install requests
```

### Project Structure
```bash
IBEXHub-API-Test/
│
├── .gitignore               # ignore file
├── README.md                # Project documentation
├── account.py               # Contains the Account class with various API methods
├── test.ipynb               # Jupyter notebook to easly test
├── test_account_creation.py # Test for creating an account
├── test_auth.py             # Test for authentication
├── test_btc_address_generation.py  # Test for generating Bitcoin addresses
├── test_create_btc_splits.py       # Test for creating btc payment splits
├── test_create_ln_address.py      # Test for generating Lightning Network addresses
├── test_create_ln_splits.py       # Test for creating LN payment splits
├── test_estimate_fee.py     # Test for fees estimation
├── test_invoice_from_lnaddress.py # Test for the invoice generation from a ln address
├── test_refresh_access_token.py  # Test for refreshing the access token
├── utils.py                 # useful functions for interaction with the API
├── requirements.txt       # dependencies file
```

### How to install and run code
1. **Clone this repository** to your local machine:
   ```bash
   git clone https://github.com/giancpl/IBEXHub-API-Test.git
   cd IBEXHub-API-Test 
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the tests
Execute each test file with:
```bash
python <test-file.py>
```
Examples:
- Account Creation: tests the creation of a new account using a name and access token
  ```bash
  python test_account_creation.py
  ```
- Authentication: verifies user authentication via the access token
  ```bash
  python test_auth.py
  ```
- Bitcoin Address Generation: tests generating a Bitcoin address for a specific account
  ```bash
  python test_btc_address_generation.py
  ```

### Jupyter Notebook
The test code can also be launched from a Jupyter Notebook, thanks to the script collected in the file test.ipynb.

To run the notebook:
1. Install Jupyter Notebook (if not already installed):
  ```bash
  # Download Jupyter Notebook
  $ pip install notebook
  ```
2. Launch Jupyter:
  ```bash
  # Launch
  $ python -m notebook
  ```
3. Select test.ipynb from the Jupyter interface, or run the cells individually to test the APIs interactively.

