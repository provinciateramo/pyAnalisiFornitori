import sys, getopt

def parse_parametri(argv):
    inputfolder = './'
    outputfile = ''
    fornitore = ''

    try:
        opts, args = getopt.getopt(argv, "hi:f:o:", ["ifolder=", "fornitore=", "ofile="])
    except getopt.GetoptError:
        print('analisi_fatture.py -i <inputfolder> -f <fornitore> -o <csvfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('analisi_fatture.py -i <inputfolder> -f <fornitore> -o <csvfile>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            inputfolder = arg
        elif opt in ("-f", "--fornitore"):
            fornitore = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    return [inputfolder, fornitore, outputfile]