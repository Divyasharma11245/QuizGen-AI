import html
import streamlit as st
from ai_helper import generate_questions


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="QuizGen AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        .stApp {
            font-family: 'Inter', sans-serif;
            background: #0b1020;
            color: #f1f5f9;
        }

        [data-testid="stSidebar"] {
            background: #11182b;
            border-right: 1px solid #25304a;
        }

        .hero {
            padding: 30px;
            border-radius: 22px;
            background: linear-gradient(120deg, #172554, #312e81, #581c87);
            border: 1px solid #4338ca;
            margin-bottom: 25px;
        }

        .hero-label {
            display: inline-block;
            background: rgba(255,255,255,0.12);
            color: #c4b5fd;
            padding: 7px 12px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }

        .hero h1 {
            font-size: 40px;
            font-weight: 800;
            color: white;
            margin: 0;
        }

        .hero p {
            color: #ddd6fe;
            font-size: 15px;
            line-height: 1.7;
            margin-top: 12px;
            max-width: 750px;
        }

        .section-title {
            font-size: 22px;
            font-weight: 700;
            color: #f8fafc;
            margin: 25px 0 8px 0;
        }

        .section-description {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 18px;
        }

        .feature-card {
            background: #151e32;
            border: 1px solid #293650;
            border-radius: 16px;
            padding: 20px;
            min-height: 140px;
            margin-bottom: 12px;
        }

        .feature-icon {
            font-size: 27px;
            margin-bottom: 10px;
        }

        .feature-title {
            font-size: 16px;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 8px;
        }

        .feature-text {
            font-size: 13px;
            line-height: 1.6;
            color: #94a3b8;
        }

        .question-card {
            background: #151e32;
            border: 1px solid #293650;
            border-radius: 15px;
            padding: 22px;
            margin: 12px 0;
        }

        .question-number {
            color: #a5b4fc;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        .question-text {
            font-size: 17px;
            font-weight: 600;
            color: #f8fafc;
            line-height: 1.7;
        }

        .answer-box {
            background: #102c26;
            border: 1px solid #166534;
            padding: 14px;
            border-radius: 10px;
            color: #bbf7d0;
            line-height: 1.7;
            margin-top: 10px;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 44px;
            transition: 0.2s ease;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
        }

        .stButton > button:hover {
            border-color: #a5b4fc;
            transform: translateY(-1px);
        }

        div[data-testid="stMetric"] {
            background: #151e32;
            border: 1px solid #293650;
            padding: 16px;
            border-radius: 14px;
        }

        .footer {
            text-align: center;
            color: #64748b;
            font-size: 12px;
            padding: 25px 0 10px 0;
        }

        .stTextArea textarea,
        .stTextInput input {
            background-color: #11182b;
            color: #f8fafc;
            border-radius: 10px;
        }

        div[data-baseweb="select"] > div {
            background-color: #11182b;
            border-radius: 10px;
        }

        .stCaption {
            color: #94a3b8;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR SETTINGS
# --------------------------------------------------

with st.sidebar:
    st.markdown("# 🧠 QuizGen AI")
    st.caption("Your AI-powered study companion")
    st.divider()

    st.markdown("### ⚙️ Quiz Settings")

    question_type = st.selectbox(
        "Question Type",
        ["MCQs", "Short Answer"],
    )

    difficulty = st.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"],
    )

    number_of_questions = st.slider(
        "Number of Questions",
        min_value=1,
        max_value=10,
        value=5,
    )

    st.divider()
    st.markdown("### ✨ Features")
    st.markdown(
        """
        - 📚 Topic-based quizzes
        - 📝 Questions from study notes
        - 🎯 Adjustable difficulty
        - 💡 Answers and explanations
        - 📥 Downloadable quizzes
        """
    )
    st.divider()
    st.caption("Powered by Google Gemini")


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">AI-POWERED LEARNING</div>
        <h1>Learn smarter. Test yourself.</h1>
        <p>
            Turn your study topics and academic notes into practice questions
            using AI. Choose your difficulty, generate a quiz, and understand
            the answers with clear explanations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Your Study Workspace</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">'
    'Create a personalized quiz in just a few steps.'
    '</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Smart Questions</div>
            <div class="feature-text">
                Generate questions from a topic or your own study material.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Choose Your Level</div>
            <div class="feature-text">
                Practice at Easy, Medium, or Hard difficulty.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Understand Answers</div>
            <div class="feature-text">
                Review answers and explanations after generating questions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Create Your Quiz</div>',
    unsafe_allow_html=True,
)

