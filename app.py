import streamlit as st
import mysql.connector
from mysql.connector import Error


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Login System",
    page_icon="🔐",
    layout="centered"
)


# --------------------------------------------------
# MYSQL DATABASE CONNECTION
# --------------------------------------------------

def get_connection():
    try:
        conn_obj = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bittu@04051993",
            database="PROJECT_1"
        )

        if conn_obj.is_connected():
            return conn_obj

    except Error as e:
        st.error(f"Database connection error: {e}")

    return None


# --------------------------------------------------
# CUSTOMER SIGN-UP FUNCTION
# --------------------------------------------------

def cust_data_entry_sql_CUSTOMER_DETAILS(
    CUSTOMER_NAME,
    ADDRESS,
    PH_NO,
    user_id,
    password
):

    conn_obj = get_connection()

    if conn_obj is None:
        return False

    cur_obj = conn_obj.cursor()

    sql = """
        INSERT INTO CUST_DETAILS
        (CUSTOMER_NAME, ADDRESS, PH_NO, USER_ID, PASSWORD)
        VALUES (%s, %s, %s, %s, %s)
    """

    data = (
        CUSTOMER_NAME,
        ADDRESS,
        PH_NO,
        user_id,
        password
    )

    try:

        cur_obj.execute(sql, data)

        conn_obj.commit()

        cur_obj.close()
        conn_obj.close()

        return True

    except Error as e:

        conn_obj.rollback()

        cur_obj.close()
        conn_obj.close()

        st.error(f"Error inserting data into MySQL: {e}")

        return False


# --------------------------------------------------
# CUSTOMER LOGIN FUNCTION
# --------------------------------------------------

def customer_login(user_id, password):

    conn_obj = get_connection()

    if conn_obj is None:
        return None

    cur_obj = conn_obj.cursor()

    sql = """
        SELECT CUSTOMER_ID, CUSTOMER_NAME
        FROM CUST_DETAILS
        WHERE USER_ID = %s AND PASSWORD = %s
    """

    data = (user_id, password)

    try:

        cur_obj.execute(sql, data)

        result = cur_obj.fetchone()

        cur_obj.close()
        conn_obj.close()

        return result

    except Error as e:

        st.error(f"Error checking login: {e}")

        cur_obj.close()
        conn_obj.close()

        return None


# --------------------------------------------------
# STREAMLIT APPLICATION
# --------------------------------------------------

st.title("🔐 Customer Authentication System")

st.write("Login or create a new customer account.")


# --------------------------------------------------
# SELECT LOGIN / SIGN UP
# --------------------------------------------------

option = st.radio(
    "Choose an option:",
    ["Login", "Sign Up"],
    horizontal=True
)


# ==================================================
# LOGIN
# ==================================================

if option == "Login":

    st.subheader("🔑 Customer Login")

    user_id = st.text_input(
        "Enter your User ID"
    )

    password = st.text_input(
        "Enter your Password",
        type="password"
    )

    if st.button("Login", type="primary"):

        if user_id == "" or password == "":

            st.warning("Please enter User ID and Password.")

        else:

            result = customer_login(
                user_id,
                password
            )

            if result:

                st.success("Login successful! 🎉")

                st.write(
                    f"**Customer ID:** {result[0]}"
                )

                st.write(
                    f"**Customer Name:** {result[1]}"
                )

            else:

                st.error(
                    "Invalid User ID or Password."
                )


# ==================================================
# SIGN UP
# ==================================================

elif option == "Sign Up":

    st.subheader("📝 Create New Customer Account")

    CUSTOMER_NAME = st.text_input(
        "Enter your full name"
    )

    ADDRESS = st.text_area(
        "Enter your address"
    )

    PH_NO = st.text_input(
        "Enter your phone number"
    )

    user_id = st.text_input(
        "Set your User ID"
    )

    password = st.text_input(
        "Set your Password",
        type="password"
    )

    password2 = st.text_input(
        "Re-enter your Password",
        type="password"
    )


    if st.button("Create Account", type="primary"):

        # ------------------------------------------
        # VALIDATION
        # ------------------------------------------

        if CUSTOMER_NAME == "":
            st.warning("Please enter your name.")

        elif ADDRESS == "":
            st.warning("Please enter your address.")

        elif PH_NO == "":
            st.warning("Please enter your phone number.")

        elif not PH_NO.isnumeric():
            st.error("Phone number must contain only digits.")

        elif len(PH_NO) != 10:
            st.error("Phone number must be exactly 10 digits.")

        elif user_id == "":
            st.warning("Please enter a User ID.")

        elif password == "":
            st.warning("Please enter a password.")

        elif password != password2:

            st.error(
                "Both passwords do not match. Please try again."
            )

        else:

            # Convert name and address to uppercase
            CUSTOMER_NAME = CUSTOMER_NAME.strip().upper()
            ADDRESS = ADDRESS.strip().upper()

            result = cust_data_entry_sql_CUSTOMER_DETAILS(
                CUSTOMER_NAME,
                ADDRESS,
                PH_NO,
                user_id,
                password
            )

            if result:

                st.success(
                    "New account creation successful! 🎉"
                )

                st.info(
                    f"Welcome, {CUSTOMER_NAME}"
                )