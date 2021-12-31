import requests
from bs4 import BeautifulSoup
import json


def main():
    job_dict = get_jobs_dict()
    # Commit to Json file
    with open("jobs.json", "w") as fp:
        json.dump(job_dict, fp)


def get_jobs_dict() -> dict:
    """Gets jobs from careerguide.com and returns it
    as dictionary object.
    """
    url = "https://www.careerguide.com/career-options"

    # Create soup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Get all required elements from HTML
    job_catags = soup.find_all("h2", class_="c-font-bold")
    job_list = soup.find_all("ul", class_="c-content-list-1 c-theme c-separator-dot")

    # Create Dictionary of {job_catagory: job_list}
    job_dict = {}
    for i in range(len(job_catags)):
        job_dict[job_catags[i].a.text] = [job.a.text for job in job_list[i]]

    return job_dict


if __name__ == "__main__":
    main()
