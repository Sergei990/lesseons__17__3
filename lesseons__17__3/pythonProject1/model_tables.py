# from http.cookiejar import offset_from_tz_string

from flask import Flask
from sqlalchemy import or_, desc, func
from flask_sqlalchemy import SQLAlchemy
from data_for_table import data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genres = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    directors = db.relationship("Director")

    def add_all_movie(self):
        """Добавляет данные в таблицу"""

        for movie in data['movies']:
            m = Movie(
                id=movie["pk"],
                title=movie["title"],
                description=movie["description"],
                trailer=movie["trailer"],
                year=movie["year"],
                rating=movie["rating"],
                genre_id=movie["genre_id"],
                director_id=movie["director_id"]
            )
            with app.app_context():
                db.session.add(m)
                db.session.commit()

    def get_all_movies(self):
        """Возвращает все фильмы из базы данных"""
        with app.app_context():
            result = db.session.query(Movie).limit(5).offset(0).all()

        return result

    def get_one_movie_by_id(self, iup):
        """Возвращает  один фильм по Id"""
        with app.app_context():
            movie = db.session.query(Movie).filter(Movie.id == iup).one()
        return movie

    def get_one_movie_by_director(self, id):
        """Возвращает фильмы по режиссерам"""
        with app.app_context():
            movies_by_director = db.session.query(Movie).filter(Movie.director_id == id).all()
            # Если нет фильма
            if not movies_by_director:
                return Exception
        return movies_by_director

    def get_one_movie_by_genre(self, genre_id):
        """Возвращает фильмы по жанру"""
        with app.app_context():
            genre = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()

        return genre


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    directors = db.relationship('Movie')

    def add_all_direktors(self):
        """Добавляет режиссеров в БД"""
        for director in data['directors']:
            all_director = Director(
                id=director['pk'],
                name=director['name']

            )
            with app.app_context():
                db.session.add(all_director)
                db.session.commit()

    def get_all_directors(self):
        """Возвращает всех режиссеров"""
        with app.app_context():
            all_directors = db.session.query(Director).all()
        return all_directors

    def get_one_director_by_id(self, uip):
        """Возвращает одного директора по ID"""
        with app.app_context():
            one_director = db.session.query(Director).filter(Director.id == uip).one()
        return one_director


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    genres = db.relationship('Movie')

    def add_all_gnres(self):
        """Добавляет жанры в БД"""
        for genre in data['genres']:
            genres = Genre(
                id=genre['pk'],
                name=genre['name']
            )
            with app.app_context():
                db.session.add(genres)
                db.session.commit()

    def get_all_genres(self):
        """Возвращает все жанры"""
        with app.app_context():
            query_by_genre = db.session.query(Genre).all()
        return query_by_genre

    def get_one_genre_by_id(self, id):
        """Возвращает жанр по ID"""
        with app.app_context():
            get_one_genre = db.session.query(Genre).filter(Genre.id == id).one()
        return get_one_genre


directors = Director()
movies = Movie()
genres = Genre()
if __name__ == '__main__':
    with app.app_context():
        print('ok', movies.get_one_movie_by_genre(7))
