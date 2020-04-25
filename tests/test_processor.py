import pytest
import json
import os
from datetime import datetime

from src.processor import build_statistics
from src.stat_data import StatItem
from src.log import Log


filenames = []
DATA_DIR = 'tests/data'

for current, dirs, files in os.walk(DATA_DIR):
    filenames += map(lambda x: os.path.join(DATA_DIR, x), files)


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
                        referrer=result_item['referrer'],
                        datetime=datetime.strftime(result_item['datetime'])))

    result = build_statistics(data=logs,
                              shop_domain=input_data['shop_domain'],
                              finish_url=input_data['finish_url'],
                              target_domain=input_data['target_domain'],
                              another_domains=input_data['another_domains'])

    result = sorted(result, key=lambda x: x.url)
    assert result == available

