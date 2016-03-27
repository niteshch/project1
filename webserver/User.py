from datetime import datetime
from flask.ext.login import login_user , logout_user , current_user , login_required, UserMixin
class User(UserMixin):
    def __init__(self, user_id, username ,password , email, active=True,registered_on=datetime.utcnow()):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.active = active
        self.registered_on = registered_on
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return self.active
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.user_id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)
