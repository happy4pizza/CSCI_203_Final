####################################################
#
#            CSCI 203 Final Project
#                  Spring 2023
#
# William Crosswhite
#
#National Park API Key: F1IaGExQAdMOkMCjbgSIm8ht2dcYCiNJUMfgs6Ou

#Recreation.gov API Key: 922f3ad6-5320-4559-9e34-bbb89a929e6e
####################################################
# Import Libraries
#
from info_read_write import *
import matplotlib.pyplot as plt
import operator
#
####################################################
# CONSTANTS
# DONE - Do not modify.
####################################################

# STATES - a list of the state abbreviations
STATES = ['ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']

# ACTIVITIES - a list of possible NPS activities
ACTIVITIES = ['Guided Tours', 'Hiking', 'Birdwatching', 'Biking', 'Camping', 'Fishing', 'Picnicking']

# OPTIONS - a list of options for the user
OPTIONS = ['Printing NPS units for the state with the most NPS units', 'Plotting top five states with the most NPS units', 'Printing NPS units for the state with the most nps units with a given activity', 'Plotting top five states with the most nps units with a given activity', 'Quit program']


####################################################
# Class Definitions
####################################################

class StateUnits:
  ''' Information about NPS units in a state'''
  
  def __init__(self, state_abbrev):
    ''' DO NOT TOUCH. This is already completed for you.
    The constructor for an instance of the 
        StateUnits class 
    
    Class attributes:
    - state (string): two-letter uppercase state abbreviation
    - unit_list (list): a list of dictionaries
      each dictionary has information on an NPS unit
    - num_units (integer): number of the 
      state's NPS units
    
    Parameters:
    - self (StateUnits class instance)
    - state_abbrev (string): two-letter lowercase
      state abbreviation
    '''
    # Retrieve info from json file
    filepath = "state_park_info/" + state_abbrev + "_parks.json"
    info = load_json_file(filepath)
    # Assign class attributes
    self.state = state_abbrev.upper() 
    self.unit_list = info['data']
    self.num_units = int(info["total"])

  def __str__(self):
    ''' DO NOT TOUCH. This is already completed for you.
    String representation of the StateUnits class
    
    Parameters:
    - self (StateUnits class instance)
    '''
    border = 65 *'-' +'\n'
    s = border
    s += f'{"NPS Units in " + self.state: ^65}\n'
    s += border
    for unit in self.unit_list:
      s += f'{unit["fullName"]: ^65}\n'
    s += border
    return s

  def __eq__(self, other):
    ''' TO DO
    Returns True if the two state have the 
    same number of NPS units.

    Parameters:
    - self (StateUnits class instance)
    - other (StateUnits class instance):
        a StateUnits class instance to be compared with self

    Returns:
    - True (Boolean): both instances have the same number of NPS units
    - False (Boolean): both instances do not have the same number of NPS units
    '''
    if self.num_units == other.num_units:
      return True
    else:
      return False

  def __gt__(self, other):
    ''' TO DO
    Returns True if the instance self has more NPS units than the instance other

    Parameters:
    - self (StateUnits class instance)
    - other (StateUnits class instance):
        a StateUnits class instance to be compared with self

    Returns:
    - True (Boolean): the instance self has more NPS units than the instance other
    - False (Boolean): the instance self has equal or less NPS units than the instance other
    '''
    if self.num_units > other.num_units:
      return True
    else:
      return False

  def __lt__(self, other):
    ''' TO DO
    Returns True if the instance self has less NPS units than the instance other

    Parameters:
    - self (StateUnits class instance)
    - other (StateUnits class instance):
        a StateUnits class instance to be compared with self

    Returns:
    - True (Boolean): the instance self has less NPS units than the instance other
    - False (Boolean): the instance self has equal or more NPS units than the instance other
    '''
    if self.num_units < other.num_units:
      return True
    else:
      return False

    
