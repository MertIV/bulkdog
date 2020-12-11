from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from app import login
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(13))
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attachment = db.Column(db.String())
    template_body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Message {}>'.format(self.id)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_phone = db.Column(db.String(13), index=True, unique=True)
    customer_status = db.Column(db.Integer)
    insert_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Customer {}>'.format(self.id)

# #
# class MessageDetail(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     md_id = db.Column(db.Integer)
#     m_id = db.Column(db.Integer, db.ForeignKey('message.id'))
#     attachment_path = db.Column(db.String)
#     insert_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     update_date = db.Column(db.DateTime)
#
#     def __repr__(self):
#         return '<MessageDetail {}>'.format(self.body)
#
# #
# # message_activity = db.Table('Message_Activity', db.Column('u_id', db.Integer, db.ForeignKey('User.id')),
# #                             db.Column('c_id', db.Integer, db.ForeignKey('Costumer.id')),
# #                             db.Column('m_id', db.Integer, db.ForeignKey('Message.id')),
# #                             db.Column('template_body', db.String, db.ForeignKey('Message.template_body')),
# #                             db.Column('send_date', db.DateTime))
# #
