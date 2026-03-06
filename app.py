from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import datetime
import os

app = Flask(__name__)
app.secret_key = 'sunbelt-snack-station-secret-2024'

DATABASE = 'concession_stand.db'

SPECIAL_CHARS = ['$', '#', '@', '!', '*', '%']

SPORT_MENUS = {
    'Football Game': [
        ('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'),
        ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'), ('Tea', 2.00, 'drink'),
        ('Coffee', 1.00, 'drink'), ('Hot Chocolate', 2.00, 'drink'),
        ('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'), ('Hot Dog', 2.00, 'food'),
        ('Pepperoni Pizza', 4.00, 'food'), ('Cheese Pizza', 3.00, 'food'),
        ('Cheesesteak', 4.00, 'food'), ('Pickles', 2.00, 'food'),
        ('Donnie Coleman BBQ', 5.00, 'food'),
        ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'), ('Hersheys', 2.00, 'snack'),
        ('Skittles', 2.00, 'snack'), ('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'),
        ('Nachos', 3.00, 'snack'), ('French Fries', 2.00, 'snack'),
        ('Pretzel', 3.00, 'snack'), ('Pretzel with Cheese', 4.00, 'snack'), ('Chips', 1.00, 'snack'),
    ],
    'Basketball Game': [
        ('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'),
        ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'),
        ('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'), ('Hot Dog', 2.00, 'food'),
        ('Pickles', 2.00, 'food'),
        ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'), ('Hersheys', 2.00, 'snack'),
        ('Skittles', 2.00, 'snack'), ('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'),
        ('Nachos', 3.00, 'snack'),
    ],
    'Soccer Game': [
        ('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'),
        ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'), ('Tea', 2.00, 'drink'),
        ('Coffee', 1.00, 'drink'),
        ('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'), ('Hot Dog', 2.00, 'food'),
        ('Pepperoni Pizza', 4.00, 'food'), ('Cheese Pizza', 3.00, 'food'),
        ('Donnie Coleman BBQ', 5.00, 'food'),
        ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'), ('Hersheys', 2.00, 'snack'),
        ('Skittles', 2.00, 'snack'), ('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'),
        ('Nachos', 3.00, 'snack'), ('Chips', 1.00, 'snack'),
    ],
    'Baseball Game': [
        ('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'),
        ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'), ('Tea', 2.00, 'drink'),
        ('Coffee', 1.00, 'drink'),
        ('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'), ('Hot Dog', 2.00, 'food'),
        ('Pepperoni Pizza', 4.00, 'food'), ('Cheese Pizza', 3.00, 'food'),
        ('Donnie Coleman BBQ', 5.00, 'food'),
        ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'), ('Chewing Gum', 2.00, 'snack'),
        ('Skittles', 2.00, 'snack'), ('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'),
        ('Sunflower Seeds', 2.00, 'snack'), ('Chips', 1.00, 'snack'),
    ],
    'Softball Game': [
        ('Gatorade', 2.00, 'drink'), ('Pepsi', 2.00, 'drink'), ('Diet Pepsi', 2.00, 'drink'),
        ('Dr. Wham', 2.00, 'drink'), ('Starry', 2.00, 'drink'), ('Tea', 2.00, 'drink'),
        ('Coffee', 1.00, 'drink'),
        ('Hamburger', 3.00, 'food'), ('Cheeseburger', 4.00, 'food'), ('Hot Dog', 2.00, 'food'),
        ('Pepperoni Pizza', 4.00, 'food'), ('Cheese Pizza', 3.00, 'food'),
        ('Donnie Coleman BBQ', 5.00, 'food'),
        ('Popcorn', 1.00, 'snack'), ('M&Ms', 2.00, 'snack'), ('Chewing Gum', 2.00, 'snack'),
        ('Skittles', 2.00, 'snack'), ('Reeses Cup', 2.00, 'snack'), ('Tootsie Pop', 1.00, 'snack'),
        ('Sunflower Seeds', 2.00, 'snack'), ('Chips', 1.00, 'snack'),
    ],
}