class ActivityUnits(StateUnits):

  def __init__(self, state_abbrev, desired_activity):
    ''' TO DO
    The constructor for an ActivityUnits class instance
      - a child of the StateUnits class
    
    Class attributes:
    - activity (string): user's desired activity
    - state (string): two-letter uppercase state abbreviation (in StateUnits)
    - unit_list (list): list of dictionaries,
        each dictionary has information about a 
        single NPS unit with the desired activity
      num_units (integer): number of state's nps units with the desired activity
    
    Parameters:
    - self (ActivityUnits class instance)
    - state_abbrev (string): two-letter lowercase state abbreviation
    - desired_activity (string): user's desired activity
    '''
    super().__init__(state_abbrev)
    self.activity = desired_activity
    self.unit_list = find_activity_units(self.unit_list, self.activity)
    self.num_units = len(self.unit_list)
    
  def __str__(self):
    '''  TO DO
    String representation of the ActivityUnits class
    
    Parameters:
    - self (ActivityUnits class instance)
    '''
    BORDER = 46 * '-'

    return_string = BORDER + '\n' + 'Where to find ' + self.activity + '\n' + BORDER + '\nNPS Units in ' + self.state + '\n' + BORDER + '\n'
  
    loop_string = ""
    for unit in self.unit_list: 
        loop_string += unit["fullName"] + '\n'
      

    return return_string + loop_string

class CompareUnits:
  ''' Compares NPS units in different states '''

  def __init__(self, desired_activity = None):
    ''' DO NOT TOUCH. This is already completed for you.
    The constructor for an instance of CompareUnits class 
    
    Class attributes:
    - list_of_units (list): a list of instances 
        of the StateUnits or ActivityUnits class
    - activity (string): the desired activity 
    
    Parameters:
    - self (CompareUnits class instance)
    - desired_activity (string): the activity 
      that the user seeks. The default value 
      is None to be used with the StateUnits class
    '''
    self.list_of_units = []
    self.activity = desired_activity

  def add_all_states(self):
    ''' TO DO
    For each state, adds instances of the:
    - StateUnits class if the 
        class attribute activity is None 
    - ActivityUnits class if the
        class attribute activity is not None

    Parameters:
    - self (CompareUnits class instance)
    '''
    if self.activity is None:
      for state_indv in STATES:
        self.list_of_units.append(StateUnits(state_indv))
    else:
      for state_indv in STATES:
        self.list_of_units.append(ActivityUnits(state_indv, self.activity))
        
  def __str__(self):
    ''' TO DO
    String representation of the CompareUnits class

    Parameters:
    - self (CompareUnits class instance)
    '''
    HEADER = 18 * "*"
    SMALL_HEADER = 6 * '-'
    WHITESPACE = 5 * ' '

    if self.activity == None:
      Activity = '(None)'
    else:
      Activity = '\n with ' + self.activity
      
    welcome = HEADER + '\n NPS Units ' + Activity + '\n' + HEADER + '\nState' + WHITESPACE + ' Number\n' + SMALL_HEADER + WHITESPACE + SMALL_HEADER + '\n'
    return_string = ''
    for unit in self.list_of_units:
      return_string += '  ' + unit.state + '         ' + str(unit.num_units) + '\n'
     


    return welcome + return_string
        

      
      
  def state_with_most_units(self):
    ''' TO DO
    Returns the state with greatest number of NSP units
    
    Parameters:
    - self (CompareUnits class instance)

    Returns:
    - an instance of the StateUnits or ActivityUnits class
    '''
    return max(self.list_of_units)
    

  def five_states_with_most_units(self):
    ''' TO DO
    Returns the five states with greatest number of NPS units
    
    Parameters:
    - self (CompareUnits class instance)

    Returns:
    - five_states (list): list of strings
        each string is an uppercase state abbreviation
    - num_units_five_states (list): list of integers
        each integer is the num_units 
        corresponding to the state in five_states
    '''
    dict_helper = {}
    for unit in self.list_of_units:
      dict_helper[unit.state] = unit.num_units

    sorted_dict = sorted(dict_helper.items(), key=operator.itemgetter(1), reverse=True)
    
    top_5_states = []
    top_5_units = []
    for indv in sorted_dict[:5]:
      top_5_states.append(indv[0])
      top_5_units.append(indv[1])

    return top_5_states, top_5_units

  
