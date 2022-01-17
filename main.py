#!/usr/bin/env python3


from flask import render_template, request, url_for, session, redirect
from flask.helpers import flash
from src import App, is_mail
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship


full_app = App("shop", "super secret key")
app = full_app.get_flask()
db = full_app.get_db()
db.create_all()


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
    products = Column(ARRAY(Integer))
    products_amount = Column(ARRAY(Integer))
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


@app.route('/')
def index():
    username = session.get("username")
    if username:
        template = render_template("index.html", name=username)
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
                print("here first")
                query = Users.query.filter_by(email=name_email, password=password)
                if q := query.first():
                    print("got query")
                    session["logged"] = True
                    session["user_id"] = q.id
                    session["username"] = q.name
                    return redirect("/")
                else:
                    flash("Wrong username or password!")
            else:
                print("here")
                query = Users.query.filter_by(name=name_email, password=password)
                if q := query.first():
                    print("got query")
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
                db.session.add(new_user)
                success = False
                try:
                    db.session.commit()
                    success = True
                except:
                    flash("Internal error occured when adding a new user!")
                if success:
                    redirect(url_for("log_in"))
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

    template = render_template("catalogue.html", shop_items=items)
    return template


@app.route('/cart')
def cart():
    logged = session.get("logged")
    if logged:
        user_id = session.get("user_id")
        if user_id:
            products = Orders.query.filter_by(belongs_to=user_id).all()

            return render_template("cart.html", cart_items=products)
    else:
        flash("You are not logged in!")
    template = render_template("cart.html")
    return template


@app.route('/product/<id>')
def product(id: str):
    i = int(id)
    query = Products.query.filter_by(id=i)
    if p := query.first():
        return render_template("product.html", item=p)
    flash("Such product does not exist!")


@app.route('/order/<id>')
def order(id: str):
    i = int(id)
    query = Orders.query.filter_by(id=i)
    if q := query.first():
        products = []
        for product in q.products:
            query = Products.query.filter_by(id=product)
            if q2 := query.first():
                products.append(q2)
        return render_template("order.html", item=q, items=products)
    flash("Such order does not exist!")


def main() -> None:
    full_app.run()


if __name__ == "__main__":
    main()
