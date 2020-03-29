from sqlalchemy import PrimaryKeyConstraint
from app import db, ma

class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = (
        PrimaryKeyConstraint(
            'ID',
            name='PK_User_ID'
        ),
    )

    ID = db.Column(db.Integer)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(320))

    def __repr__(self):
        return f'Model({self.ID}: {self.Name})'

    def __str__(self):
        return f'{self.Name}'


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User