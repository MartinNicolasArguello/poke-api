from . import db


class Pokemon(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    type = db.Column(db.String(100))
    height = db.Column(db.String(100))
    weight = db.Column(db.String(
        100))
    image = db.Column(db.String(
        1000))
    black_listed = db.Column(db.Boolean())
    modified = db.Column(db.Boolean())

    def __init__(self, name, type, height, weight, image, modified, black_listed):
        self.name = name
        self.type = type
        self.height = height
        self.weight = weight
        self.image = image
        self.modified = modified
        self.black_listed = black_listed
