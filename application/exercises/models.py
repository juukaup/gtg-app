from application import db
        
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.Text, nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),nullable=False)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def change_description(self, description):
        self.description = description
