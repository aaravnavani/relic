from pyicloud import PyiCloudService
import getpass
import re

apple_id = getpass.getpass("Enter your Apple ID: ")
password = getpass.getpass("Enter your Apple ID password: ")

# Initialize the iCloud service
api = PyiCloudService(apple_id, password)

# Handle two-factor authentication if required
if api.requires_2fa:
    print("Two-factor authentication is required.")
    code = input("Enter the 2FA code: ")
    if not api.validate_2fa_code(code):
        print("Failed to verify 2FA code.")
        exit(1)

def normalize_phone(phone_str):
    """
    Normalize the phone string:
      - If it contains a '+', return the plus sign followed by the first 11 digits.
      - If no '+', return '+1' plus the first 10 digits.
    """
    phone_str = phone_str.strip()
    if phone_str.startswith('+'):
        digits = re.sub(r'\D', '', phone_str)
        return '+' + digits[:11]
    else:
        digits = re.sub(r'\D', '', phone_str)
        return '+1' + digits[:10]

# Retrieve all contacts from iCloud
contacts = api.contacts.all()

# Process and print each contact's details with normalized first phone number
dictionary = {}
for contact in contacts:
    first_name = contact.get('firstName', '')
    last_name = contact.get('lastName', '')
    name = f"{first_name} {last_name}".strip()
    
    # Get the first phone number only
    phones = contact.get('phones', [])
    normalized_number = ""
    if phones:
        raw = phones[0].get('field', '')
        if raw:
            normalized_number = normalize_phone(raw)
    
    dictionary[normalized_number] = name
    
print(dictionary)