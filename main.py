import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key - The json file is obtained by going to 
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "learndb-51e07-firebase-adminsdk-wc3d4-5d434a2fa8.json"

    # Use the application default credentials.  The projectID is obtianed 
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'learndb-51e07',
    })

    # Get reference to database
    db = firestore.client()
    return db

def add_new_user(db):
    
    # Prompt the user for a new item to add to the users database.  The
    # item name must be unique (firestore document id).

    username = input("Choose your username.(It has to be Unique): ")
    firstName = input("First Name: ")
    lastName = input("Last Name: ")
    dateOfBirth = input("Date of birth: ")

    # Check for an already existing item by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("users").document(username).get()
    if result.exists:
      print("This user already exist")
      return

    # Build a dictionary to hold the contents of the firestore document.
    data = {"firstName": firstName , "lastName:": lastName, "dateOfBirth:": dateOfBirth}
    db.collection("users").document(username).set(data)

    # Save this in the log collection in Firestore       
    # log_transaction(db, f"Added {name} with initial quantity {qty}")

def Update_user(db):
    '''
    Prompt the user to add quantity to an already existing item in the
    inventory database.  
    '''

    userName = input("User to update: ")


    # Check for an already existing item by the same name.
    # The document ID must be unique in Firestore.
    check = db.collection("users").document(userName).get()
    if check.exists:
        firstName = input("New First Name: ")
        lastName = input("New Last Name: ")
        dateOfBirth = input("New Date of birth: ")
        data = {"firstName": firstName , "lastName": lastName, "dateOfBirth": dateOfBirth}
        db.collection("users").document(userName).set(data)
        return
    else:
        print("The user dose not exist!")

    # Save this in the log collection in Firestore
    # log_transaction(db, f"Added {add_qty} {name}")

def search_user(db):
    '''
    Search the database in multiple ways.
    '''

    print("Select Query")
    print("1) Show All users")        
    print("2) Show users with missing info")
    choice = input("> ")
    print()

    # Build and execute the query based on the request made
    if choice == "1":
        results = db.collection("users").get()
    elif choice == "2":
        results = db.collection("users").where("firstName", "==" , "").where("lastNmae", "==", "").where("dateOfBirth", "==", "").get()
    elif choice == "3":
        results = None
    else:
        print("Invalid Selection")
        return
    
    # Display all the results from any of the queries
    print("")
    print("Search Results")
    print(f"{'userNmae':<20}  {'firstName':<10}  {'lastName':<10}  {'dateOfBirth':<10}")
    for result in results:
      data = result.to_dict()
      print(f"{result.id:<20}  {data['firstName']:<10}  {data['lastName']:<10}  {data['dateOfBirth']:<10}")
    print() 

def main():
    db = initialize_firestore()
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) Add New user")
        print("2) Update existing user")
        print("3) Search user")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_new_user(db)
        elif choice == "2":
            Update_user(db)
        elif choice == "3":
            search_user(db)    

if __name__ == "__main__":
    main()