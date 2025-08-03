import streamlit_authenticator as stauth
import yaml
import secrets
from datetime import datetime

# 🔐 Define users with extended metadata
users = {
    "jsdosanjh": {
        "name": "Jagdev Singh Dosanjh",
        "email": "jagdevsinghdosanjh@gmail.com",
        "password": "Jsdasr@1973",
        "role": "superadmin",
        "department": "Administration",
        "subject": "Mathematics",
        "access_expires": "2026-12-31",
        "location": "Amritsar"
    },
    "admin": {
        "name": "Admin User",
        "email": "jagdevsinghdosanjh@gmail.com",
        "password": "Admin@123",
        "role": "admin",
        "department": "IT",
        "subject": "System Management",
        "access_expires": "2025-12-31",
        "location": "Delhi"
    },
    "teacher": {
        "name": "Math Teacher",
        "email": "amritkaurdosanjh@gmail.com",
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
    },
    "cookie": {
        "name": "stock_app_session",
        "key": secrets.token_hex(16),  # Secure random key
        "expiry_days": 30
    },
    "preauthorized": {
        "emails": [user["email"] for user in users.values()]
    }
}

# 🧠 Add user metadata
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

print("✅ config.yaml with full metadata and session settings generated successfully!")

# import streamlit_authenticator as stauth
# import yaml

# # 🔐 Define users with roles
# users = {
#     "jsdosanjh": {
#         "name": "Jagdev Singh Dosanjh",
#         "email": "jsdosanjh@example.com",
#         "password": "Jsdasr@1973",
#         "role": "superadmin"
#     },
#     "admin": {
#         "name": "Admin User",
#         "email": "admin@example.com",
#         "password": "Admin@123",
#         "role": "admin"
#     },
#     "teacher": {
#         "name": "Math Teacher",
#         "email": "teacher@example.com",
#         "password": "Teach@2025",
#         "role": "teacher"
#     }
# }

# # 🔄 Hash the passwords
# passwords = [user["password"] for user in users.values()]
# hashed_passwords = stauth.Hasher(passwords).generate()

# # 🧩 Build the config dictionary
# config = {
#     "credentials": {
#         "usernames": {}
#     }
# }

# for i, username in enumerate(users):
#     config["credentials"]["usernames"][username] = {
#         "name": users[username]["name"],
#         "email": users[username]["email"],
#         "password": hashed_passwords[i],
#         "role": users[username]["role"]
#     }

# # 📝 Save to config.yaml
# with open("config.yaml", "w") as file:
#     yaml.dump(config, file, sort_keys=False)

# print("✅ config.yaml with roles generated successfully!")

# # import streamlit_authenticator as stauth
# # import yaml

# # # 🔐 Define your users and plaintext passwords
# # users = {
# #     "jsdosanjh": {
# #         "name": "Jagdev Singh Dosanjh",
# #         "email": "jsdosanjh@example.com",
# #         "password": "Jsdasr@1973"
# #     },
# #     "admin": {
# #         "name": "Admin User",
# #         "email": "admin@example.com",
# #         "password": "Admin@123"
# #     },
# #     "teacher": {
# #         "name": "Math Teacher",
# #         "email": "teacher@example.com",
# #         "password": "Teach@2025"
# #     }
# # }

# # # 🔄 Hash the passwords
# # passwords = [user["password"] for user in users.values()]
# # hashed_passwords = stauth.Hasher(passwords).generate()

# # # 🧩 Build the config dictionary
# # config = {
# #     "credentials": {
# #         "usernames": {}
# #     }
# # }

# # for i, username in enumerate(users):
# #     config["credentials"]["usernames"][username] = {
# #         "name": users[username]["name"],
# #         "email": users[username]["email"],
# #         "password": hashed_passwords[i]
# #     }

# # # 📝 Save to config.yaml
# # with open("config.yaml", "w") as file:
# #     yaml.dump(config, file, sort_keys=False)

# # print("✅ config.yaml generated successfully!")
