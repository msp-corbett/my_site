from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint
from app import db, ma

class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = (
        PrimaryKeyConstraint(
            'ID',
            name='PK_User_ID'
        ),
        UniqueConstraint(
            "UserName",
            name="UNQ_UserName"
        ),
        UniqueConstraint(
            "Email",
            name="UNQ_Email"
        ),
    )

    ID = db.Column(db.Integer)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    UserName = db.Column(db.String(100))
    Email = db.Column(db.String(320))

    def __repr__(self):
        return f'Model({self.ID}: {self.Name})'

    def __str__(self):
        return f'{self.Name}'


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User