# About
*shop* is a simple website for an imaginary PC shop. It's written in Python, using the [Flask](https://flask.palletsprojects.com/en/2.0.x/) framework. It communicates with a [PostgreSQL](https://www.postgresql.org/) SQL database using [psycopg](https://www.psycopg.org/) and the whole thing is brought together with [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/).

# Usage
Firstly, make sure you have all the dependencies installed and in your path.

## Python
To install all python dependencies:

```console
$ python3 -m pip install -r requirements.txt
```

This command ensures that all dependencies and necessary version of these dependencies are installed.

## PostgreSQL
This is the tricky part. For building the PostgreSQL container, we need [nix](https://nixos.org) and [Docker](https://docker.com). Once installing both of these tools, there is helpful bash script called `p` in the project's root directory. You can pass three command line arguments to this script:
- `build`: Builds the Docker image using Nix and outputs to the `result` file.
- `load`: Load the result into Docker.
- `run`: Run the Docker image, saving the container id to `.id` file in the project's root directory.
- `kill`: This than kills the Docker container, using it's id which is located in the `.id` file.
- `db`: This has a few subcommands as well, `import` import a database from a supplied `.sql` file, `export` exports the current database into a `db.sql` file and finally `shell` which drops you into a `psql` shell.

# Overview
In this simple overview, we're going to walk through the inner workings of the app. The app is started by running the `main.py` python file:

```console
$ python3 main.py
```

After the command is run, the web server is started and you will be able to see the web address of the web server printed into to program's standard output. After visiting the web site in your browser, you will be greeted with the main page of the shop, where all the necessary information is located. On the top of the site you will see a navigation bar. There are four entries in the navigation bar: `Home`, `Catalogue`, and lastly, on the right most side of the screen a `User` entry. From here, you can choose any of these entries. `Home` is where we are located now, `Catalogue` is the place where all the products are located and where each product can be added to cart or examined further. `Cart` is where each user has all the information about their orders. This will not be available to you right away however, you will first be prompted to create an account. `Users` will take you to the same page, here you can create an account, or log in to an already existing account. Each account has three required fields, username, email and password. After filling these out, your new account will be created and you will be able to log in (note that when you are logging in into an already existing account, you can use either the username or the email associated with the account). After that, you can freely visit your `Cart` and manage all your orders.

## Admin account
The credentials for an admin account are:

```
username: admin
email: admin@shop.shop
password: nimda
```

If you choose to log in as an admin, you will be able to add new products in catalogue, as well as preview all users and their orders. This is mostly just a DEBUG feature.

## Catalogue
Catalogue consists of two parts, the search field and the alphabetical order of all search matches. When the search field is empty, all products are shown. When clicking a product, you will be redirected to its page, where more information about the product will be shown. A product can be added to cart from the catalogue itself, as well as its own page.

## Cart
When a user visits their cart, a list of all orders, starting with the most recent one at the top, is show. After clicking each order, the user can view its page and inspect or modify the order.

## Home
Home is the start page of the website, here the store administrators can add information about any discounts, sales or basically anything else they wish to add and show to the user. This can be added with the admin account.

# Docs
All code is documented.
