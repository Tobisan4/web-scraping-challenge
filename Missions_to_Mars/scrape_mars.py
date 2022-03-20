#!/usr/bin/env python
# coding: utf-8

# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from time import sleep 

def scraper():
    # Setup splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = False)

    ### NASA Mars News
    ## Scrape for the latest News Title and Paragraph Text

    # Open the target url
    url_1 = "https://redplanetscience.com/"
    browser.visit(url_1)
    sleep(3)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(html, "html.parser")
    # Create lists that will hold the scraped information
    titles = []
    paragraphs = []
    # Retrieve all the elements that contain the News Title and Paragraph Text
    articles = news_soup.find_all("div", class_ = "list_text")
    # Iterate through each element and save the latest data to a list
    for article in articles:
        try:
            titles.append(article.find("div", class_ = "content_title").text)
            paragraphs.append(article.find("div", class_ = "article_teaser_body").text)
        except:
            print("Ooops something happened!")
    # Save and display the first entree in the News Title list
    news_title = titles[0]
    print(news_title)
    # Save and display the first entree in the News Paragraph list
    news_paragraph = paragraphs[0]
    print(news_paragraph)

    ### JPL Mars Space Images - Featured Image
    ## Find the image url for the current Featured Mars Image and assign the url string to a variable

    # Open the target url
    url_2 = "https://spaceimages-mars.com/"
    browser.visit(url_2)
    sleep(3)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html, "html.parser")
    # Retrieve all the elements that contains the  featured picture
    featured_picture = image_soup.find_all("a", class_ = "showimg fancybox-thumbs")
    # Iterate through each element and save the url to a variable
    for picture in featured_picture:
        try:
            href = picture["href"]
            featured_image_url = url_2 + href
        except:
            print("Ooops something happened!")
    # Display the url for the current Featured Mars Image
    print(f"featured image url: {featured_image_url}")  

    ### Mars Facts
    ##  Use Pandas to scrape the table containing facts about the planet

    # Open the target url
    url_3 = "https://galaxyfacts-mars.com/"
    browser.visit(url_3)
    sleep(3)
    # Scrape all the tabular data from the webpage and save to a list
    facts_tables = pd.read_html(url_3)
    # From the tables list, select and save to a dataframe the element that contains the comparison stats between Mars and Earth
    facts_table_df = facts_tables[0]
    # Create a dictionary that contains the column headers
    facts_table_dict = {
        0 : "Description",
        1 : "Mars",
        2 : "Earth"
    }
    # Rename the column headers based on the dictionary
    facts_table_df.rename(columns = facts_table_dict, inplace = True)
    # Set the "Description" column as index
    facts_table_df.set_index("Description", drop = True, inplace = True)
    # Display the dataframe
    print(facts_table_df)
    # Generate the HTML table from the dataframe
    facts_table_html = facts_table_df.to_html()
    # Display the HTML table
    print(facts_table_html)

    ### Mars Hemispheres
    ## Scrape to obtain high resolution images for each of Mar's hemispheres

    # Open the target url
    url_4 = "https://marshemispheres.com/"
    browser.visit(url_4)
    sleep(3)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    hs_soup = BeautifulSoup(html, "html.parser")
    # Retrieve all the elements that contains the links to each of Mar's hemispheres and save to a list
    hemispheres = hs_soup.body.find_all("div", class_ = "description")
    # Create a list that will hold the titles and urls of the different Mar's hemispheres
    hs_data = []
    # Iterate through each element and save the picture title and urls to a dictionary
    for hemisphere in hemispheres:
        try:
            # Create dictionary that will hold the image titles and urls
            hs_dict = {}
            # Save the image's title to a variable
            hs_title = hemisphere.find("h3").text
            sleep(2)
            # Click on the link to the image url
            browser.links.find_by_partial_text(hs_title).click()
            sleep(2)
            # HTML object
            html = browser.html
            # Parse HTML with Beautiful Soup
            link_soup = BeautifulSoup(html, "html.parser")
            # Save the image url to a variable
            hs_image = link_soup.find("img", class_ = "wide-image")["src"]
            img_url = url_4 + hs_image
            # Save the title and image url to the dictionary
            hs_dict = {
                "title" : hs_title, 
                "img_url" : img_url
            }
            # Append the dictionary information to the Hemisphere's Data list
            hs_data.append(hs_dict)
            # Direct the browser to go back to the previous page
            browser.back()
        except:
            print("Ooops something happened!")
    # Display the list containing the Hemisphere data
    print(hs_data)
    # Quit the browser
    browser.quit()

    # Store all the Mars data to a dictionary
    mission_mars_data = {
            "news_title" : news_title,
            "news_paragraph" : news_paragraph,
            "featured_image_url" : featured_image_url,
            "html_table" : facts_table_html,
            "hs_data" : hs_data
    }
    # Display the dictionary containing the Mars data
    print(mission_mars_data)

    return mission_mars_data
