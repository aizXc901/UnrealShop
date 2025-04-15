from flask_login import login_required, current_user

from .models import Product
from .db import db
from sqlalchemy.sql import text
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    try:
        # Проверяем подключение к БД
        db.session.execute(text("SELECT 1"))

        # Добавляем тестовый товар если таблица пуста
        if not Product.query.first():
            test_product = Product(
                name="Тестовый товар",
                price=99.99,
                description="Пример описания"
            )
            db.session.add(test_product)
            db.session.commit()

        products = Product.query.all()
        return render_template("home.html", products=products)

    except Exception as e:
        print(f"Ошибка БД: {e}")  # Вывод в консоль сервера
        return "<center><h2>Добро пожаловать в UnrealShop (режим без БД)</h2></center>"

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@views.route('/cart')
@login_required
def cart():
    return render_template('cart.html')

@views.route('/catalog')
def catalog():
    return render_template('catalog.html')

@views.route('/catalog/clothing')
def clothing():
    return render_template('clothing.html')

@views.route('/catalog/accessories')
def accessories():
    return render_template('accessories.html')

@views.route('/catalog/gifts')
def gifts():
    return render_template('gifts.html')
