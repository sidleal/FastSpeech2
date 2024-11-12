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

lexicon = {}
with open('../data/nurc_min/metadata.csv', 'r') as arquivo:
    for linha in arquivo:
        linha = linha.strip()
        arquivo_audio, texto = linha.split('|')
        print(f"Arquivo de áudio: {arquivo_audio} Texto: {texto}")
        lexicon.update(get_phonemes(texto))

print(lexicon)
