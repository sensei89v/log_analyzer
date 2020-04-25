import pytest
from datetime import datetime

from src.log import Log

###################   Check finish url
@pytest.mark.parametrize("location_url", ["https://finish.com/finish",
                                          "https://finish.com/finish/",
                                          "http://finish.com/finish",
                                          "http://finish.com/finish/",])
@pytest.mark.parametrize("finish_url", ["https://finish.com/finish",
                                        "https://finish.com/finish/",
                                        "http://finish.com/finish",
                                        "http://finish.com/finish/",])
def test_check_good_finish_url_without_queries(location_url, finish_url):
    log = Log("user_id", location_url, "https://sth.com/bla-bla", datetime.now())
    assert log.is_finish_url(finish_url)


@pytest.mark.parametrize("location_url,finish_url", [("https://finish.com/finish?abc=1", "https://finish.com/finish/?abc=1"),
                                                     ("https://finish.com/finish?abc=1&wed=dsfs", "https://finish.com/finish/?wed=dsfs&abc=1")])
def test_check_good_finish_url_with_queries(location_url, finish_url):
    log = Log("user_id", location_url, "https://sth.com/bla-bla", datetime.now())
    assert log.is_finish_url(finish_url)


@pytest.mark.parametrize("location_url,finish_url", [("https://finish.com/finish?abc=1", "https://finish.com/finish/?abc=2"),
                                                     ("https://d.finish.com/finish?abc=1&wed=dsfs", "https://finish.com/finish/?wed=dsfs&abc=1"),
                                                     ("https://finish.com/finish?abc=1&wed=dsfs", "http://finish.com/finish/p/?wed=dsfs&abc=1"),
                                                     ("https://finish.com/finish?abc=1&wed=dsfs", "https://finish.com/finish"),
                                                     ("https://finish.com/finish?abc=1", "https://finish.com/finish/?cba=1"),])
def test_check_bad_finish_url_without_queries(location_url, finish_url):
    log = Log("user_id", location_url, "https://sth.com/bla-bla", datetime.now())
    assert not log.is_finish_url(finish_url)


###################   Check location domain
@pytest.mark.parametrize("location_url,domain", [("https://finish.com/finish?abc=1", "finish.com"),
                                                 ("https://d.finish.com/finish?abc=1&wed=dsfs", "d.finish.com"),
                                                 ("https://a.d.finish.com/finish?abc=1&wed=dsfs", "finish.com")])
def test_good_check_location_domain(location_url, domain):
    log = Log("user_id", location_url, "https://sth.com/bla-bla", datetime.now())
    assert log.check_location_domain(domain)


@pytest.mark.parametrize("location_url,domain", [("https://finish.com/finish?abc=1", "finish.dot"),
                                                 ("https://finish.com/finish?abc=1", "ish.dot"),
                                                 ("https://d.finish.com/finish?abc=1&wed=dsfs", "b.finish.com"),
                                                 ("https://d.finish.com/finish?abc=1&wed=dsfs", "a.d.finish.com"),
                                                 ("https://a.d.finish.com/finish?abc=1&wed=dsfs", "a.b.finish.com"),
                                                 ("https://a.d.finish.com/finish?abc=1&wed=dsfs", "")])
def test_bad_check_location_domain(location_url, domain):
    log = Log("user_id", location_url, "https://sth.com/bla-bla", datetime.now())
    assert not log.check_location_domain(domain)


###################   Check referral domain
@pytest.mark.parametrize("referral_url,domains", [("https://finish.com/finish?abc=1", ["finish.com"]),
                                                  ("https://finish.com/finish?abc=1", ["a.com", "finish.com"]),
                                                  ("https://d.finish.com/finish?abc=1&wed=dsfs", ["a.com", "finish.com"]),
                                                  ("https://a.d.finish.com/finish?abc=1&wed=dsfs", ["b.d.finish.com", "d.finish.com"])])
def test_good_check_referral_domains(referral_url, domains):
    log = Log("user_id", "https://sth.com/bla-bla", referral_url, datetime.now())
    assert log.check_referral_domains(domains)


@pytest.mark.parametrize("referral_url,domains", [("https://finish.com/finish?abc=1", ["a.com", "b.com"]),
                                                  ("https://finish.com/finish?abc=1", ["ish.com", "finish.a.com"]),
                                                  ("https://d.finish.com/finish?abc=1&wed=dsfs", ["a.d.finish.com", "b.d.finish.com"]),
                                                  ("https://a.d.finish.com/finish?abc=1&wed=dsfs", ["b.d.finish.com", "a.e.finish.com"])])
def test_bad_check_referral_domains(referral_url, domains):
    log = Log("user_id", "https://sth.com/bla-bla", referral_url, datetime.now())
    assert not log.check_referral_domains(domains)