AWAY_TEAMS = {
    "East Rockingham": 1, "Harrisonburg": 2, "Rockbridge County": 3,
    "Spotswood": 4, "Turner Ashby": 5, "William Monroe": 6
}

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS ITEMS (
        ITEM_ID INTEGER PRIMARY KEY, ITEM TEXT NOT NULL,
        PRICE TEXT NOT NULL, ITEM_TYPE TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS INVENTORY (
        ITEM TEXT PRIMARY KEY, QUANTITY INTEGER NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS INVENTORY_ITEMS (
        ITEM_ID INTEGER NOT NULL, ITEM TEXT NOT NULL,
        FOREIGN KEY (ITEM_ID) REFERENCES ITEMS(ITEM_ID),
        FOREIGN KEY (ITEM) REFERENCES INVENTORY(ITEM))''')
    c.execute('''CREATE TABLE IF NOT EXISTS GAME_ANALYTICS (
        game_ID TEXT PRIMARY KEY, sport TEXT NOT NULL,
        away_team TEXT, order_count INTEGER, earnings FLOAT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ORDERS (
        order_ID int PRIMARY KEY, game_ID TEXT NOT NULL, total_cost float)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ORDERED_ITEMS (
        order_ID int NOT NULL, item_ID TEXT NOT NULL,
        quantity int NOT NULL, cost float NOT NULL,
        FOREIGN KEY (order_ID) REFERENCES ORDERS(order_ID),
        FOREIGN KEY (item_ID) REFERENCES ITEMS(ITEM_ID))''')
    c.execute('''CREATE TABLE IF NOT EXISTS USERS (
        USERNAME TEXT PRIMARY KEY UNIQUE, PASSWORD TEXT NOT NULL, IS_ADMIN TEXT NOT NULL)''')

    # Seed items
    all_items = set()
    for menu in SPORT_MENUS.values():
        for item, price, item_type in menu:
            if item not in all_items:
                all_items.add(item)
                c.execute("SELECT ITEM FROM ITEMS WHERE ITEM = ?", (item,))
                if not c.fetchone():
                    c.execute("INSERT INTO ITEMS (ITEM, PRICE, ITEM_TYPE) VALUES (?, ?, ?)", (item, price, item_type))

    # Seed inventory
    inventory_seeds = [
        ('Gatorade',100),('Pepsi',100),('Diet Pepsi',100),('Dr. Wham',100),('Starry',100),
        ('Tea',100),('Coffee',100),('Hamburger Buns',100),('Burger Patties',100),
        ('Cheese Slices',100),('Hot Dog Buns',100),('Hot Dogs',100),('Popcorn',100),
        ('M&Ms',100),('Hersheys',100),('Skittles',100),('Reeses Cup',100),('Tootsie Pop',100),
        ('Nachos',100),('French Fries',100),('Cheesesteak',100),('Pretzel',100),
        ('Pretzel with Cheese',100),('Hot Chocolate',100),('Pickles',100),('Chips',100),
        ('Sunflower Seeds',100),('Gum',100),('Donnie Coleman BBQ',100),('Pepperoni Pizza',100),
        ('Cheese Pizza',100),('Chewing Gum',100),
    ]
    for item, qty in inventory_seeds:
        c.execute("SELECT ITEM FROM INVENTORY WHERE ITEM = ?", (item,))
        if not c.fetchone():
            c.execute("INSERT INTO INVENTORY (ITEM, QUANTITY) VALUES (?, ?)", (item, qty))

    # Seed ingredient mappings
    item_mappings = {
        'Hamburger': ['Hamburger Buns', 'Burger Patties'],
        'Cheeseburger': ['Hamburger Buns', 'Burger Patties', 'Cheese Slices'],
        'Hot Dog': ['Hot Dog Buns', 'Hot Dogs'],
    }
    for item_name, ingredients in item_mappings.items():
        row = c.execute("SELECT ITEM_ID FROM ITEMS WHERE ITEM = ?", (item_name,)).fetchone()
        if row:
            item_id = row[0]
            for ing in ingredients:
                c.execute("SELECT ITEM FROM INVENTORY_ITEMS WHERE ITEM = ? AND ITEM_ID = ?", (ing, item_id))
                if not c.fetchone():
                    c.execute("INSERT INTO INVENTORY_ITEMS (ITEM_ID, ITEM) VALUES (?, ?)", (item_id, ing))

    conn.commit()
    conn.close()

def generate_game_id(gender, sport, away_team, level):
    prefixes = {'Football Game': '1', 'Baseball Game': '2', 'Softball Game': '2',
                'Basketball Game': '3', 'Soccer Game': '4'}
    prefix = prefixes.get(sport, '0')
    suffix = 'M' if gender == "Men's" else 'W'
    lvl = 'J' if level == 'JV' else 'V'
    team_number = AWAY_TEAMS.get(away_team, 0)
    date = datetime.date.today().strftime('%m/%d/%y')
    return f"{prefix}{suffix}{lvl}{team_number}{date}"

def update_inventory(cursor, item):
    row = cursor.execute("SELECT ITEM_ID FROM ITEMS WHERE ITEM = ?", (item,)).fetchone()
    if row:
        item_id = row[0]
        ingredients = cursor.execute("SELECT ITEM FROM INVENTORY_ITEMS WHERE ITEM_ID = ?", (item_id,)).fetchall()
        if ingredients:
            for ing in ingredients:
                cursor.execute("UPDATE INVENTORY SET QUANTITY = QUANTITY - 1 WHERE ITEM = ?", (ing[0],))
        else:
            cursor.execute("UPDATE INVENTORY SET QUANTITY = QUANTITY - 1 WHERE ITEM = ?", (item,))

# ── ROUTES ──────────────────────────────────────────────

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        is_admin_reg = request.form.get('is_admin', 'No')
        error = None
        if len(password) < 8:
            error = 'Password must be at least 8 characters.'
        elif not any(c in SPECIAL_CHARS for c in password):
            error = 'Password must contain a special character ($ # @ ! * %).'
        else:
            conn = get_db()
            existing = conn.execute("SELECT USERNAME FROM USERS WHERE USERNAME = ?", (username,)).fetchone()
            if existing:
                error = 'Username already taken.'
            else:
                conn.execute("INSERT INTO USERS (USERNAME, PASSWORD, IS_ADMIN) VALUES (?, ?, ?)",
                             (username, password, is_admin_reg))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
            conn.close()
        return render_template('register.html', error=error, is_admin_page=(is_admin_reg == 'Yes'))
    is_admin_page = request.args.get('admin', 'false') == 'true'
    return render_template('register.html', error=None, is_admin_page=is_admin_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        conn = get_db()
        user = conn.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,)).fetchone()
        conn.close()
        if user and user['PASSWORD'] == password:
            session['username'] = username
            session['is_admin'] = user['IS_ADMIN'] == 'Yes'
            session['cart'] = {}
            return redirect(url_for('event_selection'))
        return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/event', methods=['GET', 'POST'])
def event_selection():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        sport = request.form.get('sport')
        gender = request.form.get('gender', "Men's")
        level = request.form.get('level', 'Varsity')
        away_team = request.form.get('away_team')
        if not all([sport, away_team]):
            return render_template('event.html', sports=list(SPORT_MENUS.keys()),
                                   away_teams=list(AWAY_TEAMS.keys()), error='Please fill all fields.')
        game_id = generate_game_id(gender, sport, away_team, level)
        conn = get_db()
        existing = conn.execute("SELECT game_ID FROM GAME_ANALYTICS WHERE game_ID = ?", (game_id,)).fetchone()
        if not existing:
            conn.execute("INSERT INTO GAME_ANALYTICS (game_ID, sport, away_team, order_count, earnings) VALUES (?, ?, ?, 0, 0)",
                         (game_id, sport, away_team))
            conn.commit()
        conn.close()
        session['game_id'] = game_id
        session['sport'] = sport
        session['cart'] = {}
        return redirect(url_for('pos'))
    return render_template('event.html', sports=list(SPORT_MENUS.keys()),
                           away_teams=list(AWAY_TEAMS.keys()), error=None)

@app.route('/pos')
def pos():
    if 'username' not in session or 'game_id' not in session:
        return redirect(url_for('login'))
    sport = session.get('sport', 'Football Game')
    conn = get_db()
    # Get live prices from DB
    db_prices = {row['ITEM']: float(row['PRICE']) for row in conn.execute("SELECT ITEM, PRICE FROM ITEMS").fetchall()}
    conn.close()
    menu = SPORT_MENUS.get(sport, [])
    # Apply DB prices
    menu = [(name, db_prices.get(name, price), itype) for name, price, itype in menu]
    cart = session.get('cart', {})
    total = sum(v['price'] * v['qty'] for v in cart.values())
    return render_template('pos.html', menu=menu, cart=cart, total=total,
                           sport=sport, game_id=session['game_id'])

@app.route('/cart/add', methods=['POST'])
def cart_add():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    data = request.get_json()
    item_name = data.get('item')
    conn = get_db()
    row = conn.execute("SELECT PRICE FROM ITEMS WHERE ITEM = ?", (item_name,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Item not found'}), 404
    price = float(row['PRICE'])
    cart = session.get('cart', {})
    if item_name in cart:
        cart[item_name]['qty'] += 1
    else:
        cart[item_name] = {'qty': 1, 'price': price}
    session['cart'] = cart
    total = sum(v['price'] * v['qty'] for v in cart.values())
    cart_count = sum(v['qty'] for v in cart.values())
    return jsonify({'success': True, 'total': f'{total:.2f}', 'cart_count': cart_count,
                    'item': item_name, 'item_price': f'{price:.2f}',
                    'item_qty': cart[item_name]['qty']})

@app.route('/cart/remove', methods=['POST'])
def cart_remove():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    data = request.get_json()
    item_name = data.get('item')
    cart = session.get('cart', {})
    if item_name in cart:
        cart[item_name]['qty'] -= 1
        if cart[item_name]['qty'] <= 0:
            del cart[item_name]
    session['cart'] = cart
    total = sum(v['price'] * v['qty'] for v in cart.values())
    cart_count = sum(v['qty'] for v in cart.values())
    return jsonify({'success': True, 'total': f'{total:.2f}', 'cart_count': cart_count})

@app.route('/cart/clear', methods=['POST'])
def cart_clear():
    session['cart'] = {}
    return jsonify({'success': True})

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'username' not in session or 'game_id' not in session:
        return redirect(url_for('login'))
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('pos'))
    game_id = session['game_id']
    total = sum(v['price'] * v['qty'] for v in cart.values())
    conn = get_db()
    c = conn.cursor()
    # Check inventory
    for item_name, info in cart.items():
        row = c.execute("SELECT ITEM_ID FROM ITEMS WHERE ITEM = ?", (item_name,)).fetchone()
        if row:
            item_id = row[0]
            ingredients = c.execute("SELECT ITEM FROM INVENTORY_ITEMS WHERE ITEM_ID = ?", (item_id,)).fetchall()
            check_items = [i[0] for i in ingredients] if ingredients else [item_name]
            for ci in check_items:
                inv = c.execute("SELECT QUANTITY FROM INVENTORY WHERE ITEM = ?", (ci,)).fetchone()
                if inv and inv[0] < info['qty']:
                    conn.close()
                    session['checkout_error'] = f'Insufficient inventory for {item_name}.'
                    return redirect(url_for('pos'))
    # Create order
    result = c.execute("SELECT MAX(order_ID) FROM ORDERS").fetchone()
    order_id = (result[0] or 0) + 1
    c.execute("INSERT INTO ORDERS (order_ID, game_ID, total_cost) VALUES (?, ?, ?)", (order_id, game_id, total))
    # Record items and update inventory
    for item_name, info in cart.items():
        row = c.execute("SELECT ITEM_ID FROM ITEMS WHERE ITEM = ?", (item_name,)).fetchone()
        if row:
            item_id = row[0]
            cost = info['price'] * info['qty']
            c.execute("INSERT INTO ORDERED_ITEMS (order_ID, item_ID, quantity, cost) VALUES (?, ?, ?, ?)",
                      (order_id, item_id, info['qty'], cost))
            for _ in range(info['qty']):
                update_inventory(c, item_name)
    # Update analytics
    c.execute("UPDATE GAME_ANALYTICS SET earnings = IFNULL(earnings,0) + ?, order_count = IFNULL(order_count,0) + 1 WHERE game_ID = ?",
              (total, game_id))
    conn.commit()
    # Get order number for receipt
    order_num = c.execute("SELECT order_count FROM GAME_ANALYTICS WHERE game_ID = ?", (game_id,)).fetchone()[0]
    conn.close()
    receipt = {'items': dict(cart), 'total': total, 'order_num': order_num, 'order_id': order_id}
    session['cart'] = {}
    session['receipt'] = receipt
    return redirect(url_for('receipt'))

@app.route('/receipt')
def receipt():
    if 'receipt' not in session:
        return redirect(url_for('pos'))
    r = session.pop('receipt')
    return render_template('receipt.html', receipt=r, sport=session.get('sport',''))

# ── ADMIN ROUTES ──────────────────────────────────────

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('pos'))
    return render_template('admin.html', sport=session.get('sport',''))

@app.route('/admin/inventory')
def admin_inventory():
    if not session.get('is_admin'):
        return redirect(url_for('pos'))
    conn = get_db()
    inventory = conn.execute("SELECT ITEM, QUANTITY FROM INVENTORY ORDER BY ITEM").fetchall()
    conn.close()
    return render_template('admin_inventory.html', inventory=inventory)

@app.route('/admin/inventory/update', methods=['POST'])
def update_inventory_route():
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    conn = get_db()
    conn.execute("UPDATE INVENTORY SET QUANTITY = ? WHERE ITEM = ?", (data['quantity'], data['item']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/admin/menu')
def admin_menu():
    if not session.get('is_admin'):
        return redirect(url_for('pos'))
    sport = session.get('sport', 'Football Game')
    conn = get_db()
    db_prices = {row['ITEM']: float(row['PRICE']) for row in conn.execute("SELECT ITEM, PRICE FROM ITEMS").fetchall()}
    all_items = conn.execute("SELECT ITEM, PRICE, ITEM_TYPE FROM ITEMS ORDER BY ITEM").fetchall()
    conn.close()
    menu = SPORT_MENUS.get(sport, [])
    menu_names = {name for name, _, _ in menu}
    current_menu = [(name, db_prices.get(name, price), itype) for name, price, itype in menu]
    other_items = [(row['ITEM'], float(row['PRICE']), row['ITEM_TYPE'])
                   for row in all_items if row['ITEM'] not in menu_names]
    return render_template('admin_menu.html', sport=sport, current_menu=current_menu,
                           other_items=other_items)

@app.route('/admin/menu/update_price', methods=['POST'])
def update_price():
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    conn = get_db()
    conn.execute("UPDATE ITEMS SET PRICE = ? WHERE ITEM = ?", (data['price'], data['item']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/admin/menu/add_item', methods=['POST'])
def add_item():
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    name, price, item_type, qty = data['name'], data['price'], data['type'], data.get('qty', 100)
    conn = get_db()
    existing = conn.execute("SELECT ITEM FROM ITEMS WHERE ITEM = ?", (name,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'error': 'Item already exists'}), 400
    conn.execute("INSERT INTO ITEMS (ITEM, PRICE, ITEM_TYPE) VALUES (?, ?, ?)", (name, price, item_type))
    inv = conn.execute("SELECT ITEM FROM INVENTORY WHERE ITEM = ?", (name,)).fetchone()
    if not inv:
        conn.execute("INSERT INTO INVENTORY (ITEM, QUANTITY) VALUES (?, ?)", (name, qty))
    conn.commit()
    conn.close()
    sport = session.get('sport', 'Football Game')
    if sport in SPORT_MENUS:
        SPORT_MENUS[sport].append((name, float(price), item_type))
    return jsonify({'success': True})

@app.route('/admin/menu/remove_item', methods=['POST'])
def remove_item():
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    item_name = data['item']
    sport = session.get('sport', 'Football Game')
    if sport in SPORT_MENUS:
        SPORT_MENUS[sport] = [(n, p, t) for n, p, t in SPORT_MENUS[sport] if n != item_name]
    return jsonify({'success': True})

@app.route('/admin/menu/transfer_item', methods=['POST'])
def transfer_item():
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    item_name = data['item']
    sport = session.get('sport', 'Football Game')
    conn = get_db()
    row = conn.execute("SELECT PRICE, ITEM_TYPE FROM ITEMS WHERE ITEM = ?", (item_name,)).fetchone()
    conn.close()
    if row and sport in SPORT_MENUS:
        menu_names = {n for n, _, _ in SPORT_MENUS[sport]}
        if item_name not in menu_names:
            SPORT_MENUS[sport].append((item_name, float(row['PRICE']), row['ITEM_TYPE']))
    return jsonify({'success': True})

@app.route('/admin/analytics')
def analytics():
    if not session.get('is_admin'):
        return redirect(url_for('pos'))
    conn = get_db()
    top_sellers = conn.execute('''
        SELECT item_ID, SUM(quantity) AS total_sold FROM ORDERED_ITEMS
        GROUP BY item_ID HAVING total_sold = (
            SELECT SUM(quantity) FROM ORDERED_ITEMS GROUP BY item_ID ORDER BY SUM(quantity) DESC LIMIT 1)
    ''').fetchall()
    low_sellers = conn.execute('''
        SELECT item_ID, SUM(quantity) AS total_sold FROM ORDERED_ITEMS
        GROUP BY item_ID HAVING total_sold = (
            SELECT SUM(quantity) FROM ORDERED_ITEMS GROUP BY item_ID ORDER BY SUM(quantity) ASC LIMIT 1)
    ''').fetchall()
    avg_by_team = conn.execute('''
        SELECT away_team, AVG(earnings) AS avg_earnings FROM GAME_ANALYTICS
        GROUP BY away_team ORDER BY avg_earnings DESC
    ''').fetchall()
    avg_by_sport = conn.execute('''
        SELECT sport, AVG(earnings) AS avg_earnings FROM GAME_ANALYTICS
        GROUP BY sport ORDER BY avg_earnings DESC
    ''').fetchall()
    individual_sales = conn.execute('''
        SELECT ga.game_ID, ga.sport, ga.away_team, i.ITEM, oi.quantity, oi.cost
        FROM GAME_ANALYTICS ga
        JOIN ORDERS o ON ga.game_ID = o.game_ID
        JOIN ORDERED_ITEMS oi ON o.order_ID = oi.order_ID
        JOIN ITEMS i ON oi.item_ID = i.ITEM_ID
        ORDER BY ga.away_team
    ''').fetchall()
    summary_sales = conn.execute('''
        SELECT ga.sport, i.ITEM, SUM(oi.quantity) AS total_qty,
               SUM(oi.quantity * oi.cost) AS total_earnings
        FROM GAME_ANALYTICS ga
        JOIN ORDERS o ON ga.game_ID = o.game_ID
        JOIN ORDERED_ITEMS oi ON o.order_ID = oi.order_ID
        JOIN ITEMS i ON oi.item_ID = i.ITEM_ID
        GROUP BY ga.sport, i.ITEM ORDER BY total_qty DESC
    ''').fetchall()
    all_games = conn.execute("SELECT * FROM GAME_ANALYTICS ORDER BY game_ID DESC").fetchall()
    conn.close()
    return render_template('analytics.html',
        top_sellers=top_sellers, low_sellers=low_sellers,
        avg_by_team=avg_by_team, avg_by_sport=avg_by_sport,
        individual_sales=individual_sales, summary_sales=summary_sales,
        all_games=all_games)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
