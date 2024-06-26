from tests.server_calls import clear_v2, auth_register_v2
from tests.helpers import clear_database

"""
==============================================================
AUTH_REGISTER_V1 TESTS
==============================================================
"""

# Test single registers with valid emails
def test_register_unique_tokens_valid():
    token1 = auth_register_v2("test", "test@test.com", "luciddreams14")["token"]
    token2 = auth_register_v2("test", "test1@test.com", "luciddreams14")["token"]
    # Testing if tokens are unique
    assert token1 != token2

# Test multiple registers
def test_register_multiple_success():
    token1 = auth_register_v2("test", "test@test.com", "www.www")["token"]
    token2 = auth_register_v2("test", "test1@test.com", "lisbon2424")["token"]
    token3 = auth_register_v2("test", "test2@test.com", "janedoe")["token"]
    token4 = auth_register_v2("test", "test3@test.com", "knittingislife")["token"]
    assert token1 != token2 != token3 != token4

# Test Input errors for invalid email - failing regex match
def test_register_invalid_email():
    # Not matching regex after first character class
    assert auth_register_v2("test", "chocoalate", "covered")['detail'] == "Email is invalid!"

    # Doesn't have an @
    assert auth_register_v2("test", "waterfordsgmail.com", "dasani2048")['detail'] == "Email is invalid!"

    # Fails last part of the regex - missing 2 alphabetic characters after '.'
    assert auth_register_v2("test", "test@test.c", "paperboy")['detail'] == "Email is invalid!"

    # No email given
    assert auth_register_v2("test", "", "paperboy")['detail'] == "Email is invalid!"

# Email is not unique - Raise Input Error
def test_register_duplicate_email():
    # Duplicate email example 1
    token = auth_register_v2("test", "test@test.com", "iloveyou")["token"]
    assert auth_register_v2("test", "test@test.com", "iloveyou")['detail'] == "Invalid input: Email test@test.com is already taken."

    # Duplicate email example 2 - only email is duplicated
    auth_register_v2("test", "test1@test.com", "dasani2048")
    assert auth_register_v2("test", "test1@test.com", "dasani")['detail'] == "Invalid input: Email test1@test.com is already taken."

# Length of password is less than 6 characters
def test_register_short_passwords():
    assert auth_register_v2("test", "test@test.com", "2048")['detail'] == "Invalid input: Password is too short."

    assert auth_register_v2("test", "test1@test.com", "LoVer")['detail'] == "Invalid input: Password is too short."

    assert auth_register_v2("test", "test2@test.com", "")['detail'] == "Invalid input: Password is too short."

