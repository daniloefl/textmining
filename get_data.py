#!/usr/bin/env python

import os
import utils
import datetime

def main():
  for s in utils.sources:
    source = utils.sources[s]
    output = 'data/%s/%s' % (datetime.date.today().strftime("%Y%m%d"), s)
    try:
      os.makedirs(output)
    except:
      pass
    os.system('wget -O %s/front.html %s' % (output, source.www))

if __name__ == "__main__":
  main()

