import requests

BASE_URL = "http://localhost:8000"

def test_chatbot():
    # Test the chatbot endpoint
    response = requests.post(
        f"{BASE_URL}/ask",
        json={"query": "What is the price of MRI scan?"}
    )
    print("Chatbot Response:")
    print(response.json())
    print("\n" + "="*50 + "\n")

def test_admin_endpoints():
    # Test table listing
    tables = requests.get(f"{BASE_URL}/admin/tables").json()
    print("Available Tables:", tables)
    
    # Choose a table to test (using Policy as example)
    test_table = "Policy"
    
    # Test record creation
    new_record = {
        "data": {
            "Name": "Test Policy",
            "Open_Date": "2024-01-01",
            "Policy_Description": "Test policy description"
        }
    }
    create_response = requests.post(
        f"{BASE_URL}/admin/{test_table}",
        json=new_record
    )
    print("Create Response:", create_response.json())
    
    # Get created record ID (assuming SQL Server identity column)
    records = requests.get(f"{BASE_URL}/admin/{test_table}").json()
    record_id = records[-1].get('ID')  # Get last inserted ID
    
    # Test record update
    if record_id:
        updated_data = {
            "data": {
                "Policy_Description": "Updated description"
            }
        }
        update_response = requests.put(
            f"{BASE_URL}/admin/{test_table}/{record_id}",
            json=updated_data
        )
        print("Update Response:", update_response.json())
        
        # Test record deletion
        delete_response = requests.delete(
            f"{BASE_URL}/admin/{test_table}/{record_id}"
        )
        print("Delete Response:", delete_response.json())
    
    print("\n" + "="*50 + "\n")

def test_invalid_requests():
    # Test invalid table
    response = requests.get(f"{BASE_URL}/admin/invalid_table")
    print("Invalid Table Response:", response.status_code, response.json())
    
    # Test invalid record ID
    response = requests.put(
        f"{BASE_URL}/admin/Policy/999999",
        json={"data": {"Name": "Invalid"}}
    )
    print("Invalid ID Response:", response.status_code, response.json())

if __name__ == "__main__":
    # Run tests
    test_chatbot()
    test_admin_endpoints()
    test_invalid_requests()