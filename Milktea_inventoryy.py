from tkinter import Tk, Button, Entry, Frame, Label, Listbox, Canvas, StringVar, LEFT, RIGHT, CENTER, END, Toplevel
from tkinter import ttk, messagebox, font
import tkinter
from PIL import ImageTk, Image
import mysql.connector
import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
from mysql.connector import Error

def connect_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin123",
            port=3305,
            database="milktea"
        )
        cursor = conn.cursor()
        return cursor, conn
    except Error as e:
        print(f"❌ Error connecting to the database: {e}")
        return None, None


def fetch_dashboard_data():
    cursor, conn = connect_database()
    if not cursor or not conn:
        return 0, 0, 0, 0

    try:
        # Total Sales
        cursor.execute("""
            SELECT IFNULL(SUM(price * quantity), 0)
            FROM product_sales
            WHERE DATE(order_date) = CURDATE()
        """)
        total_sales = cursor.fetchone()[0]

        # Expenses
        cursor.execute("""
            SELECT IFNULL(SUM(price * quantity), 0)
            FROM inventory
            WHERE DATE(created_at) = CURDATE()
        """)

        total_expenses = cursor.fetchone()[0]

        # Net Profit
        net_profit = total_sales - total_expenses

        # Total Orders
        cursor.execute("""
            SELECT COUNT(*) FROM product_sales
            WHERE DATE(order_date) = CURDATE()
        """)
        total_orders = cursor.fetchone()[0]

    except Error as err:
        print("❌ Query error:", err)
        total_sales, total_expenses, net_profit, total_orders = 0, 0, 0, 0

    finally:
        conn.close()

    return total_orders, total_sales, total_expenses, net_profit

def animate_bar(canvas, label_text, x, y, target_width, bar_color, value_text):
    BAR_HEIGHT = 60
    steps = 60
    delay = 10

    def draw_frame(step):
        current_width = int((step / steps) * target_width)
        canvas.delete(f"{label_text}_bar")

        canvas.create_text(20, y + BAR_HEIGHT / 2, text=label_text, anchor="w",
                           font=("Arial", 30, "bold"), fill="black", tags=f"{label_text}_bar")

        canvas.create_rectangle(x, y, x + current_width, y + BAR_HEIGHT,
                                fill=bar_color, outline="", tags=f"{label_text}_bar")

        value_x = x + current_width / 2
        canvas.create_text(value_x, y + BAR_HEIGHT / 2,
                           text=value_text, fill="white", font=("Arial", 30, "bold"), tags=f"{label_text}_bar")

        if step < steps:
            canvas.after(delay, lambda: draw_frame(step + 1))

    draw_frame(0)



# --------------- Main Application Window ---------------
root = Tk()
root.geometry('1920x1080+0+0')
root.resizable(0, 0)
root.title('Milktea Inventory')
root.config(bg='white')


selected_inventory_id = None

# Fonts
title_font = font.Font(family="Georgia", size=22, weight="bold")
stat_font = font.Font(family="Arial", size=14)

# ---------- Load Images (Update file paths as needed) ----------
icon_Label_img = Image.open(r"C:\Users\glycel\Downloads\inventoryy.png")
icon_Label_resized = icon_Label_img.resize((70, 70), Image.Resampling.LANCZOS)
icon_Label = ImageTk.PhotoImage(icon_Label_resized)

logoImage_img = Image.open(r"C:\Users\glycel\Downloads\Sulasok.png")
logoImage_resized = logoImage_img.resize((450, 400), Image.Resampling.LANCZOS)
logoImage = ImageTk.PhotoImage(logoImage_resized)
imageLabel = Label(image=logoImage)
imageLabel.place(x=0, y=640)

log_icon_img = Image.open(r"C:\Users\glycel\Downloads\logout.png")
log_icon_resized = log_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
log_icon = ImageTk.PhotoImage(log_icon_resized)

Sign_icon_img = Image.open(r"C:\Users\glycel\Downloads\Sign-in.png")
Sign_icon_resized = Sign_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
Sign_icon = ImageTk.PhotoImage(Sign_icon_resized)

dash_icon_img = Image.open(r"C:\Users\glycel\Downloads\dashboard.png")
dash_icon_resized = dash_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
dash_icon = ImageTk.PhotoImage(dash_icon_resized)

inv_icon_img = Image.open(r"C:\Users\glycel\Downloads\inventory.png")
inv_icon_resized = inv_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
inv_icon = ImageTk.PhotoImage(inv_icon_resized)

productm_icon_img = Image.open(r"C:\Users\glycel\Downloads\productm.png")
productm_icon_resized = productm_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
productm_icon = ImageTk.PhotoImage(productm_icon_resized)

supplier_icon_img = Image.open(r"C:\Users\glycel\Downloads\supplier.png")
supplier_icon_resized = supplier_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
supplier_icon = ImageTk.PhotoImage(supplier_icon_resized)

bell_icon_img = Image.open(r"C:\Users\glycel\Downloads\bell.png")
bell_icon_resized = bell_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
bell_icon = ImageTk.PhotoImage(bell_icon_resized)

userm_icon_img = Image.open(r"C:\Users\glycel\Downloads\userm.png")
userm_icon_resized = userm_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
userm_icon = ImageTk.PhotoImage(userm_icon_resized)

# Header Labels
Label1 = Label(root, image=icon_Label, compound=LEFT, text="Milktea Inventory", font=('Helvetica', 13, 'bold'),
               bg='#1e405d', fg='White', padx=90, pady=13.4, anchor='nw')
Label1.place(x=0, y=0)

Label2 = Label(root, bg='#244d6f', anchor='c', padx=900, pady=40)
Label2.place(x=450, y=0)




def dashboard():
    try:
        dashboard_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
        dashboard_frame.place(x=450, y=100)

        headlabel = Label(dashboard_frame, text="Dashboard", font=('times new roman', 20, 'bold'),
                          bg='#7aabd4', fg='black', padx=680, pady=15)
        headlabel.place(x=0, y=0)

        # Undo Button
        undo_icon_img = Image.open(r"C:\Users\glycel\Downloads\undo.png")
        undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
        undo_icon = ImageTk.PhotoImage(undo_icon_resized)
        undolabel = Button(dashboard_frame, image=undo_icon, compound=RIGHT, borderwidth=0,
                           bg='#7aabd4', cursor='hand2', command=lambda: dashboard_frame.place_forget())
        undolabel.place(x=5, y=2)
        undolabel.image = undo_icon

        # Fetch data
        orders, total_sales, total_expenses, profit = fetch_dashboard_data()

        # Total Sales
        sales_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
        sales_box.place(x=100, y=100)
        Label(sales_box, text="Total Sales", font=("Arial", 28), bg="white", fg="#666").pack()
        Label(sales_box, text=f"₱{total_sales:,.0f}", font=("Arial", 32, "bold"), bg="white", fg="#333").pack()

        # Expenses
        expenses_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
        expenses_box.place(x=400, y=100)
        Label(expenses_box, text="Expenses Today", font=("Arial", 28), bg="white", fg="#666").pack()
        Label(expenses_box, text=f"₱{total_expenses:,.0f}", font=("Arial", 32, "bold"), bg="white", fg="#333").pack()

        # Orders
        orders_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
        orders_box.place(x=780, y=100)
        Label(orders_box, text="Orders Today", font=("Arial", 28), bg="white", fg="#666").pack()
        Label(orders_box, text=str(orders), font=("Arial", 32, "bold"), bg="white", fg="#333").pack()

        # Net Profit
        netprofit_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
        netprofit_box.place(x=1100, y=100)
        Label(netprofit_box, text="Net Profit", font=("Arial", 28), bg="white", fg="#666").pack()
        Label(netprofit_box, text=f"₱{profit:,.0f}", font=("Arial", 32, "bold"), bg="white", fg="green").pack()

        # Chart Canvas
        chart_canvas = Canvas(dashboard_frame, width=1200, height=250, bg='white')
        chart_canvas.place(x=100, y=300)

        max_val = max(total_sales, total_expenses)
        if max_val == 0:
            max_val = 1

        BAR_MAX_WIDTH = 360
        sales_width = int((total_sales / max_val) * BAR_MAX_WIDTH)
        expenses_width = int((total_expenses / max_val) * BAR_MAX_WIDTH)

        animate_bar(chart_canvas, "Total Sales", x=300, y=50, target_width=sales_width,
                    bar_color="green", value_text=f"₱{total_sales:,.0f}")
        animate_bar(chart_canvas, "Expenses", x=300, y=130, target_width=expenses_width,
                    bar_color="red", value_text=f"₱{total_expenses:,.0f}")

    except Exception as e:
        print(f"❌ Dashboard loading failed: {e}")

