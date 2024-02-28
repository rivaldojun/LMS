from Main.controllers.scheduler import *
from flask_migrate import Migrate
from Main import *
from jinja2.filters import do_striptags


app.jinja_env.filters['strip_tags'] = do_striptags

with app.app_context():
        db.create_all()
#end model



if __name__ == "__main__":
    schedule_email_reminders()
    app.run(debug=False)
