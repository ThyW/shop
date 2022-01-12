#!/usr/bin/env python3


from flask import Flask, render_template, session, request, redirect, url_for


app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    print("Index!")
    template = render_template("index.html")
    return template

app.run()
