import os
import tempfile
from django.test import TestCase
from nose.tools import assert_equal, assert_raises
from . import posts


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
        assert_equal(posts.default_post_dir, self.post_dir)

    def test_get_post_abspath(self):
        post_path = os.path.join(self.post_dir, 'foo')
        assert_equal(posts.get_post_abspath('foo'), post_path)

    def test_does_not_exist(self):
        with assert_raises(posts.PostDoesNotExist):
            posts.Post('loremipsum', self.post_dir)

    def test_default_dir(self):
        post = posts.Post('01-the-macdown-blog.md')
        assert_equal(post.dirpath, self.post_dir)


class PostTests(TestCase):
    """Tests for Post model.
    """
    def setUp(self):
        fd, path = tempfile.mkstemp(prefix='1-', suffix='.md')
        f = os.fdopen(fd, 'w')
        f.write(EXAMPLE_POST_CONTENT)
        f.close()
        dirpath, filename = os.path.split(path)
        self.post = posts.Post(filename, dirpath)
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

    def test_meta(self):
        assert_equal(self.post.meta, {
            'title': 'Test Post', 'author': 'Tzu-ping Chung',
        })
        assert_equal(self.post.title, 'Test Post')
        assert_equal(self.post.author, 'Tzu-ping Chung')
        with assert_raises(AttributeError):
            self.post.foobar

    def test_rendered_content(self):
        assert_equal(self.post.rendered_content, '<p>Lorem ipsum.</p>\n')

    def test_get_absolute_url(self):
        # Strip "1-" and ".md" from filename to get the slug.
        expected = '/blog/post/1/{slug}/'.format(slug=self.filename[2:-3])
        assert_equal(self.post.get_absolute_url(), expected)
