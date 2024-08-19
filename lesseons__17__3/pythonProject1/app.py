from logging import exception

from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from model_tables import movies, Movie, directors, Director, genres, Genre
from sterelisation import movieschema, movieschemas, directorschemas, directorschema, genreschemas, genreschema

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


# api = Api.namespace('movies')
@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        """Возвращает все фильмы.
        Возвращает фильмы по режиссерам или по жанру
        """
        query_director_by_id = request.args.get('director_id')
        query_genre_by_id = request.args.get('genre_id')
        # Если в URL есть поиск по режиссеру
        if query_director_by_id:
            # Возвращаем фильмы по режиссерам
            return movieschemas.dump(movies.get_one_movie_by_director(query_director_by_id))
        # Если в URL строке есть поиск по жанру
        if query_genre_by_id:
            # Возвращаем фильмы по жанру
            return movieschemas.dump(movies.get_one_movie_by_genre(query_genre_by_id))
        # Возвращаем все фильмы
        return movieschemas.dump(movies.get_all_movies()), 200

    def post(self):
        """Добавляет фильм"""
        try:
            new_movie = request.json
            with app.app_context():
                db.session.add(Movie(**new_movie))
                db.session.commit()
            return "Фильм добавлен", 200
        except Exception:
            db.session.rollback()
            return "Фильм не добавлен", 400


@movies_ns.route('/<int:uip>')
class MoviesViewOne(Resource):
    def get(self, uip: int):
        """Возвращает фильм по ID"""
        try:
            result_id = movieschema.dump(movies.get_one_movie_by_id(uip))
            return result_id, 200
        except Exception:
            return f'нет такого фильма с id:{uip}', 404


@movies_ns.route('/genre/<int:id>')
class MovieViewGenre(Resource):
    """Возвращает фильмы по жанру"""

    def get(self, id: int):
        try:
            result_genre = movieschemas.dump(movies.get_one_movie_by_genre(id))
            return result_genre, 200
        except Exception:
            return "", 404


@directors_ns.route('/')
class DirectorViewAll(Resource):
    def get(self):
        all_directors = directors.get_all_directors()
        return directorschemas.dump(all_directors)

    def post(self):
        """Добавляет одного режиссера в бд"""
        try:
            file = request.json
            with db.session.begin():
                db.session.add(Director(**file))
                db.session.commit()
            return "Режиссер добавлен", 308
        except Exception:
            # Если ошибка добавления режиссера
            db.session.rollback()
            return "Режиссер не добавлен", 400


@directors_ns.route('/<int:uip>')
class DirectorViewOne(Resource):
    """Обновляет режиссера"""

    def put(self, uip):
        try:
            query_for_director = request.json
            one_director = directors.get_one_director_by_id(uip)

            one_director.name = query_for_director.get('name')

            db.session.add(one_director)
            db.session.commit()
            return 'Успешно', 201
        except Exception:
            # Если возникла ошибка обновления режиссера
            db.session.rollback()
            return "не успешно", 404

    def delete(self, uip):
        """Удаляет одного режиссера из бд"""
        try:
            db.session.delete(directors.get_one_director_by_id(uip))
            db.session.commit()
            return 'Успешно', 200
        except Exception:
            db.session.rollback()
            return 'Не успешно', 400


@genres_ns.route('/')
class GenreViewAll(Resource):
    """Возвращает все жанры"""

    def get(self):
        all_genres = genreschemas.dump(genres.get_all_genres())
        return all_genres

    def post(self):
        """Добавляет один жанр"""
        try:
            query_genre = request.json
            db.session.add(Genre(**query_genre))
            db.session.commit()
            return 'Успешно', 308
        except Exception:
            db.session.rollback()
            return 'Не успешно'


@genres_ns.route('/<int:id>')
class GenreViewOne(Resource):
    """Обновляет жанр"""

    def put(self, id):
        try:
            query_genre_for_method_put = request.json
            genre_one = genres.get_one_genre_by_id(id)
            genre_one.name = query_genre_for_method_put.get('name')

            db.session.add(genre_one)
            db.session.commit()
            return 'Успешно', 201
        except Exception:
            db.session.rollback()
            return 'Не успешно', 404

    def delete(self, id):
        """Удаляет один жанр"""
        try:
            genre_delete_by_id = genres.get_one_genre_by_id(id)
            db.session.delete(genre_delete_by_id)
            db.session.commit()
            return 'Успешно '
        except Exception:
            db.session.rollback()
            return 'Не успешно'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000, debug=True)
