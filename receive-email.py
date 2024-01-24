#!/usr/bin/env python
# -*- coding: utf-8 -*-
#The code is not yet read for implementation

"""import imaplib
import getpass

M = imaplib.IMAP4_SSL('imap.gmail.com')

email = getpass.getpass("Email :")
password = getpass.getpass("Password :")

M.login(email,password)

print(M.list())                       # print various inboxes
status, messages = M.select("INBOX")  # select inbox"""
"""Trying new way to do it"""
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

def send_reply(email_address, message):
    # Generate response using ChatGPT API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}],
    }

    response = requests.post(api_url, json=data, headers=headers)
    response_data = response.json()
    reply = response_data["choices"][0]["message"]["content"]

    # Send the reply email
    # You'll need to implement the email sending part here using your preferred email library

# Main script
if __name__ == "__main__":
    email_ids = fetch_unread_emails()
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_username, email_password)

    for email_id in email_ids:
        subject, from_email, body = get_email_content(email_id)
        
        # Extract the user's message from the email body
        user_message = re.sub(r"(?i)(?:\s*re:\s*)?{}".format(re.escape(subject)), "", body).strip()

        # Generate and send reply
        reply = send_reply(from_email, user_message)
        print("Generated reply:", reply)

        # Mark the email as read
        mail.store(email_id, "+FLAGS", "\\Seen")

    mail.logout()
