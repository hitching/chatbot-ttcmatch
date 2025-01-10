import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Turn The Corner - GP Match")

with st.chat_message("assistant"):
    st.write("Hi! I’m Dr. Tamsin Franklin. TTC is a team of 35 GPs, who together bring an unrivalled breadth of experience for your healthcare needs and goals.")
    st.write("Please answer some anonymous questions to help identify which of our GPs are the best match for your immediate or long term needs.")

if "ai_response" not in st.session_state: 
    st.session_state.ai_response = None

client = OpenAI(api_key=st.secrets["openai_key"])
def submit_enquiry():
    prompt = f"You are the receptionist at a doctors clinic. Respond to the following patient enquiry with 3 answers, each from a fictional TV doctor giving an in-character response to the enquiry. For each doctor's response, include a statement of which location(s) from the enquiry the doctor works at, and when the doctor is available for an appointment. Here's the enquiry: {enquiry}."

    st.session_state.ai_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )

matching_option = st.selectbox(
    'Firstly, do you want an appointment as soon as possible, or to find the best matched GP?',
     ['', 'I\'m okay with any GP', 'I\'m looking for the best matched GP']
)

if matching_option:

    who_option = None
    who_self_age = None
    who_partner_age = None

    if 'best matched' in matching_option:
        who_option = st.selectbox(
            'Who are you choosing a GP for?',
            ['', 'Myself', 'My family']
        )

        if who_option:
            who_self_age = st.selectbox(
                'What is your age?',
                ['', '18 to 25', '26 to 35', '36 to 45', '46 to 55', '56 to 65', '66 to 75', 'Over 75']
            )

        if who_option == 'My family':
            who_partner_age = st.selectbox(
                'Do you have a partner? What is their age?',
                ['', 'No', '18 to 25', '26 to 35', '36 to 45', '46 to 55', '56 to 65', '66 to 75', 'Over 75']
            )

    gender_pref = None
    if ('any GP' in matching_option) or (who_self_age and (who_option == 'Myself' or who_partner_age)):
        gender_pref = st.selectbox(
            'Do you have a preference for a male or female GP?',
            ['', 'No preference', 'Male', 'Female']
        )

        locations = []
        if gender_pref:
            locations = st.multiselect(
                'Which TTC locations can you get to?',
                ['Northcote', 'Brunswick', 'Fairfield']
            )

            goals = None
            if locations:
                goals = st.text_area('What are your health issues and goals?')

                if goals:
                    who_str = 'we\'re' if who_option == 'My family' else 'I\'m'


                    gender_str = ''
                    location_str = ' or '.join(locations)
                    
                    family_str = 'for my family' if who_option == 'My family' else ''
                    
                    criteria = []
                    if 'any GP' in matching_option:
                        criteria.append('availability as soon as possible')

                    criteria.append(f'expertise in: {goals}')
                    
                    criteria_str = ', and '.join(criteria)

                    enquiry_value = f'Hi, {who_str} looking for a {gender_str} GP in {location_str} {family_str} with {criteria_str}.'

                    enquiry = st.text_area('Finally, edit your enquiry and click submit to find your best matched GPs and their available appointments:', enquiry_value)

                    submit_button = st.button('Submit', type="primary", on_click=submit_enquiry)

if st.session_state.ai_response:
    with st.chat_message("assistant"):
        st.write_stream(st.session_state.ai_response)