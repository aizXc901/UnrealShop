from flask import Blueprint, render_template
from .models import Product
from .db import db
from sqlalchemy.sql import text
from flask import Blueprint, render_template, request, redirect, url_for



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
