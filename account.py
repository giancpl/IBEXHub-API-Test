import requests
import json
import os

class Account: 
    def __init__(self, access_token):
        account_name = input("Enter the account name: ")
        self.ln_addresses = []
        self.btc_addresses = []

        # account creation
        url = "https://api-sandbox.poweredbyibex.io/account/create"
        payload = { 
            "currencyId": 0, 
            "name": account_name
        }
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json", 
            "Authorization": access_token
        }
        try: 
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            account = response.json()
            print("Account successfully created!")
            if not os.path.exists('users'):
                os.makedirs('users')
            file_name = os.path.join('users', f'{account_name}.json')
            # file_name = f'{account_name}.json'
            with open(file_name, 'w') as file:
                json.dump(account, file, indent=4)
            print(f"Account details saved to {file_name}")
            with open(file_name, 'r') as file:
                try: 
                    data = json.load(file)
                    self.accountId = data['id']
                    self.userId = data['userId']
                    self.organizationId = data['organizationId']
                    self.name = data['name']
                    self.currencyId = data['currencyId']
                except json.JSONDecodeError as err:
                    print(f"Error decoding JSON: {err}")
        except requests.exceptions.HTTPError as err:
            print(f"Error in creating account: {err}")
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")

    def get_account_details(self, access_token):
        url = f"https://api-sandbox.poweredbyibex.io/v2/account/{self.accountId}"
        headers = {
            "Authorization": access_token,
            "Accept": "application/json"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() 
            account_details = response.json()
            return account_details
        except requests.exceptions.HTTPError as err:
            print(f"Error retrieving account details: {err}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            return None
    

    def generate_bitcoin_address(self, access_token):
        url = "https://api-sandbox.poweredbyibex.io/onchain/address"
        headers = {
            "Content-Type": "application/json",
            "Authorization": access_token
        }
        payload = {
            "accountId": self.accountId
        }
        try: 
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            btc_address = response.json()
            self.btc_addresses.append(btc_address)
            return btc_address
        except requests.exceptions.HTTPError as err:
            print(f"Error during on-chain address creation: {err}")
            if response.status_code == 400:
                print("Bad request:", response.json())
            elif response.status_code == 403:
                print("Forbidden:", response.json())
            else:
                print("Unexpected error:", response.status_code, response.json())
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            return None 


    def create_ln_address(self, access_token):
        url = "https://api-sandbox.poweredbyibex.io/lightning-address"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": access_token
        }
        try: 
            username = input(f'Insert a valid username for the LN address: ') 
            if any(addr['username'][0:len(username)] == username for addr in self.ln_addresses):
                print(f"Error: The username '{username}' is already in use for this.")
                return None 
            payload = { 
                "accountId": self.accountId, 
                "username": username
            }
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 201:
                ln_address = response.json()
                self.ln_addresses.append(ln_address)
                return ln_address
            elif response.status_code == 400:
                print("Error 400: Bad request. Please check the input data.")
                return None
            elif response.status_code == 403:
                print("Error 403: Forbidden. You do not have permission to create this address.")
                return None
            else:
                response.raise_for_status()
        
        except requests.exceptions.HTTPError as err:
            print(f"Error in creating the address: {err}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            return None 
    
    def add_invoice(self, access_token, amount = 1000.0, msg = "", expiration = 9000):
        url = "https://api-sandbox.poweredbyibex.io/v2/invoice/add"

        payload = {
            "expiration": expiration,
            "accountId": self.accountId,
            "amount": amount, 
            "memo": msg,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": access_token
        }

        try: 
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            invoice = response.json()
            return invoice
        
        except requests.exceptions.HTTPError as err:
            print(f"Error in adding invoice: {err}") 
            return None
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            return None

    def get_account_transactions(self, access_token, limit=0, page=0, sort='settledAt'):
        url = f"https://api-sandbox.poweredbyibex.io/v2/transaction/account/{self.account_id}/all"
        headers = {
            "Authorization": access_token,
            "Accept": "application/json"
        }
        params = {
            "limit": limit,
            "page": page,
            "sort": sort
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  
            transactions = response.json()
            return transactions
        except requests.exceptions.HTTPError as err:
            print(f"Error retrieving transactions: {err}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            return None


    def create_splits(self, accessToken, btc_address=None, ln_address=None, uuid=None):
        url = f"https://api-sandbox.poweredbyibex.io/account/{self.accountId}/splits"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": accessToken
        }
        payload = []
        if btc_address is not None:
            payload.append({
                "percent": 1,
                "destination": btc_address # onchain address
            })
        if ln_address is not None:
            payload.append({
                "percent": 10,
                "destination": ln_address # lightning address
            })
        if uuid is not None: 
            payload.append({
                "percent": 15,
                "destination": uuid # hub account UUID
            })
        if not payload: # Check if payload is empty
            raise ValueError("At least one destination must be provided.") 
        try: 
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            split = response.json()
            return split
        except requests.exceptions.HTTPError as err:
            print(f"Error during split creation: {err}")
            if response.status_code == 400:
                print("Bad request:", response.json())
            elif response.status_code == 404:
                print("Not found:", response.json())
            else:
                print("Unexpected error:", response.status_code, response.json())


    
