import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

class EmailAssistant:
    def __init__(self):
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.embeddings = OpenAIEmbeddings()
        # Initialize empty FAISS store
        self.vector_store = FAISS.from_texts(["initialization"], self.embeddings)
        self.llm = ChatOpenAI(temperature=0)
        
    def connect_to_email(self):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.email, self.password)
        return mail

    def fetch_recent_emails(self, limit=10):
        mail = self.connect_to_email()
        mail.select("inbox")
        _, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()[-limit:]
        
        emails = []
        for email_id in email_ids:
            _, msg = mail.fetch(email_id, "(RFC822)")
            email_body = msg[0][1]
            email_message = email.message_from_bytes(email_body)
            
            subject = decode_header(email_message["subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
                
            body = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = email_message.get_payload(decode=True).decode()
                
            emails.append({"subject": subject, "body": body})
            
        mail.logout()
        return emails

    def categorize_email(self, email_text):
        prompt = PromptTemplate(
            input_variables=["email"],
            template="Categorize this email into one of these categories: Work, Personal, Finance, Shopping, Other.\nEmail: {email}\nCategory:"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(email_text)

    def summarize_email(self, email_text):
        prompt = PromptTemplate(
            input_variables=["email"],
            template="Summarize this email in 2-3 sentences:\n{email}\nSummary:"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(email_text)

    def process_emails(self):
        emails = self.fetch_recent_emails()
        results = []
        
        for email in emails:
            category = self.categorize_email(email["body"])
            summary = self.summarize_email(email["body"])
            
            # Add to FAISS store
            new_store = FAISS.from_texts(
                [email["body"]], 
                self.embeddings, 
                metadatas=[{
                    "subject": email["subject"],
                    "category": category,
                    "summary": summary
                }]
            )
            self.vector_store.merge_from(new_store)
            
            results.append({
                "subject": email["subject"],
                "category": category,
                "summary": summary
            })
        
        # Save the vector store
        self.vector_store.save_local("email_vectors")
        return results
