import pandas as pd
import PyPDF2
import os
import shutil
import time
from tkinter import messagebox as msgbox
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
import tkinter as tk
import re
import PyPDF2

class DirectoryManager:
    def __init__(self, path_katalog='PDF_NEW/'):
        self.path_katalog = os.path.abspath(os.curdir) + "/" + path_katalog
        self.path_katalog = self.path_katalog.replace("/", "\\")
        

    def create_directory(self): 
        if not os.path.exists(self.path_katalog): 
            os.makedirs(self.path_katalog) 

    def remove_directory(self): 
        try: 
            shutil.rmtree(self.path_katalog) 
            time.sleep(2) 
        except: 
            while os.path.exists(self.path_katalog) == True: 
                msgbox.showerror("Внимание!", "Не смог удалить файлы, возможно они все таки открыты в каком-то приложении.\n" + "Удалите каталог вручную и запустите скрипт заново.") 
                exit() 

    def get_file_path(self, message): 
        msgbox.showwarning("Выберите файл", message) 
        file_path = askopenfilename() 
        return file_path


class ExcelProcessor:
    def __init__(self, xls_file, sheet_name='Лист1'):
        self.xls_file = xls_file
        self.sheet_name = sheet_name

    def read_excel_data(self): 
        df = pd.read_excel(self.xls_file, sheet_name=self.sheet_name) 
        return df 

    def create_pivot_table(self): 
        itogi = os.path.abspath(os.curdir) + "/" + "Итоги.xlsx" 
        itogi = itogi.replace("/", "\\") 
        df = self.read_excel_data() 
        df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: str(x).zfill(4)) 
        pivot_table = pd.pivot_table(df, index=df.iloc[:, 3], aggfunc='count', margins=True).astype(int) 
        pivot_table = pivot_table.iloc[:, :1] 
        pivot_table.to_excel(itogi, sheet_name='Сводная таблица', index=True) 

    def process_data_frame(self): 
        df = self.read_excel_data()
        payment_number_to_code = {} 

        for row in df.itertuples(index=False):  
            date_of_file = str(row[0])  
            payment_number = str(row[1])  
            summa_of_payment = "{:.2f}".format(row[2]).replace(".", "-")  
            kod_SP = str(row[3]).zfill(4)  
            payment_number_to_code[payment_number] = [summa_of_payment, kod_SP] 
        return payment_number_to_code, date_of_file


class PDFExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self): 
        with open(self.file_path, 'rb') as pdf_file_obj:
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj) 

            num_pages = len(pdf_reader.pages) 
            text = "" 
            for page in range(num_pages): 
                page_obj = pdf_reader.pages[page] 
                text += page_obj.extract_text() 
        return text

    def find_payment_number(self, text):
        pattern = r'ПЛАТЕЖНОЕ ПОРУЧЕНИЕ № (\d+)'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None 
  
    def split_pdf_by_payment_number(self, payment_number_to_code_result, path_katalog, date_of_file_result):
        with open(self.file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            pages_by_kod_SP = {}

            for page in range(num_pages):
                page_obj = pdf_reader.pages[page]
                text = page_obj.extract_text()
                payment_number = self.find_payment_number(text)
                print(payment_number)
                #print(payment_number_to_code_result)
                if payment_number and payment_number in payment_number_to_code_result:
                    summa_of_payment, kod_SP = payment_number_to_code_result[payment_number]
                    #print(payment_number_to_code_result)
                    if kod_SP not in pages_by_kod_SP:
                        # Create a new PDF file for this kod_SP key
                        pages_by_kod_SP[kod_SP] = PyPDF2.PdfWriter()
                    pages_by_kod_SP[kod_SP].add_page(page_obj)
        return pages_by_kod_SP  

    def put_pdf_into_file (self, path_katalog, pages_by_kod_SP,date_of_file_result, manager):
        print("ghbdtn")
        for kod_SP, pdf_writer in pages_by_kod_SP.items():
            num_pages_in_pdf = len(pdf_writer.pages)
            output_file_name = os.path.join(manager.path_katalog, f"{date_of_file_result}_{kod_SP}_{num_pages_in_pdf}.pdf")
            #create directory, if it doesn't exist
            os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
            with open(output_file_name, "wb") as output_pdf:
                pdf_writer.write(output_pdf)  
        

            
def main():
    manager = DirectoryManager()
    manager.create_directory()
    manager.remove_directory()

    user_input = 'пп'
    xls_file = manager.get_file_path("Выберите подготовленный XLSx файл")
    pdf_file_name = manager.get_file_path("Выберите многостроничный PDF файл")

    processor = ExcelProcessor(xls_file)
    payment_number_to_code_result, date_of_file_result = processor.process_data_frame()
    processor.create_pivot_table()


    # Открываем PDF файл и создаем объект PdfFileReader
    pdf_extractor = PDFExtractor(pdf_file_name)
    #pdf_extractor.split_pdf_by_payment_number(payment_number_to_code_result, path_katalog, date_of_file_result)
    pages_by_kod_SP = pdf_extractor.split_pdf_by_payment_number(payment_number_to_code_result, manager.path_katalog, date_of_file_result)
    pdf_extractor.put_pdf_into_file(manager.path_katalog, pages_by_kod_SP, date_of_file_result, manager)

if __name__ == "__main__":
    main()
