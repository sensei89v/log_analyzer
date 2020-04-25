from urllib.parse import urlparse


def _is_part_domain(original_domain, checked_domain):
    return original_domain == checked_domain or original_domain.endswith("." + checked_domain)


class Log:
    def __init__(self, client_id, location, referrer, datetime):
        self.client_id = client_id
        self.location = location
        self.referrer = referrer
        self.datetime = datetime

    def __str__(self):
        return f"client_id: {self.client_id}, location: {self.location}, referrer: {self.referrer}, datetime: {self.datetime}"

    def check_location_domain(self, domain):
        parsed = urlparse(self.location)
        path = parsed.netloc
        return _is_part_domain(path, domain)

    def check_referral_domains(self, domains):
        parsed = urlparse(self.referrer)
        path = parsed.netloc

        for domain_item in domains:
            if _is_part_domain(path, domain_item):
                return True

        return False


    def is_finish_url(self, finish_url):
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
