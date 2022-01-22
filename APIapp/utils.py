from random import choices
import string


def generate_random_company_id():
    characters = string.digits + string.ascii_letters
    id = "".join(choices(characters, k=8))

    return id