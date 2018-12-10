from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'adano' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT adano, adapass FROM adacode WHERE adano = '" + session['adano'] + "'")
            adaNo = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE adaNo = " + str(adaNo))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, noOfItems)

@app.route("/")
def root():
    loggedIn, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)   
    return render_template('index.html', itemData=itemData, loggedIn=loggedIn, noOfItems=noOfItems, categoryData=categoryData)

@app.route("/add")
def admin():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    return render_template('add.html', categories=categories)

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        categoryId = int(request.form['category'])

        #Uploading image procedure
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO products (name, price, description, image, stock, categoryId) VALUES (?, ?, ?, ?, ?, ?)''', (name, price, description, imagename, stock, categoryId))
                conn.commit()
                msg="added successfully"
            except:
                msg="error occured"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect(url_for('root'))

@app.route("/remove")
def remove():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        data = cur.fetchall()
    conn.close()
    return render_template('remove.html', data=data)

@app.route("/removeItem")
def removeItem():
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM products WHERE productID = ' + productId)
            conn.commit()
            msg = "Deleted successfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    print(msg)
    return redirect(url_for('root'))

@app.route("/displayCategory")
def displayCategory():
        loggedIn, noOfItems = getLoginDetails()
        categoryId = request.args.get("categoryId")
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = " + categoryId)
            data = cur.fetchall()
        conn.close()
        categoryName = data[0][4]
        data = parse(data)
        return render_template('displayCategory.html', data=data, loggedIn=loggedIn, noOfItems=noOfItems, categoryName=categoryName)

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, noOfItems = getLoginDetails()
    return render_template("profileHome.html", loggedIn=loggedIn, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = '" + session['email'] + "'")
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = '" + session['email'] + "'")
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect('database.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        adano = request.form['adano']
        adapass = request.form['adapass']
        if is_valid(adano, adapass):
            session['adano'] = adano
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/productDescription")
def productDescription():
    loggedIn, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ' + productId)
        productData = cur.fetchone()
    conn.close()
    return render_template("productDescription.html", data=productData, loggedIn = loggedIn, noOfItems = noOfItems)

@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = '" + session['email'] + "'")
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('root'))

@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, noOfItems = getLoginDetails()
    adano = session['adano']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT adano FROM adacode WHERE adano = '" + adano + "'")
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = " + str(adano))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, noOfItems=noOfItems)


@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    productId = int(request.args.get('productId'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM kart WHERE userId = " + str(userId) + " AND productId = " + str(productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('root'))


@app.route("/logout")
def logout():
    session.pop('adano', None)
    return redirect(url_for('root'))

def is_valid(adano, adapass):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT adano, adapass FROM adacode')
    data = cur.fetchall()
    for row in data:
        if row[0] == adano and row[1] == hashlib.md5(adapass.encode()).hexdigest():
            return True
    return False


@app.route("/checkout", methods=['GET','POST'])
def payment():
    if 'adano' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, noOfItems = getLoginDetails()
    adano = session['adano']

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT adano FROM adacode WHERE adano = '" + adano + "'")
        adano = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.adaNo = " + str(adano))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
        print(row)
        cur.execute("INSERT INTO Orders (userId, productId) VALUES (?, ?)", (adano, row[0]))
    cur.execute("DELETE FROM kart WHERE adaNo = " + str(adano))
    conn.commit()

    return render_template("checkout.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, noOfItems=noOfItems)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        adapass = request.form['adapass']
        adano = request.form['adano']
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO adacode (adano, adapass) VALUES (?, ?)', (hashlib.md5(adapass.encode()).hexdigest(), adano))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)


@app.route('/registerationForm')
def registrationForm():
    return render_template("register.html")


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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


if __name__ == '__main__':
    app.run(debug=True)
