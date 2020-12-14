import csv
from json import load
import requests
from .json_extractor import *


# Uses Duke's API to find all Duke courses that match with the current user's preferences. Writes these to a CSV to be
# downloaded and also returns data to be used by the front end
def find_personal_courses(preferences):
    data = load(open('course_codes.json'))
    courses = data['scc_lov_resp']['lovs']['lov']['values']['value']

    found_codes = []
    for course in courses:
        for pref in preferences:
            if pref != "" and pref.lower() == course['desc'].lower() and course['code'] not in found_codes and '_' not in course['code']:
                found_codes.append(course['code'])

    found_courses = [['Subject', 'Course Title', 'When Course Occurs', 'Course ID']]
    for code in found_codes:
        url = 'https://streamer.oit.duke.edu/curriculum/courses/subject/' + code + '?access_token=ba76439cca2e05f5860f3245ecbe7c77'
        resp = requests.get(url=url)
        data = resp.json()
        titles = json_extract(data, 'course_title_long')
        ids = json_extract(data, 'crse_id')
        subject = json_extract(data, 'subject')
        occurs = json_extract(data, 'ssr_crse_typoff_cd_lov_descr')
        for i in range(len(titles)):
            found_courses.append([subject[i], titles[i], xstr(occurs[i]), ids[i]])

    with open("duke_courses_for_you.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(found_courses)

    return found_courses


def xstr(s):
    return '' if s is None else str(s)