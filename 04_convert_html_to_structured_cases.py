import os
import re
import sys
from pathlib import Path
from typing import List, Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import bs4
from bs4 import BeautifulSoup, Tag


def convert_single_file(single_html_file: str, single_json_file: str, output_xml_file: str) -> None:
    # if Path(output_xml_file).exists():
    #     raise FileExistsError("File {:s} exists already".format(output_xml_file))

    with open(single_html_file, 'rt', encoding='utf-8') as f:
        bs: BeautifulSoup = BeautifulSoup(f, features='html.parser')

    # root_children = [e.name for e in bs.children if e.name is not None]
    # print(root_children)

    # remove the first "style" element
    try:
        bs.find('style').decompose()
    except AttributeError as er:
        # ignore
        pass

    # all simple paragraphs
    for _ in bs.findAll('p', {'class': 's30EEC3F8'}):
        _.attrs.__delitem__('class')

    # all simple spans
    for _ in bs.findAll('span', {'class': 'sB8D990E2'}):
        _.attrs.__delitem__('class')

    # Section headings
    for _ in bs.findAll('p', {'class': 's30CCF494'}):
        _.attrs.update({'class': 'section_heading'})

    # Dissent headings
    for _ in bs.findAll('p', {'class': 'sC8420256'}):
        _.attrs.update({'class': 'dissent_section_heading'})

    # Header paragraphs
    for _ in bs.findAll('p', {'class': 's32B251D'}):
        _.attrs.update({'class': 'header_paragraph'})

    # Header paragraph starting with letters
    for _ in bs.findAll('p', {'class': 'sD5B7D322'}):
        _.attrs.update({'class': 'header_letters'})

    # Header paragraph starting with roman numbers
    for _ in bs.findAll('p', {'class': 's1BD70772'}):
        _.attrs.update({'class': 'header_roman_numbers'})

    # Header paragraph starting with arabic number
    for _ in bs.findAll('p', {'class': 'sCC3BCF28'}):
        _.attrs.update({'class': 'header_arabic_numbers'})

    # Very rare paragraph
    for _ in bs.findAll('p', {'class': 'sB9059D72'}):
        _.attrs.update({'class': 'rare_paragraph'})

    # a name="..." is very interesting... See output of
    # $ grep -r -o -h -E '<a name=\"(\w+)' | sort | uniq -c | sort -n

    # Maybe the "LAW" references?
    for _ in bs.findAll('p', {'class': 's19630BCC'}):
        _.attrs.update({'class': 'some_existing_article'})

    # Quoted paragraphs (only one type)
    for _ in bs.findAll('p', {'class': 's9E9B0CD7'}):
        _.attrs.update({'class': 'some_quoted_text_level1'})

    # Quoted paragraphs (mostly as sub-text of the above)
    for _ in bs.findAll('p', {'class': 's395BF5DF'}):
        _.attrs.update({'class': 'some_quoted_text_level2'})

    # Final judgment level 1
    for _ in bs.findAll('p', {'class': 's52B9FB1C'}):
        _.attrs.update({'class': 'judgment_level1'})

    # Final judgment level
    for _ in bs.findAll('p', {'class': 's6C21291F'}):
        _.attrs.update({'class': 'judgment_level2'})

    # Seems like all quoted spans
    for _ in bs.findAll('span', {'class': 'sFBBFEE58'}):
        _.attrs.update({'class': 'quoted_span'})

    # Typically reference to some articles (maybe quoted?)
    for _ in bs.findAll('span', {'class': 'sDFC50A6A'}):
        _.attrs.update({'class': 'span_article_reference'})

    # This is a mixed one
    for _ in bs.findAll('span', {'class': 's6B621B36'}):
        _.attrs.update({'class': 'span_previous_case_name_or_entities_or_others'})

    # Only line breaks
    for _ in bs.findAll('br', {'class': 'sDCD70A49'}):
        _.attrs.update({'class': 'line_break'})

    # Rare empty span
    for _ in bs.findAll('span', {'class': 's50CFE236'}):
        _.attrs.update({'class': 'rare_empty_span'})

    # These look like headers starting with a letter
    for _ in bs.findAll('span', {'class': 's7D2086B4'}):
        _.attrs.update({'class': 'header_span_mostly_letters'})

    # Perhaps final or non-final judgment
    for _ in bs.findAll('p', {'class': 's746C8714'}):
        _.attrs.update({'class': 'paragraph_final_judgment_or_not'})

    # Perhaps final or non-final judgment (span)
    for _ in bs.findAll('span', {'class': 's2359E37B'}):
        _.attrs.update({'class': 'span_final_judgment_or_not'})

    # These are most likely only judges
    for _ in bs.findAll('p', {'class': 's6E50BD9A'}):
        _.attrs.update({'class': 'paragraph_judges'})

    # Some empty spans
    for _ in bs.findAll('span', {'class': 's783FD90F'}):
        _.attrs.update({'class': 'empty_span'})

    # Perhaps the first judge
    for _ in bs.findAll('span', {'class': 's251D1A53'}):
        _.attrs.update({'class': 'judge_span_signature'})

    # All judges signed
    for _ in bs.findAll('p', {'class': 's63F375A7'}):
        _.attrs.update({'class': 'judge_signature'})

    # Some headers reg. dissent and when done
    for _ in bs.findAll('p', {'class': 'sFA83D483'}):
        _.attrs.update({'class': 'when_done_and_is_there_dissent'})

    # G.R. and S.C.P
    for _ in bs.findAll('p', {'class': 'sF61DD143'}):
        _.attrs.update({'class': 'gr_or_scp'})

    # Entities at hearing
    for _ in bs.findAll('span', {'class': 's547CEB99'}):
        _.attrs.update({'class': 'span_entity_appeared_before_court'})

    # Entities at hearing
    for _ in bs.findAll('p', {'class': 's5B69B037'}):
        _.attrs.update({'class': 'paragraph_entity_appeared_before_court'})

    # This one is rare but looks like a normal text span, is mixed with others
    # has only font-weight:normal
    # .sF8BFA2BC { font-family:Arial; font-size:12pt; font-weight:normal }
    # .sB8D990E2 { font-family:Arial; font-size:12pt }
    for _ in bs.findAll('span', {'class': 'sF8BFA2BC'}):
        _.attrs.__delitem__('class')

    # Quoted letters or cases
    for _ in bs.findAll('span', {'class': 's1A844BC0'}):
        _.attrs.update({'class': 'quoted_letter_or_case_or_similar'})

    # This started with "There the Court made clear that"
    for _ in bs.findAll('p', {'class': 'sFD185AC1'}):
        _.attrs.update({'class': 'there_the_court_made_clear_that'})

    # This started with "There the Court made clear that"
    for _ in bs.findAll('p', {'class': 's936379BD'}):
        _.attrs.update({'class': 'dissent_header'})

    # This is only a simple quote character inside
    for _ in bs.findAll('span', {'class': 's3AEEAB2'}):
        _.attrs.update({'class': 'span_quote_character'})

    # Any section heading spans
    for _ in bs.findAll('span', {'class': 's32A37344'}):
        _.attrs.update({'class': 'any_section_heading_span'})

    # change links <a> to simple spans too, they seem to have no functionality
    for _ in bs.findAll('a'):
        _.name = 'span'

    # now iterate over all paragraphs (without class) and all spans and connect them
    # collect all paragraphs from all divs
    all_paragraph_tags: List[Tag] = bs.select("p")

    # We'll be copying output to XML
    output_body: Element = ElementTree.Element('body')

    # filter out empty paragraph tags (that happens very rarely)
    all_paragraph_tags_non_empty = [p for p in all_paragraph_tags if len(p) > 0]

    for p in all_paragraph_tags_non_empty:
        assert isinstance(p, bs4.element.Tag)
        # collect consecutive sub-elements of the same class
        sub_elements_by_same_class: List[List[Tag]] = []

        # current list of sub-elements of the same class for collecting
        current_list: List[Tag] = []

        children_list: List[Tag] = [_ for _ in p.children]

        for child in children_list:
            previous_child: Optional[Tag] = None
            if current_list:
                previous_child: Tag = current_list[-1]

            if previous_child:
                # compare element type and attribute
                if previous_child.name == child.name and \
                        previous_child.attrs.get('class', None) == child.attrs.get('class', None):
                    current_list.append(child)
                # or if the current span is just a white space
                elif re.match(r'^\s+$', child.text):
                    # raise Exception(len(child.text))
                    current_list.append(child)
                else:
                    # mismatch: close current list, append, and open a new one
                    sub_elements_by_same_class.append(current_list)
                    current_list: List[Tag] = [child]
            else:
                current_list.append(child)

        # make sure to add the "last" open current list
        sub_elements_by_same_class.append(current_list)

        output_p = ElementTree.SubElement(output_body, 'p')
        # copy class; not: it can be a string or a list (thanks BS4)
        if p.attrs and 'class' in p.attrs:
            if isinstance(p.attrs['class'], str):
                output_p.attrib['class'] = p.attrs['class']
            elif isinstance(p.attrs['class'], list):
                output_p.attrib['class'] = p.attrs['class'][0]

        # now collapse list of spans into one
        for list_of_same_elements in sub_elements_by_same_class:
            collapsed_text: str = ''.join([_.text for _ in list_of_same_elements])

            # sanitize HTML nbsp parsed as '\xa0' and replace by a simple space
            nbsp_character = u'\xa0'
            clean_text = collapsed_text.replace(nbsp_character, ' ')
            # collapse multiple whitespaces into one
            clean_text = re.sub(' +', ' ', clean_text)

            group_tag: str = list_of_same_elements[0].name
            group_class: Optional[str] = list_of_same_elements[0].get('class', None)

            # copy to the output XML element
            output_element = ElementTree.SubElement(output_p, group_tag)
            output_element.text = clean_text
            if group_class:
                output_element.attrib['class'] = group_class

        # print("+ ******")
        # print('input_p', p)
        # print(type(output_p))
        # print(ElementTree.dump(output_p))
        # print("- ******")

    # print(ElementTree.dump(output_body))
    # exit(0)
    # so far looks good

    output_without_br: Element = ElementTree.Element('body')
    # Linearize line breaks <br> by two paragraphs
    for paragraph_element in output_body:
        assert paragraph_element.tag == 'p'
        # make a copy
        p = ElementTree.SubElement(output_without_br, 'p', paragraph_element.attrib)

        for span in paragraph_element:
            # paragraphs should only contain <br> or <span>
            # but rarely there is <img>, as in HUDOC ID '001-58586'
            if span.tag == 'br' or span.tag == 'span':
                # print(span.tag)
                assert isinstance(span, Element)

                # opy only non-empty spans
                if span.tag == 'span' and len(span.text) > 0:
                    span_copy = ElementTree.SubElement(p, 'span', span.attrib)
                    # copy text now as an attribute
                    span_copy.attrib['text'] = span.text
                else:  # it's <br>, start a new paragraph
                    p = ElementTree.SubElement(output_without_br, 'p', paragraph_element.attrib)

    # print("---")
    # print(ElementTree.dump(output_without_br))

    # and remove paragraphs that have only white spaces
    paragraphs_to_delete: List[Element] = []
    for paragraph in output_without_br:
        assert isinstance(paragraph, Element)
        sub_spans: List[Element] = [_ for _ in paragraph]
        if len(sub_spans) == 1 and len(sub_spans[0].attrib.get('text', '').strip()) == 0:
            paragraphs_to_delete.append(paragraph)
        elif len(sub_spans) == 0:  # or completely empty paragraphs
            paragraphs_to_delete.append(paragraph)

    for paragraph_to_delete in paragraphs_to_delete:
        output_without_br.remove(paragraph_to_delete)

    # print("---")
    # print(ElementTree.dump(output_without_br))

    # save to XML
    with open(output_xml_file, 'wb') as f:
        ElementTree.ElementTree(output_without_br).write(f, encoding='utf-8', xml_declaration=True)


