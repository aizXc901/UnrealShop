from .models import CartItem
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_login import current_user

admin_email = 'lidamoskvina2008@gmail.com'  # эл. почта администратора, на которую приходит заказ


def send_email(customer, to_email=admin_email):
    def form_title():
        title = f"Новый заказ от {customer.email}"
        return title

    def form_message():
        message = "ЗАКАЗ\n"

        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        sum = 0
        for item in cart_items:
            about_item = (f"{item.product.name} ({item.product.price} руб.) - "
                          f"{item.quantity} шт.\n"
                          f"Общая стоимость: {round(item.quantity * item.product.price, 2)}\n")
            message += about_item
            message += "\n"
            sum += round(item.quantity * item.product.price, 2)
        message += f"ИТОГО: {sum}\n\n"
        message += "Почта для связи с покупателем:\n"
        message += customer.email

        return message

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = 'unrealshopyandexlyceumproject@gmail.com'  # адрес электронной почты магазина
    password = 'gkgxknvfyucofjsj'  # пароль от электронной почты

    subject = form_title()
    body = form_message()

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        server.quit()
