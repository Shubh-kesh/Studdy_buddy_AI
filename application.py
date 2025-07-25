import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator
from src.common.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def main():
    st.set_page_config(page_title="Studdy Buddy AI", page_icon="$$")
    


    ## to avoid the erasure of output while presssing different button we are defining session state
    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
    # if quiz generated is running then other should not be affected
    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False
    
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    
    if 'rerun_trigger' not in st.session_state:
        st.session_state.rerun_trigger = False

    st.title("Studdy Buddy AI")
    st.write("Welcome to the Studdy Buddy AI Quiz Generator and Quizzer. This application is designed to help you generate quizzes and take quizzes on a variety of topics. You can create quizzes for yourself or share them with others. The application is built using Streamlit, a Python library for building web applications.")

    st.sidebar.header("Quiz Settings")

    question_type = st.sidebar.selectbox(
        "Selection Question Type",
        ["Multiple Choice", "Fill in the Blank"],
        index = 0 # default is Multiple Choice
    )
        
    topic = st.sidebar.text_input("Enter Topic", placeholder='Indian History , Geography')
    difficulty = st.sidebar.selectbox(
        "Selection Difficulty",
        ["Easy", "Medium", "Hard"],
        index = 1 # default is medium
        )
    
    num_questions = st.sidebar.number_input(
        "Number of Question",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False

        generator = QuestionGenerator()
        success = st.session_state.quiz_manager.question_generator(
            generator = generator,
            question_type = question_type,
            topic = topic,
            difficulty = difficulty,
            num_questions = num_questions
        )

        st.session_state.quiz_generated = success
        rerun() # rerun the app to show the generated quiz 

    if st.session_state.quiz_generated and st.session_state.quiz_manager.llm_response:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Quiz Button"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()

    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()
        # st.dataframe(results_df['user_answer'])
        
        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count / total_questions) * 100
            st.write(f"Score: { score_percentage:.2f}%")

            for _, result in results_df.iterrows():
                question_number = result['question_number']
                if result["is_correct"]:
                    st.success(f"Question {question_number}: {result['question']} is correct")
                
                else:
                    st.error(f"Question {question_number}: {result['question']} is not correct")
                    st.write(f"your answer: {result['user_answer']}")
                    st.write(f"correct answer: {result['correct_answer']}")
                    

               
                st.markdown("-----------")

            if st.button("Save Results"):
                saved_file= st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file, "rb") as f:
                        st.download_button(
                            label = "Download Results",
                            data = f.read(),
                            file_name = os.path.basename(saved_file),
                            mime = "text/csv"
                        )
                else:
                    st.warning("No Results available")

if __name__ == "__main__":
    main()