# City Finder Web Application

This web application recommends cities based on user preferences using data from Numbeo. This web app is built using Python and Flask. It is hosted on AWS using Elasticbeanstalk. The data is webscraped from Numbeo.

## URL

The live application can be accessed at: [http://cityfinder2-env.eba-xvmwdsf9.us-east-2.elasticbeanstalk.com/)

## Features

- **User Preferences**: Users can input their preferences for various categories such as Purchasing Power, Safety, Health Care, Climate, Cost of Living, and Pollution.
- **Web Scraping**: The application scrapes data from Numbeo to gather up-to-date information about different cities.
- **Cosine Similarity**: The recommendation algorithm uses cosine similarity to find the best matching city based on user preferences.
- **User Interface**: A simple and intuitive web interface built with Flask.

## Deployment

The application is hosted on AWS using Elastic Beanstalk.

## Code Structure

- **application.py**: The main Flask application.
- **webscraping/**: Contains the web scraping logic to fetch data from Numbeo and other data that did not end up being used.
- **templates/**: Contains HTML file for the website.
- **static/**: Contains CSS file for website styling.
