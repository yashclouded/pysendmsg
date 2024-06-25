import csv
import time
import random
import PyTextNow as pytextnow

# Configuration 
textnow_file = 'textnow.csv'
contacts_file = 'contacts.csv'
contents_file = 'contents.txt'
sms_notepad_file = 'sms_notepad.txt'
sms_limit_per_account = 10
sms_delay = 1  # in seconds

# Load TextNow accounts
textnow_accounts = []
with open(textnow_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) == 2:
            textnow_accounts.append(row)
if not textnow_accounts:
    print('Error: No TextNow accounts found in the file.')
    exit()

# Test TextNow accounts
print('Testing TextNow accounts...')
good_textnow_accounts = []
for i, account in enumerate(textnow_accounts):
    print(f'Testing account {i+1}/{len(textnow_accounts)}...')
    try:
        client = pytextnow.Client(account[0], account[1])
        client.login()
        client.logout()
        good_textnow_accounts.append(account)
    except Exception as e:
        print(f'Error: Could not log in to account {account[0]}. {e}')
print(f'{len(good_textnow_accounts)} TextNow accounts are ready for use.')

# Load contacts
contacts = []
with open(contacts_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 1:
            contacts.append(row[0])
if not contacts:
    print('Error: No contacts found in the file.')
    exit()

# Load message contents
contents = []
with open(contents_file, 'r') as file:
    contents = file.read().splitlines()
if not contents:
    print('Error: No message contents found in the file.')
    exit()

# Prepare SMS notepad
sms_notepad = {'Total data': len(contacts), 'Total sms sent': 0, 'Total sms failed': 0}

# Send SMS
print('Sending SMS...')
while contacts:
    for account in good_textnow_accounts:
        try:
            client = pytextnow.Client(account[0], account[1])
            client.login()
            for i in range(sms_limit_per_account):
                if not contacts:
                    break
                contact = random.choice(contacts)
                message = random.choice(contents)
                client.send_sms(contact, message)
                contacts.remove(contact)
                sms_notepad['Total sms sent'] += 1
                print(f'Sent SMS to {contact} using {account[0]}.')
                time.sleep(sms_delay)
            client.logout()
        except Exception as e:
            print(f'Error: Could not send SMS using {account[0]}. {e}')
            sms_notepad['Total sms failed'] += sms_limit_per_account
            good_textnow_accounts.remove(account)
    if not good_textnow_accounts:
        print('Error: No TextNow accounts available for sending SMS.')
        exit()

# Write SMS notepad to file
with open(sms_notepad_file, 'w') as file:
    for key, value in sms_notepad.items():
        file.write(f'{key}: {value}\n')
print('SMS sending complete.')
