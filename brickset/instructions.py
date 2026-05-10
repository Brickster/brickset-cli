import hashlib
import re
import requests
from pathlib import Path

from . import api
from .cache import id_to_set_number_generator, set_number_to_id_generator


def _parse_pdf_number(instruction_url):
    match = re.compile(r'^https://www\.lego\.com.*/(.*)\.pdf$').match(instruction_url)
    if match:
        pdf_name = match.group(1).lower()

        # just a number
        match = re.compile(r'^\d+$').match(pdf_name)
        if match:
            return pdf_name

        # main build
        match = re.compile(r'^(\d+)_(\d+)_build_main$').match(pdf_name)
        if match:
            return match.group(1) + match.group(2)
    return None


def _clean_region(region_to_clean):
    result = re.sub(r'[\s.]', '', region_to_clean)
    result = result.replace('V/', 'V')
    result = result.replace('/V', '/')
    result = result.replace('/', '_V')
    result = re.sub('[+&]', '_', result)
    return result.lower()


_RULES = []


def _rule(regex, flags=0):
    def decorator(fn):
        _RULES.append((re.compile(regex, flags), fn))
        return fn
    return decorator


@_rule(r'^BI.*?(IN|NA|V[\.\s]*\d+(?:/\d+)?)\s+(?:BOOK\s*)?(\d+)(?:\s*/\s*\d+)?$', re.IGNORECASE)
def _region_book(set_number, pdf_number, match, _description):
    region = _clean_region(match.group(1))
    book = match.group(2)
    return f'{set_number}_{region}_b{book}_{pdf_number}.pdf'


@_rule(r'^BI.*?\s+(?:BOOK\s+)?(\d+)/\d+\s+(IN|NA|V[\.\s]*\d+(?:/V?\d+)?)$', re.IGNORECASE)
def _book_region(set_number, pdf_number, match, _description):
    region = _clean_region(match.group(2))
    book = match.group(1)
    return f'{set_number}_{region}_b{book}_{pdf_number}.pdf'


@_rule(r'^(?:BI|BUILDING INSTRUCTION)\s+\d+/(\d+)$')
def _book_only(set_number, pdf_number, match, _description):
    return f'{set_number}_b{match.group(1)}_{pdf_number}.pdf'


@_rule(r'^BI.*?\s+(IN|NA|V/?[\.\s]*\d+(?:((?:/|\s[+&]\s)V?\d+)+)?)$')
def _region_only(set_number, pdf_number, match, description):
    region = _clean_region(match.group(1))
    if 'comic book' in description.lower():
        return f'{set_number}_comic_{region}_{pdf_number}.pdf'
    return f'{set_number}_{region}_{pdf_number}.pdf'


@_rule(r'^BI.*?\s+(?:BOOK\s+)?(\d+)/\d+$')
def _book_of_books(set_number, pdf_number, match, _description):
    return f'{set_number}_b{match.group(1)}_{pdf_number}.pdf'


@_rule(r'^\d+_\d+_build_main$', re.IGNORECASE)
def _build_main(set_number, pdf_number, _match, _description):
    return f'{set_number}_{pdf_number}.pdf'


@_rule(r'^\d+_(\d+)_(?:BI_)?Build_Alt$', re.IGNORECASE)
def _build_alt(set_number, _pdf_number, match, _description):
    return f'{set_number}_alt_{match.group(1)}.pdf'


@_rule(r'\d+_[a-z]+', re.IGNORECASE)
def _set_short_desc(set_number, _pdf_number, _match, description):
    return f'{set_number}_{hashlib.sha256(description.encode("utf-8")).hexdigest()[0:8]}.pdf'


@_rule(r'^INSPIRATIONAL MATERIAL,.*?\s+(IN|NA|V/?[\.\s]*\d+(?:(?:/|\s[+&]\s)V?\d+)*)$', re.IGNORECASE)
def _inspirational_material_region(set_number, pdf_number, match, _description):
    region = _clean_region(match.group(1))
    return f'{set_number}_{region}_{pdf_number}.pdf'


@_rule(r'^INSPIRATIONAL MATERIAL,', re.IGNORECASE)
def _inspirational_material(set_number, pdf_number, _match, _description):
    return f'{set_number}_{pdf_number}.pdf'


@_rule(r'^(?:BI|BUI?LDING\s*INSTRUCTION).*?[\s-]+(\d+)$')
def _other(set_number, pdf_number, _match, _description):
    return f'{set_number}_{pdf_number}.pdf'


def _construct_instruction_filename(set_number, instruction_description, instruction_url):
    pdf_number = _parse_pdf_number(instruction_url)

    if instruction_description == '{No longer listed at LEGO.com}':
        return f'{set_number}_{pdf_number}.pdf'

    for pattern, handler in _RULES:
        if m := pattern.match(instruction_description):
            return handler(set_number, pdf_number, m, instruction_description)

    return None


def get_instructions(id, directory, set_number=None):
    ids = id if id is not None else set_number_to_id_generator(set_number)
    set_numbers = set_number if set_number is not None else id_to_set_number_generator(id)
    for set_id, cur_set_number in zip(ids, set_numbers):
        if not set_id:
            print(f'No instructions found for set number {cur_set_number}')
            continue
        if not cur_set_number:
            print(f'No instructions found for set ID {set_id}')
            continue
        instructions_json = api.execute_api_request('getInstructions', setID=set_id)
        if not instructions_json['instructions']:
            print(f'No instructions found for {cur_set_number} ({set_id})')
            if directory:
                with open(Path(directory) / f'{cur_set_number}_noinstructions.txt', 'wb'):
                    pass
            continue

        fetched = instructions_json['instructions']
        if directory:
            for i in fetched:
                download_instruction(directory, cur_set_number, i)
        else:
            for i in fetched:
                _print_instruction(cur_set_number, i)


def _print_instruction(set_number, instruction):
    print(f'{set_number}: "{instruction["description"]}" {instruction["URL"]}')


def download_instruction(directory, set_number, instruction):
    url = instruction['URL']
    filename = _construct_instruction_filename(set_number, instruction['description'], url)
    if not filename:
        print(f'WARN: Skipping unknown instruction format: "{instruction["description"]}" {url}')
        return
    print(f'Downloading "{instruction["description"]}" {url} as {filename}')
    r = requests.get(url)
    with open(Path(directory) / filename, 'wb') as f:
        f.write(r.content)
