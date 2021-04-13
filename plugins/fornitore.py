import os
from pathlib import Path
from decimal import Decimal as D


plugins_fatture = {}

def register_plugin_fattura(fornitore, classe):
    plugins_fatture[fornitore] = classe

class PluginFornitore(object):
    def __init__(self, fornitore, csvfile='dati.csv', inputfolder='./', outputwriter=None):
        self.fornitore = fornitore
        self.inputfolder = inputfolder + (inputfolder[:-1]!='/' and '/' or '')
        self.csvfile = csvfile
        self.logfile = open('%s.log' % self.csvfile, 'w+')
        self.outputwriter = outputwriter
        self.fatture = []
        self.data = {}
        self.totale = D(0.0)
        self.totale_fatture = 0
        self.leggi_fatture()

    def append_to_log(self, message):
        self.logfile.write(message+'\r\n')

    def path_to_fattura(self, nomefile):
        return '%s%s' % (self.inputfolder, nomefile)

    def leggi_fatture(self):
        self.append_to_log('Avvio ricerca delle fatture...')
        for file in Path(self.inputfolder).glob('*.xml'):
            self.fatture.append(file.name)
            self.append_to_log('Trovata la fattura %s' % file.name)

    def parse_fattura(self, nomefile):
        """ metodo per estrarre i dati dalla fattura"""
        return []

    def genera_dati(self):
        """ metodo per analizzare i file e generare la struttura dati
        """

    def intestazione_csv(self):
        """ restituisce la riga di intestazione del csv"""
        return []

    def footer_csv(self):
        """ restituisce la riga di footer del csv"""
        return []

    def riga_dati_csv(self, key, data):
        """ restituisce una riga di dati del csv"""
        return []

    def genera_output(self):
        """ crea il file csv. chiama intestazione_csv e riga_dati_csv
        """
        self.append_to_log('Avvio generazione del file csv %s\r\n' % self.csvfile)
        if not self.data:
            self.genera_dati()
        self.outputwriter.write_row(self.intestazione_csv())
        for key, row in self.data.items():
            self.outputwriter.write_row(self.riga_dati_csv(key, row))
        self.outputwriter.write_row(self.footer_csv())
        self.append_to_log('Conclusa generazione del file csv %s\r\n' % self.csvfile)
        self.logfile.close()
        self.outputwriter.close_writer()