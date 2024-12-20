from utils import invoice_from_lnaddress

def test_invoice_from_lnaddress():
    accessToken = input("Enter access token: ")
    ln_address = input("Enter LN address: ")
    amount = input("Select the amount: ")
    comment = input("Insert a comment: ")

    invoice = invoice_from_lnaddress(accessToken, ln_address, amount, comment)

    if invoice is not None:
        print(f"Invoice from LN address: {invoice}")
    else: 
        print("Invoice generation failed.")

if __name__ == '__main__':
    test_invoice_from_lnaddress()