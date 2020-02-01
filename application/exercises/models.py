from application import db
from application.models import Base
        
class Exercise(Base):

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.Text, nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),nullable=False)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def change_description(self, description):
        self.description = description
