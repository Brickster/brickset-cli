import re
import requests
import sys

import config

_API = 'https://brickset.com/api/v3.asmx'


def execute_api_request(api, include_hash=False, **kwargs):
    brickset_config = config.get_config()
    params = {'apiKey': brickset_config['api_key']}
    if include_hash:
        if 'hash' not in brickset_config:
            sys.exit('ERROR: user hash required. Run: brickset login')
        params['userHash'] = brickset_config['hash']
    for key, value in kwargs.iteritems():
        params[key] = str(value)  # important when value='params' but str everything anyway

    response = requests.get(_API + '/' + api, params=params)
    if response.status_code != 200:
        print response.text
        sys.exit('ERROR: {} API returned an unexpected error'.format(api))
    response_json = response.json()
    if response_json['status'] != 'success':
        print response.text
        sys.exit('ERROR: {} API returned an unexpected error'.format(api))

    return response_json


def download_instruction(directory, set_number, instruction):
    url = instruction['URL']
    filename = _construct_instruction_filename(set_number, instruction['description'], url)
    print 'Downloading', '"{}"'.format(instruction['description']), instruction['URL'], 'as', filename
    r = requests.get(url)
    with open('{}/{}'.format(directory, filename), 'wb') as f:
        f.write(r.content)


def _construct_instruction_filename(set_number, instruction_description, instruction_url):
    # match = re.compile('https://www\.lego\.com/biassets/bi/(\d+)\.pdf').match(instruction_url)
    match = re.compile('https://www\.lego\.com.*?/(\d+)\.pdf').match(instruction_url)
    pdf_number = match.group(1)

    # NO DESCRIPTION
    if instruction_description == '{No longer listed at LEGO.com}':
        return '{}_{}.pdf'.format(set_number, pdf_number)

    # REGION BOOK/OF_BOOKS
    match = re.compile(
        '^BI.*?(IN|NA|V[\.\s]*\d+(?:/\d+)?)\s+(?:BOOK\s*)?(\d+)(?:\s*/\s*\d+)?$', flags=re.IGNORECASE
    ).match(instruction_description)
    if match:
        region = _clean_region(match.group(1))
        book = match.group(2)
        return '{}_{}_b{}_{}.pdf'.format(set_number, region, book, pdf_number)

    # BOOK/OF_BOOKS REGION
    match = re.compile(
        '^BI.*?\s+(?:BOOK\s+)?(\d+)/\d+\s+(IN|NA|V[\.\s]*\d+(?:/V?\d+)?)$', flags=re.IGNORECASE
    ).match(instruction_description)
    if match:
        region = _clean_region(match.group(2))
        book = match.group(1)
        return '{}_{}_b{}_{}.pdf'.format(set_number, region, book, pdf_number)

    # /BOOK
    match = re.compile('^(?:BI|BUILDING INSTRUCTION)\s+\d+/(\d+)$').match(instruction_description)
    if match:
        return '{}_b{}_{}.pdf'.format(set_number, match.group(1), pdf_number)

    # REGION
    match = re.compile('^BI.*?\s+(IN|NA|V/?[\.\s]*\d+(?:((?:/|\s[+&]\s)V?\d+)+)?)$').match(instruction_description)
    if match:
        region = _clean_region(match.group(1))
        if 'comic book' in instruction_description.lower():
            filename = '{}_comic_{}_{}.pdf'.format(set_number, region, pdf_number)
        else:
            filename = '{}_{}_{}.pdf'.format(set_number, region, pdf_number)
        return filename

    # BOOK/OF_BOOKS
    match = re.compile('^BI.*?\s+(?:BOOK\s+)?(\d+)/\d+$').match(instruction_description)
    if match:
        book = match.group(1)
        return '{}_b{}_{}.pdf'.format(set_number, book, pdf_number)

    # OTHER
    match = re.compile('^(?:BI|BUI?LDING\s*INSTRUCTION).*?[\s-]+(\d+)$').match(instruction_description)
    if match:
        return '{}_{}.pdf'.format(set_number, pdf_number)


def _clean_region(region_to_clean):
    result = re.sub('[\s.]', '', region_to_clean)
    result = result.replace('V/', 'V')
    result = result.replace('/V', '/')
    result = result.replace('/', '_V')
    result = re.sub('[+&]', '_', result)
    return result.lower()
