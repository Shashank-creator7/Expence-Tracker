import streamlit as st
import pandas as pd
import datetime
import os
import csv
import matplotlib.pyplot as plt
import time
# from pydrive2.auth import ServiceAccountCredentials
# from pydrive2.drive import GoogleDrive

# gauth = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", ["https://www.googleapis.com/auth/drive"])
# drive = GoogleDrive(gauth)

# Ensure files exist with proper headers
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

menu = ["Login", "Signup"]

choice = st.sidebar.selectbox("Menu", menu )

if choice == "Login":
    if not st.session_state["logged_in"]:
        st.subheader("Login")
        username = st.text_input("Username", key = "login_username")
        password = st.text_input("Password", type= "password", key= "login_password")

        if st.button("Login"):
            found = False
            with open ("accounts.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Username"] == username and row["Password"] == password:
                        found = True
                        break
            if found:
                st.session_state["logged_in"] = True
                st.success("Login Successfully")
                
                countdown = st.empty()
                for i in range(3, 0, -1):
                    countdown.info(f'Logging in {i} seconds')
                    time.sleep(1)
                countdown.empty()
                st.rerun()
            else:
                if username and password:
                    st.error("Invalid Credintial")

if st.session_state["logged_in"]:
    # if not os.path.exists("expenses.csv"):
    #     pd.DataFrame(columns=["Amount", "Category", "Note", "Date"]).to_csv("expenses.csv",     index=False)

    st.title("💰 Personal Expense Tracker")

    # Sidebar for Navigation
    menu = ["View Expenses", "Add Expense", "View Budget", "Add Money to Budget", "See Budget Entries"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View Expenses":
        st.subheader("Your Expenses")
        expenses_df = pd.read_csv("expenses.csv")

        if not expenses_df.empty:
            expenses_df["Category"] = expenses_df["Category"].str.strip().str.capitalize()
            st.dataframe(expenses_df) # Displays an interactive table

            total = expenses_df["Amount"].sum()
            st.metric(label="Total Expenses", value=f"₹{total}")
        else:
            st.info("No expenses recorded yet!")


        col1, col2, col3 = st.columns([1,2,1])

        with col3:  # center horizontally
            # Create a container with vertical spacing
            with st.container():
                st.write("----------------------------")   # vertical gap
                # st.write("")   # more gap
                if st.button("View Budget"):
                    if os.path.exists("budget.csv"):

                        budget_df = pd.read_csv("budget.csv", header=None)
                        budget = budget_df.iloc[:, 0].sum()
                        st.metric(label="Total Budget", value=f'₹{float(budget)}')
                    else:
                        budget_df = pd.read_csv("sample_budget.csv", header=None)
                        budget = budget_df.iloc[:, 0].sum()
                        st.metric(label="Total Budget", value=f'₹{float(budget)}')
                        

        # col1, col2 = st.columns([2,1])
        with st.container():
            with col2:  # left column ---->(change to col1 for left alignment)
                grouped = expenses_df.groupby("Category")["Amount"].sum().reset_index()

                categories = grouped["Category"]
                values = grouped["Amount"]
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig)


    elif choice == "Add Expense":
        st.subheader("Add a New Expense")
        rows = []
        # Form layout
        amount = st.number_input("Enter Amount", min_value=0.0, step=10.0)
        category = st.selectbox("Category", ["Food", "Travel", "Self-Care", "Bills", "Other"])
        note = st.text_input("Note (Optional)")

        if st.button("Submit Expense"):
            if os.path.exists("expenses.csv"):
                with open ("expenses.csv", "a", newline="") as file:
                    fieldnames = ["Amount", "Category", "Note", "Date"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)

                    if file.tell() == 0:
                        writer.writeheader()
                    writer.writerow({"Amount": amount, "Category": category, 'Note': note, 'Date':  datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")} )
            else:
                with open ("sample_expenses.csv", "a", newline="") as file:
                    fieldnames = ["Amount", "Category", "Note", "Date"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)

                    if file.tell() == 0:
                        writer.writeheader()
                    writer.writerow({"Amount": amount, "Category": category, 'Note': note, 'Date':  datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")} )
            if os.path.exists("budget.csv"):
                with open ("budget.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            if float(row[0]) < amount:
                                print("You are out of the budget. Add money in the")
                            old_amount = float(row[0])
                            new = old_amount - amount
                            row[0]= str(new)
                        rows.append(row)
            else:
                with open ("sample_budget.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            if float(row[0]) < amount:
                                print("You are out of the budget. Add money in the")
                            old_amount = float(row[0])
                            new = old_amount - amount
                            row[0]= str(new)
                        rows.append(row)
            if os.path.exists("budget.csv"):
                with open("budget.csv", "w", newline="") as file:

                    writer = csv.writer(file)
                    writer.writerows(rows)
                st.success(f"Successfully added ₹{amount} to {category}!")
            else:
                with open("sample_budget.csv", "w", newline="") as file:

                    writer = csv.writer(file)
                    writer.writerows(rows)
                st.success(f"Successfully added ₹{amount} to {category}!")

    elif choice == 'View Budget':
        st.subheader("See your budget")
        if os.path.exists("budget.csv"):
            df = pd.read_csv("budget.csv", header=None) #file with no header
            budget = df.iloc[:, 0].sum() 
            st.metric(label="Total Budget", value=f'₹{float(budget)}')
        else:
            df = pd.read_csv("sample_budget.csv", header=None) #file with no header
            budget = df.iloc[:, 0].sum() 
            st.metric(label="Total Budget", value=f'₹{float(budget)}')

    elif choice == 'Add Money to Budget':
        st.subheader("Budget Entries")
        df2 = pd.read_csv("budgetentry.csv")
        if not df2.empty:
            st.dataframe(df2)
        else:
            st.info("No budget entries recorded yet!")
        st.subheader("Add Money to Budget")
        amount =st.number_input("Enter amount", min_value = 0.0, step = 10.0)
        if st.button("Add amount"):
            rows = []
            if os.path.exists("budgetentry.csv"):
                with open ("budget.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            old_amount = float(row[0])
                            new = old_amount + amount
                            row[0] = str(new)
                        rows.append(row)
            else:
                with open ("budget.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            old_amount = float(row[0])
                            new = old_amount + amount
                            row[0] = str(new)
                        rows.append(row)


            if not rows:
                rows = [[str(amount)]]
            if os.path.exists("budget.csv"):

                with open ("budget.csv", "w", newline ="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
            else:
                with open ("sample_budget.csv", "w", newline ="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
            if os.path.exists("budgetentry.csv"):
                with open("budgetentry.csv", "a" , newline="")as file:
                    writer = csv.DictWriter(file, fieldnames=["Amount", "Date"])
                    if file.tell() == 0:
                        writer.writeheader()
                    writer.writerow({'Amount':amount, 'Date': datetime.datetime.now().strftime  ("%Y-%m-%d %H:%M:%S")})
                st.success(f'Successfully added ₹{amount} to your budget!')

                st.subheader("Budget Entries")
            else:
                with open("sample_budgetentry.csv", "a" , newline="")as file:
                    writer = csv.DictWriter(file, fieldnames=["Amount", "Date"])
                    if file.tell() == 0:
                        writer.writeheader()
                    writer.writerow({'Amount':amount, 'Date': datetime.datetime.now().strftime  ("%Y-%m-%d %H:%M:%S")})
                st.success(f'Successfully added ₹{amount} to your budget!')

                st.subheader("Budget Entries")
            
    elif choice == ("See Budget Entries"):
        st.subheader("Budget Entries")
        if os.path.exists("budgetentry.csv"):
            df2 = pd.read_csv("budgetentry.csv")
            if not df2.empty:
                st.dataframe(df2)
            else:
                st.info("No budget entries recorded yet!")
        else:
            df2 = pd.read_csv("sample_budgetentry.csv")
            if not df2.empty:
                st.dataframe(df2)
            else:
                st.info("No budget entries recorded yet!")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()           

if choice == "Signup":
    
    st.subheader("Signup")
    username = st.text_input("Enter username :" )
    if len(username)>0:

        with open ("accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            existing_username = [row["Username"] for row in reader]
            if username not in existing_username:
                password = st.text_input("Enter password:")
                if len(password)>0:
                    if st.button("Signup"):
                        with open("accounts.csv", "a", newline="") as file:
                            fieldnames= ["Username", "Password"]
                            writer = csv.DictWriter(file, fieldnames=fieldnames)
                            if file.tell == 0:
                                writer.writeheader()

                            writer.writerow({"Username":username, "Password":password})
                            st.success("Signup Successfully")
                else:
                    st.info("Password must contain charecters")
            else:
                st.info("Username already exists")
                
    #         for row in reader:
    #             # existing_username = [row["Username"] for row in reader]
    #             if userid != row['Username']:
    #                 password = st.text_input("Enter password :")
    #                 if len(password)>0:
            
    #                     if st.button("Signup"):
    #                         with open("accounts.csv", "a", newline="") as file:
    #                             fieldnames = ["Username", "Password"]
    #                             writer = csv.DictWriter(file, fieldnames=fieldnames)

    #                             if file.tell() == 0:  # write header if file is empty
    #                                 writer.writeheader()

    #                             writer.writerow({"Username": userid, "Password": password})
                                
    #                             st.success("Signup Successfully")
    #                 else:
    #                     st.info("Write Password")        
    #             else:
    #                 st.error("Username already exists, try different username.")
    #                 break

    #     # if username in existing_username:
    #     #     st.info("Username already exist, try another username")
    #     #     username = False         
        
        
       
                
    # else:
    #     st.info("Write Username")