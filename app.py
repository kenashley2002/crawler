from flask import *
import sqlite3, hashlib, os, jinja2
from werkzeug.utils import secure_filename
from api.get_weather import get_weather
from api.get_forexrate import get_forexrate
from api.get_oilrate import get_oilrate
from api.get_goldvn import get_goldvn
from api.get_news_amway import get_news_amway, get_nutrilite_amway, get_artistry_amway, get_amagram_amway
from api.get_quotes import get_quotes
import logging

app = Flask(__name__)
app.secret_key = 'robibotwebview'
UPLOAD_FOLDER = 'static/images/assets'
ALLOWED_EXTENSION = {'jpg', 'png', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def getLoginDetails():
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        if 'username' not in session:
            loggedIn = False
            username = ''
        else:
            loggedIn = True
            cur.execute("SELECT adano, username FROM adacode WHERE adano = '" + str(session['username']) + "'")
            adano, username = cur.fetchone()
    conn.close()
    return (loggedIn, username)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    loggedIn, username = getLoginDetails()
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT sku, item_name, item_desc, dp_price, cp_price, pv, categoryId FROM products")
        itemData = cur.fetchall()
        cur.execute("SELECT categoryId, categoryName FROM categories")
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('home.html', itemData=itemData, categoryData=categoryData, loggedIn=loggedIn, name=username)


@app.route('/nutrilite')
def to_nutrilite():
    loggedIn, username = getLoginDetails()
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT sku, item_name, item_desc, dp_price, cp_price, pv, categoryId FROM products WHERE categoryId ='nu'")
        itemData = cur.fetchall()
        cur.execute("SELECT categoryId, categoryName FROM categories")
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('nutrilite.html', itemData=itemData, categoryData=categoryData, loggedIn=loggedIn,
                           name=username)


@app.route('/artistry')
def to_artistry():
    loggedIn, username = getLoginDetails()
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT sku, item_name, item_desc, dp_price, cp_price, pv, categoryId FROM products WHERE categoryId ='art'")
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, categoryName FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('artistry.html', itemData=itemData, categoryData=categoryData, loggedIn=loggedIn,
                           name=username)


@app.route('/posting')
def posting():
    loggedIn, username = getLoginDetails()
    return render_template('posting.html', loggedIn=loggedIn, name=username)


@app.route('/addItem', methods=['GET', 'POST'])
def addItem():
    loggedIn, username = getLoginDetails()
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, categoryName FROM categories")
        categories = cur.fetchall()
    conn.close()
    if request.method == 'POST':
        sku = int(request.form.get('sku'))
        item_name = request.form.get('item_name')
        item_desc = request.form.get('item_desc')
        dp_price = float(request.form.get('dp_price'))
        cp_price = float(request.form.get('cp_price'))
        pv = float(request.form.get('pv'))
        categoryId = request.form.get('category')
        # Add database
        with sqlite3.connect('database/database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO products(sku, item_name, item_desc, dp_price, cp_price, pv, categoryId) VALUES (?, ?, ?, ?, ? ,? ,?)",
                    (sku, item_name, item_desc, dp_price, cp_price, pv, categoryId))
                conn.commit()
                flash('Thêm sản phẩm thành công!')
            except:
                flash('Lỗi thêm sản phẩm thất bại!')
                conn.rollback()
        conn.close()
        return redirect(url_for('addItem'))
    return render_template('additem.html', categories=categories, loggedIn=loggedIn, name=username)


@app.route('/login', methods=['GET', 'POST'])
def login(oksignup=None):
    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method == 'POST':
        adano = request.form['adano']
        adapass = request.form['adapass']
        if is_valid(adano, adapass):
            session['username'] = adano
            return redirect(url_for('home'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu!')
            return render_template('login.html')
    else:
        return render_template('login.html', oksignup=oksignup)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        adano = request.form.get('adano')
        adapass = request.form.get('adapass')
        email = request.form.get('email')
        admincode = request.form.get('admincode')
        if check_key_auth(admincode):
            if not check_data_valid(adano, email, username):
                with sqlite3.connect('database/database.db') as conn:
                    try:
                        cur = conn.cursor()
                        cur.execute("INSERT INTO adacode (adano, adapass, email, username) VALUES (?, ?, ?, ?)",
                                    (adano, hashlib.md5(adapass.encode()).hexdigest(), email, username))
                        conn.commit()
                        msg = flash('Đăng ký thành công! Vui lòng đăng nhập!')
                    except:
                        msg = flash('Đăng ký thất bại! Vui lòng thực hiện lại hoặc liên hệ BQT!')
                        conn.rollback()
                conn.close()
                return redirect(url_for('login', oksignup=msg))
            else:
                msg = flash('Tài khoản đã tồn tại! Vui lòng đăng nhập hoặc thay dổi thông tin đăng ký!')
                return redirect(url_for('login', oksignup=msg))
        else:
            msg = flash('Sai Mã quản lý! Vui lòng liên hệ BQT để lấy Mã quản lý!')
            return redirect(url_for('login', oksignup=msg))
    return render_template('signup.html')


@app.route('/edit/product')
def edit_product(msg=None):
    if 'username' not in session:
        return redirect(url_for('home'))
    loggedIn, username = getLoginDetails()
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT sku, item_name, item_desc, dp_price, cp_price, pv, categoryId FROM products")
        itemData = cur.fetchall()
        cur.execute("SELECT categoryId, categoryName FROM categories")
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('edit.html', itemData=itemData, categoryData=categoryData, loggedIn=loggedIn,
                           name=username, msg=msg)


@app.route('/edit/product/<int:sku>', methods=['GET', 'POST'])
def update_product(sku):
    if 'username' not in session:
        return redirect(url_for('home'))
    loggedIn, username = getLoginDetails()
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT sku, item_name, item_desc, dp_price, cp_price, pv, categoryId FROM products WHERE sku = " + str(
                sku))
        itemData = cur.fetchone()
        cur.execute("SELECT categoryId, categoryName FROM categories")
        categoryData = cur.fetchall()
    conn.close()
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_desc = request.form.get('item_desc')
        dp_price = request.form.get('dp_price')
        cp_price = request.form.get('cp_price')
        pv = request.form.get('pv')
        categoryId = request.form.get('category')
        with sqlite3.connect('database/database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE products SET item_name = ?, item_desc = ?, dp_price = ?, cp_price = ?, pv = ?, categoryId = ? WHERE sku = ?",
                    (item_name, item_desc, dp_price, cp_price, pv, categoryId, str(sku)))
                conn.commit()
                flash("Cập nhật sản phẩm thành công!")
            except:
                conn.rollback()
                flash("Lỗi không cập nhật thành công!")
        conn.close()
        return redirect(url_for('update_product', sku=sku))
    return render_template("editdetail.html", data=itemData, loggedIn=loggedIn, categoryData=categoryData,
                           name=username,
                           sku=sku)


@app.route('/remove/product/<int:sku>')
def remove_product(sku):
    if 'username' not in session:
        return redirect(url_for('home'))
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM products WHERE sku = " + str(sku))
            conn.commit()
            msg = flash("Xóa sản phẩm thành công!")
        except:
            conn.rollback()
            msg = flash("Lỗi không thể xóa sản phẩm")
    conn.close()
    return redirect(url_for('edit_product', msg=msg))


@app.route('/check-contact')
def check_contact():
    if 'username' not in session:
        return redirect(url_for('home'))
    loggedIn, username = getLoginDetails()
    return render_template('checkContact.html', loggedIn=loggedIn, name=username)


def is_valid(adano, adapass):
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT adano, adapass, email, username FROM adacode")
        data = cur.fetchall()
    conn.close()
    for row in data:
        if row[0] == int(adano) and row[1] == hashlib.md5(adapass.encode()).hexdigest():
            return True
    return False


def check_data_valid(adano, email, username):
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT adano, email, username FROM adacode")
        data = cur.fetchall()
    conn.close()
    for row in data:
        if row[0] == adano and row[1] == email and row[2] == username:
            return True
    return False


def check_key_auth(admincode):
    with sqlite3.connect('database/database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT token_auth, token_name FROM tokenauth")
        data = cur.fetchall()
    conn.close()
    for row in data:
        if row[0] == hashlib.md5(admincode.encode()).hexdigest():
            return True
    return False


def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


def currency(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))


### API FOR ROBIBOT ###
# API Weather
@app.route('/api/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    json_result = get_weather(city)
    return jsonify(json_result)


# API for Amway Inc.
@app.route('/api/amwaynews/news', methods=['GET'])
def amwaynews():
    json_result = get_news_amway()
    return jsonify(json_result)


@app.route('/api/amwaynews/nutrilite', methods=['GET'])
def nutrilitenews():
    json_result = get_nutrilite_amway()
    return jsonify(json_result)


@app.route('/api/amwaynews/artistry', methods=['GET'])
def artistrynews():
    json_result = get_artistry_amway()
    return jsonify(json_result)


@app.route('/api/amwaynews/amagram', methods=['GET'])
def amagram():
    json_result = get_amagram_amway()
    return jsonify(json_result)


# API Great Quotes
@app.route('/api/quotes', methods=['GET'])
def quotes():
    json_result = get_quotes()
    return jsonify(json_result)


# API Forex Rates
@app.route('/api/forexrate', methods=['GET'])
def forexrate():
    json_result = get_forexrate()
    return jsonify(json_result)


# API Oil Rates
@app.route('/api/oilrate', methods=['GET'])
def oilrate():
    json_result = get_oilrate()
    return jsonify(json_result)


# API VN Gold Rates
@app.route('/api/goldvn', methods=['GET'])
def goldvn():
    json_result = get_goldvn()
    return jsonify(json_result)


### End API ###

# Logging for error
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    app.run(debug=True)
