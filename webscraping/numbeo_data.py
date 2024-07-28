import pandas as pd
import requests
from bs4 import BeautifulSoup

def read_city_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Creates url for city
def generate_city_urls(df):
    base_url = "https://www.numbeo.com/quality-of-life/in/"
    urls = []
    for _, row in df.iterrows():
        city_name = row['city'].replace(' ', '-')
        city_url = f"{base_url}{city_name}"
        urls.append((row['city'], city_url))
    return urls

# Creates url for city-state, some cities require state abbreviation
def generate_city_state_urls(df):
    base_url = "https://www.numbeo.com/quality-of-life/in/"
    urls = []
    for _, row in df.iterrows():
        city_name = row['city'].replace(' ', '-')
        state_abbr = row['state_id']
        state_url = f"{base_url}{city_name}-{state_abbr}"
        urls.append((row['city'], state_url))
    return urls

def quality_of_life(url, city):
    for index in [2, 3]:  # Checks tables 2 and 3
        try:
            tables = pd.read_html(url)
            if len(tables) > index:
                quality_df = tables[index]
                
                if len(quality_df.columns) >= 3:
                    quality_df.rename(columns={0: 'Metric', 1: 'Value', 2: 'Compare'}, inplace=True)
                    quality_df.set_index("Metric", inplace=True)
                    
                    # Check if necessary metrics exist, add to dictionary
                    required_metrics = ['Purchasing Power Index', 'Safety Index', 'Health Care Index', 'Climate Index', 'Cost of Living Index', 'Pollution Index']
                    if all(metric in quality_df.index for metric in required_metrics):
                        data_dict = {
                            "City": city,
                            "Purchasing Power": quality_df.loc['Purchasing Power Index', 'Value'],
                            "Safety": quality_df.loc['Safety Index', 'Value'],
                            "Health Care": quality_df.loc['Health Care Index', 'Value'],
                            "Climate": quality_df.loc['Climate Index', 'Value'],
                            "Cost of Living": quality_df.loc['Cost of Living Index', 'Value'],
                            "Pollution": quality_df.loc['Pollution Index', 'Value'],
                            "Purchasing Power Comp": quality_df.loc['Purchasing Power Index', 'Compare'],
                            "Safety Comp": quality_df.loc['Safety Index', 'Compare'],
                            "Health Care Comp": quality_df.loc['Health Care Index', 'Compare'],
                            "Climate Comp": quality_df.loc['Climate Index', 'Compare'],
                            "Cost of Living Comp": quality_df.loc['Cost of Living Index', 'Compare'],
                            "Pollution Comp": quality_df.loc['Pollution Index', 'Compare']
                        }
                        return data_dict
                    else:
                        print(f"Table at index {index} for {city} does not contain all required metrics at URL {url}")
                else:
                    print(f"Table at index {index} does not have the expected columns for {city} at URL {url}")
            else:
                print(f"Table at index {index} is not available for {city} at URL {url}")
        except Exception as e:
            print(f"Error fetching data for {city} from URL {url}: {e}")
    return None

# Fetches quality of life data for all cities
def get_quality_data(urls):
    cities = []
    for city, url in urls:
        print(f"Fetching data for {city}")
        print(f"URL: {url}")
        data = quality_of_life(url, city)
        if data:
            cities.append(data)
        else:
            print(f"Failed to fetch data for {city} from URL {url}")
    return pd.DataFrame(cities)

def convert_columns_to_numeric(df):
    columns = ['Purchasing Power', 'Safety', 'Health Care', 'Climate', 'Cost of Living', 'Pollution']
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

def main():
    city_df = read_city_data("uscities.csv")

    print("Generating URLs")
    city_urls = generate_city_urls(city_df)
    city_state_urls = generate_city_state_urls(city_df)
    print(f"Number of city URLs generated: {len(city_urls)}")
    print(f"Number of city-state URLs generated: {len(city_state_urls)}")

    print("Fetching quality of life data city URLs")
    df_city = get_quality_data(city_urls)
    print(f"Number of cities with data from city URLs: {df_city.shape[0]}")

    print("Fetching quality of life data city-state URLs")
    df_state = get_quality_data(city_state_urls)
    print(f"Number of cities with data from city-state URLs: {df_state.shape[0]}")

    combined_df = pd.concat([df_city, df_state]).drop_duplicates(subset='City', keep='last')
    print(f"Total number of cities with data: {combined_df.shape[0]}")

    combined_df = convert_columns_to_numeric(combined_df)

    combined_df.to_csv("quality_of_life_metrics.csv", index=False)
    print("Data saved")

if __name__ == "__main__":
    main()