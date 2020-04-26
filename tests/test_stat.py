from src.stat_data import StatItem


def test_stat():
    url = 'http://google.com'

    stat = StatItem(url)
    stat.inc_bill_count()
    stat.inc_bill_count()
    stat.inc_bill_count()
    stat.inc_bill_count()
    stat.inc_bill_count()

    assert stat.url == url
    assert stat.bill_count == 5
