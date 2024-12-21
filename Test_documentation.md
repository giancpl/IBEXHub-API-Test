# Documentation 
## Abstract
This document provides comprehensive documentation for the implementation and testing of several APIs offered by IbexHUB. 
It includes instructions for executing the code, as well as detailed explanations of each functionality, including testing requests and responses for each endpoint.

## Introduction
IBEXHub is an API service that integrates Bitcoin and Lightning Network functionalities into applications. 
This project focuses on implementing and testing five of the available APIs, with a strong emphasis on testing account creation, Bitcoin and Lightning address generation, fee estimation, invoice generation, and payment splits.

The following paragraphs will focus on each of the different APIs that have been tested, providing detailed documentation for each step, along with relevant test cases. 
Any errors or unexpected behaviors encountered will be reported and analyzed.

## Initial set-up
This implementation is built using Python. HTTP requests are made using the requests library. 
Ensure Python is installed, then clone the Git repository 
```shell
git clone https://github.com/giancpl/IBEXHub-API-Test.git
cd IBEXHub-API-Test 
```
and install dependencies
```shell
pip install -r requirements.txt
```

## **Imported Modules**:
- `requests`: for making HTTP requests to the API.
- `json`: for working with JSON data.
- `os`: for file and directory management.

## Test Files
Here is a description of how to run each test file, along with associated input parameters required which are commonly passed as input by the user during the testing process.

### **utils.py**
Contains utility functions used across the test scripts. This file includes functions for making requests to the API, handling responses, and performing other common tasks needed for testing. In particular it includes:
- authentication function that handle the auth process
- refresh token function to retrieve an access token
- estimate fee function
- function that generate an invoice from a LN address

### **account.py**
The account.py file defines an Account class that manages the creation of an account, the generation of Bitcoin and Lightning addresses, creating payment splits, and adding invoices for an account on IBEXHub. 
The class provides methods to interact with the IBEXHub API to:
- Create an account: Takes an account name, sends a request to the API to create the account, and saves the account details in a JSON file.
- Retrieve account details: Allows fetching account information using the account ID.
- Generate a Bitcoin address: Creates a Bitcoin address for the specified account.
- Create a Lightning (LN) address: Creates a Lightning address for the account, ensuring the username is not already in use.
- Add an invoice: Allows adding an invoice associated with the account, with a specified amount and expiration.
- Get transactions: Retrieves transactions related to the account, with parameters for limit, page, and sorting.
- Create payment splits: Allows creating payment splits between Bitcoin addresses, Lightning addresses, and other accounts, with a percentage allocated to each destination.


**test_account_creation.py**
- Description: This file contains automatic tests for the account creation functionality. The tests verify that the account creation API is working properly and that the account details are saved correctly to file.
- Execution:
  ```shell
  python test_account_creation.py
  ```

**test_auth.py**
- Description: The file test_auth.py contains the tests for handling authentication in the API. The tests check that authentication with credentials works correctly, giving as output access and refresh tokens.
- Execution:
  ```shell
  python test_auth.py
  ```
> [!note] 
> I used to store the credentials in a text file named `credentials.json` which will be automatically created when you first log in using your credentials. Here is the structure of the file:
  ```shell
  {
      "email": ""
      "password": ""
  }
  ```
**test_refresh_access_token.py**
- Description: Tests the refresh functionality for expired access tokens. This script allows the user to get a new access token using the refresh token when the old token expires.
- Execution:
  ```shell
  python test_refresh_access_token.py
  ```
**test_btc_address_generation.py**
- Description: This file contains the tests for generating Bitcoin addresses. The tests verify that the addresses (P2WPKH) are generated correctly via the API.
- Execution:
  ```shell
  python test_btc_address_generation.py
  ```
**test_create_ln_address.py**
- Description: Tests the functionality of creating a Lightning address associated with a specific IBEXHub account. It ensures that a valid Lightning address is returned.
- Execution:
  ```shell
  python test_create_ln_address.py
  ```
