import sys, getopt

def parse_parametri(argv):
    inputfolder = './'
    outputfile = ''
    fornitore = ''
    outputformat = 'csv'

    try:
        opts, args = getopt.getopt(argv, "hi:f:o:t:", ["ifolder=", "fornitore=", "ofile=", "otype="])
    except getopt.GetoptError:
        print('analisi_fatture.py -i <inputfolder> -f <fornitore> -o <outputfile> -t <typeoutputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('analisi_fatture.py -i <inputfolder> -f <fornitore> -o <outputfile> -t <typeoutputfile>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            inputfolder = arg
        elif opt in ("-f", "--fornitore"):
            fornitore = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--otype"):
            outputformat = arg
    return [inputfolder, fornitore, outputfile, outputformat]