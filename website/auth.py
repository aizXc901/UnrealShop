from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .db import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Received email: {email}, password: {password}")  # Отладочный вывод

        # проверка на п поля
        if not email or not password:
            flash("Заполните все поля")
            return redirect(url_for('auth.register'))

        # проверка на сущ польз
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Такой email уже зарегистрирован")
            return redirect(url_for('auth.register'))

        # хеширование пар
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:600000')

        # нов польз
        new_user = User(email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            print("User saved successfully")  # Отладочный вывод
            flash("Регистрация прошла успешно")
            return redirect(url_for('views.home'))
        except Exception as e:
            print("Ошибка при сохранении:", e)  # Вывод ошибки
            db.session.rollback()
            flash("Произошла ошибка при регистрации")
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли в аккаунт')
            return redirect(url_for('views.home'))
        else:
            flash('Неправильный email или пароль')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('views.home'))
