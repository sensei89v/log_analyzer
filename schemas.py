from marshmallow import Schema, fields, pprint

#schema = AlbumSchema()
#result = schema.dump(album)


#    "client_id": "user7",
#    "User-Agent": "Chrome 65",
#    "document.location": "https://shop.com/products/id?=25",
#    "document.referer": "https://shop.com/products/id?=10",
#    "date": "2018-05-23T19:04:20.119000Z"

class LogSchema(Schema):
    client_id = fields.Str()
    user_agent = fields.Str(data_key="User-Agent")
    location = fields.Str(data_key="document.location")
    referrer = fields.Str(data_key="document.referer")
    date = fields.DateTime()


#class Item:
#    def __init__(self):

