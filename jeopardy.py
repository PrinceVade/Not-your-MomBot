# Hunter Graves
# 19/02/2021
# jeopardy.py

# Jeopardy game that returns a specific jeopardy board
# and plays them out appropriately. Includes Final Jeopardy!

import json
import random

# generateRounds contract here
def generateRounds():
    
    # load the data from the JSON
    with open('JEOPARDY_QUESTIONS.json') as f:
        data = json.load(f)
    
    trimmedData = [(q['category'],q['value'],q['round'],q['question'],q['answer'],q['show_number']) for q in data]
    
    # grab a random show number to pull questions from
    showNumber = random.choice([q[5] for q in trimmedData])
    return [q for q in trimmedData if q[5] == showNumber]

# retrieve all the questions for the game
allQuestions = generateRounds()

# separate all of the questions into their respective categories
firstQuestions = [q for q in allQuestions if q[2] == 'Jeopardy!']
secondQuestions = [q for q in allQuestions if q[2] == 'Double Jeopardy!']
finalQuestion = [q for q in allQuestions if q[2] == 'Final Jeopardy!'][0]

return (firstQuestions, secondQuestions,finalQuestion)