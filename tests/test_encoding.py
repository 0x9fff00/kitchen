# -*- coding: utf-8 -*-
#

import unittest
from nose import tools

import re

from kitchen.text import encoding

class UnicodeNoStr(object):
    def __unicode__(self):
        return u'café'

class StrNoUnicode(object):
    def __str__(self):
        return u'café'.encode('utf8')

class StrReturnsUnicode(object):
    def __str__(self):
        return u'café'

class UnicodeReturnsStr(object):
    def __unicode__(self):
        return u'café'.encode('utf8')

class UnicodeStrCrossed(object):
    def __unicode__(self):
        return u'café'.encode('utf8')

    def __str__(self):
        return u'café'

class TestEncoding(unittest.TestCase):
    u_spanish = u'El veloz murciélago saltó sobre el perro perezoso.'
    utf8_spanish = u_spanish.encode('utf8')
    latin1_spanish = u_spanish.encode('latin1')
    u_japanese = u"速い茶色のキツネが怠惰な犬に'増"
    utf8_japanese = u_japanese.encode('utf8')
    euc_jp_japanese = u_japanese.encode('euc_jp')
    u_accent = u'café'
    u_accent_replace = u'caf\ufffd'
    u_accent_ignore = u'caf'
    latin1_accent = u_accent.encode('latin1')
    utf8_accent = u_accent.encode('utf8')
    u_syllabary = u'く ku'
    latin1_syllabary_replace = '? ku'
    latin1_syllabary_ignore = ' ku'

    repr_re = re.compile('^<[^ ]*\.([^.]+) object at .*>$')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_guess_encoding_no_chardet(self):
        tools.ok_(encoding.guess_encoding(self.utf8_spanish, disable_chardet=True) == 'utf8')
        tools.ok_(encoding.guess_encoding(self.latin1_spanish, disable_chardet=True) == 'latin1')
        tools.ok_(encoding.guess_encoding(self.utf8_japanese, disable_chardet=True) == 'utf8')
        tools.ok_(encoding.guess_encoding(self.euc_jp_japanese, disable_chardet=True) == 'latin1')

    def test_guess_encoding_with_chardet(self):
        # We go this slightly roundabout way because multiple encodings can
        # output the same byte sequence.  What we're really interested in is
        # if we can get the original unicode string without knowing the
        # encoding beforehand
        tools.ok_(encoding.to_unicode(self.utf8_spanish,
            encoding.guess_encoding(self.utf8_spanish)) == self.u_spanish)
        tools.ok_(encoding.to_unicode(self.latin1_spanish,
            encoding.guess_encoding(self.latin1_spanish)) == self.u_spanish)
        tools.ok_(encoding.to_unicode(self.utf8_japanese,
            encoding.guess_encoding(self.utf8_japanese)) == self.u_japanese)
        tools.ok_(encoding.to_unicode(self.euc_jp_japanese,
            encoding.guess_encoding(self.euc_jp_japanese)) == self.u_japanese)

    def test_to_unicode(self):
        '''Test to_unicode when the user gives good values'''
        tools.ok_(encoding.to_unicode(self.u_japanese, encoding='latin1') == self.u_japanese)

        tools.ok_(encoding.to_unicode(self.utf8_spanish) == self.u_spanish)
        tools.ok_(encoding.to_unicode(self.utf8_japanese) == self.u_japanese)

        tools.ok_(encoding.to_unicode(self.latin1_spanish, encoding='latin1') == self.u_spanish)
        tools.ok_(encoding.to_unicode(self.euc_jp_japanese, encoding='euc_jp') == self.u_japanese)

    def test_to_unicode_errors(self):
        tools.ok_(encoding.to_unicode(self.latin1_accent) == self.u_accent_replace)
        tools.ok_(encoding.to_unicode(self.latin1_accent, errors='ignore') == self.u_accent_ignore)
        tools.assert_raises(UnicodeDecodeError, encoding.to_unicode, *[self.latin1_accent], **{'errors': 'strict'})

    def test_to_unicode_non_string(self):
        tools.ok_(encoding.to_unicode(5) == u'')
        tools.ok_(encoding.to_unicode(5, non_string='passthru') == 5)
        tools.ok_(encoding.to_unicode(5, non_string='simplerepr') == u'5')
        tools.ok_(encoding.to_unicode(5, non_string='repr') == u'5')
        tools.assert_raises(TypeError, encoding.to_unicode, *[5], **{'non_string': 'strict'})

        tools.ok_(encoding.to_unicode(UnicodeNoStr(), non_string='simplerepr') == self.u_accent)
        tools.ok_(encoding.to_unicode(StrNoUnicode(), non_string='simplerepr') == self.u_accent)
        tools.ok_(encoding.to_unicode(StrReturnsUnicode(), non_string='simplerepr') == self.u_accent)
        tools.ok_(encoding.to_unicode(UnicodeReturnsStr(), non_string='simplerepr') == self.u_accent)
        tools.ok_(encoding.to_unicode(UnicodeStrCrossed(), non_string='simplerepr') == self.u_accent)

    def test_to_bytes(self):
        '''Test to_bytes when the user gives good values'''
        tools.ok_(encoding.to_bytes(self.utf8_japanese, encoding='latin1') == self.utf8_japanese)

        tools.ok_(encoding.to_bytes(self.u_spanish) == self.utf8_spanish)
        tools.ok_(encoding.to_bytes(self.u_japanese) == self.utf8_japanese)

        tools.ok_(encoding.to_bytes(self.u_spanish, encoding='latin1') == self.latin1_spanish)
        tools.ok_(encoding.to_bytes(self.u_japanese, encoding='euc_jp') == self.euc_jp_japanese)

    def test_to_bytes_errors(self):
        tools.ok_(encoding.to_bytes(self.u_syllabary, encoding='latin1') ==
                self.latin1_syllabary_replace)
        tools.ok_(encoding.to_bytes(self.u_syllabary, encoding='latin',
            errors='ignore') == self.latin1_syllabary_ignore)
        tools.assert_raises(UnicodeEncodeError, encoding.to_bytes,
            *[self.u_syllabary], **{'errors': 'strict', 'encoding': 'latin1'})

    def _check_repr_bytes(self, repr_string, obj_name):
        tools.ok_(isinstance(repr_string, str))
        match = self.repr_re.match(repr_string)
        tools.assert_false(match == None)
        tools.ok_(match.groups()[0] == obj_name)

    def test_to_bytes_non_string(self):
        tools.ok_(encoding.to_bytes(5) == '')
        tools.ok_(encoding.to_bytes(5, non_string='passthru') == 5)
        tools.ok_(encoding.to_bytes(5, non_string='simplerepr') == '5')
        tools.ok_(encoding.to_bytes(5, non_string='repr') == '5')
        tools.assert_raises(TypeError, encoding.to_bytes, *[5], **{'non_string': 'strict'})

        # No __str__ method so this returns repr
        string = encoding.to_bytes(UnicodeNoStr(), non_string='simplerepr')
        self._check_repr_bytes(string, 'UnicodeNoStr')

        # This object's _str__ returns a utf8 encoded object
        tools.ok_(encoding.to_bytes(StrNoUnicode(), non_string='simplerepr') == self.utf8_accent)

        # This object's __str__ returns unicode which to_bytes converts to utf8
        tools.ok_(encoding.to_bytes(StrReturnsUnicode(), non_string='simplerepr') == self.utf8_accent)
        # Unless we explicitly ask ofr something different
        tools.ok_(encoding.to_bytes(StrReturnsUnicode(),
            non_string='simplerepr', encoding='latin1') == self.latin1_accent)

        # This object has no __str__ so it returns repr
        string = encoding.to_bytes(UnicodeReturnsStr(), non_string='simplerepr')
        self._check_repr_bytes(string, 'UnicodeReturnsStr')

        # This object's __str__ returns unicode which to_bytes converts to utf8
        tools.ok_(encoding.to_bytes(UnicodeStrCrossed(), non_string='simplerepr') == self.utf8_accent)

    def test_str_eq(self):
        tools.ok_(encoding.str_eq(self.u_japanese, self.u_japanese) == True)
        tools.ok_(encoding.str_eq(self.euc_jp_japanese, self.euc_jp_japanese) == True)
        tools.ok_(encoding.str_eq(self.u_japanese, self.euc_jp_japanese) == False)
        tools.ok_(encoding.str_eq(self.u_japanese, self.euc_jp_japanese, encoding='euc_jp') == True)

    def test_to_str(self):
        tools.ok_(encoding.to_str(5) == u'5')