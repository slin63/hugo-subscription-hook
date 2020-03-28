# Runs at a fixed interval and pulls in gmails & curls website
# - Email subjects contain actions + information
#   - Modify data store from email subjects
# - Notifies subscribers on website changes

# Gets account information from .env
import imaplib
import base64
import os
import pathlib
import email

from sys import byteorder
from hashlib import md5

from email.message import EmailMessage
from email.parser import BytesParser, Parser

from email.policy import default

script_path = str(pathlib.Path(__file__).parent.absolute())
debug = True

# A list of subscribers.
subscriber_list = script_path + "/subs.txt"

# A list of email hashes.
email_list = script_path + "/emails.txt"

# String constants to be interpreted as actions
SUBSCRIBE = "[SUBSCRIBE]"
UNSUBSCRIBE = "[UNSUBSCRIBE]"
DELIMITER = ","

class Email(object):
    def __init__(self, from_, subject, date):
        self.from_ = from_
        self.subject = subject
        self.date = date

    def __hash__(self):
        m = md5()
        m.update(self.__repr__().encode('utf-8'))
        return int.from_bytes(m.digest(), byteorder)

    def __repr__(self):
        return f"{self.subject} from: {self.from_} date: {self.date}"

# Read our email hashes into a set.
def get_email_hashes():
    with open(email_list) as file:
        hashes = {int(line.strip()) for line in file}
    return hashes

# Write our email hashes to a file.
def write_email_hashes(hashes):
     with open(email_list, "w") as file:
        file.writelines(["%s\n" % item for item in hashes])

# Log into the email server and get the `limit` most recent e-mails
def get_emails(limit=40):
    email_user = os.getenv("SH_EMAIL")
    email_pass = os.getenv("SH_PASSWORD")

    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(email_user, email_pass)

    emails = {}

    mail.select("Inbox")
    type_, data = mail.search(None, "ALL")
    to_parse = data[0].split()

    if len(to_parse) > limit:
        to_parse = to_parse[-limit:]

    for num in to_parse:
        typ, data = mail.fetch(num, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode("utf-8")
        headers = Parser(policy=default).parsestr(raw_email_string)
        e = Email(headers["From"], headers["Subject"], headers["Date"])
        emails[hash(e)] = e

    return emails

def process_emails(emails):
    for email in emails:
        if SUBSCRIBE in email.subject:
            target = email.subject.split(DELIMITER)[1]
            print(f"Subscribing {target}")
        elif UNSUBSCRIBE in email.subject:
            target = email.subject.split(DELIMITER)[1]
            print(f"Unsubscribing {target}")

if __name__ == "__main__":
    emails = get_emails()

    # Compare our existing hashes with the incoming new hashes to determine what e-mails are new
    hashes_seen = get_email_hashes()
    hashes_incoming = {e for e in emails.keys()}

    # Removes all elements of hashes_seen from the set hashes_incoming
    hashes_new = hashes_incoming.difference(hashes_seen)
    hashes_total = hashes_incoming.union(hashes_seen)

    emails_new = []
    print(f"{len(hashes_new)} new e-mails")
    for h in hashes_new:
        emails_new.append(emails[h])

    write_email_hashes(hashes_total)
    process_emails(emails_new)
