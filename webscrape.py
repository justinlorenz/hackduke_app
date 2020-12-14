from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
response = requests.get("https://www.coursera.org/courses")
html_soup = BeautifulSoup(response.content, 'html.parser')

url = html_soup.find_all(href=True)

def auto_Scrapper(html_tag,course_case):
  for i in range(1,100):
    url = "https://www.coursera.org/courses?page=" +str(i) + "&index=prod_all_products_term_optimization"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for j in range(0,9):
      x = soup.find_all(html_tag)[j].get_text()
      course_case.append(x)


def auto_Scrapper_Class(html_tag,course_case,tag_class):
  for i in range(1,100):
    url = "https://www.coursera.org/courses?page=" +str(i) + "&index=prod_all_products_term_optimization"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for j in range(0,9):
      try:
        x = soup.find_all(html_tag, class_ = tag_class)[j].get_text()
        course_case.append(x)
      
      except:
        course_case.append("null")
        

course_title = []
course_organization = []
course_Certificate_type = []
course_rating = []
course_difficulty = []
course_students_enrolled = []


auto_Scrapper('h2',course_title)
auto_Scrapper_Class('span',course_organization,'partner-name m-b-1s')
auto_Scrapper_Class('div',course_Certificate_type,'_jen3vs _1d8rgfy3')
auto_Scrapper_Class('span',course_rating,'ratings-text')
auto_Scrapper_Class('span',course_difficulty,'difficulty')
auto_Scrapper_Class('span',course_students_enrolled,'enrollment-number')


courses_df = pd.DataFrame({'course_title': course_title,
                          'course_organization': course_organization,
                          'course_Certificate_type': course_Certificate_type,
                          'course_rating':course_rating,
                           'course_difficulty':course_difficulty,
                           'course_students_enrolled':course_students_enrolled})
courses_df = courses_df.sort_values('course_title')

courses_df.to_csv('UCoursera_Courses1.csv')
with open('courses.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    for row in reader:
        print(row)
