import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Book an appointment with the best local GP")

st.write("We are a team of 35 amazing GPs, who together bring an unrivalled breadth and depth of experience.")
st.write("Chat privately with our AI to work out which of our GPs are the best match for your immediate or long term healthcare needs and goals.")

if "answers" not in st.session_state: 
    st.session_state.answers = []

client = OpenAI(api_key=st.secrets["openai_key"])
def submit_enquiry():
    prompt = f"You are the receptionist at Turn The Corner doctors. Respond to the following patient enquiry with 3 answers, each from a fictional TV doctor or Dr. Tamsin Franklin of Turn The Corner, each giving an in-character response to the enquiry. For each response, include a statement of which location(s) from the enquiry the doctor works at, and when the doctor is available for an appointment. Separate each response with the string <hr>. Here's the enquiry: {enquiry}."

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    response_dict = ai_response.model_dump()
    message_content = response_dict["choices"][0]["message"]["content"]

    st.session_state.answers = message_content.split('<hr>')

new_existing_option = st.selectbox(
    'Firstly, have you been seen at Turn The Corner before?',
     ['Existing patient', 'New patient']
)

if new_existing_option:

    locations = st.multiselect(
        'Great! Which Turn The Corner locations can you get to?',
        ['Northcote', 'Brunswick', 'Fairfield']
    )

    if locations:
        gender_pref = st.selectbox(
            'And do you have a preference for a male or female GP?',
            ['No preference', 'Male', 'Female']
        )

        if gender_pref:

            goals = st.text_area('What are your health issues and goals?')

            if goals:
                target = 'the best GP'
                if gender_pref == 'Male':
                    target = 'the best male GP'
                elif gender_pref == 'Female':
                    target = 'the best female GP'

                location_str = ' or '.join(locations)
                enquiry_value = f'Hi, I\'m looking for {target} in {location_str} with expertise in: {goals}.'        
                enquiry = st.text_area('Finally, add anything else you want to share with us. Your name and contact details are not required at this stage. Click submit to find your best matched GPs and their available appointment times:', enquiry_value)

                submit_button = st.button('Submit', type="primary", on_click=submit_enquiry)

if st.session_state.answers:
    st.markdown(
        """
        <style>
        .stColumn {
            padding: 10px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            height: 500px;
            overflow: scroll;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    cols = st.columns(len(st.session_state.answers))

    # Display each answer in its respective column
    for idx, (col, answer) in enumerate(zip(cols, st.session_state.answers)):

        with col:

            if 'Heidi Hillis' in answer:
                answer = answer.replace('Heidi Hillis', '<a href="https://fortunaadmissions.com/team-member/heidi-hillis/" target="_blank">Heidi Hillis</a>')
                st.html('<a href="https://fortunaadmissions.com/team-member/heidi-hillis/" target="_blank"><img src="https://poetsandquants.com/wp-content/uploads/sites/5/2015/11/Headshots-420x420.jpg" width="100%" /></a>')

            st.markdown(answer, unsafe_allow_html=True)

            name = st.text_input('Name', key=f'name-{idx}')
            email = st.text_input('Email', key=f'email-{idx}')
            enquiry_button = st.button('Submit', key=f'submit-{idx}', type="primary")

            if 'Heidi Hillis' in answer:
                st.html('<hr>')
                st.html('<b>Recent reviews</b>')
                st.html('<em>"Excellent Advisor - Stanford GSB Admit (Class Of 2027)"</em>')
                st.html('⭐⭐⭐⭐⭐ <small><a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">3 weeks ago</a></small>')
                st.html('<em>"Best Coach I Could Have Asked For! Best Coach! (Stanford / Columbia)"</em>')
                st.html('⭐⭐⭐⭐⭐ <small><a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">1 month ago</a></small>')
                st.html('<a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">More...</a>')

                st.html('<hr>')
                st.html('<b>Recent articles by Heidi</b>')
                st.html('<a href="https://fortunaadmissions.com/how-to-create-a-career-vision-for-your-mba-application/" target="_blank">How to Create a Career Vision For Your MBA Application</a>')
                st.html('<a href="https://fortunaadmissions.com/how-to-create-an-mba-career-vision-long-term-vs-short-term-goals/" target="_blank">MBA Goals: Long Term Vs. Short Term Career Vision</a>')
                st.html('<a href="https://fortunaadmissions.com/author/heidi/" target="_blank">More...</a>')
