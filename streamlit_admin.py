# streamlit_admin.py
import streamlit as st
import requests

BASE_URL = "http://localhost:8000/admin"

# Define table structure matching your database schema
TABLES = {
    "Physicians": ["Degree", "Name", "Speciality"],
    "Policy": ["Address", "Landline", "Name", "Open_Date", "Policy_Description"],
    "Pricelist": ["Price__USD_", "Service_Name"],
    "Schedules": ["Doctor_Name", "Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"],
    "Specialities": ["Definition", "Speciality_Name"]
}

def main():
    st.title("🏥 Hospital Database Admin Panel")
    
    # Table selection
    selected_table = st.selectbox("Select Table", list(TABLES.keys()))
    
    if selected_table:
        st.header(f"Manage {selected_table}")
        
        # Display existing records
        records_response = requests.get(f"{BASE_URL}/{selected_table}")
        if records_response.status_code == 200:
            records = records_response.json()
            st.write(f"Existing Records ({len(records)}):")
            if records:
                st.table(records)
            else:
                st.info("No records found")
        else:
            st.error("Error fetching records")
        
        # CRUD Operations
        operation = st.radio("Select Operation", 
                           ["Create", "Update", "Delete"], 
                           horizontal=True)
        
        if operation == "Create":
            with st.form("create_form"):
                st.subheader("Create New Record")
                new_data = {}
                for column in TABLES[selected_table]:
                    new_data[column] = st.text_input(column)
                
                if st.form_submit_button("Create"):
                    response = requests.post(
                        f"{BASE_URL}/{selected_table}",
                        json={"data": new_data}
                    )
                    handle_response(response, "created")
        
        elif operation == "Update":
            st.subheader("Update Existing Record")
            record_id = st.number_input("Record ID", min_value=1)
            
            # Load record
            if st.button("Load Record"):
                record = get_record(selected_table, record_id)
                if record:
                    with st.form("update_form"):
                        updated_data = {}
                        for column in TABLES[selected_table]:
                            updated_data[column] = st.text_input(
                                column, 
                                value=str(record.get(column, "")))
                        
                        if st.form_submit_button("Update"):
                            response = requests.put(
                                f"{BASE_URL}/{selected_table}/{record_id}",
                                json={"data": updated_data}
                            )
                            handle_response(response, "updated")
                else:
                    st.error("Record not found")
        
        elif operation == "Delete":
            st.subheader("Delete Record")
            record_id = st.number_input("Record ID to Delete", min_value=1)
            if st.button("Delete"):
                response = requests.delete(
                    f"{BASE_URL}/{selected_table}/{record_id}"
                )
                handle_response(response, "deleted")

def get_record(table: str, record_id: int):
    response = requests.get(f"{BASE_URL}/{table}")
    if response.status_code == 200:
        records = response.json()
        return next((r for r in records if r.get("ID") == record_id), None)
    return None

def handle_response(response, operation: str):
    if response.status_code == 200:
        st.success(f"Record {operation} successfully!")
        st.rerun()  # Refresh the data
    else:
        st.error(f"Error {operation} record: {response.text}")

if __name__ == "__main__":
    main()