# ------------------ INVENTORY ------------------

def inventory():
    global inv_treeview, item_name_entry, quantity_entry, category_entry, price_entry
    global unit_combobox, expiry_entry, best_before_entry, nutrition_entry, supplier_combobox, supplier_dict
    global inventory_frame

    inventory_frame = Frame(root, width=1470, height=1000, bg='#f0f0f0')
    inventory_frame.place(x=450, y=100)

    # Header label
    headlabel = Label(inventory_frame, text="Inventory Management", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    # Undo Button (optional)
    try:
        undo_icon_img = Image.open(r"C:\Users\glycel\Downloads\undo.png")
        undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
        undo_icon = ImageTk.PhotoImage(undo_icon_resized)

        undolabel = Button(inventory_frame, image=undo_icon, compound=RIGHT, borderwidth=0, bg='#7aabd4',
                           cursor='hand2', command=lambda: inventory_frame.place_forget())
        undolabel.place(x=5, y=2)
        undolabel.image = undo_icon
    except Exception as e:
        print("Undo icon load failed:", e)

    # Treeview Frame
    tree_frame = Frame(inventory_frame, bg='white')
    tree_frame.place(x=50, y=80, width=1350, height=500)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="white", foreground="black", rowheight=30,
                    fieldbackground="white", borderwidth=2, relief="solid")
    style.configure("Treeview.Heading",
                    background="lightblue", foreground="black", font=('Times New Roman', 13, 'bold'))
    style.map("Treeview",
              background=[('selected', 'yellow')],
              foreground=[('selected', 'black')])

    inv_treeview = ttk.Treeview(tree_frame,
        columns=('ItemID', 'Name', 'Qty', 'Unit', 'Category', 'Price', 'ExpiryDate', 'BestBeforeDate', 'Nutrition', 'Supplier'),
        show='headings')

    # Define columns
    inv_treeview.heading('ItemID', text='ItemID')
    inv_treeview.heading('Name', text='Item Name')
    inv_treeview.heading('Qty', text='Quantity')
    inv_treeview.heading('Unit', text='Unit')
    inv_treeview.heading('Category', text='Category')
    inv_treeview.heading('Price', text='Price')
    inv_treeview.heading('ExpiryDate', text='Expiry Date')
    inv_treeview.heading('BestBeforeDate', text='Best Before')
    inv_treeview.heading('Nutrition', text='Nutrition Info')
    inv_treeview.heading('Supplier', text='Supplier')

    inv_treeview.column('ItemID', width=80)
    inv_treeview.column('Name', width=200)
    inv_treeview.column('Qty', width=100)
    inv_treeview.column('Unit', width=100)
    inv_treeview.column('Category', width=150)
    inv_treeview.column('Price', width=100)
    inv_treeview.column('ExpiryDate', width=120)
    inv_treeview.column('BestBeforeDate', width=120)
    inv_treeview.column('Nutrition', width=200)
    inv_treeview.column('Supplier', width=150)

    inv_treeview.pack(fill='both', expand=True)
    inv_treeview.tag_configure('evenrow', background='white')
    inv_treeview.tag_configure('oddrow', background='#f0f0f0')
    inv_treeview.bind('<<TreeviewSelect>>', fill_inventory_fields)

    # Entry frame for inputs and buttons
    entry_frame = Frame(inventory_frame, bg='#f0f0f0')
    entry_frame.place(x=40, y=600)

    # Input fields
    Label(entry_frame, text='Item Name:', font=('times new roman', 17)).grid(row=0, column=0, padx=10, pady=10)
    item_name_entry = Entry(entry_frame, font=('times new roman', 17), width=20)
    item_name_entry.grid(row=0, column=1, padx=10)

    Label(entry_frame, text='Quantity:', font=('times new roman', 17)).grid(row=0, column=2, padx=10, pady=10)
    quantity_entry = Entry(entry_frame, font=('times new roman', 17), width=20)
    quantity_entry.grid(row=0, column=3, padx=10)

    Label(entry_frame, text='Unit:', font=('times new roman', 17)).grid(row=0, column=4, padx=10, pady=10)
    unit_combobox = ttk.Combobox(entry_frame, font=('times new roman', 17),
                                  values=['pcs','kg'], state='readonly', width=10)
    unit_combobox.grid(row=0, column=5, padx=10)
    unit_combobox.set("pcs")

    Label(entry_frame, text='Category:', font=('times new roman', 17)).grid(row=1, column=0, padx=10, pady=10)
    category_entry = Entry(entry_frame, font=('times new roman', 17), width=20)
    category_entry.grid(row=1, column=1, padx=10)

    Label(entry_frame, text='Expiry Date (YYYY-MM-DD):', font=('times new roman', 17)).grid(row=1, column=2, padx=10, pady=10, sticky='e')
    expiry_entry = Entry(entry_frame, font=('times new roman', 17), width=20)
    expiry_entry.grid(row=1, column=3, padx=10)

    Label(entry_frame, text='Price:', font=('times new roman', 17)).grid(row=2, column=0, padx=10, pady=10)
    price_entry = Entry(entry_frame, font=('times new roman', 17), width=20)
    price_entry.grid(row=2, column=1, padx=10)

    Label(entry_frame, text='Best Before (YYYY-MM-DD):', font=('times new roman', 17)).grid(row=2, column=2, padx=10, pady=10, sticky='e')
    best_before_entry = Entry(entry_frame, font=('times new roman', 17), width=20)
    best_before_entry.grid(row=2, column=3, padx=10)

    Label(entry_frame, text='Nutrition Info:', font=('times new roman', 17)).grid(row=3, column=0, padx=10, pady=10, sticky='ne')
    nutrition_entry = Entry(entry_frame, font=('times new roman', 17), width=20)
    nutrition_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky='w')

    Label(entry_frame, text='Supplier:', font=('times new roman', 17)).grid(row=4, column=0, padx=10, pady=10)
    supplier_combobox = ttk.Combobox(entry_frame, font=('times new roman', 17), width=20, state='readonly')
    supplier_combobox.grid(row=4, column=1, padx=10)

    # Buttons
    Button(entry_frame, text="Add", font=('times new roman', 17), bg="#0b8fcb", fg='black',
           command=add_inventory).grid(row=1, column=5, padx=5, pady=(5, 0), sticky='ew')

    Button(entry_frame, text="Update", font=('times new roman', 17), bg="#0b8fcb", fg='black',
           command=update_inventory).grid(row=2, column=5, padx=5, pady=(5, 0), sticky='ew')

    Button(entry_frame, text="Clear", font=('times new roman', 17), bg="#0b8fcb", fg='black',
           command=clear_inventory_fields).grid(row=3, column=5, padx=5, pady=(5, 0), sticky='ew')

    Button(entry_frame, text="Delete", font=('times new roman', 17), bg="red", fg='black',
           command=delete_inventory).grid(row=4, column=5, padx=5, pady=(5, 10), sticky='ew')

    supplier_dict = {}
    load_supplier_names()
    load_inventory_data()


