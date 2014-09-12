from base.markdown import PRISM_LANGAUGE_DEPENDENCIES


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
