# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time


executable_path = {"executable_path": "chromedriver.exe"} 
browser = Browser("chrome", **executable_path, headless=False)



def scrape():
    missions_dict = {}
    
    missions_dict['news']= mars_news()
    missions_dict['featured_image']= featured_image()
    missions_dict['facts_table']= mars_facts() 
    missions_dict['hemispheres']= hemispheres()
    
    print(missions_dict)
    return missions_dict


#Latest Mars News
def mars_news():

    news_list = []
    
    NASA_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(NASA_news_url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        results = soup.find("div", class_='list_text')
        news_title = results.find('div', class_='content_title').get_text()
        news_p = results.find('div', class_='article_teaser_body').get_text()
        news_list.append({'news_title': news_title, 'news_p': news_p})         
     
    except AttributeError as e:
        print(e)
    
    print(news_list)
    return news_list
    
  
#JPL Mars Space Images    
def featured_image():
    
    NASA_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(NASA_images_url)
    
    html_image = browser.html
    soup_image = BeautifulSoup(html_image, 'html.parser')

    try:
        browser.find_by_id('full_image').click()
        time.sleep(1)
    
        html_image = browser.html
        soup_image = BeautifulSoup(html_image, 'html.parser')
     
        feature_image = soup_image.find('img', class_='fancybox-image')['src']
        feature_image_url = 'https://www.jpl.nasa.gov' + feature_image
    
    except AttributeError as e:
        print(e) 
    
    print(feature_image_url)
    return feature_image_url
    


#Mars Facts    
def mars_facts():  
    facts_url = 'https://space-facts.com/mars/'
    
    tables = pd.read_html(facts_url)
    facts_table = tables[0]
    facts_table = facts_table.rename(columns = {0: 'Description', 1: 'Value'})
    facts_table = facts_table.set_index('Description')
    html_table= facts_table.to_html()
    html_table = html_table.replace('\n', '')

    return html_table


#Mars Hemispheres
def hemispheres():
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(1)
   
    hemispheres = ['Cerberus', 'Schiaparelli','Syrtis Major','Valles Marineris']
    hemisphere_images = []

    for hemisphere in hemispheres:
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        try:
            browser.click_link_by_partial_text(f'{hemisphere} Hemisphere Enhanced')
            time.sleep(1)
        
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
        
            title = soup.find('h2', class_='title').text
            image = soup.find('img', class_='wide-image')['src']
            image_url = 'https://astrogeology.usgs.gov' + image

            browser.back()
            time.sleep(1)
        
            hemisphere_images.append({'title': title, 'img_url': image_url})
        
        except AttributeError as e:
            print(e) 
    
    print(hemisphere_images)
    return hemisphere_images
