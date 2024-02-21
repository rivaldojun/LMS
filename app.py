from Main.controllers.scheduler import *
from flask_migrate import Migrate
from Main import *


with app.app_context():
        db.create_all()
#end model


if __name__ == "__main__":
    schedule_email_reminders()
    app.run(debug=True)
