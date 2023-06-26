import pandas as pd
import PyPDF2
import os
import shutil
import time
from tkinter import messagebox as msgbox
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
import tkinter as tk
import PySimpleGUI as sg


path_katalog = os.path.abspath(os.curdir) + "/PDF_NEW/"
path_katalog = path_katalog.replace("/","\\")

root = tk.Tk()
root.withdraw()

try:
    shutil.rmtree(path_katalog)
    time.sleep(2)
except:
    while os.path.exists(path_katalog) == True:
        msgbox.showerror("Внимание!", "Не смог удалить файлы, возможно они все таки открыты в каком-то приложении.\n" + "Удалите каталог вручную и запустите скрипт заново.")
        exit()

#ввод информации от пользователя
#def get_user_input(prompt):
    #user_input = simpledialog.askstring("Ввод информации", prompt)
   # return user_input

# Использование функции get_user_input для получения информации от пользователя
#prompt = "Введите приход или пп:"
#user_input = get_user_input(prompt)
user_input = 'пп'



msgbox.showwarning("XLSX", "Выберите подготовленный XLSx файл")
xls_file = askopenfilename()
msgbox.showwarning("PDF", "Выберите многостроничный PDF файл")
pdf_file_name = askopenfilename()



payment_number_to_code = {}
# Создаем словарь для хранения страниц по ключу kod_SP
pages_by_kod_SP = {} 

itogi = os.path.abspath(os.curdir) + "/" + "Итоги.xlsx"
itogi = itogi.replace("/", "\\")
df = pd.read_excel(xls_file, sheet_name='Лист1')
# Применение zfill() ко всем значениям столбца с индексом 3
df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: str(x).zfill(4))
pivot_table=(pd.pivot_table(df, index=df.iloc[:,3], aggfunc='count', margins=True).astype(int))
pivot_table = pivot_table.iloc[:, :1]
pivot_table.to_excel(itogi, sheet_name = 'Сводная таблица', index=True)


for row in df.itertuples(index=False):
    date_of_file = str(row[0])
    payment_number = str(row[1])
    summa_of_payment = "{:.2f}".format(row[2]).replace(".", "-")

    kod_SP = str(row[3]).zfill(4)
    payment_number_to_code[payment_number] = [summa_of_payment, kod_SP]


# Открываем PDF файл и создаем объект PdfFileReader
with open(pdf_file_name, 'rb') as pdf_file:  
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    num_pages = len(pdf_reader.pages)
    print(f"Количество страниц в PDF-файле: {num_pages}")


    # Проходим по каждой странице и получаем ее содержимое
    for page_num in range(num_pages):  
        page = pdf_reader.pages[page_num]
        page_content = page.extract_text()
        print(page_content)
        
        # Сравниваем содержимое страницы с данными из словаря
        for payment_number, values in payment_number_to_code.items():
            search_platezhka = "ПЛАТЕЖНОЕ ПОРУЧЕНИЕ № " + payment_number
            search_order = "БАНКОВСКИЙ ОРДЕР № " +  payment_number
            search_obyavlenie = "ОБЪЯВЛЕНИЕ N " + payment_number
 
            if (search_order in page_content) or (search_platezhka in page_content) or (search_obyavlenie in page_content) and (values[0] or values[0].replace("-", " -") in page_content):
                # Найден нужный лист 
                print(f"Платежное поручение найдено в PDF-файле: {payment_number}")
                kod_SP = values[1] 
                if kod_SP not in pages_by_kod_SP: 
                    
                    # Создаем новый PDF-файл для этого ключа kod_SP
                    pages_by_kod_SP[kod_SP] = PyPDF2.PdfWriter() 
                    # Добавляем страницу в PDF-файл 
                pages_by_kod_SP[kod_SP].add_page(page) 
                break        

# Закрываем PDF файл
pdf_file.close()
# Сохраняем каждый PDF-файл по ключу kod_SP 

# Создание папки "PDFNEW", если она еще не существует
if not os.path.exists(path_katalog):
    os.makedirs(path_katalog)

for kod_SP, pdf_writer in pages_by_kod_SP.items():
    # Создание имени файла с указанием пути к папке "PDFNEW"
    num_pages_in_pdf = len(pdf_writer.pages)
    output_file_name = os.path.join(path_katalog, f"{date_of_file}_{user_input}_{kod_SP}_{num_pages_in_pdf}_.pdf")
    
    
    with open(output_file_name, "wb") as output_pdf:
        pdf_writer.write(output_pdf) 