#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import pytest

from .. import BrowserID
from base import BaseTest
import restmail


@pytest.mark.nondestructive
class TestResetPassword(BaseTest):

    @pytest.mark.travis
    def test_reset_password(self, mozwebqa):
        user = self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
        self.log_out(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.find_element_by_css_selector('button.btn-persona').click()

        from .. pages.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout, expect='returning')
        signin.click_this_is_not_me()
        signin.email = user.primary_email
        signin.click_next()
        signin.click_forgot_password()
        mail = restmail.get_mail(user.primary_email,
                                 message_count=2,
                                 timeout=mozwebqa.timeout)
        assert 'Click to reset your password' in mail[1]['text']
        reset_url = re.search(BrowserID.RESET_URL_REGEX,
                              mail[1]['text']).group(0)
        signin.switch_to_main_window()
        mozwebqa.selenium.get(reset_url)

        from .. pages.reset_password import ResetPassword

        reset_password = ResetPassword(mozwebqa.selenium)
        user.password += '_new'
        reset_password.new_password = user.password
        reset_password.verify_password = user.password
        reset_password.click_finish()

        assert '%s has been verified!' % user.primary_email in reset_password.thank_you
