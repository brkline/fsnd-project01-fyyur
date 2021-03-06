#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.exc import DataError
from models import db, Artist, Venue, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migration = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE_URI')

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    unique_city_state = Venue.query.with_entities(
        Venue.city, Venue.state).distinct().all()
    for city_state in unique_city_state:
        city = city_state[0]
        state = city_state[1]
        venues = Venue.query.filter_by(city=city, state=state).all()
        shows = venues[0].upcoming_shows
        data.append({
            "city": city,
            "state": state,
            "venues": venues
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    #
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%'))
    data = []
    for venue in venues:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "upcoming_shows_count": venue.upcoming_shows_count
        })
    count = len(data)
    response = {
        "count": count,
        "data": data
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    if venue:
        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": True if venue.seeking_talent in (True, 't', 'True') else False,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link if venue.image_link else "",
            "past_shows_count": venue.past_shows_count,
            "upcoming_shows_count": venue.upcoming_shows_count,
        }

    past_shows = []
    for show in venue.past_shows:
        artist = Artist.query.get(show.artist_id)
        past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time)
        })

    upcoming_shows = []
    for show in venue.upcoming_shows:
        artist = Artist.query.get(show.artist_id)
        upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time)
        })

    data["past_shows"] = past_shows
    data["upcoming_shows"] = upcoming_shows
    # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    venue = Venue()
    for field in request.form:
        if field == 'genres':
            setattr(venue, field, request.form.getlist(field))
        elif field == 'seeking_talent':
            setattr(venue, field, True if request.form.get(
                field) in ('y', True, 't', 'True') else False)
        else:
            setattr(venue, field, request.form.get(field))

    try:
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    except DataError as e:
        error = str(e)
        flash('An error occurred. Show could not be listed. \n' + error)
        db.session.rollback()
        flash('An error occurred. Venue ' +
              venue.name + ' could not be listed.')
        return render_template('pages/home.html')

    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    venue = Venue.query.get(venue_id)
    try:
        # venue.delete()
        db.session.delete(venue)
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully deleted!')

    except DataError as e:
        error = str(e)
        flash('An error occurred. Venue ' +
              venue.name + ' could not be deleted.')
        db.session.rollback()
        return None

    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
    data = []
    artist_count = len(artists)
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
            "upcoming_shows_count": artist.upcoming_shows_count
        })

    response = {
        "count": artist_count,
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    artist = Artist.query.get(artist_id)
    past_shows = []
    for show in artist.past_shows:
        venue = Venue.query.get(show.venue_id)
        past_shows.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": str(show.start_time)
        })
    upcoming_shows = []
    for show in artist.upcoming_shows:
        venue = Venue.query.get(show.venue_id)
        upcoming_shows.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": str(show.start_time)
        })
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "seeking_venue": True if artist.seeking_venue in ('y', True, 't', 'True') else False,
        "seeking_description": artist.seeking_description,        
        "image_link": artist.image_link,
        "facebook_link": artist.facebook_link,
        "website": artist.website,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": artist.past_shows_count,
        "upcoming_shows_count": artist.upcoming_shows_count
    }
 
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    for field in request.form:
        if field == 'genres':
            setattr(artist, field, request.form.getlist(field))
        elif field == 'seeking_venue':
            setattr(artist, field, True if request.form.get(
                field) in ('y', True, 't', 'True') else False)
        else:
            setattr(artist, field, request.form.get(field))

    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    except DataError as e:
        error = str(e.__dict__['orig'])
        flash('An error occurred. Artist ' +
              artist.name + ' could not be listed.')
        db.session.rollback()
        db.session.close()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    for field in request.form:
        if field == 'genres':
            setattr(venue, field, request.form.getlist(field))
        elif field == 'seeking_talent':
            setattr(venue, field, True if request.form.get(
                field) in ('y', True, 't', 'True') else False)
        else:
            setattr(venue, field, request.form.get(field))
    try:
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    except DataError as e:
        error = str(e.__dict__['orig'])
        flash('An error occurred. Show could not be listed. \n' + error)
        db.session.rollback()
        flash('An error occurred. Venue ' +
              venue.name + ' could not be listed.')
        return render_template('pages/home.html')

    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    artist = Artist()
    for field in request.form:
        if field == 'genres':
            setattr(artist, field, request.form.getlist(field))
        elif field == 'seeking_venue':
            setattr(artist, field, True if request.form.get(
                field) in ('y', True, 't', 'True') else False)
        else:
            setattr(artist, field, request.form.get(field))

    try:
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    except DataError as e:
        error = str(e)
        db.session.rollback()
        flash('An error occurred. Artist ' +
              artist.name + ' could not be listed.\n' + e)
        # return render_template('pages/home.html')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # displays list of shows at /shows
    query = Show.query.join(
        Venue, (Venue.id == Show.venue_id)
    ).join(
        Artist, (Artist.id == Show.artist_id)
    ).with_entities(Show.venue_id, Venue.name.label('venue_name'), Show.artist_id, Artist.name.label('artist_name'), Artist.image_link, Show.start_time)

    data = []
    for x in query:
        data.append({
            "venue_id": x.venue_id,
            "venue_name": x.venue_name,
            "artist_id": x.artist_id,
            "artist_name": x.artist_name,
            "artist_image_link": x.image_link,
            "start_time": str(x.start_time)
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    show = Show(
        start_time=request.form.get('start_time'),
        venue_id=request.form.get('venue_id'),
        artist_id=request.form.get('artist_id')
    )

    try:
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    except DataError as e:
        error = str(e)
        flash(error + '\nAn error occurred. Show could not be listed.')
        db.session.rollback()
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
