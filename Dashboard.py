import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Set up page configuration
st.set_page_config(
    page_title="Data Display",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# This is an example app!"
    }
)

# Include Bootstrap
components.html("""
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", height=0)

# Create sidebar with buttons
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #3498db;'>Data Selection</h1>", unsafe_allow_html=True)
    selection = st.radio('Choose Data', ('Funded', 'Self Owned'))

# Display data based on selection
if selection == 'Funded':
    st.subheader('Funded Data')
    
   
elif selection == 'Self Owned':
    st.subheader('Self Owned Data')

    # Import dataset
    file_path = 'C:/Users/Vaidehi/Documents/DataAnalysis.csv'  # Replace with your actual file path
    data = pd.read_csv(file_path)
    #st.dataframe(data)

    # Filter the data for self-owned companies
    self_owned_data = data[data['Investor'] == 'Self Owned']
    st.write('Filtered Self Owned Data: ', self_owned_data)

    # Create a dropdown for self-owned company names
    company_names = self_owned_data['Company'].unique().tolist()
    selected_company = st.selectbox('Select a company', company_names)

    # Create a button for displaying profit
    # Other parts of the code remain the same

    # Create a button for displaying profit
    if st.button('No Knowledge'):
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
    