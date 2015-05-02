#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.template.loader import get_template
from ghostdown.forms.widgets import GhostdownInput


class PopupGhostdownInput(GhostdownInput):
    def get_template(self):
        return get_template('sparkle/includes/ghostdown_editor.html')
