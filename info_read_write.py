import urllib.request 
import json

STATES = ['ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']


def get_park_info(state):
  ''' Retrieves park information for a state from the nps api

  Parameters:
    state (string): The two lowercase letter abbreviation for the state name.

  Returns: 
    park_info (dictionary): information for the 
    National Park Service sites in the state
  '''
  # Configure API request
  endpoint = "https://developer.nps.gov/api/v1/parks?stateCode=" + state
  HEADERS = {"X-Api-Key":"F1IaGExQAdMOkMCjbgSIm8ht2dcYCiNJUMfgs6Ou"}
  req = urllib.request.Request(endpoint,headers=HEADERS)

  # Execute request and parse response
  response = urllib.request.urlopen(req).read()
  park_info = json.loads(response.decode('utf-8'))
  return park_info


def write_to_json_file(info, state):
  ''' Write information to a json file

  Parameters:
    info (dictionary): information for National Park System units in a state
    state (string): two-letter abbreviation for a state name

  Returns:
    None
  '''
  datas = json.dumps(info)
  filepath = "my_data/" + state + "_parks.json"
  with open(filepath,"w") as f:
    f.write(datas)


def load_json_file(filepath):
  ''' Read information from a json file

  Parameters:
    filepath (string): format of the string for a state
    "state_park_info/" + state + "_parks.json"

  Returns:
    info (dictionary): the information from a json file
  '''
  with open(filepath, "r") as read_file:
    info = json.load(read_file)
  return info

def create_all_states_info():
  ''' Writes data for all states to json files in a folder
  '''
  for state in STATES:
    park_info = get_park_info(state)
    write_to_json_file(park_info, state)


