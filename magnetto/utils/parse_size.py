import re


def parse_size(str):
    raw_str = re.findall(r'\d+', str)[0]
    raw_int = int(raw_str)
    # 0 это плохо
    # if not raw_int:
    #     raise MagnettoParseError(
    #         "Invalid parse size. DEBUG: raw_str(\"{}\")".format(raw_str))
    size_mb = 0
    if "ГБ" in str or "GB" in str:
        size_mb = raw_int * 1024
    elif "МБ" in str or "MB" in str:
        size_mb = raw_int
    # байты
    else:
        size_mb = raw_int / 1024 / 1024

    return size_mb
