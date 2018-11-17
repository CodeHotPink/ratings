"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    html = render_template("homepage.html")
    return html

@app.route('/movies')
def movies_list():
    """Shows list of movies"""
    movies = Movie.query.order_by('title').all()
    return render_template("movies_list.html", movies=movies)

@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get(movie_id)
    movie_ratings = Rating.query.filter_by(movie_id=movie_id).all()
    return render_template('movie.html', movie=movie,
                                        movie_ratings=movie_ratings)

@app.route('/add_rating', methods=['POST'])
def add_rating():
    score = request.form.get("score")
    user_id = session['user_id']
    rating = Rating(movie_id=)


@app.route('/users')
def user_list():
    """Shows list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show info about user"""
    user = User.query.get(user_id)
    rated_movies = Rating.query.filter_by(user_id=user.user_id).all() 
    return render_template("user.html", user=user,
                                        rated_movies=rated_movies)    

@app.route("/register", methods=["GET"])
def register_form():
    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():
    password = request.form.get("password")
    email = request.form.get("email")
    print(email)

    if  User.query.filter_by(email=email).first():
        flash('This email is already registered')
        return redirect("/login")
    else:
        user = User()
        user.email = email 
        user.password = password
        db.session.add(user)
        db.session.commit()
        return redirect("/")

@app.route('/login')
def login_form():
    return render_template("login_form.html",)

@app.route('/login-attempt')
def login_request():
    password = request.args.get("password")
    email = request.args.get("email")
    if User.query.filter_by(email=email).first():
        user = User.query.filter_by(email=email).first()
        if user.password == password:
            session["user_id"] = user.user_id
            flash('You are successfully logged in.')
            return redirect(f'/users/{user.user_id}')
        else:
            flash("Invalid credentials")
            return redirect("/login")
    else:
        flash("That email is not in our system")
        return redirect ("/login")

@app.route('/logout')
def logout():
    session.clear()
    flash("You are successfully logged out")
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
