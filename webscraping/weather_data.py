import pandas as pd
import requests
from bs4 import BeautifulSoup

# Ended up not using this data

def state_names(url):
    states = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features='lxml')
    table = soup.find_all('a', {"class": "stretched-link"})
    for i in range(0, len(table)):
        new_url = 'https://www.usclimatedata.com' + table[i].get('href')
        state = table[i].get_text()
        dic = {'State': state, 'url': new_url}
        states.append(dic)
    state_df = pd.DataFrame.from_dict(states)
    return state_df

def city_names(url):
    cities = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features='lxml')
    state = soup.find("p", {"class": "selection_title"})
    state = state.get_text()[:-24]
    table = soup.find_all('a', {"class": "stretched-link"})
    for i in range(0, len(table)):
        new_url = 'https://www.usclimatedata.com' + table[i].get('href')
        city = table[i].get_text()
        dic = {'State': state, 'City': city, 'url': new_url}
        cities.append(dic)
    city_df = pd.DataFrame(cities)
    return city_df

def weather_parameters(url, city, state):
    req = pd.read_html(url)

    # Seperated into two tables because website has them seperated
    jan_thru_jun = req[0]
    jul_thru_dec = req[1]
    jan_thru_jun.rename(columns={'Unnamed: 0': 'Metric'}, inplace=True)
    jul_thru_dec.rename(columns={'Unnamed: 0': 'Metric'}, inplace=True)
    
    snow, snow2, prec, prec2 = None, None, None, None

    for i, row in jan_thru_jun.iterrows():
        if ("Average high" in row['Metric']):
            high = [i for i in row[1:]]
        if ("Average low" in row['Metric']):
            low = [i for i in row[1:]]
        if ("Av. precipitation" in row['Metric']):
            prec = [i for i in row[1:]]
        if ("snowfall in inch" in row['Metric']):
            snow = [i for i in row[1:]]

    for i, row in jul_thru_dec.iterrows():
        if ("Average high" in row['Metric']):
            high2 = [i for i in row[1:]]
        if ("Average low" in row['Metric']):
            low2 = [i for i in row[1:]]
        if ("Av. precipitation" in row['Metric']):
            prec2 = [i for i in row[1:]]
        if ("snowfall in inch" in row['Metric']):
            snow2 = [i for i in row[1:]]

    if snow is None:
        snow = [0]*6
    if prec is None:
        prec = [0]*6

    highs = high + high2 
    lows = low + low2
    precs = prec + prec2
    snows = snow + snow2

    high_data = {"Jan High": highs[0], "Feb High": highs[1], "Mar High": highs[2], "Apr High": highs[3], "May High": highs[4], "Jun High": highs[5], "Jul High": highs[6], "Aug High": highs[7], "Sep High": highs[8], "Oct High": highs[9], "Nov High": highs[10], "Dec High": highs[11]}
    low_data = {"Jan Low": lows[0], "Feb Low": lows[1], "Mar Low": lows[2], "Apr Low": lows[3], "May Low": lows[4], "Jun Low": lows[5], "Jul Low": lows[6], "Aug Low": lows[7], "Sep Low": lows[8], "Oct Low": lows[9], "Nov Low": lows[10], "Dec Low": lows[11]}
    prec_data = {"Jan Prec": precs[0], "Feb Prec": precs[1], "Mar Prec": precs[2], "Apr Prec": precs[3], "May Prec": precs[4], "Jun Prec": precs[5], "Jul Prec": precs[6], "Aug Prec": precs[7], "Sep Prec": precs[8], "Oct Prec": precs[9], "Nov Prec": precs[10], "Dec Prec": precs[11]}
    snow_data = {"Jan Snow": snows[0], "Feb Snow": snows[1], "Mar Snow": snows[2], "Apr Snow": snows[3], "May Snow": snows[4], "Jun Snow": snows[5], "Jul Snow": snows[6], "Aug Snow": snows[7], "Sep Snow": snows[8], "Oct Snow": snows[9], "Nov Snow": snows[10], "Dec Snow": snows[11]}

    combined_data = pd.DataFrame.from_dict({**high_data, **low_data, **prec_data, **snow_data}, orient="index")
    combined_data = combined_data.transpose()
    combined_data['State'] = state
    combined_data['City'] = city
    return combined_data

def main():
    states_list = state_names('https://www.usclimatedata.com/')
    
    city_state_urls = []
    for i, row in states_list.iterrows():
        city_state_urls.append(city_names(row.url))

    city_state_df = pd.DataFrame()
    for i in range(0, len(city_state_urls)):
        temp_df = city_state_urls[i]
        city_state_df = pd.concat([city_state_df, temp_df], ignore_index=True)

    all_weather_data = pd.DataFrame()
    for i, row in city_state_df.iterrows():
        try:
            all_weather_data = pd.concat([all_weather_data, weather_parameters(row.url, row.City, row.State)], ignore_index=True)
        except:
            pass

    # Add state abbreviations
    abbreviations = pd.read_html('https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations', skiprows=11)[0]
    abbreviations = abbreviations[['United States of America', 'Unnamed: 5']]
    abbreviations = abbreviations.rename(columns={'United States of America': 'State', 'Unnamed: 5': 'Abbreviation'})

    weather_city = all_weather_data.merge(abbreviations, on='State')
    weather_city['CityState'] = [row.City+", "+row.Abbreviation for i, row in weather_city.iterrows()]
    cols = weather_city.columns.tolist()
    cols = cols[-4:] + cols[:-4]
    weather_city = weather_city[cols]

    weather_city.to_csv('weather_city.csv', index=False)

if __name__ == "__main__":
    main()
