from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .init import Model
from .utils import MutableList

class Users(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<Name: {self.name}, id: {self.id}, email: {self.email}, password: {self.password} is_admin={self.admin}>"


class Orders(Model):
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


class Products(Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    more_url = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"id: {self.id}, amount: {self.amount}, name: {self.name}, description: {self.description}"


class Cart(Model):
    __tablename__ = "cart"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    products = Column(MutableList.as_mutable(ARRAY(Integer)))
    user = relationship("Users")

    def __repr__(self) -> str:
        return f"<Cart belongs to: {self.id}, products: {len(self.products)}>"
