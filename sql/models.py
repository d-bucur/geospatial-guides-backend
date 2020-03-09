from geoalchemy2 import Geography

from sql import db

KEY_TYPE = db.Integer


purchased_guides = db.Table('user_purchased_guides',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('guide_id', db.Integer, db.ForeignKey('guide.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(KEY_TYPE, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    guides = db.relationship('Guide', backref='user', lazy=True)
    purchased_guides = db.relationship('Guide', secondary=purchased_guides, lazy='subquery',
                             backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %s: %s>' % (self.id, self.email)


class Place(db.Model):
    id = db.Column(KEY_TYPE, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    position = db.Column(Geography('POINT'))
    tags = db.Column(db.Text)

    guides = db.relationship('Guide', backref='place', lazy=True)

    def __repr__(self):
        return '<Place %s: %s>' % (self.id, self.name)


class Guide(db.Model):
    id = db.Column(KEY_TYPE, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    full_text = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    download_link = db.Column(db.String(200), nullable=False)

    place_id = db.Column(KEY_TYPE, db.ForeignKey('place.id'), nullable=False)
    user_id = db.Column(KEY_TYPE, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Guide %s>' % self.id
