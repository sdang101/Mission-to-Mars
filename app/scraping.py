# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "mars_hemisphere":mars_hemi(browser)
        }
    
    browser.quit()
    
    return data

def mars_hemi(browser):
    try:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        soup = BeautifulSoup(browser.html, 'html.parser')
        # Get the 4 hemispheres where class ='item'
        hemispheres = soup.find_all('div', class_='item')

        # Create empty list for image urls
        hemisphere_image_urls = []
        # Loop through each hemisphere
        for hemisphere in hemispheres:
            title = (hemisphere.h3.string).replace(' Enhanced', '')
            img_cache_url = hemisphere.img['src']
            img_url = f'https://astrogeology.usgs.gov/{img_cache_url}'
            print(img_url)
            hemisphere_image_urls.append({'title': title, 'img_url': img_url})  
    except AttributeError:
        return None

    return hemisphere_image_urls

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)
    
    # HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Pinpoints the <ul /> tag with a class of 'item_list',and the <li /> tag with the class of 'slide' 
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


# Featured Images
def featured_image(browser):
    try:
        # Visit URL
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        a_tag = img_soup.find("a", class_ = "button fancybox")
        featured_image_url = a_tag["data-fancybox-href"]
        featured_image_url_with_root = f'https://www.jpl.nasa.gov{featured_image_url}'
    except AttributeError:
        return None
        
    return featured_image_url_with_root


# --- Scrape Mars Data: Mars Facts ---
def mars_facts():
    # Add try/except for error handling
    try:
        # Create new DataFrame from the HTML table at index 0
        df = pd. read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns to the new DataFrame
    df.columns=['Description', 'Mars']
    # Turn Description columns into DataFrame's index
    df.set_index('Description', inplace=True) # True means updated indes will remain in place, w/out having the reassign DataFrame to new variable
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())