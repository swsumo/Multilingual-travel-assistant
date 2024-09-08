import streamlit as st
import re

def main():
    st.title("Login/Sign Up")

    # Initialize session state variables
    if 'show_form' not in st.session_state:
        st.session_state.show_form = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:   # Initialize 'page' session state
        st.session_state.page = "login"  # Default to "login" or another initial state

    # Get the query parameters using st.query_params
    query_params = st.query_params

    # Update session state based on query parameters
    if "page" in query_params:
        st.session_state.page = query_params["page"][0]

    # Add a button that redirects to main.py
    if st.button("Site"):
        # Simulate page change by updating the session state
        st.session_state.page = "main"
        # Update the URL without rerunning the script
        st.experimental_set_query_params(page="main")

    # Show content based on session state
    if st.session_state.page == "main":
        if st.session_state.logged_in:
            main_page()
        else:
            st.error("You need to be logged in to access this page.")
    elif st.session_state.page == "signup":
        sign_up()
    elif st.session_state.page == "login":
        login()
    else:
        st.write("Please select an option to log in or sign up.")

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def sign_up():
    st.subheader("Sign Up")

    with st.form(key='signup_form'):
        name = st.text_input("First Name")
        surname = st.text_input("Surname")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        
        submit_button = st.form_submit_button("Sign Up")
        
        if submit_button:
            if not all([name, surname, email, password]):
                st.error("Please fill in all fields.")
            elif not validate_email(email):
                st.error("Invalid email format. Must be @example.com")
            else:
                st.success(f"Signed up successfully with email: {email}")

def login():
    st.subheader("Login")

    with st.form(key='login_form'):
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        
        login_button = st.form_submit_button("Log In")
        
        if login_button:
            if not email or not password:
                st.error("Please enter both email and password.")
            elif not validate_email(email):
                st.error("Invalid email format. Must be @example.com")
            else:
                st.session_state.logged_in = True
                st.session_state.page = "main"
                st.experimental_set_query_params(page="main")
                st.write("You are now logged in. Redirecting...")

def main_page():
    st.write("Welcome to the main page!")

if __name__ == "__main__":
    main()

