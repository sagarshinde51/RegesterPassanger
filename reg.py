import streamlit as st
import mysql.connector
from mysql.connector import Error, IntegrityError
import io

# MySQL database connection details
host = "82.180.143.66"
user = "u263681140_students"
passwd = "testStudents@123"
db_name = "u263681140_students"

# Function to insert data into BusPassangers table
def insert_data_into_buspassangers(name, gender, age, rfid, balance, photo_data):
    try:
        # Establishing connection to the database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Query to insert data into BusPassangers table
        query = """INSERT INTO BusPassangers (Name, Gender, Age, RFID, Balance, photo)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, gender, age, rfid, balance, photo_data))
        
        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success("Registration successful!")
    except Error as e:
        st.error(f"Database error: {e}")
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")

# Streamlit app
st.title("BusPassangers Registration Form")

# Streamlit form for registration
with st.form(key='registration_form'):
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=1, max_value=120)
    rfid = st.text_input("RFID")
    balance = st.number_input("Balance", min_value=0.0, step=0.01)
    
    # Upload photo (either from camera or file)
    photo = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
    if photo is not None:
        st.image(photo, caption="Uploaded Photo", use_column_width=True)

    # Submit button for form
    submit_button = st.form_submit_button(label="Register")

# Handle the form submission
if submit_button:
    if name and gender and age and rfid and balance and photo:
        # Convert image to binary for storage in database
        img_data = photo.read()

        # Insert the data into the BusPassangers table
        insert_data_into_buspassangers(name, gender, age, rfid, balance, img_data)
    else:
        st.warning("Please fill out all fields and upload a photo.")
