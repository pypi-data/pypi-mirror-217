from mathtext.answer_checkers import check_answer_type
from collections import Counter
from mathtext.nlutils import (
    extract_nums_tokens,
    is_int, 
    text2num,
    text2time,
    text2text,
    text2exponent,
    text2fraction,
    text2symbol,
    text2equation,
    )
from mathtext.constants import TOKENS2INT_ERROR_INT
from unidecode import unidecode
import re
from mathtext.tokenizers import tokenize_words as tokenize
from mathtext.text2int_so import text2int, text2float

import logging
log = logging.getLogger(__name__)


# Change this according to what words should be corrected to
SPELL_CORRECT_MIN_CHAR_DIFF = 2

ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]

CHAR_MAPPING = {
    "-": " ",
    "_": " ",
    "and": " ",
    ",": "",
}

TOKEN_MAPPING = {
    "and": " ",
    "oh": "0",
}

NUMBERS = [
    'hundred', 'thousand', 'million', 'trillion', 'twenty',
    'thirty', 'fourty', 'fifty', 'sixty', 'seventy',
    'eighty', 'ninety', 'one', 'two', 'three', 'four', 'five',
    'six', 'seven', 'eight', 'nine', 'zero', 'eleven',
    'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen', 'nineteen'
]

WORDS = Counter(NUMBERS)


def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N


def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)


def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def find_char_diff(a, b):
    # Finds the character difference between two str objects by counting the occurrences of every character. Not edit distance.
    char_counts_a = {}
    char_counts_b = {}
    for char in a:
        if char in char_counts_a.keys():
            char_counts_a[char] += 1
        else:
            char_counts_a[char] = 1
    for char in b:
        if char in char_counts_b.keys():
            char_counts_b[char] += 1
        else:
            char_counts_b[char] = 1
    char_diff = 0
    for i in char_counts_a:
        if i in char_counts_b.keys():
            char_diff += abs(char_counts_a[i] - char_counts_b[i])
        else:
            char_diff += char_counts_a[i]
    return char_diff


def text2float_or_int(text):
    """ Return a float or an integer based on the text

    >>> text2float_or_int("1.2")
    1.2
    >>> text2float_or_int("1")
    1

    NOTE: 1.0 > 1 , not 1.0
    """
    try:
        value = float(text)
    except ValueError:
        return TOKENS2INT_ERROR_INT

    if is_int(value):
        return int(value)
    return value


def text2numtexts(text):
    """ Create a list of intergers or floating point values

    >>> text2numtexts("2, 3")
    [2, 3]
    >>> text2numtexts("15;13")
    [32202]
    >>> text2numtexts("0.1.2")
    [32202]
    >>> text2numtexts(",9")
    [9]

    FIX: text2int recognizes '' as 0 - needs to throw errors more often when something isn't a valid number
    """
    nums_tokens = extract_nums_tokens(text)
    nums = []
    for x in nums_tokens:
        nums.append(text2int(" ".join(x)))
    return nums


def text2nums(text):
    nums = []
    for s in text2numtexts(text):
        nums.append(text2float_or_int(s))
    return nums


def detokenize(tokens):
    return ' '.join(tokens)


def replace_tokens(tokens, token_mapping=TOKEN_MAPPING):
    return [token_mapping.get(tok, tok) for tok in tokens]


def replace_chars(text, char_mapping=CHAR_MAPPING):
    return [char_mapping.get(c, c) for c in text]


def convert_word_to_int(in_word, numwords=None):
    """ Convert a single word (str) into a single int

    >>> convert_word_to_int("eleven hundred")
    """
    teens = {
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19
    }

    tens = ["", "", "twenty", "thirty", "forty",
            "fifty", "sixty", "seventy", "eighty", "ninety"]
    scales = ["hundred", "thousand", "million", "billion", "trillion"]
    if not numwords:
        numwords = dict(teens)
        for idx, word in enumerate(ONES):
            numwords[word] = idx
        for idx, word in enumerate(tens):
            numwords[word] = idx * 10
        for idx, word in enumerate(scales):
            numwords[word] = 10 ** (idx * 3 or 2)
    if in_word in numwords:
        # print(in_word)
        # print(numwords[in_word])
        return numwords[in_word]
    try:
        int(in_word)
        return int(in_word)
    except ValueError:
        pass
    corrected_word = correction(in_word)
    if corrected_word in numwords:
        return numwords[corrected_word]
    # print(f'{in_word}=>corrected=>{corrected_word} not in numwords')
    if in_word in numwords:
        return numwords[in_word]
    # print(f'{in_word} not in numwords')
    return TOKENS2INT_ERROR_INT


