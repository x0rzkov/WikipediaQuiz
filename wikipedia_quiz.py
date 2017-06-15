"""
Wikipedia Quiz
Are you able to pick out the correct wikipedia article based on a small passage
of text pulled from it? What if it's multiple choice?
Written by Nicholas Moser. NicholasMoser56@gmail.com www.github.com/NicholasMoser
"""
from builtins import input
import sys
import getopt
import wikipedia
import random

NUMBER_OF_ARTICLES_DEFAULT = 5
PASSAGE_LENGTH_DEFAULT = 64

def main():
    number_of_articles, passage_length = handle_args()
    wikipedia_quiz(number_of_articles, passage_length)

def wikipedia_quiz(number_of_articles, passage_length):
    """Generates a multiple choice quiz to identify the correct wikipedia article that
    a random passage is pulled from. The number of articles determines how many choices
    you must pick from. The passage length determines the number of characters that the
    random passage will be. 
    """
    print("*** Wikipedia Quiz ***")
    random_articles = wikipedia.random(number_of_articles)
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
    
    # If title is not allowed in passage, keep generating passages until that is not the case.
    while passage_contains_title(random_passage, correct_article):
        random_passage = retrieve_random_passage(correct_page, passage_length)

    print("...%s..." % random_passage)
    for index, random_articles in enumerate(random_articles):
        print("%d: %s" % (index, random_articles))
        
    answer = request_answer(number_of_articles)
    if answer == str(correct_article_index):
        print("Correct!")
    else:
        print("Incorrect, answer was: %d" % correct_article_index)
    
def handle_args():
    """Handle the command line arguments provided for the program.
    There is an argument for the number of articles to make it configurable.
    There is also an argument for the length of the passage to make it configurable.
    If the argument is not provided it uses the provided default.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:],"n:l:",["numberofarticles=","passagelength="])
    except getopt.GetoptError:
        print('wikipedia_quiz.py -n <numberofarticles> -l <passagelength>')
        sys.exit(2)
    number_of_articles = NUMBER_OF_ARTICLES_DEFAULT
    passage_length = PASSAGE_LENGTH_DEFAULT
    for opt, arg in opts:
        if opt in ("-n", "--numberofarticles"):
            number_of_articles = int(arg)
        elif opt in ("-l", "--passagelength"):
            passage_length = int(arg)
    return number_of_articles, passage_length
    
def retrieve_random_passage(page, length):
    """Given a wikipedia page and length, retrieves a random passage of text from
    the content of the wikipedia page with the given length.
    """
    content = page.content
    start = random.randrange(len(content) - length)
    end = start + length
    return content[start:end]

def passage_contains_title(passage, title):
    """Given a passage of text and title, returns true if any of the words of
    the title are found in the passage of text.
    """
    return True if [x for x in title.split() if x in passage] else False 
    
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
            print("Not valid selection...")
    
if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)