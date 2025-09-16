from utils.get_job_dsc import get_urls_from_file, scrape_job_description, scrape_all_jobs
from utils.tailor_resume import get_gemini_api_key, generate_custom_resume
from utils.export_resume import create_resume_docx, create_resume_pdf
import json
import time
import os

# Your Resume, edit placeholder content as required,
# but keep the lettered headings and format same.
resume_text = """John Doe
Phone: (123) 456-7890 | Email: john.doe@email.com

A. Education
1. Master of Science in Computer Science
    1.1. University of Technology, Anytown, USA
    1.2. GPA: 3.8/4.0
2. Bachelor of Science in Electrical Engineering
    2.1. State University, Hometown, USA
    2.2. GPA: 3.6/4.0

B. Skills
1. Programming Languages: Python, Java, C++
2. Data Science: Pandas, NumPy, Scikit-learn, TensorFlow
3. Web Development: HTML, CSS, JavaScript, React, Node.js
4. Cloud & DevOps: AWS, Docker, Kubernetes, Git

C. Experience
1. Senior Software Engineer, Tech Solutions Inc., Anytown, USA (Sept'23 - Present)
    - Led the development of a scalable e-commerce platform using Python and Django, resulting in a 20% increase in transaction volume.
    - Optimized database queries and backend services, reducing latency by 30% and improving user experience.
    - Collaborated with a cross-functional team to deploy new features using an agile methodology, ensuring timely releases.

2. Software Developer, Innovate Co., Anytown, USA (Jun'21 - Aug'23)
    - Developed and maintained key features for a mobile application used by over 50,000 users.
    - Implemented RESTful APIs to connect front-end applications with back-end services, streamlining data flow.
    - Participated in code reviews and provided constructive feedback to junior developers, contributing to a high-quality codebase.

D. Projects
1. Personal Finance Dashboard: Developed a web application using React and Node.js that visualizes personal spending habits and investment growth.
2. Image Recognition Model: Trained a convolutional neural network (CNN) using TensorFlow to classify images with 95% accuracy.
3. Home Automation System: Built an IoT-based system using a Raspberry Pi to control home lighting and temperature remotely.

E. Research Publications
PUBLICATIONS
1. Vaswani, Ashish, et al. "Attention Is All You Need." Advances in Neural Information Processing Systems 30 (NIPS 2017), 2017.
2. Rose, C. "The Literature of Memes and the New Way to Write." Florida's Classical Studies Publication 2,000, October 1, 2018.
3. Rose, C. "Social Media and the New English Literature." The Mercury: The Student Art & Literary Magazine of Gettysburg College 1,019, April 2, 2017
"""

# Sample Output from Gemini, to demonstrate the expected output from generate_custom_resume()
s = """
{
    "Name": "John Doe",
    "Education": {
        "Degree 1": {
            "Institution": "University of Technology, Anytown, USA",
            "GPA": "3.8/4.0"
        },
        "Degree 2": {
            "Institution": "State University, Hometown, USA",
            "GPA": "3.6/4.0"
        }
    },
    "Skills": {
        "Programming Languages": ["C++", "Python", "Java"],
        "Development Practices": ["Agile Methodologies", "Git", "Code Reviews", "RESTful APIs", "Scalable Systems", "Backend Services", "Database Optimization", "Performance Optimization"],
        "Cloud & DevOps": ["AWS", "Docker", "Kubernetes"],
        "Data Analysis": ["Pandas", "NumPy", "Scikit-learn", "TensorFlow"],
        "Web Technologies": ["HTML", "CSS", "JavaScript", "React", "Node.js"]
    },
    "Experience": {
        "Tech Solutions Inc.": {
            "Position": "Senior Software Engineer",
            "Start": "Sep'23",
            "End": "Present",
            "Experience": [
                "Led the development of a scalable e-commerce platform using Python and Django, resulting in a 20% increase in transaction volume and demonstrating capability to translate complex requirements into elegant design.",
                "Optimized database queries and backend services, reducing latency by 30% and improving user experience, reflecting a quality-driven mindset and strong analytical skills.",
                "Collaborated with a cross-functional team to deploy new features using an agile methodology, ensuring timely releases and active participation in scrum activities."
            ]
        },
        "Innovate Co.": {
            "Position": "Software Developer",
            "Start": "Jun'21",
            "End": "Aug'23",
            "Experience": [
                "Developed and maintained key features for a mobile application used by over 50,000 users, showcasing experience with high-impact product development.",
                "Implemented RESTful APIs to connect front-end applications with back-end services, streamlining data flow and system integration.",
                "Participated in code reviews and provided constructive feedback to junior developers, contributing to a high-quality codebase and fostering development standards."
            ]
        }
    },
    "Projects": {
        "Personal Finance Dashboard": "Developed a web application using React and Node.js that visualizes personal spending habits and investment growth.",
        "Image Recognition Model": "Trained a convolutional neural network (CNN) using TensorFlow to classify images with 95% accuracy.",
        "Home Automation System": "Built an IoT-based system using a Raspberry Pi to control home lighting and temperature remotely."
    },
    "Research Publications": {
        "Attention Is All You Need": {
            "last name": "Vaswani",
            "first initial": "A",
            "journal name": "Advances in Neural Information Processing Systems",
            "volume number": "30",
            "date": "2017"
        },
        "The Literature of Memes and the New Way to Write": {
            "last name": "Rose",
            "first initial": "C",
            "journal name": "Florida's Classical Studies Publication",
            "volume number": "2,000",
            "date": "October 1, 2018"
        },
        "Social Media and the New English Literature": {
            "last name": "Rose",
            "first initial": "C",
            "journal name": "The Mercury: The Student Art & Literary Magazine of Gettysburg College",
            "volume number": "1,019",
            "date": "April 2, 2017"
        }
    }
}
"""

# Scrape Job Descriptions from URLS present in links.txt
job_dict = scrape_all_jobs('job_links.txt')

for url, job_info in job_dict.items():
    '''
    Where it writes resume 

    It should write it in :
    - /resumes
        - /Company
            - /JobID
                - Resume_<job_id>.docx
                - Resume_<job_id>.pdf
    
    /resumes always exists
    It checks for /Company
        if /Company Exists, it creates 'JobID' directory & writes to resumes/Company/JobID
        else, it creates 'Company' & 'JobID' directory & then writes to resumes/Company/JobID
    '''
    # Use the scraped job descriptions to create custom resume for each job
    custom_resume_json = generate_custom_resume(resume_text, job_info["Job_Description"])
    print("Custom Resume from Gemini: ", custom_resume_json)

    base_dir = "resumes" # always exists
    company_dir = os.path.join(base_dir, job_info['Company'])
    job_dir = os.path.join(company_dir, job_info['Job_ID'])

    if not os.path.exists(base_dir):
        # Ensures 'resumes/' folder always exists
        os.makedirs(base_dir)
    
    if not os.path.exists(company_dir):
        os.makedirs(company_dir)

    if not os.path.exists(job_dir):
        os.makedirs(job_dir)

    docx_path = os.path.join(job_dir, f'Resume_{job_info['Job_ID']}.docx')
    pdf_path = os.path.join(job_dir, f'Resume_{job_info['Job_ID']}.pdf')

    create_resume_docx(custom_resume_json, docx_path)
    
    # Gracefully open and close the .docx file 
    # to prevent the 'AttributeError: Word.Application.Quit' error
    file = open(docx_path, "a")
    file.close()

    create_resume_pdf(docx_path, pdf_path)
    print('-------------------------------------------------------------------------')
