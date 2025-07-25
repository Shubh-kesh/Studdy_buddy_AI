import os
import streamlit as st
import pandas as pd
from datetime import datetime
from src.generator.question_generator import QuestionGenerator

def rerun():

    # Function to trigger a rerun of the Streamlit app, generate mcq again for different topics
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False) # This will toggle the rerun state


class QuizManager:
    def __init__(self):
        self.llm_response = []
        self.user_answers = []
        self.results= []
    # Function to generate questions based on the topic and difficulty level and delete the previous question, answer
    def question_generator(self, topic:str, difficulty:str, generator:QuestionGenerator, question_type:str, num_questions:int):
        self.llm_response = []
        self.user_answers = []
        self.results= []      

        try:
            for _ in range(num_questions):
                if question_type == "Multiple Choice":
                    llm_response_mcq = generator.generate_mcq(topic, difficulty)
                    self.llm_response.append(
                        {  
                            "type" : "MCQ",
                            "question": llm_response_mcq.question,
                            "options": llm_response_mcq.options,
                            "correct_answer": llm_response_mcq.correct_answer
                        }
                    )
                
                else:
                    llm_response_fb = generator.generate_fill_blank(topic, difficulty)
                    self.llm_response.append(
                        {  
                            "type" : "Fill in the blank",
                            "question": llm_response_fb.question,
                            "correct_answer": llm_response_fb.correct_answer
                        }
                    )



        except Exception as e: # error in strealit page
            st.error(f"Error generating questions: {str(e)}")
            return False
        
        return  True
    
    def attempt_quiz(self):
        # i is a number of question
        # q is a question dictionary
        self.user_answers = []  # Clear previous state on every run
        for i,q in enumerate(self.llm_response):
            st.markdown(f"**Quesition {i+1}: {q['question']}**")
            if q["type"] == "MCQ":
                user_answer = st.radio(
                    f"Select and answer for Question {i+1}",
                    q["options"],
                    key=f"mcq_{i}"
                )
                self.user_answers.append(user_answer) ## append the user answer to the list
            else:
                user_answer = st.text_input(
                        f"Fill in the blank for Question: {i+1}",
                        key=f"fill_blank_{i}"
                    )
                self.user_answers.append(user_answer) # append the user answer to the list


    def evaluate_quiz(self):
        self.results = []

        for i, (q,user_ans) in enumerate(zip(self.llm_response, self.user_answers)):
            result_dict = {
                "question_number": i+1,
                "question_type": q['type'],
                "question": q['question'],
                "user_answer": user_ans,
                "correct_answer": q['correct_answer'],
                "is_correct": False
            }

            if q['type'] == "MCQ":
                result_dict["options"]= q['options'] # multiple choice question has options # add options to the result dictionary
                result_dict["is_correct"] = user_ans == q['correct_answer'] # check if the user answer is correct then make in_Correct as true
            else:
                result_dict['options']=[] # fill in the blank question does not have option
                result_dict["is_correct"] = user_ans.strip().lower() == q['correct_answer'].strip().lower()

            self.results.append(result_dict)
            

    def generate_result_dataframe(self): # generate a dataframe from the results list
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)  # Convert the results list to a DataFrame

    def save_to_csv(self, filename_prefix="quiz_results"):
        if not self.results:
            st.error("No results to save.")
            return None
        
        df = self.generate_result_dataframe()
        if df.empty:
            st.error("No results to save.")
            return
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.csv"
        
        os.makedirs("results", exist_ok=True)  # Ensure the results directory exists
        filepath = os.path.join("results", filename)
        try:
            df.to_csv(filepath, index=False)
            st.success(f"Results saved to {filepath}")
            return filepath
        except Exception as e:
            return None
    