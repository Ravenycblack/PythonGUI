import sqlite3
import tkinter as tk
from tkinter import messagebox
import csv


conn = sqlite3.connect('customer.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS customers
             (customer_number INTEGER PRIMARY KEY, name TEXT, email TEXT, postcode TEXT, address TEXT)''')
conn.commit()

def load_data_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['fname'] + ' ' + row['ename']
            email = row['epost']
            postcode = row['postnummer']
            address = row['tlf']
            c.execute("INSERT INTO customers (name, email, postcode, address) VALUES (?, ?, ?, ?)",
                      (name, email, postcode, address))
    conn.commit()

csv_file = 'C:/Users/yasch/Downloads/Listeforad.csv'
load_data_from_csv(csv_file)

def search_customer(first_name, last_name):
    name = first_name + ' ' + last_name
    c.execute("SELECT * FROM customers WHERE name=?", (name,))
    customer = c.fetchone()
    if customer:
        show_search_result(customer)
    else:
        messagebox.showinfo("Search Result", "Customer not found.")

def open_create_customer_window():
    create_customer()

def open_delete_customer_window():
    delete_customer()

def show_search_result(customer):
    search_result_window = tk.Toplevel(root)
    search_result_window.title("Search Result")
    search_result_window.configure(bg="black")

    labels = ["Customer Number:", "Name:", "Email:", "Postcode:", "Address:"]
    for i, label_text in enumerate(labels):
        label = tk.Label(search_result_window, text=label_text, bg="black", fg="white")
        label.grid(row=i, column=0, padx=5, pady=5)
        value_label = tk.Label(search_result_window, text=customer[i], bg="black", fg="white")
        value_label.grid(row=i, column=1, padx=5, pady=5)

    button1 = tk.Button(search_result_window, text="Create customer", command=open_create_customer_window, bg="black", fg="white")  # Set button colors
    button1.grid(row=len(labels)+1, column=0, padx=5, pady=5)
    button2 = tk.Button(search_result_window, text="Delete customer", command=open_delete_customer_window, bg="black", fg="white")  # Set button colors
    button2.grid(row=len(labels)+1, column=1, padx=5, pady=5)

def create_customer():
    def save_customer():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        postcode = postcode_entry.get()
        address = address_entry.get()
        name = first_name + ' ' + last_name
        c.execute("INSERT INTO customers (name, email, postcode, address) VALUES (?, ?, ?, ?)",
                  (name, email, postcode, address))
        conn.commit()
        messagebox.showinfo("Success", "Customer created successfully!")
        create_customer_window.destroy()

    create_customer_window = tk.Toplevel(root)
    create_customer_window.title("Create Customer")
    create_customer_window.configure(bg="black")

    tk.Label(create_customer_window, text="First Name:", bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
    first_name_entry = tk.Entry(create_customer_window, bg="black", fg="white")  
    first_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(create_customer_window, text="Last Name:", bg="black", fg="white").grid(row=1, column=0, padx=5, pady=5)
    last_name_entry = tk.Entry(create_customer_window, bg="black", fg="white") 
    last_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(create_customer_window, text="Email:", bg="black", fg="white").grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(create_customer_window, bg="black", fg="white") 
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(create_customer_window, text="Postcode:", bg="black", fg="white").grid(row=3, column=0, padx=5, pady=5)
    postcode_entry = tk.Entry(create_customer_window, bg="black", fg="white") 
    postcode_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(create_customer_window, text="Address:", bg="black", fg="white").grid(row=4, column=0, padx=5, pady=5)
    address_entry = tk.Entry(create_customer_window, bg="black", fg="white") 
    address_entry.grid(row=4, column=1, padx=5, pady=5)

    save_button = tk.Button(create_customer_window, text="Save", command=save_customer, bg="black", fg="white") 
    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

def delete_customer():
    def delete():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        name = first_name + ' ' + last_name
        c.execute("DELETE FROM customers WHERE name=?", (name,))
        conn.commit()
        messagebox.showinfo("Success", "Customer deleted successfully!")
        delete_customer_window.destroy()

    delete_customer_window = tk.Toplevel(root)
    delete_customer_window.title("Delete Customer")
    delete_customer_window.configure(bg="black") 

    tk.Label(delete_customer_window, text="First Name:", bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
    first_name_entry = tk.Entry(delete_customer_window, bg="black", fg="white") 
    first_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(delete_customer_window, text="Last Name:", bg="black", fg="white").grid(row=1, column=0, padx=5, pady=5)
    last_name_entry = tk.Entry(delete_customer_window, bg="black", fg="white")  
    last_name_entry.grid(row=1, column=1, padx=5, pady=5)

    delete_button = tk.Button(delete_customer_window, text="Delete", command=delete, bg="black", fg="white") 
    delete_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

root = tk.Tk()
root.title("Customer Management System")
root.configure(bg="black")  

search_frame = tk.Frame(root, bg="black") 
search_frame.pack(padx=10, pady=10)

tk.Label(search_frame, text="First Name:", bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
first_name_entry = tk.Entry(search_frame, bg="black", fg="white")  
first_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(search_frame, text="Last Name:", bg="black", fg="white").grid(row=1, column=0, padx=5, pady=5)
last_name_entry = tk.Entry(search_frame, bg="black", fg="white")  
last_name_entry.grid(row=1, column=1, padx=5, pady=5)

search_button = tk.Button(search_frame, text="Search", command=lambda: search_customer(first_name_entry.get(), last_name_entry.get()), bg="black", fg="white")
search_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

customer_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Customers", menu=customer_menu)
customer_menu.add_command(label="Create Customer", command=create_customer)
customer_menu.add_command(label="Delete Customer", command=delete_customer)

root.mainloop()

conn.close()


