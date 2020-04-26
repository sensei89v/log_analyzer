import pytest
from src.utils import is_domain_part_of_another


@pytest.mark.parametrize("origianl,checked", [("finish.com", "finish.com"),
                                              ("d.finish.com", "d.finish.com"),
                                              ("finish.com", "a.d.finish.com")])
def test_good_subdomain(origianl, checked):
    assert is_domain_part_of_another(origianl, checked)


@pytest.mark.parametrize("origianl,checked", [("finish.com", "finish.net"),
                                              ("lfinish.com", "finish.com"),
                                              ("a.d.finish.com", "finish.com")])
def test_bad_subdomain(origianl, checked):
    assert not is_domain_part_of_another(origianl, checked)
