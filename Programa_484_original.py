from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import Toplevel
from tkinter import messagebox
import datetime
import sqlite3

# VARIABLES
is_admin = 'No'
machine_on = 'yes'
username = ' '
password = ' '
game_ID = None
item = ' '
price = 0.00
selected_sport = "None"
quantity = 0
cust_order = []
item_cost = 0.00
total_cost = 0.00
cash = 200.0
order_count = 0
earnings = 0 
cont_order = 'y'
item_count = {}

specialChar = ['$', '#', '@', '!', '*','%']

conn = sqlite3.connect('concession_stand.db')
cursor = conn.cursor()

# ITEMS TABLE
cursor.execute('''CREATE TABLE IF NOT EXISTS ITEMS
                (ITEM_ID INTEGER PRIMARY KEY,
                ITEM TEXT NOT NULL,
                PRICE TEXT NOT NULL,
                ITEM_TYPE TEXT NOT NULL)''')
conn.commit()

# INVENTORY TABLE
cursor.execute('''CREATE TABLE IF NOT EXISTS INVENTORY (
                ITEM TEXT PRIMARY KEY,
                QUANTITY INTEGER NOT NULL)''')
conn.commit()

# INVENTORY ITEMS TABLE (FOF ITEMS WITH MORE THAN ONE INGREDIENT)
cursor.execute('''CREATE TABLE IF NOT EXISTS INVENTORY_ITEMS (
                ITEM_ID INTEGER NOT NULL,
                ITEM TEXT NOT NULL,
                FOREIGN KEY (ITEM_ID) REFERENCES ITEMS(ITEM_ID),
                FOREIGN KEY (ITEM) REFERENCES INVENTORY(ITEM))''')
conn.commit()


# GAME ANALYTICS TABLE
cursor.execute('''CREATE TABLE IF NOT EXISTS GAME_ANALYTICS (
                game_ID TEXT PRIMARY KEY,
                sport TEXT NOT NULL,
                away_team TEXT,
                order_count INTEGER,
                earnings FLOAT)''')
conn.commit()

# ORDERS TABLE
cursor.execute('''CREATE TABLE IF NOT EXISTS ORDERS (
                order_ID int PRIMARY KEY,
                game_ID TEXT NOT NULL,
                total_cost float)''')
conn.commit()

# ORDERED ITEMS TABLE
cursor.execute('''CREATE TABLE IF NOT EXISTS ORDERED_ITEMS (
                order_ID int NOT NULL,
                item_ID TEXT NOT NULL,
                quantity int NOT NULL,
                cost float NOT NULL,
                FOREIGN KEY (order_ID) REFERENCES ORDERS(order_ID),
                FOREIGN KEY (item_ID) REFERENCES ITEMS(ITEM_ID))''')
conn.commit()

