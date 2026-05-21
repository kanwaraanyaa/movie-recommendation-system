import streamlit_authenticator as stauth

passwords = ['abc123']

hashed_passwords = stauth.Hasher.hash_passwords(passwords)

print(hashed_passwords)