**test_invoice_from_lnaddress.py**
- Description: Tests the generation of a Bolt11 invoice from a Lightning address. This test ensures that a valid invoice can be created using a specified Lightning address.
- Execution:
  ```shell
  python test_invoice_from_lnaddress.py
  ```
**test_create_btc_splits.py**
- Description: Tests the creation of payment splits for Bitcoin payments. Payment splits are a "promise" made from one account to another account, a Lightning address, or an on-chain address.
- Execution:
  ```shell
  python test_create_btc_splits.py
  ```
**test_create_ln_splits.py**
- Description: Tests the creation of payment splits for Lightning Network payments. It ensures that a Lightning payment can be split across multiple destinations.
- Execution:
  ```shell
  python test_create_ln_splits.py
  ```
**test_estimate_fee.py**
- Description: Tests the fee estimation functionality for on-chain Bitcoin payments. This test verifies that the estimated transaction fees are correctly calculated based on the provided Bitcoin address and amount.
- Execution:
  ```shell
  python test_estimate_fee.py
  ```



## Authentication phase
To begin the API testing process, the authentication phase must be completed first. Once the credentials are obtained, successful authentication will provide the *access token* and the *refresh token*.
IbexHUB uses JWT-based authentication, meaning that when an endpoint returns a 401 response code, it indicates that the access token has expired. In this case, the Refresh Access Token endpoint must be called to obtain a new token.

