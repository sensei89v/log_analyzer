import pytest
from datetime import datetime

from src.log import Log


@pytest.mark.parametrize("check_url", ["https://finish.com/finish",
                                       "https://finish.com/finish/",
                                       "http://finish.com/finish",
                                       "http://finish.com/finish/",])
@pytest.mark.parametrize("finish_url", ["https://finish.com/finish",
                                        "https://finish.com/finish/",
                                        "http://finish.com/finish",
                                        "http://finish.com/finish/",])
def test_check_good_finish_url_without_queries(check_url, finish_url):
    log = Log("user_id", finish_url, "https://finish.com/bla-bla", datetime.now())
    assert log.is_finish_url(check_url)


@pytest.mark.parametrize("check_url,finish_url", [("https://finish.com/finish?abc=1", "https://finish.com/finish/?abc=1"),
                                                  ("https://finish.com/finish?abc=1&wed=dsfs", "https://finish.com/finish/?wed=dsfs&abc=1")])
def test_check_good_finish_url_with_queries(check_url, finish_url):
    log = Log("user_id", finish_url, "https://finish.com/bla-bla", datetime.now())
    assert log.is_finish_url(check_url)


@pytest.mark.parametrize("check_url,finish_url", [("https://finish.com/finish?abc=1", "https://finish.com/finish/?abc=2"),
                                                  ("https://d.finish.com/finish?abc=1&wed=dsfs", "https://finish.com/finish/?wed=dsfs&abc=1"),
                                                  ("https://finish.com/finish?abc=1&wed=dsfs", "http://finish.com/finish/p/?wed=dsfs&abc=1"),
                                                  ("https://finish.com/finish?abc=1&wed=dsfs", "https://finish.com/finish"),
                                                  ("https://finish.com/finish?abc=1", "https://finish.com/finish/?cba=1"),])
def test_check_bad_finish_url_without_queries(check_url, finish_url):
    log = Log("user_id", finish_url, "https://finish.com/bla-bla", datetime.now())
    assert not log.is_finish_url(check_url)
