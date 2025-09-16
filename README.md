# Tailored Resume Generator

A python project to generate tailored resume, using Google's Gemini Flash 2.5 LLM, for jobs posted on any/most workday websites.

> **Note:** Some career websites (e.g. TD) ask for cookies to accepted/declined when selenium opens the URL, this needs to be done manually

> **Note:** Other times, you may see the following error:
> 
> [14004:16120:0916/174039.157:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
> [14004:16120:0916/174039.157:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: PHONE_REGISTRATION_ERROR
> [14004:16120:0916/174039.331:ERROR:google_apis\gcm\engine\mcs_client.cc:700]   Error code: 401  Error message: Authentication Failed: wrong_secret
> [14004:16120:0916/174039.332:ERROR:google_apis\gcm\engine\mcs_client.cc:702] Failed to log in to GCM, resetting connection.
> 
> This is expected (Some websites try to ask for login initially, even when it's not required), and the jojb description is also scraped successfully

> **Note:** While This error has been rectified, it is still possible you might get the `AttributeError: Word.Application.Quit` error again, this depends on the sysem & usually happens when the system isn't able to close the `.docx` the resume properly before converting it to pdf, just run the script again and it shold work.

## Steps to use:
It is recommended (but not mandatory) that you create a virtual environment using python's `venv` package (`python -m venv my_project_venv`, then activate the virtual environment) before installing all dependencies and running the project, but below steps can be done even without a virtual environment.

1. Create a `.env` file in the root directory. Then generate a gemini API Key (Ensure you have your Gemini API key), then paste it in the `.env` file like this:

    ```GEMINI_API_KEY=<your API key>```

2. At the root of the directory, Install required libraries using:
    
    ```pip install requirements.txt```

3. Paste all the workday URLs of the job posting that you want to customize your resume for in the `job_links.txt`, with each URL on a separate line. Your `job_links.txt` should look like this:
    ```
    <URL 1>
    <URL 2>
    ... and so on
    ```

    > **Note:** Ensure the URL is the correct format & only has the name & job details of the job you are tailoring your resume for , not any other jobs
    > 
    > A sample url would be:
    > 
    > https://[company name].wd1.myworkdayjobs.com/en-US/CorporateCareers/ **job/Some-Role-Name_3_JobID**
    >
    > and not 
    > 
    > https://[company name].wd1.myworkdayjobs.com/en-US/CorporateCareers/ **details/Some-Role-Name_3_JobID**
    > 
    > The latter has other HTML elements and is not the XPath used in this project to get the job description 

4. From the root of the dierctory, simply run the main script using:
    
    ```python (or python3) main.py```

4. The tailored resumes can be found in respective `/resumes/company/job_id/` folders. The script generates 2 resumes, a `.docx` resume, and a `.pdf` resume. The `.docx` can be further tailored and exported to `.pdf` if required.

## Future Work:
1. Improve error handling.
2. Scrapers for other websites (Glassdoor etc.).
3. Ability to use other LLMs (OpenAI, mistral etc.).