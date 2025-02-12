import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import csv


base_url = "https://indiankanoon.org/search/?formInput=murder%20%20%20doctypes%3A%20gujarat%20year%3A%202016&pagenum="


def get_driver():
    options = uc.ChromeOptions()
    options.headless = False  
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    return driver

def get_case_details(driver, case_url):
    driver.get(case_url)
    time.sleep(5)
    
    
    try:
        view_complete = driver.find_element("link text", "View Complete document")
        view_complete.click()
        time.sleep(3)  
    except:
        print("No 'View Complete document' link found")
    
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    print(f"Fetching case details from: {case_url}")
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
   
    doc2_content = soup.find("div", class_="doc2")
    if doc2_content:
        print("Found content in doc2")
        return doc2_content.get_text(strip=True)
    
   
    highlighted_text = soup.find_all(class_="highlight_text")
    if highlighted_text:
        print("Found highlighted text")
        return " ".join([span.get_text(strip=True) for span in highlighted_text])
    
    
    highlighted = soup.find_all(class_="highlight")
    if highlighted:
        print("Found highlight class text")
        return " ".join([span.get_text(strip=True) for span in highlighted])
    
    
    text_blocks = []
    for element in soup.find_all(["p", "div"], class_=["doc_content", "judgments"]):
        if element.get_text(strip=True):
            text_blocks.append(element.get_text(strip=True))
    
    if text_blocks:
        print("Found content in text blocks")
        return "\n".join(text_blocks)
    
    
    try:
        expand_buttons = driver.find_elements("css selector", ".context_button")
        for button in expand_buttons:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
        
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        expanded_content = soup.find_all(class_="highlight_text")
        if expanded_content:
            print("Found content after expanding sections")
            return " ".join([span.get_text(strip=True) for span in expanded_content])
    except Exception as e:
        print(f"Error expanding sections: {e}")
    
    print("No content found. URL:", case_url)
    return "Content not found"

def scrape_page(driver, url):
    driver.get(url)
    time.sleep(7)  
    
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    print("Page source length:", len(driver.page_source))
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    
    results = soup.find_all("div", class_="result_title")
    if not results:
        results = soup.find_all("div", class_="result")
        
    print(f"Found {len(results)} results on page")
    
    cases = []
    for result in results:
        try:
            link_elem = result.find("a")
            if link_elem:
                case_title = result.get_text(strip=True)
                case_link = "https://indiankanoon.org" + link_elem["href"]
                case_content = get_case_details(driver, case_link)
                cases.append((case_title, case_link, case_content))
                print(f"Successfully scraped case: {case_title[:50]}...")
                time.sleep(3)  # Add delay between cases
        except Exception as e:
            print(f"Error processing result: {e}")
    
    return cases

def main():
    driver = get_driver()
    all_cases = []
    page_num = 1
    
    try:
        while True:  # Loop through all pages
            url = base_url + str(page_num)
            print(f"Scraping page {page_num}...")
            
            driver.get(url)
            time.sleep(3)
            
            # Check if we've reached the last page
            if "No documents found" in driver.page_source:
                print(f"No more results found after page {page_num-1}")
                break
                
            cases = scrape_page(driver, url)
            
            # If no cases found on this page, we've probably reached the end
            if not cases:
                print(f"No cases found on page {page_num}, stopping...")
                break
                
            all_cases.extend(cases)
            print(f"Completed page {page_num}. Total cases so far: {len(all_cases)}")
            
            page_num += 1
            time.sleep(2)  
            
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
    finally:
        driver.quit()
    
    # Save data to CSV
    with open("cases.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Case Title", "Case Link", "Case Content"])
        writer.writerows(all_cases)
    
    print(f"Scraping completed. Total cases scraped: {len(all_cases)}")
    print("Data saved to cases.csv")

if __name__ == "__main__":
    main()