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


url = "http://nyheder.tv2.dk/folketingsvalg/kandidattest"

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

def answer_all():
    # execute js to click a button; for some reason
    # it doesn't work using selenium .click()
    #driver.execute_script('$("#answerdiv'+str(q)+' label.btn-default")['+str(val)+'].click()')

    randoms_js = []
    for i in range(0,21):
        randoms_js.append(random.randint(0,4))

    js = '''
        var randoms = '''+str(randoms_js)+'''; // 30 randoms
        var qs = $("li.t-bgcolor_offwhite div ul");
        for(var i = 1; i < qs.length; i++){ // skip 0th
            $($(qs[i]).children()[randoms[i-1]]).children()[1].click();
        }
        '''

    driver.execute_script(js)

    return randoms_js


def go_test():
    try:
        driver.delete_all_cookies()
        driver.get(url)

        el = Select(driver.find_element_by_id("question-municipality"))
        el.select_by_visible_text("København")

        # Temaer
        themes = list(range(14))
        pick1 = themes[random.randint(0,len(themes)-1)]
        themes.remove(pick1)
        pick2 = themes[random.randint(0,len(themes)-1)]

        js = '''
            // pick two random themes
            var themes = $("ul.c-candidate-test_item_answer_multi li label");
            themes['''+str(pick1)+'''].click();
            themes['''+str(pick2)+'''].click();
        '''

        driver.execute_script(js)

        qs = answer_all()
        data = {'questions': {}, 'result': {}}
        for i,q in enumerate(qs):
            data['questions'][str(i+1)] = q

        # se resultatet
        time.sleep(1)
        driver.find_element_by_css_selector('button[type=submit]').click()

        # get result
        res_names = driver.find_elements_by_css_selector('span.c-candidate_name')
        res_percentage = driver.find_elements_by_css_selector('div.c-candidate_result strong')
        res_parties = driver.find_elements_by_css_selector('div.c-candidate_party :nth-child(2)')

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
        raise e
        return None


if __name__ == "__main__":
    r = go_test()
    if r:
        with open('data/data'+sys.argv[1]+'.json', 'w') as outfile:
            json.dump([r], outfile)

    close()

