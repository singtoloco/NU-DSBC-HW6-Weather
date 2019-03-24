#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# ### Analysis
# * As expected, the weather becomes significantly warmer as one approaches the equator (0 Deg. Latitude). More interestingly, however, is the fact that the southern hemisphere tends to be warmer this time of year than the northern hemisphere. This may be due to the tilt of the earth.
# * There is no strong relationship between latitude and cloudiness. However, it is interesting to see that a strong band of cities sits at 0, 80, and 100% cloudiness.
# * There is no strong relationship between latitude and wind speed. However, in northern hemispheres there is a flurry of cities with over 20 mph of wind.
# 
# ---
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time

from pprint import pprint
import openweathermapy.core as owm

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[3]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(len(cities))
if len(cities) >= 500:
    print("We have >= 500 unique (non-repeat) cities")
else:
    print("WARNING! We have less than 500 unique (non-repeat) cities")
    
df_city = pd.DataFrame(cities, columns = ['City'])

df_city['Cloudiness'] = ""
df_city['Country'] = ""
df_city['Date'] = ""
df_city['Humidity'] = ""
df_city['Lat'] = ""
df_city['Lng'] = ""
df_city['Max Temp'] = ""
df_city['Wind Speed'] = ""


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

print("Beginning Data Retrieval")
print("-----------------------------")


# use iterrows to iterate through pandas dataframe

"""using owm.get_current, can't catch error but WHY???"""
# Create settings dictionary with information we're interested in
#settings = {"units": "Imperial", "appid": api_key}
#for index, row in df_city.iterrows():
#    
#    city = row['City']
#    print(f"Processing Record {index} | {city}")
#    try:        
#        current_weather = owm.get_current(city, **settings)
#        df_city.loc[index, 'Cloudiness'] = current_weather['clouds']['all']
#        df_city.loc[index, 'Country'] = current_weather['sys']['country']
#        df_city.loc[index, 'Date'] = current_weather['dt']
#        df_city.loc[index, 'Humidity'] = current_weather['main']['humidity']
#        df_city.loc[index, 'Lat'] = current_weather['coord']['lat']
#        df_city.loc[index, 'Lng'] = current_weather['coord']['lon']
#        df_city.loc[index, 'Max Temp'] = current_weather['main']['temp_max']
#        df_city.loc[index, 'Wind Speed'] = current_weather['wind']['speed']
#
#    except KeyError:
#        print("Can't find data for city: {city} ... skipping.")

# Save config information.
url = "http://api.openweathermap.org/data/2.5/weather?"
units = "Imperial"

# Build partial query URL
query_url = f"{url}appid={api_key}&units={units}&q="
print(query_url)

for index, row in df_city.iterrows():
    
    city = row['City']
    print(f"Processing Record {index} | {city}")
    try:        
        response = requests.get(query_url + city).json()
        #just b/c it's in Example
#        print(query_url + city)
        df_city.loc[index, 'Cloudiness'] = response['clouds']['all']
        df_city.loc[index, 'Country'] = response['sys']['country']
        df_city.loc[index, 'Date'] = response['dt']
        df_city.loc[index, 'Humidity'] = response['main']['humidity']
        df_city.loc[index, 'Lat'] = response['coord']['lat']
        df_city.loc[index, 'Lng'] = response['coord']['lon']
        df_city.loc[index, 'Max Temp'] = response['main']['temp_max']
        df_city.loc[index, 'Wind Speed'] = response['wind']['speed']

    except KeyError:
        print("Can't find data for city: {city} ... skipping.")
        
df = df_city[df_city['Date'] != ""]
if len(df) >= 500:
    print("After filtering, we still have sufficient numbers of data (>=500)")
else:
    print("WARNING! After filtering, We have less than 500 unique (non-repeat) rows of data")
df.head()  

unix_timestamp  = int(df['Date'][0])
local_time = time.localtime(unix_timestamp)

# In[3]:

# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
df.to_csv('weather_data.csv')
# * Display the DataFrame

# In[4]:


# In[5]:

# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot
plt.scatter(df['Lat'], df['Max Temp'], color='blue', edgecolors = 'black', zorder = 3)
plt.grid(color = 'white', zorder = 0)
plt.xlim(-80, 100)
plt.ylim(-100, 150)

#"get current axes"
ax = plt.gca()
ax.set_facecolor('lightsteelblue')

plt.title(f"City Latitude vs. Max Temperature ({time.strftime('%m/%d/%y')})")
plt.xlabel("Latitude")
plt.ylabel("Max Temperature (F)")

plt.savefig('Lat_vs_Temp.png', bbox_inches = "tight")

plt.show()

# In[6]:

# #### Latitude vs. Humidity Plot
plt.scatter(df['Lat'], df['Humidity'], color='blue', edgecolors = 'black', zorder = 3)
plt.grid(color = 'white', zorder = 0)
plt.xlim(-80, 100)
plt.ylim(-20, 120)

#"get current axes"
ax = plt.gca()
ax.set_facecolor('lightsteelblue')

plt.title(f"City Latitude vs. Humidity ({time.strftime('%m/%d/%y')})")
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")

plt.savefig('Lat_vs_Humid.png', bbox_inches = "tight")

plt.show()


# In[7]:

# #### Latitude vs. Cloudiness Plot
plt.scatter(df['Lat'], df['Cloudiness'], color='blue', edgecolors = 'black', zorder = 3)
plt.grid(color = 'white', zorder = 0)
plt.xlim(-80, 100)
plt.ylim(-20, 120)

#"get current axes"
ax = plt.gca()
ax.set_facecolor('lightsteelblue')

plt.title(f"City Latitude vs. Cloudiness ({time.strftime('%m/%d/%y')})")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")

plt.savefig('Lat_vs_Cloud.png', bbox_inches = "tight")

plt.show()

# In[8]:

# #### Latitude vs. Wind Speed Plot
plt.scatter(df['Lat'], df['Wind Speed'], color='blue', edgecolors = 'black', zorder = 3)
plt.grid(color = 'white', zorder = 0)
plt.xlim(-80, 100)
plt.ylim(-5, 50)

#"get current axes"
ax = plt.gca()
ax.set_facecolor('lightsteelblue')

plt.title(f"City Latitude vs. Wind Speed ({time.strftime('%m/%d/%y')})")
plt.xlabel("Latitude")
plt.ylabel("Wind Speed (mph)")

plt.savefig('Lat_vs_Wind.png', bbox_inches = "tight")

plt.show()


# In[9]:





# In[ ]:




