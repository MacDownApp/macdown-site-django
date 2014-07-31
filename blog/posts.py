import os
import re
import yaml
from django.utils.functional import cached_property
from django.conf import settings
from django.core.urlresolvers import reverse
from django.apps import apps
from django.template import TemplateDoesNotExist


FRONT_MATTER_PATTERN = re.compile(r'^---\n(.*?\n)---', re.DOTALL)


class PostDoesNotExist(TemplateDoesNotExist):
    pass


class Post:

    FILENAME_PATTERN = re.compile(r'^(\d+)-([\w-]+)$')

    def __init__(self, filename, dirpath=None):
        filename, ext = os.path.splitext(filename)
        match = self.FILENAME_PATTERN.match(filename)
        if match is None:
            raise PostDoesNotExist(
                os.path.join(dirpath, ''.join([filename, ext]))
            )
        self.id = int(match.group(1))
        self.slug = match.group(2)

        if dirpath is None:
            dirpath = default_post_dir
        self.dirpath = dirpath

    def __getattr__(self, key):
        try:
            value = self.file_content[0][key]
        except KeyError:
            raise AttributeError(key)
        return value

    @property
    def filename(self):
        return '{id}-{slug}.md'.format(id=self.id, slug=self.slug)

    @property
    def abspath(self):
        return os.path.join(self.dirpath, self.filename)

    @cached_property
    def file_content(self):
        """Returns a 2-tuple (meta, content).
        """
        full_content = self.read()
        front_matter, offset = get_front_matter(full_content)
        return (front_matter, full_content[offset:])

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'id': self.id, 'slug': self.slug})

    def read(self):
        return load_post_source(self.filename, self.dirpath)


def calculate_post_dir():
    app_config = apps.get_app_config('blog')
    return os.path.join(app_config.path, 'posts')


default_post_dir = calculate_post_dir()


def get_post_filelist(post_dir=None):
    if post_dir is None:
        post_dir = default_post_dir
    return os.listdir(post_dir)


def get_post_filename(id, post_dir=None):
    prefix = '{id}-'.format(id=id)
    for filename in get_post_filelist(post_dir):
        if filename.startswith(prefix):
            return filename
    if post_dir is None:
        post_dir = default_post_dir
    raise PostDoesNotExist(
        'ID {id} in directory {dir}'.format(id=id, dir=post_dir)
    )


def get_post_abspath(filename, post_dir=None):
    if post_dir is None:
        post_dir = default_post_dir
    return os.path.join(post_dir, filename)


def load_post_source(filename, post_dir=None):
    filepath = get_post_abspath(filename, post_dir)
    try:
        with open(filepath, 'rb') as f:
            return f.read().decode(settings.FILE_CHARSET)
    except IOError:
        pass
    raise PostDoesNotExist(filepath)


def get_front_matter(markdown):
    """Returns a 2-tuple (front_matter, content_offset)
    """
    front_matter = None
    offset = 0
    match = FRONT_MATTER_PATTERN.search(markdown)
    if match:
        try:
            front_matter = yaml.load(match.group(1))
        except yaml.YAMLError:
            pass
        else:
            offset = match.end(0) + 1   # Eat newline after closing "---"
    return (front_matter, offset)
