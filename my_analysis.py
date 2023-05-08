####################################################
#
#            CSCI 203 Final Project
#                     Part 2
#                  Spring 2023
#
# Add your name here
#
####################################################
# Import Libraries
#
from info_read_write import *
import matplotlib.pyplot as plt
import urllib.request
import urllib.parse
import math
import pandas as pd
import plotly.express as px #https://towardsdatascience.com/simplest-way-of-creating-a-choropleth-map-by-u-s-states-in-python-f359ada7735e
import plotly.io as pio #https://plotly.com/python/static-image-export/
#
####################################################
# CONSTANTS
API_KEYS = load_json_file("API_KEYS.json")
LUM_API_KEY = API_KEYS['LUM_API_KEY']
PARKS_FILE = load_json_file("my_data/all_states_parks.json")
# DONE - Do not modify.
####################################################

# STATES - a list of the state abbreviations
STATES = [
  'ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'ia',
  'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms',
  'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
  'sd', 'tn', 'tx', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']

# Add your functions for Part 2 here

def calculate_SQM(artificial_brightness):
  '''Takes the input artifical brightness and returns that value of SQM (Sky Quality Meter) in magnitudes per square arcsecond'''
  return (math.log10((artificial_brightness + 0.171168465) / 108000000) / -0.4)


def get_long_lat(state):
  '''Returns a list with dictionary muiltiple dictionaries with the longitude and latitude of the given state.'''
  info = get_park_info(state)
  units = info["data"]

  return_list = []
  for unit in units:
    # Creates the dictionary of what we are looking for
    constructor_dict = {"State": "", "Park_Name": "", "Lat": 0, "Long": 0}

    if unit["latitude"] == "" or unit["longitude"] == "":
      constructor_dict["Lat"] = 0
      constructor_dict["Long"] = 0
    else:
      # Updates the constructor_dict with the new information
      constructor_dict["State"] = state.upper()
      constructor_dict["Park_Name"] = unit["fullName"]
      constructor_dict["Lat"] = float(unit["latitude"])
      constructor_dict["Long"] = float(unit["longitude"])

    return_list.append(constructor_dict)

  return return_list


def get_state_luminosity(state):
  '''Takes the input of the perfered state and returns the artificial brightness for every Park Unit in the state. It using Longitude and Latitude data parsed into an external API. Limit 500 daily calls'''
  # Gathers Long Lat data for each Park Unit
  long_lat_data = get_long_lat(state)

  # Defines API endpoint
  endpoint = 'https://www.lightpollutionmap.info/QueryRaster/'

  # Loops through each Park Unit to gather Long Lat and parses it into the API
  return_list = []
  for state_idv in long_lat_data:
    # Established what values to return
    return_dict = {"State": "", "Park": "", "SQM": 0}

    # Acceses the Long Lat data from each Park Unit
    Lat = state_idv["Lat"]
    Long = state_idv["Long"]

    # Adds the Long Lat values to an API readable String
    qd_value = str(Long) + "," + str(Lat)

    # Sets Parameters for the API call. ql is map model, qt is data type, qd is coordinates, key is api key
    params = {
      'ql': 'wa_2015',
      'qt': 'point',
      'qd': qd_value,
      'key': LUM_API_KEY
    }

    # Parses Parameters using the urlib library
    query_string = urllib.parse.urlencode(params)

    url = endpoint + '?' + query_string

    # Calls the API
    response = urllib.request.urlopen(url)

    # Decodes the content to make it readable, returns a luminosity value
    content = float(response.read().decode())

    # Updates return_dict with new values
    return_dict["State"] = state_idv["State"]
    return_dict["Park"] = state_idv["Park_Name"]
    return_dict["SQM"] = calculate_SQM(content)

    # Parses return_dict into a list which can be returned
    return_list.append(return_dict)

  return return_list


def process_data_json():
  '''Create a json file from the API data so it doesn't have to constantly be called'''
  data = []
  for states in STATES:
    print(states)
    data.append(get_state_luminosity(states))
    
  write_to_json_file(data, 'all_states')


def top_10_locations():
  '''Returns the 10 parks with the highest SQM'''

  # Gathers each individual dictionary and put them in a list 
  all_parks = []
  for state_parks in PARKS_FILE:
    for park in state_parks:
      all_parks.append(park)
  
  # Sorts the list in reverse so the highest values are last
  sorted_parks = sorted(all_parks, key=lambda park: park['SQM'], reverse=True)
  
  # Returns the last 10 items of the sorted string which should be the highest values
  lowest_sqm_parks = sorted_parks[:10]

  # Takes the data and puts it back into a dictionary nested in a list
  return_data = []
  for i, park in enumerate(lowest_sqm_parks):
    i += 1
    
    helper_dict = {
      "Rank": 0,
      "Park": "",
      "State": "",
      "SQM": 0
    }
    
    helper_dict["Rank"] = i
    helper_dict["Park"] = park['Park']
    helper_dict["State"] = park['State']
    helper_dict["SQM"] = park['SQM']

    return_data.append(helper_dict)

  # Creates a string to return the data
  return_str = "Top 10 parks for Stargazing\n"
  return_str += "------------------\n"
  for park_data in return_data:
    return_str += f"Rank: {park_data['Rank']}\n"
    return_str += f"Park: {park_data['Park']}\n"
    return_str += f"State: {park_data['State']}\n"
    return_str += f"SQM: {park_data['SQM']}\n"
    return_str += "------------------\n"
    

  return return_str


def top_10_locations_no_AK():
  '''Returns the 10 parks with the highest SQM but excludes AK''' 
  # Gathers each individual dictionary and put them in a list 
  all_parks = []
  for state_parks in PARKS_FILE:
    for park in state_parks:
      # Excludes AK from the output
      if park["State"] == "AK":
        pass
      else:
        all_parks.append(park)
  
  # Sorts the list in reverse so the highest values are last
  sorted_parks = sorted(all_parks, key=lambda park: park['SQM'], reverse=True)
  
  # Returns the last 10 items of the sorted string which should be the highest values
  lowest_sqm_parks = sorted_parks[:10]

  # Takes the data and puts it back into a dictionary nested in a list
  return_data = []
  for i, park in enumerate(lowest_sqm_parks):
    i += 1
    
    helper_dict = {
      "Rank": 0,
      "Park": "",
      "State": "",
      "SQM": 0
    }
    
    helper_dict["Rank"] = i
    helper_dict["Park"] = park['Park']
    helper_dict["State"] = park['State']
    helper_dict["SQM"] = park['SQM']

    return_data.append(helper_dict)

  # Creates a string to return the data
  return_str = "Top 10 parks for Stargazing (No AK)\n"
  return_str += "------------------\n"
  for park_data in return_data:
    return_str += f"Rank: {park_data['Rank']}\n"
    return_str += f"Park: {park_data['Park']}\n"
    return_str += f"State: {park_data['State']}\n"
    return_str += f"SQM: {park_data['SQM']}\n"
    return_str += "------------------\n"
    

  return return_str


def worst_10_locations():
  '''Returns the 10 parks with the lowest SQM''' 

  # Gathers each individual dictionary and put them in a list 
  all_parks = []
  for state_parks in PARKS_FILE:
    for park in state_parks:
      all_parks.append(park)
  
  # Sorts the list in reverse so the lowest values are last
  sorted_parks = sorted(all_parks, key=lambda park: park['SQM'])
  
  # Returns the last 10 items of the sorted string which should be the lowest values
  lowest_sqm_parks = sorted_parks[:10]

  # Takes the data and puts it back into a dictionary nested in a list
  return_data = []
  for i, park in enumerate(lowest_sqm_parks):
    i += 1
    helper_dict = {
      "Rank": 0,
      "Park": "",
      "State": "",
      "SQM": 0
    }
    
    helper_dict["Rank"] = i
    helper_dict["Park"] = park['Park']
    helper_dict["State"] = park['State']
    helper_dict["SQM"] = park['SQM']

    return_data.append(helper_dict)

  # Creates a string to return the data
  return_str = "Worst 10 parks for Stargazing\n"
  return_str += "------------------\n"
  for park_data in return_data:
    return_str += f"Rank: {park_data['Rank']}\n"
    return_str += f"Park: {park_data['Park']}\n"
    return_str += f"State: {park_data['State']}\n"
    return_str += f"SQM: {park_data['SQM']}\n"
    return_str += "------------------\n"
    

  return return_str


def worst_10_locations_no_DC():
  '''Returns the 10 parks with the lowest SQM excluding DC'''

  # Gathers each individual dictionary and put them in a list
  all_parks = []
  for state_parks in PARKS_FILE:
    for park in state_parks:
      # Removes DC from the list
      if park["State"] == "DC":
        pass
      else:
        all_parks.append(park)
  
  # Sorts the list in reverse so the lowest values are last
  sorted_parks = sorted(all_parks, key=lambda park: park['SQM'])
  
  # Returns the last 10 items of the sorted string which should be the lowest values
  lowest_sqm_parks = sorted_parks[:10]

  # Takes the data and puts it back into a dictionary nested in a list
  return_data = []
  for i, park in enumerate(lowest_sqm_parks):
    i += 1
    
    helper_dict = {
      "Rank": 0,
      "Park": "",
      "State": "",
      "SQM": 0
    }
    
    helper_dict["Rank"] = i
    helper_dict["Park"] = park['Park']
    helper_dict["State"] = park['State']
    helper_dict["SQM"] = park['SQM']

    return_data.append(helper_dict)

  # Creates a string to return the data
  return_str = "Worst 10 parks for Stargazing (No DC)\n"
  return_str += "------------------\n"
  for park_data in return_data:
    return_str += f"Rank: {park_data['Rank']}\n"
    return_str += f"Park: {park_data['Park']}\n"
    return_str += f"State: {park_data['State']}\n"
    return_str += f"SQM: {park_data['SQM']}\n"
    return_str += "------------------\n"
    

  return return_str


def parks_over_20_SQM():
  '''Returns a dictionary nested in a list of all the parks with over 20.5 SQM'''
  return_list = []
  for states in PARKS_FILE:
    for parks in states:
      dict_helper = {
        "Park": "",
        "State": "",
        "SQM": 0
      }
      
      if parks["SQM"] >= 20.5:
        dict_helper["Park"] = parks["Park"]
        dict_helper["State"] = parks["State"]
        dict_helper["SQM"] = parks["SQM"]
        return_list.append(dict_helper)

  return return_list
        
        
def states_over_20_SQM():
  '''Returns all the States with an SQM over 20.5 and counts how many parks each has'''
  data = parks_over_20_SQM()
  
  # Creates a dictionary with the state and state count
  state_counts = {}
  for d in data:
    state = d['State']
    # Counts each states and adds it to the dictionary if there is a park in state with more then 20.5 SQM
    if state in state_counts:
      state_counts[state] += 1
    else:
      state_counts[state] = 1
  
  # Sorts the dictionary values from smallest to largest
  sorted_data = dict(sorted(state_counts.items(), key=lambda item: item[1]))
  
  return sorted_data


def state_SQM_avg():
  '''Returns the average SQM for each state'''

  # Creates a dictionary that can be used to calculate Avg SQM
  state_sqms = {}
  for state_parks in PARKS_FILE:
    for park in state_parks:
      state = park['State']
      sqm = park['SQM']

      if state in state_sqms:
        state_sqms[state].append(sqm)
      else:
        state_sqms[state] = [sqm]
  
  # Calculates the Avg SQM for each state
  state_avg = {}
  for state, sqm_list in state_sqms.items():
    avg_sqm = sum(sqm_list) / len(sqm_list)
    state_avg[state] = avg_sqm

  return state_avg


def graph_state_parks():
  '''Graphs the avg state SQM using a matplotlib bar graph'''

  # Gathers data in the form of a dicionary
  data = states_over_20_SQM()

  # Plots graph
  plt.figure(figsize=(18, 12))
  plt.title('States with most Parks over 20.5 SQM', fontdict={'fontsize': 35})
  plt.xlabel('States', fontdict={'fontsize': 20})
  plt.ylabel('Park Count', fontdict={'fontsize': 20})
  plt.bar(data.keys(), data.values(), align='center')
  plt.savefig("state_info.png")


def map_SQM_avg():
  '''Creates a choropleth of the United States using the Avg state SQM data. Returns the graph as a png.'''
  data = state_SQM_avg()
  
  # Creates a dictionary with a value of a nested list so it can be in a readable form for the graph
  states_for_graph = {
    "States": list(data.keys()),
    "SQM": list(data.values())
  }

  # Graphs the data in a choropleth map 
  fig = px.choropleth(states_for_graph, 
                      locations='States', 
                      locationmode='USA-states', 
                      color='SQM', 
                      scope="usa", 
                      color_continuous_scale="blues", 
                      title='Average State SQM')
  
  # Adjusts the figure layout
  fig.update_layout(
    title_text = 'Average State SQM',
    title_font_size = 22,
    title_x=0.45
    )

  # Writes the data to a png
  pio.write_image(fig, 'choropleth_map.png')


def main():
  '''Calls all the important functions.'''
  graph_state_parks()
  map_SQM_avg()
  print(top_10_locations())
  print(top_10_locations_no_AK())
  print(worst_10_locations())
  print(worst_10_locations_no_DC())

main()





  
  
  