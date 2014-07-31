import mistune


PRISM_LANGUAGE_ALIASES = {
    'c++': 'cpp',
    'coffee': 'coffeescript',
    'coffee-script': 'coffeescript',
    'cs': 'csharp',
    'html': 'markup',
    'js': 'javascript',
    'json': 'javascript',
    'objective-c': 'objectivec',
    'obj-c': 'objectivec',
    'objc': 'objectivec',
    'py': 'python',
    'rb': 'ruby',
    'sh': 'bash',
    'xml': 'markup',
}


PRISM_LANGAUGE_DEPENDENCIES = {
    'aspnet': 'markup',
    'bash': 'clike',
    'c': 'clike',
    'coffeescript': 'javascript',
    'cpp': 'c',
    'csharp': 'clike',
    'go': 'clike',
    'groovy': 'clike',
    'java': 'clike',
    'javascript': 'clike',
    'objectivec': 'c',
    'php': 'clike',
    'ruby': 'clike',
    'scala': 'java',
    'scss': 'css',
    'swift': 'clike',
}


class Renderer(mistune.Renderer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.languages = set()

    def block_code(self, code, lang=None):
        if lang in PRISM_LANGUAGE_ALIASES:
            lang = PRISM_LANGUAGE_ALIASES[lang]
        if lang is not None:
            self.languages.add(lang)
        return super().block_code(code, lang)


def resolve_prism_languages(language_set):
    """Resolve language aliases, add required dependencies, and order them.

    Returns a list of languages used. The more dependant langauge will be
    listed LAST.
    """
    languages = []

    def put_lang(lang):
        try:
            languages.remove(lang)
        except ValueError:  # Not found.
            pass
        languages.append(lang)

    for lang in language_set:
        put_lang(lang)
        while lang in PRISM_LANGAUGE_DEPENDENCIES:
            lang = PRISM_LANGAUGE_DEPENDENCIES[lang]
            put_lang(lang)

    return languages
