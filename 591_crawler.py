import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from house import House
from mongo_client import MongoPipeline


chromedriver = r"driver\chromedriver.exe"


def get_house_info(link, browser):
    # element = wait.WebDriverWait(EC.element_to_be_clickable((By.XPATH, r'//*[@id="rightConFixed"]/section/div[1]/div[2]/p[1]')))
    browser.get(link)
    name = browser.find_element_by_xpath(r'//*[@id="rightConFixed"]/section/div[1]/div[2]/p[1]')
    print(name, link)


mongo_pipe = MongoPipeline()
with webdriver.Chrome(chromedriver) as browser:
    browser.implicitly_wait(10)
    browser.maximize_window()
    sourceurl = 'https://rent.591.com.tw/'
    browser.get(sourceurl)
    # //*[@id="area-box-body"]/dl[1]/dd[1]

    # Houses
    # //*[@id="content"]/ul[1]/li[2]/h3/a
    # //*[@id="content"]/ul[2]/li[2]/h3/a
    # //*[@id="content"]/ul[3]/li[2]/h3/a
    # ...
    # //*[@id="content"]/ul[30]/li[2]/h3/a
    # //*[@id="content"]/ul[1]/li[2]/h3/a
    target_city = "台北市"
    districts = {"台北市": '//*[@id="area-box-body"]/dl[1]/dd[1]',
                 "新北市": '//*[@id="area-box-body"]/dl[1]/dd[2]'}
    clickme = browser.find_element_by_xpath(districts["台北市"])
    clickme.click()
    time.sleep(10)

    houses = browser.find_elements_by_xpath(r"//*[@id='content']/ul/li[2]/h3/a")
    print("hello")
    userElems = len(houses)

    cur_win = browser.current_window_handle
    next_button = browser.find_element_by_xpath(r'//*[@id="container"]/section[5]/div/div[1]/div[5]/div/a[8]/span')

    while(next_button.value_of_css_property('color') == 'rgba(57, 62, 66, 1)'):
        print(browser.current_url)

        temp = []
        for i in range(1, len(houses) + 1):
        # for i in range(1, 3):
            print(f"==== {i} ====")

            xpath = f"//*[@id='content']/ul[{i}]/li[2]/h3/a"

            wait = WebDriverWait(browser, 10)
            accept = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            browser.execute_script("arguments[0].scrollIntoView(true);", accept)
            actions = ActionChains(browser)
            actions.move_to_element(accept).click().perform()

            # each house
            browser.switch_to.window(browser.window_handles[-1])

            # get info of each house
            print(browser.current_url)
            house_id = browser.current_url.split('/')[-1]
            raw_name = browser.find_element_by_xpath(r'//*[@id="rightConFixed"]/section/div[1]/div[2]/p[1]').text
            role = raw_name.split(':')[0]
            gender = "小姐" if "小姐" in raw_name else "先生"
            name = raw_name.split(gender)[0].split(' ')[-1] + gender
            # print("role: ", role)
            # print("name: ", name)
            # print("gender: ", gender)
            phone_num = browser.find_element_by_xpath(r'//*[@id="rightConFixed"]/section/div[2]/div/div[1]/span[2]').text
            # print("phone_num: ", phone_num)
            house_kind = browser.find_element_by_xpath(r'//*[@id="houseInfo"]/div[2]/span[7]').text
            # print("kind: ", house_kind)
            room_kind = browser.find_element_by_xpath(r'//*[@id="houseInfo"]/div[2]/span[1]').text
            # print("room_kind: ", room_kind)
            accepted_gender = None
            try:
                desc = browser.find_element_by_xpath(r'//*[@id="service"]/div[3]/div/span').text
                if "不限" in desc or "男女皆可" in desc:
                    accepted_gender = "不限"  # ex: 不限男女
                elif "限女" in desc:
                    accepted_gender = "限女"
                elif "限男" in desc:
                    accepted_gender = "限男"
                else:
                    # Other or uncovered
                    accepted_gender = desc
            except:
                pass
            # print("accepted_gender: ", accepted_gender)
            house = House(house_id, target_city, name, role, phone_num, house_kind, room_kind, accepted_gender)
            temp.append(house)
            # browser.switch_to.window(browser.window_handles[0])
            browser.switch_to.window(cur_win)

        mongo_pipe.process_items(temp)

        # close other tabs
        origin_tab = browser.window_handles[0]
        for tab in browser.window_handles:
            if tab != origin_tab:
                browser.switch_to.window(tab)
                browser.close()
        browser.switch_to.window(origin_tab)

        # go to next page
        scrolls = 2
        while True:
            scrolls -= 1
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            if scrolls < 0:
                break
        browser.find_element_by_xpath(r'//*[@id="container"]/section[5]/div/div[1]/div[5]/div/a[last()]/span').click()
        time.sleep(5)

        cur_win = browser.current_window_handle
        next_button = browser.find_element_by_xpath(r'//*[@id="container"]/section[5]/div/div[1]/div[5]/div/a[last()]/span')