# python -m spacy download en_core_web_sm-3.0.0 --direct
from pathlib import Path
from typing import List, Any
from xml.etree import ElementTree

import cassis
import spacy
from cassis import Cas
from cassis.typesystem import Type
from spacy.tokens import Token, Doc

# init spacy
nlp: spacy.Language = spacy.load("en_core_web_sm")


def xml_to_plain_text(input_xml_file):
    xml: ElementTree.ElementTree = ElementTree.parse(input_xml_file)
    body: ElementTree.Element = xml.getroot()
    paragraph_list = []
    for paragraph in body:
        paragraph_text = ''.join([span.attrib['text'] for span in paragraph])
        paragraph_list.append(paragraph_text)
    document_text = '\n'.join(paragraph_list)
    return body, document_text


def convert_single_file(input_xml_file: str, output_xmi_file: str, manual_break_sentences: bool = False) -> None:
    body, document_text = xml_to_plain_text(input_xml_file)

    cas = Cas(typesystem=cassis.load_dkpro_core_typesystem())
    cas.sofa_string = document_text

    print("----")
    print(document_text)
    print("----")

    token_type: Type = cas.typesystem.get_type(
        'de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token')
    paragraph_type: Type = cas.typesystem.get_type(
        'de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Paragraph')
    sentence_type: Type = cas.typesystem.get_type(
        'de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence')

    total_doc_offset: int = 0
    for paragraph in body:
        this_paragraph_total_offset = total_doc_offset
        for span in paragraph:
            span_text = span.attrib['text']

            doc: Doc = nlp(span_text)

            for token in doc:
                assert isinstance(token, Token)
                # print(token.text, token.idx, len(token), token.idx + len(token), token.is_space)
                begin: int = total_doc_offset + token.idx
                end: int = total_doc_offset + token.idx + len(token)
                # annotate token -- only if it is not a space!
                if not token.is_space:
                    cas.add_annotation(token_type.__call__(begin=begin, end=end))

            total_doc_offset += len(span_text)

        # annotate paragraph
        this_paragraph_annotation = paragraph_type.__call__(
            begin=this_paragraph_total_offset, end=total_doc_offset)
        cas.add_annotation(this_paragraph_annotation)
        # and for paragraph too; but how about the '\n' char? maybe +1?
        total_doc_offset += 1

        # now create artificial sentences inside this paragraph, each one max N
        # characters long, to be properly displayed in Inception
        paragraph_tokens: List[Any] = cas.select_covered(token_type.name, this_paragraph_annotation)

        if manual_break_sentences:
            # Ugly manual split by character length into sequences
            max_characters_per_line = 120
            lines: List[List] = []
            current_line: List = []
            for token in paragraph_tokens:
                if len(current_line) == 0:
                    current_line.append(token)
                else:
                    first_line_token_begin: int = current_line[0].begin
                    this_token_end: int = token.end
                    char_length = this_token_end - first_line_token_begin
                    if char_length < max_characters_per_line:
                        current_line.append(token)
                    else:
                        lines.append(current_line)
                        current_line = [token]

            lines.append(current_line)

            for line in lines:
                cas.add_annotation(sentence_type.__call__(begin=line[0].begin, end=line[-1].end))
        else:
            # add sentences aligned exactly to paragraphs
            cas.add_annotation(sentence_type.__call__(
                begin=this_paragraph_annotation.begin,
                end=this_paragraph_annotation.end))

    print([x.get_covered_text() for x in cas.select(paragraph_type.name)])
    print([x.get_covered_text() for x in cas.select(sentence_type.name)])
    print([x.get_covered_text() for x in cas.select(token_type.name)])

    # create parent folder if not exists
    Path(output_xmi_file).parent.mkdir(parents=True, exist_ok=True)

    cas.to_xmi(output_xmi_file)


if __name__ == '__main__':
    annotations_2021_10_06__2021_10_31_N = ['001-86490', '001-161408', '001-60728', '001-57422', '001-115396',
                                            '001-67720', '001-146047', '001-102957', '001-70853', '001-96339', ]

    for i in annotations_2021_10_06__2021_10_31_N:
        convert_single_file('05_structured_cases/{}.xml'.format(i),
                            '06_xmi_cases/annotations_2021_10_06__2021_10_31_N/{}.xmi'.format(i))
