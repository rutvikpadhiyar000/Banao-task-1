from os import write
from typing import Tuple
from selenium import webdriver
import time
import json
import csv

# Local Imports
from careerguide import job_name_scrap

# Comment out if not available
from my_secrets.my_secrets import LINKEDIN_USERNAME, LINKEDIN_PASSWORD

# Enter Linkedin username password here
# LINKEDIN_USERNAME = ""
# LINKEDIN_PASSWORD = ""


def main():

    # Creating a webdriver instance
    # This instance will be used to connect to LinkedIn
    driver = webdriver.Chrome("./chromedriver_v96_linux")

    # Get job name dictionary
    all_jobs = get_job_names(filename="careerguide/jobs.json")

    # Open CSV file to commit data about jobs
    csv_file = open("linkedin_scraped/job_details.csv", "w")
    write = csv.writer(csv_file)

    # Add header to CSV file
    write.writerow(["Title", "Company", "Location"])

    # select sample to iterate over
    sample_job_name_list = all_jobs["Automobile / Autocomponents"]

    # Iterate over sample jobs and commit title, company, location
    # to CSV file
    for job in sample_job_name_list[:1]:
        list_for_csv, company_dict = get_job_data_from_name(driver, job)

        # Add data to CSV file
        write.writerows(list_for_csv)

    csv_file.close()

    # Need to login to get company data
    login_link = "https://www.linkedin.com/authwall?trk=bf&trkInfo=AQELd4yPwv2R5QAAAX4Bt0Dwm_qV1ILFWFMnUzQ-UA2DpmNmOr2fmiwYL9OL5PFIlVih-GP0svwER2Dc3eWFVuyfNAUG_cM_ZjoQkG9hylKLPLMGJKfd8Zt7gUpz4o0726CFpic=&originalReferer=&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fcompany%2Ftesla-motors%3Ftrk%3Dpublic_jobs_jserp-result_job-search-card-subtitle"
    login_to_linkedin(driver, login_link)

    # get company data
    company_data = []
    for name, link in company_dict.items():
        company_data.append([name] + get_company_data(driver, link))

    # Add gethered data to CSV file
    csv_file = open("linkedin_scraped/company_details.csv", "w")
    write = csv.writer(csv_file)
    write.writerow(["Name", "Location", "Employee Numbers", "Description"])
    write.writerows(company_data)


def get_job_names(filename: str = None) -> dict:
    """Takes Json file with
    `job_catagory:job_name_list` as `key:value`
    and converts it into dictionary if no file is provided
    returns data from careerguide.com.
    """

    # Load jobs from json file if provided.
    if filename is not None:
        with open(filename) as fp:
            job_dict = json.load(fp)
            return job_dict

    # if json file is not provided than get jobs from internet.
    job_dict = job_name_scrap.get_jobs_dict()
    return job_dict


def get_transpose(lst: list) -> list:
    """Takes list of list and returns list of tuples
    as transpose of input.
    """
    return list(zip(*lst))


def get_job_data_from_name(driver, job_name) -> Tuple[list, dict]:
    """Tacks Driver and job name serches Linkedin jobs
    for job name and returns data about jobs on first page
    and dictionary of `company_name:company_link`
    """

    driver.get("https://www.linkedin.com/jobs/search?keywords=" + job_name)
    time.sleep(3)

    # Get job_title, job_company, job_location from job page
    job_title_result = driver.find_elements_by_class_name("base-search-card__title")
    job_company_links = driver.find_elements_by_css_selector(
        ".base-search-card__subtitle > a"
    )
    job_location_result = driver.find_elements_by_class_name(
        "job-search-card__location"
    )

    # Sometimes it gives login page if that happens we get empty
    # return value in which case try again
    if not job_title_result:
        return get_job_data_from_name(driver, job_name)

    # Extract text from webelements and get company links
    job_title_name_text = [_.text for _ in job_title_result]
    job_company_name_text = [_.text for _ in job_company_links]
    job_company_dict = {_.text: _.get_attribute("href") for _ in job_company_links}
    job_location_name_text = [_.text for _ in job_location_result]

    # Make transpose of data to commit in csv file
    lst = get_transpose(
        [job_title_name_text, job_company_name_text, job_location_name_text]
    )
    # list of job data and dictionary of company_name:company_link
    return lst, job_company_dict


def login_to_linkedin(driver, link) -> None:
    """Tackes Driver and login link and uses it to login to with
    predefines credentials.
    """
    driver.get(link)
    time.sleep(2)

    # Set to True for manual login
    manual_login = True

    if manual_login:
        time.sleep(60)
        return

    # Flip button (To go from signup to login page)
    try:
        flip_btn = driver.find_element_by_class_name(
            "authwall-join-form__form-toggle--bottom"
        )
    except Exception:
        flip_btn = driver.find_element_by_class_name("authwall-join-form__form-toggle")
    flip_btn.click()

    # Get username and password input boxes path
    username = driver.find_element_by_xpath('//*[@id="session_key"]')
    password = driver.find_element_by_xpath('//*[@id="session_password"]')

    # Input the email id and password
    username.send_keys(LINKEDIN_USERNAME)
    password.send_keys(LINKEDIN_PASSWORD)

    login_btn = driver.find_element_by_xpath(
        "//button[@class='sign-in-form__submit-button']"
    )
    login_btn.click()


def get_company_data(driver, link) -> list:
    """Tackes driver and company link and returns list containing
    basic data about company from linkedin if data is not found puts `NA`
    as placeholder."""

    # get company page
    driver.get(link)
    time.sleep(3)

    # get company data if we cant find something we put 'NA' in place.
    try:
        company_location = driver.find_element_by_css_selector(
            "div.inline-block > div.org-top-card-summary-info-list__info-item"
        ).text
    except Exception:
        company_location = "NA"

    try:
        company_employees = driver.find_element_by_css_selector(
            "div.display-flex.mt2.mb1 > a#ember45 > span"
        ).text
    except Exception as e:
        company_employees = "NA"

    try:
        company_desc = driver.find_element_by_css_selector(
            "div > div.ph5.pb5 > div#ember66 "
        ).text
    except Exception as e:
        try:
            company_desc = driver.find_element_by_css_selector(
                "div > div.ph5.pb5 > div#ember64"
            ).text
        except Exception:
            company_desc = "NA"

    # Get employee number from company employee string
    if company_employees != "NA":
        num_emp = ext_num_from_str(company_employees)
    else:
        num_emp = company_employees
    lst = [company_location, num_emp, company_desc]
    return lst


def ext_num_from_str(string) -> str:
    """Gets number from employee string of linkedin
    company page if."""
    lst = string.split()
    ret_val = lst[2]
    if ret_val == "employee":
        ret_val = "1"
    return ret_val


def make_unique_list(lst) -> list:
    """Removes Duplicate from list"""
    return list(set(lst))


if __name__ == "__main__":
    main()