The authentication function accepts the email, password, and an optional user-agent parameter. 
It constructs a JSON object containing the email and password in the body and sends a POST request to the Sign In endpoint (https://api-sandbox.poweredbyibex.io/auth/signin).
If the response status code is 200, the returned JSON includes the *accessToken*, *expirationTime*, and *refreshToken*.

### Test results 
Here is a list of possible test cases to observe how the API behaves:
- 400 Bad Request (Wrong Password): This occurs when the password is incorrect, but the email is valid.
- 403 Forbidden (Wrong Credentials): This occurs when either the email is incorrect or both the email and password are wrong.

### Suggestions 
- The documentation does not consistently mention the 401 response code, which typically occurs when the access token has expired. So it would be helpful to specify this response code as a possible outcome.
- Currently, the web UI for the API is not responsive, which prevents users from manually entering email, password, and authentication token. Implementing a more user-friendly and responsive interface would improve the overall experience and make testing easier for users.
- Although I have not yet reached the limit for creating access tokens from a single refresh token, it would be beneficial to implement a threshold for the maximum number of access tokens that can be generated in a given time period. This would act as an additional security measure to prevent potential abuse. If this limitation is not already in place, it is recommended to consider adding it.



## Generate onchain address 

This feature is implemented as method in the account class and takes as input the *accessToken*. 
Then you can call the function that performs a POST request to the endpoint (https://api-sandbox.poweredbyibex.io/onchain/address) to generate the onchain address for the account chosen.

### Test result
- 201 - Created: A new bitcoin on-chain address (P2WPKH) is successfully created.
- 400 - Bad Request: The account is specified in an unexpected format.
- 401 - Unauthorized: Invalid token provided.
- 404 - Not Found: The specified account is not present in the list of available accounts.
### Suggestions
- The documentation contains a truncated sentence: "Funds will only show up after a transaction's status is...". This incomplete sentence needs clarification to properly explain when and how funds will appear in the new onchain address.
- It would be an excellent implementation to be able to select the type of address to be generated, despite the fact that those currently present (P2WPKH) are the most common. 
- Another option could be to link a unique on-chain address to each user or account using a silent payment address (as specified in BIP 352). This new system eliminates the need for users to create a new address every time they want to receive a payment. Instead, the payer automatically generates the address based on a fixed starting point (an 'sp1' address) provided by the recipient. The implementation of this new protocol does not compromise address privacy due to the incorporation of Taproot technology.



## Create and associate a lightning address to the IBEXHub account
Lightning addresses provide a user-friendly way to facilitate payments on the Lightning Network, aiming to enhance the usability of Bitcoin for everyday transactions. 
This functionality allows the creation of a Lightning address linked to a user account. Multiple Lightning addresses can be generated from the same account. 

The first step in the implementation process is creating a new user account using the Create User API. This process is handled by creating a new account object using the associated class, which requires the following parameters: *accessToken*, *username* (given as input), and the *currencyId* for the desired currency in the new account. 
The response will contain important information, such as the *accountID* (which should be stored for future use, for example using the export command), *userID*, *organizationId* (shared across all accounts created by the same operator), *name*, and *currencyId*. 
In the response, the balance should also be included, but during testing, this field was not returned.

To generate a Lightning address, the create_ln_address function is used. It is a method of the account class that accepts the accessToken, accountId, and username as parameters. 
The values are passed as input in a JSON format in the body of a POST request to the endpoint (https://api-sandbox.poweredbyibex.io/lightning-address). The response will include the *Id*, the *accountId*, and the newly created *lightningAddress* with the specified username.

### Test results
- 201 Created: A new Lightning address has been successfully created with the specified username.
- 400 Bad Request: The accountId is in an invalid format (e.g., incorrect characters or length), or the username is already in use.
- 401 Unauthorized: The accessToken is invalid or has expired.
- 404 Not Found: The specified accountId does not exist in the list of accounts.

### Suggestions
- While the current implementation checks for username availability, it could be enhanced by providing more detailed error messages if a username already exists. For example, instead of just a general error, it could suggest similar available usernames or provide a clearer indication of why the username is invalid.
- The web interface example (executed in Python) currently returns a 400 response code due to an EOF error.
- If too many Lightning addresses are being created, there could be rate limiting or throttling mechanisms in place to prevent abuse or accidental flooding of the system. A limit on the number of addresses per account within a specific timeframe could be beneficial for both security and performance reasons.
- If an address is not used for a long period, it might be helpful to add an automatic expiration or deactivation feature to prevent old, unused addresses from cluttering the system. Users could be notified about the expiration date or prompted to confirm continued usage.



## Create a Bolt11 invoice using the lightning address
BOLT11 invoices are a standardized format for requesting payments on the Lightning Network. This format allows users to generate and share invoices easily, enabling quick payments. This functionality allows the creation of a Bolt11 invoice linked to an existing Lightning address.

The function responsible for this feature is invoice_from_lnaddress from the utils file. 
It takes some input parameters: *accessToken*, the *lightning address* associated with a specific account, the *amount* for the invoice and the *comment* attached to it (optional). 
These values are then passed as parameters in the URL of the GET request to the endpoint: https://api-sandbox.poweredbyibex.io/lnurl/pay/invoice?amount={amount}&ln-address={ln-address}&comment={comment}

However, the behavior of this API was not as expected. Despite the request being correctly formatted (with the correct number and type of parameters), the response code was consistently 201, and the body of the response contained:
```shell
{
  "reason": "record not found",
  "status": "ERROR"
}
```
Despite this, I was still able to generate a valid Bolt11 invoice using the *Add Invoice V2* API, which requires the accountId instead of the lightning address. 
Using this method, it should be possiblee to successfully proceed with making a payment to the generated invoice.
 
### Test results
Whether tested from the web UI or directly with my implementation, the response code was always 201, even when using an incorrect accessToken. 
The response body remained the same, indicating a 201 Created status but containing the error message mentioned above.

### Suggestions
The error previously mentioned — where a 201 status code is returned with an error message ("record not found") — should be addressed. 
It is important to investigate and fix this issue to ensure that the API behaves as expected and provides the correct status codes and meaningful responses for different scenarios. 
Proper error handling and clearer documentation would enhance the overall usability of the API.



## Estimate fee required to send sats 
This feature is implemented in the utils file as a function easly named *estimate_fee*. 
It takes as parameters the *accessToken*, the *on-chain address*, and an *amount* (in millisats). 
The function performs a GET request to the endpoint (https://api-sandbox.poweredbyibex.io/v2/onchain/estimate-fee?address={address}&amount={amount}&currency-id={curr}). 
This request returns an estimation of the fees required to send sats to the specified onchain address.

### Test results
- 200 - OK: The fees estimation is returned. In my tests, the fee was always 0, but this may be due to the absence of sats in any of the accounts.
- 400 - Bad Request: This error occurs if the specified Bitcoin address is invalid or if the amount is not within the expected range.
- 401 - Unauthorized: This error occurs when the provided token is invalid.

### Suggestions
- In testing, the returned fee was consistently 0. This could be due to test environment limitations (e.g., no sats in the account). It would be helpful to clarify in the documentation whether the test environment accurately reflects real-world behavior and under what circumstances a fee of 0 might be returned.
- For the amount parameter, the valid range or acceptable values are not explicitly documented. Including this information would prevent unnecessary 400 errors and improve user experience.



## Create a payment Split 
A payment split involves dividing a single incoming payment into multiple portions, distributing the funds to designated destinations once they are received in the account. This feature provides a seamless way to automate fund allocation.

The split function is implemented as a method of the account class object. 
It requires as input the *accessToken* that allows you to be authenticated by the API and three optional parameters depending on the split you want to make. 
These parameters are passed to the request as a json file formatted as:
```shell
[
  {
    "percent": "",  // Percentage of the funds to this destination
    "destination": ""  // On-chain address
  },
  {
    "percent": "",  
    "destination": ""  // Lightning address
  },
  {
    "percent": "",  
    "destination": ""  // Hub account UUID
  }
]
```

The percent attribute specifies the portion of funds allocated to each destination. Destinations can be:
- On-chain addresses
- Lightning Network addresses
- Account UUIDs within the hub
In the test file you can simulate it by creating new accounts and trying to send funds to new btc or LN addresses.

### Test results
- 200 - OK: The split configuration is valid, and the specified destinations exist, are correctly formatted, and are distinct from the source address
- 400 - Bad Request:
  - An edge already exists between the specified accounts
  - Source and destination addresses are the same
  - Duplicate entries in the JSON body
- 404 - Not Found: The specified account does not exist

### Suggestions
The example provided in the web UI is static and non-interactive, preventing users from executing split creation directly from the interface. 
It would be beneficial to enable an interactive example for better usability and testing.



## Conclusions
The IBEXHub API provides a robust and flexible platform for managing Bitcoin and Lightning Network operations. 
From creating accounts and generating on-chain and Lightning addresses to estimating fees and implementing advanced features like payment splits, the API offers powerful tools to streamline payment processes. 
However, the following key observations and recommendations were made during testing and implementation.

### Strengths
- Comprehensive Functionality: The API supports a wide range of Bitcoin and Lightning Network features, catering to diverse use cases.
- Standardized Protocols: The use of industry standards like BOLT11 ensures compatibility with the broader Lightning Network ecosystem.
- Customizability: Features like payment splits allow for highly specific and dynamic fund management scenarios.

## Areas for Improvement
- Documentation Quality: Several endpoints lack sufficient detail, such as the incomplete description for k1 and missing parameters in some examples. Enhanced documentation would improve the developer experience.
- Error Handling: Some endpoints return ambiguous or misleading responses. This behavior needs clarification or correction to ensure reliability.
- Interactive Examples: The current web UI examples are static and do not allow hands-on testing. Enabling interactivity would help users better understand and implement the API features.
- Edge Case Management: Clearer guidance on edge cases, such as rate limits or duplicate entry handling, would help developers build more robust integrations.

## Final Thoughts
The IBEXHub API is a promising tool for enabling innovative Bitcoin and Lightning Network applications. 
With improvements in documentation, error messaging, and user interface interactivity, it has the potential to significantly enhance usability and adoption. 
By addressing these areas, IBEXHub can better support developers in creating seamless, efficient, and secure financial solutions.


