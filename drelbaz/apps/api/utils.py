import re

MINIMUM_PASSWORD_LENGTH = 6
REGEX_VALID_PASSWORD = (
    ## Don't allow any spaces, e.g. '\t', '\n' or whitespace etc.
    r'^(?!.*[\s])'
    ## Check for a digit
    '((?=.*[\d])'
    ## Check for an uppercase letter
    '(?=.*[A-Z])'
    ## check for special characters. Something which is not word, digit or
    ## space will be treated as special character
    '(?=.*[^\w\d\s])).'
    ## Minimum 8 characters
    '{' + str(MINIMUM_PASSWORD_LENGTH) + ',}$')


def validate_password(password):
    if re.match(REGEX_VALID_PASSWORD, password):
        return True
    return False

def retrieve_oauth_client(user):
    try:
        client_id = user.oauth2_client.all()[0].client_id
        client_secret = user.oauth2_client.all()[0].client_secret
        return (client_id, client_secret)

    except IndexError:
        Client.objects.create(
                    user=user,
                    name=user.username,
                    url='http://mondentisteapp.com',
                    redirect_uri='http://mondentisteapp.com',
                    client_type=0)
        client_id = user.oauth2_client.all()[0].client_id
        client_secret = user.oauth2_client.all()[0].client_secret
        return (client_id, client_secret)