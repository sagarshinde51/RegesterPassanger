import streamlit as st
import mysql.connector  # Using mysql.connector
from mysql.connector import Error, IntegrityError  # For handling MySQL exceptions

# MySQL database connection details
host = "82.180.143.66"
user = "u263681140_students"
passwd = "testStudents@123"
db_name = "u263681140_students"

# Function to create a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Function to create table if it doesn't exist
def create_table_if_not_exists():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bot (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """)
        conn.commit()
        conn.close()

# Function to insert user data into the bot table
def insert_user_data(name, email, password):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO bot (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, password))
            conn.commit()
            conn.close()
            return True
        except mysql.connector.IntegrityError as e:
            st.error(f"Error inserting data: Integrity issue (likely a duplicate email): {e}")
            conn.close()
            return False
        except Error as e:
            st.error(f"Error inserting data: Operational error: {e}")
            conn.close()
            return False
    return False

# Streamlit UI with Sidebar
def main():
    # Create the table if it doesn't exist
    create_table_if_not_exists()

    st.title("User Registration")

    # Sidebar content
    with st.sidebar:
        st.header("Register New User")
        
        # User inputs for registration form in the sidebar
        name = st.text_input("Enter your name:")
        email = st.text_input("Enter your email:")
        password = st.text_input("Enter your password:", type="password")

        if st.button("Register"):
            if name and email and password:
                success = insert_user_data(name, email, password)
                if success:
                    st.success("User registered successfully!")
                else:
                    st.error("Registration failed. Try again.")
            else:
                st.warning("Please fill in all fields!")

    # Main content
    st.write("""
        ## Welcome to the User Registration Page
        
        Use the form on the left to register a new user. Your details will be stored in our database.
        
        Make sure your email is unique! If you have any questions or issues, feel free to contact support.
    """)

if __name__ == "__main__":
    main()
