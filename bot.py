#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import os
import sys

class PlayOKSeleniumBot:
    def __init__(self):
        self.base_url = "https://www.playok.com"
        self.username = os.environ.get('PLAYOK_USERNAME', 'bot1024')
        self.password = os.environ.get('PLAYOK_PASSWORD', 'bot123')
        self.driver = None
        self.logged_in = False
        self.session_start_time = time.time()
        
    def setup_driver(self):
        """设置 Chrome 无头浏览器"""
        print("🚀 初始化 Chrome 无头浏览器...")
        
        chrome_options = Options()
        
        # 无头模式配置
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 反检测配置
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 用户代理
        user_agents = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        ]
        chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # 执行脚本隐藏 webdriver 属性
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": random.choice(user_agents)
            })
            
            print("✅ 浏览器初始化成功")
            return True
            
        except Exception as e:
            print(f"❌ 浏览器初始化失败: {e}")
            return False
    
    def random_delay(self, min_seconds=2, max_seconds=5):
        """随机延迟"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def wait_for_element(self, by, value, timeout=10):
        """等待元素出现"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"❌ 等待元素超时: {by}={value}")
            return None
    
    def login_to_gomoku(self):
        """登录到五子棋游戏"""
        print("🎮 正在访问五子棋页面...")
        
        try:
            self.driver.get(f"{self.base_url}/zh/gomoku/")
            self.random_delay(3, 5)