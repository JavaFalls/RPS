import tensorflow as tf
from tensorflow import keras
import numpy as np
import copy
import easygui as eg
import sys

class DataEntry(object):
    def __init__(self):
        self.user_choice = 0
        self.ai_choice   = 0

def test():
    print("Enter your choice: ", end='')
    choice = int(input())
    return choice

def parse_single_result(result):
    x = result.item(0)
    return int(x)

def response(choice):
    response = 0
    response = (choice % 3) + 1
    return response


def parse_result(result):
    answer = DataEntry()
    data = []
    entry = DataEntry()
    num = 1

    for x in np.nditer(result):
        entry = DataEntry()
        entry.user_choice = num
        entry.ai_choice = x
        data.append(entry)
        if (num > 1) and (data[num-2].ai_choice < data[num-1].ai_choice):
            print(str(data[num-2].ai_choice) + " is less than " + str(data[num-1].ai_choice))
            answer = entry
        elif num == 1:
            answer = entry
        num +=1
        print("Choice: " + str(entry.user_choice) + ", Probable answer: " + str(entry.ai_choice))
        print("Most probable: " + str(answer.user_choice))
    return answer.user_choice

def process_choice(model, curr_round, entries):
    choice = [[entry.user_choice]]
    decision = model.predict(choice, batch_size=1, verbose=0)
    decision = parse_single_result(decision)
    start_from = curr_round-6
    if (start_from < 0):
       start_from = 0
    if curr_round > 0:
        for x in range(start_from,curr_round):
           model.fit([[entries[x-1].user_choice]], [[entries[x].user_choice]], epochs=100, verbose=0)
    return decision

def build_model():
   model = keras.Sequential([keras.layers.Dense(1, activation=tf.nn.relu, input_shape=(1,)),
   keras.layers.Dense(6, activation=tf.nn.relu),
   keras.layers.Dense(6, activation=tf.nn.relu),
   keras.layers.Dense(1)
   ])

   optimizer = tf.train.RMSPropOptimizer(0.01)
   model.compile(loss='mse',
                 optimizer=optimizer,
                 metrics=['mae'])
   return model

def gui(wins, ties, losses, last_play):
   choice = 0
   message = ("\t\tWins: " + str(wins) + " Ties: " + str(ties) + " Losses: " + str(losses) + "\n\n" + last_play)
   response = eg.buttonbox(message, choices=["Rock", "Paper", "Scissors"], title="Java Falls: Rock, Paper, Scissors")
   if response == "Rock":
      choice = 1
   elif response == "Paper":
      choice = 2
   elif response == "Scissors":
      choice = 3
   else:
      sys.exit(0)
   return choice

data_entries = [] # list containing each data entry
user_input = 0 # current number input by user
data_input = 0 # number of inputs from user
data_model = build_model()

wins = 0
ties = 0
losses = 0
last_play = ""
entry = DataEntry()
entry.user_choice = 2
data_entries.append(entry)
entry.ai_choice = process_choice(data_model, data_input, data_entries)
entry.ai_choice = response(entry.ai_choice)

while entry.user_choice != 4:
   entry = DataEntry()
   entry.user_choice = gui(wins, ties, losses, last_play)
   data_entries.append(entry)
   entry.ai_choice = process_choice(data_model, data_input, data_entries)
   entry.ai_choice = response(entry.ai_choice)

   print("You chose " + str(entry.user_choice) + " vs. " + str(entry.ai_choice) + "\n")
   if (entry.user_choice == 2 and entry.ai_choice == 1):
      last_play = "\t\tPaper beats Rock, You win!"
      wins +=1
   elif (entry.user_choice == 3 and entry.ai_choice == 2):
      last_play = "\t\tScissors beats Paper, You win!"
      wins +=1
   elif (entry.user_choice == 1 and entry.ai_choice == 3):
      last_play = "\t\tRock beats Scissors, You win!"
      wins +=1
   elif (entry.user_choice == 1 and entry.ai_choice == 1):
      last_play = "\t\tRock vs Rock, nobody wins -_-"
      ties +=1
   elif (entry.user_choice == 2 and entry.ai_choice == 2):
      last_play = "\t\tPaper vs Paper, nobody wins -_-"
      ties +=1
   elif (entry.user_choice == 3 and entry.ai_choice == 3):
      last_play = "\t\tScissors vs Scissors, nobody wins -_-"
      ties +=1
   elif (entry.user_choice == 1 and entry.ai_choice == 2):
      last_play = "\t\tRock losses to Paper, I wins ☜( ﾟヮﾟ☜)"
      losses +=1
   elif (entry.user_choice == 2 and entry.ai_choice == 3):
      last_play = "\t\tPaper losses to Scissors, I wins ☜( ﾟヮﾟ☜)"
      losses +=1
   elif (entry.user_choice == 3 and entry.ai_choice == 1):
      last_play = "\t\tScissors losses to Rock, I wins ☜( ﾟヮﾟ☜)"
      losses +=1
   else:
      last_play = "\t\tWait! I wasn't ready . . ."
   data_entries.append(entry)
   data_input += 1
   print("Ties: ", ties ,"Wins: ",wins, "Losses: ",losses)
