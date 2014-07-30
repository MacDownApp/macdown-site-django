import os
import tempfile
from django.test import TestCase
from nose.tools import assert_equal
from . import utils


EXAMPLE_POST_CONTENT = (
    """---
title: Test Post
author: Tzu-ping Chung
---

Lorem ipsum.
""")


class PostDirTests(TestCase):
    """Tests for Post lookup-related things.
    """
    def setUp(self):
        self.post_dir = os.path.join(os.path.dirname(__file__), 'posts')

    def test_post_dir(self):
        assert_equal(utils.default_post_dir, self.post_dir)

    def test_get_post_abspath(self):
        post_path = os.path.join(self.post_dir, 'foo')
        assert_equal(utils.get_post_abspath('foo'), post_path)


class PostTests(TestCase):
    """Tests for Post model.
    """
    def setUp(self):
        fd, path = tempfile.mkstemp(prefix='1-', suffix='.md')
        f = os.fdopen(fd, 'w')
        f.write(EXAMPLE_POST_CONTENT)
        f.close()
        dirpath, filename = os.path.split(path)
        self.post = utils.Post(filename, dirpath)
        self.filename = filename

    def tearDown(self):
        os.remove(self.post.abspath)

    def test_load(self):
        pass    # If this fails, Post initialization failed.

    def test_filename(self):
        assert_equal(self.post.filename, self.filename)

    def test_file_content(self):
        fm, content = self.post.file_content
        assert_equal(fm, {'title': 'Test Post', 'author': 'Tzu-ping Chung'})
        assert_equal(content.strip(), 'Lorem ipsum.')
