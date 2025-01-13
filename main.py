from email_model import EmailAssistant


def main():
    assistant = EmailAssistant()
    results = assistant.process_emails()

    for result in results: 
        print(f"\nSubject: {result['subject']}")
        print(f"Category: {result['category']}")
        print(f"Summary: {result['summary']}")

    print("Hello from rag-ai")

if __name__ == "__main__":
    main()
