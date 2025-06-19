import streamlit as st
import pandas as pd
import pyodbc

# Function to connect to SQL Server
def create_connection(server, database, username, password):
    try:
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};DATABASE={database};'
            f'UID={username};PWD={password}'
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        st.error(f"❌ Error connecting to SQL Server: {e}")
        return None

# Function to fetch data from SQL Server
def fetch_data(conn, query):
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return None

# Streamlit UI Elements
st.title("🗃️ SQL Server Connection Example")

server = st.text_input("Server:")
database = st.text_input("Database:")
username = st.text_input("Username:")
password = st.text_input("Password", type="password")

if st.button("Fetch Data"):
    if server and database and username and password:
        conn = create_connection(server, database, username, password)
        if conn:
            st.success("✅ Connected to SQL Server!")

            # Sample SQL query to fetch data (change table name as needed)
            query = "SELECT TOP 10 * FROM DocumentAcquisition.dbo.abbr"
            data = fetch_data(conn, query)

            if data is not None:
                st.write("📄 Retrieved Data:")
                st.dataframe(data)

            conn.close()
    else:
        st.error("⚠️ Please enter all the connection details.")
