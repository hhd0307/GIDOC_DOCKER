# -*- coding: utf-8 -*-


class Utterance:
    """
    A class represents for an utterance

    Atributes:
        - phrases: list of phrases in current utterance
        - label: contextual label of current utterance
    """

    LABEL_FORMAT         = '{0}^{1}-{2}+{3}={4}@{5}_{6}'
    LABEL_FORMAT        += '/A:{7}_{8}_{9}/B:{10}-{11}-{12}@{13}-{14}&{15}-{16}#{17}-{18}${19}-{20}!{21}-{22};{23}-{24}|{25}/C:{26}+{27}+{28}'
    LABEL_FORMAT        += '/D:{29}_{30}/E:{31}+{32}@{33}+{34}&{35}+{36}#{37}+{38}/F:{39}_{40}'
    LABEL_FORMAT        += '/G:{41}_{42}/H:{43}={44}@{45}={46}|{47}/I:{48}_{49}'
    LABEL_FORMAT        += '/J:{50}+{51}-{52}'  

    ##### Init method
    # We'll init list of phrases from initial data and then
    # init linked list between phrases for traveling between them
    # @params:
    #   - data: list of phrases of an utterance
    #   > [[['x', 'w', 'ie', 'n', '_5'], ['m', 'a', 'ji', '_3']], [['k', 'W', 'k', '_8'], ['x', 'u', 'N', '_4']]] <--> "khuyen mai, cuc khung"
    def __init__(self, data):
        self.phrases        = []
        self.label          = ''

        for index, phrase in enumerate(data):
            if len(data) == 1:
                new_phrase = Phrase(phrase, is_first_phrase=True, is_last_phrase=True)
            elif index == 0:
                new_phrase = Phrase(phrase, is_first_phrase=True)
            elif index == len(data) - 1:
                new_phrase = Phrase(phrase, is_last_phrase=True)
            else:
                new_phrase = Phrase(phrase)
            self.phrases.append(new_phrase)

        # After init phrase we need to init linked list between phrases
        for index, phrase in enumerate(self.phrases):
            if index - 1 >= 0:
                phrase.pre_phrase = self.phrases[index-1]
            else:
                phrase.pre_phrase = None
            if index + 1 < len(self.phrases):
                phrase.next_phrase = self.phrases[index+1]
            else:
                phrase.next_phrase = None
            phrase.init_words()

        self.init_punctuation()


    ##### Method for init punctuation
    def init_punctuation(self):
        for phrase_index, phrase in enumerate(self.phrases):
            if phrase_index < len(self.phrases) - 1:
                phrase.words[-1].punctuation = 'cm' # duy mod
            else:
                phrase.words[-1].punctuation = 'pr'


    ##### Get total words in current utterance
    def get_num_words(self):
        num_words = 0
        for phrase in self.phrases:
            num_words += phrase.get_num_words()
        return num_words


    ##### Get total phrases in current utterance
    def get_num_phrases(self):
        return len(self.phrases)


    ##### Create label and save in label attribute
    # Loop through the utterance (phrase, word, phoneme by order)
    # to create destination label
    def create_label(self):
        for phrase_index, phrase in enumerate(self.phrases):
            for word_index, word in enumerate(phrase.words):
                for phoneme_index, phoneme in enumerate(word.phonemes):
                    p1  = word.get_before_pre_phoneme(phoneme_index) if (not word.is_silent_phoneme(phoneme_index) and word.get_pre_phoneme(phoneme_index) !=  word.SILENT_PHONEME) or word_index else word.SILENT_PHONEME #duy mod
                    p2  = word.get_pre_phoneme(phoneme_index) if (not word.is_silent_phoneme(phoneme_index) or word_index) else word.SILENT_PHONEME #duy mod
                    p3  = phoneme
                    p4  = word.get_next_phoneme(phoneme_index) if (not word.is_silent_phoneme(phoneme_index) or not word_index) else word.SILENT_PHONEME #duy mod
                    p5  = word.get_after_next_phoneme(phoneme_index) if (not word.is_silent_phoneme(phoneme_index) and word.get_next_phoneme(phoneme_index) !=  word.SILENT_PHONEME) or not word_index else word.SILENT_PHONEME #duy mod
                    p6  = phoneme_index if not word.is_silent_phoneme(phoneme_index) else 'x'
                    p7  = word.num_phomemes - phoneme_index - 1 if not word.is_silent_phoneme(phoneme_index) else 'x'
                    a1  = word.pre_word.tone if word.pre_word and not word.is_silent_phoneme(phoneme_index) else 'x'
                    a2  = word.pre_word.pre_word.tone if word.pre_word and word.pre_word.pre_word and not word.is_silent_phoneme(phoneme_index) else 'x'
                    a3  = len(word.pre_word.phonemes) if word.pre_word and not word.is_silent_phoneme(phoneme_index) else 'x'
                    b1  = word.tone if not word.is_silent_phoneme(phoneme_index) else 'x'
                    b2  = 'x'
                    b3  = word.num_phomemes if not word.is_silent_phoneme(phoneme_index) else 'x'
                    b4  = 0
                    b5  = 0
                    b6  = word_index if not word.is_silent_phoneme(phoneme_index) else 'x'
                    b7  = len(phrase.words) - word_index - 1 if not word.is_silent_phoneme(phoneme_index) else 'x'
                    b8  = word.punctuation if not word.is_silent_phoneme(phoneme_index) else 'x' #duy mod
                    b9  = word.next_word.punctuation if word.next_word else 'x'
                    b10 = word.next_word.next_word.punctuation if word.next_word and word.next_word.next_word else 'x'
                    b11 = word.pre_word.punctuation if word.pre_word else 'x'
                    b12 = word.pre_word.pre_word.punctuation if word.pre_word and word.pre_word.pre_word else 'x'
                    b13 = 'x'
                    b14 = 'x'
                    b15 = 'x'
                    b16 = word.vowel
                    c1  = word.next_word.tone if word.next_word else 'x'
                    c2  = word.next_word.next_word.tone if word.next_word and word.next_word.next_word else 'x'
                    c3  = len(word.next_word.phonemes) if word.next_word else 'x'
                    d1  = 'x'
                    d2  = 1 if word.pre_word else 'x'
                    e1  = 'x'
                    e2  = 1
                    e3  = b6
                    e4  = b7
                    e5  = 'x'
                    e6  = 'x'
                    e7  = 'x'
                    e8  = 'x'
                    f1  = 'x'
                    f2  = 1 if word.next_word else 'x'
                    g1  = len(phrase.pre_phrase.words) if phrase.pre_phrase else 'x'
                    g2  = g1
                    h1  = len(phrase.words)
                    h2  = h1
                    h3  = phrase_index
                    h4  = len(self.phrases) - phrase_index - 1
                    h5  = 'x'
                    i1  = len(phrase.next_phrase.words) if phrase.next_phrase else 'x'
                    i2  = i1
                    j1  = self.get_num_words()
                    j2  = j1
                    j3  = self.get_num_phrases()

                    label = self.LABEL_FORMAT.format(p1, p2, p3, p4, p5, p6, p7, a1, a2, a3, b1, b2, b3,
                                                     b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15,
                                                     b16, c1, c2, c3, d1, d2, e1, e2, e3, e4, e5, e6, e7,
                                                     e8, f1, f2, g1, g2, h1, h2, h3, h4, h5, i1, i2, j1, j2, j3)
                    self.label += label
                    self.label += '\n'
        self.label = self.label[:-1] # duy mod

