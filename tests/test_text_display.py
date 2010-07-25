# -*- coding: utf-8 -*-
#
import unittest
from nose import tools

from kitchen.text import display

import base_classes

class TestDisplay(base_classes.UnicodeTestData, unittest.TestCase):

    def test_textual_width(self):
        '''Test that we find the proper number of spaces that a utf8 string will consume'''
        tools.ok_(display.textual_width(self.u_japanese) == 31)
        tools.ok_(display.textual_width(self.u_spanish) == 50)
        tools.ok_(display.textual_width(self.u_mixed) == 23)

    def test_textual_width_chop(self):
        '''utf8_width_chop with byte strings'''
        tools.ok_(display.textual_width_chop(self.u_mixed, 1000) == self.u_mixed)
        tools.ok_(display.textual_width_chop(self.u_mixed, 23) == self.u_mixed)
        tools.ok_(display.textual_width_chop(self.u_mixed, 22) == self.u_mixed[:-1])
        tools.ok_(display.textual_width_chop(self.u_mixed, 19) == self.u_mixed[:-4])
        tools.ok_(display.textual_width_chop(self.u_mixed, 2) == self.u_mixed[0])
        tools.ok_(display.textual_width_chop(self.u_mixed, 1) == u'')
"""

    def test_utf8_width_chop_unicode(self):
        '''utf8_width_chop with unicode input'''
        tools.ok_(utf8.utf8_width_chop(self.u_mixed) == (23, self.u_mixed))
        tools.ok_(utf8.utf8_width_chop(self.u_mixed, 23) == (23, self.u_mixed))
        tools.ok_(utf8.utf8_width_chop(self.u_mixed, 22) == (22, self.u_mixed[:-1]))
        tools.ok_(utf8.utf8_width_chop(self.u_mixed, 19) == (18, self.u_mixed[:-4]))
        tools.ok_(utf8.utf8_width_chop(self.u_mixed, 2) == (2, self.u_mixed[0]))
        tools.ok_(utf8.utf8_width_chop(self.u_mixed, 1) == (0, ''))

    def test_utf8_width_fill(self):
        '''Pad a utf8 string'''
        tools.ok_(utf8.utf8_width_fill(self.utf8_mixed, 1) == self.utf8_mixed)
        tools.ok_(utf8.utf8_width_fill(self.utf8_mixed, 25) == self.utf8_mixed + '  ')
        tools.ok_(utf8.utf8_width_fill(self.utf8_mixed, 25, left=False) == '  ' + self.utf8_mixed)
        tools.ok_(utf8.utf8_width_fill(self.utf8_mixed, 25, chop=18) == self.u_mixed[:-4].encode('utf8') + '       ')
        tools.ok_(utf8.utf8_width_fill(self.utf8_mixed, 25, chop=18, prefix=self.utf8_spanish, suffix=self.utf8_spanish) == self.utf8_spanish + self.u_mixed[:-4].encode('utf8') + self.utf8_spanish + '       ')
        tools.ok_(utf8.utf8_width_fill(self.utf8_mixed, 25, chop=18) == self.u_mixed[:-4].encode('utf8') + '       ')
        tools.ok_(utf8.utf8_width_fill(self.u_mixed, 25, chop=18, prefix=self.u_spanish, suffix=self.utf8_spanish) == self.u_spanish.encode('utf8') + self.u_mixed[:-4].encode('utf8') + self.u_spanish.encode('utf8') + '       ')
        pass

    def test_utf8_valid(self):
        '''Test that a utf8 byte sequence is validated'''
        warnings.simplefilter('ignore', DeprecationWarning)
        tools.ok_(utf8.utf8_valid(self.utf8_japanese) == True)
        tools.ok_(utf8.utf8_valid(self.utf8_spanish) == True)
        warnings.simplefilter('default', DeprecationWarning)

    def test_utf8_invalid(self):
        '''Test that we return False with non-utf8 chars'''
        warnings.simplefilter('ignore', DeprecationWarning)
        tools.ok_(utf8.utf8_valid('\xff') == False)
        tools.ok_(utf8.utf8_valid(self.latin1_spanish) == False)
        warnings.simplefilter('default', DeprecationWarning)

    def test_utf8_text_wrap(self):
        tools.ok_(utf8.utf8_text_wrap(self.utf8_mixed) == [self.utf8_mixed])
        tools.ok_(utf8.utf8_text_wrap(self.paragraph) == self.paragraph_out)
        tools.ok_(utf8.utf8_text_wrap(self.utf8_mixed_para) == self.utf8_mixed_para_out)
        tools.ok_(utf8.utf8_text_wrap(self.utf8_mixed_para, width=57,
            initial_indent='    ', subsequent_indent='----') ==
            self.utf8_mixed_para_57_initial_subsequent_out)
    """