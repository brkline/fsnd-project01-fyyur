from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String(120)))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(800))
    shows = db.relationship('Show', backref='Venue',
                            lazy=True, cascade='all, delete-orphan')
    UniqueConstraint('name', 'city', 'state', 'address',
                     name='unique_name_city_state_address')

    @property
    def upcoming_shows(self):
        upcoming_shows = [
            show for show in self.shows if show.start_time > datetime.now()]
        return upcoming_shows

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    @property
    def past_shows(self):
        past_shows = [
            show for show in self.shows if show.start_time < datetime.now()]
        return past_shows

    @property
    def past_shows_count(self):
        return len(self.past_shows)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(800))
    shows = db.relationship('Show', backref='Artist', lazy=True)

    @property
    def upcoming_shows(self):
        upcoming_shows = [
            show for show in self.shows if show.start_time > datetime.now()]
        return upcoming_shows

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    @property
    def past_shows(self):
        past_shows = [
            show for show in self.shows if show.start_time < datetime.now()]

        return past_shows

    @property
    def past_shows_count(self):
        return len(self.past_shows)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
