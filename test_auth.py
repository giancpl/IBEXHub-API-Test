from utils import authenticate

def test_authenticate():
    tokens = authenticate()
    if tokens:
        print("Authentication successful!")
        print(f"Access Token: {tokens.get('accessToken')}")
    else:
        print("Authentication failed.")

if __name__ == "__main__":
    test_authenticate()
    