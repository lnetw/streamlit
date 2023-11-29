import datetime
import pickle
import settings
import utils
import pandas as pd
import streamlit as st
import plotly.express as px
# Base config page
st.set_page_config(page_title="Temperature forcast app", layout="wide")
# Add gif
row0_col1, row0_col2, row0_col3 = st.columns(3)
row0_col3.image(settings.image_path, use_column_width='never', width=150)
# Add title
st.markdown("<h1 style='text-align: center; color: white;'>Temperature forcast dashboard</h1>",
            unsafe_allow_html=True)
# Read models
model = pickle.load(open(settings.model_path, 'rb'))
scaler = pickle.load(open(settings.scaler_path, 'rb'))
# Read data
df_raw = pd.read_csv(settings.view_path)
df_raw['date'] = pd.to_datetime(df_raw['date'])
# Predict mean temperature
data_to_predict, date = utils.prepare_data(df_raw, scaler)
mean_temp = utils.predict_temprature(data_to_predict, model)
df_predict = pd.DataFrame({'date': date, 'meantemp': mean_temp})
# Prepare data for visualization
df_all = df_raw.drop([0, 1], axis=0)
df_all['date'] = pd.to_datetime(df_all['date'])
df_all = df_all.rename(columns={'date': 'Date', 'meanpressure': 'Mean Pressure',
                                'humidity': 'Humidity', 'wind_speed': 'Wind Speed',
                                'meantemp': 'Mean Temperature'})
# Visualization data section
with st.expander("See all data"):
    st.dataframe(df_all, use_container_width=True)
# Slider for choosing time range
time_delta = st.slider(
    "Choose a range for meantemp",
    min_value=df_predict['date'].min().date(),
    max_value=df_predict['date'].max().date(),
    value=(df_predict['date'].min().date(), df_predict['date'].max().date()),
    format="YYYY/MM/DD",)
# Gpahs section
graphs = st.container()
with graphs:
    df_to_grpah = df_predict[(df_predict['date'] >= pd.to_datetime(time_delta[0])) &
                             (df_predict['date'] <= pd.to_datetime(time_delta[1]))]
    row1_col1, row1_col2 = st.columns(2)
    row1_col1.subheader('History temperature forcast')
    fig = px.line(
        df_to_grpah,
        x="date",
        y="meantemp",
        color_discrete_sequence=["#4BB0FF"])
    fig.update_xaxes(title_text="Temperature")
    fig.update_yaxes(title_text="Date")
    fig.update_layout(showlegend=False)
    row1_col1.plotly_chart(fig, theme="streamlit", use_container_width=True)

    row1_col2.subheader('Distribution of temperature')
    fig = px.bar(
        df_to_grpah['meantemp'].round(0).value_counts(),
        color_discrete_sequence=["#4BB0FF"],)
    fig.update_xaxes(title_text="Temperature")
    fig.update_yaxes(title_text="Count")
    fig.update_layout(showlegend=False)
    row1_col2.plotly_chart(fig, theme="streamlit", use_container_width=True)
# Add value section
add_value = st.container()
with add_value:
    metric_col, sub_header_col = st.columns((1, 3))
    sub_header_col.subheader(
        f"Add value for forcast temperature on {df_predict['date'].max().date() + datetime.timedelta(days=1)}")
    metric_col.metric(label=f"Mean temperature on {df_predict['date'].max().date()}",
                      value=f"{round(df_predict['meantemp'].values[-1], 2)} °C",
                      delta=f"{round(df_predict['meantemp'].values[-1] - df_predict['meantemp'].values[-2], 2)} °C")
    value_col1, value_col2, value_col3, value_col4 = st.columns(4)
    humidity = value_col2.number_input('Insert a humidity', min_value=0,
                                       max_value=100, value=None, placeholder="Type a value of humidity")
    wind_speed = value_col3.number_input('Insert a wind speed', min_value=0,
                                         max_value=50, value=None, placeholder="Type a value of wind speed")
    meanpressure = value_col4.number_input('Insert a mean pressure', min_value=0,
                                           max_value=1500, value=None, placeholder="Type a value of wind speed")
    wihte_space, bottom = st.columns((8, 1))
    with bottom:
        action = st.button('Add value in dataframe')
    if action:
        if humidity is None or wind_speed is None or meanpressure is None:
            st.warning(
                'Please insert a value in humidity, wind speed and mean pressure')
        else:
            # Predict mean temperature and add new value
            mean_temp = utils.construct_and_predict_new_temprature(humidity, wind_speed,
                                                                   df_predict['meantemp'].values[-2],
                                                                   df_predict['meantemp'].values[-1],
                                                                   scaler, model)
            df_raw.loc[len(df_raw)] = [df_raw['date'].max() + datetime.timedelta(days=1),
                                       mean_temp, humidity, wind_speed, meanpressure]
            # Update view file
            df_raw.to_csv(settings.view_path, index=False)
