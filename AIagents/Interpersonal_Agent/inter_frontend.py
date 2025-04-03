import base64
import streamlit as st
import requests

# Predefined question
question = (
    "Please provide one idea to enhance productivity and effectiveness when collaborating "
    "with the other two freelancers on the website creation project. Your idea should focus "
    "on improving communication and collaboration in a virtual setting, given that the team "
    "will be managing the project through Zoom for meetings and Microsoft Teams for daily interactions."
)

# Set wide layout
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        /* Remove top, bottom, left, right padding */
        .appview-container .main .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }

        /* Hide top navbar and footer (Optional) */
        header { visibility: hidden; }
        footer { visibility: hidden; }

        /* Reduce heading sizes */
        h1 { font-size: 18px !important; }
        h2 { font-size: 18px !important; }
        h3 { font-size: 16px !important; }
        h4 { font-size: 14px !important; }

        /* Reduce general text size */
        div.stMarkdown { font-size: 12px !important; }

        /* --- Button Styling (NEW) --- */
        .stButton > button {
            border: 1px solid #ccc !important; /* Grey border */
            border-radius: 5px !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            background-color: transparent !important;
            color: #000 !important;
            box-shadow: none !important;
        }
        
        .stButton > button:hover {
            border: 1px solid red !important;
            color: red !important;
            background-color: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Helper function to initialize session state
def initialize_session_state():
    if "ai_response" not in st.session_state:
        st.session_state.ai_response = None
    if "show_response" not in st.session_state:
        st.session_state.show_response = False
    if "user_idea" not in st.session_state:
        st.session_state.user_idea = ""
    if "resubmit_user_idea" not in st.session_state:
        st.session_state.resubmit_user_idea = ""
    if "idea_submitted" not in st.session_state:
        st.session_state.idea_submitted = False
    if "current_screen" not in st.session_state:
        st.session_state.current_screen = "consent_form"  # Start at consent form
    if "session_completed" not in st.session_state:
        st.session_state.session_completed = False  # Track if session is completed
    if "consent_given" not in st.session_state:
        st.session_state.consent_given = False # track is user give concent or not
    if " practice_idea" not in st.session_state:
        st.session_state.practice_idea = ""
    if "practice_submitted" not in st.session_state:
        st.session_state.practice_submitted = False


# Helper function to display the predefined question inside a single styled div
def display_predefined_question():
    # Apply custom CSS for centering and styling
    st.markdown(
        """
        <style>
        .question-container {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 0 auto;
            max-width: 900px;
            background-color: #f9f9f9;
            text-align: center;
        }
        .question-header {
            color: #336699;
            font-size: 24px;
            margin-bottom: 15px;
        }
        .question-text {
            font-size: 16px;
            line-height: 1.6;
            text-align: justify;
        }
        .center-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 40px auto;
            width: 100%;
        }
        .center-content {
            max-width: 80%;
            padding: 0 20px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="question-container">
            <h1 class="question-header">Interpersonal AI Manager</h1>
            <h2 class="question-header">📢 Freelancing Scenario</h2>
            <p class="question-text">Now that you’ve completed the practice task, let’s return to our main scenario.</p>
            <p class="question-text">{question}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Helper function to send the request to the backend API and get AI response
def get_ai_response(user_idea):

    try:    
        with st.spinner("🤔 Interpersonal AI Agent is Analyzing.. Please wait..."):
            # Prepare your question and include user_idea in the payload

            payload = {"idea": user_idea}

            response = requests.post(
                "http://127.0.0.1:5001/ask", json=payload
            )

        if response.status_code == 200:
            data = response.json()
            st.session_state.ai_response = data.get("response", "No response received.")
            # st.session_state.evaluation = data.get("evaluation", "No evaluation available.")
            # st.session_state.references = data.get("references", [])
            st.session_state.show_response = True
            st.session_state.idea_submitted = True  # Prevent AI re-call
            st.session_state.current_screen = "ai_response"  # Move to AI response screen
            st.success("✅ Response received!")

        else:
            st.error(f"❌ Error {response.status_code}")

    except Exception as e:
        st.error(f"⚠️ Failed to connect to backend: {e}")


# Helper function to send the request to the backend API and get AI response
def get_ai_response2(user_idea):

    try:    
        with st.spinner("🤔 Interpersonal AI Agent is Analyzing.. Please wait..."):
            # Prepare your question and include user_idea in the payload
            #question = "Your predefined question here"  # Replace with your actual question logic

            payload = {"idea": user_idea}

            response = requests.post(
                "http://127.0.0.1:5001/ask", json=payload
            )

        if response.status_code == 200:
            data = response.json()
            st.session_state.ai_response = data.get("response", "No response received.")
            # st.session_state.evaluation = data.get("evaluation", "No evaluation available.")
            # st.session_state.references = data.get("references", [])
            st.session_state.show_response = True
            st.session_state.idea_submitted = True  # Prevent AI re-call
            #st.session_state.current_screen = "ai_response"  # Move to AI response screen
            st.success("✅ Response received!")

        else:
            st.error(f"❌ Error {response.status_code}")

    except Exception as e:
        st.error(f"⚠️ Failed to connect to backend: {e}")


def display_ai_response2(image_path, video_path):
    # Create a container to hold all content
    container = st.container()

    # Use a single column to center content
    with container:
        col1, col2, col3 = st.columns([1, 3, 1])  # Create three columns, middle one is wider

        # Place content in the middle column
        with col2:
            st.header("🤖🧠 I am the Interpersonal AI manager and have compiled the following information on this matter:")
            st.success(st.session_state.ai_response)

            st.write("Based on the feedback provided above, if you would like to resubmit your idea please enter it below")

            # Display Resubmit and Complete buttons
            display_resubmit_complete_buttons()

    st.session_state.current_screen = "input_1"


def display_ai_response1(image_path, video_path):
    # Create a container to hold all content
    container = st.container()

    # Use a single column to center content
    with container:
        col1, col2, col3 = st.columns([1, 3, 1])  # Create three columns, middle one is wider

        # Place content in the middle column
        with col2:
            st.header("🤖🧠 I am the Interpersonal AI manager and have compiled the following information on this matter:")
            st.success(st.session_state.ai_response)


            st.write("Based on the feedback provided above, if you would like to resubmit your idea please enter it below.")

            # Display Resubmit and Complete buttons
            display_resubmit_complete_buttons()



    st.session_state.current_screen = "completed"



# Helper function to display media (image and video)
def display_media(image_path, video_path):
    # st.subheader("📸 Image Related to the Response:")

    # st.subheader("🎥 Video Related to the Response:")
    try:
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
            video_base64 = base64.b64encode(video_bytes).decode()
            video_html = f"""
                <video width="450" autoplay loop muted controls>
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            """
            st.markdown(video_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Video file not found: {video_path}")
    except Exception as e:
        st.error(f"Error displaying video: {e}")

    image_width = 450
    st.image(image_path, caption="Collaboration Image", width=image_width)


def display_resubmit_complete_buttons():
    # Initialize session state for resubmitted idea if it doesn't exist
    if 'resubmitted_idea' not in st.session_state:
        st.session_state.resubmitted_idea = ""

    # Resubmit Idea Input Field
    st.session_state.resubmitted_idea = st.text_area("💡 Resubmit your idea:", key="resubmit_idea_input")

    # Create a container to center the button
    with st.container():
        col1, col2, col3 = st.columns([1.7, 1, 1])  # Equal columns for centering
        with col2:
            # Handle "Complete" button click
            if st.button("SUBMIT", key="complete_button", use_container_width=False):
                st.session_state.session_completed = True
                st.session_state.current_screen = "completed"
                st.rerun()


def display_consent_form():
    # Display consent form styles
    st.markdown(
        """
        <style>
        .consent-container {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 0 auto;
            margin-bottom: 20px;
            max-width: 900px;
            background-color: #f9f9f9;
            box-sizing: border-box;
        }
        .consent-header {
            color: #336699;
            font-size: 24px;
            margin-bottom: 15px;
            text-align: center;
        }
        .consent-text {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
            text-align: justify;
            word-wrap: break-word;
            max-width: 100%;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 5px; /* Adjust gap here */
            margin-top: 20px;
        }
        .stButton > button {
            border: 1px solid #ccc; /* Grey border initially */
            border-radius: 5px !important; 
            padding: 10px 20px !important;
            font-size: 16px !important; /* Adjust font size */
            cursor: pointer; /* Keep pointer cursor */
            box-shadow: none; /* Remove shadow */
            background-color: transparent; /* No background color initially */
            color: #000; /* Black text initially */
        }
        .stButton > button:hover {
            background-color: transparent !important; /* Keep no background color on hover */
            color: red !important; /* Change text color to red on hover */
            border: 1px solid red !important; /* Change border color to red on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display consent form content
    st.markdown(
        """
        <div class="consent-container">
            <h2 class="consent-header">Informed Consent Form</h2>
            <p class="consent-text">
                Please read this consent form carefully before deciding to participate in this study.
            </p>
            <p class="consent-text">
                <b>Purpose of the research study:</b> We are conducting research to understand how Interpersonal AI managers affect workers. Your participation in this survey is highly appreciated.
            </p>
            <p class="consent-text">
                <b>Risks/Discomforts:</b> The risks involved in this study are minimal. No sensitive data will be collected.
            </p>
            <p class="consent-text">
                <b>Benefits:</b> While there are no direct benefits to you, the findings from this study will hopefully benefit others in the future.
            </p>
            <p class="consent-text">
                <b>Voluntary participation:</b> Your participation is completely voluntary. You can withdraw from the task at any time without penalty.
            </p>
            <p class="consent-text">
                <b>Confidentiality:</b> Your identity will remain strictly confidential. Your personal information will be protected, and your responses will be used solely for scientific purposes. All data will be securely stored and only accessed by the research team. This study has been reviewed and deemed exempt by the Institutional Review Board.
            </p>
            <p class="consent-text">
                <b>Questions:</b> If you have any questions about this research, please contact Rasha Alahmad at <a href="mailto:Rasha.ahmad@kfupm.edu.sa">Rasha.ahmad@kfupm.edu.sa</a>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Create buttons
    with st.container():
        col1, col2, col3 = st.columns([1.5, 1.4, 2])  # Adjust column widths
        with col2:
            if st.button("Yes, I agree", key="consent_yes"):
                st.session_state.consent_given = True
                st.session_state.current_screen = "instruction_page"
                st.rerun()
        with col3:
            if st.button("No, I don't agree", key="consent_no"):
                st.session_state.session_completed = True
                st.rerun()


def display_instruction_page():
    # Path to the instruction image (replace with your actual image path)
    instruction_image_path = "imag3.jpeg"  # or .jpg, etc.

    # Custom CSS (reusing consent container styles)
    st.markdown(
        """
        <style>
        .instruction-container {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 0 auto; /* Center the container */
            margin-bottom: 20px;
            max-width: 900px; /* Limit the container width */
            background-color: #f9f9f9;
        }
        .instruction-header {
            color: #336699;
            font-size: 24px;
            margin-bottom: 15px;
            text-align: center; /* Center the header text */
        }
        .instruction-text {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
            text-align: justify; /* Justify the text */
            word-wrap: break-word; /* Break long words */
            max-width: 100%; /* Ensure full width within container */
        }
        .instruction-image {
            display: block; /* Ensure it behaves like a block element */
            margin: 0 auto; /* Center the image horizontally */
            margin-bottom: 20px; /* Add some space below the image */
            max-width: 100%; /* Make image responsive */
            max-height: 200px; /* Limit the image height */
            height: auto; /* Maintain aspect ratio */
        }
        .stButton > button {
            border: 1px solid #ccc; /* Grey border initially */
            border-radius: 5px !important; 
            padding: 10px 20px !important;
            font-size: 16px !important; /* Adjust font size */
            cursor: pointer; /* Keep pointer cursor */
            box-shadow: none; /* Remove shadow */
            background-color: transparent; /* No background color initially */
            color: #000; /* Black text initially */
        }
        .stButton > button:hover {
            background-color: transparent !important; /* Keep no background color on hover */
            color: red !important; /* Change text color to red on hover */
            border: 1px solid red !important; /* Change border color to red on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Instruction content
    st.markdown(
        f"""
        <div class="instruction-container">
            <h2 class="instruction-header">Instruction</h2>
            <p class="instruction-text">
                We are conducting an experiment to examine how Artificial Intelligence (AI) managers influence individual performance. In this experiment, you will generate ideas for various situations and will be managed by an Interpersonal AI manager.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    with st.container():
        col1, col2, col3 = st.columns([1.8, 1, 1])  # Create columns for centering
        with col2:
            if st.button("Next", key="next_button"):
                st.session_state.current_screen = "freelancing_scenario"
                st.rerun()


# New function to display the freelancing scenario
def display_freelancing_scenario():
    # Content for the freelancing scenario
    scenario_title = "Freelancing Scenario"
    scenario_content = """
    Imagine you’re a freelancer, hired through a platform called FreelanceHub, to collaborate with two other freelancers on a short-term project to create a website for a client. The project must be completed within two weeks, and since you all live in different cities, the entire project is managed virtually through Zoom for meetings and emails for daily communication and collaboration.

    The client has set strict deadlines and expects daily updates on progress. To ensure the project's success, each team member has been asked to come up with one idea that specifically focuses on improving the efficiency of your 30-minute daily Zoom meetings and enhancing collaboration on Microsoft Teams. Your idea should aim to optimize communication, ensure that everyone is clear on their tasks, and help the team meet the tight deadline.

    The top three ideas will each receive a $5 reward.
    """

    # Custom CSS (reusing consent container styles)
    st.markdown(
        """
        <style>
        .scenario-container {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 0 auto; /* Center the container */
            margin-bottom: 20px;
            max-width: 900px; /* Limit the container width */
            background-color: #f9f9f9;
        }
        .scenario-header {
            color: #336699;
            font-size: 24px;
            margin-bottom: 15px;
            text-align: center; /* Center the header text */
        }
        .scenario-text {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
            text-align: justify; /* Justify the text */
            word-wrap: break-word; /* Break long words */
            max-width: 100%; /* Ensure full width within container */
        }
        .stButton > button {
            border: 1px solid #ccc; /* Grey border initially */
            border-radius: 5px !important; 
            padding: 10px 20px !important;
            font-size: 16px !important; /* Adjust font size */
            cursor: pointer; /* Keep pointer cursor */
            box-shadow: none; /* Remove shadow */
            background-color: transparent; /* No background color initially */
            color: #000; /* Black text initially */
        }
        .stButton > button:hover {
            background-color: transparent !important; /* Keep no background color on hover */
            color: red !important; /* Change text color to red on hover */
            border: 1px solid red !important; /* Change border color to red on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Scenario content
    st.markdown(
        f"""
        <div class="scenario-container">
            <h2 class="scenario-header">{scenario_title}</h2>
            <p class="scenario-text">{scenario_content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        col1, col2, col3 = st.columns([1.8, 1, 1])  # Create columns for centering
        with col2:
            if st.button("Next", key="next_button"):
                st.session_state.current_screen = "ai_manager_info"  # Proceed to the AI manager info
                st.rerun()

# New function to display the AI manager information
def display_ai_manager_info():
    # Content for the AI manager information
    ai_manager_title = "Interpersonal AI Manager"
    ai_manager_content = """
    I am the Interpersonal AI Manager, developed by Tech Innovate Inc. I am designed to serve as an interpersonal AI manager, assisting participants in generating better ideas by providing them with relevant information. I leverage advanced large language models (LLMs) such as OpenAI's GPT-4 and proprietary machine learning algorithms to assist you. My system integrates neural network architectures and natural language processing techniques to provide accurate and contextually relevant support. I will interact with you following the steps outlined in the graph below.

    I will be here throughout the experiment to ensure that your contributions are effective.
    """
    # Path to the AI manager image (replace with your actual image path)
    ai_manager_image_path = "/home/dev/rasha project/AI_Community_projectV2/img2.png"  # or .jpg, etc.

    st.markdown(
        """
        <style>
        .ai-manager-container {
            padding: 20px 20px 0 20px; /* Reduced bottom padding */
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 0 auto;
            margin-bottom: 20px;
            max-width: 900px;
            background-color: #f9f9f9;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between; /* Changed to space-between */
        }
        .ai-manager-header {
            color: #336699;
            font-size: 24px;
            margin-bottom: 15px;
            text-align: center;
        }
        .ai-manager-text {
            flex-grow: 1; /* Added to make text expand and push image down */
        }
        .ai-manager-image {
            display: block;
            margin: 0;
            max-width: 100%; /* Adjusted to full container width */
            max-height: 250px; /* Keep this for height constraint */
            height: auto; /* Maintain aspect ratio */
            object-fit: contain; /* Maintain aspect ratio */
            width: 100%; /* Full container width */
        }
        .stButton > button {
            border-radius: 5px !important; 
            padding: 10px 20px !important;
        }
        .stButton > button:hover {
            background-color: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="ai-manager-container">
            <h2 class="ai-manager-header">{ai_manager_title}</h2>
            <p class="ai-manager-text">{ai_manager_content}</p>
            <img src="data:image/jpeg;base64,{base64.b64encode(open(ai_manager_image_path, "rb").read()).decode()}" class="ai-manager-image">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Create a centered "Next" button
    with st.container():
        col1, col2, col3 = st.columns([1.8, 1, 1])  # Adjust column widths for centering
        with col2:
            if st.button("Next", key="next_button"):
                st.session_state.current_screen = "training_intro"  # Proceed to the next screen
                st.rerun()





# New function to display the training introduction
def display_training_intro():
    # Content for the training introduction
    training_title = "Training Task"
    training_content = """
    On the following pages, you’ll complete a practice task, where you’ll be presented with a problem scenario, and the goal is to come up with an innovative idea to address it.

    After doing this, you will be presented with the main problem and you need to provide an innovative idea.
    """

    # Custom CSS (reusing consent container styles)
    st.markdown(
        """
        <style>
        .training-container {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 0 auto; /* Center the container */
            margin-bottom: 20px;
            max-width: 900px; /* Limit the container width */
            background-color: #f9f9f9;
        }
        .training-header {
            color: #336699;
            font-size: 24px;
            margin-bottom: 15px;
            text-align: center; /* Center the header text */
        }
        .training-text {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
            text-align: justify; /* Justify the text */
            word-wrap: break-word; /* Break long words */
            max-width: 100%; /* Ensure full width within container */
        }
        .stButton > button {
            border: 1px solid #ccc; /* Grey border initially */
            border-radius: 5px !important; 
            padding: 10px 20px !important;
            font-size: 16px !important; /* Adjust font size */
            cursor: pointer; /* Keep pointer cursor */
            box-shadow: none; /* Remove shadow */
            background-color: transparent; /* No background color initially */
            color: #000; /* Black text initially */
        }
        .stButton > button:hover {
            background-color: transparent !important; /* Keep no background color on hover */
            color: red !important; /* Change text color to red on hover */
            border: 1px solid red !important; /* Change border color to red on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Training introduction content
    st.markdown(
        f"""
        <div class="training-container">
            <h2 class="training-header">{training_title}</h2>
            <p class="training-text">{training_content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Create a centered "Next" button
    with st.container():
        col1, col2, col3 = st.columns([1.8, 1, 1])  # Adjust column widths for centering
        with col2:
            if st.button("Next", key="next_button"):
                st.session_state.current_screen = "practice_task"  # Proceed to the practice task
                st.rerun()



def display_practice_task(image_path, video_path):
    # Initialize session state variables if they don't exist
    if 'practice_submitted' not in st.session_state:
        st.session_state.practice_submitted = False
    if 'practice_idea' not in st.session_state:
        st.session_state.practice_idea = ""
    if 'show_next' not in st.session_state:
        st.session_state.show_next = False  # Controls visibility of Next button

    # Content for the practice task
    practice_title = "Practice Task"
    practice_content = """
    Imagine you are organizing a community event in a local park.
    Please suggest one innovative way to promote the event and attract attendees from the neighborhood.
    """

    # Custom CSS for centering elements
    st.markdown(
        """
        <style>
        .practice-container {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 0 auto;
            max-width: 900px;
            background-color: #f9f9f9;
            text-align: center;
        }
        .practice-header {
            color: #336699;
            font-size: 24px;
            margin-bottom: 15px;
            text-align: center;
        }
        .practice-text {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
            text-align: justify;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.practice_submitted:
        container = st.container()
        with container:
            col1, col2, col3 = st.columns([1, 4.2, 1])  # Center-align the content
            with col2:
                st.markdown(
                    f"""
                    <div class="practice-container">
                        <h2 class="practice-header">{practice_title}</h2>
                        <p class="practice-text">{practice_content}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.session_state.practice_idea = st.text_area("💡 Enter your idea:", key="practice_idea_input")

        with st.container():
            col1, col2, col3 = st.columns([9, 10, 0.1])  # Center-align the Submit button
            with col2:
                if st.button("SUBMIT", key="submit_button"):
                    if st.session_state.practice_idea.strip():  # Check if idea is not empty
                        st.session_state.practice_submitted = True
                        st.session_state.show_next = True  # Enable Next button after displaying table
                        get_ai_response2(st.session_state.practice_idea)
                        st.rerun()
                    else:
                        st.warning("⚠️ Please enter an idea before submitting.")  # Display warning if idea is empty

    elif st.session_state.show_response:
        display_ai_response2(image_path, video_path)




# Main function that controls the flow of the app
def main():
    # Paths to image and video (these can be passed dynamically if needed)
    image_path = "img1.png"  # Update with your local image path
    video_path = "7665d69d-73ca-4072-b5f6-5a35200a29e4.MP4"  # Update with your local video path
    practice_image_path = "img1.png"
    practice_video_path = "7665d69d-73ca-4072-b5f6-5a35200a29e4.MP4"

    initialize_session_state()

    # Conditional display based on session state
    if st.session_state.session_completed:
        st.header("Thank you for your time 😃")
        st.write("✅ Session Completed!")
        return

    if st.session_state.current_screen == "consent_form":
        display_consent_form()

    elif st.session_state.current_screen == "instruction_page":
        display_instruction_page()

    elif st.session_state.current_screen == "freelancing_scenario":
        display_freelancing_scenario()

    elif st.session_state.current_screen == "ai_manager_info":
        display_ai_manager_info()

    elif st.session_state.current_screen == "training_intro":
        display_training_intro()

    elif st.session_state.current_screen == "practice_task":
        display_practice_task(practice_image_path, practice_video_path)

    elif st.session_state.current_screen == "input_1":
        container = st.container()
        with container:
            col1, col2, col3 = st.columns([1, 4.2, 1])  # Center-align the input box
            with col2:
                display_predefined_question()
                st.session_state.user_idea = st.text_area("💡 Enter your idea:")
                
                # Create a centered button
                button_col1, button_col2, button_col3 = st.columns([1.7, 1, 1])  # Split the column into three parts
                with button_col2:  # Place the button in the middle column
                    if st.button("Submit", key="next_button"):
                        if st.session_state.user_idea.strip():
                            get_ai_response(st.session_state.user_idea)  # This will set current_screen to "ai_response"
                            st.rerun()  # Use st.experimental_rerun() instead of st.rerun()
                        else:
                            st.warning("⚠️ Please enter an idea before proceeding.")



    elif st.session_state.current_screen == "ai_response":
        display_ai_response1(image_path, video_path)

    elif st.session_state.current_screen == "resubmit":
        st.subheader("Interpersonal AI Manager")
        resubmit_text = st.text_area("💡 Resubmit your idea:")
        if st.button("Resubmit Done", key="resubmit_done"):
            st.session_state.session_completed = True
            st.session_state.current_screen = "completed"
            st.rerun()

    elif st.session_state.current_screen == "completed":
        st.header("Thank you for your participation. Please complete the following survey. 😃")
        st.write("✅ Session Completed!")
        return

if __name__ == "__main__":
    main()