def convert_selected_files(list_of_files):
    for i in list_of_files:
        try:
            convert_single_file('03_all_cases_html/{}/{}.html'.format(i[-2:], i),
                                '03_all_cases_html/{}/{}.json'.format(i[-2:], i),
                                '05_structured_cases/{}.xml'.format(i))
        except Exception as e:
            print("Parsing failed on {:s}".format(i), file=sys.stderr)
            raise e



if __name__ == '__main__test_one_file':
    i = '001-152647'
    convert_single_file('03_all_cases_html/{}/{}.html'.format(i[-2:], i),
                        '03_all_cases_html/{}/{}.json'.format(i[-2:], i),
                        '04_structured_cases/{}.xml'.format(i))

if __name__ == '__main__':
    folder = '03_all_cases_html'
    for sub_folder in [f.path for f in os.scandir(folder) if f.is_dir()]:
        for single_html_file in [f for f in os.scandir(sub_folder) if f.name.endswith('.html')]:
            doc_id: str = Path(single_html_file).stem

            try:
                convert_single_file('03_all_cases_html/{}/{}.html'.format(doc_id[-2:], doc_id),
                                    '03_all_cases_html/{}/{}.json'.format(doc_id[-2:], doc_id),
                                    '04_structured_cases/{}.xml'.format(doc_id))
            except (AttributeError, IOError) as ex:
                print(single_html_file.name)
                print(ex)

