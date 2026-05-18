# 🖼️ pinterest_image_downloader

> Scrape and download images from Pinterest

A command-line tool for searching and downloading images from Pinterest in bulk using Selenium and BeautifulSoup.

## ✨ Features

- **Keyword search** — Search for images by keyword and download all results
- **Direct link scraping** — Paste a Pinterest board/collection URL to download all pins
- **Bulk download** — Download hundreds of images at once
- **Progress tracking** — Visual progress bar during download
- **Auto-organization** — Images saved in `images/` folder
- **Selenium automation** — Uses Chrome browser for JavaScript-heavy Pinterest pages

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Chrome/Chromium browser
- 500MB+ free disk space (depending on number of images)

### Installation

```bash
git clone https://github.com/w1cee/pinterest_image_downloader.git
cd pinterest_image_downloader
pip install -r requirements.txt
```

### Setup

The tool automatically downloads ChromeDriver via `webdriver_manager`, so no manual setup needed.

### Run the Tool

```bash
python main.py
```

## 💻 How to Use

### Option 1: Keyword Search

```
$ python main.py

If you want to use a ready link write 1, if you want to use keyword search write 2 (1/2): 2
What kind of images do you need to download?: interior design

✅ Images search started
Collecting urls: ✅
✅ Total media found: 152
✅ Image download started
Downloading: |████████████████████████| 152/152
```

### Option 2: Direct Link (Board/Collection)

```
$ python main.py

If you want to use a ready link write 1, if you want to use keyword search write 2 (1/2): 1
Enter url: https://pinterest.com/username/board-name/

✅ Images search started
Collecting urls: ✅
✅ Total media found: 89
✅ Image download started
Downloading: |████████████████████████| 89/89
```

## 🛠️ Tech Stack

- **Language**: Python 3.7+
- **Browser Automation**: Selenium with Chrome WebDriver
- **Web Scraping**: BeautifulSoup 4
- **HTTP Requests**: requests library
- **Progress UI**: yaspin (spinner), progress (progress bar)
- **WebDriver Management**: webdriver_manager (auto-downloads ChromeDriver)

## 📚 Code Structure

### Main Flow

```python
def main():
    finding_images()   # Search and collect URLs
    download_images()  # Download all images
    driver.close()
    driver.quit()
```

### 1. Finding Images (`finding_images()`)

```python
def finding_images():
    global pins_list
    
    # User chooses: keyword search or direct link
    choice = input('1 for link, 2 for keyword search: ')
    
    if choice == '1':
        url = input('Enter url: ')  # Direct Pinterest URL
    elif choice == '2':
        var = input('What kind of images?: ')
        url = f"https://pinterest.com/search/pins/?q={var}"  # Search URL
    
    # Launch Chrome with Selenium
    driver.get(url)
    
    # Parse page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all pin links
    for link in soup.find_all('a', href=True):
        if link.get('href').startswith('/pin/'):
            pin_url = f"https://www.pinterest.com{link.get('href')}"
            pins_list.append(pin_url)
```

**Key Points:**
- Uses Selenium to handle JavaScript (Pinterest loads pins dynamically)
- Collects all `/pin/` URLs from the page
- Shows spinner while collecting URLs

### 2. Downloading Images (`download_images()`)

```python
def download_images():
    # Clean previous downloads
    try:
        shutil.rmtree('images/')
    except Exception:
        pass
    
    # Create images folder
    os.makedirs(os.path.dirname('images/'), exist_ok=True)
    
    # Progress bar
    bar = ChargingBar('Downloading', max=len(pins_list))
    
    counter = 0
    for url in pins_list:
        counter += 1
        driver.get(url)  # Load pin page
        
        # Find image on pin page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        image = soup.find('img')
        image_link = image.get('src')
        
        # Download image
        filename = f'media_{counter}'
        img_data = requests.get(image_link).content
        
        # Save to disk
        with open(f'images/{filename}.jpg', 'wb') as handler:
            handler.write(img_data)
        
        bar.next()  # Update progress
```

**Key Points:**
- Removes old `images/` folder
- Creates new `images/` folder
- Downloads each pin individually
- Saves with numeric naming: `media_1.jpg`, `media_2.jpg`, etc.
- Shows progress bar during download

## 🔌 Pinterest Structure

### Search URL Format
```
https://pinterest.com/search/pins/?q=KEYWORD
```

### Pin URL Structure
```
https://www.pinterest.com/pin/PIN_ID/
```

### Pin HTML Structure
```html
<!-- Pin link in search results -->
<a href="/pin/123456789/">...</a>

<!-- Image on pin page -->
<img src="https://i.pinimg.com/...jpg" />
```

## 📁 File Structure

```
pinterest_image_downloader/
├── main.py              # Main script
├── chromedriver.exe     # Chrome WebDriver (Windows)
├── images/              # Downloaded images (auto-created)
│   ├── media_1.jpg
│   ├── media_2.jpg
│   └── media_152.jpg
├── requirements         # Dependencies
├── LICENSE
└── README.md
```

## 📊 Output

All images are saved in the `images/` folder:

```
images/
├── media_1.jpg
├── media_2.jpg
├── media_3.jpg
└── ... (up to number of pins found)
```

Each image is numbered sequentially: `media_1.jpg`, `media_2.jpg`, etc.

## 🐛 Troubleshooting

### "Chrome not found" error
```
WebDriverException: chrome binary not found
```
- Install Chrome/Chromium browser
- `webdriver_manager` will auto-download ChromeDriver

### "Images folder permission denied"
```
PermissionError: [Errno 13] Permission denied: 'images/'
```
- Close any file explorer windows with `images/` folder open
- Try deleting `images/` folder manually
- Ensure write permissions on directory

### No images found
- Try with a different search term
- Wait longer (JavaScript rendering takes time)
- Check if Pinterest URL is public
- Pinterest may have blocked automated access

### Slow download speeds
- Check internet connection
- Close other browsers/apps
- Pinterest rate limiting may apply
- Consider adding delays between requests

### BeautifulSoup parsing issues
- Pinterest HTML structure may have changed
- May need to update CSS selectors
- Check browser DevTools for current HTML structure

## 📝 Requirements File

```
beautifulsoup4
yaspin
progress
selenium
webdriver_manager
requests
```

## ⚠️ Important Notes

- **Terms of Service**: Check Pinterest's ToS regarding scraping
- **Rate Limiting**: Large downloads may trigger rate limiting
- **Copyright**: Downloaded images are copyrighted; use for personal use only
- **Headless Mode**: Browser window opens during scraping (normal)
- **Speed**: Downloading 100+ images can take several minutes

## 🔄 Workflow

```
User runs: python main.py
        ↓
Choose: Link (1) or Keyword (2)
        ↓
If keyword search:
  Construct search URL with keyword
        ↓
Launch Chrome with Selenium
        ↓
Load Pinterest page
        ↓
Parse HTML with BeautifulSoup
        ↓
Find all pin links (/pin/...)
        ↓
Collect URLs in pins_list
        ↓
Close/clear old images/
        ↓
Create new images/ folder
        ↓
For each pin URL:
  Load pin page
  Extract image src
  Download image
  Save as media_N.jpg
  Update progress bar
        ↓
Close Chrome
        ↓
All images in images/ folder
```

## 📄 License

MIT License - See LICENSE file

## 👨‍💻 Author

**w1cee** — Backend Developer | Systems Builder  
💬 [GitHub](https://github.com/w1cee)

---

**Building things that work while I sleep** 🎨
