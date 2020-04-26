from marshmallow import Schema, fields, pre_load


class _Temp(Schema):
    referer = fields.Url(required=True)


class LogSchema(Schema):
    client_id = fields.Str(required=True)
    user_agent = fields.Str(data_key="User-Agent", required=True)
    location = fields.Url(data_key="document.location", required=True)  # ключевое поле, должно быть корректым точно
    referer = fields.Str(data_key="document.referer", required=True)    # Важное поле, но в теории допускаем фигню там
    date = fields.DateTime(required=True)

    @pre_load
    def fix_referer(self, item, many, **kwargs):
        if 'document.referer' not in item:
            return item

        value = item['document.referer']
        temp_schema = _Temp()

        try:
            temp_schema.load({'referer': value})
        except Exception:
            item['document.referer'] = ""

        return item
