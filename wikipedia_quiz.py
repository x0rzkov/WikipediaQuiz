"""
Wikipedia Quiz
Are you able to pick out the correct wikipedia article based on a small passage
of text pulled from it? What if it's multiple choice?
Written by Nicholas Moser. NicholasMoser56@gmail.com www.github.com/NicholasMoser
"""
from __future__ import division
from builtins import input
import sys
import re
import getopt
import random
import logging
import wikipedia

# Default number of articles for the quiz if no command line argument given
NUMBER_OF_ARTICLES_DEFAULT = 5

# Default length of the passage for the quiz if no command line argument given
PASSAGE_LENGTH_DEFAULT = 64

# Maximum percent of whitespace allowed in a passage
WHITE_SPACE_PERCENT_ALLOWED = .30

def main():
    logging.basicConfig(filename='info.log',level=logging.DEBUG)
    number_of_articles, passage_length = handle_args()
    wikipedia_quiz(number_of_articles, passage_length)

def wikipedia_quiz(number_of_articles, passage_length):
    """Generates a multiple choice quiz to identify the correct wikipedia article that
    a random passage is pulled from. The number of articles determines how many choices
    you must pick from. The passage length determines the number of characters that the
    random passage will be. 
    """
    print('*** Wikipedia Quiz ***')
    logging.info('Quiz is starting')
    random_articles = wikipedia.random(number_of_articles)
    logging.debug('Random articles: %s' % str(random_articles).encode('utf-8'))
    correct_article_index = random.randrange(number_of_articles)
    page_retrieved = False
    while not page_retrieved:
        try:
            correct_article = random_articles[correct_article_index]
            correct_page = wikipedia.page(correct_article)
            page_retrieved = True
        except wikipedia.exceptions.DisambiguationError as e:
            # Wikipedia provides options to choose from, but if we pick one, the title will be 
            # much more descriptive (particularly by using parenthesis like so). This usually
            # ends up making the guessing too easy. Let's just reroll and put the new random 
            # article in the place of the old one.
            new_random_article = wikipedia.random()
            random_articles[correct_article_index] = new_random_article
            
    random_passage = retrieve_random_passage(correct_page, passage_length)
    
    while is_passage_unfair(random_passage, correct_article):
        logging.info('Passage is unfair, generating a new one...')
        random_passage = retrieve_random_passage(correct_page, passage_length)

    print('...%s...' % random_passage)
    
    encodeUTF8 = sys.version_info.major == 2 # Hack support for Python 2
    for index, random_article in enumerate(random_articles):
        if encodeUTF8:
            random_article = random_article.encode('utf-8')
        print('%d: %s' % (index, random_article))
        
    answer = request_answer(number_of_articles)
    if answer == str(correct_article_index):
        print('Correct!')
        logging.info('Correct, answer was %d' % correct_article_index)
    else:
        print('Incorrect, answer was: %d' % correct_article_index)
        logging.info('Incorrect, answer was: %d' % correct_article_index)
    logging.info('Quiz is ending')
    
def retrieve_random_passage(page, length):
    """Given a wikipedia page and length, retrieves a random passage of text from
    the content of the wikipedia page with the given length.
    """
    content = page.content
    start = random.randrange(len(content) - length)
    end = start + length
    return content[start:end]
    
def is_passage_unfair(passage, title):
    """Checks if a passage is unfair or not. This means it is either unfair to the player in being
    too hard, or unfair to the quiz by being too easy. The particular things that it checks is that
    the passage does not contain any words of the article title or that there is too much white
    space in the passage.
    """
    return passage_contains_title(passage, title) or has_too_much_whitespace(passage)

def has_too_much_whitespace(passage):
    """Given a passage of text, returns true if there is too much whitespace in it. The amount
    allowed is defined by a global constant (lol).
    """
    length = len(passage)
    length_without_whitespace = len(re.sub('[\s+]', '', passage))
    whitespace = length - length_without_whitespace
    percent_whitespace = whitespace / length
    too_much_whitespace = percent_whitespace >= WHITE_SPACE_PERCENT_ALLOWED
    logging.debug('Passage length: %d; Whitespace: %d' % (length, whitespace))
    if too_much_whitespace:
        logging.debug('Too much whitespace for this passage')
    return too_much_whitespace
    
def passage_contains_title(passage, title):
    """Given a passage of text and title, returns true if any of the words of
    the title are found in the passage of text.
    """
    title_words_in_passage = [x for x in title.split() if x in passage]
    if title_words_in_passage:
        logging.debug('Passage contains word(s) from title: %s' % str(title_words_in_passage).encode('utf-8'))
    return True if title_words_in_passage else False
    
def request_answer(number_of_articles):
    """Asks the user to provide an answer to the quiz. The answer must be
    an integer that is within the range of the number of articles or else the user
    will be asked again.
    """
    valid_answer = False
    while not valid_answer:
        answer = input('Please select your answer: ')
        if answer in ''.join(str(e) for e in range(number_of_articles)):
            valid_answer = True
        else:
            print('Not valid selection...')
    logging.info('Answer retrieved from user')
    return answer
    
def handle_args():
    """Handle the command line arguments provided for the program.
    There is an argument for the number of articles to make it configurable.
    There is also an argument for the length of the passage to make it configurable.
    If the argument is not provided it uses the provided default.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:],'n:l:',['numberofarticles=','passagelength='])
    except getopt.GetoptError:
        print('wikipedia_quiz.py -n <numberofarticles> -l <passagelength>')
        logging.error('Opt error encountered')
        sys.exit(2)
    number_of_articles = NUMBER_OF_ARTICLES_DEFAULT
    passage_length = PASSAGE_LENGTH_DEFAULT
    for opt, arg in opts:
        if opt in ('-n', '--numberofarticles'):
            number_of_articles = int(arg)
            logging.info('Number of articles parameter found')
        elif opt in ('-l', '--passagelength'):
            passage_length = int(arg)
            logging.info('Passage length parameter found')
    return number_of_articles, passage_length
    
if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)