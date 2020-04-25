import json

from src.schemas import LogSchema
from src.log import Log


class FileLoader:
    def __init__(self, filename: str):
        self.filename = filename

    def _load(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)
            return data

    def load(self):
        data = self._load()
        schema = LogSchema()
        result = []

        for item in data:
            value = schema.load(item)
            log_tem = Log(client_id=value['client_id'],
                          location=value['location'],
                          referrer=value['referrer'],
                          datetime=value['date'])

            result.append(log_tem)

        return result
