import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("darkgrid")

# states 121
environment_rows = 11
environment_columns = 11

episodes = 1000

cummulative_rewards=[]

q_values = np.zeros((environment_rows, environment_columns, 4))

# ACTIONS : 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

# REWARDS
rewards = np.full((environment_rows, environment_columns), -100.)
rewards[0, 5] = 100. #reward for the GOAL is 100

#define aisle locations (i.e., white squares) for rows 1 through 9
aisles = {} #store locations in a dictionary
# aisles[1] = [i for i in range(1, 10)]
aisles[1] = [i for i in range(1, 8)]
aisles[1].append(9)
aisles[2] = [1, 7, 9]
aisles[3] = [i for i in range(1, 8)]
aisles[3].append(9)
aisles[4] = [3, 7]
aisles[5] = [i for i in range(11)]
aisles[6] = [5]
aisles[7] = [i for i in range(1, 10)]
aisles[8] = [3, 7]
# aisles[8] = []
aisles[9] = [i for i in range(11)]

#set the rewards for all aisle locations (i.e., white squares)
for row_index in range(1, 10):
  for column_index in aisles[row_index]:
    rewards[row_index, column_index] = -1.


# for row in rewards:
#   print(row)


def is_terminal_state(current_row_index, current_column_index):
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True


def get_starting_location():
  #get a random row and column index
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  #continue choosing random row and column indexes until a non-terminal state is identified
  #(i.e., until the chosen state is a 'white square').
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index


def get_next_action(current_row_index, current_column_index, epsilon):
  #if a randomly chosen value between 0 and 1 is greater than epsilon,
  #then choose the most promising value from the Q-table for this state.
  if np.random.random() > epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else: #choose a random action
    return np.random.randint(4)

#define a function that will get the next location based on the chosen action
def get_next_location(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index

#Define a function that will get the shortest path between any location within the warehouse that
#the robot is allowed to travel and the item packaging location.
def get_shortest_path(start_row_index:int, start_column_index:int):
  #return immediately if this is an invalid starting location
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else: #if this is a 'legal' starting location
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    #continue moving along the path until we reach the goal (i.e., the item packaging location)
    while not is_terminal_state(current_row_index, current_column_index):
      #get the best action to take
      action_index = get_next_action(current_row_index, current_column_index, 0.)
      #move to the next location on the path, and add the new location to the list
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      if [current_row_index, current_column_index] in shortest_path:
        return "BOUNDED"
      
      shortest_path.append([current_row_index, current_column_index])
    
    return shortest_path
  

def train():
  #define training parameters
  epsilon = 0.1
  discount_factor = 0.9
  learning_rate = 0.9

  for episode in range(episodes):
    row_index, column_index = get_starting_location()
    
    while not is_terminal_state(row_index, column_index):
      action_index = get_next_action(row_index, column_index, epsilon)

      old_row_index, old_column_index = row_index, column_index 
      row_index, column_index = get_next_location(row_index, column_index, action_index)

      reward = rewards[row_index, column_index]
      old_q_value = q_values[old_row_index, old_column_index, action_index]
      temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

      new_q_value = old_q_value + (learning_rate * temporal_difference)
      q_values[old_row_index, old_column_index, action_index] = new_q_value
    x=np.sum(q_values)
    cummulative_rewards.append(x)

  print('Training complete!')


# FOR GUI ===============================================================
def get_path(a,b):
    return get_shortest_path(a,b)

def get_grid():
  grid = []
  for rows in rewards:
    x=[]
    for cols in rows:
      if(cols == -100):
        x.append(1)
      elif(cols == -1):
        x.append(0)
      else:
        x.append(2)
    grid.append(x)
  return grid 

# train()
# print(q_values)

# plt.plot(range(1000), cummulative_rewards)
# ax = sns.lineplot(x = range(episodes), y = cummulative_rewards)

# minimum_value_index = np.argmin(cummulative_rewards)
# maximum_value_index = max(cummulative_rewards[minimum_value_index :])
# maximum_value_episode = np.argmax(cummulative_rewards[minimum_value_index :])+ len(cummulative_rewards[:minimum_value_index])

# ax.axvline(x = minimum_value_index ,   
#               ymin = 0, 
#               ymax = 1, 
#               color = 'r')
# plt.text(minimum_value_index+10, 0, f'x = {minimum_value_index}', color='r', fontsize=12)


# ax.axhline(y = maximum_value_index ,      
#             xmin = 0,
#             xmax = 1, 
#             color = 'g')
# plt.text(900, maximum_value_index+100, f'y = {maximum_value_index:.2f} for episode {maximum_value_episode}', color='g', fontsize=12)

# plt.show()


# examples of a few shortest paths
# print(get_shortest_path(3, 9)) #starting at row 3, column 9
# print(get_shortest_path(5, 0)) #starting at row 5, column 0
# print(get_shortest_path(9, 5)) #starting at row 9, column 5

# example of reversed shortest path
# path = get_shortest_path(5, 2) #go to row 5, column 2
# path.reverse()
# print(path)