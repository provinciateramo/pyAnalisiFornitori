__all__ = []

from pathlib import Path
import xlsxwriter
import csv

plugins_writer = {}


def register_plugins_writer(extension, classe):
    plugins_writer[extension] = classe


class OutputFileWriter(object):
    def __init__(self, wtype='csv', outputfile='output'):
        self.wtype = wtype
        f_ext = outputfile.rpartition('.')[-1]
        if f_ext and f_ext == wtype:
            self.outputfile = outputfile
        else:
            self.outputfile = '%s.%s' % (outputfile, f_ext)
        self.f_writer = None
        self.writer = None
        self.generate_writer()

    def generate_writer(self):
        """
        Implementa nelle sotto classi
        :return:
        """

    def write_row(self, row):
        """
        Scrive una riga
        """

    def close_writer(self):
        self.f_writer.close()


class CSVFileWriter(OutputFileWriter):
    """CSV Output File
    """

    def generate_writer(self):
        self.f_writer = open(self.outputfile, mode='w')
        self.writer = csv.writer(self.f_writer, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    def write_row(self, row):
        self.writer.writerow(row)


register_plugins_writer('csv', CSVFileWriter)


class ExcelFileWriter(OutputFileWriter):
    """CSV Output File
    """

    def __init__(self, wtype='csv', outputfile='output'):
        super(ExcelFileWriter, self).__init__(wtype, outputfile)
        self.current_row = 0

    def generate_writer(self):
        self.f_writer = xlsxwriter.Workbook(self.outputfile)
        self.writer = self.f_writer.add_worksheet()

    def write_row(self, row):
        for cell, data in enumerate(row):
            self.writer.write(self.current_row, cell, data)
        self.current_row += 1


register_plugins_writer('xlsx', ExcelFileWriter)