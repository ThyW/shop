#!/usr/bin/env python3


from flask import render_template
from src import App
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship


full_app = App("shop")
app = full_app.get_flask()
db = full_app.get_db()


class Users(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<Name: {self.name}, id: {self.id}, email: {self.email}>"


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
    print("Index!")
    template = render_template("index.html")
    return template


@app.route('/log_in')
def log_in():
    pass


@app.route('/sign_up')
def sing_up():
    pass


@app.route('/catalogue')
def catalogue():
    pass


@app.route('/cart')
def cart():
    pass


def main() -> None:
    full_app.run()


if __name__ == "__main__":
    main()
