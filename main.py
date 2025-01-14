import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


# def create_streamlit_app(llm, portfolio, clean_text):
#     st.title("Cold Mail Generator")
#     url_input = st.text_input("Enter a URL:", value="https://amazon.jobs/en/jobs/2866652/software-development-engineer-ii-amazon-advertising-partner-enablement-and-growth-team-amazon-ads")
#     submit_button = st.button("Submit")

#     if submit_button:
#         try:
#             loader = WebBaseLoader([url_input])
#             data = clean_text(loader.load().pop().page_content)
#             portfolio.load_portfolio()
#             jobs = llm.extract_jobs(data)
#             for job in jobs:
#                 skills = job.get('skills', [])
#                 links = portfolio.query_links(skills)
#                 email = llm.write_mail(job, links)
#                 st.code(email, language='markdown')
#         except Exception as e:
#             st.error(f"An Error Occurred: {e}")

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cold Mail Generator")

    # Input for URL
    url_input = st.text_input("Enter a URL:", value="")

    # Text area for dynamic input (alternative to URL scraping)
    job_posting_input = st.text_area("Or paste the job posting text directly:", value="", height=200)

    submit_button = st.button("Submit")

    if submit_button:
        try:
            if url_input:
                # Process URL input
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
            elif job_posting_input.strip():
                # Use the pasted job posting text
                data = clean_text(job_posting_input)
            else:
                st.error("Please provide either a URL or paste the job posting text.")
                return

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator")
    create_streamlit_app(chain, portfolio, clean_text)