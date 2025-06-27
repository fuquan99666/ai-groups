from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
from config import CHROME_PATH  # 你需要配置 CHROME_PATH

def fetch_pku_course_updates():
    """
    登录北京大学选课系统并获取更新信息。
    返回:
        str: 若成功，返回更新内容；否则返回错误信息。
    """
    username = os.getenv("YOUR_STUDENT_ID")
    password = os.getenv("YOUR_PASSWORD")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--headless')  # 无头模式
        # options.add_argument('--disable-gpu')
        service = Service(CHROME_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get('https://course.pku.edu.cn/')
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, "login_stu_a").click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login_panel"))
        )

        driver.find_element(By.ID, "user_name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "logon_button").click()

        time.sleep(3)

        # 同意隐私条款
        try:
            agree = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "agree_button"))
            )
            agree.click()
        except:
            pass
        
        driver.maximize_window()

        # 点击展开导航
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "global-toggle-img"))
            ).click()
        except:
            pass

        # 点击“更新”按钮
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "AlertsOnMyBb_____AlertsTool"))
            ).click()
        except:
            pass

        # 切换 iframe 获取内容
        html_content = ""
        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame(iframe)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#left_stream_alerts .stream_item"))
                )
                left_stream = driver.find_element(By.ID, "left_stream_alerts")
                html_content = driver.execute_script("return arguments[0].outerHTML;", left_stream)
                break
            except:
                continue

        if not html_content:
            return "❌ 未获取到更新区域的内容"

        soup = BeautifulSoup(html_content, "html.parser")
        updates = []

        for item in soup.select(".stream_item"):
            date = item.select_one(".stream_datestamp")
            date_text = date.text.strip() if date else "未知时间"

            context = item.select_one(".stream_context")
            title = ""
            type_ = ""
            course = ""
            detail = ""

            if context:
                if context.select_one(".eventTitle"):
                    title = context.select_one(".eventTitle").text.strip()
                    type_ = "作业"
                elif context.select_one(".announcementType"):
                    type_ = context.select_one(".announcementType").text.strip()
                    if context.select_one(".announcementTitle"):
                        title = context.select_one(".announcementTitle").text.strip()
                course_tag = context.select_one(".stream_area_name")
                if course_tag:
                    course = course_tag.text.strip()
            bottom_course = item.select_one(".stream_context_bottom .stream_area_name")
            if not course and bottom_course:
                course = bottom_course.text.strip()
            details_tag = item.select_one(".stream_details")
            if details_tag:
                detail = details_tag.get_text(separator="\n", strip=True)

            updates.append(f"""时间: {date_text}
类型: {type_}
标题: {title}
课程: {course}
详情: {detail}
{'-' * 40}""")

        return "\n".join(updates)

    except Exception as e:
        return f"❌ 错误: {str(e)}"
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    username = os.getenv("YOUR_STUDENT_ID")
    password = os.getenv("YOUR_PASSWORD")
    result = fetch_pku_course_updates(username, password)
    print(result)