#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009-2013 Zuza Software Foundation
#
# This file is part of Pootle.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from django.utils.translation import ugettext_lazy as _, ungettext

from .stats import get_raw_stats, stats_descriptions
from .baseurl import l


HEADING_CHOICES = [
    {
        'id': 'name',
        'class': 'stats',
        'display_name': _("Name"),
    },
    {
        'id': 'project',
        'class': 'stats',
        'display_name': _("Project"),
    },
    {
        'id': 'language',
        'class': 'stats',
        'display_name': _("Language"),
    },
    {
        'id': 'progress',
        'class': 'stats',
        # Translators: noun. The graphical representation of translation status
        'display_name': _("Progress"),
    },
    {
        'id': 'total',
        'class': 'stats-number sorttable_numeric',
        # Translators: Heading representing the total number of words of a file
        # or directory
        'display_name': _("Total"),
    },
    {
        'id': 'need-translation',
        'class': 'stats-number sorttable_numeric',
        'display_name': _("Need Translation"),
    },
    {
        'id': 'suggestions',
        'class': 'stats-number sorttable_numeric',
        # Translators: The number of suggestions pending review
        'display_name': _("Suggestions"),
    },
    {
        'id': 'activity',
        'class': 'stats',
        'display_name': _("Last Activity"),
    },
]


def get_table_headings(choices):
    """Filters the list of available table headings to the given `choices`."""
    return filter(lambda x: x['id'] in choices, HEADING_CHOICES)


def make_generic_item(path_obj, action):
    """Template variables for each row in the table.

    :func:`make_directory_item` and :func:`make_store_item` will add onto these
    variables.
    """
    try:
        stats = get_raw_stats(path_obj, include_suggestions=True)
        info = {
            'href': l(action),
            'href_all': path_obj.get_translate_url(),
            'href_todo': path_obj.get_translate_url(state='incomplete'),
            'href_sugg': path_obj.get_translate_url(state='suggestions'),
            'stats': stats,
            'tooltip': _('%(percentage)d%% complete',
                         {'percentage': stats['translated']['percentage']}),
            'title': path_obj.name,
        }

        errors = stats.get('errors', 0)
        if errors:
            info['errortooltip'] = ungettext('Error reading %d file',
                                             'Error reading %d files',
                                             errors, errors)

        info.update(stats_descriptions(stats))
    except IOError, e:
        info = {
            'href': l(action),
            'title': path_obj.name,
            'errortooltip': e.strerror,
            'data': {'errors': 1},
            }

    return info


def make_directory_item(directory):
    action = directory.pootle_path
    item = make_generic_item(directory, action)
    item.update({
        'icon': 'folder',
        'isdir': True,
    })
    return item


def make_store_item(store):
    action = store.pootle_path
    item = make_generic_item(store, action)
    item.update({
        'icon': 'file',
        'isfile': True,
    })
    return item


def get_children(translation_project, directory):
    """Returns a list of children directories and stores for this
    ``directory``, and also the parent directory.

    The elements of the list are dictionaries which keys are populated after
    in the templates.
    """
    parent = []
    parent_dir = directory.parent

    if not (parent_dir.is_language() or parent_dir.is_project()):
        parent = [{'title': u'..', 'href': l(parent_dir.pootle_path)}]

    directories = [make_directory_item(child_dir)
                   for child_dir in directory.child_dirs.iterator()]

    stores = [make_store_item(child_store)
              for child_store in directory.child_stores.iterator()]

    return parent + directories + stores
