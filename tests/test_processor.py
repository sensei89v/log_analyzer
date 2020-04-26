import pytest
import json
import os
from datetime import datetime

from src.processor import build_statistics, INCORRECT_SORTED_ERROR, INCORRECT_SHOP_DOMAIN_ERROR, INCORRECT_FINISH_URL_ERROR, \
    INCORRECT_TARGET_DOMAIN_ERROR, INCORRECT_ANOTHER_DOMAIN_ERROR, MIX_TARGET_AND_ANOTHER_DOMAINS_ERROR, MIX_TARGET_AND_SHOP_DOMAINS_ERROR, \
    MIX_ANOTHER_AND_SHOP_DOMAINS_ERROR


from src.stat_data import StatItem
from src.log import Log


filenames = []
DATA_DIR = './tests/data'


for current, dirs, files in os.walk(DATA_DIR):
    filenames += map(lambda x: os.path.join(DATA_DIR, x), files)
    break

filenames = sorted(filenames)


@pytest.mark.parametrize("filename", filenames)
def test_processor(filename):
    input_data = {}

    with open(filename) as json_file:
        input_data = json.load(json_file)

    # build available
    available = []

    for result_item in input_data['result']:
        item = StatItem(result_item['url'])
        item.bill_count = result_item['count']
        available.append(item)

    available = sorted(available, key=lambda x: x.url)

    # build input data
    logs = []

    for result_item in input_data['logs']:
        logs.append(Log(client_id=result_item['client_id'],
                        location=result_item['location'],
                        referer=result_item['referer'],
                        request_datetime=datetime.strptime(result_item['datetime'], '%Y-%m-%dT%H:%M:%S.%f')))

    result = build_statistics(data=logs,
                              shop_domain=input_data['shop_domain'],
                              finish_url=input_data['finish_url'],
                              target_domain=input_data['target_domain'],
                              another_domains=input_data['another_domains'])

    result = sorted(result, key=lambda x: x.url)
    assert result == available

def test_incorrect_sorted_data():
    logs = [
        Log(client_id="user1", location="http://shop.ru", referer="http://shop.ru", request_datetime=datetime(2018, 1, 2, 20, 3, 4)),
        Log(client_id="user1", location="http://shop.ru", referer="http://shop.ru", request_datetime=datetime(2018, 1, 1, 20, 3, 4))
    ]

    with pytest.raises(ValueError, match=INCORRECT_SORTED_ERROR) as excinfo:
        build_statistics(data=logs,
                         shop_domain="shop.ru",
                         finish_url="http://shop.ru/checkout",
                         target_domain="our.com",
                         another_domains=[])


def test_incorrect_target_shop():
    with pytest.raises(ValueError, match=INCORRECT_SHOP_DOMAIN_ERROR) as excinfo:
        build_statistics(data=[],
                         shop_domain="",
                         finish_url="http://shop.ru/checkout",
                         target_domain="our.com",
                         another_domains=[])


def test_incorrect_finish_url():
    with pytest.raises(ValueError, match=INCORRECT_FINISH_URL_ERROR) as excinfo:
        build_statistics(data=[],
                         shop_domain="shop.ru",
                         finish_url="",
                         target_domain="our.com",
                         another_domains=[])


def test_incorrect_target_domain():
    with pytest.raises(ValueError, match=INCORRECT_TARGET_DOMAIN_ERROR) as excinfo:
        build_statistics(data=[],
                         shop_domain="shop.ru",
                         finish_url="http://shop.ru/checkout",
                         target_domain="",
                         another_domains=[])


def test_incorrect_another_domain():
    with pytest.raises(ValueError, match=INCORRECT_ANOTHER_DOMAIN_ERROR) as excinfo:
        build_statistics(data=[],
                         shop_domain="shop.ru",
                         finish_url="http://shop.ru/checkout",
                         target_domain="our.com",
                         another_domains=["their1.com", ""])


@pytest.mark.parametrize("target,another", [("data.com", ["their1.com", "data.com", "their2.com"]),
                                            ("a.data.com", ["their1.com", "data.com", "their2.com"]),
                                            ("data.com", ["their1.com", "a.data.com", "their2.com"])])
def test_incorrect_mix_target_and_another_domains(target, another):
    with pytest.raises(ValueError, match=MIX_TARGET_AND_ANOTHER_DOMAINS_ERROR) as excinfo:
        build_statistics(data=[],
                         shop_domain="shop.ru",
                         finish_url="http://shop.ru/checkout",
                         target_domain=target,
                         another_domains=another)


@pytest.mark.parametrize("shop,target", [("data.com", "data.com"),
                                         ("a.data.com", "data.com"),
                                         ("data.com", "a.data.com")])
def test_incorrect_mix_shop_and_target_domains(shop, target):
    with pytest.raises(ValueError, match=MIX_TARGET_AND_SHOP_DOMAINS_ERROR) as excinfo:
        build_statistics(data=[],
                         shop_domain=shop,
                         finish_url="http://shop.ru/checkout",
                         target_domain=target,
                         another_domains=["their1.com", ""])


@pytest.mark.parametrize("shop,another", [("data.com", ["their1.com", "data.com", "their2.com"]),
                                          ("a.data.com", ["their1.com", "data.com", "their2.com"]),
                                          ("data.com", ["their1.com", "a.data.com", "their2.com"])])
def test_incorrect_mix_shop_and_another_domains(shop, another):
    with pytest.raises(ValueError, match=MIX_ANOTHER_AND_SHOP_DOMAINS_ERROR) as excinfo:
        build_statistics(data=[],
                         shop_domain=shop,
                         finish_url="http://shop.ru/checkout",
                         target_domain="our.com",
                         another_domains=another)
