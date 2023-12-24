import requests
import time
from bs4 import BeautifulSoup


def find_jobs(soup):
    try:
        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
        for index, job in enumerate(jobs):
            published_date = job.find('span', class_='sim-posted').span.text
            if 'few' not in published_date:
                continue
            company_name = job.find(
                'h3', class_='joblist-comp-name').text.strip()
            skills = job.find(
                'span', class_='srp-skills').text.replace(' ', '').strip()
            if filter_out_skill in skills:
                continue
            more_info = job.header.h2.a['href']

            with open(f"posts/{index+1}.txt", 'w') as file:
                file.write(f"Company Name: {company_name} \n")
                file.write(f"Skill required: {skills} \n")
                file.write(f"More Info: {more_info}")
            print(f"File Saved: {index+1}.txt")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        print('Enter skill you want to filter')
        filter_out_skill = input('>')
        print(f"Filtering out {filter_out_skill}...")

        URL = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation='
        html_text = requests.get(URL).text
        soup = BeautifulSoup(html_text, 'lxml')

        while True:
            find_jobs(soup)
            time_wait = 60
            print(f"Waiting {time_wait} minutes...")
            time.sleep(time_wait * 60)

    except Exception as e:
        print(f"Error: {e}")
