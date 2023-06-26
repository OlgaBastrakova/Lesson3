import pandas as pd
import PyPDF2


payment_number_to_code = {}
# Создаем словарь для хранения страниц по ключу kod_SP
pages_by_kod_SP = {} 

df = pd.read_excel('ВТБ 11.05.23.xlsx', sheet_name='Лист1')

for row in df.itertuples(index=False):
    payment_number = str(row[0])
    summa_of_payment = "{:.2f}".format(row[1]).replace(".", "-")
    if summa_of_payment.endswith("-"):
        summa_of_payment = value1[:-1]
    kod_SP = str(row[2]).zfill(4)
    payment_number_to_code[payment_number] = [summa_of_payment, kod_SP]


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
    for payment_number, values in payment_number_to_code.items():
        
        search_platezhka = "ПЛАТЕЖНОЕ ПОРУЧЕНИЕ № " + payment_number
        search_order = "БАНКОВСКИЙ ОРДЕР № " +  payment_number
        #search_obyavlenie = "ОБЪЯВЛЕНИЕ N " + payment_number
        #print(search_platezhka)
        print(page_content)
        if search_platezhka or search_order in page_content and (values[0]  or values[0].replace("-", " -") in page_content):
            # Найден нужный лист 
            kod_SP = values[1] 
            if kod_SP not in pages_by_kod_SP: 
                print(kod_SP)
                
                # Создаем новый PDF-файл для этого ключа kod_SP
                pages_by_kod_SP[kod_SP] = PyPDF2.PdfWriter() 
                # Добавляем страницу в PDF-файл 
            pages_by_kod_SP[kod_SP].add_page(page) 
            break 
        

# Закрываем PDF файл
pdf_file.close()
# Сохраняем каждый PDF-файл по ключу kod_SP 
for kod_SP, pdf_writer in pages_by_kod_SP.items(): 
    with open(f"{kod_SP}.pdf", "wb") as output_pdf: 
        pdf_writer.write(output_pdf)

 