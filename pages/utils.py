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


def get_prism_languages():
    """Use the GitHub API to get a list of currently contained Prism languages.
    """
    # Get latest stable tag.
    tag_data_list = get_endpoint('/repos/uranusjr/macdown/tags')
    tag = None
    for tag_data in tag_data_list:
        tag_name = tag_data['name']
        if STABLE_TAG_PATTERN.match(tag_name):
            tag = tag_name
            break
    assert tag is not None

    # Get Git URL of Prism submodule at the tag.
    data = get_endpoint(
        '/repos/uranusjr/macdown/contents/Dependency/prism',
        params={'ref': tag},
    )
    sha = data['sha']

    data = get_endpoint(
        '/repos/PrismJS/prism/contents/components.js',
        params={'ref': sha},
    )
    components_str = base64.b64decode(data['content']).decode('utf8')
    # Make this string JSON-compatible.
    components_str = components_str[
        components_str.find('{'):components_str.rfind('}') + 1
    ]
    components = json.loads(components_str)

    languages = components['languages']
    return languages


def get_language_aliases():
    """Get a list of MacDown-maintained language aliases.
    """
    # Currently hard-coded. We need to make this a JSON file in MacDown repo
    # in the future.
    return {
        'c++': 'cpp',
        'coffee': 'coffeescript',
        'coffee-script': 'coffeescript',
        'cs': 'csharp',
        'html': 'markup',
        'jl': 'julia',
        'js': 'javascript',
        'json': 'javascript',
        'obj-c': 'objectivec',
        'objc': 'objectivec',
        'objective-c': 'objectivec',
        'py': 'python',
        'rb': 'ruby',
        'sh': 'bash',
        'xml': 'markup',
    }


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
