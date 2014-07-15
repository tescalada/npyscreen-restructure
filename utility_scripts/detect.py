#!/usr/bin/env python

import os
import sys

print(sys.stdin.isatty(), os.environ.get("TERM", None))

