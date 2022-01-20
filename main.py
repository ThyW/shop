#!/usr/bin/env python3
from flask import render_template, request, session, redirect
from flask.helpers import flash
from src import is_mail, Users, Orders, Cart, Products, app, db, full_app


@app.route('/')
def index():
    logged = session.get("username")
    uid = session.get("user_id")
    if logged:
        u = Users.query.filter_by(id=uid).first()
        admin = u.admin
        template = render_template("index.html", user=logged, name=logged, admin=admin)
    else:
        template = render_template("index.html")
    return template


@app.route('/log_in', methods=['POST', 'GET'])
def log_in():
    if request.method == "POST":
        session.clear()
        name_email = request.form.get("username")
        password = request.form.get("password")
        if name_email and password:
            if is_mail(name_email):
                query = Users.query.filter_by(email=name_email, password=password)
                if q := query.first():
                    session["logged"] = True
                    session["user_id"] = q.id
                    session["username"] = q.name
                    return redirect("/")
                else:
                    flash("Wrong username or password!")
            else:
                query = Users.query.filter_by(name=name_email, password=password)
                if q := query.first():
                    session["logged"] = True
                    session["user_id"] = q.id
                    session["username"] = q.name
                    session["admin"] = q.admin
                    return redirect("/")
                else:
                    flash("Wrong username or password!")
        else:
            flash("Missing email or password in form!")
    template = render_template("login.html")
    return template


@app.route('/sign_up', methods=['POST', 'GET'])
def sing_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if username and email and password:
            if is_mail(email) and not is_mail(username):
                new_user = Users(name=username, email=email, password=password)
                cart = Cart(id=new_user.id, products=[])
                db.session.add(new_user)
                db.session.add(cart)
                success = False
                try:
                    db.session.commit()
                    success = True
                except:
                    flash("Internal error occured when adding a new user!")
                if success:
                    redirect("/log_in")
                else:
                    template = render_template("signup.html")
                    return template
            else:
                flash("Invalid username or email address!")

    template = render_template("signup.html")
    return template


@app.route('/catalogue')
def catalogue():
    items = Products.query.all()
    logged = session.get("username")
    admin = session.get("admin")
    template = render_template("catalogue.html", shop_items=items, user=logged, admin=admin)
    return template

# TODO: add support for removing stuff from the cart
@app.route('/cart')
def cart():
    logged = session.get("username")
    if logged:
        user_id = session.get("user_id")
        if user_id:
            orders = Orders.query.filter_by(belongs_to=user_id).all()
            cart = Cart.query.filter_by(id=user_id)
            if q := cart.first():
                cart_items = []
                for each in q.products:
                    query = Products.query.filter_by(id=each)
                    if q := query.first():
                        cart_items.append(q)
                return render_template("cart.html", cart_items=cart_items, orders=orders, user=logged, admin=session.get("admin"))
        return render_template("cart.html", user=logged)
    else:
        template = render_template("cart.html", user=logged)
        return template


@app.route('/product/<id>')
def product(id: str):
    i = int(id)
    logged = session.get("username")
    query = Products.query.filter_by(id=i)
    if p := query.first():
        return render_template("product.html", item=p, user=logged)
    flash("Such product does not exist!")


@app.route('/order/<id>')
def order(id: str):
    i = int(id)
    logged = session.get("username")
    query = Orders.query.filter_by(id=i)
    if q := query.first():
        products = []
        for product in q.products:
            query = Products.query.filter_by(id=product)
            if q2 := query.first():
                products.append(q2)
        return render_template("order.html",
                               item=q,
                               items=products,
                               user=logged)


@app.route('/log_out')
def log_out():
    session.clear()
    return redirect("/")


@app.route('/new_order')
def new_order():
    uid = session.get("user_id")
    if uid:
        cart_query = Cart.query.filter_by(id=uid)
        if q := cart_query.first():
            new_order = Orders(belongs_to=uid, products=q.products)
            q.products = []
            db.session.add(new_order)
            db.session.commit()
            session["most_recent_order"] = new_order.id
            return redirect("/cart")
    else:
        flash("Not logged in!")
        return redirect("/cart")


@app.route('/add_to_cart/<id>')
def add_to_cart(id: str):
    i = int(id)
    user_id = session.get("user_id")
    if user_id:
        print(user_id)
        c = Cart.query.filter_by(id=user_id).first()
        c.products.append(i)
        db.session.commit()
        return redirect(f"/product/{id}")
    else:
        return redirect(f"/product/{id}")


@app.route('/add_product', methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        if uid := session.get("user_id"):
            query = Users.query.filter_by(id=uid)
            if q := query.first():
                if q.admin:
                    product_name = request.form.get("product_name")
                    product_description = request.form.get("product_description")
                    product_amount = request.form.get("product_amount")
                    if product_name and product_description\
                            and product_amount:
                                product = Products(name=product_name,
                                                   amount=product_amount,
                                                   description=product_description)
                                db.session.add(product)
                                succ = False
                                try:
                                    db.session.commit()
                                    succ = True
                                except:
                                    flash("failed")
                                if succ:
                                    return redirect("/add_product")
                                else:
                                    return redirect("/")
    return render_template("add_product.html", user=session.get("username"))


def main() -> None:
    app.debug = True
    full_app.run()


if __name__ == "__main__":
    main()
