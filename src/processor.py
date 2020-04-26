from typing import Iterable, Dict, List

from src.stat_data import StatItem
from src.log import Log
from src.utils import is_domain_part_of_another


INCORRECT_SORTED_ERROR = "Incorrect sorted input data"
INCORRECT_SHOP_DOMAIN_ERROR = "Incorrect shop domain"
INCORRECT_FINISH_URL_ERROR = "Incorrect finish url"
INCORRECT_TARGET_DOMAIN_ERROR = "Incorrect target domain"
INCORRECT_ANOTHER_DOMAIN_ERROR = "Incorrect another domain"
MIX_TARGET_AND_ANOTHER_DOMAINS_ERROR = "Mix target and another domains"
MIX_TARGET_AND_SHOP_DOMAINS_ERROR = "Mix target and shop domains"
MIX_ANOTHER_AND_SHOP_DOMAINS_ERROR = "Mix another and shop domains"


def build_statistics(data: Iterable[Log],
                     shop_domain: str,
                     finish_url: str,
                     target_domain: str,
                     another_domains: List[str]):
    # check input data to algorithm
    if not shop_domain:
        raise ValueError(INCORRECT_SHOP_DOMAIN_ERROR)

    if not finish_url:
        raise ValueError(INCORRECT_FINISH_URL_ERROR)

    if not target_domain:
        raise ValueError(INCORRECT_TARGET_DOMAIN_ERROR)

    if is_domain_part_of_another(target_domain, shop_domain) or is_domain_part_of_another(shop_domain, target_domain):
        raise ValueError(MIX_TARGET_AND_SHOP_DOMAINS_ERROR)

    for another_item in another_domains:
        if not another_item:
            raise ValueError(INCORRECT_ANOTHER_DOMAIN_ERROR)

        if is_domain_part_of_another(target_domain, another_item) or is_domain_part_of_another(another_item, target_domain):
            raise ValueError(MIX_TARGET_AND_ANOTHER_DOMAINS_ERROR)

        if is_domain_part_of_another(shop_domain, another_item) or is_domain_part_of_another(another_item, shop_domain):
            raise ValueError(MIX_ANOTHER_AND_SHOP_DOMAINS_ERROR)

    # start algorithm
    current_datetime = None
    current_payments: Dict[str, str] = {}      # "user_id" -> "url"
    current_stat: Dict[str, StatItem] = {}     # "url" -> StatItem

    for item in data:
        # verify input data
        if current_datetime is not None:
            if current_datetime > item.request_datetime:
                raise ValueError(INCORRECT_SORTED_ERROR)

        current_datetime = item.request_datetime

        # Check domain
        if not item.check_location_domain(shop_domain):
            continue

        # try analyze item
        if item.check_referral_domains(another_domains):
            # Transmition from competitors
            if item.client_id in current_payments:
                del current_payments[item.client_id]
        elif item.check_referral_domains((target_domain, )):
            # Transmition from our server
            current_payments[item.client_id] = item.referer
        elif item.is_finish_url(finish_url):
            # PURCHASE!!!!!
            if item.client_id in current_payments:
                # Transmition from our server
                transition_url = current_payments[item.client_id]
                stat_item = current_stat.get(transition_url)

                if stat_item is None:
                    stat_item = StatItem(transition_url)
                    current_stat[transition_url] = stat_item

                stat_item.inc_bill_count()
            else:
                # Transmition from not our server
                pass
        else:
            # internal or correct external transmits
            pass

    return current_stat.values()
