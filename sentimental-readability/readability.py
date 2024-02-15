# TODO

# -----------------------------------------------------------------------------
# Constantes
# -----------------------------------------------------------------------------

PUNTUACIONES = ['.', '!', '?']

# -----------------------------------------------------------------------------
# Funciones
# -----------------------------------------------------------------------------

def count_letters(text):
    count = 0
    for ch in text:
        if ch.isalpha()==True:
            count = count + 1
    return count

def count_words(text):
    count = 1
    for ch in text:
        if ch.isspace()==True:
            count = count + 1
    return count

def count_sentences(text):
    count = 0
    for ch in text:
        if ch in PUNTUACIONES:
            count = count + 1
    return count

def calculate_index(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)
    return index

# -----------------------------------------------------------------------------
# MAin
# -----------------------------------------------------------------------------

text = input("Text: ")

letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

index = calculate_index(letters, words, sentences)

if index < 1:
    print("Before Grade 1")
elif index > 15:
    print("Grade 16+")
else:
    print(f"Grade {int(index)}")