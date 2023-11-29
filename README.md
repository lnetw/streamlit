# Temperature Dashboard using Streamlit

This project contains a dashboard showcasing the average temperature in Delphi, deployed using the Streamlit library. The project also includes a model for predicting heart temperature and analyzing the associated data in the provided Jupyter Notebook. The predictive model generates data and presents it on the dashboard, featuring visual data representation, graphs, and a filtering mechanism. Additionally, the dashboard allows for the supplementation of the dataset to enable further forecasting.


## Data Usage

The dashboard utilizes an open dataset from [Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white), specifically the [Daily Climate](https://www.kaggle.com/datasets/sumanthvrao/daily-climate-time-series-data)  dataset. This dataset contains information on meantemp and other climate-related variables in the city of Delhi from 2013 to 2017.


## Using framework

[Streamlit](https://streamlit.io) is a powerful library used for developing and deploying interactive, aesthetically pleasing, and scalable web pages with minimal lines of code. The framework provides various objects that aid in building your app and supports HTML, Markdown, and Plotly for expanding the frontend creation possibilities.


## Repository Structure

1. ``main_app.py`` - the main file for running the dashboard
2. ``utils.py`` - contains useful functions for the dashboard
3. ``settings.py`` - the settings file that contains paths to models and data
4. ``Research_notebook.ipynb`` - a notebook for data analysis and building the forecasting model
5. ``data`` - a folder containing datasets (train, test, and datasets for visualization)
6. ``models`` - a folder containing models (scaler and ML model)
7. ``image`` - a folder containing images for the dashboard
8. ``.streamlit`` - a folder containing configurations for deploying the project on Streamlit


## Deploying the Project on Streamlit.io

Streamlit not only serves as a powerful library for building web interfaces, but it also provides the opportunity to host projects on a website. After deployment, the user receives a unique URL with the format ``name_project.streamlit.io``. To take advantage of this feature, users need to consolidate their project into a single file (in this case, ``main_app.py``), prepare a requirements.txt file containing a list of all project dependencies, and set up a configuration file for Streamlit itself. More details about the deployment process can be found in the [documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app).


## Docker