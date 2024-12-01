import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# File to store contacts
DETAILS_FILE = "details.json"

def load_contacts():
    """Load contacts from the file."""
    if os.path.exists(DETAILS_FILE):
        try:
            with open(DETAILS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

def save_contacts(contacts):
    """Save contacts to the file."""
    with open(DETAILS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

def add_contact():
    """Add a new contact."""
    name = simpledialog.askstring("Add Contact", "Enter name:")
    if not name:
        return
    if name in contacts:
        messagebox.showerror("Error", "Contact already exists.")
        return
    
    phone = simpledialog.askstring("Add Contact", "Enter phone number:")
    email = simpledialog.askstring("Add Contact", "Enter email address:")
    if not phone or not email:
        messagebox.showerror("Error", "Phone number and email are required.")
        return
    
    contacts[name] = {"phone": phone, "email": email}
    save_contacts(contacts)
    update_contact_list()
    messagebox.showinfo("Success", "Contact added successfully.")

def view_contact():
    """View the selected contact."""
    selected = contact_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No contact selected.")
        return
    
    name = contact_listbox.get(selected)
    contact = contacts[name]
    messagebox.showinfo("Contact Details", f"Name: {name}\nPhone: {contact['phone']}\nEmail: {contact['email']}")

def edit_contact():
    """Edit the selected contact."""
    selected = contact_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No contact selected.")
        return
    
    name = contact_listbox.get(selected)
    phone = simpledialog.askstring("Edit Contact", "Enter new phone number (leave blank to keep current):", initialvalue=contacts[name]["phone"])
    email = simpledialog.askstring("Edit Contact", "Enter new email address (leave blank to keep current):", initialvalue=contacts[name]["email"])
    
    if phone:
        contacts[name]["phone"] = phone
    if email:
        contacts[name]["email"] = email
    
    save_contacts(contacts)
    update_contact_list()
    messagebox.showinfo("Success", "Contact updated successfully.")

def delete_contact():
    """Delete the selected contact."""
    selected = contact_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No contact selected.")
        return
    
    name = contact_listbox.get(selected)
    if messagebox.askyesno("Delete Contact", f"Are you sure you want to delete {name}?"):
        del contacts[name]
        save_contacts(contacts)
        update_contact_list()
        messagebox.showinfo("Success", "Contact deleted successfully.")

def update_contact_list():
    """Update the listbox with current contacts."""
    contact_listbox.delete(0, tk.END)
    for name in contacts:
        contact_listbox.insert(tk.END, name)

# Load existing contacts
contacts = load_contacts()

# Create the main Tkinter window
root = tk.Tk()
root.title("Contact Management System")

# Create the listbox to display contacts
contact_listbox = tk.Listbox(root, width=50, height=20)
contact_listbox.pack(padx=10, pady=10)

# Create buttons for actions
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

add_button = tk.Button(button_frame, text="Add Contact", command=add_contact)
add_button.grid(row=0, column=0, padx=5, pady=5)

view_button = tk.Button(button_frame, text="View Contact", command=view_contact)
view_button.grid(row=0, column=1, padx=5, pady=5)

edit_button = tk.Button(button_frame, text="Edit Contact", command=edit_contact)
edit_button.grid(row=0, column=2, padx=5, pady=5)

delete_button = tk.Button(button_frame, text="Delete Contact", command=delete_contact)
delete_button.grid(row=0, column=3, padx=5, pady=5)

# Populate the listbox with initial data
update_contact_list()

# Start the Tkinter event loop
root.mainloop()
