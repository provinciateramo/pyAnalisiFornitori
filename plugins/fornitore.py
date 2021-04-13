from pathlib import Path
from decimal import Decimal as D
import csv

plugins_fatture = {}

def register_plugin_fattura(fornitore, classe):
    plugins_fatture[fornitore] = classe

class PluginFornitore(object):
    def __init__(self, fornitore, csvfile='dati.csv', inputfolder='./'):
        self.fornitore = fornitore
        self.inputfolder = inputfolder
        self.csvfile = csvfile
        self.logfile = open('%s.log' % self.csvfile, 'w+')
        self.fatture = []
        self.data = {}
        self.totale = D(0.0)
        self.totale_fatture = 0
        self.leggi_fatture()

    def append_to_log(self, message):
        self.logfile.write(message+'\r\n')

    def leggi_fatture(self):
        self.append_to_log('Avvio ricerca delle fatture...')
        for file in Path(self.inputfolder).glob('*.xml'):
            nome_file = self.inputfolder + '/' + file.name
            self.fatture.append(nome_file)
            self.append_to_log('Trovata la fattura %s' % nome_file)

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

    def genera_csv(self):
        """ crea il file csv. chiama intestazione_csv e riga_dati_csv
        """
        self.append_to_log('Avvio generazione del file csv %s\r\n' % self.csvfile)
        if not self.data:
            self.genera_dati()
        with open(self.csvfile, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(self.intestazione_csv())
            for key, row in self.data.items():
                csv_writer.writerow(self.riga_dati_csv(key, row))
            csv_writer.writerow(self.footer_csv())
        self.append_to_log('Conclusa generazione del file csv %s\r\n' % self.csvfile)
        self.logfile.close()