# USERS TABLE
cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (
                USERNAME TEXT PRIMARY KEY UNIQUE,
                PASSWORD TEXT NOT NULL,
                IS_ADMIN TEXT NOT NULL)''')
conn.commit()

# SEPARATE MENUS FOR SPORTS
football_menu = [('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'), ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'),
                ('Tea', 2.00, 'drink'), ('Coffee', 1.00, 'drink'),('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'),
                ('Hot Dog', 2.00, 'food'), ('Pepperoni Pizza', 4.00, 'food'), ('Cheese Pizza', 3.00, 'food'), ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'),
                ('Hersheys', 2.00, 'snack'), ('Skittles', 2.00, 'snack'), ('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'),
                ('Nachos', 3.00, 'snack'), ('French Fries', 2.00, 'snack'), ('Cheesesteak', 4.00, 'food'), ('Pretzel', 3.00, 'snack'),
                ('Pretzel with Cheese', 4.00, 'snack'), ('Hot Chocolate', 2.00, 'drink'), ('Pickles', 2.00, 'food'),('Chips', 1.00, 'snack'),
                ('Donnie Coleman BBQ', 5.00, 'food')]

for item, price, item_type in football_menu:
    cursor.execute("SELECT ITEM FROM ITEMS WHERE ITEM = ?", (item,))
    existing_item = cursor.fetchone()
    if existing_item:
        continue   
    
    try:
        cursor.execute("INSERT INTO ITEMS (ITEM, PRICE, ITEM_TYPE) VALUES (?, ?, ?)", (item, price, item_type))
    except sqlite3.IntegrityError:
        break
conn.commit()

basketball_menu = [('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'), ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'),
                ('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'), ('Hot Dog', 2.00, 'food'), ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'),
                ('Hersheys', 2.00, 'snack'), ('Skittles', 2.00, 'snack'),('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'), ('Nachos', 3.00, 'snack'),
                   ('Pickles', 2.00, 'food')]

for item, price, item_type in basketball_menu:
    cursor.execute("SELECT ITEM FROM ITEMS WHERE ITEM = ?", (item,))
    existing_item = cursor.fetchone()
    if existing_item:
        continue  
    
    try:
        cursor.execute("INSERT INTO ITEMS (ITEM, PRICE, ITEM_TYPE) VALUES (?, ?, ?)", (item, price, item_type))
    except sqlite3.IntegrityError:
        break
    
    try:
        cursor.execute("INSERT INTO ITEMS (ITEM, PRICE, ITEM_TYPE) VALUES (?, ?, ?)", (item, price, item_type))
    except sqlite3.IntegrityError:
        break
conn.commit()

soccer_menu = [('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'), ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'),
                ('Tea', 2.00, 'drink'), ('Coffee', 1.00, 'drink'),('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'), ('Hot Dog', 2.00, 'food'),
                ('Pepperoni Pizza', 4.00, 'food'), ('Cheese Pizza', 3.00, 'food'), ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'), ('Hersheys', 2.00, 'snack'),
                ('Skittles', 2.00, 'snack'), ('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'), ('Nachos', 3.00, 'snack'), ('Chips', 1.00, 'snack'),
                ('Donnie Coleman BBQ', 5.00, 'food')]

for item, price, item_type in soccer_menu:
    cursor.execute("SELECT ITEM FROM ITEMS WHERE ITEM = ?", (item,))
    existing_item = cursor.fetchone()
    if existing_item:
        continue  
    
    try:
        cursor.execute("INSERT INTO ITEMS (ITEM, PRICE, ITEM_TYPE) VALUES (?, ?, ?)", (item, price, item_type))
    except sqlite3.IntegrityError:
        break
conn.commit()

baseball_menu = [('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'), ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'),
                ('Tea', 2.00, 'drink'), ('Coffee', 1.00, 'drink'),('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'),
                ('Hot Dog', 2.00, 'food'), ('Pepperoni Pizza', 4.00, 'food'), ('Cheese Pizza', 3.00, 'food'), ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'),
                ('Chewing Gum', 2.00, 'snack'), ('Skittles', 2.00, 'snack'), ('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'),
                ('Sunflower Seeds', 2.00, 'snack'), ('Chips', 1.00, 'snack'), ('Donnie Coleman BBQ', 5.00, 'food')]

for item, price, item_type in baseball_menu:
    cursor.execute("SELECT ITEM FROM ITEMS WHERE ITEM = ?", (item,))
    existing_item = cursor.fetchone()
    if existing_item:
        continue      
    
    try:
        cursor.execute("INSERT INTO ITEMS (ITEM, PRICE, ITEM_TYPE) VALUES (?, ?, ?)", (item, price, item_type))
    except sqlite3.IntegrityError:
        break
conn.commit()

inventory_items = [('Gatorade', 100), ('Pepsi', 100),('Diet Pepsi', 100),('Dr. Wham', 100), ('Starry', 100),
                ('Tea', 100), ('Coffee', 100), ('Hamburger Buns', 100), ('Burger Patties', 100), ('Cheese Slices', 100), ('Hot Dog Buns', 100),
                ('Hot Dogs', 100), ('Popcorn', 100), ('M&Ms', 100), ('Hersheys', 100), ('Skittles', 100), ('Reeses Cup', 100), ('Tootsie Pop', 100),
                ('Nachos', 100), ('French Fries', 100), ('Cheesesteak', 100), ('Pretzel', 100), ('Pretzel with Cheese', 100), ('Hot Chocolate', 100),
                ('Pickles', 100), ('Chips', 100), ('Sunflower Seeds', 100), ('Gum', 100), ('Donnie Coleman BBQ', 100)]

for item, quantity in inventory_items:
    try:
        cursor.execute("INSERT INTO INVENTORY (ITEM, QUANTITY) VALUES (?, ?)", (item, quantity))
    except sqlite3.IntegrityError:
        break
conn.commit()

item_mappings = {
    'Hamburger': ['Hamburger Buns', 'Burger Patties'],
    'Cheeseburger': ['Hamburger Buns', 'Burger Patties', 'Cheese Slices'],
    'Hot Dog': ['Hot Dog Buns', 'Hot Dogs']
}


# ITEMS WITH MORE THAN 1 INGREDIENT
for item, inventory_items in item_mappings.items():
    item_id = cursor.execute("SELECT ITEM_ID FROM ITEMS WHERE ITEM = ?", (item,)).fetchone()[0]
    for inventory_item in inventory_items:
        # Check if the inventory item already exists
        cursor.execute("SELECT ITEM FROM INVENTORY_ITEMS WHERE ITEM = ? AND ITEM_ID = ?", (inventory_item, item_id))
        existing_item = cursor.fetchone()
        if existing_item:
            continue  # Skip inserting if the inventory item already exists

        cursor.execute('''INSERT INTO INVENTORY_ITEMS (ITEM_ID, ITEM) VALUES (?, ?)''', (item_id, inventory_item))
        conn.commit()

# STORE INVENTORY ITEMS IN A VARIABLE FOR DISPLAY PURPOSES
cursor.execute("SELECT ITEM, QUANTITY FROM INVENTORY")
inventory_items = cursor.fetchall()
    

# FUNCTION TO CREATE PRIMARY KEY FOR GAME ID
def generate_game_ID(gender, sport, away_team, away_teams, level):
    if sport == 'Football Game':
        prefix = '1'
    elif sport == 'Baseball Game':
        prefix = '2'
    elif sport == 'Softball Game':
        prefix = '2'
    elif sport == 'Basketball Game':
        prefix = '3'
    elif sport == 'Soccer Game':
        prefix = '4'
    else:
        raise ValueError("Invalid sport provided.")

    if gender == "Men's":
        suffix = 'M'
    elif gender == "Women's":
        suffix = 'W'
    else:
        raise ValueError("Invalid.")
    
    if level == 'JV':
        level = 'J'
    elif level == 'Varsity':
        level = 'V'
    
    team_number = int(away_teams.get(away_team))

    date = datetime.date.today()
    formatted_date = date.strftime('%m/%d/%y')

    ID = prefix + suffix + level + str(team_number) + formatted_date 

    return ID


# LOGIN/REGISTRATION FUNCTIONS
def username_exists(u):
    cursor.execute("SELECT COUNT(*) FROM USERS WHERE USERNAME = ?", (u,))
    count = cursor.fetchone()[0]
    return count > 0    

def admin_user(a):
    cursor.execute("SELECT IS_ADMIN FROM USERS WHERE USERNAME = ?", (a,))
    r = cursor.fetchone()

    if r is None:
        return False
    else:
        iz = r[0]
        if iz == "Yes":
            return True
        else:
            return False
    
def authenticate_user(u, p):
    cursor.execute("SELECT password FROM USERS WHERE username = ?", (u,))
    z = cursor.fetchone()

    if z is not None:
        stored_password = z[0]
        if p == stored_password:
            return True
    return False


# UPDATE INVENTORY TABLE WHEN A TRANSACTION IS CONFIRMED
def update_inventory(item):
    # Check if the item has associated ingredients in the INVENTORY_ITEMS table
    cursor.execute("SELECT ITEM_ID FROM ITEMS WHERE ITEM = ?", (item,))
    item_ID = cursor.fetchone()

    if item_ID is not None:
        item_ID = item_ID[0]
        cursor.execute("SELECT ITEM FROM INVENTORY_ITEMS WHERE ITEM_ID = ?", (item_ID,))
        result = cursor.fetchone()
        
        if result is None:
            cursor.execute("UPDATE INVENTORY SET quantity = quantity - 1 WHERE ITEM = ?", (item,))
        else:
            cursor.execute("SELECT ITEM FROM INVENTORY_ITEMS WHERE ITEM_ID = ?", (item_ID,))
            ingredients = cursor.fetchall()
            for ingredient in ingredients:
                cursor.execute("UPDATE INVENTORY SET quantity = quantity - 1 WHERE ITEM = ?", (ingredient[0],))

    conn.commit()

# KEEP TRACK OF ITEMS BEING BOUGHT FOR EACH ORDER
def update_sales(iID, oID, count, item_price):
    cost = count * float(item_price)
    cursor.execute('''INSERT INTO ORDERED_ITEMS (order_ID, item_ID, quantity, cost) VALUES (?, ?, ?, ?)''', (oID, iID, count, cost))
    conn.commit()

def event_selection(sport):
    frames = Tk()
    global width
    global height
    
    def selection_function(event):
        selected_event = event.widget.get()
    
    def go_back(sporting_event):
        global total_cost
        global cust_order
        global item_count
        total_cost = 0
        cust_order = []
        item_count = {}
        sporting_event.destroy()
        main_menu()
         
    def confirm(sport):
        global selected_sport
        def handle_gender_selection(gender, popup, level):
            global game_ID
            global selected_sport
            if popup is not None:
                popup.destroy()

            pop = Toplevel(frames)
            pop.title("Enter Away Team")
            pop.geometry("250x150")

            window_width = pop.winfo_width()
            window_height = pop.winfo_height()
            screen_width = pop.winfo_screenwidth()
            screen_height = pop.winfo_screenheight()

            x_coordinate = ((screen_width - 300)// 2)
            y_coordinate = ((screen_height - 300) // 2)

            pop.geometry(f"+{x_coordinate}+{y_coordinate}")

            selected_team = StringVar()
            away_team_dropdown = ttk.Combobox(pop, textvariable=selected_team)
            away_teams = {
                "East Rockingham": 1,
                "Harrisonburg": 2,
                "Rockbridge County": 3,
                "Spotswood": 4,
                "Turner Ashby": 5,
                "William Monroe": 6
            }
            away_team_dropdown["values"] = tuple(away_teams.keys())
            away_team_dropdown.pack(pady=(10, 0))

            button = Button(pop, text="Log Away Team", command=lambda: enter_away_team(gender, away_team_dropdown, button, sport, away_teams, level), font=("Arial", 12), height=1)
            button.pack()
        
        def set_men(popup, level):
            handle_gender_selection("Men's", popup, level)

        def set_women(popup, level):
            handle_gender_selection("Women's", popup, level)
        
        sport = dropdown.get()
        selected_sport = sport
        if sport == "Basketball Game" or sport == "Soccer Game":
            popup = Toplevel(frames)
            popup.title("Select Gender")
            popup.geometry("250x150")
            # Center the popup window
            window_width = popup.winfo_width()
            window_height = popup.winfo_height()
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()

            x_coordinate = ((screen_width - 300)// 2)
            y_coordinate = ((screen_height - 300) // 2)

            popup.geometry(f"+{x_coordinate}+{y_coordinate}")

            men_button1 = Button(popup, text="Men's JV", command=lambda: set_men(popup, 'JV'), font=("Arial", 12), height=1)
            men_button1.pack(pady=(10,0))
            men_button1 = Button(popup, text="Men's Varsity", command=lambda: set_men(popup, 'Varsity'), font=("Arial", 12), height=1)
            men_button1.pack()
            women_button1 = Button(popup, text="Women's JV", command=lambda: set_women(popup, 'JV'), font=("Arial", 12), height=1)
            women_button1.pack()
            women_button2 = Button(popup, text="Women's Varsity", command=lambda: set_women(popup, 'Varsity'), font=("Arial", 12), height=1)
            women_button2.pack()
            
        elif sport == "Football Game" or sport == "Baseball Game":
            popup1 = Toplevel(frames)
            popup1.title("Select")
            popup1.geometry("250x150")
            # Center the popup window
            window_width = popup1.winfo_width()
            window_height = popup1.winfo_height()
            screen_width = popup1.winfo_screenwidth()
            screen_height = popup1.winfo_screenheight()

            x_coordinate = ((screen_width - 300)// 2)
            y_coordinate = ((screen_height - 300) // 2)

            popup1.geometry(f"+{x_coordinate}+{y_coordinate}")

            men_button1 = Button(popup1, text=f"JV {sport}", command=lambda: set_men(popup1, 'JV'), font=("Arial", 12), height=1)
            men_button1.pack(pady=(10,0))
            men_button1 = Button(popup1, text=f"Varsity {sport}", command=lambda: set_men(popup1, 'Varsity'), font=("Arial", 12), height=1)
            men_button1.pack()
        elif sport == "Softball Game":
            popup1 = Toplevel(frames)
            popup1.title("Select")
            popup1.geometry("250x150")
            window_width = popup1.winfo_width()
            window_height = popup1.winfo_height()
            screen_width = popup1.winfo_screenwidth()
            screen_height = popup1.winfo_screenheight()

            x_coordinate = ((screen_width - 300)// 2)
            y_coordinate = ((screen_height - 300) // 2)

            popup1.geometry(f"+{x_coordinate}+{y_coordinate}")
            women_button1 = Button(popup1, text="JV Softball Game", command=lambda: set_women(popup1, 'JV'), font=("Arial", 12), height=1)
            women_button1.pack(pady=(10,0))
            women_button1 = Button(popup1, text="Varsity Softball Game", command=lambda: set_women(popup1, 'Varsity'), font=("Arial", 12), height=1)
            women_button1.pack()
        else:
            print("No gender selected")

    
    def enter_away_team(gender, dropdown, button, sport, away_teams, level):
        global game_ID
        away_team = dropdown.get()
        
        if away_team:
            ID = generate_game_ID(gender, sport, away_team, away_teams, level)
            game_ID = ID

            cursor.execute('''
                SELECT COUNT(*) FROM GAME_ANALYTICS WHERE game_ID = ?
                ''', (ID,))
            result = cursor.fetchone()

            if result[0] == 0:
                cursor.execute('''
                    INSERT INTO GAME_ANALYTICS (game_ID, sport, away_team, order_count, earnings)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (ID, sport, away_team, 0, 0))
            conn.commit()

            messagebox.showinfo("Success", "Away team registered successfully.")
            dropdown.destroy()
            button.destroy()
            frames.destroy()
            open_sport_page(sport)
        else:
            print("Error")
        
            
    global open_sport_page
    
    def open_sport_page(sport):
        
        global item_text
        global cust_order
        global is_admin
        global football_menu
        global baseball_menu
        global basketball_menu
        global soccer_menu
        admin_permissions = is_admin
        global sporting_event
        global width
        global height
        menu_category = 'food'
        
        sporting_event = Tk()
        sporting_event.title(sport + " Page")
        sporting_event.geometry(f"{width}x{height}+0+0")
        
        menu_label = Label(sporting_event, text=f"{sport} Menu:", font=("Arial", 20, "bold"))
        menu_label.pack(side=TOP, padx=10, pady=10)
        
        content_frame = Frame(sporting_event)
        content_frame.pack(side=TOP, padx=10, pady=10)

        menu_frame = Frame(content_frame)
        menu_frame.pack(side=LEFT, padx=10, pady=10)

        food_button = Button(menu_frame, text=" FOOD ", command=lambda: menu_categories('food'), font=("Arial", 15), height=3)
        snacks_button = Button(menu_frame, text="SNACKS", command=lambda: menu_categories('snack'), font=("Arial", 15), height=3)
        drinks_button = Button(menu_frame, text="DRINKS", command=lambda: menu_categories('drink'), font=("Arial", 15), height=3)

        food_button.grid(row=0, column=0, columnspan=2)
        snacks_button.grid(row=0, column=1, columnspan=2)
        drinks_button.grid(row=0, column=2, columnspan=2)
        
        def update_menu_prices(menu, item_updates):
            updated_menu = []
            for item, price, item_type in menu:
                if item in item_updates:
                    for item, price, item_type in item_updates:
                        updated_menu.append((item, price, item_type))
                else:
                    updated_menu.append((item, price, item_type))
            return updated_menu
        
        def menu_categories(category):
            nonlocal menu_category
            if category == 'food':
                menu_category = 'food'
                display_menu()
            elif category == 'snack':
                menu_category = 'snack'
                display_menu()
            elif category == 'drink':
                menu_category = 'drink'
                display_menu()
            else:
                print("invalid category selected")
                
        def display_menu():
            global cust_order
            global football_menu
            global baseball_menu
            global basketball_menu
            global soccer_menu
            global menu
            global item_count

            max_row_index = max([int(widget.grid_info()["row"]) for widget in menu_frame.grid_slaves()], default=0)
            if max_row_index > 0:
                for widget in menu_frame.grid_slaves():
                    if int(widget.grid_info()["row"]) > 0:
                        widget.destroy()

            cursor.execute("SELECT ITEM, PRICE, ITEM_TYPE FROM ITEMS")
            item_updates = cursor.fetchall()
    
            football_menu = update_menu_prices(football_menu, item_updates)
            basketball_menu = update_menu_prices(basketball_menu, item_updates)
            soccer_menu = update_menu_prices(soccer_menu, item_updates)
            baseball_menu = update_menu_prices(baseball_menu, item_updates)
            softball_menu = baseball_menu

            if sport == "Football Game":
                menu = football_menu
            elif sport == "Basketball Game":
                menu = basketball_menu
            elif sport == "Soccer Game":
                menu = soccer_menu
            elif sport == "Baseball Game":
                menu = baseball_menu
            elif sport == "Softball Game":
                menu = baseball_menu
            else:
                menu = []

            row = 1
            col = 0
            for item_index, item in enumerate(menu):
                item_name, item_price, item_type = item

                if item_type == menu_category:
                    item_button = Button(menu_frame,
                                         text=f"{item_name} - ${float(item_price):.2f}",
                                         command=lambda index=item_index: select_item(index),
                                         font=("Arial", 12), height=1)
                    item_button.grid(row=row, column=col, padx=10, pady=10)
                    if item_count:
                        if item_name in cust_order:
                            for i in cust_order:
                                item_count[i] = item_count.get(i)
                                if item_count[i] > 0:
                                    remove_button = Button(menu_frame, text="Remove",
                                        command=lambda index=item_index:remove_item(index, remove_button),
                                        font=("Arial", 12),height=1)
                                    remove_button.grid(row=row+1, column=col, padx=10, pady=0)
                    col += 1
                    if col == 4:
                        col = 0
                        row += 2
            if col < 4:
                empty_space = Label(menu_frame)
                empty_space.grid(row=row, column=col, padx=10, pady=10)
     
        display_menu()
     
        if admin_permissions.lower() == "yes":
            manage_button = Button(sporting_event, text="Manage Menu",command=lambda: manage_menu(sport),
                font=("Arial", 12),height=1)
            manage_button.pack(side="left", anchor="sw", padx=10, pady=10)
            
        if admin_permissions.lower() == "yes":
            analytics_button = Button(sporting_event, text="Analytics",command=lambda: show_analytics(sport),
                font=("Arial", 12),height=1)
            analytics_button.pack(side="right", anchor="se", padx=10, pady=10)   
     
        back_button = Button(sporting_event, text="Log Out",command=lambda: go_back(sporting_event),font=("Arial", 12),height=1)
        back_button.pack(side=BOTTOM, padx=10, pady=10)
     
        def menu_return():
            global payment_window
            global cust_order
            global total_cost
            cust_order = []
            total_cost = 0.0
            payment_window.destroy()
            open_sport_page(sport)
        
        def clear_cart(menu, menu_frame):
            global cust_order
            global item_text
            global item_count
            global total_cost

            if cust_order:
                items_to_remove = []

                if cust_order:
                    for item, count in item_count.items():
                        while count > 0:
                            items_to_remove.append(item)
                            count -= 1
                else:
                    print("Error1")

                for product in items_to_remove:
                    for indx, (item, price, item_type) in enumerate(menu):
                        if item == product:
                            item, price, item_type = menu[indx]
                            if item in cust_order:
                                cust_order.remove(item)
                                while item_count[item] > 0:
                                    item_count[item] -= 1
                                del item_count[item]
                                total_cost = 0
                            else:
                                print("Error2")

                item_text.config(state=NORMAL)
                item_text.delete('1.0', END)
                item_text.insert(END, f"CART CLEARED!\n")
                item_text.tag_configure("center", justify="center")
                item_text.tag_add("center", "1.0", "end")
                item_text.config(state=DISABLED)

            else:
                messagebox.showerror("Error", "There are no items in your cart.")
                
            display_menu()
            
     
        def confirm_transaction():
            global total_cost
            global payment_window
            global cash
            global earnings
            global game_ID
            global inventory_items
            global item_count
            global order_count
            global cust_order
            global width
            global height
            
            cursor.execute('SELECT order_count FROM GAME_ANALYTICS WHERE game_ID = ?', (game_ID,))
            result = cursor.fetchone()
            
            order_count = 0
            sufficient_inventory = True
            
            if result:
                order_count = result[0]
        
            for item, count in item_count.items():
                    for inventory_item in inventory_items:
                        if item == inventory_item[0]:
                            if count > inventory_item[1]:
                                sufficient_inventory = False
                                messagebox.showerror("Insufficient Inventory", f"There is insufficient inventory for {item}.")
                                break
            if cust_order and sufficient_inventory:
                cursor.execute("SELECT MAX(order_ID) FROM ORDERS")
                result = cursor.fetchone()
                order_ID = result[0] + 1 if result[0] else 1
                
                cursor.execute(
                    "INSERT INTO ORDERS (order_ID, game_ID, total_cost) VALUES (?, ?, ?)",
                (order_ID, game_ID, total_cost)
                )
                conn.commit()

                
                order_count += 1
                sporting_event.destroy()
                payment_window = Tk()
                payment_window.title("Payment Page")
                payment_window.geometry(f"{width}x{height}+0+0")
                frame = Frame(payment_window)
                frame.pack(expand=True)
                
                cash += total_cost
                earnings += total_cost
                cursor.execute('UPDATE GAME_ANALYTICS SET earnings = IFNULL(earnings, 0) + ? WHERE game_ID = ?', (total_cost, game_ID))
                cursor.execute('UPDATE GAME_ANALYTICS SET order_count = IFNULL(order_count, 0) + 1 WHERE game_ID = ?', (game_ID,))
                
                confirmed_label = Text(frame, width=40, height=10)
                confirmed_label.pack(padx=40, pady=40)
                frame.place(relx=0.5, rely=0.5, anchor=CENTER)

                confirmed_label.config(state=NORMAL)
                confirmed_label.delete('1.0', END)

                confirmed_label.tag_configure("center", justify="center", wrap="word")
                confirmed_label.insert(END, f"You ordered:\n\n")
                for item, count in item_count.items():
                    cursor.execute("SELECT PRICE FROM ITEMS WHERE ITEM = ?", (item,))
                    result = cursor.fetchone()
                    if result:
                        p = result[0] 
                    
                    if count > 1:
                        update_sales(item, order_ID, count, p)
                        confirmed_label.insert(END, f"{count}x {item}\n")
                        for _ in range(count):
                            update_inventory(item)
                    else:
                        confirmed_label.insert(END, f"{item}\n")
                        update_inventory(item)
                        update_sales(item, order_ID, 1, p)
    

                confirmed_label.insert(END, f"Total Cost: ${total_cost:.2f}\n\n")
                confirmed_label.insert(END, f"ORDER NUMBER: {order_count}")
                confirmed_label.tag_add("center", "1.0", "end")
                confirmed_label.config(state=DISABLED)
                confirmed_label.see(END)
                
                item_count = {}
                cust_order = []
                total_cost = 0
                item_cost = 0
                            
                next_button = Button(frame, text="Return to Menu", command=menu_return, font=("Arial", 12), height=1)
                next_button.pack(pady=(0, 10))
             
                payment_window.mainloop()
            elif sufficient_inventory and not cust_order:
                messagebox.showerror("Error", "There are no items in your cart.")
     
        complete_button = Button(sporting_event, text="Complete Transaction", command=lambda: confirm_transaction(),
                                 font=("Arial", 12), height=1)
        complete_button.pack(side=BOTTOM, padx=10, pady=10)
        
        clear_button = Button(sporting_event, text="Clear Cart", command=lambda: clear_cart(menu, menu_frame), font=("Arial", 12), height=1)
        clear_button.pack(side=BOTTOM, padx=10, pady=10)
     
        item_text = Text(content_frame, width=40, height=20)
        item_text.config(state=DISABLED)
        item_text.pack(side=RIGHT, padx=30, pady=30)
          
        
        def remove_item(index, remove_button):
            global item_text
            global item_count
            global price
            global cust_order
            global total_cost
            global item_cost
            global menu
            item, price, item_type = menu[index]
            
            if item_count[item] >= 1:
                item_count[item] -= 1
                total_cost -= float(price)
                if item_count[item] == 0:
                    cust_order.remove(item)
                    del item_count[item]
                    remove_button.destroy()
            
            item_text.tag_configure("center", justify="center")

            item_text.config(state=NORMAL)
            item_text.delete("1.0", END)

            item_text.insert(END, f"You removed: {item}\n")
            item_text.insert(END, f"Current cost: ${total_cost:.2f}\n\n")
            item_text.insert(END, f"Cart: {len(cust_order)} item(s) in cart\n")
            for i, count in item_count.items():
                if count > 1:
                    item_text.insert(END, f"\t{count}x {i}\n")
                else:
                    item_text.insert(END, f"\t{i}\n")
            
            item_text.tag_add("center", "1.0", "end")

            item_text.config(state=DISABLED)
            item_text.see(END)
            
            display_menu()
        
        def select_item(index):
            #global item
            global item_text
            global item_cost
            global price
            global cust_order
            global total_cost
            global item_count

            item, price, item_type = menu[index]
            if item not in cust_order:
                cust_order.append(item)
            
            item_count[item] = item_count.get(item, 0) + 1
            item_cost = float(price)
            total_cost += float(price)

            item_text.tag_configure("center", justify="center")

            item_text.config(state=NORMAL)
            item_text.delete("1.0", END)

            item_text.insert(END, f"You ordered: {item}\n")
            item_text.insert(END, f"Item cost: ${item_cost:.2f}\n")
            item_text.insert(END, f"Current cost: ${total_cost:.2f}\n\n")
            item_text.insert(END, f"Cart: {len(cust_order)} item(s) in cart\n")
            for item, count in item_count.items():
                if count > 1:
                    item_text.insert(END, f"\t{count}x {item}\n")
                else:
                    item_text.insert(END, f"\t{item}\n")
           
            item_text.tag_add("center", "1.0", "end")

            item_text.config(state=DISABLED)
            item_text.see(END)
            
            display_menu()
         
        sporting_event.mainloop()
    
    frames.title("Event Selection")
    frames.geometry(f"{width}x{height}+0+0")


    # Create a label
    label = Label(frames, text="Select a sport:")
    label.pack(anchor="n", pady=10)

    selected_event = StringVar()
    dropdown = ttk.Combobox(frames, textvariable=selected_event)
    dropdown["values"] = ("Football Game", "Basketball Game", "Soccer Game", "Baseball Game", "Softball Game")
    dropdown.pack(anchor="n")

    confirm_button = Button(frames, text="Confirm", command=lambda: confirm(sport), font=("Arial", 12), height=1)
    confirm_button.pack(anchor="n")

    back_button = Button(frames, text="Log Out", command=lambda: go_back(frames), font=("Arial", 12), height=1)
    back_button.pack(anchor="n")

    # Bind the dropdown to a function
    dropdown.bind("<<ComboboxSelected>>", selection_function)

    frames.mainloop()

