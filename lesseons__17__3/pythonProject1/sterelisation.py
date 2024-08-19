from marshmallow import Schema, fields

from model_tables import movies, directors


class DirectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class GenreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class MoviesSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Integer()
    # genre_id = fields.Nested(DirectorSchema)
    genre = fields.Nested(DirectorSchema)
    # director_id = fields.Nested(GenreSchema)
    director = fields.Nested(GenreSchema)


movieschemas = MoviesSchema(many=True)
movieschema = MoviesSchema()
directorschema = DirectorSchema()
directorschemas = DirectorSchema(many=True)
genreschemas = GenreSchema(many=True)
genreschema = GenreSchema()

