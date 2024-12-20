from account import Account

def test_create_ln_splits():
    accessToken = input("Enter access token: ")
    carl = Account(accessToken)
    robert = Account(accessToken)
    lightning_address = robert.create_ln_address(accessToken).get('username') 

    split_ln = carl.create_splits(accessToken, ln_address=lightning_address)
    if split_ln is not None:
        print(f'LN split created successfully: {split_ln}')
    else:
        print("Failed to create split.")

if __name__ == "__main__":
    test_create_ln_splits()
