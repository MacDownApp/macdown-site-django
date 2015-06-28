import base64
import json
import os
import re

from django.apps import apps
from django.utils.six.moves import urllib


GITHUB_API_BASE_URL = 'https://api.github.com/'
STABLE_TAG_PATTERN = re.compile(r'^v[\d\.]+$')


def get_endpoint(path, params=None):
    url = urllib.parse.urljoin(GITHUB_API_BASE_URL, path)
    if params is not None:
        url = url + '?' + '&'.join('{k}={v}'.format(
            k=key, v=params[key],
        ) for key in params)
    response = urllib.request.urlopen(url)
    return json.loads(response.read().decode('utf8'))


def get_latest_tag():
    tag_data_list = get_endpoint('/repos/uranusjr/macdown/tags')
    tag = None
    for tag_data in tag_data_list:
        tag_name = tag_data['name']
        if STABLE_TAG_PATTERN.match(tag_name):
            tag = tag_name
            break
    assert tag is not None
    return tag


def download_endpoint(endpoint, ref, encoding='utf-8'):
    data = get_endpoint(endpoint, params={'ref': ref})
    content_str = base64.b64decode(data['content']).decode(encoding)
    return content_str


def get_prism_languages():
    """Use the GitHub API to get a list of currently contained Prism languages.
    """
    # Get Git URL of Prism submodule at the tag.
    data = get_endpoint(
        '/repos/uranusjr/macdown/contents/Dependency/prism',
        params={'ref': get_latest_tag()},
    )
    components_str = download_endpoint(
        endpoint='/repos/PrismJS/prism/contents/components.js',
        ref=data['sha'],
    )
    # Make this string JSON-compatible.
    components_str = components_str[
        components_str.find('{'):components_str.rfind('}') + 1
    ]
    components_str_lines = [
        line for line in components_str.splitlines(True)
        if not line.strip().startswith('//')
    ]
    components = json.loads(''.join(components_str_lines))

    languages = components['languages']
    return languages


def get_language_aliases():
    """Get a list of MacDown-maintained language aliases.
    """
    info_str = download_endpoint(
        endpoint=(
            '/repos/uranusjr/macdown/contents/MacDown/Resources/'
            'syntax_highlighting.json'
        ),
        ref=get_latest_tag(),
    )
    info = json.loads(info_str)
    return info['aliases']


def get_language_notes():
    """Get custom notes for languages.

    The values are raw HTML content. A key can be either a Prism language ID, or
    a MacDown language alias.
    """
    app_config = apps.get_app_config('pages')
    path = os.path.join(
        app_config.path, 'static', 'pages', 'data', 'language_notes.json',
    )
    with open(path) as f:
        return json.load(f)


LANGUAGE_INFO_CACHE = None


def get_language_infos():
    if LANGUAGE_INFO_CACHE is None:
        languages = get_prism_languages()
        del languages['meta']
        infos = {lang: '' for lang in languages if not lang.endswith('-extras')}

        aliases = get_language_aliases()
        infos.update({
            k: 'Alias to <code>{lang}</code>.'.format(lang=aliases[k])
            for k in aliases
        })

        notes = get_language_notes()
        for lang in notes:
            infos[lang] = notes[lang]

        infos = [(key, infos[key]) for key in sorted(infos.keys())]
        global LANGUAGE_INFO_CACHE
        LANGUAGE_INFO_CACHE = infos
    return LANGUAGE_INFO_CACHE
