#analysis.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

# Read the CSV data
top_movies_file = 'public/top_movies_by_year.csv'
movies_rating_file = 'public/movies_rating.csv'
top_movies_data = pd.read_csv(top_movies_file)
movies_rating_data = pd.read_csv(movies_rating_file)

# Initialize the Dash app
app = dash.Dash(__name__)
#app = dash.Dash(__name__, external_stylesheets=['/src/analysis.css'])
#app = dash.Dash(__name__, url_base_pathname='/data_analysis/')

# Layout of the Dash app
app.layout = html.Div(style={'backgroundColor': '#2C343F', 'color': 'white'}, children=[
    dcc.Graph(
        id='rating-chart',
        figure=px.line(top_movies_data, x='Year', y='Average', labels={'Average': 'Average Rating'})
            .update_traces(
                mode='markers+lines',
                marker=dict(size=6.5, color='#F27405'),  # Set marker color
                line=dict(color='#00B021'),  # Set line color
            )
            .update_layout(
                plot_bgcolor='#556678',  # Set line graph background color
                paper_bgcolor='#2C343F',  # Set figure background color
                xaxis=dict(
                    title=dict(text='Year', font=dict(color='white')),
                    tickfont=dict(color='white'),
                    tickmode='linear',
                    tick0=top_movies_data['Year'].min(),
                    dtick=5,
                ),
                yaxis=dict(title=dict(text='Average Rating', font=dict(color='white')), tickfont=dict(color='white')),  # Set y-axis title and tick color
                title=dict(text="Average Ratings Over the Years", font=dict(color='white', size=22), x=0.5, y=0.95),  # Add centered title
                annotations=[
                    dict(
                        x=0.5,
                        y=1.06,
                        xref='paper',
                        yref='paper',
                        showarrow=False,
                        text="Click a Point to view more information about the Year",
                        font=dict(size=12, color='lightgray'),
                    )
                ],
            ),
        style={'backgroundColor': '#14171c'}
    ),
    html.Hr(style={'backgroundColor': 'white'}),
    html.Div(id='chart-info-box', style={'marginTop': '20px'}),
])

# Callback for updating the info box when a point is clicked
@app.callback(
    Output('chart-info-box', 'children'),
    [Input('rating-chart', 'clickData')]
)
def update_info_box(click_data):
    if click_data is None:
        return ""

    year = click_data['points'][0]['x']
    selected_year_data = top_movies_data[top_movies_data['Year'] == year].iloc[0]

    # Fetch additional information about the top movies for the clicked year
    top_movies_titles = eval(selected_year_data['Movies'])
    
    # Filter movies_rating_data based on title and year
    top_movies_info = movies_rating_data[
        (movies_rating_data['Title'].isin(top_movies_titles)) & 
        (movies_rating_data['Year'] == year)
    ]

    # Create a list of Div elements for each top movie
    top_movies_divs = []
    for index, movie_info in top_movies_info.iterrows():
        movie_div = html.Div([
            html.H4(movie_info['Title'], style={'font-size':'17px'}),
            html.Img(src=movie_info['Poster'], alt=movie_info['Title'], style={'width': '100px', 'height': '150px'}),
            html.P(f"Rating: {movie_info['Rating']}"),
            html.P(f"Director(s): {', '.join(eval(movie_info['Director']))}"),
            html.P(f"Genres: {', '.join(eval(movie_info['Genres']))}")
        ], style={'marginRight': '20px'})
        top_movies_divs.append(movie_div)

    info_box_content = html.Div([
        html.H3(f"Year: {year}", style={'textAlign': 'center'}),
        html.P(f"Average Rating: {selected_year_data['Average']:.2f}", style={'textAlign': 'center'}),
        html.P(f"Total Rated Movies: {selected_year_data['Total']}", style={'textAlign': 'center'}),
        #html.Hr(style={'backgroundColor': 'white'}),
        html.H4("Top Movies for the Year:", style={'textAlign': 'center', 'font-size': '20px'}),
        html.Div(top_movies_divs, style={'display': 'flex', 'justifyContent': 'center'}),
    ], style={'backgroundColor': '#2C343F', 'padding': '10px', 'borderRadius': '5px', 'textAlign': 'center'})

    return info_box_content


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
