import os
from time import sleep
from typing import Tuple, List

import requests

# Due to some issues with Python and SSL
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'


def generate_year_months_pairs() -> List[Tuple[int, int]]:
    result = []
    for year in range(1950, 2022):
    # for year in range(1999, 2000):
        for month in range(1, 13):
            result.append((year, month))

    return result


def get_absolute_file_name(year: int, month: int, output_folder: str) -> str:
    result = os.path.join(output_folder,
                          "{:d}_{:02d}.rss.xml".format(year, month))
    return result


def download_single_rss(year: int, month: int, output_file: str, sleep_timeout: int) -> None:
    end_year = year
    end_month = month + 1

    # end month is January next year -> update end year too
    if end_month == 13:
        end_year += 1
        end_month = 1

    rss_url = 'https://hudoc.echr.coe.int/app/transform/rss?library=echreng&query=contentsitename:' \
              'ECHR%20AND%20(NOT%20(doctype=PR%20OR%20doctype=HFCOMOLD%20OR%20doctype=HECOMOLD))' \
              '%20AND%20(kpdate%3E=%22' \
              '{:d}-{:02d}-01T00:00:00.0Z' \
              '%22%20AND%20kpdate%3C=%22' \
              '{:d}-{:02d}-01T00:00:00.0Z' \
              '%22)&sort=&start=0&length=1000&rankingModelId=11111111-0000-0000-0000-000000000000'.format(
        year, month, end_year, end_month
    )

    print(rss_url)

    page = requests.get(rss_url, verify=False, timeout=10)
    print(page.content)
    with open(output_file, 'wb') as f:
        f.write(page.content)
        f.flush()
        f.close()

    # parse: FeedParserDict = feedparser.parse(page.content)
    # print(len(parse['entries']))

    print("Sleeping for {} seconds".format(sleep_timeout))
    sleep(sleep_timeout)


if __name__ == '__main__':
    output_folder = '01_downloaded_rss_files'
    sleep_timeout = 5

    for (year, month) in generate_year_months_pairs():
        output_file_name = get_absolute_file_name(year, month, output_folder)

        if not os.path.exists(output_file_name):
            print("File {} does not exist yet, downloading".format(output_file_name))
            download_single_rss(year, month, output_file_name, sleep_timeout)
