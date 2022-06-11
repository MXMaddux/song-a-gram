
from flask import flash
import re
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONENUMBER_REGEX = re.compile(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})")


class User:


    @staticmethod
    def is_valid(information):
        is_valid = True
        if len(information['your_name']) < 2:
            flash("Please input your name", "information")
            is_valid = False
        if len(information['friend_name']) < 2:
            flash("Please input your friend's name", "information")
            is_valid = False
        if len(information['friend_number']) < 10:
            flash('Please input a valid phone number', "information")
        if len(information['artist']) < 2:
            flash("Please input an artist or band name", "information")
            is_valid = False
        if len(information['song_title']) < 2:
            flash("Please input a song title", "information")
            is_valid = False
        return is_valid
