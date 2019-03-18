# This Python file uses the following encoding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time 
import random
import json
import sys


url = "https://www.altinget.dk/kandidater/ft19/holdningsprofil.aspx?opstillingskreds=12"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

try:
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(3)
except:
    sys.exit()


def close():
    try:
        driver.close()
    except:
        pass

def answer(val, q):
    # execute js to click a button; for some reason
    # it doesn't work using selenium .click()
    driver.execute_script('$("#answerdiv'+str(q)+' label.btn-default")['+str(val)+'].click()')


def go_test():
    try:
        driver.get(url)

        # remove annoying popup
        try:
            time.sleep(.1)
            p = driver.find_elements_by_class_name('btn-allowcookies')[0].click()
            time.sleep(.1)
        except:
            pass

        data = {'questions': {}, 'result': {}}

        # answer questions
        for i in range(1,31):
            v = random.randint(0,3)
            data['questions'][str(i)] = v
            answer(v, i)

        try:
            # "se dit resultat"
            driver.find_element_by_id('submit').click()
        except:
            # popup might have shown up now :/
            p = driver.find_elements_by_class_name('btn-allowcookies')[0].click()
            time.sleep(.1)
            driver.find_element_by_id('submit').click()

        res_names = driver.find_elements_by_css_selector('div.media-body h3.media-heading a')
        res_percentage = driver.find_elements_by_css_selector('div.media-body p strong')
        res_parties = driver.find_elements_by_css_selector('div.media-body :nth-child(4)')

        data['result'] = {
            'top1': {'name': res_names[0].text, 'percentage': res_percentage[0].text, 'parti': res_parties[0].text},
            'top2': {'name': res_names[1].text, 'percentage': res_percentage[1].text, 'parti': res_parties[1].text},
            'top3': {'name': res_names[2].text, 'percentage': res_percentage[2].text, 'parti': res_parties[2].text},
            'top4': {'name': res_names[3].text, 'percentage': res_percentage[3].text, 'parti': res_parties[3].text},
            'top5': {'name': res_names[4].text, 'percentage': res_percentage[4].text, 'parti': res_parties[4].text},
        }

        return data

    except Exception as e:
        close()
        return None


if __name__ == "__main__":
    master = []
    for i in range(0, 10):
        r = go_test()
        if r:
            master.append(r)

    with open('data/data'+sys.argv[1]+'.json', 'w') as outfile:
        json.dump(master, outfile)

    close()

