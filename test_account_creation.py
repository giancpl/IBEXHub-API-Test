from account import Account

def test_account_creation():
    access_token = input("Enter access token: ")
    account = Account(access_token)
    if account:
        print(f"Account {account.name} created successfully!")
    else:
        print("Account creation failed.")

if __name__ == "__main__":
    test_account_creation()
