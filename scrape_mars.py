#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import dependencies
import pandas as pd
import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Configure ChromeDriver
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# # NASA Mars News

# In[3]:


url = "https://mars.nasa.gov/news/"
browser.visit(url)


# In[4]:


html = browser.html
news_soup = BeautifulSoup(html, "html.parser")
mars_news = news_soup.select_one("ul.item_list li.slide")


# In[5]:


mars_news.find("div", class_="content_title")


# In[ ]:


news_title = mars_news.find("div", class_="content_title").get_text()
print(news_title)


# In[ ]:


news_paragraph = mars_news.find("div", class_="article_teaser_body").get_text()
print(news_paragraph)


# # JPL Mars Space Images - Featured Image

# In[ ]:


# Visit the NASA JPL (Jet Propulsion Laboratory) Site

url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[ ]:


# <button class="full_image">Full Image</button>
full_image_button = browser.find_by_id("full_image")
full_image_button.click()


# In[ ]:


browser.is_element_present_by_text("more info", wait_time=1)
more_info_element = browser.find_link_by_partial_text("more info")
more_info_element.click()


# In[ ]:


# Parse Results HTML with BeautifulSoup
html = browser.html
image_soup = BeautifulSoup(html, "html.parser")


# In[ ]:



img_url = image_soup.select_one("figure.lede a img").get("src")
img_url


# In[ ]:


# Use Base URL to Create Absolute URL
img_url = f"https://www.jpl.nasa.gov{img_url}"
print(img_url)


# # Mars Facts

# In[ ]:


def mars_facts():
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    mars_facts_df = pd.read_html(url)
    mars_facts_df = mars_facts_df[0]
    mars_facts_df.columns = ['Description', 'Mars']
    mars_facts_df

    mars_facts_html = mars_facts_df.to_html(classes='table table-striped')
    
    return mars_facts_html


# In[ ]:


# Visit the Mars Facts Site Using Pandas to Read
mars_df = pd.read_html("https://space-facts.com/mars/")[0]
print(mars_df)
mars_df.columns=["Description", "Value"]
mars_df.set_index("Description", inplace=True)
mars_df


# In[ ]:


# Visit the USGS Astrogeology Science Center Site
# executable_path = {"executable_path": "/Users/redea/.wdm/drivers/chromedriver/win32/87.0.4280.88/chromedriver"}
# browser = Browser("chrome", **executable_path, headless=False)
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)


# # Mars Hemispheres

# In[ ]:



hemisphere_image_urls = []

# Get a List of All the Hemispheres
links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
    browser.find_by_css("a.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
    sample_element = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append Hemisphere Object to List
    hemisphere_image_urls.append(hemisphere)
    
    # Navigate Backwards
    browser.back()
hemisphere_image_urls


 #if __name__ == '__main__':
    #scrape_all()



