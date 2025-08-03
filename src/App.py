"""
# @ Author: FlowDND
# @ Create Time: 2025-08-03 15:26:37
# @ Description: FDRoller is a dice roller for TRPG.
"""

import streamlit as st

# login page


def login_page() -> None:
    st.title("FDRoller Login")
    st.write("Please enter your credentials to log in.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "password":
            st.success("Login successful!")
            # Redirect to the main app or dashboard
            st.session_state.logged_in = True
            pass
        else:
            st.error("Invalid credentials, please try again.")
            pass


# main app page
def main_app_page() -> None:
    st.title("FDRoller Main App")
    st.write("Welcome to FDRoller! You can roll dice here.")

    if st.button("Roll a D20"):
        import random

        result = random.randint(1, 20)
        st.success(f"You rolled a {result}!")
        pass


# main function to run the app
def main() -> None:
    st.set_page_config(page_title="FDRoller", page_icon="🎲")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        main_app_page()
        pass


if __name__ == "__main__":
    main()
    pass
