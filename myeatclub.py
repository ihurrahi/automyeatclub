import argparse
import simplejson
import sys
import time
import re
from selenium import webdriver

p = argparse.ArgumentParser()
p.add_argument('--avoid-tag', default=[], action='append')
p.add_argument('--require-tag', default=[], action='append')
p.add_argument('--avoid-restaurant', default=[], action='append')
p.add_argument('--place-order', action='store_true')
p.add_argument('--preserve-browser', action='store_true')
p.add_argument('--menu-number', default=1)
p.add_argument('--cookies-path', default='myeatclub_cookies')
cfg = p.parse_args(sys.argv[1:])

# Load cookies
print "Loading cookies..."
with open(cfg.cookies_path) as c:
  cookies = simplejson.load(c)
  phantomjs_cookies = []
  for key, val in cookies.items():
    phantomjs_cookies.append({"name": key, "value": val, "domain": "eatclub.com"})

browser = webdriver.Chrome()
browser.get('https://eatclub.com')
for cookie in phantomjs_cookies:
  browser.add_cookie(cookie)

# History
browser.get('https://www.eatclub.com/orders/history/')
history_re = r'<td class="item"><a href="(.*)">'
history = set()
for match in re.findall(history_re, browser.page_source):
  history.add(match.strip('/'))

# Current menu
print "Retrieving menu..."
browser.get('https://eatclub.com/menu/' + str(cfg.menu_number))
browser.implicitly_wait(1)
time.sleep(1)

# Parse menu
print "Processing menu..."
menu = []
elements = browser.find_elements_by_class_name('mi-infobox')
for element in elements:
  item = element.find_element_by_class_name('mi-item-name-link')
  link = item.get_attribute('href')
  link = link.replace('https://eatclub.com', '', 1)
  link = link[:link.find('?')].strip('/')
  name = item.text
  rest = element.find_element_by_class_name('mi-restaurant-name')
  restaurant = rest.text
  ratings = element.find_elements_by_class_name('mi-i-stars-text')
  rating = ratings[-1].text
  tag_holder = element.find_element_by_class_name('mi-dish-tags')
  links = tag_holder.find_elements_by_css_selector('a')
  tags = map(lambda x: x.get_attribute('data-content'), links)
  add = element.find_element_by_class_name('mi-add-btn')
  if link not in history:
    menu.append((rating, name, restaurant, tags, add))

def filter_menu(menu, num_choices, cfg):
  menu = filter(lambda x: len(set(cfg.avoid_tag).intersection(set(x[3]))) == 0, menu)
  if cfg.require_tag:
    menu = filter(lambda x: all(t in x[3] for t in cfg.require_tag), menu)
  menu = filter(lambda x: x[2] not in cfg.avoid_restaurant, menu)
  return sorted(menu, key=lambda x: x[0], reverse=True)[:num_choices]

num_choices = 5
result = "Top %d choices:\n" % num_choices
new_menu = filter_menu(menu, num_choices, cfg)
for index, menu_item in enumerate(new_menu):
  if cfg.place_order and index == 0:
    print "Ordering " + menu_item[1]
    menu_item[4].click()
    time.sleep(5)
    element = browser.find_element_by_class_name('checkout-btn')
    element.click()
  result += str(index) + ". Rating: " + menu_item[0] + " " + menu_item[1] + " by " + menu_item[2] + " (" + ", ".join(menu_item[3]) + ")\n"
print result

if not cfg.preserve_browser:
  browser.quit()
