from urllib.parse import urlparse


def _is_part_domain(original_domain, checked_domain):
    return original_domain == checked_domain or original_domain.endswith("." + checked_domain)

class Log:
    def __init__(self, client_id, location, referrer, datetime):
        self.client_id = client_id
        self.location = location
        self.referrer = referrer
        self.datetime = datetime

    # datetime =
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
        return self.location == finish_url
        # TODO: сделать схемонезависимой штукой
