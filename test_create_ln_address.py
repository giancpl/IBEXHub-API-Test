from account import Account

def test_create_ln_address():
    access_token = input("Enter access token: ")
    alice = Account(access_token)
    ln_address = alice.create_ln_address(access_token)
    if ln_address:
        print(f"Generated Lightning address: {ln_address['username']}")
    else:
        print("Failed to create Lightning address.")

if __name__ == "__main__":
    test_create_ln_address()
