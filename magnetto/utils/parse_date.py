import re


def parse_date(str):
    time_str = re.findall(r'\d{1,2}:\d{2}', str)[0]
    date_str = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}', str)[0]

    datetime_str = "{} {}".format(date_str, time_str)

    unix = time.strptime(datetime_str, "%d.%m.%Y %H:%M")

    # переводим в timestamp
    # TODO: посмотреть позже
    return repr(int(float(time.mktime(unix))))
