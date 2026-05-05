import hashlib
import re
import requests


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
    return '{}_{}_b{}_{}.pdf'.format(set_number, region, book, pdf_number)


@_rule(r'^BI.*?\s+(?:BOOK\s+)?(\d+)/\d+\s+(IN|NA|V[\.\s]*\d+(?:/V?\d+)?)$', re.IGNORECASE)
def _book_region(set_number, pdf_number, match, _description):
    region = _clean_region(match.group(2))
    book = match.group(1)
    return '{}_{}_b{}_{}.pdf'.format(set_number, region, book, pdf_number)


@_rule(r'^(?:BI|BUILDING INSTRUCTION)\s+\d+/(\d+)$')
def _book_only(set_number, pdf_number, match, _description):
    return '{}_b{}_{}.pdf'.format(set_number, match.group(1), pdf_number)


@_rule(r'^BI.*?\s+(IN|NA|V/?[\.\s]*\d+(?:((?:/|\s[+&]\s)V?\d+)+)?)$')
def _region_only(set_number, pdf_number, match, description):
    region = _clean_region(match.group(1))
    if 'comic book' in description.lower():
        return '{}_comic_{}_{}.pdf'.format(set_number, region, pdf_number)
    return '{}_{}_{}.pdf'.format(set_number, region, pdf_number)


@_rule(r'^BI.*?\s+(?:BOOK\s+)?(\d+)/\d+$')
def _book_of_books(set_number, pdf_number, match, _description):
    return '{}_b{}_{}.pdf'.format(set_number, match.group(1), pdf_number)


@_rule(r'^\d+_\d+_build_main$', re.IGNORECASE)
def _build_main(set_number, pdf_number, _match, _description):
    return '{}_{}.pdf'.format(set_number, pdf_number)


@_rule(r'\d+_[a-z]+', re.IGNORECASE)
def _set_short_desc(set_number, _pdf_number, _match, description):
    return '{}_{}.pdf'.format(set_number, hashlib.sha256(description.encode('utf-8')).hexdigest()[0:8])


@_rule(r'^(?:BI|BUI?LDING\s*INSTRUCTION).*?[\s-]+(\d+)$')
def _other(set_number, pdf_number, _match, _description):
    return '{}_{}.pdf'.format(set_number, pdf_number)


def _construct_instruction_filename(set_number, instruction_description, instruction_url):
    pdf_number = _parse_pdf_number(instruction_url)

    if instruction_description == '{No longer listed at LEGO.com}':
        return '{}_{}.pdf'.format(set_number, pdf_number)

    for pattern, handler in _RULES:
        if m := pattern.match(instruction_description):
            return handler(set_number, pdf_number, m, instruction_description)

    return None


def download_instruction(directory, set_number, instruction):
    url = instruction['URL']
    filename = _construct_instruction_filename(set_number, instruction['description'], url)
    if not filename:
        print('WARN: Skipping unknown instruction URL format: {}'.format(url))
        return
    print('Downloading "{}" {} as {}'.format(instruction['description'], url, filename))
    r = requests.get(url)
    with open('{}/{}'.format(directory, filename), 'wb') as f:
        f.write(r.content)