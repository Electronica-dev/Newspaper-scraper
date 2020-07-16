# Prajavani Newspaper Scraper
This is a python project which enables a user to scrape newspapers from [Prajavani](http://epaper.prajavani.net). It currently supports only Chromium based Edge browser.
This project has multiple modules written in Python which can be used for different purposes.
## Setup
### Requirements
1. [Python interpreter](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html) (The latest one at the time of writing this is 3.8.3. But the installation instructions are the same.)
2. [Chromium based Edge browser](https://www.microsoft.com/en-us/edge)
3. [WebDriver for Edge](https://msedgewebdriverstorage.z22.web.core.windows.net/)
4. Additional modules required
   1. selenium
   2. requests
   3. PyPDF2
   4. natsort
   
   To install these, run `pip install [module-name]` in the command prompt.
#### Webdriver Installation
1. Download the WebDriver from the link. The version you would want to download is the version of your Edge browser. To check your version, type `edge://version/` in the address bar.
<br/><br/>![About version](../assets/newspaper-scraper/edge-webdriver-download-delay-10ms.gif)
![Download dialog](../assets/newspaper-scraper/download-dialog.png)
2. In the zip, there will be a `msedgedriver.exe` file.<br/><br/>![zip folder](../assets/newspaper-scraper/zip-folder.png)
3. Extract this file to the `Scripts` folder of your Python installation. Usually, this would be located in `%USERPROFILE%\AppData\Local\Programs\Python\Python38-32\Scripts`.
<br/><br/>![Scripts folder](../assets/newspaper-scraper/script-folder.png)
4. After this, go to your selenium package, usually located in `%USERPROFILE%\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\selenium`. Then go to `webdriver` -> `edge` -> `webdriver.py` and open this file in an editor.<br/><br/>![Selenium Webdriver.py location](../assets/newspaper-scraper/selenium-webdriver-location.gif)
5. After opening it, change the `executable_path` from `MicrosoftWebDriver.exe` to `msedgedriver.exe` and save it.<br/><br/>![Change webdriver executable](../assets/newspaper-scraper/change-webdriver.gif)
### You're all set now!
