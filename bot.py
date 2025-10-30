#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
import sys

class PlayOKSeleniumBot:
    def __init__(self):
        self.base_url = "https://www.playok.com"
        # 硬编码账号密码
        self.username = "bot1024"
        self.password = "bot123"
        self.driver = None
        self.logged_in = False
        
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
            # 使用 webdriver-manager 自动管理 ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 执行脚本隐藏 webdriver 属性
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
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
    
    def wait_for_element_clickable(self, by, value, timeout=10):
        """等待元素可点击"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            print(f"❌ 等待元素可点击超时: {by}={value}")
            return None
    
    def execute_js_cookies(self):
        """执行JS文件中的Cookie设置逻辑"""
        print("🍪 执行JS Cookie设置...")
        
        # 执行 inline_js_2.js 中的引用跟踪代码
        ref_js = """
        var sh = location.protocol + '//' + location.hostname;
        var rv = (document.referrer.indexOf(sh) == 0 ? "-" : document.referrer);
        document.cookie = 'ref=' + escape(rv) + ';path=/;max-age=300';
        """
        self.driver.execute_script(ref_js)
        
        # 设置游戏相关的Cookie（模仿 inline_js_1.js）
        kbexp_js = "document.cookie = 'kbexp=0;path=/;'"
        self.driver.execute_script(kbexp_js)
        
        print("✅ Cookie设置完成")
    
    def close_popups(self):
        """关闭所有可能的弹窗和广告"""
        print("🎯 尝试关闭弹窗和广告...")
        
        # 尝试关闭常见的广告和Cookie弹窗
        popup_selectors = [
            # Cookie同意弹窗
            "div[class*='qc-cmp'] button",
            "button[class*='accept']",
            "button[class*='agree']",
            # 广告弹窗
            "div[class*='popup'] button[class*='close']",
            "button[class*='close']",
        ]
        
        closed_any = False
        for selector in popup_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        if element.is_displayed():
                            self.driver.execute_script("arguments[0].click();", element)
                            print(f"✅ 关闭弹窗: {selector}")
                            self.random_delay(1, 2)
                            closed_any = True
                    except:
                        continue
            except:
                continue
        
        if not closed_any:
            print("ℹ️ 未找到需要关闭的弹窗")
    
    def click_with_js(self, element):
        """使用JavaScript点击元素，避免被遮挡"""
        try:
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"❌ JavaScript点击失败: {e}")
            return False
    
    def ensure_form_visible(self):
        """确保登录表单可见"""
        print("🔍 确保登录表单可见...")
        
        # 检查表单是否已经可见
        form_selectors = [
            "//form[@name='f']",
            "//form[contains(@action, 'gomoku')]"
        ]
        
        for selector in form_selectors:
            try:
                form = self.driver.find_element(By.XPATH, selector)
                if form.is_displayed():
                    print("✅ 登录表单已可见")
                    return True
            except:
                continue
        
        # 如果表单不可见，尝试点击登录按钮
        print("📝 登录表单不可见，尝试展开...")
        login_selectors = [
            "//button[contains(text(), '登入')]",
            "//button[contains(text(), '登录')]",
        ]
        
        for selector in login_selectors:
            try:
                login_button = self.wait_for_element_clickable(By.XPATH, selector)
                if login_button:
                    self.click_with_js(login_button)
                    print("✅ 点击登录按钮展开表单")
                    self.random_delay(2, 3)
                    
                    # 再次检查表单是否可见
                    for form_selector in form_selectors:
                        try:
                            form = self.driver.find_element(By.XPATH, form_selector)
                            if form.is_displayed():
                                print("✅ 登录表单现在可见")
                                return True
                        except:
                            continue
                    break
            except:
                continue
        
        return False
    
    def login_to_gomoku(self):
        """登录到五子棋游戏"""
        print("🎮 正在访问五子棋页面...")
        
        try:
            # 访问页面
            self.driver.get(f"{self.base_url}/zh/gomoku/")
            self.random_delay(3, 5)
            
            # 执行JS Cookie设置
            self.execute_js_cookies()
            
            # 关闭弹窗
            self.close_popups()
            self.random_delay(2, 3)
            
            # 确保登录表单可见
            if not self.ensure_form_visible():
                print("❌ 无法使登录表单可见")
                return False
            
            # 再次关闭可能新出现的弹窗
            self.close_popups()
            
            # 查找表单字段
            print("🔍 查找登录表单字段...")
            username_field = self.wait_for_element(By.NAME, "username")
            password_field = self.wait_for_element(By.NAME, "pw")
            
            if not username_field or not password_field:
                print("❌ 未找到用户名或密码输入框")
                # 尝试通过ID查找
                username_field = self.wait_for_element(By.ID, "id")
                if not username_field:
                    print("❌ 也未找到ID为'id'的用户名字段")
                    return False
            
            # 输入凭据
            print("⌨️ 输入用户名...")
            username_field.clear()
            username_field.send_keys(self.username)
            self.random_delay(1, 2)
            
            print("⌨️ 输入密码...")
            password_field.clear()
            password_field.send_keys(self.password)
            self.random_delay(1, 2)
            
            # 提交表单 - 尝试多种方式
            print("📤 尝试提交登录表单...")
            
            # 方式1: 通过JavaScript直接提交表单
            form = self.driver.find_element(By.XPATH, "//form[@name='f']")
            if form:
                self.driver.execute_script("arguments[0].submit();", form)
                print("✅ 通过JS提交表单")
            else:
                # 方式2: 点击提交按钮
                submit_selectors = [
                    "//button[contains(text(), '登入')]",
                    "//button[contains(text(), '登录')]",
                    "//button[@type='submit']",
                    "//input[@type='submit']"
                ]
                
                submitted = False
                for selector in submit_selectors:
                    try:
                        submit_button = self.driver.find_element(By.XPATH, selector)
                        if submit_button:
                            self.click_with_js(submit_button)
                            print(f"✅ 点击提交按钮: {selector}")
                            submitted = True
                            break
                    except:
                        continue
                
                if not submitted:
                    print("❌ 未找到提交按钮")
                    return False
            
            # 等待登录完成 - 增加等待时间
            print("⏳ 等待登录处理...")
            self.random_delay(8, 12)  # 延长等待时间
            
            # 检查登录状态
            if self.check_login_success():
                print("✅ 登录成功！")
                self.logged_in = True
                return True
            else:
                print("❌ 登录失败")
                # 保存页面用于调试
                try:
                    page_source = self.driver.page_source
                    with open("debug_login_page.html", "w", encoding="utf-8") as f:
                        f.write(page_source)
                    print("📄 保存页面到 debug_login_page.html")
                except:
                    pass
                return False
                
        except Exception as e:
            print(f"❌ 登录过程中发生错误: {e}")
            return False
    
    def check_login_success(self):
        """检查登录是否成功 - 更严格的检查"""
        try:
            page_source = self.driver.page_source
            current_url = self.driver.current_url
            
            print(f"🔍 详细检查登录状态 - URL: {current_url}")
            
            # 严格的成功标识检查
            success_indicators = [
                'logout', 'log out', '退出', '登出'
            ]
            
            for indicator in success_indicators:
                if indicator.lower() in page_source.lower():
                    print(f"✅ 找到明确成功标识: {indicator}")
                    return True
            
            # 检查用户名是否出现在页面中（非表单字段）
            if f">{self.username}<" in page_source or f'">{self.username}"' in page_source:
                print(f"✅ 用户名 {self.username} 在页面内容中")
                return True
            
            # 检查是否有欢迎消息
            if 'welcome' in page_source.lower() or '欢迎' in page_source:
                print("✅ 找到欢迎消息")
                return True
            
            # 严格的失败标识检查
            failure_indicators = [
                'username', 'password', '登录', '登入', '帳號'
            ]
            
            failure_count = 0
            for indicator in failure_indicators:
                if indicator in page_source.lower():
                    failure_count += 1
            
            if failure_count >= 2:
                print("❌ 页面仍然显示登录表单元素")
                return False
            
            # URL 检查
            if 'login' not in current_url and 'signin' not in current_url:
                print("✅ URL 没有登录相关路径")
                return True
            
            print("❓ 无法确定登录状态")
            return False
            
        except Exception as e:
            print(f"❌ 检查登录状态时出错: {e}")
            return False
    
    def maintain_active_session(self, max_minutes=10):
        """保持活跃会话"""
        if not self.logged_in:
            print("❌ 请先登录")
            return False
        
        print(f"🕒 开始保持活跃会话，最长 {max_minutes} 分钟")
        
        start_time = time.time()
        max_duration = max_minutes * 60
        activity_count = 0
        
        while time.time() - start_time < max_duration:
            try:
                activity_count += 1
                elapsed_minutes = (time.time() - start_time) / 60
                
                print(f"\n--- 活动轮次 #{activity_count} (已运行 {elapsed_minutes:.1f} 分钟) ---")
                
                # 刷新页面并保持活动
                print("🔄 刷新游戏大厅...")
                self.driver.refresh()
                self.random_delay(3, 5)
                
                # 执行Cookie设置
                self.execute_js_cookies()
                
                # 关闭弹窗
                self.close_popups()
                
                # 检查是否仍然登录
                if not self.check_login_success():
                    print("❌ 检测到已退出登录")
                    break
                
                # 随机等待时间
                wait_time = random.randint(60, 180)
                print(f"⏳ 等待 {wait_time} 秒后进行下一次活动...")
                time.sleep(wait_time)
                
            except Exception as e:
                print(f"❌ 活动过程中出错: {e}")
                time.sleep(60)
        
        print(f"✅ 会话保持完成，共进行 {activity_count} 次活动")
        return True
    
    def run(self, max_minutes=10):
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
    # 测试运行较短时间
    bot = PlayOKSeleniumBot()
    success = bot.run(max_minutes=10)
    
    sys.exit(0 if success else 1)