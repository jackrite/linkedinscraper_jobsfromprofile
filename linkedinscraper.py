import time
import pandas as pd    
import random
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import psutil
from datetime import datetime



def startscrape():
    # Get a list of running processes and kill previous instance of chrome
    for proc in psutil.process_iter(['name']):    
        try:
            if proc.info['name'] == 'chrome.exe':
                proc.terminate()
        except psutil.AccessDenied:
            continue
    #for chrome version 119
    chrome_options = webdriver.ChromeOptions()
    #path to the profil folder of chrome , replace username with your own
    pathprofil=r'C:\Users\username\AppData\Local\Google\Chrome\User Data'
    chrome_options.add_argument(f"--user-data-dir={pathprofil}")
    driver = webdriver.Chrome( options=chrome_options)
        

    driver.maximize_window()  
    driver.switch_to.window(driver.current_window_handle)
    driver.implicitly_wait(5)
    # list of recommended jobs or any personalized search
    driver.get('https://www.linkedin.com/jobs/collections/recommended/')

    timesl =random.randint(10, 20)
    time.sleep(timesl)

    job_titles, company_names,company_locations= [],[],[]
    lslinks,apply_method ,job_idcol= [],[],[]
    job_desc = []
    start = 2   


    page_state = driver.execute_script("return document.querySelector('.jobs-search-results-list__pagination .artdeco-pagination__page-state').textContent;")
    # endpage=int(page_state.split("of ")[1])+1 # allpages
    endpage=start+1  #only the first page
    
    try:
        for page in range(start,endpage):    
            li_elements = driver.find_elements(By.CSS_SELECTOR, '.jobs-search-results-list [data-occludable-job-id]')
            
            for li in li_elements:
                time.sleep(random.randint(5, 20))
                driver.execute_script("arguments[0].scrollIntoView();", li)
                action = ActionChains(driver)
                action.move_to_element(li).click().perform()
                             
                job_id = li.get_attribute("data-occludable-job-id")
                jbt = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title"))).text
                info = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "job-details-jobs-unified-top-card__primary-description"))).text                
                name, location, nr_app = info.split(' · ')
                try:           
                    apply_button = driver.find_element(By.XPATH, "//div[@class='jobs-apply-button--top-card']//span[@class='artdeco-button__text']").text
                except:
                    pass
                
                xpathlink=f"//a[contains(@href, '{job_id}')]"
                link = driver.find_element(By.XPATH,xpathlink)
                linkjob=link.get_attribute('href')                
                job_text = driver.find_element(By.XPATH,'//*[@id="job-details"]').text     
                                
                for i,j in zip((job_titles,company_names,company_locations,apply_method,job_desc,job_idcol,lslinks),
                               (jbt,name,location,apply_button,job_text,job_id,linkjob)):
                    i.append(j)
            driver.find_element(By.XPATH,f"//button[@aria-label='Page {page}']").click()
            print(f'PAGE {start-1} ')
            time.sleep(random.randint(15, 30))
    except:
        pass

    # Creating the dataframe 
    df = pd.DataFrame( {i:j for i,j in zip(['job_title','company_name','company_location','apply_method','description','job_id','link'],
                                           [job_titles,company_names,company_locations,apply_method,job_desc,job_idcol,lslinks]   )})
    date_string = datetime.now().strftime("%d_%m_%y")
    filename=f'job_offers{date_string}.csv'
    df.to_csv(filename, index=False)

    print('DONE')

if __name__ == "__main__":
    startscrape()