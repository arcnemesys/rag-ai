import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from config import ConfigParser

config = ConfigParser()

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
    emails = []
    for message in mbox:
        email_subject = message['subject']
        email_sender = message['from']
        email_body = extract_body(message )
        email = Email()
        email.__init__(email_subject, email_body, email_sender)
        emails.push(email)
        print(f"Subject: {email.subject}")
        print(f"From: {email.sender}")
        # print(f"Date: {message['date']}")
        # body = extract_body(message)
        print(f"Body: \n{email_body}\n")
    return emails

email_profile = get_profile()
email_inbox = get_inbox(email_profile)
email_list = read_inbox(email_inbox)
email_bodies = [email.body for email in email_list]

labels = ["Work", "Updates", "Personal", "Promotions", "Spam"]


def train_classifier(email_texts, labels):
    """
    Train a Naive Bayes classifier using TF-IDF vectorization.
    """
    # Convert text data to TF-IDF features
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(email_texts)
    y = labels

    # Train a Naive Bayes classifier
    model = MultinomialNB()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    # Test model accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")

    return model, vectorizer

def classify_emails(model, vectorizer, new_emails):
    """
    Classify new emails into predefined categories.
    """
    new_X = vectorizer.transform(new_emails)
    predictions = model.predict(new_X)

    # Associate emails with their predicted categories
    email_categories = {email: category for email, category in zip(new_emails, predictions)}
    return email_categories

def query_by_category(email_categories, category):
    """
    Query emails by category.
    """
    return [email for email, cat in email_categories.items() if cat == category]

# Train the classifier
model, vectorizer = train_classifier(email_texts, labels)

# Classify new emails
email_categories = classify_emails(model, vectorizer, new_emails)

# Display the categorized emails
print("\nCategorized Emails:")
for email, category in email_categories.items():
    print(f"Email: '{email}' -> Category: {category}")

# Query emails by category
category_to_query = "Work"
queried_emails = query_by_category(email_categories, category_to_query)
print(f"\nEmails in category '{category_to_query}':")
for email in queried_emails:
    print(f"- {email}")