def show_analytics(sport):
    global sporting_event
    global width
    global height
    sporting_event.destroy()
    sorting = 0
    which_one = 0
    
    def return_to_menu(analytics_window):
        analytics_window.destroy()
        open_sport_page(sport)
        
    def switch_sorting(s):
        nonlocal sorting
        nonlocal which_one
        if which_one == 2:
            report_text2.config(state=NORMAL)
            report_text2.delete(1.0, "end")
            if s == 1:
                sum_query = '''
                SELECT query.sport, query.item_ID, SUM(query.quantity) AS total_quantity, SUM(query.quantity * query.cost) AS item_earnings
                FROM (
                    SELECT ga.sport, oi.item_ID, oi.quantity, oi.cost
                    FROM GAME_ANALYTICS ga
                    JOIN ORDERS o ON ga.game_ID = o.game_ID
                    JOIN ORDERED_ITEMS oi ON o.order_ID = oi.order_ID
                    ) AS query
                GROUP BY query.sport, query.item_ID
                ORDER BY query.item_ID, total_quantity DESC;
                '''
                cursor.execute(sum_query)
                results8 = cursor.fetchall()
                report_text2.insert(END, "SUMMARIZED ITEM PERFORMANCE\n\n")
                if results8:
                    column_width = 20  
                    report_text2.insert(END, "\t\t\t\tItem\t\t          Sport\t\t\t    Quantity\t      Earnings\n\n")
                    for row in results8:
                        sports2 = row[0]
                        sports2 = sports2[0:-5]
                        item_id = row[1]
                        total_quantity = int(row[2])
                        item_earnings = float(row[3])
                        report_text2.insert(END, "\t\t\t\t{:<{width}} {:<{width}} {:<10d} ${:<{width}.2f}\n".format(str(item_id), sports2, total_quantity, item_earnings, width=column_width))
                else:
                    print("No data found.")
                report_text2.tag_configure("bold large", font=("Arial", 14, "bold"))
                report_text2.tag_configure("bold", font=("Arial", 12, "bold"))
                report_text2.tag_configure("center", justify="center")
                report_text2.tag_add("bold large", "1.0", "1.end")
                report_text2.tag_add("bold", "3.0", "3.end")
                report_text2.tag_add("center", "1.0", "1.end")
                report_text2.config(state=DISABLED)
                sorting = 0
            elif s == 0:
                sum_query = '''
                SELECT query.sport, query.item_ID, SUM(query.quantity) AS total_quantity, SUM(query.quantity * query.cost) AS item_earnings
                FROM (
                    SELECT ga.sport, oi.item_ID, oi.quantity, oi.cost
                    FROM GAME_ANALYTICS ga
                    JOIN ORDERS o ON ga.game_ID = o.game_ID
                    JOIN ORDERED_ITEMS oi ON o.order_ID = oi.order_ID
                    ) AS query
                GROUP BY query.sport, query.item_ID
                ORDER BY query.sport, total_quantity DESC;
                '''
                cursor.execute(sum_query)
                results8 = cursor.fetchall()
                report_text2.insert(END, "SUMMARIZED ITEM PERFORMANCE\n\n")
                if results8:
                    column_width = 20  
                    report_text2.insert(END, "\t\t\t\tItem\t\t          Sport\t\t\t    Quantity\t      Earnings\n\n")
                    for row in results8:
                        sports2 = row[0]
                        sports2 = sports2[0:-5]
                        item_id = row[1]
                        total_quantity = int(row[2])
                        item_earnings = float(row[3])
                        report_text2.insert(END, "\t\t\t\t{:<{width}} {:<{width}} {:<10d} ${:<{width}.2f}\n".format(str(item_id), sports2, total_quantity, item_earnings, width=column_width))
                else:
                    print("No data found.")
                report_text2.tag_configure("bold large", font=("Arial", 14, "bold"))
                report_text2.tag_configure("bold", font=("Arial", 12, "bold"))
                report_text2.tag_configure("center", justify="center")
                report_text2.tag_add("bold large", "1.0", "1.end")
                report_text2.tag_add("bold", "3.0", "3.end")
                report_text2.tag_add("center", "1.0", "1.end")
                report_text2.config(state=DISABLED)
                sorting = 1
            else:
                print("Error switching sorting")
        elif which_one == 1:
            report_text2.config(state=NORMAL)
            report_text2.delete(1.0, "end")
            if s == 1:
                query = '''
                SELECT ga.game_ID, ga.sport, ga.away_team, oi.item_ID, oi.quantity, oi.cost
                FROM GAME_ANALYTICS ga
                JOIN ORDERS o ON ga.game_ID = o.game_ID
                JOIN ORDERED_ITEMS oi ON o.order_ID = oi.order_ID
                GROUP BY ga.away_team, oi.item_ID
                ORDER BY ga.away_team;
                '''
                cursor.execute(query)
                results7 = cursor.fetchall()
                if results7:
                    report_text2.insert(END, "INDIVIDUAL ITEM SALES\n\n")
                    report_text2.insert(END, "\t\tDate\t      Sport\t\tAway Team\t\t          Item Name\t\t\t       Quantity\t       Total Item Cost\n\n")
                    for item_data in results7:
                        game_id = item_data[0]
                        date = game_id[4: ]
                        sports2 = item_data[1]
                        sports2 = sports2[0:-5]
                        away_team = item_data[2]
                        item_name = item_data[3]
                        quantity = int(item_data[4])
                        cost = float(item_data[5])
                        report_text2.insert(END, f"\t\t{date:<10} {sports2:<12} {away_team:<20} {item_name:<22} {quantity:<10} ${cost:.2f}\n")
                        
                else:
                    print("No data found.")
                report_text2.tag_configure("bold large", font=("Arial", 14, "bold"))
                report_text2.tag_configure("bold", font=("Arial", 12, "bold"))
                report_text2.tag_configure("center", justify="center")
                report_text2.tag_add("bold large", "1.0", "1.end")
                report_text2.tag_add("bold", "3.0", "3.end")
                report_text2.tag_add("center", "1.0", "1.end")
                report_text2.config(state=DISABLED)
                report_text2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
                
                sorting = 0
            elif s == 0:
                query = '''
                SELECT ga.game_ID, ga.sport, ga.away_team, oi.item_ID, oi.quantity, oi.cost
                FROM GAME_ANALYTICS ga
                JOIN ORDERS o ON ga.game_ID = o.game_ID
                JOIN ORDERED_ITEMS oi ON o.order_ID = oi.order_ID
                GROUP BY ga.away_team, oi.item_ID
                ORDER BY oi.item_ID;
                '''
                cursor.execute(query)
                results7 = cursor.fetchall()
                if results7:
                    report_text2.insert(END, "INDIVIDUAL ITEM SALES\n\n")
                    report_text2.insert(END, "\t\tDate\t      Sport\t\tAway Team\t\t          Item Name\t\t\t       Quantity\t       Total Item Cost\n\n")
                    for item_data in results7:
                        game_id = item_data[0]
                        date = game_id[4: ]
                        sports2 = item_data[1]
                        sports2 = sports2[0:-5]
                        away_team = item_data[2]
                        item_name = item_data[3]
                        quantity = int(item_data[4])
                        cost = float(item_data[5])
                        report_text2.insert(END, f"\t\t{date:<10} {sports2:<12} {away_team:<20} {item_name:<22} {quantity:<10} ${cost:.2f}\n")
                        
                else:
                    print("No data found.")
                report_text2.tag_configure("bold large", font=("Arial", 14, "bold"))
                report_text2.tag_configure("bold", font=("Arial", 12, "bold"))
                report_text2.tag_configure("center", justify="center")
                report_text2.tag_add("bold large", "1.0", "1.end")
                report_text2.tag_add("bold", "3.0", "3.end")
                report_text2.tag_add("center", "1.0", "1.end")
                report_text2.config(state=DISABLED)
                report_text2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
                
                sorting = 1
        elif which_one == 0:
            messagebox.showerror("Error", "No Report Selected")

    
    analytics_window = Tk()
    analytics_window.geometry(f"{width}x{height}+0+0")
    analytics_window.title("Database Reports")
    analytics_window.rowconfigure(0, weight=1)

    reports_frame = Frame(analytics_window)
    reports_frame.grid(row=0, column=1, sticky="nsew")    

    top_sellers = '''
        SELECT item_ID, SUM(quantity) AS total_sold
        FROM ORDERED_ITEMS
        GROUP BY item_ID
        HAVING total_sold = (
            SELECT SUM(quantity) AS total_sold
            FROM ORDERED_ITEMS
            GROUP BY item_ID
            ORDER BY total_sold DESC
            LIMIT 1
        )
        '''

    cursor.execute(top_sellers)
    results1 = cursor.fetchall()

    
    min_sellers =  '''
        SELECT item_ID, SUM(quantity) AS total_sold
        FROM ORDERED_ITEMS
        GROUP BY item_ID
        HAVING total_sold = (
            SELECT SUM(quantity) AS total_sold
            FROM ORDERED_ITEMS
            GROUP BY item_ID
            ORDER BY total_sold ASC
            LIMIT 1
        )
        '''
    
    cursor.execute(min_sellers)
    results3 = cursor.fetchall()

    
    average_away_team =  '''SELECT away_team, AVG(earnings) AS average_earnings
    FROM GAME_ANALYTICS
    GROUP BY away_team
    ORDER BY average_earnings DESC'''
    
    cursor.execute(average_away_team)
    results5 = cursor.fetchall()
    
    
    average_sport =  '''SELECT sport, AVG(earnings) AS average_earnings
    FROM GAME_ANALYTICS
    GROUP BY sport
    ORDER BY average_earnings DESC'''

    cursor.execute(average_sport)
    results6 = cursor.fetchall()


    query = '''
    SELECT ga.game_ID, ga.sport, ga.away_team, oi.item_ID, oi.quantity, oi.cost
    FROM GAME_ANALYTICS ga
    JOIN ORDERS o ON ga.game_ID = o.game_ID
    JOIN ORDERED_ITEMS oi ON o.order_ID = oi.order_ID
    GROUP BY ga.away_team, oi.item_ID
    ORDER BY ga.away_team;
    '''
    cursor.execute(query)
    results7 = cursor.fetchall()
    
    sum_query = '''
    SELECT query.sport, query.item_ID, SUM(query.quantity) AS total_quantity, SUM(query.quantity * query.cost) AS item_earnings
    FROM (
        SELECT ga.sport, oi.item_ID, oi.quantity, oi.cost
        FROM GAME_ANALYTICS ga
        JOIN ORDERS o ON ga.game_ID = o.game_ID
        JOIN ORDERED_ITEMS oi ON o.order_ID = oi.order_ID
        ) AS query
    GROUP BY query.sport, query.item_ID
    ORDER BY query.item_ID, total_quantity DESC;
    '''
    cursor.execute(sum_query)
    results8 = cursor.fetchall()

    report_text1 = Text(reports_frame, width=40, height=40)
    report_text1.config(state=NORMAL)
    report_text1.insert(END, "GENERAL SALES REPORTS\n\n")
    
    if results1:
        report_text1.insert(END, "TOP SELLING ITEM(s):\n")
        for result in results1:
            item = result[0]
            total_sold = result[1]
            report_text1.insert(END, f"{item}: {total_sold} Sold\n")
    else:
        print("No data found for Top Seller.")
        
    report_text1.insert(END, "\n\n")
        
    
    if results3:
        report_text1.insert(END, "LOWEST SELLING ITEM(s):\n")
        for result in results3:
            item = result[0]
            total_sold = result[1]
            report_text1.insert(END, f"{item}: {total_sold} Sold\n")
    else:
        print("No data found for Lowest Seller")
        
    report_text1.insert(END, "\n\n")
        
    if results5:
        report_text1.insert(END, "AVERAGE EARNINGS PER AWAY TEAM:\n")
        for result in results5:
            away_team = result[0]
            avg_earnings = float(result[1])
            report_text1.insert(END, f"{away_team}: ${avg_earnings:.2f} \n")
    else:
        print("No data found for Away Team Earnings")
        
    report_text1.insert(END, "\n\n")
        
    if results6:
        report_text1.insert(END, "AVERAGE EARNINGS PER SPORT:\n")
        for result in results6:
            sports = result[0]
            avg_earnings = float(result[1])
            report_text1.insert(END, f"{sports}: ${avg_earnings:.2f} \n")
    else:
        print("No data found for Sport Earnings")
        
    report_text1.tag_configure("bold", font=("Arial", 14, "bold"))
    report_text1.tag_configure("center", justify="center", wrap="word")
    report_text1.tag_add("bold", "1.0", "1.25")
    report_text1.tag_add("center", "1.0", "end")
    report_text1.config(state=DISABLED)
    
    report_text2 = Text(reports_frame, width=120, height=40)
        
    def select_report(report):
        nonlocal which_one
        if which_one != report: 
            report_text2.config(state=NORMAL)
            report_text2.delete('1.0', END)
            if report == 1:
                report_text2.insert(END, "INDIVIDUAL ITEM SALES\n\n")
                if results7:
                    report_text2.insert(END, "\t\tDate\t      Sport\t\tAway Team\t\t          Item Name\t\t\t       Quantity\t       Total Item Cost\n\n")
                    for item_data in results7:
                        game_id = item_data[0]
                        date = game_id[4: ]
                        sports2 = item_data[1]
                        sports2 = sports2[0:-5]
                        away_team = item_data[2]
                        item_name = item_data[3]
                        quantity = int(item_data[4])
                        cost = float(item_data[5])
                        report_text2.insert(END, f"\t\t{date:<10} {sports2:<12} {away_team:<20} {item_name:<22} {quantity:<10} ${cost:.2f}\n")
                        
                else:
                    print("No data found.")
                report_text2.tag_configure("bold large", font=("Arial", 14, "bold"))
                report_text2.tag_configure("bold", font=("Arial", 12, "bold"))
                report_text2.tag_configure("center", justify="center")
                report_text2.tag_add("bold large", "1.0", "1.end")
                report_text2.tag_add("bold", "3.0", "3.end")
                report_text2.tag_add("center", "1.0", "1.end")
                report_text2.config(state=DISABLED)
                report_text2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
                which_one = 1
            elif report == 2:
                report_text2.insert(END, "SUMMARIZED ITEM PERFORMANCE\n\n")
                
                if results8:
                    column_width = 20  
                    report_text2.insert(END, "\t\t\t\tItem\t\t          Sport\t\t\t    Quantity\t      Earnings\n\n")
                    for row in results8:
                        sports2 = row[0]
                        sports2 = sports2[0:-5]
                        item_id = row[1]
                        total_quantity = int(row[2])
                        item_earnings = float(row[3])
                        report_text2.insert(END, "\t\t\t\t{:<{width}} {:<{width}} {:<10d} ${:<{width}.2f}\n".format(str(item_id), sports2, total_quantity, item_earnings, width=column_width))
                else:
                    print("No data found.")
                report_text2.tag_configure("bold large", font=("Arial", 14, "bold"))
                report_text2.tag_configure("bold", font=("Arial", 12, "bold"))
                report_text2.tag_configure("center", justify="center")
                report_text2.tag_add("bold large", "1.0", "1.end")
                report_text2.tag_add("bold", "3.0", "3.end")
                report_text2.tag_add("center", "1.0", "1.end")
                report_text2.config(state=DISABLED)
                which_one = 2

    
    sorting_button = Button(analytics_window, text="Switch Table Sorting", command=lambda: switch_sorting(sorting), font=("Arial", 12), height=1)
    report_text1.grid(row=0, column=0, padx=(200, 10), pady=10, sticky="nsew")
    report_text2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    sorting_button.grid(row=2, column=1)
    big_button = Button(analytics_window, text="Individual Sales Report", command=lambda: select_report(1), font=("Arial", 12), height=1)
    small_button = Button(analytics_window, text="Summarized Sales Report", command=lambda: select_report(2), font=("Arial", 12), height=1)
    back_button = Button(analytics_window, text="Go Back", command=lambda: return_to_menu(analytics_window), font=("Arial", 12), height=1)
    big_button.grid(row=1, column=1, padx=(0,275), pady=(0,50))
    small_button.grid(row=1, column=1, padx=(275,0), pady=(0,50))
    back_button.grid(row=3, column=1, pady=(0,10))

    analytics_window.mainloop()

    
