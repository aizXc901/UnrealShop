from flask_login import login_required, current_user


from .models import Product, CartItem
from .db import db
from .send_email import send_email
from sqlalchemy.sql import text
from flask import Blueprint, render_template, session
from flask import redirect, url_for, request
from flask_login import login_required, current_user


views = Blueprint('views', __name__)


@views.route('/')
def home():
    try:
        # Проверяем подключение к БД
        db.session.execute(text("SELECT 1"))

        products = Product.query.limit(3).all()  # Получаем первые 3 продукта
        return render_template("home.html", products=products)

    except Exception as e:
        print(f"Ошибка БД: {e}")
        return "<center><h2>Добро пожаловать в UnrealShop (режим без БД)</h2></center>"

@views.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@views.route('/cart')
@login_required  # Доступно только авторизованным
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)


@views.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required  # Доступно только авторизованным
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    # Проверяем, есть ли товар уже в корзине
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()

    if cart_item:
        # Если товар уже в корзине, увеличиваем количество
        cart_item.quantity += 1
    else:
        # Иначе создаем новую запись
        cart_item = CartItem(user_id=current_user.id, product_id=product.id)
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('views.product', product_id=product.id, cart_item=cart_item))


@views.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)

    if cart_item.user_id != current_user.id:
        return redirect(url_for('views.cart'))

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        # Удаляем товар из корзины, если количество <= 1
        db.session.delete(cart_item)

    db.session.commit()
    return redirect(url_for('views.cart'))

@views.route('/cart/decrease/<int:product_id>', methods=['POST'])
@login_required
def decrease_quantity(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            db.session.commit()
        else:
            db.session.delete(cart_item)
            db.session.commit()
    return redirect(request.referrer or url_for('views.cart'))

@views.route('/catalog')
def catalog():
    return render_template('catalog.html')


@views.route('/catalog/clothing')
def clothing():
    clothes = Product.query.filter_by(category='clothing').all()
    return render_template('clothing.html', products=clothes)


@views.route('/catalog/accessories')
def accessories():
    items = Product.query.filter_by(category='accessories').all()
    return render_template('accessories.html', products=items)


@views.route('/catalog/gifts')
def gifts():
    items = Product.query.filter_by(category='gifts').all()
    return render_template('gifts.html', products=items)


@views.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = None  # по умолчанию значение

    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    else:
        # сессия для временного хранения
        cart = session.get('cart', {})
        # если над проверить наличие товара в корзине гостя
        in_cart = str(product.id) in cart
        # Можно передать в шаблон флаг или количество
        return render_template('product.html', product=product, in_cart=in_cart)

    return render_template('product.html', product=product, cart_item=cart_item)


@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/cart/checkout')
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    sum = 0
    for item in cart_items:
        sum += item.product.price * item.quantity
    sum = round(sum, 2)
    return render_template('checkout.html', cart_items=cart_items, sum=sum)


@views.route('/order_message')
@login_required
def order_message():
    success = send_email(current_user)

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    for item in cart_items:
        db.session.delete(item)  # удаление заказанных товаров из корзины
    db.session.commit()

    return render_template('order_message.html', success=success)