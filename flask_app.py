# from flask import Flask, render_template, url_for
# import sqlalchemy

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mail.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

# @app.route('/')
# @app.route('/home')
# def index():
#     return render_template('index.html')
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_email():
    email = request.form.get('textInput', '').strip().lower()
    print(email[-4:-1]+email[-1])
    if ("@" in email and "." in email and ((email[-3:-1]+email[-1] ==".ru") and (email[-4]!="@") or (email[-4:-1]+email[-1] ==".com") and (email[-5]!="@"))):
        new_user = User(email=email)
        db.session.add(new_user)
        db.session.commit()

    flash('Спасибо за подписку!', 'success')
    return redirect(url_for('index'))
# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных
    app.run(debug=True)