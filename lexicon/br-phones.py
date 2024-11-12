from phonemizer.backend import EspeakBackend
from phonemizer.punctuation import Punctuation
from phonemizer.separator import Separator

backend = EspeakBackend('pt-br')
separator = Separator(phone=' ', word=None)

def get_phonemes(text):
    text = Punctuation(';:,.!"?()-').remove(text)
    words = {w.upper() for w in text.split(' ') if w}
    lexicon = {
        word: backend.phonemize([word], separator=separator, strip=True)[0]
        for word in words}
    return lexicon

def get_phonemes_word(word):
    return backend.phonemize([word], separator=separator, strip=True)[0]

words = set()
with open('../data/nurc_min/metadata.csv', 'r') as arquivo:
    for linha in arquivo:
        linha = linha.strip()
        arquivo_audio, texto = linha.split('|')
        print(f"Arquivo de áudio: {arquivo_audio} Texto: {texto}")
        for palavra in texto.split():
            words.add(palavra.lower())

    phonemes = list()
    i = 0
    total = len(words)
    sorted_words = sorted(words)
    with open("nurc-min-lexicon.txt", 'a') as f:
        for word in sorted_words:
            i += 1
            if i < 3789:
                continue
            linha = f"{word.upper()}\t{get_phonemes_word(word)}\n"
            f.write(linha)
            if i % 100 == 0:
                print(word, i, '/', total)

#text =  'O rato roeu a roupa do rei de roma.'
#lexicon = get_phonemes(text)
#text =  'E o pinguim mergulhou no Piauí.'
#lexicon.update(get_phonemes(text))
#print(lexicon)
