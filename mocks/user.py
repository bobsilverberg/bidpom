#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MockUser(dict):

    def __init__(self, **kwargs):
        self['primary_email'] = ''
        self['password'] = ''
        self['additional_emails'] = []

        self.update(**kwargs)

    def __getattr__(self, attr):
        return self[attr]
