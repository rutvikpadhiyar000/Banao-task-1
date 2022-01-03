from django.http.response import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from .job_name_scrap import get_jobs_dict
from .models import JobCatag, JobName, JobDetails, CompanyDetails
from .scraper import get_job_data_from_name, get_company_data, login_to_linkedin

# Create your views here.


def getjobnames(request):
    job_dict = get_jobs_dict()
    for key, value in job_dict.items():
        catag = JobCatag.objects.create(catag=key)
        for i in value:
            JobName.objects.create(name=i, catag=catag)
    return HttpResponse(job_dict)


def getjobs(request, jobname):
    driver = webdriver.Chrome(ChromeDriverManager().install())

    job_details, job_company_dict = get_job_data_from_name(driver, jobname)

    # Need to login to get company data
    login_link = "https://www.linkedin.com/authwall?trk=bf&trkInfo=AQELd4yPwv2R5QAAAX4Bt0Dwm_qV1ILFWFMnUzQ-UA2DpmNmOr2fmiwYL9OL5PFIlVih-GP0svwER2Dc3eWFVuyfNAUG_cM_ZjoQkG9hylKLPLMGJKfd8Zt7gUpz4o0726CFpic=&originalReferer=&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fcompany%2Ftesla-motors%3Ftrk%3Dpublic_jobs_jserp-result_job-search-card-subtitle"
    login_to_linkedin(driver, login_link)

    for name, link in job_company_dict.items():
        company_details = get_company_data(driver, link)
        company = CompanyDetails.objects.create(
            name=name, desc=company_details[2], location=company_details[0]
        )
        time.sleep(2)
        for job in job_details:
            if job[1] == company.name:
                JobDetails.objects.create(
                    company=company, position=job[0], location=job[2]
                )

    return HttpResponse("Got Data")
