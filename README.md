# Newspaper Scraper
[![License: MIT](https://img.shields.io/github/license/Electronica-dev/Newspaper-scraper)](https://opensource.org/licenses/MIT)
<br/>This is a python project that enables you to scrape newspapers from [Prajavani](http://epaper.prajavani.net) and [Karavali Munjavu](http://www.karavalimunjavu.com/). It supports Chromium based Edge and Chrome.
This project has multiple modules written in Python which can serve different purposes.

- [Setup mail address and application password (Gmail-only)](#setup-mail-address-and-application-password-gmail-only)
- [Setup (Prajavani)](#setup-prajavani)
   * [Requirements](#requirements)
     + [Webdriver Installation](#webdriver-installation)
   * [Usage](#usage)
- [Setup (Karavali Munjavu)](#setup-karavali-munjavu)
   * [Requirements](#requirements-1)
   * [Usage](#usage-1)
- [GUI](#using-the-gui)
   * [Requirements](#requirements-1)
     * [Usage](#usage-2)
## Setup mail address and application password (Gmail-only)
1. The first step is to go to `https://myaccount.google.com/security` and check if you have 2-Step Verification for your google account enabled. If not, then go ahead and enable it.
2. Then click on App passwords, sign in to your Google account, and in the **Select App** dropdown, select __Other *(Custom Name)*__, and give it a name (e.g. paper-scraper).
3. Click on Generate.
4. You will get your 12-digit application password.<br/><br/>![Creating-app-password](../assets/newspaper-scraper/paper-scraper.gif)<br/><br/>
5. If you are the only user of your computer, you may add your mail address and the application password directly to `email = environ.get('EMAIL_ADDRESS')` as `email = 'your-email'` and `pwd = environ.get('EMAIL_PASSWORD')` as `pwd = '12-digit-password'` in the `send_email.py` module.
6. If you have multiple users who have access to your computer, and you are the administrator, you can store your mail address and application password as [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). If you choose to do so, be sure to specify your mail address variable name as `EMAIL_ADDRESS` and your application password variable name as `EMAIL_PASSWORD`.
## Setup (Prajavani) 
### Requirements
1. [Python interpreter](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html) (The latest version at the time of writing this is 3.8.3. But the installation instructions are the same.)
2. [Chromium based Edge browser](https://www.microsoft.com/en-us/edge) or [Google Chrome](https://www.google.com/intl/en_in/chrome/)
3. [WebDriver for Edge](https://msedgewebdriverstorage.z22.web.core.windows.net/) or [WebDriver for Chrome](https://chromedriver.storage.googleapis.com/index.html)
4. Additional modules required
   1. selenium
   2. requests
   3. PyPDF2
   4. natsort
   
   To install these, run `pip install -r requirements-pv.txt` in the command prompt.
#### Webdriver Installation
1. Download the WebDriver from the link. The version you would want to download is the version of your Edge browser. To check your version, type `edge://version/` or `chrome://version/` in the address bar.
<br/><br/>![About version](../assets/newspaper-scraper/edge-webdriver-download-delay-10ms.gif)
![Download dialog](../assets/newspaper-scraper/download-dialog.png)
2. In the zip, there will be a `msedgedriver.exe` file.`chromedriver.exe` for Chrome.<br/><br/>![zip folder](../assets/newspaper-scraper/zip-folder.png)
3. Extract this to the folder of your choice.
4. Open `prajavani-dl.py` with a text editor and replace `path/to/webdriver` with the path `msedgedriver.exe` or `chromewebdriver.exe` is located in. You actually need only one for your preferred browser. It doesn't matter if you leave the other one as `path/to/webdriver` itself as long as you choose your browser.<br/><br/>![Webdriver-path-change](../assets/newspaper-scraper/change-webdriver-location-small.gif) 
### Usage
`py prajavani-dl.py [browser] [directory-location] [file-size] [send-mail] [recipient-email-address 1] [recipient-email-address 2] [recipient-email-address n]`
<br/>Example: `py prajavani-dl.py c desktop 8 1 abc@mail.com def@mail.com`<br/>
<br/>**Note:** You will need to update the webdriver as and when you update Edge or Chrome, as it is not forward compatible.
<br/>**Note 2:** For the directory location; desktop, documents and downloads are the only options available. If you wish to store it in any other location, you will have to explicitly mention the whole path.
<br/>**Note 3:** To give the browser choice, either type c for chrome or e for edge.
<br/>File size is in megabytes, if you give it as 8, the program will automatically split the individual file(s) to 8 mb. If you wish to have a single file, then give it a value of 0.
<br/>If you don't want to send a mail, you may change the 1 to a 0 and not provide any mail.
## Setup (Karavali Munjavu)
### Requirements
1. [Python interpreter](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html) (The latest version at the time of writing this is 3.8.3. But the installation instructions are the same.)
2. [Chromium based Edge browser](https://www.microsoft.com/en-us/edge) or [Google Chrome](https://www.google.com/intl/en_in/chrome/)
3. Additional modules required
   1. BeautifulSoup4
   2. requests
   3. lxml
   4. img2pdf
   5. PyPDF2
   
   To install these, run `pip install -r requirements-km.txt` in the command prompt.
### Usage
Open command prompt and enter:<br/>`py karavali-dl-edge.py [directory-location] [send-mail] [recipient-email-address 1] [recipient-email-address 2] [recipient-email-address n]`
## Using the GUI
If you want a more intuitive way to scrape newspapers using an application, then you can make use of the gui program.

### Requirements
1. [Python interpreter](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html) (The latest version at the time of writing this is 3.8.3. But the installation instructions are the same.)
2. Additional modules required are there in the file requirements.txt. To install these, run `pip install -r requirements.txt` in the command prompt.
3. [Web Driver (Chrome or Edge)](#webdriver-installation)
3. You also need to follow [these steps](#setup-mail-address-and-application-password-gmail-only) if sending an email is a priority.

#### Usage
After you have the above prerequisites, you can run the main program by opening cmd in the folder in which you have all your files in and typing: `py paper_scraper.py`. Or you can make an exe by following [this tutorial](https://www.youtube.com/watch?v=UZX5kH72Yx4).
