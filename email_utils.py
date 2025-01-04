import os 
import configparser
import mailbox
import chromadb
from bs4 import BeautifulSoup
from email.message import EmailMessage
from sentence_transformers import SentenceTransformer 

config = configparser.ConfigParser() 
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()

collection = client.get_or_create_collection("emails")

email_texts = [
    "Hello, this is a test email about meeting schedules.",
    "Your order has been shipped. Check your tracking details.",
    "Reminder: Your appointment is tomorrow at 3 PM."
]

embeddings = mode.encode(email_texts)

collection.add(
        embeddings=embeddings.tolist(),
        documents=email_texts,
        ids=[f"email_{i}" for i in range(len(email_texts))]
        )

query_text = "What categories are these?"
query_embedding = model.encode([query_text])

results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=10
        )

class Email:
    """A representation of an email from a local user inbox."""

    def __init__(self, subject, body, sender):
        self.subject = subject
        self.body = body
        self.sender = sender

def get_profile():
    # Target users Thunderbird profile.
    profile_ini = os.path.expanduser("~/.thunderbird/profiles.ini")

    if not os.path.exists(profile_ini):
        raise FileNotFoundError("Thunderbird profile not found")

    config.read(profile_ini)

    section_name = "Profile0"
    if section_name in config:
        section = config[section_name]
        profile_path = section.get("Path")
        is_relative = section.get("IsRelative", "0") == "1"
        if is_relative:
            profile_path = os.path.join(os.path.expanduser("~/.thunderbird"), profile_path)
        return profile_path
    else:
        raise ValueError(f"Section '{section_name}'")

def get_inbox(profile_folder):
    inbox_paths = []
    for root, dirs, files, in os.walk(profile_folder):
        for file in files:
            if file == "Inbox" and not file.endswith(".msf"):
                inbox_paths.append(os.path.join(root, file))

    if not inbox_paths:
        raise FileNotFoundError("No Thunderbird Inbox file found.")
    return inbox_paths[0]

def extract_body(message):

    if message.is_multipart():
        for part in message.get_payload():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode('utf-8', errors='ignore')
            elif part.get_content_type() == "text/html":
                html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                extracted_content = BeautifulSoup(html_content, "html.parser")
                return extracted_content.get_text(separator="\n").strip()
    else:
        if message.get_content_type() == "text/plain":
            return message.get_payload(decode=True).decode('utf-8', errors='ignore')
        elif message.get_content_type() == "text/html":
            html_content = message.get_payload(decode=True).decode('utf-8', errors='ignore')
            extracted_content = BeautifulSoup(html_content, "html.parser")
            return extracted_content.get_text(separator="\n").strip()


def read_inbox(inbox_path):
    mbox = mailbox.mbox(inbox_path)
    count_num = 0

    for message in mbox:
        count_num += 1
        print(count_num)
        if count_num >= 5:
            break
        print(f"Subject: {message['subject']}")
        print(f"From: {message['from']}")
        print(f"Date: {message['date']}")
        body = extract_body(message)
        print(f"Body: \n{body}\n")
