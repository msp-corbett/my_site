from app import db, ma

# widget_example = {
# 'id': 1,
# 'name': 'WX5',
# 'size': '2XL',
# 'fizzler : {
#     'id': 1,
#     'name': 'FZ_900'
#     'color': 'Red'
#     'speed': 20.0
#     },
# 'bangers': [
#     {
#         'id': 1,
#         'type': 'YLW'
#     },
#     {
#         'id': 2,
#         'type': 'BLK'
#     }
#     ]
# }

class Widget(db.Model):
    __tablename__ = 'Widget'
    ID = db.Column(db.Integer)
    Name = db.Column(db.String(150))
    Size = db.Column(db.String(5))

    fizzler = db.relationship("Fizzler", back_populates='Widget')


class Fizzler(db.Model):
    __tablename__ = "Fizzler"
    ID = db.Column(db.Intger)
    Name = db.Column(db.String(150))
    Color = db.Column(db.String(10))
    Speed = db.Column(db.Numeric(precision=5, scale=1))
    WidgetID = db.Column(db.Integer)

    widget = db.relationship("Widget", back_populates='Fizzler')

class Banger(db.Model):
    __tablename__ = "Banger"
    ID = db.Column(db.Integer)
    Type = db.Column(db.String(3))

    widget = db.relationship("Widget", back_populates='Banger')

class BangerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Banger

class FizzlerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Fizzler

class WidgetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Widget
    
    fizzler = ma.Nested(FizzlerSchema)
    banger = ma.Nested(BangerSchema).many()