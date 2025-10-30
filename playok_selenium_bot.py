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
    
    def take_screenshot(self, name):
        """截图用于调试"""
        try:
            self.driver.save_screenshot(f"{name}.png")
            print(f"📸 截图保存: {name}.png")
        except Exception as e:
            print(f"截图失败: {e}")
    
    def login_to_gomoku(self):
        """登录到五子棋游戏"""
        print("🎮 正在访问五子棋页面...")
        
        try:
            self.driver.get(f"{self.base_url}/zh/gomoku/")
            self.take_screenshot("01_initial_page")
            self.random_delay(3, 5)
            
            # 查找并点击登录按钮
            print("🔍 寻找登录按钮...")
            
            # 尝试多种选择器找到登录按钮
            login_selectors = [
                "//button[contains(text(), '登入')]",
                "//button[contains(text(), '登录')]",
                "//button[contains(@onclick, 'login')]",
                "//button[contains(@class, 'login')]"
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    login_button = self.driver.find_element(By.XPATH, selector)
                    if login_button:
                        break
                except NoSuchElementException:
                    continue
            
            if login_button:
                login_button.click()
                print("✅ 点击登录按钮")
                self.take_screenshot("02_after_login_click")
                self.random_delay(2, 3)
                
                # 等待并填写登录表单
                print("🔍 等待登录表单...")
                username_field = self.wait_for_element(By.NAME, "username")
                password_field = self.wait_for_element(By.NAME, "pw")
                
                if username_field and password_field:
                    # 输入凭据
                    print("⌨️ 输入用户名...")
                    username_field.clear()
                    username_field.send_keys(self.username)
                    self.random_delay(1, 2)
                    
                    print("⌨️ 输入密码...")
                    password_field.clear()
                    password_field.send_keys(self.password)
                    self.random_delay(1, 2)
                    
                    # 提交表单
                    print("📤 提交登录表单...")
                    submit_selectors = [
                        "//button[contains(text(), '登入')]",
                        "//button[contains(text(), '登录')]",
                        "//button[@type='submit']"
                    ]
                    
                    submit_button = None
                    for selector in submit_selectors:
                        try:
                            submit_button = self.driver.find_element(By.XPATH, selector)
                            if submit_button:
                                break
                        except NoSuchElementException:
                            continue
                    
                    if submit_button:
                        submit_button.click()
                        self.take_screenshot("03_after_submit")
                        
                        # 等待登录完成
                        self.random_delay(5, 8)
                        self.take_screenshot("04_after_login")
                        
                        # 检查登录状态
                        if self.check_login_success():
                            print("✅ 登录成功！")
                            self.logged_in = True
                            return True
                        else:
                            print("❌ 登录状态检查失败")
                            return False
                    else:
                        print("❌ 未找到提交按钮")
                        return False
                else:
                    print("❌ 未找到用户名或密码输入框")
                    return False
            else:
                print("❌ 未找到登录按钮")
                # 可能已经自动展开表单，尝试直接查找表单
                username_field = self.wait_for_element(By.NAME, "username")
                if username_field:
                    print("🔍 直接找到登录表单，尝试登录...")
                    return self.direct_login()
                return False
                
        except Exception as e:
            print(f"❌ 登录过程中发生错误: {e}")
            self.take_screenshot("login_error")
            return False
    
    def direct_login(self):
        """直接登录（如果表单已经可见）"""
        try:
            username_field = self.wait_for_element(By.NAME, "username")
            password_field = self.wait_for_element(By.NAME, "pw")
            
            if username_field and password_field:
                username_field.clear()
                username_field.send_keys(self.username)
                self.random_delay(1, 2)
                
                password_field.clear()
                password_field.send_keys(self.password)
                self.random_delay(1, 2)
                
                # 查找提交按钮
                submit_selectors = [
                    "//button[contains(text(), '登入')]",
                    "//button[contains(text(), '登录')]",
                    "//button[@type='submit']",
                    "//input[@type='submit']"
                ]
                
                for selector in submit_selectors:
                    try:
                        submit_button = self.driver.find_element(By.XPATH, selector)
                        submit_button.click()
                        self.random_delay(5, 8)
                        
                        if self.check_login_success():
                            print("✅ 直接登录成功！")
                            self.logged_in = True
                            return True
                    except NoSuchElementException:
                        continue
                
                print("❌ 直接登录失败")
                return False
            return False
        except Exception as e:
            print(f"❌ 直接登录错误: {e}")
            return False
    
    def check_login_success(self):
        """检查登录是否成功"""
        try:
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url
            
            print(f"🔍 检查登录状态 - URL: {current_url}")
            
            # 成功标识
            success_indicators = [
                'logout', 'log out', '退出', '登出', 
                self.username.lower(), '我的账户', 'my account'
            ]
            
            for indicator in success_indicators:
                if indicator in page_source:
                    print(f"✅ 找到成功标识: {indicator}")
                    return True
            
            # 检查是否有登录表单（失败标识）
            failure_indicators = ['username', 'password', '登录', '登入']
            if all(indicator in page_source for indicator in failure_indicators[:2]):
                print("❌ 仍然显示登录表单")
                return False
            
            # URL 检查
            if 'login' not in current_url and 'signin' not in current_url:
                print("✅ URL 表明可能已登录")
                return True
                
            return False
            
        except Exception as e:
            print(f"❌ 检查登录状态时出错: {e}")
            return False
    
    def maintain_active_session(self, max_minutes=350):
        """保持活跃会话"""
        if not self.logged_in:
            print("❌ 请先登录")
            return False
        
        print(f"🕒 开始保持活跃会话，最长 {max_minutes} 分钟")
        
        start_time = time.time()
        max_duration = max_minutes * 60
        activity_count = 0
        last_activity_time = time.time()
        
        while time.time() - start_time < max_duration:
            try:
                activity_count += 1
                elapsed_minutes = (time.time() - start_time) / 60
                
                print(f"\n--- 活动轮次 #{activity_count} (已运行 {elapsed_minutes:.1f} 分钟) ---")
                
                # 随机选择活动类型
                activity_type = random.choice(['refresh', 'navigate', 'check_status'])
                
                if activity_type == 'refresh':
                    success = self.refresh_lobby()
                elif activity_type == 'navigate':
                    success = self.navigate_around()
                else:
                    success = self.check_online_status()
                
                if not success:
                    print("❌ 活动失败，尝试重新登录...")
                    if self.recover_session():
                        continue
                    else:
                        print("❌ 会话恢复失败")
                        break
                
                # 更新最后活动时间
                last_activity_time = time.time()
                
                # 随机等待时间（2-5分钟）
                wait_time = random.randint(120, 300)
                print(f"⏳ 等待 {wait_time} 秒后进行下一次活动...")
                
                # 在等待期间定期检查状态
                wait_start = time.time()
                while time.time() - wait_start < wait_time:
                    # 每30秒检查一次会话状态
                    if time.time() - last_activity_time > 600:  # 10分钟无活动
                        print("🔄 长时间无活动，执行状态检查...")
                        if not self.check_online_status():
                            print("❌ 状态检查失败，尝试恢复...")
                            self.recover_session()
                        last_activity_time = time.time()
                    
                    time.sleep(30)  # 30秒检查一次
                
            except Exception as e:
                print(f"❌ 活动过程中出错: {e}")
                self.take_screenshot(f"error_activity_{activity_count}")
                time.sleep(60)  # 出错后等待1分钟
        
        print(f"✅ 会话保持完成，共进行 {activity_count} 次活动")
        return True
    
    def refresh_lobby(self):
        """刷新大厅"""
        print("🔄 刷新游戏大厅...")
        try:
            self.driver.refresh()
            self.random_delay(3, 5)
            self.take_screenshot(f"refresh_{int(time.time())}")
            
            if self.check_login_success():
                print("✅ 刷新成功，登录状态正常")
                return True
            else:
                print("❌ 刷新后登录状态异常")
                return False
        except Exception as e:
            print(f"❌ 刷新失败: {e}")
            return False
    
    def navigate_around(self):
        """在网站内导航"""
        pages = [
            f"{self.base_url}/zh/gomoku/",
            f"{self.base_url}/zh/",
            f"{self.base_url}/en/gomoku/",
        ]
        
        target_page = random.choice(pages)
        print(f"🧭 导航到: {target_page}")
        
        try:
            self.driver.get(target_page)
            self.random_delay(3, 5)
            
            if self.check_login_success():
                print("✅ 导航成功，登录状态正常")
                return True
            else:
                print("❌ 导航后登录状态异常")
                return False
        except Exception as e:
            print(f"❌ 导航失败: {e}")
            return False
    
    def check_online_status(self):
        """检查在线状态"""
        print("📊 检查在线状态...")
        try:
            # 获取页面内容检查用户名是否显示
            page_source = self.driver.page_source
            
            if self.username.lower() in page_source.lower():
                print("✅ 用户名在页面中可见")
                return True
            else:
                print("⚠️ 用户名未在页面中找到（可能正常）")
                return self.check_login_success()  # 回退到基础登录检查
        except Exception as e:
            print(f"❌ 状态检查失败: {e}")
            return False
    
    def recover_session(self):
        """恢复会话（重新登录）"""
        print("🔄 尝试恢复会话...")
        self.take_screenshot("before_recovery")
        
        # 先回到登录页面
        try:
            self.driver.get(f"{self.base_url}/zh/gomoku/")
            self.random_delay(3, 5)
        except Exception as e:
            print(f"❌ 恢复页面访问失败: {e}")
        
        # 重新登录
        return self.login_to_gomoku()
    
    def run(self, max_minutes=350):
        """运行主程序"""
        print("=" * 60)
        print("🎮 PlayOK Selenium 机器人启动")
        print(f"📝 账号: {self.username}")
        print(f"⏰ 计划运行: {max_minutes} 分钟")
        print("=" * 60)
        
        try:
            # 1. 初始化浏览器
            if not self.setup_driver():
                return False
            
            # 2. 登录
            if not self.login_to_gomoku():
                print("❌ 登录失败，程序终止")
                return False
            
            # 3. 保持活跃会话
            self.maintain_active_session(max_minutes)
            
            print("✅ 程序执行完成")
            return True
            
        except Exception as e:
            print(f"❌ 程序执行失败: {e}")
            return False
            
        finally:
            # 4. 清理资源
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        if self.driver:
            print("🧹 关闭浏览器...")
            try:
                self.driver.quit()
                print("✅ 浏览器已关闭")
            except Exception as e:
                print(f"❌ 关闭浏览器时出错: {e}")

if __name__ == "__main__":
    # 在 GitHub Actions 中，单次运行最长为 6 小时（360分钟）
    # 我们设置为 350 分钟以留出缓冲时间
    bot = PlayOKSeleniumBot()
    success = bot.run(max_minutes=350)
    
    sys.exit(0 if success else 1)