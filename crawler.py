from time import sleep
from browser import Browser
from utils import text_to_num, export_to_csv, retry
import urllib.parse

class InstagramCrawler:
    URL = "https://www.instagram.com"

    def __init__(self, has_screen=False):
        self.browser = Browser(has_screen)
        self.page_height = 0
    
    def login(self):
        browser = self.browser
        url = "%s/accounts/login/" % (InstagramCrawler.URL)
        browser.get(url)
        username_input = browser.find_one('input[name="username"]')
        username_input.send_keys("*******")
        sleep(1)
        password_input = browser.find_one('input[name="password"]')
        password_input.send_keys("*****")
        sleep(1)

        login_btn = browser.find_one(".L3NKy")
        login_btn.click()
        
        sleep(3)
    
    def search_post(self, keyword, num=1):
        self.login()
        browser = self.browser
        url = "%s/explore/tags/%s/" % (InstagramCrawler.URL, urllib.parse.quote_plus(keyword))
        browser.get(url)
        sleep(5)
        first_post = "div.v1Nh3.kIKUG._bz0w"
        username_selector = "a.sqdOP.yWX7d._8A5w5.ZIAjV"
        arrow_selector = "div.l8mY4.feth3 > .wpO6b "
        result = set()
        self._click_delay(first_post)
        result.add(self._get_username(username_selector))

        if num == 1:
            return result
        
        for _ in range(num):
            if not self._is_element_exist(arrow_selector):
                break
            self._click_delay(arrow_selector)
            result.add(self._get_username(username_selector))
        
        return result

    def _get_username(self, selector):
        try:
            user_name = self.browser.find_one(selector).get_attribute("innerHTML")
            return user_name
        except:
            return None

    def _is_element_exist(self, selector):
        try:
            return self.browser.find_one(selector)
        except:
            return None

    def _click_delay(self, selector):
        self.browser.find_one(selector).click()
        sleep(2)
    
    def get_followers(self, accounts):
        @retry()
        def get_statistics():
            try:
                stats = [ele.text for ele in self.browser.find(".g47SY")]
                posts, follower, following = stats
                return {
                    "posts": posts,
                    "followers": text_to_num(follower),
                    "following": text_to_num(following),
                }
            except Exception as e:
                print(e)
                return None
        result_dict = {}
        try:
            for account in accounts:
                self._direct_to_user_profile(account)
                result_dict[account] = get_statistics()
            return result_dict
        except:
            return result_dict
    
    def _get_statistics(self):
        try:
            stats = [ele.text for ele in self.browser.find(".g47SY")]
            posts, follower, following = stats
            return {
                "posts": posts,
                "followers": text_to_num(follower),
                "following": text_to_num(following),
            }
        except Exception as e:
            print(e)
            return None
    
    def _direct_to_user_profile(self, account):
        url = "%s/%s/" % (InstagramCrawler.URL, account)
        self.browser.get(url)
        sleep(1)

