from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

application = Flask(__name__)

def load_data(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('Comp')] # Remove because non-numeric
    return df

# For parameters that are better when lower, invert the values
def invert_values(df, columns):
    for column in columns:
        df[column] = df[column].max() - df[column] + df[column].min()
    return df

def find_similarity(columns, user, scores):
    # Reshape user array to 2D, required for cosine similarity
    user = user.reshape(1, -1)
    values = []

    for index, city in enumerate(scores.index):
        # Reshape each city's values to 2D, run cosine similarity on user preference and city
        city_old = scores.loc[city, columns].values.reshape(1, -1)
        score = cosine_similarity(city_old, user)
        values.append(score[0][0])

    sim = pd.Series(values, index=scores.index)
    answer = sim.sort_values(ascending=False).astype(float).idxmax()
    return answer

# Setup Flask routes
@application.route('/')
def home():
    return render_template('index.html')

@application.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_pref = data['preferences']
    df = load_data('cleaned_qual_of_life.csv')

    invert = ['Cost of Living', 'Pollution']
    df = invert_values(df, invert)

    columns = list(user_pref.keys())
    scores = df.set_index('City')[columns].round().astype(int)
    user = np.array([user_pref[col] for col in columns])

    recommended_city = find_similarity(columns, user, scores)
    return jsonify({'city': recommended_city})

if __name__ == '__main__':
    application.run()
