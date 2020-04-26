import json
import marshmallow

from src.schemas import LogSchema
from src.log import Log


class ReadError(Exception):
    pass


class FileLoader:
    def __init__(self, filename: str, ignore_error: bool):
        self.filename = filename
        self.ignore_error = ignore_error

    def _load(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)
            return data

    def load(self):
        try:
            data = self._load()
        except Exception:
            raise ReadError(f"Cann't read json file {self.filename}")

        schema = LogSchema()
        result = []
        # Todo: добавить проверку что это список объектов
        for item in data:
            try:
                value = schema.load(item)

                log_tem = Log(client_id=value['client_id'],
                              location=value['location'],
                              referer=value['referer'],
                              request_datetime=value['date'])

                result.append(log_tem)
            except marshmallow.exceptions.ValidationError as e:
                if not self.ignore_error:
                    raise e

        return result
