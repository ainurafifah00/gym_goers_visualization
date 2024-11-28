import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

#Page title
st.set_page_config(page_title='Interactive Gym Data Explorer', page_icon='📊')
st.title('Gym Goers Dashboard')



#Load data - CSV to dataframe
df = pd.read_csv('data/gym_members_exercise_tracking_cleaned.csv')
df.session_duration_mins = df.session_duration_mins.astype('int')


avg_bmi = df['BMI'].mean(axis=0)
avg_bpm = df['Resting_BPM'].mean(axis=0)
avg_fat = df['Fat_Percentage'].mean(axis=0)

st.markdown("### General Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("BMI", round(avg_bmi,2), "-2.3")
col2.metric("Resting BPM", round(avg_bpm,2), "3.0")
col3.metric("Fat percentage", round(avg_fat,2), "-4%")


st.sidebar.header("Interactive Data Explorer")
#Workout selection - dropdown menu for genre selection
workout_list = df.Workout_Type.unique()
workout_selection = st.sidebar.multiselect('Select workout type', workout_list, ['Yoga', 'HIIT', 'Cardio', 'Strength'])

session_selection = st.sidebar.slider('Select session duration (mins)', 30, 120, (45,60), 5)
session_selection_list = list(np.arange(session_selection[0], session_selection[1]+1))
print(session_selection_list)

#Question Header
st.subheader(' Which Workout type burns most calories?')

#Subset data - Filter dataframe based on selections
df_selection = df[df.Workout_Type.isin(workout_selection) & df['session_duration_mins'].isin(session_selection_list)]
reshaped_df = df_selection.pivot_table(index='session_duration_mins', columns='Workout_Type', values='Calories_Burned', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='session_duration_mins', ascending=False)

#Editable dataframe -
df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
							column_config={'session_duration_mins': st.column_config.TextColumn('Session Duration')},
							num_rows='dynamic')

#Date prep for charting
df_chart = pd.melt(df_editor.reset_index(), id_vars='session_duration_mins', var_name='Workout_Type', value_name='Calories_Burned')


#Display line chart
# st.markdown("Line Chart")
chart = alt.Chart(df_chart).mark_line().encode(
			x=alt.X('session_duration_mins:N', title='Session (mins)'),
			y=alt.Y('Calories_Burned:Q', title='Calories Burned (kcal)'),
			color='Workout_Type:N').properties(height=320)

st.altair_chart(chart, use_container_width=True)

st.write('----------')

#Second question
st.subheader(" Water Intake According to Workout Type")


#Subset data - Filter dataframe based on selections
df_selection_water = df[df.Workout_Type.isin(workout_selection) & df['session_duration_mins'].isin(session_selection_list)]
reshaped_df_water = df_selection_water.pivot_table(index='session_duration_mins', columns='Workout_Type', values='Water_Intake', aggfunc='median', fill_value=0)
reshaped_df_water = reshaped_df_water.sort_values(by='session_duration_mins', ascending=False)

#Editable dataframe -
df_editor_water = st.data_editor(reshaped_df_water, height=212, use_container_width=True,
							column_config={'session_duration_mins': st.column_config.TextColumn('Session Duration')},
							num_rows='dynamic')

#Date prep for charting
df_chart_water = pd.melt(df_editor_water.reset_index(), id_vars='session_duration_mins', var_name='Workout_Type', value_name='Water_Intake')



# st.markdown("Bar chart")
bar_chart = alt.Chart(df_chart_water).mark_bar().encode(
		x=alt.X('session_duration_mins:N', title='Session Duration (mins)'),
			y=alt.Y('Water_Intake:Q', title='Water Intake (liter)'),
			color='Workout_Type:N').properties(height=320)
st.altair_chart(bar_chart, use_container_width=True)


left, middle, right = st.columns(3)
right.link_button("Go back to portfolio", "https://ainurafifah00.github.io/", type='primary')