class Phrase:
    """
    A class represents for phrase, phrase is child of utterance

    Atributes:
        - words: list of words of current phrase
        - pre_phrase: previous phrase in current utterance
        - next_phrase: next phrase in current utterance
    """

    ##### Init method
    # We'll init list of word from initial data and then
    # init linked list between words for traveling between them
    # @params:
    #   - data: list of words
    #   > [['x', 'w', 'ie', 'n', '_5'], ['m', 'a', 'ji', '_3']]
    #   - is_first_phrase: determine if current phrase is first phrase
    #   - is_last_phrase: determine if current phrase is last phrase
    def __init__(self, data, is_first_phrase=False, is_last_phrase=False):
        self.pre_phrase     = None
        self.next_phrase    = None
        self.words          = []

        for index, word in enumerate(data):
            if len(data) == 1:
                new_words = Word(word, is_first_word=True, is_last_word=True)
            if is_first_phrase and index == 0:
                new_words = Word(word, is_first_word=True)
            elif is_last_phrase and index == len(data) - 1:
                new_words = Word(word, is_last_word=True)
            else:
                new_words = Word(word)
            self.words.append(new_words)

    ##### Init linked list between words
    def init_words(self):
        for index, word in enumerate(self.words):
            if index != 0:
                word.pre_word = self.words[index-1]
            else:
                if self.pre_phrase:
                    word.pre_word = self.pre_phrase.get_last_word_in_phrase()
                else:
                    word.pre_word = None
            if index + 1 < len(self.words):
                word.next_word = self.words[index+1]
            else:
                if self.next_phrase:
                    word.next_word = self.next_phrase.get_first_word_in_phrase()
                else:
                    word.next_word = None


    ##### Get total words of current phrase
    def get_num_words(self):
        return len(self.words)


    ##### Get first word of current phrase
    def get_first_word_in_phrase(self):
        return self.words[0]


    ##### Get last word of current phrase
    def get_last_word_in_phrase(self):
        return self.words[-1]


