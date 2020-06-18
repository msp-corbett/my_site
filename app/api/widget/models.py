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
    """ A widget class """

    __tablename__ = 'Widget'

    ID = db.Column(
        db.Integer,
        primary_key=True)

    Name = db.Column(
        db.String(150))

    Size = db.Column(
        db.String(5))


class Fizzler(db.Model):
    """ Fizzler extends widget model """

    __tablename__ = "Fizzler"

    ID = db.Column(
        db.Integer, primary_key=True)

    Name = db.Column(
        db.String(150))

    Color = db.Column(
        db.String(10))

    Speed = db.Column(
        db.Numeric(precision=5, scale=1))

    WidgetID = db.Column(
        db.Integer,
        db.ForeignKey("Widget.ID"))

    widget = db.relationship(
        "Widget",
        backref='fizzler')


class Banger(db.Model):
    """ Banger extends the widget """

    __tablename__ = "Banger"

    ID = db.Column(
        db.Integer,
        primary_key=True)

    Type = db.Column(
        db.String(3))

    WidgetID = db.Column(
        db.Integer, db.ForeignKey("Widget.ID"))

    widget = db.relationship(
        "Widget",
        backref='banger')


class BangerSchema(ma.SQLAlchemyAutoSchema):
    """ Banger Schema
    """
    class Meta:
        model = Banger


class FizzlerSchema(ma.SQLAlchemyAutoSchema):
    """ Fizzler Schema
    """
    class Meta:
        model = Fizzler


class WidgetSchema(ma.SQLAlchemyAutoSchema):
    """ Widget Schema
    """
    class Meta:
        model = Widget

    fizzler = ma.Nested(FizzlerSchema)
    banger = ma.Nested(
        BangerSchema,
        many=True)
