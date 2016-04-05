# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 22:52:53 2016

@author: Bella
"""

import hashlib
import types

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def md5(s):
    if type(s) is types.StringType:
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()
    else:
        return ''      