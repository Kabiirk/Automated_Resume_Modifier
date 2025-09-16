from google import genai
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Dict, List

# class Resume(BaseModel):
#     name: str = Field(description="The full name of the resume owner.")
#     skills: Dict[str, List[str]] = Field(description="A dictionary of skills, with domains as keys and a list of skills as values.")
#     experience: Dict[str, List[str]] = Field(description="A dictionary of work experience, with company names as keys and a list of bullet points as values.")
#     projects: Dict[str, str] = Field(description="A dictionary of projects, with project titles as keys and a short description as values.")

# response_schema = {
#     "type": "OBJECT",
#     "properties": {
#             "name": {
#                         "type": "STRING"
#                     },
#             "skills": {
#                         "type": "OBJECT"
#                         "properties": {
#                             "type": "ARRAY",
#                             "items"
#                         }
#                     },
#         },
#     "required": ["recipe_name", "ingredients"],
# }

def get_gemini_api_key():
    """Retrieves the Gemini API key from an environment variable."""
    # Load environment variables from the .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    return api_key

def generate_custom_resume(user_resume_text, job_description):
    """
    Queries the Gemini API to create a custom resume.
    """
    # genai.configure(api_key=get_gemini_api_key())
    # model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert resume writer. Your task is to analyze a user's resume and a job description to create a custom, tailored resume.

    Based on the provided job description and the user's resume, extract and re-format the user's information to align with the job requirements.

    Job Description:
    {job_description}

    User's Resume Text:
    {user_resume_text}

    Provide the output in a structured JSON format. Ensure all sections (Name, Skills, Experience) are present and populated with relevant information from the user's resume, prioritized based on the job description.
    

    The  output must have the following fields and strictly use the 3 letter notation for months while mentioning dates in the experience. If the user has research experience in their resume, add that as well, otherwise leave it.:
    {{
        "Name": "Some Name",
        "Education":{{
           "1st Degree name from user resume": {{
                "Institution": "1st Institution name",
                "GPA": "GPA"
           }},
           "2nd Degree name from user resume": {{
                "Institution": "2nd Institution name",
                "GPA": "GPA"
           }},
           and so on ...
        }},
        "Skills": {{
            "Domain 1": ["skill 1", "skill 2", ...],
            "Domain 2": ["skill 1", "skill 2", ...]
            ... and so on
        }},
        "Experience": {{
            "Company 1": {{
                "Position": Job Role (Software Developer, Data Scientist etc..),
                "Start": "Date 1" (3 letter Month and Year e.g. Jun'24)
                "End": "Date 2" (3 letter Month and Year e.g. Jun'24, can also be "Present" for current company)
                "Experience": ["Experience bullet 1", "Experience bullet 2", ...],
            }},
            "Company 2": {{
                "Position": Job Role (Sftware Developer, Data Scientist etc..),
                "Start": "Date 1" (3 letter Month and Year e.g. June'24)
                "End": "Date 2" (3 letter Month and Year e.g. June'24)
                "Experience": ["Experience bullet 1", "Experience bullet 2", ...],
            }},
            ... and so on
        }},
        "Projects": {{
            "Project 1": Short Project Description,
            "Project 2": Short Project Description,
            ... and so on
        }},
        "Research Publications": {{
            "Article title 1":{{
                "last name": last name,
                "first initial": first initial,
                "journal name": journal name,
                "volume number": volume number,
                "issue number": issue number,
                "date": date,
                "pages": pages
            }},
            "Article title 2":{{
                "last name": last name,
                "first initial": first initial,
                "journal name": journal name,
                "volume number": volume number,
                "issue number": issue number, (Optional)
                "date": date,
                "pages": pages (Optional)
            }},
            ... and so on
        }}
    }}
    """
    
    try:
        key = get_gemini_api_key()
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        # The API may return a text string containing the JSON
        # structured_output = json.loads(response.text.strip())
        # structured_output = json.loads(response.text.strip())
        print("✅ Successfully tailored Resume.")
        res = response.text
        res_json = json.loads(res[res.index('```')+7:len(res)-3])
        return res_json
    except Exception as e:
        print(f"❌ Error generating resume with Gemini API: {e}")
        return None

# Example Usage:
# user_resume = "Your entire resume text here..."
# job_desc = "The job description scraped from Workday..."
# custom_resume_data = generate_custom_resume(user_resume, job_desc)
# if custom_resume_data:
#     print(custom_resume_data)