def load_supplier_names():
    cursor, conn = connect_database()
    if cursor:
        cursor.execute("SELECT id, name FROM suppliers")
        suppliers = cursor.fetchall()
        # Format: "Supplier Name (ID:123)"
        supplier_combobox['values'] = [f"{name} (ID:{sid})" for sid, name in suppliers]
        supplier_dict.clear()
        for sid, name in suppliers:
            supplier_dict[f"{name} (ID:{sid})"] = sid
        conn.close()

def is_valid_date_format(date_str):
    """Validates if the date string is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def add_inventory():
    item = item_name_entry.get()
    quantity = quantity_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    unit = unit_combobox.get()
    expiry = expiry_entry.get()
    best_before = best_before_entry.get()
    nutrition = nutrition_entry.get()
    supplier_name = supplier_combobox.get()
    supplier_id = supplier_dict.get(supplier_name)

    if not is_valid_date_format(expiry) and expiry:  # Allow empty strings
        messagebox.showerror("Error", "Invalid Expiry Date format. Use YYYY-MM-DD.")
        return
    if not is_valid_date_format(best_before) and best_before:  # Allow empty strings
        messagebox.showerror("Error", "Invalid Best Before Date format. Use YYYY-MM-DD.")
        return

    cursor, conn = connect_database()
    if cursor:
        cursor.execute("""
            INSERT INTO inventory (item_name, quantity, unit, category, price, expiry_date, best_before_date, nutrition_info, supplier_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (item, quantity, unit, category, price, expiry, best_before, nutrition, supplier_id))
        conn.commit()
        conn.close()
        load_inventory_data()
        clear_inventory_fields()
        messagebox.showinfo("Success", "Item added successfully.")
        add_notification(f"Item '{item}' was added to inventory.", 'info')




def update_inventory():
    global selected_inventory_id
    selected = inv_treeview.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an item to update.")
        return

    item_id = inv_treeview.item(selected[0])['values'][0]
    item = item_name_entry.get()
    quantity = quantity_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    unit = unit_combobox.get()
    expiry = expiry_entry.get()
    best_before = best_before_entry.get()
    nutrition = nutrition_entry.get()
    supplier_name = supplier_combobox.get()
    supplier_id = supplier_dict.get(supplier_name)

    if not is_valid_date_format(expiry) and expiry:  # Allow empty strings
        messagebox.showerror("Error", "Invalid Expiry Date format. Use YYYY-MM-DD.")
        return
    if not is_valid_date_format(best_before) and best_before:  # Allow empty strings
        messagebox.showerror("Error", "Invalid Best Before Date format. Use YYYY-MM-DD.")
        return

    cursor, conn = connect_database()
    if cursor:
        cursor.execute("""
            UPDATE inventory
            SET item_name=%s, quantity=%s, unit=%s, category=%s, price=%s,
                expiry_date=%s, best_before_date=%s, nutrition_info=%s, supplier_id=%s
            WHERE item_id=%s
        """, (item, quantity, unit, category, price, expiry, best_before, nutrition, supplier_id, item_id))
        conn.commit()
        conn.close()
        load_inventory_data()
        clear_inventory_fields()
        messagebox.showinfo("Success", "Item updated successfully.")
        add_notification(f"Item '{item}' was updated in inventory.", 'info')




def delete_inventory():
    global selected_inventory_id
    selected = inv_treeview.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an item to delete.")
        return

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this item?")
    if not confirm:
        return

    item_id = inv_treeview.item(selected[0])['values'][0]

    cursor, conn = connect_database()
    if cursor:
        cursor.execute("DELETE FROM inventory WHERE item_id = %s", (item_id,))
        conn.commit()
        conn.close()
        load_inventory_data()
        clear_inventory_fields()
        messagebox.showinfo("Success", "Item deleted successfully.")
        add_notification(f"Item with ID {item_id} was deleted from inventory.", 'info')



def clear_inventory_fields():
    for widget in [item_name_entry, quantity_entry, category_entry, price_entry,
                   expiry_entry, best_before_entry, nutrition_entry]:
        widget.delete(0, END)
    unit_combobox.set("pcs")
    supplier_combobox.set("")


def fill_inventory_fields(event):
    global selected_inventory_id
    selected = inv_treeview.selection()
    if not selected:
        return
    values = inv_treeview.item(selected[0])['values']

    item_name_entry.delete(0, END)
    item_name_entry.insert(0, values[1])

    quantity_entry.delete(0, END)
    quantity_entry.insert(0, values[2])

    unit_combobox.set(values[3])

    category_entry.delete(0, END)
    category_entry.insert(0, values[4])

    price_entry.delete(0, END)
    price_entry.insert(0, values[5])

    expiry_entry.delete(0, END)
    expiry_entry.insert(0, values[6])

    best_before_entry.delete(0, END)
    best_before_entry.insert(0, values[7])

    nutrition_entry.delete(0, END)
    nutrition_entry.insert(0, values[8])

    # supplier name from DB is only the name, but combobox values have format "Name (ID:xxx)"
    supplier_name = values[9] or ""
    # find the full display string in supplier_dict keys with matching supplier name
    for key in supplier_dict.keys():
        if supplier_name in key:
            supplier_combobox.set(key)
            break
    else:
        supplier_combobox.set("")


def load_inventory_data():
    for item in inv_treeview.get_children():
        inv_treeview.delete(item)

    cursor, conn = connect_database()
    if cursor:
        cursor.execute("""
            SELECT i.item_id, i.item_name, i.quantity, i.unit, i.category, i.price,
                   i.expiry_date, i.best_before_date, i.nutrition_info, s.name
            FROM inventory i
            LEFT JOIN suppliers s ON i.supplier_id = s.id
        """)
        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            inv_treeview.insert('', 'end', values=row, tags=(tag,))
        conn.close()

