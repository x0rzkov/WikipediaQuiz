"""
Wikipedia Quiz
Are you able to pick out the correct wikipedia article based on a small passage
of text pulled from it? What if it's multiple choice?
Written by Nicholas Moser. NicholasMoser56@gmail.com www.github.com/NicholasMoser
"""
from builtins import input
import sys
import wikipedia
import random

NUMBER_OF_ARTICLES_DEFAULT = 5
PASSAGE_LENGTH_DEFAULT = 64
ALLOW_TITLE_IN_PASSAGE_DEFAULT = False

def wikipedia_quiz(number_of_articles, passage_length, allow_title_in_passage):
    """Generates a multiple choice quiz to identify the correct wikipedia article that
    a random passage is pulled from. The number of articles determines how many choices
    you must pick from. The passage length determines the number of characters that the
    random passage will be. You also can decide whether or not to prevent the random
    passage from containing any words from the title of the article.
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
    if not allow_title_in_passage:
        while passage_contains_title(random_passage, correct_article):
            random_passage = retrieve_random_passage(correct_page, passage_length)

    print(random_passage)
    for index, random_articles in enumerate(random_articles):
        print("%d: %s" % (index, random_articles))
        
    answer = request_answer(number_of_articles)
    if answer == str(correct_article_index):
        print("Correct!")
    else:
        print("Incorrect, answer was: %d" % correct_article_index)
    
def retrieve_random_passage(page, length):
    """Given a wikipedia page and length, retrieves a random passage of text from
    the content of the wikipedia page with the given length.
    """
    content = page.content
    start = random.randrange(len(content) - length)
    end = start + length
    return content[start:end]
    #return "...%s..." % passage

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
    wikipedia_quiz(NUMBER_OF_ARTICLES_DEFAULT, PASSAGE_LENGTH_DEFAULT, ALLOW_TITLE_IN_PASSAGE_DEFAULT)