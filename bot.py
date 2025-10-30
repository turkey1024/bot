#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
import sys
import requests

class PlayOKSeleniumBot:
    def __init__(self):
        self.base_url = "https://www.playok.com"
        # 硬编码账号密码
        self.username = "bot1024"
        self.password = "bot123"
        self.driver = None
        self.logged_in = False
        self.heartbeat_count = 0
        
    def setup_driver(self):
        """设置 Chrome 无头浏览器 - 优化稳定版"""
        print("🚀 初始化 Chrome 无头浏览器...")
        
        chrome_options = Options()
        
        # 无头模式配置
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 性能优化
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-background-timer-throttling')
        
        # 反检测配置
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # 使用 webdriver-manager 自动管理 ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)
            
            # 执行脚本隐藏 webdriver 属性
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ 浏览器初始化成功")
            return True
            
        except Exception as e:
            print(f"❌ 浏览器初始化失败: {e}")
            return False
    
    def robust_delay(self, seconds, reason=""):
        """稳健的延迟函数，带原因说明"""
        if reason:
            print(f"⏳ {reason} - 等待 {seconds} 秒...")
        else:
            print(f"⏳ 等待 {seconds} 秒...")
        time.sleep(seconds)
    
    def wait_for_element(self, by, value, timeout=20, description=""):
        """等待元素出现 - 增加超时时间和描述"""
        try:
            if description:
                print(f"🔍 等待元素: {description}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            if description:
                print(f"✅ 找到元素: {description}")
            return element
        except TimeoutException:
            print(f"❌ 等待元素超时: {by}={value} ({description})")
            return None
    
    def wait_for_element_clickable(self, by, value, timeout=20, description=""):
        """等待元素可点击 - 增加超时时间和描述"""
        try:
            if description:
                print(f"🔍 等待元素可点击: {description}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            if description:
                print(f"✅ 元素可点击: {description}")
            return element
        except TimeoutException:
            print(f"❌ 等待元素可点击超时: {by}={value} ({description})")
            return None
    
    def close_popups_robust(self):
        """稳健的弹窗关闭"""
        print("🎯 处理弹窗...")
        
        popup_selectors = [
            "div[class*='qc-cmp'] button",
            "button[class*='accept']",
            "button[class*='agree']",
            "button[onclick*='close']",
        ]
        
        closed = False
        for selector in popup_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        if element.is_displayed():
                            self.driver.execute_script("arguments[0].click();", element)
                            print(f"✅ 关闭弹窗: {selector}")
                            self.robust_delay(2, "弹窗关闭后等待")
                            closed = True
                            break
                    except:
                        continue
                if closed:
                    break
            except:
                continue
        
        if not closed:
            print("ℹ️ 未找到需要关闭的弹窗")
        
        return closed
    
    def robust_login(self):
        """稳健的登录流程"""
        print("🎮 开始登录流程...")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            print(f"\n--- 登录尝试 {attempt + 1}/{max_attempts} ---")
            
            try:
                # 访问页面
                print("📄 加载登录页面...")
                self.driver.get(f"{self.base_url}/zh/gomoku/")
                self.robust_delay(5, "页面加载")
                
                # 处理弹窗
                self.close_popups_robust()
                
                # 查找并点击登录按钮
                login_button = self.wait_for_element_clickable(
                    By.XPATH, 
                    "//button[contains(text(), '登入')]", 
                    description="登录按钮"
                )
                
                if not login_button:
                    print("❌ 未找到登录按钮")
                    continue
                
                # 点击登录按钮
                self.driver.execute_script("arguments[0].click();", login_button)
                print("✅ 点击登录按钮")
                self.robust_delay(3, "登录表单展开")
                
                # 再次处理可能出现的弹窗
                self.close_popups_robust()
                
                # 查找表单字段
                username_field = self.wait_for_element(
                    By.NAME, "username", 
                    description="用户名字段"
                )
                password_field = self.wait_for_element(
                    By.NAME, "pw", 
                    description="密码字段"
                )
                
                if not username_field or not password_field:
                    print("❌ 未找到登录表单字段")
                    continue
                
                # 输入凭据
                print("⌨️ 输入登录信息...")
                username_field.clear()
                username_field.send_keys(self.username)
                self.robust_delay(1, "用户名输入后")
                
                password_field.clear()
                password_field.send_keys(self.password)
                self.robust_delay(1, "密码输入后")
                
                # 提交表单
                print("📤 提交登录表单...")
                submit_button = self.wait_for_element_clickable(
                    By.XPATH, 
                    "//button[contains(text(), '登入')]", 
                    description="提交按钮"
                )
                
                if submit_button:
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    print("✅ 提交登录表单")
                else:
                    # 尝试直接提交表单
                    form = self.driver.find_element(By.XPATH, "//form")
                    if form:
                        self.driver.execute_script("arguments[0].submit();", form)
                        print("✅ 通过JS提交表单")
                    else:
                        print("❌ 未找到提交方式")
                        continue
                
                # 等待登录处理
                self.robust_delay(8, "登录处理")
                
                # 检查登录状态
                if self.check_login_status():
                    print("🎉 登录成功！")
                    self.logged_in = True
                    return True
                else:
                    print("❌ 登录状态检查失败")
                    continue
                    
            except Exception as e:
                print(f"❌ 登录尝试 {attempt + 1} 失败: {e}")
                if attempt < max_attempts - 1:
                    print("🔄 准备重试...")
                    self.robust_delay(5, "重试前等待")
                continue
        
        print("💥 所有登录尝试均失败")
        return False
    
    def check_login_status(self):
        """检查登录状态"""
        try:
            page_source = self.driver.page_source
            current_url = self.driver.current_url
            
            print(f"🔍 检查登录状态 - URL: {current_url}")
            
            # 检查登出标识
            logout_indicators = ['logout', 'log out', '退出', '登出']
            for indicator in logout_indicators:
                if indicator in page_source.lower():
                    print(f"✅ 找到登出标识: {indicator}")
                    return True
            
            # 检查用户名是否在页面内容中
            if self.username in page_source:
                # 确保不是在表单值中
                if f'value="{self.username}"' not in page_source and f"value='{self.username}'" not in page_source:
                    print(f"✅ 用户名 {self.username} 在页面内容中")
                    return True
            
            # 检查是否仍在登录页面
            if 'username' in page_source.lower() and 'password' in page_source.lower():
                print("❌ 仍在登录页面")
                return False
            
            # 如果URL变化且没有登录表单，认为成功
            if 'login' not in current_url and 'signin' not in current_url:
                print("✅ URL已变化，可能登录成功")
                return True
            
            print("❓ 无法确定登录状态")
            return False
            
        except Exception as e:
            print(f"❌ 检查登录状态时出错: {e}")
            return False
    
    def heartbeat_activity(self):
        """心跳活动 - 保持会话活跃"""
        self.heartbeat_count += 1
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n❤️ 心跳 #{self.heartbeat_count} - {current_time}")
        
        try:
            # 随机选择活动类型
            activity_type = random.choice(['refresh', 'navigate', 'check'])
            
            if activity_type == 'refresh':
                print("🔄 刷新页面...")
                self.driver.refresh()
                self.robust_delay(5, "页面刷新后")
                
            elif activity_type == 'navigate':
                pages = [
                    f"{self.base_url}/zh/gomoku/",
                    f"{self.base_url}/zh/",
                ]
                target = random.choice(pages)
                print(f"🧭 导航到: {target}")
                self.driver.get(target)
                self.robust_delay(5, "页面导航后")
                
            else:  # check
                print("📊 检查状态...")
                # 只是保持活动，不进行页面操作
            
            # 处理可能出现的弹窗
            self.close_popups_robust()
            
            # 检查登录状态
            if not self.check_login_status():
                print("❌ 登录状态丢失，尝试重新登录...")
                return self.robust_login()
            
            print("✅ 心跳活动完成，状态正常")
            return True
            
        except Exception as e:
            print(f"❌ 心跳活动出错: {e}")
            # 尝试恢复
            try:
                self.driver.get(f"{self.base_url}/zh/gomoku/")
                self.robust_delay(5, "恢复页面后")
                return self.check_login_status()
            except:
                return False
    
    def maintain_session_60min(self):
        """保持会话60分钟"""
        if not self.logged_in:
            print("❌ 未登录，无法保持会话")
            return False
        
        print("🕒 开始60分钟会话保持...")
        print("📊 将定期进行心跳活动保持在线状态")
        
        start_time = time.time()
        end_time = start_time + (60 * 60)  # 60分钟
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while time.time() < end_time:
            try:
                elapsed = (time.time() - start_time) / 60
                remaining = (end_time - time.time()) / 60
                
                print(f"\n--- 会话状态: 已运行 {elapsed:.1f} 分钟，剩余 {remaining:.1f} 分钟 ---")
                
                # 执行心跳活动
                if self.heartbeat_activity():
                    consecutive_errors = 0  # 重置错误计数
                else:
                    consecutive_errors += 1
                    print(f"⚠️ 连续错误计数: {consecutive_errors}/{max_consecutive_errors}")
                    
                    if consecutive_errors >= max_consecutive_errors:
                        print("💥 连续错误过多，停止会话保持")
                        break
                
                # 计算下一次心跳的等待时间（2-5分钟）
                next_heartbeat = random.randint(120, 300)
                
                # 如果剩余时间不足，调整等待时间
                if time.time() + next_heartbeat > end_time:
                    next_heartbeat = max(60, int(end_time - time.time()))
                    if next_heartbeat <= 0:
                        break
                
                print(f"⏰ 下次心跳在 {next_heartbeat} 秒后...")
                
                # 在等待期间进行简单的状态检查
                wait_start = time.time()
                while time.time() - wait_start < next_heartbeat:
                    # 每30秒检查一次基本状态
                    time.sleep(30)
                    
                    # 简单状态检查（不进行页面操作）
                    elapsed_total = (time.time() - start_time) / 60
                    if elapsed_total % 5 < 0.1:  # 每5分钟打印一次状态
                        print(f"📈 持续运行中: {elapsed_total:.1f} 分钟")
                
            except Exception as e:
                print(f"❌ 会话保持过程中出错: {e}")
                consecutive_errors += 1
                
                if consecutive_errors >= max_consecutive_errors:
                    print("💥 错误过多，停止运行")
                    break
                
                self.robust_delay(30, "错误恢复")
        
        total_duration = (time.time() - start_time) / 60
        print(f"\n🎊 会话保持完成 - 总计运行: {total_duration:.1f} 分钟")
        print(f"❤️ 总心跳次数: {self.heartbeat_count}")
        
        return total_duration >= 55  # 如果运行了55分钟以上认为成功
    
    def run_60min_test(self):
        """运行60分钟测试"""
        print("=" * 60)
        print("🎮 PlayOK Selenium 机器人 - 60分钟测试版")
        print(f"📝 账号: {self.username}")
        print("⏰ 计划运行: 60分钟")
        print("=" * 60)
        
        success = False
        try:
            # 1. 初始化浏览器
            if not self.setup_driver():
                return False
            
            # 2. 登录
            print("\n" + "="*30)
            print("阶段 1: 登录")
            print("="*30)
            
            if not self.robust_login():
                print("❌ 登录阶段失败")
                return False
            
            # 3. 保持会话60分钟
            print("\n" + "="*30)
            print("阶段 2: 60分钟会话保持")
            print("="*30)
            
            session_success = self.maintain_session_60min()
            
            if session_success:
                print("🎉 60分钟测试成功完成！")
                success = True
            else:
                print("❌ 60分钟测试未完成完整时长")
                success = False
                
        except Exception as e:
            print(f"💥 程序运行出错: {e}")
            success = False
            
        finally:
            print("\n" + "="*30)
            print("阶段 3: 清理资源")
            print("="*30)
            self.cleanup()
        
        return success
    
    def cleanup(self):
        """清理资源"""
        if self.driver:
            print("🧹 关闭浏览器...")
            try:
                self.driver.quit()
                print("✅ 浏览器已关闭")
            except Exception as e:
                print(f"⚠️ 关闭浏览器时出错: {e}")

if __name__ == "__main__":
    # 创建机器人实例
    bot = PlayOKSeleniumBot()
    
    # 运行60分钟测试
    success = bot.run_60min_test()
    
    # 退出
    if success:
        print("\n🎊 60分钟测试成功完成！")
        sys.exit(0)
    else:
        print("\n💥 60分钟测试失败")
        sys.exit(1)