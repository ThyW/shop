#!/usr/bin/env python3


from flask import render_template, request, url_for, session, redirect
from flask.helpers import flash
from src import App, is_mail, MutableList
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship


full_app = App("shop", "super secret key")
app = full_app.get_flask()
db = full_app.get_db()


class Users(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<Name: {self.name}, id: {self.id}, email: {self.email}, password: {self.password}>"


class Orders(db.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    belongs_to = Column(Integer, ForeignKey("users.id"))
    products = Column(MutableList.as_mutable(ARRAY(Integer)))
    user = relationship("Users")

    def __repr__(self) -> str:
        s = ""
        s += f"<Id: {self.id}, belongs to: {Users.query.filter_by(id=self.belongs_to).first()}"
        for each in self.products:
            s += f"\t\n{Products.query.filter_by(id=each).first()}"
        s += ">"
        return s


class Products(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    more_url = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"id: {self.id}, amount: {self.amount}, name: {self.name}, description: {self.description}"


class Cart(db.Model):
    __tablename__ = "cart"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    products = Column(MutableList.as_mutable(ARRAY(Integer)))
    user = relationship("Users")

    def __repr__(self) -> str:
        return f"<Cart belongs to: {self.id}, products: {len(self.products)}>"


@app.route('/')
def index():
    username = session.get("username")
    logged = session.get("logged")
    if username:
        template = render_template("index.html", name=username, user=logged)
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
    logged = session.get("logged")

    template = render_template("catalogue.html", shop_items=items, user=logged)
    return template

# TODO: add support for removing stuff from the cart
@app.route('/cart')
def cart():
    logged = session.get("logged")
    if logged:
        user_id = session.get("user_id")
        if user_id:
            orders = Orders.query.filter_by(belongs_to=user_id).all()
            cart = Cart.query.filter_by(id=user_id)
            if q := cart.first():
                cart_items = []
                print(q)
                for each in q.products:
                    query = Products.query.filter_by(id=each)
                    if q := query.first():
                        cart_items.append(q)
                return render_template("cart.html", cart_items=cart_items, orders=orders, user=logged)
    else:
        template = render_template("cart.html", user=logged)
        return template


@app.route('/product/<id>')
def product(id: str):
    i = int(id)
    logged = session.get("logged")
    query = Products.query.filter_by(id=i)
    if p := query.first():
        return render_template("product.html", item=p, user=logged)
    flash("Such product does not exist!")


@app.route('/order/<id>')
def order(id: str):
    i = int(id)
    logged = session.get("logged")
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
        new_order = Orders(belongs_to=uid, products=[], products_amount=[])
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
        print(c)
        db.session.commit()
        return redirect(f"/product/{id}")
    else:
        return redirect(f"/product/{id}")


def main() -> None:
    full_app.run()


if __name__ == "__main__":
    main()
