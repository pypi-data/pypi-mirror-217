def exclude_dict_empty_values(dictionary: dict):
    """
    빈 문자열 또는 None 값을 가진 key를 dict에서 제거
    """
    return {k: v for k, v in dictionary.items() if v != "" and v is not None}
