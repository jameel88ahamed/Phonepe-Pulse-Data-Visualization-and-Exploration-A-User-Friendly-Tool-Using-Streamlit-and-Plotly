# Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly
This project aims to extract the data from PhonePe Pulse github repository and process it to obtain insights and information that can be visualized in a user-friendly manner.

## Introduction
PhonePe has become a leader among digital payment platforms, serving millions of users for their daily transactions. Known for its easy-to-use design, fast and secure payment processing, and creative features, PhonePe has gained praise and recognition in the industry. The PhonePe Pulse Data Visualization and Exploration project aims to gather valuable information from PhonePe's GitHub repository, process the data, and present it using an interactive dashboard that's visually appealing. This is accomplished using Python, Streamlit, and Plotly.

## REQUIRED LIBRARIES

+ import json
+ import pandas as pd
+ import psycopg2
+ import plotly.express as px
+ import plotly.graph_objects as go
+ import streamlit as st
+ from streamlit_option_menu import option_menu
+ import requests
+ from PIL import Image

## Steps:

### Step 1. Importing the Libraries:
Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install.

### Step 2. Data Extraction:
Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as JSON.

### Step 3. Data Transformation:
In this step the JSON files that are available in the folders are converted into the readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. In order to perform this step I've used os, json and pandas packages.
  
### Step 4. Database Insertion:
To insert the datadrame into SQL first I've created a new database and tables using psycopg2" library in Python to connect to a PostgreSQL database and insert the transformed data using SQL commands.
   
### Step 5. Dashboard Creation: Using Streamlit and Plotly to build an interactive dashboard.
To create colourful and insightful dashboard I've used Plotly libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in Pie, Bar, Geo map functions are used to display the data on a charts and map and Streamlit is used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.
   
### Step 6. Data Retrieval: 
Fetching data from the database and fetch the data into a Pandas dataframe to dynamically update the dashboard.


