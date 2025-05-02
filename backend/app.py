from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sdckl_printing.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from backend import models, routes

if __name__ == '__main__':
    app.run(debug=True)
