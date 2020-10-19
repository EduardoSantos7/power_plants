from marshmallow import Schema, fields


class UrlQuerySchema(Schema):
    number_plants = fields.Integer(required=True)
    state_abbreviation = fields.String()
