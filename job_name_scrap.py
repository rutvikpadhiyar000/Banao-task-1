import requests
from bs4 import BeautifulSoup
import json

# URL for scraping
URL = "https://www.careerguide.com/career-options"

# Create soup
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# Get all required elements from HTML
job_catags = soup.find_all("h2", class_="c-font-bold")
job_list = soup.find_all("ul", class_="c-content-list-1 c-theme c-separator-dot")

# Create Dictionary of {job_catagory: job_name}
job_dict = {}
for i in range(39):
    job_dict[job_catags[i].a.text] = [job.a.text for job in job_list[i]]

# Commit to Json file
with open("jobs.json", "w") as fp:
    json.dump(job_dict, fp)
