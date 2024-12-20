from account import Account

def test_btc_address_generation():
    access_token = input("Enter access token: ")
    acc = Account(access_token)
    btc_address = acc.generate_bitcoin_address(access_token)
    if btc_address:
        print(f"BTC Address: {btc_address.get('address')}")
    else:
        print("BTC address generation failed.")

if __name__ == "__main__":
    test_btc_address_generation()