def manage_menu(sport):
    global sporting_event
    global menu_items
    global inventory_items
    global width
    global height
    sporting_event.destroy()

    if sport == "Football Game":
        menu_items = [f"{item}: ${float(price):.2f}\n" for item, price, item_type in football_menu]
    elif sport == "Basketball Game":
        menu_items = [f"{item}: ${float(price):.2f}\n" for item, price, item_type in basketball_menu]
    elif sport == "Soccer Game":
        menu_items = [f"{item}: ${float(price):.2f}\n" for item, price, item_type in soccer_menu]
    elif sport == "Baseball Game" or sport == "Softball Game":
        menu_items = [f"{item}: ${float(price):.2f}\n" for item, price, item_type in baseball_menu]
    else:
        return
    
    cursor.execute("SELECT ITEM, PRICE, ITEM_TYPE FROM ITEMS")
    all_items = cursor.fetchall()
    all_items = [(item, price, item_type) for item, price, item_type in all_items]
    all_items = {item: (price, item_type) for item, price, item_type in all_items}
    

    def return_to_menu():
        adminmenu_window.destroy()
        open_sport_page(sport)
        
    def refresh_menu(menu_text, inventory_text):
        nonlocal sport
        global menu_items
        global football_menu
        global basketball_menu
        global soccer_menu
        global baseball_menu
        global inventory_items

        menu_text.config(state=NORMAL)
        inventory_text.config(state=NORMAL)
        menu_text.delete('1.0', END)
        inventory_text.delete('1.0', END)

        if sport == "Football Game":
            menu_items = [f"{item}: ${float(price):.2f}" if isinstance(price, float) else f"{item}: ${float(price):.2f}" for item, price, item_type in football_menu]
        elif sport == "Basketball Game":
            menu_items = [f"{item}: ${float(price):.2f}" if isinstance(price, float) else f"{item}: ${float(price):.2f}" for item, price, item_type in basketball_menu]
        elif sport == "Soccer Game":
           menu_items = [f"{item}: ${float(price):.2f}" if isinstance(price, float) else f"{item}: ${float(price):.2f}" for item, price, item_type in soccer_menu]
        elif sport == "Baseball Game" or sport == "Softball Game":
            menu_items = [f"{item}: ${float(price):.2f}" if isinstance(price, float) else f"{item}: ${float(price):.2f}" for item, price, item_type in baseball_menu]
        else:
            return
        
        cursor.execute("SELECT ITEM, QUANTITY FROM INVENTORY")
        inventory_items = cursor.fetchall()
        
        menu_text.insert(END, f"{sport} Menu:\n\n\n")
        menu_text.insert(END, '\n'.join(menu_items))
        menu_text.tag_configure("center", justify='center')
        menu_text.tag_add("center", "1.0", "end")
        menu_text.config(state=DISABLED)
        
        inventory_text.insert(END, "Inventory:\n\n\n")
        inventory_items_formatted = [f"{item[0]} - {item[1]}" for item in inventory_items]
        inventory_text.insert(END, '\n'.join(inventory_items_formatted))
        inventory_text.tag_configure("center", justify='center')
        inventory_text.tag_add("center", "1.0", "end")
        inventory_text.config(state=DISABLED)

    def open_manage_menu_window(manage_menu_button):
        nonlocal sport
        global menu_items
        global inventory_items
        global width
        global height
        manage_menu_button.destroy()

        def update_price():
            global menu_items
            global football_menu
            global basketball_menu
            global soccer_menu
            global baseball_menu
            nonlocal sport
            item_name = item_dropdown.get()
            new_price = float(price_entry.get())
            if sport == "Football Game":
                for i, (item, price, item_type) in enumerate(football_menu):
                    if item == item_name:
                        football_menu[i] = (item_name, new_price, item_type)
                        cursor.execute("UPDATE ITEMS SET PRICE = ? WHERE ITEM = ?", (new_price, item_name))
                        break
            elif sport == "Basketball Game":
                for i, (item, price, item_type) in enumerate(basketball_menu):
                    if item == item_name:
                        basketball_menu[i] = (item_name, new_price, item_type)
                        cursor.execute("UPDATE ITEMS SET PRICE = ? WHERE ITEM = ?", (new_price, item_name))
                        break
            elif sport == "Soccer Game":
                for i, (item, price, item_type) in enumerate(soccer_menu):
                    if item == item_name:
                        soccer_menu[i] = (item_name, new_price, item_type)
                        cursor.execute("UPDATE ITEMS SET PRICE = ? WHERE ITEM = ?", (new_price, item_name))
                        break
            elif sport == "Baseball Game" or sport == "Softball Game":
                for i, (item, price, item_type) in enumerate(baseball_menu):
                    if item == item_name:
                        baseball_menu[i] = (item_name, new_price, item_type)
                        cursor.execute("UPDATE ITEMS SET PRICE = ? WHERE ITEM = ?", (new_price, item_name))
                        break
            else:
                return
            conn.commit()
            messagebox.showinfo("Success", "Price updated successfully.")
            refresh_menu(menu_text, inventory_text)

        def update_quantity():
            nonlocal sport
            global menu_items       
            item = item_dropdown.get()
            quantity = int(inventory_entry.get())
            cursor.execute("UPDATE INVENTORY SET QUANTITY = ? where ITEM = ?", (quantity, item))
            conn.commit() 
            messagebox.showinfo("Success", "Inventory updated successfully.")
            refresh_menu(menu_text, inventory_text)

        def add_item():
            nonlocal sport
            global menu_items
            global football_menu
            global basketball_menu
            global soccer_menu
            global baseball_menu
            # check if item is already in inventory/menu table and if it is just add it from that row...
            new_item = item_entry.get()
            new_price = price_entry.get()
            item_type = type_entry.get()
            inventory_amount = inventory_entry.get()

            if new_item == "" or new_price == "" or item_type == "" or inventory_amount == "":
                messagebox.showerror("Error", "Please fill in all the fields.")
                return

            try:
                new_price = float(new_price)
            except ValueError:
                messagebox.showerror("Error", "Invalid price format.")
                return

            cursor.execute("SELECT ITEM FROM ITEMS WHERE ITEM = ?", (new_item,))
            result = cursor.fetchone()
            
            if result is not None:
                messagebox.showerror("Error", "Item already exists")
                return
            else:
                cursor.execute("INSERT INTO ITEMS (ITEM, PRICE, ITEM_TYPE) VALUES (?, ?, ?)", (new_item, new_price, item_type))
                cursor.execute("INSERT INTO INVENTORY (ITEM, QUANTITY) VALUES (?, ?)", (new_item, inventory_amount))
                if sport == "Football Game":
                    football_menu.append((new_item, new_price, item_type))
                elif sport == "Basketball Game":
                    basketball_menu.append((new_item, new_price, item_type))
                elif sport == "Soccer Game":
                    soccer_menu.append((new_item, new_price, item_type))
                elif sport == "Baseball Game" or sport == "Softball Game":
                    baseball_menu.append((new_item, new_price, item_type))
                else:
                    return
                conn.commit() 
                messagebox.showinfo("Success", "Item added successfully.")
                refresh_menu(menu_text, inventory_text)
            
        def transfer_item():
            nonlocal sport
            global football_menu
            global basketball_menu
            global soccer_menu
            global baseball_menu
            item_name = item_dropdown2.get()
            
            cursor.execute("SELECT PRICE, ITEM_TYPE FROM ITEMS WHERE ITEM = ?", (item_name,))
            result = cursor.fetchone()
            
            if result:
                price, item_type = result

                if sport == "Football Game":
                    football_menu.append((item_name, price, item_type))
                elif sport == "Basketball Game":
                    basketball_menu.append((item_name, price, item_type))
                elif sport == "Soccer Game":
                    soccer_menu.append((item_name, price, item_type))
                elif sport == "Baseball Game" or sport == "Softball Game":
                    baseball_menu.append((item_name, price, item_type))
                else:
                    return
            
            conn.commit()
            messagebox.showinfo("Success", "Item added successfully.")
            refresh_menu(menu_text, inventory_text)

        def remove_item():
            nonlocal sport
            global menu_items
            global football_menu
            global basketball_menu
            global soccer_menu
            global baseball_menu            
            item_name = item_dropdown.get()
            if sport == "Football Game":
                for i, (item, price, item_type) in enumerate(football_menu):
                    if item == item_name:
                        del football_menu[i]
                        break
            elif sport == "Basketball Game":
                for i, (item, price, item_type) in enumerate(basketball_menu):
                    if item == item_name:
                        del basketball_menu[i]
                        break
            elif sport == "Soccer Game":
                for i, (item, price, item_type) in enumerate(soccer_menu):
                    if item == item_name:
                        del soccer_menu[i]
                        break
            elif sport == "Baseball Game" or sport == "Softball Game":
                for i, (item, price, item_type) in enumerate(baseball_menu):
                    if item == item_name:
                        del baseball_menu[i]
                        break
            else:
                return
            conn.commit()
            messagebox.showinfo("Success", "Item removed successfully.")
            refresh_menu(menu_text, inventory_text)

        # Manage menu frame
        manage_menu_frame = Frame(adminmenu_window, padx=180, pady=10)
        manage_menu_frame.grid(row=0, column=1, sticky="n")

        # Dropdown menu for item selection
        item_label = Label(manage_menu_frame, text="Select Item:")
        item_label.grid(row=0, column=0)
        item_names = [item.split(":")[0] for item in menu_items]
        item_dropdown = ttk.Combobox(manage_menu_frame, values=item_names, state="readonly")
        item_dropdown.grid(row=0, column=1)

        # Item entry
        item_entry_label = Label(manage_menu_frame, text="New Item:")
        item_entry_label.grid(row=1, column=0)
        item_entry = Entry(manage_menu_frame)
        item_entry.grid(row=1, column=1)

        # Price entry
        price_label = Label(manage_menu_frame, text="Price:")
        price_label.grid(row=2, column=0)
        price_entry = Entry(manage_menu_frame)
        price_entry.grid(row=2, column=1)
        
        inventory_label = Label(manage_menu_frame, text="Inventory Quantity:")
        inventory_label.grid(row=3, column=0)
        inventory_entry = Entry(manage_menu_frame)
        inventory_entry.grid(row=3, column=1)
        
        type_label = Label(manage_menu_frame, text="Item Type:")
        type_label.grid(row=4, column=0)
        item_type_text = StringVar()
        type_entry = ttk.Combobox(manage_menu_frame, textvariable=item_type_text)
        type_entry["values"] = ('drink', 'food', 'snack')
        type_entry.grid(row=4, column=1)
        type_entry.current(0)

        # Update price button
        update_button = Button(manage_menu_frame, text="Update Price", command=update_price)
        update_button.grid(row=5, column=0, columnspan=2)
        
        inventory_button = Button(manage_menu_frame, text="Update Inventory", command=update_quantity)
        inventory_button.grid(row=6, column=0, columnspan=2)

        # Add item button
        add_button = Button(manage_menu_frame, text="Add Item", command=add_item)
        add_button.grid(row=7, column=0, columnspan=2)

        # Remove item button
        remove_button = Button(manage_menu_frame, text="Remove Item", command=remove_item)
        remove_button.grid(row=8, column=0, columnspan=2)
        
        empty_row = Label(manage_menu_frame)
        empty_row.grid(row=9, pady=30)
        
        item_label2 = Label(manage_menu_frame, text="Select Item not in Menu:")
        item_label2.grid(row=13, column=0)
        missing_items = set(all_items.keys()) - set(item.split(":")[0] for item in menu_items)
        missing_item_names = [item_name for item_name in missing_items]
        item_dropdown2 = ttk.Combobox(manage_menu_frame, values=missing_item_names, state="readonly")
        item_dropdown2.grid(row=13, column=1)
        
        transfer_button = Button(manage_menu_frame, text="Transfer Item", command=transfer_item)
        transfer_button.grid(row=14, column=0, columnspan=2)


    # Main GUI window
    adminmenu_window = Tk()
    adminmenu_window.geometry(f"{width}x{height}+0+0")
    adminmenu_window.title("Concession Stand Menu")

    adminmenu_window.columnconfigure(0, weight=1)
    adminmenu_window.rowconfigure(0, weight=1)

    menu_frame = Frame(adminmenu_window)
    menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    menu_text = Text(menu_frame, width=40, height=40)
    menu_text.config(state=NORMAL)
    menu_text.insert(END, f"{sport} Menu:\n\n\n")
    for item in menu_items:
        menu_text.insert(END, item)
    menu_text.tag_configure("center", justify="center", wrap="word")     
    menu_text.tag_add("center", "1.0", "end")
    menu_text.config(state=DISABLED)

    inventory_text = Text(menu_frame, width=40, height=40) 
    inventory_text.config(state=NORMAL)
    inventory_text.insert(END, "Inventory:\n\n\n")
    for item, quantity in inventory_items:
        inventory_display = f"{item} - {quantity}"
        inventory_text.insert(END, inventory_display + "\n")
    inventory_text.tag_configure("center", justify="center", wrap="word")     
    inventory_text.tag_add("center", "1.0", "end")
    inventory_text.config(state=DISABLED)

    # Adjust the grid layout for the text widgets
    menu_text.grid(row=0, column=1, padx=40, pady=10, sticky="nsew")
    inventory_text.grid(row=0, column=0, padx=40, pady=10, sticky="nsew")

    manage_menu_button = Button(adminmenu_window, text=f"Manage {sport} Menu", command=lambda:open_manage_menu_window(manage_menu_button))
    manage_menu_button.grid(row=1, column=0, pady=10)

    back_button = Button(adminmenu_window, text="Go Back", command=return_to_menu, font=("Arial", 12), height=1)
    back_button.grid(row=2, column=0, pady=10)

    adminmenu_window.mainloop()
   

    
