import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

class ColdEmailGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.2, # Adjuste temperature for creativity
            groq_api_key=os.getenv("GROQ_API_KEY"), # Retrive API key from environment variable
            model_name="llama-3.3-70b-versatile"  # Select the appropriate model
        )

    def extract_jobs(self, page_data): # Prompt to extract job details
        prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            Extract job details in JSON with keys: role, experience, skills, and description.

            ### JSON OUTPUT:
            """
        )
        chain = prompt | self.llm # Chaining the prompt with the LLM
        res = chain.invoke({"page_data": page_data})
        try:
            return JsonOutputParser().parse(res.content)
        except OutputParserException:
            raise OutputParserException("Unable to parse job details")

    def generate_email(self, job_info, resume_text): # Prompt to generate cold email
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CANDIDATE RESUME:
            {resume_text}

            ### INSTRUCTION:
            Write a short, personalized cold email to apply for the job. Be specific and highlight resume-relevant strengths.

            ### EMAIL:
            """
        )
        chain = prompt | self.llm # chaining the prompt with the LLM
        res = chain.invoke({
            "job_description": str(job_info),
            "resume_text": resume_text
        })
        return res.content
