from stat_data import StatItem


def build_statistics(data, shop_domain, finish_url, target_domain, another_domains):
    current_payments = {} # "user_id" -> "url"
    current_stat = {} # "url" -> StatItem

    import pdb
    pdb.set_trace()

    for item in data:
        if not item.check_location_domain(shop_domain):
            pass

        if item.check_referral_domains(another_domains):
            if item.client_id in current_payments:
                del current_payments[item.client_id]
        elif item.check_referral_domains((target_domain, )):
            current_payments[item.client_id] = item.referrer
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