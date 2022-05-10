from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    username = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    trainer_since = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.String)
    # team = db.relationship('Trainer',
    #         primaryjoin=)

    def __repr__(self):
        return f'<User: {self.username} | {self.id} >'    

    def __str__(self):
        return f'<User: {self.username} | {self.first_name} {self.last_name}>'

    def hash_password(self, orinigal_password):
        return generate_password_hash(orinigal_password)

    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    def save(self):
        db.session.add(self)
        db.session.commit() 

    def get_icon_url(self):
        return f"{self.icon}"

class Pokedex(db.Model):
    pd_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hp = db.Column(db.Integer)

class PokeTrainer(db.Model):
    trainer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


    # def catch_em_all(self, pokemon):
    #     self.poketeam.append(pokemon)
    #     db.session.commit()

class PokeTeam(db.Model):
    pokedex_id = db.Column(db.Integer, db.ForeignKey('pokedex.pd_id'), primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('poketrainer.user_id'), primary_key=True)
        



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    