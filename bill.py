import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime


order_items = []
tax_rate = 0.1  
discount = 0.0
menu_items = []

def load_menu():
    global menu_items
    menu_items = []
    try:
        with open('menu.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                if len(row) >= 2:
                    menu_items.append({"name": row[0], "price": float(row[1])})
    except FileNotFoundError:
        
        menu_items = [
            {"name": "Burger", "price": 8.99},
            {"name": "Pizza", "price": 12.99},
            {"name": "Salad", "price": 6.99},
            {"name": "Pasta", "price": 10.99},
            {"name": "Soda", "price": 2.99}
        ]
        save_menu()

def save_menu():
    with open('menu.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Item', 'Price'])
        for item in menu_items:
            writer.writerow([item["name"], item["price"]])

def calculate_subtotal():
    subtotal = sum(item["price"] * item["quantity"] for item in order_items)
    return round(subtotal, 2)

def calculate_tax():
    tax = calculate_subtotal() * tax_rate
    return round(tax, 2)

def calculate_total():
    subtotal = calculate_subtotal()
    tax = calculate_tax()
    discount_amount = subtotal * discount
    total = subtotal + tax - discount_amount
    return round(total, 2)

def apply_discount(discount_percentage):
    global discount
    discount = discount_percentage / 100

def generate_bill():
    bill = f"{'='*30}\nTasty Bites Restaurant Bill\n{'='*30}\n"
    bill += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    bill += "Items Ordered:\n"
    for item in order_items:
        bill += f"{item['name']} x{item['quantity']}: ${item['price'] * item['quantity']:.2f}\n"
    bill += f"\nSubtotal: ${calculate_subtotal():.2f}"
    bill += f"\nTax (10%): ${calculate_tax():.2f}"
    if discount > 0:
        bill += f"\nDiscount ({discount*100:.0f}%): -${calculate_subtotal() * discount:.2f}"
    bill += f"\nTotal: ${calculate_total():.2f}\n"
    bill += f"{'='*30}\n"
    return bill

def create_widgets(root, item_var, quantity_var, discount_var, order_listbox, total_label):
    
    tk.Label(root, text="Tasty Bites", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    
    
    tk.Label(root, text="Menu", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    
    menu_frame = tk.Frame(root, bg="#f0f0f0")
    menu_frame.pack(pady=5)
    
    
    item_dropdown = ttk.Combobox(menu_frame, textvariable=item_var, 
                                values=[item["name"] for item in menu_items])
    item_dropdown.grid(row=0, column=0, padx=5)
    
    
    tk.Label(menu_frame, text="Quantity:", bg="#f0f0f0").grid(row=0, column=1, padx=5)
    tk.Entry(menu_frame, textvariable=quantity_var, width=5).grid(row=0, column=2, padx=5)
    
    
    tk.Button(menu_frame, text="Add to Order", 
              command=lambda: add_to_order(item_var, quantity_var, order_listbox, total_label)).grid(row=0, column=3, padx=5)
    
    
    order_listbox.pack(pady=10)
    
    
    tk.Label(root, text="Discount (%):", bg="#f0f0f0").pack()
    tk.Entry(root, textvariable=discount_var, width=10).pack()
    tk.Button(root, text="Apply Discount", 
              command=lambda: apply_discount_handler(discount_var, total_label)).pack(pady=5)
    
    
    total_label.pack(pady=10)
    
    
    tk.Button(root, text="Calculate Total", 
              command=lambda: update_total(total_label)).pack(pady=5)
    tk.Button(root, text="Generate Bill", command=save_bill).pack(pady=5)
    tk.Button(root, text="Clear Order", 
              command=lambda: clear_order(order_listbox, discount_var, total_label)).pack(pady=5)

def add_to_order(item_var, quantity_var, order_listbox, total_label):
    item_name = item_var.get()
    try:
        quantity = int(quantity_var.get())
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        item = next((i for i in menu_items if i["name"] == item_name), None)
        if item:
            order_items.append({"name": item["name"], "price": item["price"], "quantity": quantity})
            order_listbox.insert(tk.END, f"{item['name']} x{quantity}: ${item['price'] * quantity:.2f}")
            update_total(total_label)
        else:
            messagebox.showerror("Error", "Please select a valid menu item")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid quantity")

def apply_discount_handler(discount_var, total_label):
    try:
        discount_percent = float(discount_var.get())
        if 0 <= discount_percent <= 100:
            apply_discount(discount_percent)
            update_total(total_label)
        else:
            messagebox.showerror("Error", "Discount must be sister 0 and 100")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid discount percentage")

def update_total(total_label):
    total = calculate_total()
    total_label.config(text=f"Total: ${total:.2f}")

def save_bill():
    bill = generate_bill()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bill_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(bill)
    messagebox.showinfo("Success", f"Bill saved as {filename}")

def clear_order(order_listbox, discount_var, total_label):
    global order_items, discount
    order_items = []
    discount = 0.0
    order_listbox.delete(0, tk.END)
    discount_var.set("0")
    update_total(total_label)

def main():
    root = tk.Tk()
    root.title("Tasty Bites - Restaurant Order System")
    root.geometry("600x500")
    root.configure(bg="#f0f0f0")  

    load_menu()
    
    
    item_var = tk.StringVar()
    quantity_var = tk.StringVar(value="1")
    discount_var = tk.StringVar(value="0")
    order_listbox = tk.Listbox(root, height=10, width=50)
    total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 12), bg="#f0f0f0")
   
    create_widgets(root, item_var, quantity_var, discount_var, order_listbox, total_label)
    
    root.mainloop()

if __name__ == "__main__":
    main()