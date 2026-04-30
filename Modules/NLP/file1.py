import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# download karein internet se seedha
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("omw-1.4")

# text base sentence dena hai
text = "Students are learning Python"

# tokenization
tokens = word_tokenize(text)
print("Tokenization data:", tokens)

# lemmatization
l = WordNetLemmatizer()  # iss tool se words ko base form me convert karte hain

l_w = []  # empty list for storing lemmatized words

# loop tokens par chalega
for w in tokens:
    l_w.append(l.lemmatize(w))

# output
print("Lemmatization Words:", l_w)