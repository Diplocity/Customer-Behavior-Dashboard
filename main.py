import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load your CSV file here
# Replace 'your_data.csv' with the actual path to your CSV file
df = pd.read_csv('starbucks  - Transactional data.csv')

# Clean column names by stripping any extra spaces
df.columns = df.columns.str.strip()

# Check the CSV columns to ensure they match what you're using in the plot
print(df.columns)

# Group by Age and calculate the average purchase
df_age_grouped = df.groupby('Age', as_index=False)['Average Purchase ($)'].mean()

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a line chart that demonstrates how average spending changes with customer age
line_fig = px.line(df_age_grouped,
                   x='Age',
                   y='Average Purchase ($)',
                   title='Average Spending by Age Group',
                   labels={'Age': 'Customer Age', 'Average Purchase ($)': 'Average Purchase ($)'})

# Create the Scatter Plot: Age vs. Frequency with Size and Color
scatter_fig = px.scatter(df,
                         x='Age',
                         y='Frequency (for visits)',
                         size='Average Purchase ($)',
                         color='Gender',
                         title='Scatter Plot: Age vs. Visit Frequency with Spending',
                         labels={'Age': 'Customer Age', 'Frequency (for visits)': 'Visit Frequency',
                                 'Average Purchase ($)': 'Average Purchase ($)'},
                         hover_data=['Name'])

# Create the Bar Chart: Average Purchase by Gender
bar_fig = px.bar(df,
                 x='Gender',
                 y='Average Purchase ($)',
                 title='Bar Chart: Average Purchase by Gender',
                 labels={'Gender': 'Customer Gender', 'Average Purchase ($)': 'Average Purchase ($)'})

# Create the Pie Chart: Distribution of Gender and Average Purchase Ranges
df['Purchase Range'] = pd.cut(df['Average Purchase ($)'], bins=[0, 20, 50, 100, 200, 500, 1000],
                              labels=['$0-$20', '$21-$50', '$51-$100', '$101-$200', '$201-$500', '$501+'])

pie_fig = px.pie(df,
                 names='Purchase Range',
                 title='Pie Chart: Distribution of Average Purchase Ranges',
                 labels={'Purchase Range': 'Purchase Range'})

# Define the layout of the app
app.layout = html.Div([
    html.H1("Customer Behavior Dashboard"),

    # Scatter plot
    dcc.Graph(
        id='scatter-plot',
        figure=scatter_fig
    ),

    # Line graph (average spending by age group)
    dcc.Graph(
        id='line-plot',
        figure=line_fig
    ),

    # Bar graph
    dcc.Graph(
        id='bar-graph',
        figure=bar_fig
    ),

    # Pie chart with added purchase range data
    dcc.Graph(
        id='pie-chart',
        figure=pie_fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
