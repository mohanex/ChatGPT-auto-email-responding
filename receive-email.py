"""import imaplib
import getpass

M = imaplib.IMAP4_SSL('imap.gmail.com')

email = getpass.getpass("Email :")
password = getpass.getpass("Password :")

M.login(email,password)

print(M.list())                       # print various inboxes
status, messages = M.select("INBOX")  # select inbox"""

import imaplib
import email
import re
import requests

# Set up your ChatGPT API credentials
api_key = "YOUR_API_KEY"
api_url = "https://api.openai.com/v1/chat/completions"

# Email settings
email_username = "your_email@example.com"
email_password = "your_email_password"
imap_server = "imap.example.com"

def fetch_unread_emails():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_username, email_password)

    # Select the mailbox you want to read from
    mail.select("inbox")

    # Search for unread emails
    _, data = mail.search(None, "UNSEEN")

    email_ids = data[0].split()
    return email_ids

def get_email_content(email_id):
    _, data = mail.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])

    subject = msg["subject"]
    from_email = msg["from"]
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()

    return subject, from_email, body

