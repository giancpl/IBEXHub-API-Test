import json, os, requests

def authenticate():
    url = "https://api-sandbox.poweredbyibex.io/auth/signin"
    headers = {
        "Content-Type": "application/json"
    }
    credentials_file = 'credentials.json' 
    # Read credentials from the JSON file
    try:
        # check if the credentials file already exists 
        if os.path.isfile(credentials_file):
            print(f"The file '{credentials_file}' already exists.")
        else:
            print(f"The file '{credentials_file}' does not exist yes.")
            email = input("Insert the email: ")
            password = input("Insert the password: ")
            credentials = {
                "email": email,
                "password": password
            }
            with open(credentials_file, 'w') as json_file:
                json.dump(credentials, json_file)
            print(f"Email: {email}, Password: {password}") 
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{credentials_file}' was not found.")
        return None, None
    except json.JSONDecodeError:
        print(f"Error: The file '{credentials_file}' is not a valid JSON.")
        return None, None
    
    payload = {
        "email": credentials["email"],
        "password": credentials["password"]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for error responses
        tokens = response.json() # If the request is successful, return the tokens
        return tokens
    
    except requests.exceptions.HTTPError as err:
        # Handle authentication errors 
        print(f"Error during authentication: {err}")
        if response.status_code == 400:
            error_message = response.json().get("error", "Unknown error")
            print(f"Bad Request (400): {error_message}")
        elif response.status_code == 401:
            print("Unauthorized (401): Invalid email or password.")
        elif response.status_code == 403: 
            print("Forbidden (403): Access denied.")
        elif response.status_code == 404:
            print("Not Found (404): The requested resource was not found.")
        elif response.status_code == 500:
            print("Internal Server Error (500): An error occurred on the server.")
        else:
            print(f"Error {response.status_code}: {err}")
        return None
    except requests.exceptions.RequestException as err:
        # Handle other request-related errors
        print(f"Request error: {err}")
        return None
    

def refresh_access_token(refresh_token):
    url = "https://api-sandbox.poweredbyibex.io/auth/refresh-access-token"
    payload = {
        "refreshToken": refresh_token
    }
    headers={
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() 
        access_token = response.json() # If the request is successful, return the tokens
        return access_token
    except requests.exceptions.HTTPError as err:
        print(f"Error during authentication: {err}")
        return None


def estimate_fee(access_token, btc_address, amount, currency_id = 0): 
    url = f"https://api-sandbox.poweredbyibex.io/v2/onchain/estimate-fee?address={btc_address}&amount={amount}&currency-id={currency_id}"
    headers = {
        "accept": "application/json",
        "Authorization": access_token
    }
    try: 
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        fee = response.json()
        return fee
    except requests.exceptions.HTTPError as err:
        print(f"Error during on-chain address creation: {err}")
        if response.status_code == 400:
            print("Bad request:", response.json())
        elif response.status_code == 404:
            print("Not found:", response.json())
        else:
            print("Unexpected error:", response.status_code, response.json())


def invoice_from_lnaddress(access_token, ln_address, amount = 0, comment = ""):
        url = f"https://api-sandbox.poweredbyibex.io/lnurl/pay/invoice?amount={amount}&ln-address={ln_address}&comment={comment}"
        headers = {
            "accept": "application/json",
            "Authorization": access_token
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                bolt11 = response.json()
                return bolt11
            elif response.status_code == 400:
                print("Error: Bad request. Please check the LN address and amount.")
                return None
            else:
                response.raise_for_status()  

        except requests.exceptions.HTTPError as err:
            print(f"Error in generating an invoice from the ln-address: {err}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            return None 
        
def get_transaction_details(transaction_id, access_token):
    url = f"https://api-sandbox.poweredbyibex.io/transaction/{transaction_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        transaction_data = response.json()
        return transaction_data
    except requests.exceptions.HTTPError as err:
        print(f"Error retrieving transaction details: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return None