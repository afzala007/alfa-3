"""
====================================
  🛒 Python E-Commerce Shopping App
====================================
Complete beginner-friendly project
Features: Login/Signup, Products, Cart, Checkout, Admin Panel
"""

import json
import os
import hashlib
from datetime import datetime

# ─────────────────────────────────────────
#  DATA STORAGE (saved in JSON files)
# ─────────────────────────────────────────

USERS_FILE = "users.json"
PRODUCTS_FILE = "products.json"
ORDERS_FILE = "orders.json"

def load_data(filename):
    """Load data from a JSON file."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    """Convert password to a secure hash."""
    return hashlib.sha256(password.encode()).hexdigest()

# ─────────────────────────────────────────
#  INITIALIZE DEFAULT DATA
# ─────────────────────────────────────────

def initialize_data():
    """Create default products and admin user if not exist."""
    
    # Create default products
    if not os.path.exists(PRODUCTS_FILE):
        default_products = {
            "1": {"name": "Apple iPhone 15", "price": 999.99, "stock": 10, "category": "Electronics", "description": "Latest iPhone with A17 chip"},
            "2": {"name": "Samsung 4K TV 55\"", "price": 599.99, "stock": 5, "category": "Electronics", "description": "Ultra HD Smart TV"},
            "3": {"name": "Nike Running Shoes", "price": 89.99, "stock": 20, "category": "Footwear", "description": "Comfortable sports shoes"},
            "4": {"name": "Python Programming Book", "price": 39.99, "stock": 15, "category": "Books", "description": "Learn Python from scratch"},
            "5": {"name": "Coffee Maker Deluxe", "price": 79.99, "stock": 8, "category": "Kitchen", "description": "Brew perfect coffee every time"},
            "6": {"name": "Wireless Headphones", "price": 149.99, "stock": 12, "category": "Electronics", "description": "Noise cancelling Bluetooth"},
            "7": {"name": "Yoga Mat Premium", "price": 29.99, "stock": 25, "category": "Sports", "description": "Non-slip, eco-friendly mat"},
            "8": {"name": "Laptop Stand", "price": 49.99, "stock": 18, "category": "Accessories", "description": "Adjustable aluminum stand"},
        }
        save_data(PRODUCTS_FILE, default_products)

    # Create admin user
    if not os.path.exists(USERS_FILE):
        default_users = {
            "admin": {
                "password": hash_password("admin123"),
                "name": "Administrator",
                "email": "admin@shop.com",
                "role": "admin",
                "joined": str(datetime.now().date())
            }
        }
        save_data(USERS_FILE, default_users)

    # Create empty orders file
    if not os.path.exists(ORDERS_FILE):
        save_data(ORDERS_FILE, {})

# ─────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "=" * 50)
    print(f"  🛒  {title}")
    print("=" * 50)

def print_line():
    print("-" * 50)

def press_enter():
    input("\n  Press Enter to continue...")

# ─────────────────────────────────────────
#  USER AUTHENTICATION
# ─────────────────────────────────────────

def signup():
    """Register a new user account."""
    print_header("CREATE ACCOUNT")
    users = load_data(USERS_FILE)

    username = input("  Choose a username: ").strip()
    if not username:
        print("  ❌ Username cannot be empty!")
        press_enter()
        return None
    
    if username in users:
        print("  ❌ Username already taken! Try another.")
        press_enter()
        return None

    name = input("  Your full name: ").strip()
    email = input("  Your email: ").strip()
    password = input("  Choose a password: ").strip()

    if len(password) < 4:
        print("  ❌ Password must be at least 4 characters!")
        press_enter()
        return None

    users[username] = {
        "password": hash_password(password),
        "name": name,
        "email": email,
        "role": "customer",
        "joined": str(datetime.now().date())
    }
    save_data(USERS_FILE, users)
    print(f"\n  ✅ Account created! Welcome, {name}!")
    press_enter()
    return username

def login():
    """Login with existing credentials."""
    print_header("LOGIN")
    users = load_data(USERS_FILE)

    username = input("  Username: ").strip()
    password = input("  Password: ").strip()

    if username in users and users[username]["password"] == hash_password(password):
        print(f"\n  ✅ Welcome back, {users[username]['name']}! 👋")
        press_enter()
        return username
    else:
        print("\n  ❌ Wrong username or password!")
        press_enter()
        return None

# ─────────────────────────────────────────
#  PRODUCT LISTING & SEARCH
# ─────────────────────────────────────────

def show_all_products(cart=None):
    """Display all available products."""
    print_header("ALL PRODUCTS")
    products = load_data(PRODUCTS_FILE)
    
    if not products:
        print("  No products available.")
        press_enter()
        return

    print(f"  {'ID':<4} {'Product Name':<30} {'Price':>10} {'Stock':>6} {'Category':<15}")
    print_line()
    
    for pid, p in products.items():
        stock_str = f"{p['stock']}" if p['stock'] > 0 else "Out of Stock"
        print(f"  {pid:<4} {p['name']:<30} ${p['price']:>9.2f} {stock_str:>6} {p['category']:<15}")
    
    print_line()
    if cart:
        total_items = sum(cart.values())
        print(f"  🛒 Items in your cart: {total_items}")

def search_products():
    """Search for products by name or category."""
    print_header("SEARCH PRODUCTS")
    products = load_data(PRODUCTS_FILE)
    
    keyword = input("  Enter search keyword: ").strip().lower()
    if not keyword:
        return

    results = {}
    for pid, p in products.items():
        if keyword in p['name'].lower() or keyword in p['category'].lower() or keyword in p['description'].lower():
            results[pid] = p

    if results:
        print(f"\n  Found {len(results)} result(s):\n")
        print(f"  {'ID':<4} {'Product Name':<30} {'Price':>10} {'Category':<15}")
        print_line()
        for pid, p in results.items():
            print(f"  {pid:<4} {p['name']:<30} ${p['price']:>9.2f} {p['category']:<15}")
            print(f"       📝 {p['description']}")
    else:
        print(f"\n  ❌ No products found for '{keyword}'")

    press_enter()

# ─────────────────────────────────────────
#  SHOPPING CART
# ─────────────────────────────────────────

def add_to_cart(cart):
    """Add a product to the cart."""
    products = load_data(PRODUCTS_FILE)
    show_all_products(cart)
    
    print()
    product_id = input("  Enter Product ID to add to cart (or 0 to go back): ").strip()
    
    if product_id == "0":
        return cart
    
    if product_id not in products:
        print("  ❌ Invalid Product ID!")
        press_enter()
        return cart
    
    product = products[product_id]
    
    if product['stock'] <= 0:
        print("  ❌ Sorry, this product is out of stock!")
        press_enter()
        return cart
    
    try:
        qty = int(input(f"  How many '{product['name']}' do you want? "))
    except ValueError:
        print("  ❌ Please enter a valid number!")
        press_enter()
        return cart
    
    if qty <= 0:
        print("  ❌ Quantity must be at least 1!")
        press_enter()
        return cart
    
    current_in_cart = cart.get(product_id, 0)
    if current_in_cart + qty > product['stock']:
        print(f"  ❌ Not enough stock! Available: {product['stock']}")
        press_enter()
        return cart
    
    cart[product_id] = current_in_cart + qty
    print(f"\n  ✅ Added {qty}x '{product['name']}' to cart!")
    press_enter()
    return cart

def view_cart(cart):
    """Display cart contents with total."""
    print_header("YOUR SHOPPING CART")
    products = load_data(PRODUCTS_FILE)
    
    if not cart:
        print("  🛒 Your cart is empty!")
        press_enter()
        return cart
    
    total = 0
    print(f"  {'#':<4} {'Product':<30} {'Price':>10} {'Qty':>5} {'Subtotal':>10}")
    print_line()
    
    for i, (pid, qty) in enumerate(cart.items(), 1):
        if pid in products:
            p = products[pid]
            subtotal = p['price'] * qty
            total += subtotal
            print(f"  {i:<4} {p['name']:<30} ${p['price']:>9.2f} {qty:>5} ${subtotal:>9.2f}")
    
    print_line()
    print(f"  {'TOTAL':>51} ${total:>9.2f}")
    print()
    
    action = input("  Options: [R] Remove item | [C] Clear cart | [Enter] Go back: ").strip().upper()
    
    if action == "R":
        try:
            num = int(input("  Enter item number to remove: "))
            keys = list(cart.keys())
            if 1 <= num <= len(keys):
                removed = keys[num - 1]
                del cart[removed]
                print(f"  ✅ Item removed from cart!")
            else:
                print("  ❌ Invalid item number!")
        except ValueError:
            print("  ❌ Please enter a valid number!")
        press_enter()
    
    elif action == "C":
        confirm = input("  Clear entire cart? (yes/no): ").strip().lower()
        if confirm == "yes":
            cart = {}
            print("  ✅ Cart cleared!")
            press_enter()
    
    return cart

# ─────────────────────────────────────────
#  CHECKOUT
# ─────────────────────────────────────────

def checkout(cart, username):
    """Process the order and place it."""
    print_header("CHECKOUT")
    products = load_data(PRODUCTS_FILE)
    orders = load_data(ORDERS_FILE)
    users = load_data(USERS_FILE)
    
    if not cart:
        print("  ❌ Your cart is empty! Add items first.")
        press_enter()
        return cart
    
    # Show order summary
    total = 0
    order_items = {}
    print("  📦 ORDER SUMMARY")
    print_line()
    
    for pid, qty in cart.items():
        if pid in products:
            p = products[pid]
            subtotal = p['price'] * qty
            total += subtotal
            order_items[pid] = {"name": p['name'], "price": p['price'], "qty": qty, "subtotal": subtotal}
            print(f"  • {p['name']} x{qty} = ${subtotal:.2f}")
    
    print_line()
    print(f"  💰 Total Amount: ${total:.2f}")
    print()
    
    # Shipping info
    print("  📬 SHIPPING INFORMATION")
    address = input("  Enter delivery address: ").strip()
    if not address:
        print("  ❌ Address is required!")
        press_enter()
        return cart
    
    # Payment method
    print("\n  💳 PAYMENT METHOD")
    print("  [1] Cash on Delivery")
    print("  [2] Credit/Debit Card")
    print("  [3] Online Banking")
    payment_choice = input("  Choose payment method (1-3): ").strip()
    
    payment_methods = {"1": "Cash on Delivery", "2": "Credit/Debit Card", "3": "Online Banking"}
    payment = payment_methods.get(payment_choice, "Cash on Delivery")
    
    if payment_choice in ["2", "3"]:
        input("  Enter card/account number (demo - press Enter): ")
    
    # Confirm order
    print(f"\n  ✅ Payment: {payment}")
    print(f"  ✅ Address: {address}")
    confirm = input(f"\n  Place order for ${total:.2f}? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print("  ❌ Order cancelled.")
        press_enter()
        return cart
    
    # Save order
    order_id = f"ORD{len(orders) + 1:04d}"
    orders[order_id] = {
        "username": username,
        "items": order_items,
        "total": total,
        "address": address,
        "payment": payment,
        "status": "Confirmed",
        "date": str(datetime.now())
    }
    save_data(ORDERS_FILE, orders)
    
    # Update stock
    for pid, qty in cart.items():
        if pid in products:
            products[pid]['stock'] -= qty
    save_data(PRODUCTS_FILE, products)
    
    print(f"\n  🎉 ORDER PLACED SUCCESSFULLY!")
    print(f"  📋 Order ID: {order_id}")
    print(f"  💰 Total Paid: ${total:.2f}")
    print(f"  🚚 Expected delivery in 3-5 business days")
    
    press_enter()
    return {}  # Clear cart after successful order

def view_my_orders(username):
    """View order history for current user."""
    print_header("MY ORDERS")
    orders = load_data(ORDERS_FILE)
    
    my_orders = {oid: o for oid, o in orders.items() if o['username'] == username}
    
    if not my_orders:
        print("  You have no orders yet.")
        press_enter()
        return
    
    for oid, order in my_orders.items():
        print(f"\n  📦 Order ID: {oid}")
        print(f"  📅 Date: {order['date'][:19]}")
        print(f"  🚚 Status: {order['status']}")
        print(f"  💰 Total: ${order['total']:.2f}")
        print(f"  💳 Payment: {order['payment']}")
        print(f"  Items:")
        for item in order['items'].values():
            print(f"    • {item['name']} x{item['qty']} = ${item['subtotal']:.2f}")
        print_line()
    
    press_enter()

# ─────────────────────────────────────────
#  ADMIN PANEL
# ─────────────────────────────────────────

def admin_panel():
    """Admin management panel."""
    while True:
        print_header("ADMIN PANEL")
        print("  [1] View All Products")
        print("  [2] Add New Product")
        print("  [3] Edit Product")
        print("  [4] Delete Product")
        print("  [5] View All Orders")
        print("  [6] View All Users")
        print("  [7] Update Order Status")
        print("  [0] Logout")
        
        choice = input("\n  Enter choice: ").strip()
        
        if choice == "1":
            admin_view_products()
        elif choice == "2":
            admin_add_product()
        elif choice == "3":
            admin_edit_product()
        elif choice == "4":
            admin_delete_product()
        elif choice == "5":
            admin_view_orders()
        elif choice == "6":
            admin_view_users()
        elif choice == "7":
            admin_update_order()
        elif choice == "0":
            break
        else:
            print("  ❌ Invalid choice!")
            press_enter()

def admin_view_products():
    print_header("ALL PRODUCTS (ADMIN)")
    products = load_data(PRODUCTS_FILE)
    
    print(f"  {'ID':<4} {'Product Name':<28} {'Price':>10} {'Stock':>6} {'Category':<15}")
    print_line()
    for pid, p in products.items():
        print(f"  {pid:<4} {p['name']:<28} ${p['price']:>9.2f} {p['stock']:>6} {p['category']:<15}")
        print(f"       📝 {p['description']}")
    print_line()
    print(f"  Total Products: {len(products)}")
    press_enter()

def admin_add_product():
    print_header("ADD NEW PRODUCT")
    products = load_data(PRODUCTS_FILE)
    
    name = input("  Product name: ").strip()
    if not name:
        print("  ❌ Name required!")
        press_enter()
        return
    
    try:
        price = float(input("  Price ($): "))
        stock = int(input("  Stock quantity: "))
    except ValueError:
        print("  ❌ Invalid price or stock!")
        press_enter()
        return
    
    category = input("  Category: ").strip()
    description = input("  Description: ").strip()
    
    new_id = str(max([int(k) for k in products.keys()], default=0) + 1)
    products[new_id] = {
        "name": name,
        "price": price,
        "stock": stock,
        "category": category,
        "description": description
    }
    save_data(PRODUCTS_FILE, products)
    print(f"\n  ✅ Product '{name}' added with ID: {new_id}")
    press_enter()

def admin_edit_product():
    print_header("EDIT PRODUCT")
    products = load_data(PRODUCTS_FILE)
    admin_view_products()
    
    pid = input("  Enter Product ID to edit: ").strip()
    if pid not in products:
        print("  ❌ Product not found!")
        press_enter()
        return
    
    p = products[pid]
    print(f"\n  Editing: {p['name']} (press Enter to keep current value)")
    
    name = input(f"  Name [{p['name']}]: ").strip()
    price_str = input(f"  Price [{p['price']}]: ").strip()
    stock_str = input(f"  Stock [{p['stock']}]: ").strip()
    category = input(f"  Category [{p['category']}]: ").strip()
    description = input(f"  Description [{p['description']}]: ").strip()
    
    if name: p['name'] = name
    if price_str:
        try: p['price'] = float(price_str)
        except: pass
    if stock_str:
        try: p['stock'] = int(stock_str)
        except: pass
    if category: p['category'] = category
    if description: p['description'] = description
    
    products[pid] = p
    save_data(PRODUCTS_FILE, products)
    print(f"\n  ✅ Product updated successfully!")
    press_enter()

def admin_delete_product():
    print_header("DELETE PRODUCT")
    products = load_data(PRODUCTS_FILE)
    admin_view_products()
    
    pid = input("  Enter Product ID to delete: ").strip()
    if pid not in products:
        print("  ❌ Product not found!")
        press_enter()
        return
    
    confirm = input(f"  Delete '{products[pid]['name']}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        del products[pid]
        save_data(PRODUCTS_FILE, products)
        print("  ✅ Product deleted!")
    else:
        print("  ❌ Deletion cancelled.")
    press_enter()

def admin_view_orders():
    print_header("ALL ORDERS (ADMIN)")
    orders = load_data(ORDERS_FILE)
    
    if not orders:
        print("  No orders yet.")
        press_enter()
        return
    
    for oid, order in orders.items():
        print(f"\n  📦 {oid} | 👤 {order['username']} | 💰 ${order['total']:.2f} | 🚚 {order['status']}")
        print(f"     📅 {order['date'][:19]} | 💳 {order['payment']}")
    
    print_line()
    print(f"  Total Orders: {len(orders)}")
    press_enter()

def admin_view_users():
    print_header("ALL USERS (ADMIN)")
    users = load_data(USERS_FILE)
    
    print(f"  {'Username':<15} {'Name':<20} {'Email':<25} {'Role':<10} {'Joined'}")
    print_line()
    for uname, u in users.items():
        print(f"  {uname:<15} {u['name']:<20} {u['email']:<25} {u['role']:<10} {u['joined']}")
    print_line()
    print(f"  Total Users: {len(users)}")
    press_enter()

def admin_update_order():
    print_header("UPDATE ORDER STATUS")
    orders = load_data(ORDERS_FILE)
    admin_view_orders()
    
    oid = input("  Enter Order ID: ").strip()
    if oid not in orders:
        print("  ❌ Order not found!")
        press_enter()
        return
    
    print("\n  Status options:")
    statuses = ["Confirmed", "Processing", "Shipped", "Delivered", "Cancelled"]
    for i, s in enumerate(statuses, 1):
        print(f"  [{i}] {s}")
    
    try:
        choice = int(input("  Choose status: ")) - 1
        if 0 <= choice < len(statuses):
            orders[oid]['status'] = statuses[choice]
            save_data(ORDERS_FILE, orders)
            print(f"  ✅ Order {oid} status updated to '{statuses[choice]}'")
        else:
            print("  ❌ Invalid choice!")
    except ValueError:
        print("  ❌ Invalid input!")
    press_enter()

# ─────────────────────────────────────────
#  CUSTOMER MENU
# ─────────────────────────────────────────

def customer_menu(username):
    """Main menu for logged-in customers."""
    users = load_data(USERS_FILE)
    user_name = users[username]['name']
    cart = {}  # Cart stored in memory during session
    
    while True:
        clear()
        print_header(f"WELCOME, {user_name.upper()}!")
        print("  🛍️  SHOP MENU")
        print_line()
        print("  [1] Browse All Products")
        print("  [2] Search Products")
        print("  [3] Add to Cart")
        print(f"  [4] View Cart ({sum(cart.values())} items)")
        print("  [5] Checkout")
        print("  [6] My Orders")
        print("  [0] Logout")
        print_line()
        
        choice = input("  Enter choice: ").strip()
        
        if choice == "1":
            clear()
            show_all_products(cart)
            press_enter()
        elif choice == "2":
            clear()
            search_products()
        elif choice == "3":
            clear()
            cart = add_to_cart(cart)
        elif choice == "4":
            clear()
            cart = view_cart(cart)
        elif choice == "5":
            clear()
            cart = checkout(cart, username)
        elif choice == "6":
            clear()
            view_my_orders(username)
        elif choice == "0":
            print(f"\n  👋 Goodbye, {user_name}! Come back soon!")
            press_enter()
            break
        else:
            print("  ❌ Invalid choice!")
            press_enter()

# ─────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────

def main():
    """Main entry point of the app."""
    initialize_data()
    
    while True:
        clear()
        print("=" * 50)
        print("   🛒  PYTHON E-COMMERCE SHOPPING APP   ")
        print("=" * 50)
        print("  [1] Login")
        print("  [2] Sign Up (Create Account)")
        print("  [0] Exit")
        print("=" * 50)
        print("  💡 Admin login: username=admin, password=admin123")
        print("=" * 50)
        
        choice = input("\n  Enter choice: ").strip()
        
        if choice == "1":
            clear()
            username = login()
            if username:
                users = load_data(USERS_FILE)
                if users[username]['role'] == "admin":
                    admin_panel()
                else:
                    customer_menu(username)
        
        elif choice == "2":
            clear()
            username = signup()
            if username:
                customer_menu(username)
        
        elif choice == "0":
            clear()
            print("\n  👋 Thank you for shopping with us! Goodbye!\n")
            break
        
        else:
            print("  ❌ Invalid choice! Please enter 1, 2, or 0.")
            press_enter()

# ─────────────────────────────────────────
#  RUN THE APP
# ─────────────────────────────────────────

if __name__ == "__main__":
    main()