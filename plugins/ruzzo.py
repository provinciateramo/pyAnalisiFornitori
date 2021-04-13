import re
import xml.etree.ElementTree as ET
from decimal import Decimal as D
from .fornitore import PluginFornitore, register_plugin_fattura

class Ruzzo(PluginFornitore):
    def __init__(self, csvfile='dati.csv', inputfolder='./', outputwriter=None):
        self.fornitore = 'fastweb'
        super(Ruzzo,self).__init__(self.fornitore, csvfile, inputfolder, outputwriter)

    def parse_fattura(self, nomefile):
        data = {'pod': '', 'importo': D(0.0)}
        fattura = ET.parse(self.path_to_fattura(nomefile))
        root = fattura.getroot()

        nodo_pod = root.findall(".//FatturaElettronicaBody/DatiGenerali/DatiContratto/IdDocumento")
        print(nodo_pod)

        if not nodo_pod is None and len(nodo_pod):
            id_pod = nodo_pod[0].text

            self.append_to_log('Trovato POD %s\r\n' % id_pod)
            data['pod'] = id_pod
        else:
            self.append_to_log('ERRORE: non trovato POD per fattura %s\r\n' % nomefile)
            return data
        nodo_pagamento = root.findall(".//DatiPagamento/DettaglioPagamento/ImportoPagamento")
        if not nodo_pagamento is None and len(nodo_pagamento):
            data['importo'] = D(nodo_pagamento[0].text)
        else:
            self.append_to_log('ERRORE: non trovato importo per fattura %s\r\n' % nomefile)
            return data
        return data

    def genera_dati(self):
        """ metodo per analizzare i file e generare la struttura dati
        """
        for fattura in self.fatture:
            row = self.parse_fattura(fattura)
            if not row['pod']:
                continue
            if not row['pod'] in self.data.keys():
                self.data[row['pod']] = {}
                self.data[row['pod']]['importo'] = D(0.0)
                self.data[row['pod']]['fatture'] = []

            self.data[row['pod']]['importo'] += row['importo']
            self.data[row['pod']]['fatture'].append(fattura)


    def intestazione_csv(self):
        """ restituisce la riga di intestazione del csv"""
        return ['POD', 'Importo', 'Fatture', 'Totale Fatture']

    def footer_csv(self):
        """ restituisce la riga di footer del csv"""
        self.append_to_log('Totale: € %s, N. Fatture: %s\r\n' % (self.totale, self.totale_fatture))
        return ['Totale', self.totale, 'N. Fatture', self.totale_fatture]

    def riga_dati_csv(self, key, data):
        """ restituisce una riga di dati del csv"""
        importo = data['importo']
        fatture = ','.join(data['fatture'])
        self.totale += importo
        self.totale_fatture += len(data['fatture'])
        self.append_to_log('POD: %s, importo: € %s, n. fatture: %s\r\n' % (key, importo, len(data['fatture'])))
        return [key, importo, fatture, len(data['fatture'])]

register_plugin_fattura('ruzzo', Ruzzo)