# ------------------ PRODUCT MANAGEMENT ------------------
selected_product_id = None
def product_management():
    global product_treeview, product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry
    product_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    product_frame.place(x=450, y=100)

    # Header
    headlabel = Label(product_frame, text="Product Management", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    # Undo Button
    undo_icon_img = Image.open(r"C:\Users\glycel\Downloads\undo.png")
    undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    undolabel = Button(product_frame, image=undo_icon, compound=RIGHT, borderwidth=0,
                       bg='#7aabd4', cursor='hand2', command=lambda: product_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    # === Product Table (Top) ===
    tree_frame = Frame(product_frame, bg='white')
    tree_frame.place(x=50, y=80, width=1350, height=500)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="white",
                    borderwidth=2,
                    relief="solid")

    style.configure("Treeview.Heading",
                    background="lightblue",
                    foreground="black",
                    font=('Times New Roman', 13, 'bold'))

    style.map("Treeview",
              background=[('selected', 'yellow')],
              foreground=[('selected', 'black')])

    product_treeview = ttk.Treeview(tree_frame, columns=('ProductID', 'Product', 'Customers', 'Price', 'Quantity', 'Category', 'OrderDate'), show='headings')
    product_treeview.heading('ProductID', text='ProductID')
    product_treeview.heading('Product', text='Product Name')
    product_treeview.heading('Customers', text='Customers Count')
    product_treeview.heading('Price', text='Price')
    product_treeview.heading('Quantity', text='Quantity')
    product_treeview.heading('Category', text='Category')
    product_treeview.heading('OrderDate', text='Order Date')

    product_treeview.column('ProductID', width=100)
    product_treeview.column('Product', width=200)
    product_treeview.column('Customers', width=150)
    product_treeview.column('Price', width=100)
    product_treeview.column('Quantity', width=100)
    product_treeview.column('Category', width=150)
    product_treeview.column('OrderDate', width=150)

    product_treeview.pack(fill='both', expand=True)
    product_treeview.bind('<<TreeviewSelect>>', fill_product_fields)

    load_product_data()

    # === Entry Fields (Below Table) ===
    entry_frame = Frame(product_frame, bg='#f0f0f0')
    entry_frame.place(x=40, y=600)

    # Row 0
    Label(entry_frame, text='Product Name:', font=('times new roman', 20)).grid(row=0, column=0, padx=10, pady=10)
    product_name_entry = Entry(entry_frame, font=('times new roman', 20), width=20)
    product_name_entry.grid(row=0, column=1, padx=10)

    Label(entry_frame, text='Customers Count:', font=('times new roman', 20)).grid(row=0, column=2, padx=10, pady=10)
    customers_entry = Entry(entry_frame, font=('times new roman', 20), width=20)
    customers_entry.grid(row=0, column=3, padx=10)

   
    Button(entry_frame, text="Add", font=('times new roman', 20), bg='#0b8fcb', fg='black', width=10,
       command=add_product).grid(row=0, column=4, padx=10, pady=5)

    Button(entry_frame, text="Update", font=('times new roman', 20), bg='#0b8fcb', fg='black', width=10,
        command=update_product).grid(row=1, column=4, padx=10, pady=5)

    Button(entry_frame, text="Clear", font=('times new roman', 20), bg='#0b8fcb', fg='black', width=10,
        command=clear_product_fields).grid(row=2, column=4, padx=10, pady=5)

    Button(entry_frame, text="Delete", font=('times new roman', 20), bg='red', fg='black', width=10,
        command=delete_product).grid(row=3, column=4, padx=10, pady=5)




    # Row 1
    Label(entry_frame, text='Price:', font=('times new roman', 20)).grid(row=1, column=0, padx=10, pady=10)
    price_entry = Entry(entry_frame, font=('times new roman', 20), width=20)
    price_entry.grid(row=1, column=1, padx=10)

    Label(entry_frame, text='Quantity:', font=('times new roman', 20)).grid(row=1, column=2, padx=10, pady=10)
    quantity_entry = Entry(entry_frame, font=('times new roman', 20), width=20)
    quantity_entry.grid(row=1, column=3, padx=10)

    # Row 2
    Label(entry_frame, text='Category:', font=('times new roman', 20)).grid(row=2, column=0, padx=10, pady=10)
    product_category_entry = Entry(entry_frame, font=('times new roman', 20), width=20)
    product_category_entry.grid(row=2, column=1, padx=10)

    Label(entry_frame, text='Order Date (YYYY-MM-DD):', font=('times new roman', 20)).grid(row=2, column=2, padx=10, pady=10)
    order_date_entry = Entry(entry_frame, font=('times new roman', 20), width=20)
    order_date_entry.grid(row=2, column=3, padx=10)




def add_product():
    global product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry, product_treeview
    product = product_name_entry.get()
    customers = customers_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    category = product_category_entry.get()
    order_date = order_date_entry.get()
    if product and customers and price and quantity and category and order_date:
        cursor, conn = connect_database()
        if cursor:
            try:
                cursor.execute("""
                    INSERT INTO product_sales (product_name, customers_count, price, quantity, category, order_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (product, customers, price, quantity, category, order_date))
                conn.commit()
                messagebox.showinfo("Success", "Product added successfully!")
                add_notification(f"Product added: {product}", notif_type='info')
                load_product_data()
                clear_product_fields()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")


def load_product_data():
    global product_treeview
    cursor, conn = connect_database()
    if cursor:
        cursor.execute("SELECT id, product_name, customers_count, price, quantity, category, order_date FROM product_sales")
        rows = cursor.fetchall()
        product_treeview.delete(*product_treeview.get_children())

        # Define row tag styles
        product_treeview.tag_configure('oddrow', background='#f0f0f0')  
        product_treeview.tag_configure('evenrow', background='white')    

        for index, row in enumerate(rows):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            product_treeview.insert('', 'end', values=row, tags=(tag,))

        conn.close()



def update_product():
    global selected_product_id
    if not selected_product_id:
        messagebox.showwarning("Warning", "Select a product to update.")
        return

    new_product = product_name_entry.get()
    new_customers = customers_entry.get()
    new_price = price_entry.get()
    new_quantity = quantity_entry.get()
    new_category = product_category_entry.get()
    new_order_date = order_date_entry.get()

    if not new_product or not new_customers or not new_price or not new_quantity or not new_category or not new_order_date:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("""
                UPDATE product_sales 
                SET product_name=%s, customers_count=%s, price=%s, quantity=%s, category=%s, order_date=%s 
                WHERE id=%s
            """, (new_product, new_customers, new_price, new_quantity, new_category, new_order_date, selected_product_id))
            conn.commit()
            messagebox.showinfo("Success", "Product updated successfully!")
            add_notification(f"Product updated: {new_product}", notif_type='info')
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to update product: {e}")
        finally:
            conn.close()

        load_product_data()
        clear_product_fields()
        selected_product_id = None



def delete_product():
    global selected_product_id
    if not selected_product_id:
        messagebox.showwarning("Warning", "Select a product to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
    if not confirm:
        return

    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("DELETE FROM product_sales WHERE id = %s", (selected_product_id,))
            conn.commit()
            messagebox.showinfo("Deleted", "Product has been deleted.")
            add_notification("Product deleted.", notif_type='info')
            load_product_data()
            clear_product_fields()
            selected_product_id = None
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()



def clear_product_fields():
    global product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry
    product_name_entry.delete(0, END)
    customers_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    product_category_entry.delete(0, END)
    order_date_entry.delete(0, END)


def fill_product_fields(event):
    global product_treeview, product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry, selected_product_id
    selected = product_treeview.focus()
    if selected:
        values = product_treeview.item(selected, 'values')
        if values:
            selected_product_id = values[0]  # First value is ProductID

            product_name_entry.delete(0, END)
            product_name_entry.insert(0, values[1])
            customers_entry.delete(0, END)
            customers_entry.insert(0, values[2])
            price_entry.delete(0, END)
            price_entry.insert(0, values[3])
            quantity_entry.delete(0, END)
            quantity_entry.insert(0, values[4])
            product_category_entry.delete(0, END)
            product_category_entry.insert(0, values[5])
            order_date_entry.delete(0, END)
            order_date_entry.insert(0, values[6])




# ------------------ SUPPLIER MANAGEMENT ------------------
def supplier():
    global supplier_treeview, name_entry_supp, contact_entry_supp, address_entry_supp, email_entry_supp, product_entry_supp

    supplier_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    supplier_frame.place(x=450, y=100)

    # Header
    headlabel = Label(supplier_frame, text="Supplier Management", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    # Undo Button
    undo_icon = Image.open(r"C:\Users\glycel\Downloads\undo.png")
    undo_icon_resized = undo_icon.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    undolabel = Button(supplier_frame, image=undo_icon, borderwidth=0, bg='#7aabd4', cursor='hand2',
                       command=lambda: supplier_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    # === Supplier Table (Top) ===
    tree_frame = Frame(supplier_frame)
    tree_frame.place(x=50, y=80, width=1350, height=500)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="white",
                    borderwidth=2,
                    relief="solid")
    style.configure("Treeview.Heading",
                    background="lightblue",
                    foreground="black",
                    font=('Times New Roman', 13, 'bold'))
    style.map("Treeview",
              background=[('selected', 'yellow')],
              foreground=[('selected', 'black')])

    supplier_treeview = ttk.Treeview(tree_frame, columns=('SupplierID', 'Name', 'Contact', 'Email', 'Address', 'Product'), show='headings')
    supplier_treeview.tag_configure('evenrow', background='white')
    supplier_treeview.tag_configure('oddrow', background='#f0f0f0')


    
    supplier_treeview.column('SupplierID', width=100)
    supplier_treeview.heading('Name', text='Name')
    supplier_treeview.heading('Contact', text='Contact')
    supplier_treeview.heading('Email', text='Email')
    supplier_treeview.heading('Address', text='Address')
    supplier_treeview.heading('Product', text='Product')

    supplier_treeview.heading('SupplierID', text='SupplierID')
    supplier_treeview.column('Name', width=200)
    supplier_treeview.column('Contact', width=150)
    supplier_treeview.column('Email', width=250)
    supplier_treeview.column('Address', width=300)
    supplier_treeview.column('Product', width=200)

    supplier_treeview.pack(fill='both', expand=True)
    supplier_treeview.bind('<<TreeviewSelect>>', fill_supplier_fields)
    load_supplier_data()

    # === Data Entry Fields (Below Table) ===
    entry_frame = Frame(supplier_frame, bg='#f0f0f0')
    entry_frame.place(x=40, y=600)

    Label(entry_frame, text='Name:', font=('times new roman', 20)).grid(row=0, column=0, padx=10, pady=10)
    name_entry_supp = Entry(entry_frame, font=('times new roman', 20), width=20)
    name_entry_supp.grid(row=0, column=1, padx=10)

    Label(entry_frame, text='Contact:', font=('times new roman', 20)).grid(row=0, column=2, padx=10, pady=10)
    contact_entry_supp = Entry(entry_frame, font=('times new roman', 20), width=20)
    contact_entry_supp.grid(row=0, column=3, padx=10)

    # Buttons aligned vertically next to "Contact" with rectangular shape
    # Buttons aligned vertically next to "Contact" with thin rectangular shape
    Button(entry_frame, text="Add", font=('times new roman', 20), bg='#0b8fcb', fg='black', width=10,
        command=add_supplier).grid(row=0, column=4, padx=10, pady=5)

    Button(entry_frame, text="Update", font=('times new roman', 20), bg='#0b8fcb', fg='black', width=10,
        command=update_supplier).grid(row=1, column=4, padx=10, pady=5)

    Button(entry_frame, text="Clear", font=('times new roman', 20), bg='#0b8fcb', fg='black', width=10,
        command=clear_supplier_fields).grid(row=2, column=4, padx=10, pady=5)

    Button(entry_frame, text="Delete", font=('times new roman', 20), bg='red', fg='black', width=10,
        command=delete_supplier).grid(row=3, column=4, padx=10, pady=5)


    Label(entry_frame, text='Email:', font=('times new roman', 20)).grid(row=1, column=0, padx=10, pady=10)
    email_entry_supp = Entry(entry_frame, font=('times new roman', 20), width=20)
    email_entry_supp.grid(row=1, column=1, padx=10)

    Label(entry_frame, text='Address:', font=('times new roman', 20)).grid(row=1, column=2, padx=10, pady=10)
    address_entry_supp = Entry(entry_frame, font=('times new roman', 20), width=20)
    address_entry_supp.grid(row=1, column=3, padx=10)

    Label(entry_frame, text='Product:', font=('times new roman', 20)).grid(row=2, column=0, padx=10, pady=10)
    product_entry_supp = Entry(entry_frame, font=('times new roman', 20), width=20)  # font size changed to 17 here too
    product_entry_supp.grid(row=2, column=1, padx=10)



def add_supplier():
    name = name_entry_supp.get()
    contact = contact_entry_supp.get()
    email = email_entry_supp.get()
    address = address_entry_supp.get()
    product = product_entry_supp.get()
    if not name or not contact or not email or not address or not product:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("INSERT INTO suppliers (name, contact, email, address, product) VALUES (%s, %s, %s, %s, %s)",
                           (name, contact, email, address, product))
            conn.commit()
            messagebox.showinfo("Success", "Supplier added successfully!")
            add_notification(f"Added supplier '{name}'.", notif_type='info')
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()


def update_supplier():
    selected = supplier_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a supplier to update.")
        return

    new_name = name_entry_supp.get()
    new_contact = contact_entry_supp.get()
    new_email = email_entry_supp.get()
    new_address = address_entry_supp.get()
    new_product = product_entry_supp.get()

    if not new_name or not new_contact or not new_email or not new_address or not new_product:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("""
                UPDATE suppliers SET name = %s, contact = %s, email = %s, address = %s, product = %s
                WHERE id = %s
            """, (new_name, new_contact, new_email, new_address, new_product, selected_supplier_id))
            conn.commit()
            messagebox.showinfo("Success", "Supplier updated successfully!")
            add_notification(f"Updated supplier ID {selected_supplier_id}.", notif_type='info')
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()



def delete_supplier():
    selected = supplier_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a supplier to delete.")
        return

    values = supplier_treeview.item(selected, 'values')
    supplier_id = values[0]
    supplier_name = values[1]
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{supplier_name}'?")
    if not confirm:
        return

    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("DELETE FROM suppliers WHERE id = %s", (supplier_id,))
            conn.commit()
            messagebox.showinfo("Deleted", f"{supplier_name} has been deleted.")
            add_notification(f"Deleted supplier '{supplier_name}'.", notif_type='info')
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()



def load_supplier_data():
    cursor, conn = connect_database()
    if cursor:
        try:
            supplier_treeview.delete(*supplier_treeview.get_children())
            cursor.execute("SELECT id, name, contact, email, address, product FROM suppliers")
            rows = cursor.fetchall()
            for index, row in enumerate(rows):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                supplier_treeview.insert('', 'end', values=row, tags=(tag,))
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to load supplier data: {e}")
        finally:
            conn.close()


def clear_supplier_fields():
    name_entry_supp.delete(0, 'end')
    contact_entry_supp.delete(0, 'end')
    email_entry_supp.delete(0, 'end')
    address_entry_supp.delete(0, 'end')
    product_entry_supp.delete(0, 'end')


def fill_supplier_fields(event):
    global selected_supplier_id
    selected = supplier_treeview.focus()
    if selected:
        values = supplier_treeview.item(selected, 'values')
        if values:
            selected_supplier_id = values[0]  # Store the ID
            name_entry_supp.delete(0, 'end')
            name_entry_supp.insert(0, values[1])
            contact_entry_supp.delete(0, 'end')
            contact_entry_supp.insert(0, values[2])
            email_entry_supp.delete(0, 'end')
            email_entry_supp.insert(0, values[3])
            address_entry_supp.delete(0, 'end')
            address_entry_supp.insert(0, values[4])
            product_entry_supp.delete(0, 'end')
            product_entry_supp.insert(0, values[5])




# ------------------ NOTIFICATIONS ------------------
def notification_df():
    notification_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    notification_frame.place(x=450, y=100)
    

    headlabel = Label(notification_frame, text="Notifications", font=('times new roman', 20, 'bold'), bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    undo_pil = Image.open(r"C:\Users\glycel\Downloads\undo.png").resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_pil)

    # Save a reference to avoid garbage collection
    notification_frame.undo_icon = undo_icon

    Button(notification_frame, image=undo_icon, borderwidth=0, bg='#7aabd4',
        command=lambda: notification_frame.place_forget()).place(x=5, y=2)


    notif_container = Frame(notification_frame, bg='#f0f0f0')
    notif_container.place(x=50, y=80, width=1300, height=780)

    canvas = tkinter.Canvas(notif_container, bg='#f0f0f0', highlightthickness=0)
    scrollbar = ttk.Scrollbar(notif_container, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    frame_inside = Frame(canvas, bg='#f0f0f0')
    canvas.create_window((0, 0), window=frame_inside, anchor='nw')
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    notifications = load_notifications()
    colors = {'info': '#dff0d8', 'warning': '#fcf8e3', 'error': '#f2dede'}

    for message, created_at, notif_type in notifications:
        color = colors.get(notif_type, '#dff0d8')
        notif_box = Frame(frame_inside, bg=color, bd=1, relief='solid', padx=10, pady=5)
        notif_box.pack(anchor='w', pady=5, fill='x', padx=5)

        timestamp = created_at.strftime('%b %d, %Y - %I:%M %p')
        Label(notif_box, text=timestamp, font=('times new roman', 11, 'italic'), bg=color).pack(anchor='w')
        Label(notif_box, text=message, font=('times new roman', 13), bg=color, wraplength=1200, justify='left').pack(anchor='w')


def add_notification(message, notif_type='info'):
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("INSERT INTO notifications (message, type) VALUES (%s, %s)", (message, notif_type))
            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Notification Error", f"Failed to log notification: {e}")
        finally:
            conn.close()


def load_notifications():
    cursor, conn = connect_database()
    notifications = []
    if cursor:
        try:
            cursor.execute("SELECT message, created_at, type FROM notifications ORDER BY created_at DESC")
            notifications = cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Notification Error", f"Failed to load notifications: {e}")
        finally:
            conn.close()
    return notifications



def usermanage():
    global back_image, employee_treeview
    global name_entry, email_entry, contact_entry, age_entry, address_entry, gender_entry
    
    # Load and resize undo icon
    try:
        undo_icon = Image.open(r"C:\Users\glycel\Downloads\undo.png")
        undo_icon_resized = undo_icon.resize((30, 30), Image.Resampling.LANCZOS)
        undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    except:
        undo_icon = None
    
    # Create main frame with adjusted positioning - moved more to bottom right
    usermanage_frame = Frame(root, width=1470, height=1000, bg='white')
    usermanage_frame.place(x=450, y=100)
    
    # Header (50px height)
    headlabel6 = Label(usermanage_frame, text="Employee Management", 
                      font=('times new roman', 20, 'bold'), 
                      bg='#7aabd4', fg='black', height=2, padx=680, pady=5)
    headlabel6.place(x=0, y=0,)
    
    # Undo button
    if undo_icon:
        undolabel = Button(usermanage_frame, image=undo_icon, 
                          compound=RIGHT, borderwidth=0, bg='#7aabd4', 
                          cursor='hand2', 
                          command=lambda: usermanage_frame.place_forget())
        undolabel.place(x=5, y=10)
        undolabel.image = undo_icon
    
    # Search Frame (40px height)
    search_frame = Frame(usermanage_frame, bg='white', height=60)
    search_frame.place(x=0, y=100, width=1500, height=60)  # Increased width for better layout

    Label(search_frame, text="Search:", font=('times new roman', 20), bg='white').place(x=20, y=15)

    search_combobox = ttk.Combobox(search_frame, 
                                values=('Name', 'Email', 'Contact', 'Gender', 'Address', 'Age'), 
                                font=('times new roman', 22), 
                                state='readonly', width=15)
    search_combobox.set('Name')
    search_combobox.place(x=130, y=15)

    search_entry = Entry(search_frame, font=('times new roman', 22), width=50)
    search_entry.place(x=320, y=15)

    search_button = Button(search_frame, text='Search', 
                        font=('times new roman', 22), 
                        bg='#0b8fcb', fg='white',
                        padx=10, pady=2,
                        command=lambda: search_employee(search_combobox.get(), search_entry.get()))
    search_button.place(x=1100, y=12)

    clear_search_button = Button(search_frame, text='Show All', 
                                font=('times new roman', 22), 
                                bg='#6c757d', fg='white',
                                padx=10, pady=2,
                                command=treeview_data)
    clear_search_button.place(x=1250, y=12)

    
    # Treeview Frame (280px height)
    tree_frame = Frame(usermanage_frame, bg='white',)
    tree_frame.place(x=50, y=200, width=1350, height=450)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="white",
                    borderwidth=2,
                    relief="solid")
    style.configure("Treeview.Heading",
                    background="lightblue",
                    foreground="black",
                    font=('Times New Roman', 13, 'bold'))
    style.map("Treeview",
              background=[('selected', 'yellow')],
              foreground=[('selected', 'black')])
    
    # Scrollbars
    tree_scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
    tree_scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
    
    # Treeview
    employee_treeview = ttk.Treeview(tree_frame, 
                                   columns=('ID', 'Name', 'Email', 'Contact', 'Age', 'Address', 'Gender'),
                                   show='headings',
                                   yscrollcommand=tree_scroll_y.set,
                                   xscrollcommand=tree_scroll_x.set,
                                   height=12)
    
    tree_scroll_y.config(command=employee_treeview.yview)
    tree_scroll_x.config(command=employee_treeview.xview)
    
    
    tree_scroll_y.pack(side=RIGHT, fill=Y)
    tree_scroll_x.pack(side=BOTTOM, fill=X)

    employee_treeview.tag_configure('oddrow', background='#f0f0f0')   # Light gray
    employee_treeview.tag_configure('evenrow', background='white')   # White
    employee_treeview.pack(fill=BOTH, expand=True)
    
    # Configure columns
    employee_treeview.heading('ID', text='ID')
    employee_treeview.heading('Name', text='Name')
    employee_treeview.heading('Email', text='Email')
    employee_treeview.heading('Contact', text='Contact')
    employee_treeview.heading('Age', text='Age')
    employee_treeview.heading('Address', text='Address')
    employee_treeview.heading('Gender', text='Gender')
    
    employee_treeview.column('ID', width=40, anchor=CENTER)
    employee_treeview.column('Name', width=120, anchor=W)
    employee_treeview.column('Email', width=150, anchor=W)
    employee_treeview.column('Contact', width=100, anchor=CENTER)
    employee_treeview.column('Age', width=50, anchor=CENTER)
    employee_treeview.column('Address', width=180, anchor=W)
    employee_treeview.column('Gender', width=70, anchor=CENTER)
    
    # Details Frame (170px height)
    detail_frame = LabelFrame(usermanage_frame, text="Employee Details", 
                             font=('times new roman', 20, 'bold'), 
                             bg='white', fg='black')
    detail_frame.place(x=20, y=670, width=1400, height=250)
    
    
    Label(detail_frame, text='Name:', font=('times new roman', 20), bg='white').place(x=20, y=25)
    name_entry = Entry(detail_frame, font=('times new roman', 20), width=25)
    name_entry.place(x=140, y=25)

    Label(detail_frame, text='Age:', font=('times new roman', 20), bg='white').place(x=480, y=25)
    age_entry = Entry(detail_frame, font=('times new roman', 20), width=20)
    age_entry.place(x=580, y=25)

    # === Row 2 ===
    Label(detail_frame, text='Email:', font=('times new roman', 20), bg='white').place(x=20, y=75)
    email_entry = Entry(detail_frame, font=('times new roman', 20), width=25)
    email_entry.place(x=140, y=75)

    Label(detail_frame, text='Contact:', font=('times new roman', 20), bg='white').place(x=480, y=75)
    contact_entry = Entry(detail_frame, font=('times new roman', 20), width=20)
    contact_entry.place(x=580, y=75)

    # === Row 3 ===
    Label(detail_frame, text='Address:', font=('times new roman', 20), bg='white').place(x=20, y=125)
    address_entry = Entry(detail_frame, font=('times new roman', 20), width=25)
    address_entry.place(x=140, y=125)

    Label(detail_frame, text='Gender:', font=('times new roman', 20), bg='white').place(x=480, y=125)
    gender_entry = ttk.Combobox(detail_frame, font=('times new roman', 20),
                                values=('Male', 'Female', 'Other'),
                                state='readonly', width=20)
    gender_entry.place(x=580, y=125)

    # === Action Buttons (Aligned next to Contact field row) ===
    add_button = Button(detail_frame, text='Add', font=('Helvetica', 20), 
                        bg='#0b8fcb', fg='black', padx=10, pady=3,
                        command=add_employee)
    add_button.place(x=980, y=25)

    update_button = Button(detail_frame, text='Update', font=('Helvetica', 20), 
                        bg='#0b8fcb', fg='black', padx=10, pady=3,
                        command=update_employee)
    update_button.place(x=1130, y=25)

    clear_button = Button(detail_frame, text='Clear', font=('Helvetica', 20), 
                        bg='#0b8fcb', fg='black', padx=10, pady=3,
                        command=clear_entries)
    clear_button.place(x=980, y=100)

    delete_button = Button(detail_frame, text='Delete', font=('Helvetica', 20), 
                        bg='#dc3545', fg='black', padx=10, pady=3,
                        command=delete_employee)
    delete_button.place(x=1130, y=100)


        
    # Bind treeview selection
    employee_treeview.bind('<ButtonRelease-1>', select_data)
    
    # Load initial data
    treeview_data()


def treeview_data():
    """Load all employee data into treeview"""
    cursor, conn = connect_database()
    if not cursor or not conn:
        return

    try:
        # Clear existing data
        for item in employee_treeview.get_children():
            employee_treeview.delete(item)

        cursor.execute("SELECT * FROM employees ORDER BY id")
        records = cursor.fetchall()

        for index, record in enumerate(records):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            employee_treeview.insert('', 'end', values=record, tags=(tag,))

    except mysql.connector.Error as e:
        messagebox.showerror('Database Error', f'Error loading data: {e}')
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()


def search_employee(search_by, search_value):
    """Search employees based on criteria"""
    if not search_value.strip():
        messagebox.showwarning('Warning', 'Please enter a search value')
        return
    
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    
    try:
        # Clear existing data
        for item in employee_treeview.get_children():
            employee_treeview.delete(item)
        
        # Map search options to database columns
        column_map = {
            'Name': 'name',
            'Email': 'email',
            'Contact': 'contact',
            'Age': 'age',
            'Address': 'address',
            'Gender': 'gender'
        }
        
        column = column_map.get(search_by, 'name')
        query = f"SELECT * FROM employees WHERE {column} LIKE %s ORDER BY id"
        cursor.execute(query, (f'%{search_value}%',))
        records = cursor.fetchall()
        
        for record in records:
            employee_treeview.insert('', 'end', values=record)
        
        if not records:
            messagebox.showinfo('No Results', 'No employees found matching your search criteria.')
            
    except mysql.connector.Error as e:
        messagebox.showerror('Database Error', f'Error searching data: {e}')
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

def select_data(event):
    """Populate entry fields when treeview item is selected"""
    selection = employee_treeview.selection()
    if selection:
        values = employee_treeview.item(selection[0])['values']
        if values:
            # Clear entries first
            clear_entries()
            # Populate with selected data (skip ID which is at index 0)
            name_entry.insert(0, values[1])
            email_entry.insert(0, values[2])
            contact_entry.insert(0, values[3])
            age_entry.insert(0, values[4])
            address_entry.insert(0, values[5])
            gender_entry.set(values[6])

def add_employee():
    """Add new employee to database"""
    # Get values
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    contact = contact_entry.get().strip()
    age = age_entry.get().strip()
    address = address_entry.get().strip()
    gender = gender_entry.get()
    
    # Validation
    if not all([name, email, contact, age, address, gender]):
        messagebox.showerror('Error', 'All fields are required!')
        return
    
    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror('Error', 'Please enter a valid age!')
        return
    
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    
    try:
        # Check if email already exists
        cursor.execute("SELECT email FROM employees WHERE email = %s", (email,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'Email already exists!')
            return
        
        query = """
            INSERT INTO employees (name, email, contact, age, address, gender)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, contact, int(age), address, gender))
        conn.commit()
        messagebox.showinfo('Success', 'Employee added successfully!')
        add_notification(f'Employee "{name}" was added.', 'info')
        clear_entries()
        treeview_data()
        
    except mysql.connector.Error as e:
        messagebox.showerror('Database Error', f'Error adding employee: {e}')
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