input_mode = st.radio(
    "Choose your input method",
    ["Enter a topic", "Paste study material"],
    horizontal=True,
)

topic = ""
study_text = ""

if input_mode == "Enter a topic":
    topic = st.text_input(
        "What do you want to study?",
        placeholder="e.g. Operating System Deadlocks, DBMS, Python...",
    )
else:
    study_text = st.text_area(
        "Paste your study notes or academic content",
        placeholder="Paste your notes here. Questions will be generated from this content.",
        height=200,
    )

st.caption("Tip: Use a specific topic or paste relevant notes for better questions.")

generate_button = st.button(
    "✨ Generate My Quiz",
    type="primary",
    use_container_width=True,
)


# --------------------------------------------------
# GENERATE QUESTIONS
# --------------------------------------------------

if generate_button:
    if input_mode == "Enter a topic" and not topic.strip():
        st.warning("Please enter a topic before generating questions.")

    elif input_mode == "Paste study material" and not study_text.strip():
        st.warning("Please paste some study material first.")

    elif input_mode == "Paste study material" and len(study_text) > 12000:
        st.warning("Your text is too long. Please keep it under 12,000 characters.")

    else:
        try:
            with st.spinner("Gemini is preparing your questions..."):
                questions = generate_questions(
                    topic=topic,
                    question_type=question_type,
                    difficulty=difficulty,
                    number_of_questions=number_of_questions,
                    study_text=study_text,
                )

            st.session_state["questions"] = questions
            st.session_state["question_type"] = question_type
            st.session_state["difficulty"] = difficulty

            st.success("Your quiz has been generated successfully!")

        except Exception as error:
            st.error(
                "Unable to generate questions. Check your API configuration "
                "and internet connection, then try again."
            )
            st.caption(f"Technical details: {error}")


# --------------------------------------------------
# DISPLAY GENERATED QUESTIONS
# --------------------------------------------------

questions = st.session_state.get("questions", [])

if questions:
    st.divider()
    st.markdown(
        '<div class="section-title">📝 Your Generated Quiz</div>',
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Questions Generated", len(questions))

    with metric2:
        st.metric(
            "Question Type",
            st.session_state.get("question_type", "MCQs"),
        )

    with metric3:
        st.metric(
            "Difficulty",
            st.session_state.get("difficulty", "Medium"),
        )

    st.info(
        "Review each question below. Expand the answer section when "
        "you are ready to check your understanding."
    )

    download_content = []

    for index, question in enumerate(questions, start=1):
        question_text = str(question.get("question", "Question unavailable"))
        answer = str(question.get("answer", "Answer unavailable"))
        explanation = str(question.get("explanation", "No explanation provided"))
        options = question.get("options", {})

        # Escape AI-generated text before placing it inside HTML.
        safe_question = html.escape(question_text)
        safe_answer = html.escape(answer)
        safe_explanation = html.escape(explanation)

        st.markdown(
            f"""
            <div class="question-card">
                <div class="question-number">QUESTION {index:02d}</div>
                <div class="question-text">{safe_question}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if isinstance(options, dict):
            for option_key, option_value in options.items():
                st.markdown(
                    f"**{html.escape(str(option_key))}.** "
                    f"{html.escape(str(option_value))}"
                )

        with st.expander("💡 Reveal Answer & Explanation"):
            st.markdown(
                f"""
                <div class="answer-box">
                    <strong>Correct Answer:</strong><br>
                    {safe_answer}
                    <br><br>
                    <strong>Explanation:</strong><br>
                    {safe_explanation}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")

        download_content.append(f"QUESTION {index}")
        download_content.append(question_text)

        if isinstance(options, dict):
            for option_key, option_value in options.items():
                download_content.append(f"{option_key}. {option_value}")

        download_content.append(f"Answer: {answer}")
        download_content.append(f"Explanation: {explanation}")
        download_content.append("-" * 50)

    st.download_button(
        label="📥 Download Your Quiz",
        data="\n".join(download_content),
        file_name="quizgen_questions.txt",
        mime="text/plain",
        use_container_width=True,
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        QuizGen AI · Built with Python, Streamlit and Google Gemini
        <br>
        AI-generated answers may contain errors. Verify important information.
    </div>
    """,
    unsafe_allow_html=True,
)
