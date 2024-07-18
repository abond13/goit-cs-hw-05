import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import requests
import matplotlib.pyplot as plt
import numpy as np

# Функція для завантаження тексту за URL
def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the text: {e}")
        return None

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()
    words = [word.lower() for word in words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# Функція для візуалізації результатів
def visualize_top_words(word_counts, top_n=10):
    sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    words, counts = zip(*sorted_word_counts)
    
    plt.figure(figsize=(10, 6))
    plt.barh(np.arange(len(words)), counts, align='center', color='skyblue')
    plt.yticks(np.arange(len(words)), words)
    plt.xlabel('Frequency')
    plt.title(f'Top {top_n} Words by Frequency')
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == '__main__':
    # URL-адреса для завантаження тексту
    url = 'https://gutenberg.net.au/ebooks01/0100021.txt'
    text = get_text(url)
    
    if text:
        # Виконання MapReduce на вхідному тексті
        word_counts = map_reduce(text)

        print("Результат підрахунку слів:", word_counts)
        
        # Візуалізація топ слів з найвищою частотою використання
        visualize_top_words(word_counts, top_n=10)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")