class Word:
    """
    A class represents for word, word is child of phrase

    Atributes:
        - phonemes: list of phonemes of current word
        - pre_word: previous word in current phrase or previous phrase
        - next_word: next word in current phrase or next phrase
        - tone: tone of current word
        - vowel: vowel identify in current word
        - punctuation: punctuation following current word
    """

    VOWEL_LIST              = ['u', 'W', 'o', 'oU', 'oUs', 'O', 'Os', 'i', 'e', 'E', 'Es', 'a', 'as']
    TONE_LIST               = ['_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8']
    SILENT_PHONEME          = 'sil'

    ##### Init method
    # @params:
    #   - data: list of phoneme and the last element is tone
    #   > ['x', 'w', 'ie', 'n', '_5']
    def __init__(self, data, is_first_word=False, is_last_word=False):
        self.pre_word       = None
        self.next_word      = None
        self.phonemes       = []
        self.tone           = None
        self.vowel          = 'x'
        self.punctuation    = 'n'	# duy mod
        self.num_phomemes   = 0

        
        if is_first_word:
            self.phonemes.append(self.SILENT_PHONEME)

        for item in data:
            if item in self.VOWEL_LIST:
                self.vowel = item
                self.phonemes.append(item)
            elif item in self.TONE_LIST:
                self.tone = item[1:] # duy mod
            else:
                self.phonemes.append(item)

        if is_last_word:
            self.phonemes.append(self.SILENT_PHONEME)
        
        # Set num_phomemes properties
        self.num_phomemes = len([phoneme for phoneme in self.phonemes if phoneme != self.SILENT_PHONEME])


    ##### Get phoneme based on index in list phoneme of current word
    def get_phoneme(self, phoneme_index):
        try:
            phoneme = self.phonemes[phoneme_index]
            return phoneme
        except IndexError:
            return 'x'


    ##### Get phoneme before previous phoneme based on
    # current phoneme index in list phoneme of current word
    def get_before_pre_phoneme(self, phoneme_index):
        if phoneme_index > 1:
            return self.phonemes[phoneme_index-2]
        # If out of range in current word then search on previous word
        elif phoneme_index == 1 and self.pre_word:
            return self.pre_word.get_phoneme(-1)
        elif phoneme_index == 0 and self.pre_word:
            return self.pre_word.get_phoneme(-2)
        else:
            return 'x'


    ##### Get previous phoneme based on index in list
    # phoneme of current word
    def get_pre_phoneme(self, phoneme_index):
        if phoneme_index > 0:
            return self.phonemes[phoneme_index-1]
        # If out of range in current word then search on previous word
        elif phoneme_index == 0 and self.pre_word:
            return self.pre_word.get_phoneme(-1)
        else:
            return 'x'


    ##### Get next phoneme based on index of current phoneme index in list
    # phoneme of current word
    def get_next_phoneme(self, phoneme_index):
        if phoneme_index < len(self.phonemes) - 1:
            return self.phonemes[phoneme_index+1]
        # If out of range in current word then search on next word
        elif phoneme_index == len(self.phonemes) - 1 and self.next_word:
            return self.next_word.get_phoneme(0)
        else:
            return 'x'


    ##### Get phoeneme after next phoneme based on index of
    # current phoneme in list phoneme of current word
    def get_after_next_phoneme(self, phoneme_index):
        if phoneme_index < len(self.phonemes) - 2:
            return self.phonemes[phoneme_index+2] # duy mod
        # If out of range in current word then search on next word
        elif phoneme_index == len(self.phonemes) - 2 and self.next_word:
            return self.next_word.get_phoneme(0)
        elif phoneme_index == len(self.phonemes) - 1 and self.next_word:
            return self.next_word.get_phoneme(1)
        else:
            return 'x'


    #### Determine if given phoneme is silent or not
    def is_silent_phoneme(self, phoneme_index):
        if self.get_phoneme(phoneme_index) == self.SILENT_PHONEME:
            return True
        return False


    #### Determine if word contains silent phoneme
    def has_silent_phomeme(self):
        if self.SILENT_PHONEME in self.phonemes:
            return True
        return False
