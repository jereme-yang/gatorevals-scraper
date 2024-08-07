from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time
import pickle
WEBSITE_URL = "https://public.tableau.com/views/GatorEvalsThreeTermDataincludingSpring2024/GatorEvalsPublic?%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Aembed=true&%3Alanguage=en-US&:embed=y&:showVizHome=n&:apiID=host0#navType=1&navSrc=Parse"


def scroll_through_names(driver, n = 28):
    time.sleep(0.5)
    for _ in range(n):
        ActionChains(driver)\
        .key_down(Keys.END)\
        .key_up(Keys.END)\
        .perform()
        time.sleep(0.5)


def initialize_webdriver():
    # initialize chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_experimental_option("detach", True) 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless=new") # run without opening a browser - comment this to debug

    # initialize driver
    driver = webdriver.Chrome(options=chrome_options)

    # connect driver to website
    driver.get(WEBSITE_URL)
    driver.implicitly_wait(5)

    # wait for website to load before continuing
    time.sleep(5) 

    return driver


driver = initialize_webdriver()

# open dropdown for instructor name
names_dropdown = driver.find_element(By.ID, "tabZoneId12")
names_dropdown.click()

# uncheck the all button
time.sleep(1)
all_checkbox = driver.find_element(By.NAME, "FI_sqlproxy.1j0k1xa05f9b0k18gqber1rlouv3,none:INSTRUCTOR_NAME:nk7413426041701531777_11695660129199681370_(All)")
all_checkbox.click()

# scroll through entire list
scroll_through_names(driver)

# grab all names list from pickle file
with open('./utils/all_names.pkl', 'rb') as inp:
    all_names = pickle.load(inp)


start_index = 0
# go through all profs, query the data
for i in range(start_index, len(all_names)):
    while True:
        try:
            if i == 198 or i == 199: # broken indexes
                continue
            
            # focus table by pressing all tab
            time.sleep(3)
            table = driver.find_element(By.XPATH, '//a[@title="(All)"]')
            time.sleep(3)
            table.click()
            time.sleep(0.5)d
            print("table focused", end=" | ")

            # get the checkbox for the associated name
            time.sleep(5)
            checkbox = driver.find_element(By.XPATH, f'//a[contains(text(), "{all_names[i]}")]/preceding-sibling::input')
            time.sleep(5)
            print("checkbox found", end=" => ")

            # click the checkbox (enable)
            checkbox.click()
            time.sleep(0.5)
            print("enabled", end=" | ")

            # close dropdown for instructor names
            body = driver.find_element(By.XPATH, '//div[@class="tab-glass clear-glass tab-widget"]')
            time.sleep(3)
            body.click()
            time.sleep(0.5)
            print("dropdown disabled", end=" | ")

            # find the canvas
            canvas = driver.find_element(By.ID, "view7413426041701531777_11695660129199681370")
            time.sleep(5)
            print("canvas found", end=" => ")

            # click on the canvas
            canvas.click()
            time.sleep(0.5)
            print("focused", end=" | ")

            # perform keypresses to display the first data point
            ActionChains(driver)\
                    .key_down(Keys.RETURN)\
                    .key_up(Keys.RETURN)\
                    .perform()
            incorrect_element = driver.find_element(By.XPATH, '//span[contains(text(), "'+"%"+' of Total Count of RESPONSE_VALUE along RESPONSE_CATEGORY:") and @style="font-family:\'Tableau Book\';font-size:13px;color:#787878;font-weight:normal;font-style:normal;text-decoration:none;"]')
            while incorrect_element:
                
                ActionChains(driver)\
                    .key_down(Keys.ARROW_RIGHT)\
                    .key_up(Keys.ARROW_RIGHT)\
                    .perform()
                try:
                    incorrect_element = driver.find_element(By.XPATH, '//span[contains(text(), "'+"%"+' of Total Count of RESPONSE_VALUE along RESPONSE_CATEGORY:") and @style="font-family:\'Tableau Book\';font-size:13px;color:#787878;font-weight:normal;font-style:normal;text-decoration:none;"]')
                except:
                    break
                        
            time.sleep(0.5)

            print("loading data...")
            ]
            # parse the data
            data = ["\""+all_names[i]+"\""]
            for j in range(10):
                
                datapoint = driver.find_element(By.XPATH, '//span[@style="font-family:\'Tableau Book\';font-size:13px;color:#333333;font-weight:bold;font-style:normal;text-decoration:none;"]').text
                time.sleep(0.5)
                data.append(datapoint)

                if j == 10:
                    break

                # move to next one
                ActionChains(driver)\
                        .key_down(Keys.ARROW_DOWN)\
                        .key_up(Keys.ARROW_DOWN)\
                        .perform()
            # data.append(college)
            time.sleep(0.5)
            print(f"{data}")

            # append to csv fjle
            with open("gator_evals_data.csv", 'a') as f_object:
                f_object.write("\n" + ",".join(data))
                f_object.close()
            print("added to csv", end=" | ")


            # re open dropdown for instructor names
            names_dropdown = driver.find_element(By.ID, "tabZoneId12")
            time.sleep(3)
            print("dropdown found", end=" => ")

            names_dropdown.click()
            time.sleep(1)
            print("clicked", end=" | ")

            # click "All" to focus the scrollable section
            table = driver.find_element(By.XPATH, '//a[@title="(All)"]')
            time.sleep(5)
            print("all found", end=" => ")
            table.click()
            time.sleep(1)
            print("clicked", end=" | ")

            # scroll through the names dropdown
            scroll_through_names(driver)
            print("scroll finished", end=" | ")

            # uncheck the professor that just got queried
            clicked_checkbox = driver.find_element(By.XPATH, '//input[@checked="checked"]')
            time.sleep(5)
            clicked_checkbox.click()
            print("checkbox disabled")
            break
        except:
            # run broke. known reasons: browser times out / broken index on tableau -> restart selenium
            time.sleep(5)
            print("BROKE")
            with open("broke.txt", 'a') as f_object:
                f_object.write(f"{i}, {all_names[i]}\n")
                f_object.close()
            driver.quit()


            driver = initialize_webdriver()

            # open dropdown for instructor name
            names_dropdown = driver.find_element(By.ID, "tabZoneId12")
            names_dropdown.click()

            # uncheck the all button
            time.sleep(1)
            all_checkbox = driver.find_element(By.NAME, "FI_sqlproxy.1j0k1xa05f9b0k18gqber1rlouv3,none:INSTRUCTOR_NAME:nk7413426041701531777_11695660129199681370_(All)")
            all_checkbox.click()

            # scroll through entire list
            scroll_through_names(driver)
            time.sleep(60)





