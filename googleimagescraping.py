#pip install PILLOW
#pip install selenium
#install chrome driver from web

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "/Users/jihyunpark/chromedriver"

wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.google.com/search?q=%EC%8B%9D%ED%8C%90+%EC%8B%9D%EB%8B%A8&tbm=isch&source=hp&biw=714&bih=788&ei=KzYoY9z5BvGK2roPgrap8AQ&iflsig=AJiK0e8AAAAAYyhEO_J7M7Pl5b4vXYNe7DLgie5U0I2c&ved=0ahUKEwicu62kxaD6AhVxhVYBHQJbCk4Q4dUDCAc&uact=5&oq=%EC%8B%9D%ED%8C%90+%EC%8B%9D%EB%8B%A8&gs_lcp=CgNpbWcQAzIECAAQGDoICAAQgAQQsQM6BQgAEIAEOgsIABCABBCxAxCDAToECAAQAzoICAAQsQMQgwFQ3gNY7zJgyTNoBXAAeACAAbwBiAHcDpIBBDAuMTGYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABAA&sclient=img"
    #url = "&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq=cats&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 6)

for i, url in enumerate(urls):
	download_image("/Users/jihyunpark/Documents/scrapetest/", url, str(i) + ".jpg")

wd.quit()