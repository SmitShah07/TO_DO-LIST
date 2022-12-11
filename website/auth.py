from flask import Blueprint, redirect, render_template, url_for, request, flash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash



auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        Email = request.form["email2"]
        password = request.form["password2"]
        
        users = User.query.filter_by(email=Email).first()
        if users:
            if check_password_hash(users.password, password):
                flash("Logged In Successfully", category="Success")
                login_user(users, remember=True)
                return redirect(url_for("views.home"))   
            else:
                flash("Incorrect Password", category="error")    
        else:
            flash("Incorrect Email", category="error")
        
    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # data = request.form
        firstname = request.form.get("firstname")
        email = request.form["email"]
        password = request.form["password1"]
        confirmPass = request.form["password2"]
        
        users = User.query.filter_by(email=email).first()
        if users:
            flash("User is already Exist", category="error")
        elif len(email) < 4:
            flash("Email should be grater than 3 characters", category="error")
        elif len(firstname) < 2:
            flash("First Name should be greater than 1 character", category="error")
        elif len(password) < 8:
            flash("Password should be at least 7 characters", category="error")
        elif password != confirmPass:
            flash("Passwords don\'t match", category="error")
        else:
            new_user = User(email = email, firstname = firstname, password=generate_password_hash(password, method="sha256"))
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created", category="Success")
            return redirect(url_for("auth.login"))   
    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully Logout", category="Success")
    return redirect(url_for("auth.login"))