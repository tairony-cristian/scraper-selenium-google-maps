#Se parar de funcionar, apagar a pasta que se encontra no caminho 
#C:\Users\User\.wdm\drivers\chromedriver, e executar o sistema de novo
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re

# Configure Chrome options (optional)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keep browser open after script execution (optional)

# Create a new Chrome session with WebDriver
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=chrome_options)

segmento = str(input('Informe o Segmento: '))
cidade = str(input('Informe a Cidade: '))

# Open Google Maps in preview mode
driver.get('https://www.google.com.br/maps/preview')
driver.maximize_window()

# Search for the segment in the specified city using XPath (more reliable)
search_box = WebDriverWait(driver, 10).until(  # Wait for search box to be present (up to 10 seconds)
    lambda driver: driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
)
search_box.send_keys(segmento + ' em ' + cidade)
time.sleep(2)  # Short wait for search suggestions (adjust as needed)

# Click the search button using XPath (more reliable)
search_button = WebDriverWait(driver, 10).until(
    lambda driver: driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]/span')
)
search_button.click()

time.sleep(5)  # Wait for search results to load (adjust as needed)

try: 
  
  try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
  except Exception:
    pass

  scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
  driver.execute_script("""
          var scrollableDiv = arguments[0];
          function scrollWithinElement(scrollableDiv) {
              return new Promise((resolve, reject) => {
                  var totalHeight = 0;
                  var distance = 1000;
                  var scrollDelay = 3000;
                  
                  var timer = setInterval(() => {
                      var scrollHeightBefore = scrollableDiv.scrollHeight;
                      scrollableDiv.scrollBy(0, distance);
                      totalHeight += distance;

                      if (totalHeight >= scrollHeightBefore) {
                          totalHeight = 0;
                          setTimeout(() => {
                              var scrollHeightAfter = scrollableDiv.scrollHeight;
                              if (scrollHeightAfter > scrollHeightBefore) {
                                  return;
                              } else {
                                  clearInterval(timer);
                                  resolve();
                              }
                          }, scrollDelay);
                      }
                  }, 200);
              });
          }
          return scrollWithinElement(scrollableDiv);
  """, scrollable_div)

  items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')

  results = []
  for item in items:
    data = {}

    try:
        data['Empresa'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
    except Exception:
      pass
    try:
      text_content = item.text
      tel_pattern = r'((\+?\d{1,3}\s?)?(\(?[1-9]{2}\)?\s?)?([9]{1})?(\d{4})-?(\d{4}))'
      matches = re.findall(tel_pattern, text_content)

      tel_numbers = [match[0] for match in matches]
      unique_tel_numbers = list(set(tel_numbers))

      data['tel'] = unique_tel_numbers[0] if unique_tel_numbers else None   
    except Exception:
        pass
    
    try:
        data['link'] = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
    except Exception:
      pass

    try:
        data['website'] = item.find_element(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction] div > a').get_attribute('href')
    except Exception:
      pass
    
    try:
        rating_text = item.find_element(By.CSS_SELECTOR, '.fontBodyMedium > span[role="img"]').get_attribute('aria-label')
        rating_numbers = [float(piece.replace(",", ".")) for piece in rating_text.split(" ") if piece.replace(",", ".").replace(".", "", 1).isdigit()]

        if rating_numbers:
           data['stars'] = rating_numbers[0]
           data['reviews'] = int(rating_numbers[1]) if len(rating_numbers) > 1 else 0
    except Exception:
      pass

    if (data.get('Empresa')):
      results.append(data)
    
  with open('results.json', 'w', encoding='utf-8') as f:
      json.dump(results, f, ensure_ascii=False, indent=2)

  # Criar DataFrame com os resultados
  df = pd.DataFrame(results)


  # Salvar DataFrame em um arquivo de planilha
  df.to_excel('results.xlsx', index=False)

finally:
  time.sleep(20)
  print('Dados coletados')
  driver.quit()
