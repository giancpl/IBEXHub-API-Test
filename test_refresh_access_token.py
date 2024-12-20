from utils import refresh_access_token

def test_refresh_token():
    refresh_token = input("Enter refresh token: ")
    new_token = refresh_access_token(refresh_token)
    if new_token:
        print(f"New Access Token: {new_token.get('accessToken')}")
    else:
        print("Token refresh failed.")

if __name__ == "__main__":
    test_refresh_token()
