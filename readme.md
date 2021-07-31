


# Readme

### (a) How you have implemented the scraper, what challenges you faced and how did you solve them?
I used selenium web driver to load the pages. then I extract the required data by using their respective classes. I used automated click functions of selenium to load the next pages once finishing extracting data from the current page.

I did not face any problems while making scrapping script but Walmart was able to detect automation most of the times. because of this python script will stop working in the middle of the scraping sometimes. 


### (b) What else you could do to improve your scraper?

1. Most of the time Walmart is able to detect selenium, so it asks the user to verify his human identity. because of this script will break in the middle. the script can be made better to evade this automation detection by Walmart. 

2. As our purpose is to scrap only text from the website, the loading of the images can be disabled to make the script faster.

3. look for the possibility of parallelization.

4. Use Walmart API.

### (c) How would you design it to make it work on other retailers as well?
Most of the script will work for the other retailers as well except the parts where the name of element classes differs from those of Walmart. Change the element id and Class names and the script should work well for other retailers as well. 