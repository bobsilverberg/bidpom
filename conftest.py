#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import py
import pytest
import requests

from selenium.webdriver.support.ui import WebDriverWait

from mocks.user import MockUser


@pytest.fixture
def persona_test_user():
    return requests.get('http://personatestuser.org/email').json()


@pytest.fixture
def new_user(persona_test_user):
    return MockUser(primary_email=persona_test_user['email'],
                    password=persona_test_user['pass'])


@pytest.fixture
def login_dialog(request):
    persona_login_button_locator_css = 'button.btn-persona'
    mozwebqa = request.getfuncargvalue('mozwebqa')
    mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
    WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
        lambda s: s.find_element_by_css_selector(persona_login_button_locator_css).is_displayed())
    mozwebqa.selenium.find_element_by_css_selector(persona_login_button_locator_css).click()


def pytest_runtest_setup(item):
    item.config.option.api = 'webdriver'
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin('mozwebqa')
    pytest_mozwebqa.TestSetup.email = item.config.option.email
    pytest_mozwebqa.TestSetup.password = item.config.option.password


def pytest_addoption(parser):
    group = parser.getgroup('persona', 'persona')
    group._addoption('--email',
                     action='store',
                     metavar='str',
                     help='email address for persona account')
    group._addoption('--password',
                     action='store',
                     metavar='str',
                     help='password for persona account')


# def pytest_funcarg__mozwebqa(request):
#     persona_login_button_locator_css = 'button.btn-persona'
#     mozwebqa = request.getfuncargvalue('mozwebqa')
#     mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
#     WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
#         lambda s: s.find_element_by_css_selector(persona_login_button_locator_css).is_displayed())
#     mozwebqa.selenium.find_element_by_css_selector(persona_login_button_locator_css).click()
#     return mozwebqa
