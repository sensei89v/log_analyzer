from marshmallow import Schema, fields


# TODO: add обязательность
class LogSchema(Schema):
    client_id = fields.Str()
    user_agent = fields.Str(data_key="User-Agent")
    location = fields.Str(data_key="document.location")
    referer = fields.Str(data_key="document.referer")
    date = fields.DateTime()
