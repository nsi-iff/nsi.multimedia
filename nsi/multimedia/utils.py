#!/usr/bin/env python
#-*- coding:utf-8 -*-

def replace_file_extension(filename, extension):
    dot = filename.rfind('.')
    new_filename = filename[:dot] + '.' + extension
    return new_filename

