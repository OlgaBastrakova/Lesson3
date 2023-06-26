import pandas as pd
import PyPDF2

import os
import shutil
import time
from tkinter import messagebox as msgbox
from tkinter.filedialog import askopenfilename
import tkinter as tk
import PySimpleGUI as sg
import time

msgbox.showwarning("PDF", "Выберите многостроничный PDF файл")
pdf_file_name = askopenfilename()
print(pdf_file_name)

with open(pdf_file_name, 'rb') as pdf_file:  
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    num_pages = len(pdf_reader.pages)
    print(f"Количество страниц в PDF-файле: {num_pages}")


    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        print(f"Текст на странице {page_num + 1}:\n{page_text}\n")