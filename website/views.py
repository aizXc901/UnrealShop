from flask import Blueprint, render_template, flash, redirect, request, jsonify
from . import db
from intasend import APIService


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return ("<center><h2>Добро пожаловать в наш магазин 'UnrealShop'</h2></center>")