def tokens2int(tokens):
    # Takes a list of tokens and returns a int representation of them
    if tokens == TOKENS2INT_ERROR_INT:
        return TOKENS2INT_ERROR_INT
    types = []
    for i in tokens:
        if i <= 9:
            types.append(1)

        elif i <= 90:
            types.append(2)

        else:
            types.append(3)
    if len(tokens) <= 3:
        current = 0
        for i, number in enumerate(tokens):
            if i != 0 and types[i] < types[i - 1] and current != tokens[i - 1] and types[i - 1] != 3:
                current += tokens[i] + tokens[i - 1]
            elif current <= tokens[i] and current != 0:
                current *= tokens[i]
            elif 3 not in types and 1 not in types:
                current = int(''.join(str(i) for i in tokens))
                break
            elif '111' in ''.join(str(i) for i in types) and 2 not in types and 3 not in types:
                current = int(''.join(str(i) for i in tokens))
                break
            else:
                current += number

    elif 3 not in types and 2 not in types:
        current = int(''.join(str(i) for i in tokens))

    else:
        count = 0
        current = 0
        for i, token in enumerate(tokens):
            count += 1
            if count == 2:
                if types[i - 1] == types[i]:
                    current += int(str(token) + str(tokens[i - 1]))
                elif types[i - 1] > types[i]:
                    current += tokens[i - 1] + token
                else:
                    current += tokens[i - 1] * token
                count = 0
            elif i == len(tokens) - 1:
                current += token

    return current


def check_expected_answer_validity(expected_answer):
    """ Ensures that the expected_answer is a string or returns error code """
    # TODO: Is this necessary anymore?
    # TODO: Why are there two?
    if not isinstance(expected_answer, str) or not isinstance(expected_answer, str):
        try:
            expected_answer = str(expected_answer)
        except:
            return TOKENS2INT_ERROR_INT
    return expected_answer


# TODO: Is it okay to use tokenize here?
# ... this tokenize() contributed to the slowdown earlier?
def extract_converted_tokens(extracted_tokens):
    """ Attempts to consolidate the first group of numbers into a single number

    Returns the first number

    >>> extract_converted_tokens([['ninety', 'nine', 'hundred'], ['seventy', 'seven']])
    ['199']
    >>> extract_converted_tokens([['8']])
    ['8']
    >>> extract_converted_tokens([['20'], ['45']])
    ['20']
    """
    converted_toks = []
    extracted_token = []

    for tok_list in extracted_tokens:
        for tok in tok_list:
            # NOTE: tokenize() was called twice here
            # NOTE2: This expects [['1'],['2']], not [['1', '2']]
            try:
                tokenized_tok = tokenize(tok)[0]
            except:
                tokenized_tok = None

            if tokenized_tok:
                converted_toks.append(tokenized_tok)
            else:
                converted_toks.append(tok)
        if converted_toks:
            try:
                extracted_token.append(str(sum(x for x in converted_toks)))
            except TypeError:
                extracted_token.append(converted_toks[0])
            break
    return extracted_token


def has_unicode_characters(text):
    unicode_characters = re.compile(r'[\u0080-\uFFFF]')
    if unicode_characters.search(text):
        return True
    return False


def convert_non_superscript_unicode(text):
    """ Convert unicode characters to regular string characters

    Does not convert superscript because that will happen in text2exponents if an exponent answer
    """
    superscript_list = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    decoded_text = ""
    try:
        for char in text:
            if char in superscript_list:
                decoded_text += char
            else:
                decoded_text += unidecode(char)
    except TypeError:
        pass

    text = decoded_text
    return text


answer_evaluation_functions = {
    'exponent': text2exponent,
    'fraction': text2fraction,
    'text': text2text,
    'time': text2time,
    'symbol': text2symbol,
    'equation': text2equation,
}


def extract_and_convert_a_num_tok(text):
    extracted_tokens = extract_nums_tokens(text)

    try:
        extracted_tokens = extracted_tokens[0]
    except:
        extracted_tokens
    return extract_converted_tokens(extracted_tokens)


def format_answer_to_expected_answer_type(text, expected_answer=None):
    """ 
    >>> format_answer_to_expected_answer_type("Y", "Yes")
    "Yes"
    >>> format_answer_to_expected_answer_type("yes", "T")
    "T"
    >>> format_answer_to_expected_answer_type("1 / 2", "1/2")
    """
    expected_answer = check_expected_answer_validity(expected_answer)
    answer_type = check_answer_type(expected_answer)

    has_unicode = has_unicode_characters(text)

    if has_unicode:
        text = convert_non_superscript_unicode(text)

    if answer_type == "other":
        return TOKENS2INT_ERROR_INT

    eval_function = answer_evaluation_functions[answer_type]
    result = eval_function(text, expected_answer)
    if result != TOKENS2INT_ERROR_INT:
        return result
    return TOKENS2INT_ERROR_INT


def format_int_or_float_answer(text):
    """ Attempts to convert a student message into an int or float

    >>> format_int_or_float_answer("12")
    12
    >>> format_int_or_float_answer("maybe 0.5")
    0.5
    >>> format_int_or_float_answer("I don't know")
    32202
    >>> format_int_of_float_answer("¹1")
    32202
    """
    try:
        num = text2num(text)
        if num != TOKENS2INT_ERROR_INT:
            return num

        result = text2float(text)
        if result and result != None:
            return result

        result = text2int(text)
        if result and result != 0:
            return result
    except ValueError:
        log.exception("ValueError")
    except Exception:
        log.exception("Exception")
    return TOKENS2INT_ERROR_INT


def convert_text_to_answer_format(text, expected_answer=None):
    """ Attempts to convert a message to a text answer or float/int answer

    Used for testing in test_cases_all.py 
    """
    result = format_answer_to_expected_answer_type(text, expected_answer)
    if result != TOKENS2INT_ERROR_INT:
        return result

    return format_int_or_float_answer(text)
