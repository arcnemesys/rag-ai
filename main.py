# local message dir: /home/arcnemesys/.thunderbird/ufqe2ut1.default-release/Mail/pop.gmail.com 

import os 
import configparser 

def get_profile():
    # Target users Thunderbird profile.
    profile_ini = os.path.expanduser("~/.thunderbird/profiles.ini")

    if not os.path.exists(profile_ini):
        raise FileNotFoundError("Thunderbird profile not found")

    config = configparser.ConfigParser()
    config.read(profile_ini)
    
    # Target user default profile 
    for section in config.sections():
        if config.has_option(section, "Default") and config.get(section, "Default"):
            profile_path = config.get(section, "Path")

            if not profile_path.startswith("/"):
                profile_path = os.path.join(os.path.expanduser("~/.thunderbird"), profile_path)
            return profile_path
    raise RuntimeError("No default Thunderbird profiile found.")

def main():
    try:
        profile_folder = get_profile()
        print(f"Thunderbird profile folder: {profile_folder}")
    except Exception as e:
        print(f"Error : {e}")
    print("Hello from lemai!")


if __name__ == "__main__":
    main()
