#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from subprocess import Popen, PIPE, STDOUT

def replace_file_extension(filename, extension):
    dot = filename.rfind('.')
    new_filename = filename[:dot] + '.' + extension
    return new_filename

def get_duration(file_):
    result = Popen(["ffprobe", file_],
        stdout=PIPE, stderr=STDOUT)
    metadata = [x for x in result.stdout.readlines() if 'Duration' in x] 
    matcher = re.search(r': (\d\d:\d\d:\d\d.\d\d),', metadata[0])
    time =  matcher.groups()[0]
    time = time.split(':')
    minutes = int(time[1])
    seconds = int(time[-1].split('.')[0])
    return (minutes * 60) + seconds
