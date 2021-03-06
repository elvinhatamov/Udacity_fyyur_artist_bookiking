#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, config, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler, error
from flask_wtf import Form, form
from sqlalchemy.orm import backref, relation, relationship
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(300))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)


    # DONE: implement any missing fields, as a database migration using Flask-Migrate
    # implemented genres, not sure if it's right tho, looking at the Artist genres tho it seems right

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(300))
    seeking_shows = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)

    # DONE: implement any missing fields, as a database migration using Flask-Migrate

# DONE: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# creates a collection of Show objects for Artist
shows = db.relationship("shows", backref="artists")

class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable = False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable = False)
  start_time = db.Column(db.DateTime, nullable = False)

  def __repr__(self):
    return '<Show {} {}>'.format(self.artist_id, self.venue_id)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # date = dateutil.parser.parse(value)
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
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
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  # sets currenttime so we know which shows were in the past and which are upcoming
  current_time = datetime.now()
  venue_city_state = ''

  data = []
  # queries Venue db for all records
  venues = Venue.query.all()

  for venue in venues:
    upcomingshows = venue.shows

    filtered_upcomingshows = [show for show in upcomingshows if show.start_time > current_time]

    if venue_city_state == venue.city + venue.state:
      data[len(data) - 1]["venues"].append({
        "id": venue.id, 
        "name": venue.name,
        "num_upcoming_shows": len(filtered_upcomingshows)
      })
    else:
      venue_city_state == venue.city + venue.state
      data.append({
        "city": venue.city, 
        "state": venue.state, 
        "venues": [{
          "id": venue.id, 
          "name": venue.name, 
          "num_upcoming_shows": len(filtered_upcomingshows)
        }]
      })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # JUST NEED TO MAKE UPCOMING AND PAST SHOWS APPEAR THEN DONE
  
  # query db for the venue's ID
  venuequery = Venue.query.get(venue_id)

  shows = Show.query.all()
  filtshows = [show for show in shows if show.venue_id == venue_id]

  # if it finds a venue with that ID
  if venuequery:
    venue_details = venuequery

    data1= {
      "id": venue_details.id, 
      "name": venue_details.name, 
      "genres": venue_details.genres, 
      "addres": venue_details.address, 
      "city": venue_details.city, 
      "state": venue_details.state, 
      "phone": venue_details.phone, 
      "website": venue_details.website, 
      "facebook_link": venue_details.facebook_link, 
      "seeking_talent": venue_details.seeking_talent, 
      "seeking_description": venue_details.seeking_description, 
      "image_link": venue_details.image_link, 
      # "past_shows": [{
      #   "artist_id": show.artist_id, 
      #   "artist_name": artist.
      # }]
      }
 
# "past_shows": [{
#        "artist_id": 4,
#        "artist_name": "Guns N Petals",
#        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#        "start_time": "2019-05-21T21:30:00.000Z"
#      }],
#      "upcoming_shows": [],
#      "past_shows_count": 1,
#      "upcoming_shows_count": 0,

  return render_template('pages/show_venue.html', venue=data1)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead

  form = VenueForm(request.form)

  error = False
  
  try:
    venue = Venue(
      name = form.name.data, 
      city = form.city.data, 
      state = form.state.data, 
      address = form.address.data, 
      phone = form.phone.data, 
      genres = form.genres.data, 
      facebook_link = form.facebook_link.data, 
      # website = form.website.data, 
      # seeking_talent = form.seeking_talent.data, 
      # seeking_description = form.seeking_description.data
    )

    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured, venue could not be added.')
  
  finally:
    db.session.close()

  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # MIGHT BE DONE BUT CAN'T TRY TIL I FIX SHOWING THE VENUE PAGE, THEN I NEED TO
  # IMPLEMENT DELETE BUTON IN THE HTML.

  error = False

  try:
    venue = Venue(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue has been successfully deleted.')

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info)
    flash('An error has occured, venue could not be deleted.')
  
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database

  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  
  # query db for the artist's ID
  artistquery = Artist.query.get(artist_id)

  # if it finds an artist with that ID
  if artistquery:
    artist_details = artistquery

    data= {
      "id": artist_details.id, 
      "name": artist_details.name, 
      "genres": artist_details.genres, 
      "city": artist_details.city, 
      "state": artist_details.state, 
      "phone": artist_details.phone, 
      "website": artist_details.website, 
      "facebook_link": artist_details.facebook_link, 
      "seeking_venue": artist_details.seeking_shows, 
      "seeking_description": artist_details.seeking_description, 
      "image_link": artist_details.image_link, 
      }
  
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
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
  # DONE: insert form data as a new Artist record in the db, instead
  # DONE: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)

  error = False
  
  try:
    artist = Artist(
      name = form.name.data, 
      city = form.city.data, 
      state = form.state.data, 
      phone = form.phone.data, 
      genres = form.genres.data, 
      facebook_link = form.facebook_link.data, 
      # website = form.website.data, 
      # seeking_shows = form.seeking_shows.data, 
      # seeking_description = form.seeking_description.data
    )

    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured, artist could not be added.')
  
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

  # current_time = datetime.now()

  data = []

  allshows = Show.query.all()

  for show in allshows:
    artist = Artist.query.get(show.artist_id)
    venue = Venue.query.get(show.venue_id)

    # if show.start_time > current_time:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": venue.name,
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time
    })
  
  
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead

  form = ShowForm(request.form)

  error = False
  
  try:
    show = Show(
      artist_id = form.artist_id.data, 
      venue_id = form.venue_id.data, 
      start_time = form.start_time.data
    )

    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured, show could not be added.')
  
  finally:
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
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
    app.run(host='0.0.0.0', port=5000)