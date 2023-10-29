import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit.components.v1 as components
import plotly.express as px


st.set_page_config(
    page_title="Data Display",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        #'About': "# This is an example app!"
    }
)

# Include Bootstrap
components.html("""
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", height=0)


df = pd.read_csv('C:/Users/Vaidehi/Documents/DataAnalysis.csv')
# Title for your Streamlit app

# Add a sidebar for selecting filters
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #3498db;'>Item Selection</h1>", unsafe_allow_html=True)
    selection = st.radio('Choose Items', ('Home','Funded', 'Self Owned'))

# Display data based on selection
if selection == 'Home':
    st.title('Number of Rows per Industry')

    # Group data by industry and count the number of rows
    industry_counts = df['Industry'].value_counts()

    # Create a bar plot
    st.bar_chart(industry_counts)

    # Display the DataFrame (optional)
    st.write(df)

    # Show the plot
    # st.pyplot() 

    date_counts = df['Year'].value_counts()

    # Create a bar chart
    st.bar_chart(date_counts)

    # Show the plot
    # st.pyplot()
    

    # # Create a Streamlit app
    # st.title('Location-wise Distribution of the Top 100 Startups')

    # # Group the data by location (Country and City) and count the number of startups
    # location_distribution = top_100_startups.groupby(['Country', 'City']).size().reset_index(name='Startup Count')

    # # Display the location-wise distribution in a Streamlit table
    # st.table(location_distribution)






    # Create a Streamlit app
    

elif selection == 'Funded':
    st.subheader('Funded Data')
    st.sidebar.title('Filters')

    top_10_startups = df.sort_values(by='Revenue_final', ascending=False).head(10)
    st.title('Top 10 Startups in Terms of Revenue')

    # Display the top 10 startups in a Streamlit table
    st.table(top_10_startups[['Company', 'Revenue_final']])



    top_100_startups = df.sort_values(by='Revenue_final', ascending=False).head(100)

    # Add a dropdown menu to select a city
    st.title('Location-wise Distribution of the Top 100 Startups')
    selected_city = st.sidebar.selectbox('City Selector', ['All'] + top_100_startups['City'].unique().tolist())

    # Add a dropdown menu to select the attributes to display
    selected_attributes = st.sidebar.multiselect('Attribute Selector', ['Company', 'Country', 'City', 'Revenue_final'], default='Company')

    # Filter the data based on the selected city
    if selected_city != 'All':
        filtered_startups = top_100_startups[top_100_startups['City'] == selected_city]
    else:
        filtered_startups = top_100_startups

    # Display the selected attributes in a Streamlit tab
    # Sidebar for filtering by industry
    industry = st.sidebar.selectbox("Select Industry", df['Industry'].unique())

  



    
    filtered_data = df[df['Industry'] == industry]
    st.title("Valuation Analysis")
    st.subheader("Line Plot: Valuation Over Time")
    st.line_chart(filtered_data, x='Year', y='Valuation')

    # Scatter plot for Valuation vs. Revenue
    # st.subheader("Scatter Plot: Valuation vs. Revenue")
    # fig, ax = plt.subplots(figsize=(10, 5))
    # sns.scatterplot(x='Revenue_final', y='Valuation', data=filtered_data, marker='o', color='r', ax=ax)
    # ax.set_xlabel('Revenue_final')
    # ax.set_ylabel('Valuation')
    # st.pyplot(fig)
    # # filtered_data = df[df['Industry'] == 'AI']
    filtered_data = df[df['Industry'] == industry]

    # Create the scatter plot
    color = st.color_picker('Select a color:', '#ffaa00')

    # Create the scatter plot
    st.scatter_chart(
        data=df,
        x='Revenue_final',
        y='Valuation',
        color=color,
    )

    st.header("Treemap Visualization")
    df['Funding_Final'].fillna(0, inplace=True)


    fig = px.treemap(df, path=['Funding_Final', 'Industry'], values='Valuation',
                    title="Foreign vs. Domestic Funds by Sector")

    st.plotly_chart(fig)

    
    st.header("Stacked Bar Chart")

    fig = px.bar(df, x='Industry', y='Funding_Final', color='Funding_Final', title="Foreign vs. Domestic Funds by Sector",
                labels={'Amount': 'Investment Amount'})

    st.plotly_chart(fig)


    #4 stacked bar chart based on profit
    current_year = 2023
    df = df[df['Year'] >= current_year - 5]

    # Title of the dashboard
    st.title("Valuation-Based Analysis on Fintech Companies (Last 5 Years)")

    # Stacked bar chart to visualize valuation and profit
    st.header("Stacked Bar Chart")

    fig = px.bar(df, x='Company', y='Profit', color='Valuation',
                title="Fintech Companies Valuation and Profit (Last 5 Years)",
                labels={'Profit': 'Profit (in millions)'}, barmode='stack')

    fig.update_xaxes(title_text="Company")
    fig.update_yaxes(title_text="Profit (in millions)")

    st.plotly_chart(fig)

    # Filter data for the pre-COVID period (2019)
    pre_covid_data = df[df['Year'] == 2019]

    # Filter data for the COVID period (2020-2022)
    covid_data = df[(df['Year'] >= 2020) & (df['Year'] <= 2022)]

    # # Calculate average profits for each industry in both periods
    pre_covid_avg_profits = pre_covid_data.groupby('Industry')['Profit'].mean()
    covid_avg_profits = covid_data.groupby('Industry')['Profit'].mean()

    # df = pd.read_csv('/content/DataAnalysis.csv')

    st.title("Funding Comparison by Industry: COVID vs. Non-COVID Time")

    # Filter the data for COVID time (2020-2022)
    covid_data = df[(df['Year'] >= 2020) & (df['Year'] <= 2022)]

    # Filter the data for non-COVID time (2018-2019, 2022-2023)
    non_covid_data = df[(df['Year'] >= 2018) & (df['Year'] <= 2019) | (df['Year'] >= 2022)]

    # Group data by Industry and sum the fundings for each period
    covid_fundings_by_industry = covid_data.groupby('Industry')['Funding_Final'].sum().reset_index()
    non_covid_fundings_by_industry = non_covid_data.groupby('Industry')['Funding_Final'].sum().reset_index()

    # Create a line chart with both lines
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(covid_fundings_by_industry['Industry'], covid_fundings_by_industry['Funding_Final'], color='red', label='COVID Time (2020-2022)')
    ax.plot(non_covid_fundings_by_industry['Industry'], non_covid_fundings_by_industry['Funding_Final'], color='blue', label='Non-COVID Time (2018-2019, 2022-2023)')
    ax.set_xlabel('Industry')
    ax.set_ylabel('Funding')
    ax.set_title('Funding Comparison by Industry: COVID vs. Non-COVID Time')
    ax.legend()
    ax.grid(True)

    # Rotate the x-axis labels to display industry names vertically
    plt.xticks(rotation=90)

    st.pyplot(fig)




    st.title("Startup Distribution by Industry")

    # Create a histogram with a transparent background and white bars
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(df['Industry'], bins=30, edgecolor='k', color='white', alpha=0.7)
    ax.set_xlabel('Industry')
    ax.set_ylabel('Number of Startups')
    ax.set_title('Startup Distribution by Industry')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability

    st.pyplot(fig)


    df = pd.read_csv('C:/Users/Vaidehi/Documents/DataAnalysis.csv')

    st.title("Funding Impact on Startup Growth")

    # Select a startup
    selected_startup = st.selectbox("Select a Startup", df['Company'].unique())

    # Filter the data for the selected startup
    startup_data = df[df['Company'] == selected_startup]

    # Create a line plot
    st.subheader(f'Valuation Over Time for {selected_startup}')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(startup_data['Year'], startup_data['Valuation'], marker='o', linestyle='-', color='b')
    ax.set_xlabel('Year')
    ax.set_ylabel('Valuation')
    ax.set_title(f'Valuation Over Time for {selected_startup}')
    ax.grid(True)
    plt.xticks(rotation=45)

    st.pyplot(fig)

    #6
    startup_counts = df['Industry'].value_counts().reset_index()
    startup_counts.columns = ['Industry', 'Count']

    # Bubble chart to visualize startup sectors and their counts
    st.header("Bubble Chart")

    fig = px.scatter(startup_counts, x='Industry', y='Count', size='Count', color='Industry',
                    hover_name='Industry', title="New and Emerging Startups by Industry")

    fig.update_xaxes(title_text="Industry")
    fig.update_yaxes(title_text="Number of Startups")

    st.plotly_chart(fig)

    #9
    industry = st.selectbox("Select a Industry", df['Industry'].unique())

    # Filter the data for the selected sector
    filtered_data = df[df['Industry'] == industry]

    # Line chart to visualize funding evolution
    st.header(f"Funding Evolution for {industry}")

    # Group data by 'Year' and calculate the total funding for the sector
    funding_evolution = filtered_data.groupby('Year')['Funding_Final'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(funding_evolution.index, funding_evolution.values, marker='o', linestyle='-', color='b')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Funding')
    ax.set_title(f'{industry} Funding Evolution Over Time')
    st.pyplot(fig)


        # extra one comparison between investors location and industry
    st.title("Investment Counts and Visualization by Investors' Location")

    # Create a filter to select the location (country)
    selected_location = st.selectbox("Select Location", df["Investor's Location"].unique())

    # Filter the data based on the selected location
    filtered_data = df[df["Investor's Location"] == selected_location]

    # Group the data by industry and count the number of investors
    investment_counts = filtered_data.groupby('Industry').size().reset_index(name='Count')

    # Create a table to display the investment counts
    st.header(f"Investment Counts for {selected_location}")

    st.write(investment_counts)

    # Create a bar chart to visualize the investment counts
    st.header("Investment Counts Visualization")

    fig = px.bar(investment_counts, x='Industry', y='Count', title=f"Investment Counts by Sector for {selected_location}")
    st.plotly_chart(fig)

    st.header("Investment Counts Pie Chart")

    pie_fig = px.pie(investment_counts, names='Industry', values='Count', title=f"Investment Counts by Sector for {selected_location}")
    st.plotly_chart(pie_fig)




    #10
    st.title("Startup Analysis")

    # Filter options
    st.markdown("## Filter Data")

    # Create columns for filters
    col1, col2, col3 = st.columns(3)

    # Place the filters in the columns
    industry = col1.multiselect("Select Industries", df['Industry'].unique())
    country = col2.multiselect("Select Countries", df['Country'].unique())
    stage = col3.multiselect("Select Stages", df['Stage'].unique())

    # Filter the data based on user selections
    filtered_data = df[
        (df['Industry'].isin(industry)) &
        (df['Country'].isin(country)) &
        (df['Stage'].isin(stage))
    ]

    # Display the filtered data
    st.subheader("Filtered Data")
    st.write(filtered_data)

    # Line chart to visualize startup trends
    st.header("Startup Trends")

    # Group data by 'Date' and 'Industry' and calculate the mean valuation
    trends_data = filtered_data.groupby(['Year', 'Industry'])['Valuation'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))

    for industry, data_group in trends_data.groupby('Industry'):
        ax.plot(data_group['Year'], data_group['Valuation'], label=industry)

    ax.set_xlabel('Year')
    ax.set_ylabel('Mean Valuation')
    ax.legend()
    st.pyplot(fig)
        
elif selection == 'Self Owned':
    st.subheader('Self Owned Data')

    # Import dataset
    file_path = 'C:/Users/Vaidehi/Documents/DataAnalysis.csv'  # Replace with your actual file path
    data = pd.read_csv(file_path)
    import webbrowser

    # Define the URL you want to open
    url_to_open = "http://localhost:8080/"

    # Create a Streamlit button
    if st.button("Go to Community"):
        webbrowser.open(url_to_open)
    # Filter the data for self-owned companies
    self_owned_data = data[data['Investor'] == 'Self Owned']
    st.write('Filtered Self Owned Data: ', self_owned_data)

    # Create a dropdown for self-owned company names
    company_names = self_owned_data['Company'].unique().tolist()
    selected_company = st.selectbox('Select a company', company_names)

    # Create a button for displaying profit
    if 'profit_displayed' not in st.session_state:
        st.session_state.profit_displayed = False

    st.title("Determine Your Favorite Industry")

    def extract_investor_location(location):
        if isinstance(location, str):
            parts = location.split(',')
            if len(parts) > 0:
                return parts[0]
        return None

    df["Investor Location"] = df["Investor's Location"].apply(extract_investor_location)

    selected_investor_location = st.selectbox("Select an Investor Location", df['Investor Location'].dropna().unique())

    filtered_df = df[df['Investor Location'] == selected_investor_location]

    industry_counts = filtered_df['Industry'].value_counts().reset_index()
    industry_counts.columns = ['Industry', 'Count']

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='Count', y='Industry', data=industry_counts, ax=ax)
    ax.set_xlabel('Count')
    ax.set_ylabel('Industry')
    ax.set_title(f'Investor Location: {selected_investor_location}')
    st.pyplot(fig)

    if st.button('No Knowledge'):
        st.session_state.profit_displayed = True

    if st.session_state.profit_displayed:
        # Group the data by start year and calculate the average profit
        profit_data = self_owned_data.groupby('Year')['Profit'].mean().reset_index()
        
        # Plot the line chart
        plt.figure(figsize=(10,5))
        plt.plot(profit_data['Year'], profit_data['Profit'], marker='o')
        plt.title('Average Profit Rate by Start Year')
        plt.xlabel('Year')
        plt.ylabel('Average Profit Rate')
        plt.grid(True)

        # Use st.pyplot() in Streamlit to display the figure
        st.pyplot(plt)







