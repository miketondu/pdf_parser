import sys
from PyQt5.QtWidgets import *
from gui import Ui_MainWindow
import multiprocessing
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from multiprocessing import Process, Manager
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import resolve1
import os

ListOfStrings = []


class PdfPositionHandling:

    def add_quotes_to_list(self, start_list):
        '''Add qutes to records with ',' inside '''
        for item in start_list:
            for index in range(0, len(item)):
                if ',' in str(item[index]):
                    item[index] = '"' + str(item[index]).replace(',', '') + '"'
        return start_list

    def create_csv(self, result_list, folder, save_name, start_string):
        '''Save csv to filesystem. selected folder'''
        result_string = start_string
        for a in result_list:
            result_string += str(','.join(a))
            result_string += '\n'
        cvs_result = open(folder + '/' + str(save_name),
                          'w', encoding='utf-8')
        cvs_result.write(result_string)
        cvs_result.close()

    def parse_obj(self, lt_objs, i):
        '''parse pdf elements to python list'''

        for obj in lt_objs:
            if isinstance(obj, LTTextLine):
                ListOfStrings.append([[int(obj.bbox[0]), int(obj.bbox[1])],
                                      obj.get_text().replace('\n', ' ')])
            if isinstance(obj, LTTextBoxHorizontal):
                self.parse_obj(obj._objs, i)
            elif isinstance(obj, LTFigure):
                self.parse_obj(obj._objs, i)

    def parse_pdf(self, file_name, start_page, end_page, save_folder):
        '''parse pdf to list of lists and save to csv'''
        fp = open(file_name, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        rsrcmgr = PDFResourceManager()
        device = PDFDevice(rsrcmgr)
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        i = 0
        first_table = []
        second_table = []
        origen = ''
        for page in PDFPage.create_pages(document):
            if start_page <= i <= end_page:
                interpreter.process_page(page)
                layout = device.get_result()
                self.parse_obj(layout._objs, i)
            i += 1
            ListOfStrings.sort(key=lambda x: (-x[0][1], x[0][0]))

            required_section = False
            for a in ListOfStrings:
                if a[0][0] == 17 and a[0][1] == 482:
                    origen = a[1]
                if a[0][0] == 17 and '----' in a[1] and required_section:
                    required_section = False
                if a[0][0] == 17 and '----' in a[1] and not required_section:
                    required_section = True
                if 70 < a[0][0] < 72 and '----' not in a[1] and 'Container' not in a[1]:
                    temp_table_A = [''] * 6
                    temp_table_A[0] = ListOfStrings[ListOfStrings.index(a)][1].split()[0]
                    temp_table_A[1] = ListOfStrings[ListOfStrings.index(a)][1].split()[1]
                    temp_table_A[2] = ListOfStrings[ListOfStrings.index(a) + 1][1].split()[0]
                    temp_table_A[3] = ListOfStrings[ListOfStrings.index(a) + 1][1].split()[1]
                    temp_table_A[4] = ListOfStrings[ListOfStrings.index(a) + 2][1]
                    temp_table_A[5] = origen
                    if temp_table_A != [''] * 5:
                        first_table.append(temp_table_A)
                if a[0][0] == 17 and '----' not in a[1] and 'Freight' not in a[1] and required_section:
                    temp_table_B = [''] * 5
                    temp_table_B[0] = ListOfStrings[ListOfStrings.index(a)][1]
                    temp_table_B[1] = ListOfStrings[ListOfStrings.index(a) + 1][1]
                    temp_table_B[2] = ListOfStrings[ListOfStrings.index(a) + 2][1].split('.')[0]
                    temp_table_B[3] = ""
                    temp_table_B[4] = ListOfStrings[ListOfStrings.index(a) + 3][1].split('.')[0]
                    if temp_table_B != [''] * 5:
                        second_table.append(temp_table_B)
            ListOfStrings.clear()
        if first_table != []:
            self.create_csv(self.add_quotes_to_list(first_table), save_folder,
                            file_name.split('/')[-1].split('.')[0] + '_A.csv',
                            'sep=,\ncontainer,seall number,tare,type,packages,ORIGEN\n')
        if second_table != []:
            self.create_csv(self.add_quotes_to_list(second_table), save_folder,
                            file_name.split('/')[-1].split('.')[0] + '_B.csv',
                            'sep=,\nFreight/Charge ,Basis,Rated as,Prepaid,Collect\n')


def prepare_to_parsing(file_name, folder):
    '''get`s pdf 2 last page values'''
    pdf_handler = PdfPositionHandling()
    file = open(file_name, 'rb')
    parser = PDFParser(file)
    document = PDFDocument(parser)
    len_of_pdf = resolve1(document.catalog['Pages'])['Count']
    pdf_handler.parse_pdf(file_name, len_of_pdf - 2, len_of_pdf - 1, folder)


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = ''
        self.files = []
        self.ui.selectPDF.clicked.connect(self.select_pdf)
        self.ui.selectSaveFolder.clicked.connect(self.select_save_folder)
        self.ui.runButton.clicked.connect(self.parse_run)
        self.show()

    def select_pdf(self):
        '''get pdf`s file names'''
        caption = 'Open file'
        # use current/working directory
        directory = './'
        filter_mask = "*.pdf"
        self.files, _ = QFileDialog.getOpenFileNames(None,
                                                     caption, directory, filter_mask)

    def select_save_folder(self):
        '''get save folder'''
        self.folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.labelPATH.setText("Save dir: " + str(self.folder))

    def parse_run(self):
        if self.files == []:
            return
        files = self.files
        if self.folder != '':
            folder = self.folder
        else:
            folder = os.path.dirname(files[0])

        with Manager() as manager:
            processes = []
            for filename in files:
                p = Process(target=prepare_to_parsing, args=(filename, folder))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    w = AppWindow()
    w.setStyleSheet("QMainWindow {background: '#C2efC4';}");
    w.show()
    sys.exit(app.exec_())
