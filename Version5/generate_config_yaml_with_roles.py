import streamlit_authenticator as stauth
import yaml
from datetime import datetime

# 🔐 Define users with extended metadata
users = {
    "jsdosanjh": {
        "name": "Jagdev Singh Dosanjh",
        "email": "jsdosanjh@example.com",
        "password": "Jsdasr@1973",
        "role": "superadmin",
        "department": "Administration",
        "subject": "Mathematics",
        "access_expires": "2026-12-31",
        "location": "Amritsar"
    },
    "admin": {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "Admin@123",
        "role": "admin",
        "department": "IT",
        "subject": "System Management",
        "access_expires": "2025-12-31",
        "location": "Delhi"
    },
    "teacher": {
        "name": "Math Teacher",
        "email": "teacher@example.com",
        "password": "Teach@2025",
        "role": "teacher",
        "department": "Mathematics",
        "subject": "Algebra",
        "access_expires": "2025-06-30",
        "location": "Ludhiana"
    }
}

# 🔄 Hash passwords
passwords = [user["password"] for user in users.values()]
hashed_passwords = stauth.Hasher(passwords).generate()

# 🧩 Build config dictionary
config = {
    "credentials": {
        "usernames": {}
    }
}

for i, username in enumerate(users):
    user_data = users[username]
    config["credentials"]["usernames"][username] = {
        "name": user_data["name"],
        "email": user_data["email"],
        "password": hashed_passwords[i],
        "role": user_data["role"],
        "department": user_data["department"],
        "subject": user_data["subject"],
        "access_expires": user_data["access_expires"],
        "location": user_data["location"]
    }

# 📝 Save to config.yaml
with open("config.yaml", "w") as file:
    yaml.dump(config, file, sort_keys=False)

print("✅ config.yaml with extended metadata generated successfully!")
