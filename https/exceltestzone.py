from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO
import json


driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get('https://www.exceltestzone.com.au/')
sleep(5)
driver.find_element_by_id("username").send_keys("saga65518")
driver.find_element_by_id("password").send_keys("good63")
form = driver.find_element_by_name('login')
form.click()

sleep(5)
takeTest = driver.find_element_by_id("tests")
takeTest.click()

sleep(2)
select_maths_option = driver.find_elements_by_xpath('//*[@id="filter_form"]/table/tbody/tr/td[1]/input[5]')[0].click()

sleep(5)


allQuestionPaper = []
testHeadings = []
testTimings = []
domain = "https://www.exceltestzone.com.au"
request = requests.Session()
htmlContent = BeautifulSoup(driver.page_source)
testLinks = htmlContent.findAll('a', {"title" : "Take Test"})
parser_main = etree.HTMLParser()
tree_main = etree.parse(StringIO(driver.page_source), parser_main)
for i in range(1, len(testLinks) + 1):
    testHeadings.append(tree_main.xpath('//*[@id="content_wrapper"]/div[3]/div[2]/div/table/tbody/tr[{0}]/td[1]/text()'.format(i))[0])
for i in range(1, len(testLinks) + 1):
    testTimings.append(tree_main.xpath('//*[@id="content_wrapper"]/div[3]/div[2]/div/table/tbody/tr[{0}]/td[7]/text()'.format(i))[0])
for index, link in enumerate(testLinks):
    linkText = driver.get(domain + link['href'])
    startTest = driver.find_elements_by_xpath('//*[@id="wrapper"]/div/div[5]/div/div[1]/a')[0].click()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(driver.page_source), parser)
    Question = []
    Answer = []
    for i in range(0, 50):
        try:
            dummy_question = []
            dummy_question_new = []
            dummy_answer_new = []
            questions = []
            parser1 = etree.HTMLParser()
            tree1 = etree.parse(StringIO(driver.page_source), parser1)
            img = tree1.xpath('//*[@id="wrapper"]/div/div[6]/div[2]/div//@src')

            questions += tree1.xpath(
                '//*[@id="wrapper"]/div/div[6]/div[2]/div/div[3]//text()') + tree1.xpath(
                '//*[@id="wrapper"]/div/div[6]/div[2]/div/div[4]//text()')

            for image in img:
                if 'stimulus' in image:
                    questions.append(image)

            for question in questions:
                dummy_question.append(question.strip())
            for question in dummy_question:
                if question != "":
                    dummy_question_new.append(question)
            Question.append(",".join(dummy_question_new))
            getAnswers = BeautifulSoup(driver.page_source)
            if (len(getAnswers.findAll("span", {"for": "radio-answer1"})) != 0):
                for i in range(1, 5):
                    dummy_answer_new.append(getAnswers.findAll("span", {"for": "radio-answer{0}".format(i)})[0].text)
            else:
                for i in range(1, 5):
                    dummy_answer_new.append(
                        getAnswers.findAll("div", {"class": "image answer{0}".format(i)})[0].find('img')['src'])

            Answer.append(",".join(dummy_answer_new))
            selectOption = driver.find_element_by_xpath('//*[@id="answer1"]/a/div[2]')
            selectOption.click()

            sleep(2)
            nextQuestion = driver.find_elements_by_xpath('//a[@title="Next Question"]')[0].click()
            sleep(5)
        except:
            break
    dic = {}
    dic['Title'] = testHeadings[index]
    dic['Timing'] = testTimings[index]
    dic['Question'] = Question
    dic['Answer'] = Answer

    allQuestionPaper.append(dic)

with open('Question.txt', 'w') as f:
  json.dump(allQuestionPaper, f, ensure_ascii=False)

