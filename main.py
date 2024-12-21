# local message dir: /home/arcnemesys/.thunderbird/ufqe2ut1.default-release/Mail/pop.gmail.com 

from email_utils import get_profile, get_inbox, read_inbox
from app import Lemais
def main():
    try:
        profile_folder = get_profile()
        inbox_path = get_inbox(profile_folder)
        read_inbox(inbox_path)
    except Exception as e:
        print(f"Error : {e}")
    print("Hello from rag-ai")
if __name__ == "__main__":
   app = Lemais()
   app.run()
