from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint
from app import db, ma, encrypt

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
    PasswordHash = db.Column(db.String(128))

    def is_active(self,):
        """ Flask-Login requirement
        
        returns True as all Users are considered 'Active'
        """
        return True

    def get_id(self,):
        """Flask-Login requirement
        
        returns UserName
        
        """

        return self.UserName

    def is_authenticated(self,):
        """Flask-Login requirement
        
        returns True as all Users are considered authenticated.
        
        """
        return True

    def is_anonymous(self,):
        """Flask-Login requirement
        
        returns False as anonymous User is unsupported.
        
        """
        return False

    def set_password(self, password):
        """ Use Flask Bcrypt to hash user password.
        """
        self.PasswordHash = encrypt.generate_password_hash(
            password).decode("utf-8")

    def check_password(self, password):
        """ User Flask Bcrypt to validate password against stored hash """
        return encrypt.check_password_hash(
            self.PasswordHash.encode("utf-8"),
            password)

    def __repr__(self):
        return f'Model({self.ID}: {self.Name})'

    def __str__(self):
        return f'{self.Name}'


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User