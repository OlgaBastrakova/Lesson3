# Вывести последнюю букву в слове
word = 'Архангельск'
last = word[-1]
print(last)

# Вывести количество букв "а" в слове
word = 'Архангельск'
last = len(word)
print(last)



# Вывести количество гласных букв в слове
word = 'Архангельск'

def count_vowels(word):
  
    vowels = 'аАеоыуиэ'  # список гласных букв
    count = 0
    for letter in word:
    
        if letter in vowels:
           
            count += 1
    return count
vowel_count = count_vowels(word)
print(vowel_count)


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
a1 = sentence.split()
print(len(a1))




# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
a1 = sentence.split()
for word in a1:
    print(word[0])



# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'

def average_word_length(sentence):

    words = sentence.split()  # разбиваем предложение на слова
    total_length = sum(len(word) for word in words)  # суммируем длины всех слов
    average_length = total_length / len(words)  # вычисляем среднюю длину слова
    print("Усредненная длина слова в предложении: {:.1f}".format(average_length))

average_word_length(sentence)