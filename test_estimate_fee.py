from utils import estimate_fee

def test_estimate_fee():
    accessToken = input("Enter access token: ")
    oc_address = input("Enter the bitcoin on-chain address: ")
    amount = input("Enter the amount: ")
    fees = estimate_fee(accessToken, oc_address, amount)
    if fees is not None:
        print(f"Estimated fees: {fees}")
    else:
        print("Error in fee estimation.")

if __name__ == "__main__":
    test_estimate_fee()