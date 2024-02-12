from controllers.scheduler import *
from routes import app,db


with app.app_context():
        db.create_all()
#end model



if __name__ == "__main__":
    schedule_email_reminders()
    app.run(debug=True)
