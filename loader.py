import abc
import json
import schemas
import log

class Loader:
    def load(self):
        pass


class FileLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def _load(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)
            return data

    def load(self):
        data = self._load()
        schema = schemas.LogSchema()
        result = []

        for item in data:
            value = schema.load(item)
            log_tem = log.Log(client_id=value['client_id'],
                              location=value['location'],
                              referrer=value['referrer'],
                              datetime=value['date'])

            result.append(log_tem)

        return result
