import unicodedata
import csv

LXX_FILE = 'lxx.tsv'
MAKE_LOWERCASE = True  # Jeremy said he made them lowercase
REMOVE_PUNCTUATION = True  # Presumably punctuation is removed
REMOVE_ACCENTS = False  # Accent treatment is unspecified

greek_punctuation = "·?!,.⸀"


def treat_words(verse):
    if MAKE_LOWERCASE:
        verse = verse.lower()

    if REMOVE_ACCENTS:
        nfd_form = unicodedata.normalize('NFD', verse)
        verse = "".join([c for c in nfd_form if not unicodedata.combining(c)])

    if REMOVE_PUNCTUATION:
        for mark in greek_punctuation:
            verse = verse.replace(mark, '')
    if any(mark in verse for mark in greek_punctuation):
        print(verse)
    return verse.split()


class Book:
    def __init__(self, title, id):
        self.title = title
        self.id = int(id)

        self.num_chapters = 0
        self.words = []

    def add_verse(self, verse):
        self.words += treat_words(verse)

    def __str__(self):
        return f"{self.title} {len(self.words)}"


curr_book = None
all_books = []
with open(LXX_FILE, newline='', encoding='utf-8') as f:
    f.seek(3)  # Encoding marker at the beginning of the file is not recognized by csv library
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if not curr_book or row[0] != curr_book.title:
            curr_book = Book(row[0], row[3])
            all_books.append(curr_book)

        if len(row) == 6:
            curr_book.add_verse(row[5])
        elif len(row) == 5 and ("Hosea" in row[0] or "Zechariah" in row[0]):
            # Hosea and Zechariah are broken... idk why
            curr_book.add_verse(row[4])
        else:
            raise Exception

# for book in all_books:
#     print(book)

print(all_books[0].words[:3])