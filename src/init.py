from .app import App

full_app = App("shop", "super secret key")
app = full_app.get_flask()
db = full_app.get_db()

Model = db.Model
