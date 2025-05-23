# ECHR decisions - scraping and extraction

This project contains a set of scripts to scrape decisions of the ECHR in html and to extract semi-structured text in xml for downstream applications. An additional script can be used for converting these xml files to UIMA xmi for annotation in Inception and similar tools.

This project was used in our paper entitled "Mining legal arguments in court decisions" ( https://link.springer.com/article/10.1007/s10506-023-09361-y ), so please cite that paper if you use this project.


## Data and processing pipeline

We scraped all decisions between 1950 and the end of 2022.

`01_downloaded_rss_files`

* ECHR (HUDOC) publishes RSS files which makes further scraping more convenient
* We extract decisions IDs from the RSS files
* Generated by `01_all_years_months_rss_scraper.py`

`02_extracted_case_ids`

* All ECHR document IDs that were found in the HUDOC database through RSS as simple txt file
* Generated by `02_extract_case_ids_from_rss.py`

`03_all_cases_html` (compressed to `.tar.gz`, decompress by `$ cat 03_all_cases_html.tar.gz.* | tar xzvf -` which re-creates the folder `03_all_cases_html`)

* 172,770 court decisions as raw html scraped from HUDOC, each html document has its corresponding json metadata
* The files are spread across 100 folders starting with last two first digits of its ID for convenience manipulating with over 300k files in total
* Generated by `03_dowload_all_cases_html.py`, takes a lot of time as it scrapes from the HUDOC website with a pause between requests

`04_structured_cases`  (compressed to `.tar.gz`, decompress by `$ cat 04_structured_cases.tar.gz.* | tar xzvf -` which re-creates the folder `04_structured_cases`)

* Raw html files converted to a simple xml in UTF-8
* Split to paragraphs `<p>` corresponding to paragraphs in the original html files
* Each paragraph contains one or several spans `<span text="..."/>` where the text attribute contains the extracted text
* Converting this xml to a plain-text form can be done simply by concatenating the `text` attribute of each `span` for each paragraph `p`, no additional whitespaces are necessary (these are preserved in the `text` attribute); an implementation can be found on line 16 in `05_convert_structured_case_to_xmi_with_spacy.py` (function `def xml_to_plain_text(input_xml_file)`)
* Generated by `04_convert_html_to_structured_cases.py`
* In total 137,716 non-empty xml files (172,572 files in total minus 34,856 empty files which weren't parsed and were somehow malformed html; this is still possible to fix in the html extraction code)

(note: compressed as
$ tar cvzf - 03_all_cases_html/ | split --bytes=95MB - 03_all_cases_html.tar.gz.
due to GitHub limit 100 MB per file max )