def update_employee():
    """Update selected employee"""
    selection = employee_treeview.selection()
    if not selection:
        messagebox.showwarning('Warning', 'Please select an employee to update!')
        return
    
    # Get selected employee ID
    employee_id = employee_treeview.item(selection[0])['values'][0]
    
    # Get updated values
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    contact = contact_entry.get().strip()
    age = age_entry.get().strip()
    address = address_entry.get().strip()
    gender = gender_entry.get()
    
    # Validation
    if not all([name, email, contact, age, address, gender]):
        messagebox.showerror('Error', 'All fields are required!')
        return
    
    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror('Error', 'Please enter a valid age!')
        return
    
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    
    try:
        # Check if email already exists for another employee
        cursor.execute("SELECT id FROM employees WHERE email = %s AND id != %s", (email, employee_id))
        if cursor.fetchone():
            messagebox.showerror('Error', 'Email already exists for another employee!')
            return
        
        query = """
            UPDATE employees 
            SET name = %s, email = %s, contact = %s, age = %s, address = %s, gender = %s
            WHERE id = %s
        """
        cursor.execute(query, (name, email, contact, int(age), address, gender, employee_id))
        conn.commit()
        messagebox.showinfo('Success', 'Employee updated successfully!')
        add_notification(f'Employee ID {employee_id} was updated.', 'info')
        clear_entries()
        treeview_data()
        
    except mysql.connector.Error as e:
        messagebox.showerror('Database Error', f'Error updating employee: {e}')
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

