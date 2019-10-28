#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import sys
import os
import webbrowser

url = 'https://reports.exodus-privacy.eu.org/en/reports/%s/latest/' % os.getenv('package')
webbrowser.open(url)