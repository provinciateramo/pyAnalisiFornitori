import re
import xml.etree.ElementTree as ET
from decimal import Decimal as D
from .fornitore import PluginFornitore, register_plugin_fattura

class Fastweb(PluginFornitore):
    def __init__(self, csvfile='dati.csv', inputfolder='./'):
        self.fornitore = 'fastweb'
        super(Fastweb,self).__init__(self.fornitore, csvfile, inputfolder)

    def parse_fattura(self, nomefile):
        data = {'centro_fatturazione': '', 'importo': D(0.0)}
        fattura = ET.parse(nomefile)
        root = fattura.getroot()
        nodo_allegato = root.findall(".//Allegati/NomeAttachment")[0]
        if not nodo_allegato is None:
            nome_allegato = nodo_allegato.text
            try:
                centro_fatturazione = re.search("LA[^\.]*", nome_allegato).group()
            except:
                print('Errore nel centro di costo: %s, %s' % (nomefile, nome_allegato))
                self.append_to_log('Errore nel centro di costo: %s, %s\r\n' % (nomefile, nome_allegato))
                return data
            self.append_to_log('Trovato centro di costo %s\r\n' % centro_fatturazione)
            data['centro_fatturazione'] = centro_fatturazione
        else:
            self.append_to_log('ERRORE: non trovato centro di costo\r\n')
        nodo_pagamento = root.findall(".//DatiPagamento/DettaglioPagamento/ImportoPagamento")[0]
        if not nodo_pagamento is None:
            data['importo'] = D(nodo_pagamento.text)
        else:
            self.append_to_log('ERRORE: non trovato importo\r\n')
        return data

    def genera_dati(self):
        """ metodo per analizzare i file e generare la struttura dati
        """
        for fattura in self.fatture:
            row = self.parse_fattura(fattura)
            if not row['centro_fatturazione']:
                continue
            if not row['centro_fatturazione'] in self.data.keys():
                self.data[row['centro_fatturazione']] = {}
                self.data[row['centro_fatturazione']]['importo'] = D(0.0)
                self.data[row['centro_fatturazione']]['fatture'] = []

            self.data[row['centro_fatturazione']]['importo'] += row['importo']
            self.data[row['centro_fatturazione']]['fatture'].append(fattura)


    def intestazione_csv(self):
        """ restituisce la riga di intestazione del csv"""
        return ['CDC', 'Importo', 'Fatture', 'Totale Fatture']

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
        self.append_to_log('Centro di costo: %s, importo: € %s, n. fatture: %s\r\n' % (key, importo, len(data['fatture'])))
        return [key, importo, fatture, len(data['fatture'])]

register_plugin_fattura('fastweb', Fastweb)
