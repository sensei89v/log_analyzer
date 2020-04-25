from marshmallow import Schema, fields, pprint


# TODO: add обязательность
class LogSchema(Schema):
    client_id = fields.Str()
    user_agent = fields.Str(data_key="User-Agent")
    location = fields.Str(data_key="document.location")
    referrer = fields.Str(data_key="document.referer")
    date = fields.DateTime()