def delete_employee():
    """Delete selected employee"""
    selection = employee_treeview.selection()
    if not selection:
        messagebox.showwarning('Warning', 'Please select an employee to delete!')
        return
    
    # Get selected employee info
    values = employee_treeview.item(selection[0])['values']
    employee_id = values[0]
    employee_name = values[1]
    
    # Confirm deletion
    result = messagebox.askyesno('Confirm Delete', 
                                f'Are you sure you want to delete {employee_name}?\n\nThis action cannot be undone.')
    if not result:
        return
    
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    
    try:
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()
        messagebox.showinfo('Success', 'Employee deleted successfully!')
        add_notification(f'Employee "{employee_name}" was deleted.', 'info')
        clear_entries()
        treeview_data()
        
    except mysql.connector.Error as e:
        messagebox.showerror('Database Error', f'Error deleting employee: {e}')
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

def clear_entries():
    """Clear all entry fields"""
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    contact_entry.delete(0, END)
    age_entry.delete(0, END)
    address_entry.delete(0, END)
    gender_entry.set('')

def enable_button():
    """This function should enable your main application buttons after login"""
    # Add your code here to enable buttons in your main application
    print("Login successful - enabling main application features")

def secondary_window():
    login_window = Toplevel()
    login_window.title("Log In")
    login_window.geometry('300x450+300+450')
    login_window.config(bg='#30353a')
    login_window.resizable(False, False)  # Prevent resizing
    
    # Make the window modal (stay on top)
    login_window.grab_set()
    
    def validate(event=None):
        user = username_entry.get().strip()  # Remove whitespace
        password = password_entry.get().strip()
        correct_user = "admin"
        correct_password = "user"
        
        # Check if fields are empty
        if not user or not password:
            messagebox.showerror(title="Login Failed", message="Please enter both username and password")
            return
        
        if user == correct_user and password == correct_password:
            messagebox.showinfo(title="Login", message=f"Login Successful, Welcome {user}! :)")
            login_window.destroy()
            enable_button()
        else:
            messagebox.showerror(title="Login Failed", message="Invalid username and password")
            # Clear password field for security
            password_entry.delete(0, END)
            username_entry.focus()
    
    # Header background
    header_label = Label(login_window, padx=13, bg='#606b75', width=30, height=20)
    header_label.place(x=30, y=100)
    
    # Title label
    title_label = Label(login_window, text="LOGIN", font=('times new roman', 16, 'bold'), 
                       fg='white', bg='#606b75')
    title_label.place(x=125, y=120)
    
    # Username label and entry
    username_label = Label(login_window, text="Username:", font=('times new roman', 14), 
                          fg='white', bg='#606b75')
    username_label.place(x=40, y=200)
    
    username_entry = Entry(login_window, font=('times new roman', 12), relief='solid', bd=1)
    username_entry.place(x=140, y=202, width=120, height=25)
    
    # Password label and entry
    password_label = Label(login_window, text="Password:", font=('times new roman', 14), 
                          fg='white', bg='#606b75')
    password_label.place(x=40, y=255)
    
    password_entry = Entry(login_window, font=('times new roman', 12), show='*', 
                          relief='solid', bd=1)
    password_entry.place(x=140, y=255, width=120, height=25)
    
    # Login button
    submit_button = Button(login_window, text="Login", background='#4CAF50', fg='white', 
                          command=validate, font=('times new roman', 12, 'bold'),
                          cursor='hand2', relief='raised', bd=2)
    submit_button.place(x=120, y=310, width=80, height=35)
    
    # Cancel button
    cancel_button = Button(login_window, text="Cancel", background='#f44336', fg='white',
                          command=login_window.destroy, font=('times new roman', 12, 'bold'),
                          cursor='hand2', relief='raised', bd=2)
    cancel_button.place(x=120, y=355, width=80, height=35)
    
    # Bind Enter key to validate function
    login_window.bind("<Return>", validate)
    
    # Set focus to username entry
    username_entry.focus()
    
    # Center the window on screen
    login_window.update_idletasks()
    x = (login_window.winfo_screenwidth() // 2) - (300 // 2)
    y = (login_window.winfo_screenheight() // 2) - (450 // 2)
    login_window.geometry(f'300x450+{x}+{y}')

is_logged_in = False
# ------------------ NAVIGATION BUTTONS ------------------
button_dash = Button(root, image=dash_icon, compound=LEFT, text="Dashboard", command=dashboard,state=DISABLED, bg='#d4d4ce',
                     font=('Times', 14), fg='black', padx=115, pady=11, borderwidth=0, cursor='hand2')
button_inv = Button(root, image=inv_icon, compound=LEFT, text="Inventory", command=inventory,state=DISABLED, font=('Times', 14),
                    bg='#d4d4ce', fg='black', padx=120, pady=11, borderwidth=0, cursor='hand2')
button_prodm = Button(root, image=productm_icon, compound=LEFT, command=product_management,state=DISABLED, text="Product Management",
                      bg='#d4d4ce', font=('Times', 14), fg='black', padx=76, pady=11, borderwidth=0, cursor='hand2')
button_supplier = Button(root, image=supplier_icon, compound=LEFT, command=supplier,state=DISABLED, text="Supplier", bg='#d4d4ce',
                         font=('Times', 14), fg='black', padx=124, pady=14, borderwidth=0, cursor='hand2')
notification_btn = Button(root, image=bell_icon, compound=LEFT, command=notification_df,state=DISABLED, text="Notification",
                          bg='#d4d4ce', font=('Times', 14), fg='black', padx=110, pady=12, borderwidth=0, cursor='hand2')
user_management_btn = Button(root, image=userm_icon, compound=LEFT, command=usermanage,state=DISABLED, text="User Management", bg='#d4d4ce',
                             font=('Times', 14), fg='black', padx=86, pady=15, borderwidth=0, cursor='hand2')
Logout_Btn = Button(root, image=log_icon, compound=RIGHT, text='Exit', command=exit,
                    font=('times new roman', 15, 'bold'), padx=13)
Signin_Btn = Button(root, image=Sign_icon, compound=RIGHT, text='Log In',
                    font=('times new roman', 15, 'bold'), padx=13,
                    command=secondary_window)
protected_buttons = [
    button_dash,
    button_inv, 
    button_prodm,
    button_supplier,
    notification_btn,
    user_management_btn,
]

def enable_button():
    """Enable all buttons after successful login"""
    global is_logged_in
    is_logged_in = True
    
    # Enable all protected buttons
    for button in protected_buttons:
        button.config(state='normal', cursor='hand2')
    
    # Update login button to show logged in status
    Signin_Btn.config(text='Logged In', state='disabled', bg='#4CAF50', fg='white')
    
    print("All buttons enabled - User logged in successfully")

def disable_buttons():
    """Disable all buttons (for logout)"""
    global is_logged_in
    is_logged_in = False
    
    # Disable all protected buttons
    for button in protected_buttons:
        button.config(state='disabled', cursor='arrow')
    
    # Reset login button
    Signin_Btn.config(text='Log In', state='normal', bg='SystemButtonFace', fg='black')
    
    print("All buttons disabled - User logged out")

def logout_function():
    """Handle logout process"""
    from tkinter import messagebox
    
    result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if result:
        disable_buttons()
        messagebox.showinfo("Logout", "You have been logged out successfully")

# Alternative: Create wrapper functions that check login status
def check_login_required(func):
    """Decorator to check if user is logged in before executing function"""
    def wrapper(*args, **kwargs):
        if not is_logged_in:
            from tkinter import messagebox
            messagebox.showwarning("Access Denied", "Please log in to access this feature")
            return
        return func(*args, **kwargs)
    return wrapper


def update_button_appearance():
    """Update button appearance based on login status"""
    if is_logged_in:
        # Enabled appearance
        for button in protected_buttons:
            button.config(bg='#d4d4ce', fg='black')
    else:
        # Disabled appearance
        for button in protected_buttons:
            button.config(bg='#a0a0a0', fg="#000000")

# Call this after creating buttons
update_button_appearance()

button_dash.place(x=-40, y=100)
button_inv.place(x=-44, y=183)
button_prodm.place(x=0, y=266)
button_supplier.place(x=-50, y=350)
notification_btn.place(x=-38, y=450)
user_management_btn.place(x=-12, y=540)
Logout_Btn.place(x=1750, y=15)
Signin_Btn.place(x=1550, y=15)

root.mainloop()



