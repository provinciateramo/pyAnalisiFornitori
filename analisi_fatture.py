import os
from pathlib import Path
import xml.etree.ElementTree as ET
from decimal import Decimal as D
import sys, getopt
import re
import csv

from plugins import *
from utils import parse_parametri

def main(argv):
    inputfolder, fornitore_key, outputfile = parse_parametri(argv)
    print(inputfolder, fornitore_key, outputfile)
    c = fornitore.plugins_fatture.get(fornitore_key, None)
    if not c is None:
        f = c(csvfile=outputfile, inputfolder=inputfolder)
        f.genera_csv()
        print('File %s generato con successo' % outputfile)
    else:
       print('Plugin non trovato per il fornitore')

if __name__ == "__main__":
    main(sys.argv[1:])
