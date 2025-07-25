from langchain.output_parsers import PydanticOutputParser # llm output to structured    data
from src.models.question_schemas import MCQQuestion, FillBlankQuestion # question schemas
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template # prompt templates how to formula answers
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException


class QuestionGenerator:
    def __init__ (self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__) # logger for this class 
    
    def _retry_and_parse(self, prompt, topic, difficulty, parsor): # retry and parse the response from the LLM 
        for attempt in range(settings.MAX_RETRY):
            try:
                self.logger.info(f"Generating question for topic: {topic} and difficulty: {difficulty}")
                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty)) # invoke the LLM with the prompt
                self.logger.info(f"LLM response: {response}")
                parsed = parsor.parse(response.content) # parse the response content using the provided parser
                self.logger.info(f": {parsed}")

                return parsed
            except  Exception as e:
                self.logger.error(f"Error coming from LLM: {str(e)}")
                if attempt == settings.MAX_RETRY-1:
                    raise CustomException(f"Generation failes after {settings.MAX_RETRY} attempts for topic: {topic} and difficulty: {difficulty}. Please try again later, {e}")
                else:
                    continue
    def generate_mcq(self, topic:str, difficulty:str = "medium") -> MCQQuestion: # generate a multiple-choice question having an array of options and a correct answer and follows a MCQ question schemas
        """
        Generate a multiple-choice question using the LLM.
        :param topic: The topic for the question.
        :param difficulty: The difficulty level of the question.
        :return: An instance of MCQQuestion.
        """
        try:
            parsor = PydanticOutputParser(pydantic_object=MCQQuestion) # create a parser for MCQQuestion
            self.logger.info(f"Generating MCQ question for topic: {topic} and difficulty: {difficulty}")
            # Generate the question using the LLM and parse the response
            llm_response_mcq = self._retry_and_parse(mcq_prompt_template, topic, difficulty, parsor) # retry and parse the response
            self.logger.info("Generated a MCQ question", llm_response_mcq)
            if len(llm_response_mcq.options) < 4 or llm_response_mcq.correct_answer not in llm_response_mcq.options:
                raise CustomException(f"Generated MCQ question for topic: {topic} and difficulty: {difficulty} has less than 4 options. Please try again later.")
            self.logger.info("Generated a valid MCQ")
            return llm_response_mcq
        
        except Exception as e:
            self.logger.error(f"Error generating MCQ question for topic: {topic} and difficulty: {difficulty}: {str(e)}")
            raise CustomException(f"Error generating MCQ question for topic: {topic} and difficulty: {difficulty}. Please try again later, {str(e)}")

    def generate_fill_blank(self, topic:str, difficulty:str = "medium") -> FillBlankQuestion:
        try:
            parsor = PydanticOutputParser(pydantic_object=FillBlankQuestion) # create a parser for MCQQuestion
            self.logger.info(f"Generating Fill Blank question for topic: {topic} and difficulty: {difficulty}")
            # Generate the question using the LLM and parse the response
            llm_response_fb = self._retry_and_parse(fill_blank_prompt_template, topic, difficulty, parsor) # retry and parse the response
            self.logger.info("Generated a Fill in blank question", llm_response_fb)
           
            if "___" not in llm_response_fb.question:
                raise ValueError(f"Fill in blank question does not have '___'")

            return llm_response_fb
        
        except Exception as e:
            self.logger.error(f"Error generating Fill in blankquestion for topic: {topic} and difficulty: {difficulty}: {str(e)}")
            raise CustomException(f"Error generating fill in blank for topic: {topic} and difficulty: {difficulty}. Please try again later, {str(e)}")
