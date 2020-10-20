from marshmallow import Schema, fields


class UrlQuerySchema(Schema):
    number_plants = fields.Integer()
    state_abbreviation = fields.String()
