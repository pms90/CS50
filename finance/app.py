import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT symbol, name, shares, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["name"] = quote["name"].split('-')[-1]
        stock["total_value"] = quote["price"] * stock["total_shares"]

    stocks_value = 0
    for stock in stocks:
        stocks_value += stock["total_value"]

    portfolio_value = stocks_value + cash

    return render_template("index.html", stocks=stocks, cash=cash, portfolio_value=portfolio_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # verificar que se seleccione simbolo
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # verificar shares
        if not request.form.get("shares"):
            return apology("must provide shares", 400)

        # get
        symbol = request.form.get("symbol")
        # shares = request.form.get("shares")
        name = ' - '

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must provide a positive integer for shares", 400)
        if shares <= 0:
            return apology("must provide a positive integer for shares", 400)

        # if not (isinstance(shares, int) and shares >= 0):
        #     return apology("Invalid shares", 400)

        # if shares <= 0:
        #     return apology("Invaled shares", 400)

        # precio
        quote = lookup(symbol)

        if not quote:
            return apology("Invalid symbol", 400)


        total_cost = quote["price"] * shares

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if cash < total_cost:
            return apology("No funds", 400)

        # Update and insert
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transacted_at, name) VALUES (?, ?, ?, ?, datetime('now'), ?)",
                    session["user_id"], symbol, shares, quote["price"], quote["name"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, shares, price, transacted_at FROM transactions WHERE user_id = ? ORDER BY transacted_at DESC", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        symbol = request.form.get("symbol")

        # Price
        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        if not username:
            return apology("No username", 400)
        elif not password:
            return apology("No password", 400)
        elif password != confirmation:
            return apology("Passwords difere", 400)

        # Check if username is availsble
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("Username not available", 400)

        # Reserved names
        reserved_usernames = ['cs50', 'finace']
        if username in reserved_usernames:
            return apology("Username not available", 400)

        # Require special char
        special_characters = ['&', '!', '-', '[', ']', '*', '_', '(', ')', '~', ':', '^', '%', '#', '<', '}', '/', '{', '=', ',', '@', ';', '?', '.', '+', '`', '>', '|', "'", '$']
        have_spec = False
        for ch in password:
            if ch in special_characters:
                have_spec = True
                break
        if have_spec == False:
            return apology("Password must have at least one special character", 400)

        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)

        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must provide a positive integer for shares", 400)
        if shares <= 0:
            return apology("must provide a positive integer for shares", 400)

        symbol = request.form.get("symbol")

        # current price from api
        quote = lookup(symbol)
        name = ' - '

        if not quote:
            return apology("invalid symbol", 400)

        stocks = db.execute("SELECT symbol, shares, name, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])

        # Check enough owns
        owned_shares = next((stock["total_shares"] for stock in stocks if stock["symbol"] == symbol), 0)
        if owned_shares < shares:
            return apology("not shares to sell", 400)

        sale_value = quote["price"] * shares
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transacted_at, name) VALUES (?, ?, ?, ?, datetime('now'), ?)", session["user_id"], symbol, -shares, quote["price"], quote["name"])

        return redirect("/")

    else:

        stocks = db.execute("SELECT symbol, shares, name, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", stocks=stocks)

@app.route("/favicon.ico")
def favicon_ico():
    return send_from_directory("static", "favicon.ico", as_attachment=False)
