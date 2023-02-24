import streamlit as st
import time
from frontendAPICalls import *

# session state 
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    

st.markdown("<h2 style='text-align: center; color: #C059C0;'> Welcome!</h2>", unsafe_allow_html=True)
st.write('-----')

# Main function
def main():
    
    USERNAME_PATTERN = r"^[a-zA-Z0-9]+$"
    PASSWORD_PATTERN = r"^[a-zA-Z0-9]+$"

    loginColumn, registerColumn = st.columns(2, gap="large")

    st.session_state

    if "login_username_check" not in st.session_state:
        st.session_state.login_username_check = False
        st.session_state.login_password_check = False
        st.session_state.login_success = False
        st.session_state.login_error = False

    if "register_username_check" not in st.session_state:
        st.session_state.register_username_check = False
        st.session_state.register_password_check = False
        st.session_state.register_success = False
        st.session_state.register_error = False

    def handleRegisterUsername():
        username = st.session_state.register_username

        if re.match(USERNAME_PATTERN, username):
            st.session_state.register_username_check = True
        else:
            st.session_state.register_username_check = False

    def handleRegisterPassword():
        password = st.session_state.register_password

        if re.match(PASSWORD_PATTERN, password):
            st.session_state.register_password_check = True
        else:
            st.session_state.register_password_check = False

    def handleRegistration():
        # print('called here')
        if st.session_state.register_password_check and st.session_state.register_username_check:
            response = api_userRegistration(st.session_state.register_username, st.session_state.register_password)
            if response:
                st.session_state.register_username = ""
                st.session_state.register_password = ""
                st.session_state.register_success = True   
                st.session_state.register_error = False             
            else:
                st.session_state.register_username = ""
                st.session_state.register_password = ""
                st.session_state.register_success = False 
                st.session_state.register_error = True


    username = "Username"

    def handleLoginUsername():
        username = st.session_state.login_username

        if re.match(USERNAME_PATTERN, username):
            st.session_state.login_username_check = True
        else:
            st.session_state.login_username_check = False

    def handleLoginPassword():
        password = st.session_state.login_password

        if re.match(PASSWORD_PATTERN, password):
            st.session_state.login_password_check = True
        else:
            st.session_state.login_password_check = False

    def handleLogin():
        if st.session_state.login_password_check and st.session_state.login_username_check:
            response = api_userLogin(st.session_state.login_username, st.session_state.login_password)
            if response['status'] == 200:
                st.session_state.login_username = ""
                st.session_state.login_password = ""
                st.session_state.login_success = response['response']   
                st.session_state.login_error = False   
                # st.session_state.logged_in = response['token']
            else:
                st.session_state.login_username = ""
                st.session_state.login_password = ""
                st.session_state.login_success = False   
                st.session_state.login_error = response['response']
                

    with loginColumn:
        st.header('Login')
        username = st.text_input("Username", key="login_username", on_change=handleLoginUsername)

        if len(username) != 0 and not st.session_state.login_username_check:
            print(st.session_state.login_username_check)
            st.error("Please provide valid username")

        password = st.text_input("Password", type="password", key="login_password", on_change=handleLoginPassword)

        if len(password) != 0 and not st.session_state.login_password_check:
            print(st.session_state.login_password_check)
            st.error("Please provide valid password")

        submit_login = st.button('Login', key="login_btn", on_click=handleLogin )

        if st.session_state.login_success:
            loginSuccess = st.success('Logged in successfully!')
            time.sleep(1)
            loginSuccess.empty()
            st.session_state.logged_in = st.session_state.login_success

        elif st.session_state.login_error:
            loginError = st.error(st.session_state.login_error)
            time.sleep(2)
            loginError.empty()
            st.session_state.login_error = False

    with registerColumn:
        st.header('Register')
        
        username = st.text_input("Username", key="register_username", on_change=handleRegisterUsername)

        if len(username) != 0 and not st.session_state.register_username_check:
            print(st.session_state.register_username_check)
            st.error("Please provide valid username")

        password = st.text_input("Password", type="password", key="register_password", on_change=handleRegisterPassword)

        if len(password) != 0 and not st.session_state.register_password_check:
            print(st.session_state.register_password_check)
            st.error("Please provide valid password")

        submit_register = st.button('Register', key="register_btn", on_click=handleRegistration)

        if st.session_state.register_success:
            registerSuccess = st.success('Registerd successfully! Login with your credentials!')
            time.sleep(3)
            registerSuccess.empty()
            st.session_state.register_success = False
        elif st.session_state.register_error:
            registerError = st.error('User already exists! Login with your credentials!')
            time.sleep(3)
            registerError.empty()
            st.session_state.register_error = False

def afterLoginPage():
    def handleLogout():
        st.session_state.logged_in = False
        st.session_state.login_success = False
    
    st.write('Access the sidebar tabs to navigate to other section!')
    st.button('Logout', on_click=handleLogout)


if __name__ == "__main__":
    def handleLogout():
        st.session_state.logged_in = False
        st.session_state.login_success = False
    if st.session_state.logged_in:
        afterLoginPage()
    else:
        main()