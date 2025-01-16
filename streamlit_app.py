import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Book an appointment with the best local GP")

st.write("We are a diverse group of 35 exceptional GPs, each bringing their own unique expertise, perspective, and approach to patient care, and together creating an unrivalled depth and breadth of experience as a team.")
st.write("Chat privately with our AI to work out which of our GPs are the best match for your immediate or long term healthcare needs and goals.")

if "answers" not in st.session_state: 
    st.session_state.answers = []

client = OpenAI(api_key=st.secrets["openai_key"])
def submit_enquiry():
    prompt = f"You are the receptionist at Turn The Corner doctors. Respond to the following patient enquiry with 3 answers, each from a fictional TV doctor or Dr. Tamsin Franklin of Turn The Corner, each giving an in-character response to the enquiry. For each response, include a statement of which location(s) from the enquiry the doctor works at, and when the doctor is available for an appointment. Do not respond with anything apart from the 3 doctor answers, and separate each response with the string <hr>. Here's the enquiry: {enquiry}."

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    response_dict = ai_response.model_dump()
    message_content = response_dict["choices"][0]["message"]["content"]

    st.session_state.answers = message_content.split('<hr>')

history = st.selectbox(
    'Firstly, have you been to a Turn The Corner clinic before?',
     ['', 'Existing patient', 'New patient']
)

if history:

    location_array = ['Northcote', 'Brunswick', 'Fairfield']
    if history == 'Existing patient':
        location_array.append('Telehealth / online')

    locations = st.multiselect(
        'Great! Which Turn The Corner locations can you get to?',
        location_array
    )

    if locations:
        gender_pref = st.selectbox(
            'And do you have a preference for a male or female GP?',
            ['No preference', 'Male', 'Female']
        )

        if gender_pref:

            reason_array = ['', 'General 30 minute consult (adult)', 'General 30 minute consult (baby)', 'General 15 minute consult (child)', 'General 30 minute consult (child)', 'Pregnancy', '6 week post-partum', 'Mental Health', 'Travel']
            if history == 'Existing patient':
                reason_array.append('Repeat prescription')
                reason_array.append('Specialist referral')

            reason = st.selectbox(
                'What is your reason for seeing a GP?',
                reason_array
            )

            if reason:
                target = 'the best GP'
                if gender_pref == 'Male':
                    target = 'the best male GP'
                elif gender_pref == 'Female':
                    target = 'the best female GP'

                location_str = ' or '.join(locations)

                if reason.startswith('General'):
                    enquiry_value = f'Hi, I\'m looking for {target} in {location_str} for a {reason}.'        
                    enquiry_question = 'Finally, add some details about your health issues and goals.'
                    
                else:
                    enquiry_value = f'Hi, I\'m looking for {target} in {location_str} with expertise in: {reason}.'        
                    enquiry_question = 'Finally, add anything else you want to share with us.'

                enquiry = st.text_area(f'{enquiry_question} Your name and contact details are not required at this stage. Click submit to find your best matching GPs and their available appointment times:', enquiry_value)
                st.button('Submit', type="primary", on_click=submit_enquiry)

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

    tamsin_link = 'https://www.hotdoc.com.au/request/appointment/doctor-time?clinic=turn-the-corner-medical-clinic-fairfield&doctor=dr-tamsin-franklin-2&for=you&history=return-visit&reason=185834'

    # Display each answer in its respective column
    for idx, (col, answer) in enumerate(zip(cols, st.session_state.answers)):

        with col:

            if 'Dr. Tamsin Franklin' in answer:
                answer = answer.replace('Dr. Tamsin Franklin', f'<a href="{tamsin_link}" target="_blank">Dr. Tamsin Franklin</a>')
                st.html(f'<a href="{tamsin_link}" target="_blank"><img src="https://d3sjaxzllw9rho.cloudfront.net/doctor_images/202747/profile_a28e2326e1dab97511dabcc809d6c321.jpeg" width="100%" /></a>')

            st.markdown(answer, unsafe_allow_html=True)

            st.link_button("Book Appoinment", type="primary", url=tamsin_link)

            if 'Dr. Tamsin Franklin' in answer:
                st.html('<hr>')
                st.html('<b>Recent reviews</b>')
                st.html('<em>"Excellent Advisor - Stanford GSB Admit (Class Of 2027)"</em>')
                st.html('⭐⭐⭐⭐⭐ <small><a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">3 weeks ago</a></small>')
                st.html('<em>"Best Coach I Could Have Asked For! Best Coach! (Stanford / Columbia)"</em>')
                st.html('⭐⭐⭐⭐⭐ <small><a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">1 month ago</a></small>')
                st.html('<a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">More...</a>')

                st.html('<hr>')
                st.html('<b>Recent articles by Dr. Franklin</b>')
                st.html('<a href="https://fortunaadmissions.com/how-to-create-a-career-vision-for-your-mba-application/" target="_blank">How to Create a Career Vision For Your MBA Application</a>')
                st.html('<a href="https://fortunaadmissions.com/how-to-create-an-mba-career-vision-long-term-vs-short-term-goals/" target="_blank">MBA Goals: Long Term Vs. Short Term Career Vision</a>')
                st.html('<a href="https://fortunaadmissions.com/author/heidi/" target="_blank">More...</a>')           
