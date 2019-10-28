#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import sys
import os
import webbrowser

url = 'https://play.google.com/store/apps/details?id=' + os.getenv('package')
webbrowser.open(url)