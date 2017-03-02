import os
import utils
import datetime

def main():
  for day in os.listdir('data/'):
    for s in utils.sources:
      source = utils.sources[s]
      output = 'data/%s/%s' % (day, s)
      source.clean('%s/front.txt' %output, '%s/front_clean.txt' % output)

if __name__ == "__main__":
  main()