def login(window):
    window.destroy()
    global width
    global height

    # Create the login window
    login_window = Tk()
    login_window.geometry(f"{width}x{height}+0+0")
    login_window.title("Sunbelt Snack Station")
    
    # Function to handle login submit button click
    def user_login():
        global is_admin
        global selected_sport
        username = username_entry.get()
        password = password_entry.get()
     
        # Check if any users exist
        cursor.execute("SELECT COUNT(*) FROM USERS")
        result = cursor.fetchone()

        if result[0] == 0:
            messagebox.showerror("No users found.")
            login_window.destroy()
            main_menu()

        # Check if the username and password match
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user and existing_user[1] == password:

            if existing_user[2] == 'Yes':
                messagebox.showinfo("Login Successful", f"Hey {username}!\nLogin successful.")
                is_admin = "yes"
            else:
                messagebox.showinfo("Login Successful", f"Hey!\nLogin successful.")


            login_window.destroy()
            event_selection(selected_sport)
         
        elif not existing_user:
            messagebox.showerror("Login Failed", "User not found")
        else:
            messagebox.showerror("Login Failed", "Try Again.")
    
    def go_back():
        login_window.destroy()
        main_menu()
    
    # Create login labels and entry fields
    username_label = Label(login_window, text="Username:")
    username_entry = Entry(login_window)
    password_label = Label(login_window, text="Password:")
    password_entry = Entry(login_window)
    confirm_button = Button(login_window, text="Confirm", command=user_login)
    back_button = Button(login_window, text="Go Back", command=go_back)

    # Place the login labels and entry fields in the login window
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    confirm_button.pack()
    back_button.pack()

    login_window.mainloop()
         

