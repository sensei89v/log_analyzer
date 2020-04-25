from marshmallow import Schema, fields


class LogSchema(Schema):
    client_id = fields.Str(required=True)
    user_agent = fields.Str(data_key="User-Agent", required=True)
    location = fields.Str(data_key="document.location", required=True)
    referer = fields.Str(data_key="document.referer", required=True)
    date = fields.DateTime(required=True)
