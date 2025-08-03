import streamlit_authenticator as stauth
hashed_pw = stauth.Hasher(["Jsdasr@1973"]).generate()
print(hashed_pw[0])