def registerGUI(window):
    window.destroy()
    global width
    global height
    register_window = Tk()
    register_window.geometry(f"{width}x{height}+0+0")
    register_window.title("Sunbelt Snack Station")
    
    def go_back():
        register_window.destroy()
        main_menu()
    
    def register():
        global username
        global password
        username = username_entry.get()
        password = password_entry.get()
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Registration Failed", "Username already taken")
        else:
            if len(password) < 8:
                messagebox.showerror("Registration Failed", "Password must be at least 8 characters long.")
            elif not any(char in specialChar for char in password):
                messagebox.showerror("Registration Failed", "Password must contain a special character.")
            else:
                cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, IS_ADMIN) VALUES (?, ?, ?)", (username, password, 'No'))
                conn.commit()
                messagebox.showinfo("Registration Successful", "User registered successfully")
                register_window.destroy()
                main_menu()

    
    username_label = Label(register_window, text="Username:")
    username_entry = Entry(register_window)
    password_label = Label(register_window, text="Password:")
    password_entry = Entry(register_window)
    create_button = Button(register_window, text="Create User", command=register)
    back_button = Button(register_window, text="Go Back", command=go_back)
     
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    create_button.pack()
    back_button.pack()
     
    register_window.mainloop()
    
def adminGUI(window):
    window.destroy()
    global width
    global height
    admin_window = Tk()
    admin_window.geometry(f"{width}x{height}+0+0")
    admin_window.title("Sunbelt Snack Station")
    
    def go_back():
        admin_window.destroy()
        main_menu()
    
    def register():
        global username
        global password
        username = username_entry.get()
        password = password_entry.get()
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Registration Failed", "Username already taken")
        else:
            if len(password) < 8:
                messagebox.showerror("Registration Failed", "Password must be at least 8 characters long.")
            elif not any(char in specialChar for char in password):
                messagebox.showerror("Registration Failed", "Password must contain a special character.")
            else:
                cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, IS_ADMIN) VALUES (?, ?, ?)", (username, password, 'Yes'))
                conn.commit()
                messagebox.showinfo("Registration Successful", "User registered successfully")
                admin_window.destroy()
                main_menu()
    
    username_label = Label(admin_window, text="Username:")
    username_entry = Entry(admin_window)
    password_label = Label(admin_window, text="Password:")
    password_entry = Entry(admin_window)
    create_button = Button(admin_window, text="Create User", command=register)
    back_button = Button(admin_window, text="Go Back", command=go_back)
     
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    create_button.pack()
    back_button.pack()
     
    admin_window.mainloop()

def main_menu():
    global username
    global password
    global is_admin
    global machine_on
    global width
    global height
    username = ' '
    password = ' '
    is_admin = "No"

    def quit_window(window):
        global machine_on
        machine_on = 'no'
        window.destroy()
    
    window = Tk()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight() - 100
    window.geometry(f"{width}x{height}+0+0")
    window.title("Sunbelt Snack Station")
    admin_register = Button(window, text="Admin Register", command=lambda: adminGUI(window))
    register_button = Button(window, text="Register", command=lambda: registerGUI(window))
    login_button = Button(window, text="Login", command=lambda: login(window))
    quit_button = Button(window, text="Quit", command=lambda: quit_window(window))

    text_area = Label(window, text="\nWelcome!\n\nWhat would you like to do?\n", font=("Arial", 16, "bold"))
    text_area.pack()

    register_button.pack()
    admin_register.pack()
    login_button.pack()
    quit_button.pack()

    window.mainloop()

machine_on = 'yes'

while machine_on == 'yes':
    main_menu()

cursor.close()
conn.close()





