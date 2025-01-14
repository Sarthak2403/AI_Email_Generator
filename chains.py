import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Sarthak, a software developer. You are interested in AI, ML, & Software Enginerring, Development. You are focused, headstrong and 
            ready to take any challenge and use your knowledge and skills to complete the tasks given to you.
            Over your experience, you have learnt many things, gained knowledge about programming and also how a company works. Also during your experience
            you worked on many projects and deliverd the required result in time and efficiently.
            Also mention the you have experience in cutting edge technologies such as AI, ML, GenAI, React, etc and also the traditional programming 
            languages such as C, C++, java.
            Your job is to write a cold email to the recruiter regarding the job mentioned above describing the capability of yourself and you being capable 
            of fulfilling their needs.
            Also add the most relevant ones from the following links to showcase from thr portfolio: {link_list}
            Remember you are Sarthak, a software developer. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content