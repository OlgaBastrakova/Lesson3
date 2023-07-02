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


def remove_directory(path_katalog):
    try:
        shutil.rmtree(path_katalog)
        time.sleep(2)
    except:
        while os.path.exists(path_katalog) == True:
            msgbox.showerror("Внимание!", "Не смог удалить файлы, возможно они все таки открыты в каком-то приложении.\n" + "Удалите каталог вручную и запустите скрипт заново.")
            exit()


def get_file_path(message):
    msgbox.showwarning("Выберите файл", message)
    file_path = askopenfilename()
    return file_path

def read_excel_data(xls_file, sheet_name='Лист1'):
    df = pd.read_excel(xls_file, sheet_name=sheet_name)
    return df

def create_pivot_table(xls_file):
    itogi = os.path.abspath(os.curdir) + "/" + "Итоги.xlsx"
    itogi = itogi.replace("/", "\\")
    df = read_excel_data(xls_file, sheet_name='Лист1')
    df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: str(x).zfill(4))
    pivot_table = pd.pivot_table(df, index=df.iloc[:, 3], aggfunc='count', margins=True).astype(int)
    pivot_table = pivot_table.iloc[:, :1]
    pivot_table.to_excel(itogi, sheet_name='Сводная таблица', index=True)

 # Создаем словарь для хранения страниц по ключу kod_SP
def process_data_frame(df):
    payment_number_to_code = {}

    for row in df.itertuples(index=False): 
        date_of_file = str(row[0]) 
        payment_number = str(row[1]) 
        summa_of_payment = "{:.2f}".format(row[2]).replace(".", "-") 
        kod_SP = str(row[3]).zfill(4) 
        payment_number_to_code[payment_number] = [summa_of_payment, kod_SP]
    return payment_number_to_code, date_of_file 

            
def main():
    path_katalog = os.path.abspath(os.curdir) + "/PDF_NEW/"
    path_katalog = path_katalog.replace("/","\\")
    root = tk.Tk()
    root.withdraw()
    remove_directory(path_katalog)
    user_input = 'пп'
    xls_file = get_file_path("Выберите подготовленный XLSx файл")
    pdf_file_name = get_file_path("Выберите многостроничный PDF файл")
    df = read_excel_data(xls_file, sheet_name='Лист1')
    create_pivot_table(xls_file) 
    payment_number_to_code_result, date_of_file_result = process_data_frame(df)
    pages_by_kod_SP = {} 

    # Открываем PDF файл и создаем объект PdfFileReader

    with open(pdf_file_name, 'rb') as pdf_file:  
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        pdf_extractor = PDFExtractor(pdf_file_name)

        for page in range(num_pages): 
            page_obj = pdf_reader.pages[page] 
            text = page_obj.extract_text() 
            payment_number = pdf_extractor.find_payment_number(text)
            print(payment_number)
            if payment_number and payment_number in payment_number_to_code_result:
                summa_of_payment, kod_SP = payment_number_to_code_result[payment_number]
                if kod_SP not in pages_by_kod_SP:

                     # Создаем новый PDF-файл для этого ключа kod_SP
                    pages_by_kod_SP[kod_SP] = PyPDF2.PdfWriter()
                pages_by_kod_SP[kod_SP].add_page(page_obj)
                
        if not os.path.exists(path_katalog):
            os.makedirs(path_katalog)

        for kod_SP, pdf_writer in pages_by_kod_SP.items(): 
            num_pages_in_pdf = len(pdf_writer.pages) 
            output_file_name = os.path.join(path_katalog, f"{date_of_file_result}_{user_input}_{kod_SP}_{num_pages_in_pdf}_.pdf") 
            with open(output_file_name, "wb") as output_pdf: 
                pdf_writer.write(output_pdf)
       

        #pdf_file.close() 

if __name__ == "__main__":
    main()
