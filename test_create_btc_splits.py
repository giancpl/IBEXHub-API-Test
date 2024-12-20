from account import Account

def test_create_btc_splits():
    accessToken = input("Enter access token: ")
    paul = Account(accessToken)
    albert = Account(accessToken)
    albert_address = albert.generate_bitcoin_address(accessToken).get('address')
    split_btc = paul.create_splits(accessToken, btc_address=albert_address)
    if split_btc is not None:
        print(f'Bitcoin split created successfully: {split_btc}')
    else:
        print("Failed to create split.")

if __name__ == "__main__":
    test_create_btc_splits()
