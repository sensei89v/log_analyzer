from typing import Iterable, Dict

from src.stat_data import StatItem
from src.log import Log


def build_statistics(data: Iterable[Log],
                     shop_domain: str,
                     finish_url: str,
                     target_domain: str,
                     another_domains: Iterable[str]):
    current_payments: Dict[str, str] = {}      # "user_id" -> "url"
    current_stat: Dict[str, StatItem] = {}     # "url" -> StatItem

    for item in data:
        if not item.check_location_domain(shop_domain):
            continue

        if item.check_referral_domains(another_domains):
            if item.client_id in current_payments:
                del current_payments[item.client_id]
        elif item.check_referral_domains((target_domain, )):
            current_payments[item.client_id] = item.referer
        elif item.is_finish_url(finish_url) and item.client_id in current_payments:
            transition_url = current_payments[item.client_id]

            stat_item = current_stat.get(transition_url)

            if stat_item is None:
                stat_item = StatItem(transition_url)
                current_stat[transition_url] = stat_item

            stat_item.inc_bill_count()
        else:
            # внутренние переходы, или переходы из внешних источников
            pass

    return current_stat.values()
