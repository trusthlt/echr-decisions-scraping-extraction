import os
import re
import time
from typing import List

import requests

# Due to some issues with Python and SSL
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

if __name__ == '__main__':
    sleep_timeout_sec = 4

    input_file = '02_extracted_case_ids/case_ids_sorted.txt'
    output_main_folder = '03_all_cases_html'

    # This is a manually created text file with HUDOC case ID per line to be
    # downloaded first
    input_file_priority_download = '02_extracted_case_ids/case_ids_priority_download.txt'

    # read all ids
    all_case_ids: List[str] = []

    with open(input_file_priority_download, 'rt') as f:
        all_case_ids.extend([_.strip() for _ in f.readlines()])

    with open(input_file, 'rt') as f:
        all_case_ids.extend([_.strip() for _ in f.readlines()])

    session = requests.Session()

    for case_id in all_case_ids:
        # get output file name
        # last two digits from the file name will be used as sub-folder name
        try:
            folder_name: str = re.findall(r'(\d{2})$', case_id)[0]
        except IndexError as e:
            # there are few exceptions with only a single digit, e.g. '001-4'
            # -> prepend zero
            folder_name: str = '0' + re.findall(r'(\d)$', case_id)[0]

        output_folder: str = os.path.join(output_main_folder, folder_name)
        os.makedirs(output_folder, exist_ok=True)

        # file name is just the case ID
        output_file_name_html = os.path.join(output_folder, "{}.html".format(case_id))
        print(output_file_name_html)

        # fetch if not done yet
        if not os.path.exists(output_file_name_html):
            # After exploring the javascript, here's the entry point for HTML fragment with the actual content
            html_url = 'https://hudoc.echr.coe.int/app/conversion/docx/html/body?library=ECHR&id={}'.format(case_id)

            page = session.get(html_url, verify=False, timeout=30)
            print(page.content)
            with open(output_file_name_html, 'wb') as f:
                f.write(page.content)
                f.flush()

            print("Sleeping for {} seconds".format(sleep_timeout_sec))
            time.sleep(sleep_timeout_sec)

        # file name is just the case ID
        output_file_name_json = os.path.join(output_folder, "{}.json".format(case_id))
        print(output_file_name_json)

        # fetch if not done yet
        if not os.path.exists(output_file_name_json):
            # After exploring the javascript, here's the entry point for nice JSON response
            json_url = 'https://hudoc.echr.coe.int/app/query/results?query=' \
                       '(contentsitename=ECHR) AND {}&select=itemid,applicability,appno,' \
                       'article,conclusion,decisiondate,docname,documentcollectionid,documentcollectionid2,' \
                       'doctype,externalsources,importance,introductiondate,issue,judgementdate,kpthesaurus,' \
                       'meetingnumber,originatingbody,publishedby,referencedate,kpdate,advopidentifier,' \
                       'advopstatus,reportdate,representedby,resolutiondate,resolutionnumber,respondent,' \
                       'rulesofcourt,separateopinion,scl,typedescription,ecli,casecitation&sort=' \
                       '&start=0&length=1'.format(case_id)

            json_page = session.get(json_url, verify=False, timeout=30)
            print(json_page.content)
            with open(output_file_name_json, 'wb') as f:
                f.write(json_page.content)
                f.flush()

            print("Sleeping for {} seconds".format(sleep_timeout_sec))
            time.sleep(sleep_timeout_sec)
