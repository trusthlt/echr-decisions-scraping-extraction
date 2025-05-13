import os
import re
from typing import List, Set

import feedparser
from feedparser import FeedParserDict

if __name__ == '__main__':
    input_folder = '01_downloaded_rss_files'
    output_folder = '02_extracted_case_ids'
    output_file = 'case_ids_sorted.txt'

    # list files
    rss_files: List[str] = os.listdir(input_folder)
    print(rss_files)

    # collect all case IDs in a set
    all_case_ids: Set[str] = set()

    for rss_file in rss_files:
        parse: FeedParserDict = feedparser.parse(os.path.join(input_folder, rss_file))
        for entry in parse['entries']:
            case_link = entry['link']
            # Extract only the item id from from following line
            # http://hudoc.echr.coe.int/eng#{"itemid":["001-27878"]}
            case_id: List[str] = re.findall(r'\d+-\d+', case_link)

            all_case_ids.update(case_id)

    # convert to a sorted list
    all_case_ids_sorted_list: List[str] = sorted(all_case_ids)

    # save as txt - one item per line
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, output_file), 'wt') as f:
        f.writelines('\n'.join(all_case_ids_sorted_list))

    print("{} case IDs saved to {}".format(
        len(all_case_ids_sorted_list),
        os.path.join(output_folder, output_file))
    )
