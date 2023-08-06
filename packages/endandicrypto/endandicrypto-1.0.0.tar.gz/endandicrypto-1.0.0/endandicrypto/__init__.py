from endandicrypto.import_all import *
from endandicrypto.exception import *

api_url = "https://endandicrypto.comprobitcoin.ch"        # PUBLIC API URL


def new_address(crypto, api_token):
    if str(crypto).lower() != "litecoin" and str(crypto).lower() != "monero":
        raise error_message("'" + str(crypto) + "' is not a cryptocurrency supported by endandicrypto. Currently, the library only supports Litecoin and Monero.")

    response = requests.get(api_url + "?action=get_address&crypto=" + str(crypto).lower() + "&token=" + str(api_token))
    data = response.json()
    
    return data["response"]


def send_money(crypto, amount, recipient, api_token):
    if str(crypto).lower() != "litecoin" and str(crypto).lower() != "monero":
        raise error_message("'" + str(crypto) + "' is not a cryptocurrency supported by endandicrypto. Currently, the library only supports Litecoin and Monero.")
    
    
    elif str(recipient) == "":
        raise error_message("You have not specified the value 'recipient'")
    
    
    try:
        check = float(amount)
    except:
        raise error_message("The value 'amount' must be of type float")

    response = requests.get(api_url + "?action=send_money&crypto=" + str(crypto).lower() + "&amount=" + str(amount) + "&recipient=" + str(recipient) + "&token=" + str(api_token))
    data = response.json()
    
    return data["response"]