####################################################
# Helper Functions
####################################################

def find_activity_units(unit_list, desired_activity):
  ''' TO DO
  Returns a list of units that have the desired activity

  Parameters:
  - unit_list (list): list of dictionaries, 
    each dictionary has information about 
    a single NPS unit
  - desired_activity (string): the activity specified by the user

  Returns:
  - a new list with only those dictionaries 
    from unit_list for NPS units 
    with the desired activity. 
  '''
  return_list = []
  
  for i, open_dict in enumerate(unit_list): #https://realpython.com/python-enumerate/`
    activities = open_dict['activities']
    for j in activities:
      individual_activities = j['name']
      if individual_activities == desired_activity:
        return_list.append(unit_list[i])
        
  return return_list

def activity_menu():
  ''' DO NOT TOUCH. This is already completed for you.
  Prints the available activities '''
  print("Available activities:")
  for index in range(len(ACTIVITIES)):
    print(index + 1, ACTIVITIES[index])


def select_activity():
  ''' TO DO 
  Repeatedly ask the user for a number 
  corresponding to an activity 
  until a valid number is given
  
  Returns: an integer (corresponding to the desired activity)
  '''
  while True:
    try:
      activity_menu()
      prompt = int(input("Enter the number associated with the desired activity:"))
      if prompt < 8 and prompt > 0:
        return prompt
    except ValueError:
      continue


def option_menu():
  ''' DO NOT TOUCH. This is already completed for you.
  Prints the available options '''
  print("Available options:")
  for index in range(len(OPTIONS)):
    print(index + 1, OPTIONS[index])


def select_option():
  ''' TO DO
  Repeatedly asks the user for a number 
  corresponding to an option 
  until a valid number is given
  
  Returns: an integer (corresponding to the desired option)
  '''
  while True:
    try:
      option_menu()
      prompt = int(input("Enter the number associated with the desired option:"))
      if prompt < 8 and prompt > 0:
        return prompt
    except ValueError:
      continue
    


def plot_state_info(states, num_units, activity):
  ''' DO NOT TOUCH. This is already completed for you.
  Saves a barplot with states and the number of units
  
  Parameters:
  - states (list): a list of strings
  each string is an abbreviation for a state name
  - num_units (list), a list of integers, number of NPS units in corresponding state in states
  - activity (string): the user's selected activity
  '''
  # Open a new figure
  f1 = plt.figure()
  # Add labels to the plot
  plt.xlabel("State")
  if activity == None:
    plt.ylabel("Number of NPS Units")
  else:
    plt.ylabel("Number of NPS Units with " + activity)
  # Create list for x values- where to place labels
  x = list(range(len(states)))
  plt.xticks(x, states)
  # Plot data
  plt.bar(x, num_units)
  plt.savefig("state_info.png")


def show_results():
  ''' DO NOT TOUCH. This is already completed for you.
  Displays the results of the analysis 
  in print or graphic form
  '''
  while True:
    option_num = select_option()
    if option_num == 5: # Quit
      return
    # Create info for all states using StateUnits or ActivityUnits instances
    if option_num == 1 or option_num == 2:
      states_info = CompareUnits()
    elif option_num == 3 or option_num == 4:
      activity_num = select_activity()
      activity = ACTIVITIES[activity_num-1]
      states_info = CompareUnits(activity)
    states_info.add_all_states()
    # Print results
    if option_num == 1 or option_num == 3:
      print(states_info.state_with_most_units())
    # Plot results
    if option_num == 2 or option_num == 4:
      states, num_units =states_info.five_states_with_most_units()
      plot_state_info(states, num_units, states_info.activity)
      
    
    

    