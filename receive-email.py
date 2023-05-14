import imaplib
import getpass

M = imaplib.IMAP4_SSL('imap.gmail.com')

email = getpass.getpass("Email :")
password = getpass.getpass("Password :")

M.login(email,password)

print(M.list())                       # print various inboxes
status, messages = M.select("INBOX")  # select inbox

