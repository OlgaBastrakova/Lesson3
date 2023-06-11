import pandas as pd
import PyPDF2


my_dict = {}
# Создаем словарь для хранения страниц по ключу value2 
pages_by_value2 = {} 

df = pd.read_excel('ВТБ 11.05.23.xlsx', sheet_name='Лист1')

for row in df.itertuples(index=False):
    key = str(row[0])
    #value1 = str(row[1]).replace(".", "-")  
    value1 = "{:.2f}".format(row[1]).replace(".", "-")
    if value1.endswith("-"):
        value1 = value1[:-1]
    #print(value1)
    value2 = str(row[2]).zfill(4)
    my_dict[key] = [value1, value2]


# Открываем PDF файл и создаем объект PdfFileReader
pdf_file = open('ВТБ без выписки.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Получаем количество страниц в PDF файле
num_pages = len(pdf_reader.pages)
print(num_pages)
# Проходим по каждой странице и получаем ее содержимое

for page_num in range(num_pages):
    page = pdf_reader.pages[page_num]
    page_content = page.extract_text()
    
    # Сравниваем содержимое страницы с данными из словаря
    for key, values in my_dict.items():

        #if key in page_content and values[0] in page_content: #and values[1] in page_content:
        if key in page_content and (values[0]  or values[0].replace("-", " -") in page_content):
            # Найден нужный лист 
            value2 = values[1] 
            if value2 not in pages_by_value2: 
                print(value2)
                # Создаем новый PDF-файл для этого ключа value2 
                pages_by_value2[value2] = PyPDF2.PdfWriter() 
                # Добавляем страницу в PDF-файл 
            pages_by_value2[value2].add_page(page) 
            #print(len(pages_by_value2))
            break 
        

# Закрываем PDF файл
pdf_file.close()
# Сохраняем каждый PDF-файл по ключу value2 
for value2, pdf_writer in pages_by_value2.items(): 
    with open(f"{value2}.pdf", "wb") as output_pdf: 
        pdf_writer.write(output_pdf)

 