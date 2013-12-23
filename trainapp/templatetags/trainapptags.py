# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 09:56:49 2013

@author: amyskerry
"""

from django.template import Library

register = Library()

def removearg(string, arg):
    """Removes all values of arg from the given string"""
    return string.replace(arg, '')
def lowercase(string):
    """Converts a string into all lowercase"""    
    return string.lower()
def humanreadablespace(string):
    """Converts a string into all lowercase"""    
    return string.replace('_',' ')
def displayformat(string):
    """Converts a string into all lowercase"""    
    string=string.replace('_',' ')
    string=string.replace('--',': ')
    return string
    
removearg = register.filter('removetag', removearg)   
lowercase = register.filter('lowercase', lowercase)   
humanreadablespace = register.filter('humanreadablespace',humanreadablespace)   
displayformat = register.filter('displayformat',displayformat)   