import requests
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def map_function(text):
    words = text.split()
    return [(word, 1) for word in words]

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

# Виконання MapReduce
def map_reduce(text):
    # Крок 1: Мапінг
    mapped_values = map_function(text)

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Редукція
    reduced_values = reduce_function(shuffled_values)

    return reduced_values

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
    url = 'https://www.gutenberg.org/files/1343/1343-0.txt'
    response = requests.get(url)
    text = response.text
    
    word_counts = map_reduce(text)
    visualize_top_words(word_counts, top_n=10)
