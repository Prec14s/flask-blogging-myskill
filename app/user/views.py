from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.user.models import User
from app.extensions import db, bcrypt
from flask_login import login_user, logout_user,login_required

blueprint = Blueprint("user", __name__, url_prefix="/user")

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # cek password dan konfirmasi sama
        if password != confirm_password:
            flash("Password dan konfirmasi password tidak sama.", "error")
            return redirect(url_for("user.register"))

        # cek username sudah dipakai atau belum
        if User.query.filter_by(username=username).first():
            flash("Username sudah dipakai.", "error")
            return redirect(url_for("user.register"))

        # simpan user baru
        user = User(
            username=username,
            password=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()

        flash("Registrasi berhasil, silakan login.", "success")
        return redirect(url_for("user.login"))

    return render_template("user/register.html")
        

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        # cek user ada dan password cocok
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Selamat datang, {user.username}!", "success")
            return redirect(url_for("public.home"))

        flash("Hayo menurutmu apalah?", "error")
        return redirect(url_for("user.login"))

    return render_template("user/login.html")

@blueprint.route('/logout')
def logout():
    session.clear()
    flash("Kamu sudah logout.", "success")
    return redirect(url_for("user.login"))

