def is_domain_part_of_another(original_domain: str, checked_domain: str):
    """
    Функция проверяет равен ли original_domain checked_domain или original_domain является его частью
    """
    return original_domain == checked_domain or checked_domain.endswith("." + original_domain)
