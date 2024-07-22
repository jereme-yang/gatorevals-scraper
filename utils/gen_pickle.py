from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time
import pickle


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def scroll_through_names(driver, n = 28):
    time.sleep(0.5)
    for _ in range(n):
        ActionChains(driver)\
        .key_down(Keys.END)\
        .key_up(Keys.END)\
        .perform()
        time.sleep(0.5)


# chrome options to ignore ssl error and start maximized
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument("--enable-javascript")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless=new")

# connect driver to website
website = "https://public.tableau.com/views/GatorEvalsThreeTermDataincludingSpring2024/GatorEvalsPublic?%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Aembed=true&%3Alanguage=en-US&:embed=y&:showVizHome=n&:apiID=host0#navType=1&navSrc=Parse"
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)
driver.implicitly_wait(5)

# wait for website to load before continuing
time.sleep(5) 

# open dropdown for instructor name
names_dropdown = driver.find_element(By.ID, "tabZoneId12")
names_dropdown.click()

# uncheck the all button
time.sleep(1)
all_checkbox = driver.find_element(By.NAME, "FI_sqlproxy.1j0k1xa05f9b0k18gqber1rlouv3,none:INSTRUCTOR_NAME:nk7413426041701531777_11695660129199681370_(All)")
all_checkbox.click()

# scroll through entire list
scroll_through_names(driver)

# grab all names (str) for finding the tags (title="name")
all_name_elements = driver.find_elements(By.CLASS_NAME, "FIText")
all_names = [element.text for element in all_name_elements][2:]
del all_name_elements

# save the list of names
save_object(all_names, 'all_names.pkl')
