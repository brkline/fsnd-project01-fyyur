from datetime import datetime
from flask_wtf import Form
from flask_wtf.form import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import re
from wtforms.fields.core import BooleanField
from enums import State, Genre


def get_genre_choices(enum):
    choices = []
    for genre in enum:
        choices.append((genre.name, genre.value))
    return choices


def get_state_choices(enum):
    choices = []
    for state in enum:
        choices.append((state.name, state.value))
    return choices


class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=get_state_choices(State)
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )

    phone = StringField(
        'phone'
    )

    image_link = StringField(
        'image_link'
    )

    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=get_genre_choices(Genre)
    )

    website = StringField(
        'website', validators=[URL()]
    )

    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

    seeking_talent = BooleanField(
        'seeking_talent'
    )

    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=get_state_choices(State)
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=get_genre_choices(Genre)
    )
    website = StringField(
        'website', validators=[URL()]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )

    seeking_venue = BooleanField(
        'seeking_venue'
    )

    seeking_description = StringField(
        'seeking_description'
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
