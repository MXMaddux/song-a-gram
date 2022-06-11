from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = "Boogie"
limiter = Limiter(
    app,
    key_func=get_remote_address, # get users IP address.
    default_limits=["200 per day", "50 per hour"], # default limit to 300K request per month
)