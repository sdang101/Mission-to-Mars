
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
        "last_modified": dt.datetime.now()
        }
    
    browser.quit
    
    return data


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
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    # The browser finds an element by its id.
    full_image_elem = browser.find_by_id('full_image')
    # Splinter will 'click' the image to view its full size and save the scraping results in 'full_image_elem'
    full_image_elem.click()

    # Find the more info button and click that
    # Tells Splinter to search through the HTML for the specific text "more info."
    browser.is_element_present_by_text('more info', wait_time=1)
    # Find the link associated with the 'more info' text
    more_info_elem = browser.find_link_by_partial_text('more info')
    # Tell Splinter to click that link by chaining the '.click()' function onto our 'more_info_elem'
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        # figure.lede references the <figure /> tag and its class, lede
        img_url_rel = img_soup.select_one('figure.lede a img').get("src") # .get("src") pulls the link to the image
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url
    return img_url


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