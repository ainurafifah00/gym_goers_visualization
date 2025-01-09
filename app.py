from pathlib import Path 

import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import altair as alt


#---- PATH SETTINGS ------
THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ASSETS_DIR = THIS_DIR/ "assets"
STYLES_DIR = THIS_DIR/ "styles"
CSS_FILE = STYLES_DIR / "main.css"


# --- GENERAL SETTINGS ---
STRIPE_CHECKOUT = "https://buy.stripe.com/6oEdRj2Jp6I29qw3cd"
CONTACT_EMAIL = "ainurafifah57@gmail.com"
DEMO_VIDEO = "https://www.youtube.com/watch?v=5if4cjO5nxo&pp=ygUXZ3ltIHJvdXRpbmUgc2hvcnQgdmlkZW8%3D"
PRODUCT_NAME = "The Fitness Hive"
PRODUCT_TAGLINE = "A hub of group energy and personal strength. 🏋🏽🔥💪🏼"
PRODUCT_DESCRIPTION = """
**At The Fitness Hive, we believe in fostering a vibrant fitness community while supporting your individual goals.** 
- Join our group classes to stay motivated or use our state-of-the-art strength equipment for solo workouts. 
- Membership optional—pay per session or enjoy exclusive benefits with our flexible plans.
"""

def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#--- PAGE CONFIG ---
st.set_page_config(
    page_title=PRODUCT_NAME,
    page_icon=":star",
    layout="centered",
    initial_sidebar_state="collapsed",
    )

load_css_file(CSS_FILE)

#--- MAIN SECTION --
st.header(PRODUCT_NAME)
st.subheader(PRODUCT_TAGLINE)
left_col, right_col = st.columns((2,1))
with left_col:
    st.text("")
    st.write(PRODUCT_DESCRIPTION)
    st.markdown(
        f'<a href={STRIPE_CHECKOUT} class="button"> Book your class today </a>',
        unsafe_allow_html=True)

with right_col:
    product_image = Image.open(ASSETS_DIR / "gym-interior-with-equipments-2.jpg")
    st.image(product_image, width=450)



#--- FEATURES ----
st.write("")
st.write("----")
st.subheader("🧘🏽‍♀️ Our classes")
features = {
    "yoga.jpg": [
        "Find Your Inner Balance with Yoga",
        "Unwind and rejuvenate with our yoga classes. Perfect for all levels, these sessions enhance flexibility, \
        relieve stress, and boost mental clarity.",
    ],
    "hiit_gym.jpeg": [
        "Push Your Limits with HIIT & CrossFit",
        "Burn calories and build strength fast with high-intensity interval training and dynamic CrossFit workouts. \
        Perfect for those seeking maximum results in minimal time."
    ],
    "treadmill.jpg": [
        "Build Power and Confidence with Strength Training",
        "Enhance muscle tone and overall fitness with our expert-led strength training classes. \
         Ideal for sculpting your body and boosting your physical endurance."
    ]
}

for image, description in features.items():
    image = Image.open(ASSETS_DIR / image)
    st.write("")
    left_col, right_col = st.columns(2)
    left_col.image(image, use_column_width=True)
    right_col.write(f"**{description[0]}**")
    right_col.write(description[1])



# --- DEMO ---
st.write("")
st.write("---")
st.subheader(":tv: Demo")
st.video(DEMO_VIDEO, format="video/mp4", start_time=0)





# 3. Placement of Existing Visualizations
# Workout Calories Burned Visualization: Place this in the "Group Classes" or "Why Choose Us" section to highlight the effectiveness of classes.
# Water Intake Visualization: Add it to a "Wellness Tips" or "Member Resources" section to emphasize holistic fitness and care.

# 4. Additional Visualization Ideas
# Muscle Engagement by Exercise Type: A visual guide showing which muscle groups are targeted by specific workouts.
# Progress Tracker Sample: Interactive visualization showing how members have achieved milestones like weight loss or strength gains.
# Class Popularity and Timing Chart: A heatmap or graph showing the best times to join popular group classes to inspire scheduling.




# --- VISUALIZATIONS ---
st.write("")
st.write("---")
st.subheader("🤝 Why Choose Us?")


#Load data - CSV to dataframe
df = pd.read_csv('data/gym_members_exercise_tracking_cleaned.csv')
df.session_duration_mins = df.session_duration_mins.astype('int')


avg_bmi = df['BMI'].mean(axis=0)
avg_bpm = df['Resting_BPM'].mean(axis=0)
avg_fat = df['Fat_Percentage'].mean(axis=0)

st.markdown("### Our Members Performance")
col1, col2, col3 = st.columns(3)
col1.metric("BMI", round(avg_bmi,2), "-2.3")
col2.metric("Resting BPM", round(avg_bpm,2), "3.0")
col3.metric("Fat percentage", round(avg_fat,2), "-4%")


st.markdown("### Find Your Ideal Workout")
st.markdown("#### Which Workout Burns the Most Calories?")
workout_list = df.Workout_Type.unique()
workout_selection = st.multiselect('Select workout type', workout_list, ['Yoga', 'HIIT', 'Cardio', 'Strength'])

session_selection = st.slider('Select session duration (mins)', 30, 120, (45,60), 5)
session_selection_list = list(np.arange(session_selection[0], session_selection[1]+1))
print(session_selection_list)

#Subset data - Filter dataframe based on selections
df_selection = df[df.Workout_Type.isin(workout_selection) & df['session_duration_mins'].isin(session_selection_list)]
reshaped_df = df_selection.pivot_table(index='session_duration_mins', columns='Workout_Type', values='Calories_Burned', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='session_duration_mins', ascending=True)

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


# --- FAQ ---
st.write("")
st.write("---")
st.subheader(":raising_hand: FAQ")
faq = {
    "Do I need a membership to use the gym or attend classes?": 
    "No, you can pay per session for classes or equipment usage. Memberships offer added benefits like discounts, priority bookings, and exclusive access to events.",
    "What kind of classes do you offer?":
    "We offer group classes like yoga, HIIT & CrossFit, and strength training. These classes are designed to cater to all fitness levels and help you achieve your fitness goals.",
    "Can beginners join the gym and classes?":
    "Absolutely! Our gym and classes are beginner-friendly, with professional trainers to guide you every step of the way.",
    "What equipment is available for solo workouts?":
    "We provide a wide range of strength and cardio equipment, including treadmills, ellipticals, free weights, resistance machines, and more.",
    "Are personal trainers available?":
    "Yes, personal trainers are available to help design customized workout plans tailored to your individual needs and goals. Additional fees may apply."
}

for question, answer in faq.items():
    with st.expander(question):
        st.write(answer)


# --- CONTACT FORM ---
# video tutorial: https://youtu.be/FOULV9Xij_8
st.write("")
st.write("---")
st.subheader(":mailbox: Have A Question? Ask Away!")
contact_form = f"""
<form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit" class="button">Send ✉</button>
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)





























