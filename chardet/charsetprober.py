######################## BEGIN LICENSE BLOCK ########################
# The Original Code is Mozilla Universal charset detector code.
#
# The Initial Developer of the Original Code is
# Netscape Communications Corporation.
# Portions created by the Initial Developer are Copyright (C) 2001
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Mark Pilgrim - port to Python
#   Shy Shalom - original C code
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA
######################### END LICENSE BLOCK #########################

from . import constants
import re
from io import BytesIO


class CharSetProber:
    def __init__(self):
        pass

    def reset(self):
        self._mState = constants.eDetecting

    def get_charset_name(self):
        return None

    def feed(self, aBuf):
        pass

    def get_state(self):
        return self._mState

    def get_confidence(self):
        return 0.0

    def filter_high_bit_only(self, aBuf):
        aBuf = re.sub(b'([\x00-\x7F])+', b' ', aBuf)
        return aBuf

    def filter_international_words(self, buf):
        """
            we define three types of bytes:
            alphabet: english alphabets [a-zA-Z]
            international: international characters [\x80-\xFF]
            marker: everything else [^a-zA-Z\x80-\xFF]

            the input buffer can be thought to contain a series of words
            delimited by markers.
            this function works to filter all words that contain at-least one
            international character. all contiguous sequences of markers are
            replaced by a single space ascii character.
        """
        filtered = BytesIO()

        # this regex expression filters out only words that have at-least
        # one international character. the word may include one marker
        # character at the end
        words = \
            re.findall(b'[a-zA-Z]*[\x80-\xFF]+[a-zA-Z]*[^a-zA-Z\x80-\xFF]?',
                       buf)

        for word in words:
            filtered.write(word[:-1])

            # if the last character in the word is a marker, replace it with a
            # space as markers shouldn't affect our analysis (they are used
            # similarly across all languages and may thus have similar
            # frequencies)
            last_char = word[-1:]
            last_char = last_char if last_char.isalpha() or \
                last_char >= b'\x80' else b' '
            filtered.write(last_char)

        return filtered.getvalue()

    def filter_with_english_letters(self, aBuf):
        # TODO
        return aBuf
