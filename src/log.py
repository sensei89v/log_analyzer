from typing import Iterable
import datetime
from urllib.parse import urlparse

from src.utils import is_domain_part_of_another


class Log:
    # Todo: add hint fot datetime
    def __init__(self, client_id: str, location: str, referer: str, request_datetime: datetime.datetime):
        self.client_id = client_id
        self.location = location
        self.referer = referer
        self.request_datetime = request_datetime

    def __str__(self):
        return f"client_id: {self.client_id}, location: {self.location}, referer: {self.referer}, datetime: {self.datetime}"

    def check_location_domain(self, domain: str):
        parsed = urlparse(self.location)
        path = parsed.netloc
        return is_domain_part_of_another(domain, path)

    def check_referral_domains(self, domains: Iterable[str]):
        if not self.referer:
            return False

        parsed = urlparse(self.referer)
        path = parsed.netloc

        for domain_item in domains:
            if is_domain_part_of_another(domain_item, path):
                return True

        return False

    def is_finish_url(self, finish_url: str):
        if self.location == finish_url:
            return True

        location_parsed = urlparse(self.location)
        finish_url_parsed = urlparse(finish_url)

        if location_parsed.netloc != finish_url_parsed.netloc:
            return False

        location_path = location_parsed.path
        finish_path = finish_url_parsed.path

        if location_path.endswith("/"):
            location_path = location_path[:-1]

        if finish_path.endswith("/"):
            finish_path = finish_path[:-1]

        if finish_path != location_path:
            return False

        location_query = sorted(location_parsed.query.split('&'))
        finish_query = sorted(finish_url_parsed.query.split('&'))

        return location_query == finish_query
