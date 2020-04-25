
class StatItem:
    def __init__(self, url: str):
        self.url = url
        self.bill_count = 0

    def inc_bill_count(self):
        self.bill_count += 1

    def __str__(self):
        return f"url: {self.url}, bill_count: {self.bill_count}"

    def __eq__(self, another):
        # Need to test
        return self.url == another.url and self.bill_count == another.bill_count
