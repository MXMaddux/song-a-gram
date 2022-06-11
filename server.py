from flask_app import app as application

from flask_app.controllers import users

if __name__=="__main__":
    application.run(debug=True)