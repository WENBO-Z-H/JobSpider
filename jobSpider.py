"""
智联招聘有js动态渲染等方式生成的源代码，如果仅用普通的请求方式如requests来获取网页信息则只能获取网站原始的静态源码而不能
获取到动态渲染之后的新内容，我们的解析目标就是这部分动态渲染的新内容，所以不能用一般的请求方式,本程序使用selenium库和
FirefoxDriver来模拟用户手动点击进入网页，并获取包括动态内容在内的全部源码，然后用BeautifulSoup解析,最后将结果存入本地数据库
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import tkinter
import sys
import pymysql
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getAndSaveOnePageInfo(jobList, length):  # 获取并暂存一页的信息，形参是招聘信息列表和列表长度
    for i in range(length):  # 循环用于遍历该页所有的招聘信息
        info = {}  # 每个招聘信息的格式是固定的，使用字典保存
        # jobList列表的每个元素都是bs4.BeautifulSoup对象，可以直接调用find方法，调用后返回值依旧是对象，再连接着调用
        # attrs获取属性，或调用string获取html元素中的字符串，或调用findall获取具有特定名称的html元素的列表，最后存入字典
        info['enterUrl'] = jobList[i].find(name='a').attrs['href']
        info['jobName'] = jobList[i].find(
            attrs={'class': 'contentpile__content__wrapper__item__info__box__jobname__title'}).attrs['title']
        info['companyName'] = jobList[i].find(
            attrs={'class': 'contentpile__content__wrapper__item__info__box__cname__title company_title'}).attrs[
            'title']
        info['salary'] = jobList[i].find(
            attrs={'class': 'contentpile__content__wrapper__item__info__box__job__saray'}).string
        demandList = jobList[i].find(
            attrs={'class': 'contentpile__content__wrapper__item__info__box__job__demand'}).find_all(name='li')
        info['area'] = demandList[0].string
        info['experience'] = demandList[1].string.strip()
        info['eduBackground'] = demandList[2].string
        companyInfoList = jobList[i].find(
            attrs={'class': 'contentpile__content__wrapper__item__info__box__job__comdec'}).find_all(name='span')
        info['companyType'] = companyInfoList[0].string
        info['scale'] = companyInfoList[1].string
        try:  # 此处的异常处理是因为有极少数招聘信息的源码不规范，我们需要跳过他们
            welfareList = jobList[i].find(
                attrs={'class': 'contentpile__content__wrapper__item__info__box__welfare job_welfare'}).find_all(
                name='div')
        except AttributeError:
            continue
        welfare = welfareList[0].string  # welfare是以列表形式获取的，这里把他们连接成一个字符串并以','分隔
        for j in range(len(welfareList) - 1):
            welfare += ', ' + welfareList[j + 1].string
        info['welfare'] = welfare
        # 存入数据库中
        sql = 'INSERT INTO jobdata(enterUrl, jobName, companyName, salary, area, experience, eduBackground,' \
              'companyType, scale, welfare) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(sql, (info['enterUrl'], info['jobName'], info['companyName'], info['salary'],
                                 info['area'], info['experience'], info['eduBackground'], info['companyType'],
                                 info['scale'], info['welfare']))
            db.commit()
            print("sus")
        except:  # 异常时回滚，忽略这次插入
            print('fal')
            db.rollback()
    t.insert("end", '本页共有' + str(length) + '条信息\n')
    t.update()


def login(browser):
    wait = WebDriverWait(browser, 30, 0.4)  # 显示等待时间，定位界面元素时0.4秒搜索一次，直到搜索成功
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/a')))
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div[2]/a').click()
    browser.switch_to.window(browser.window_handles[1])
    t.insert("end", '开始登陆\n')
    t.update()
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/ul/li[2]')))
    browser.find_element_by_xpath('//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/ul/li[2]').click()
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/div/div[1]/div/zp-input[1]/input')))
    browser.find_element_by_xpath('//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/div/div['
                                  '1]/div/zp-input[1]/input').click()
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/div/div[1]/div/zp-input[1]/input')))
    browser.find_element_by_xpath('//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/div/div['
                                  '1]/div/zp-input[1]/input').send_keys('18729732092')
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/div/div[1]/div/zp-input[2]/input')))
    browser.find_element_by_xpath('//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/div/div['
                                  '1]/div/zp-input[2]/input').send_keys('mql761228')
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/div/div[1]/div/zp-submit/button')))
    browser.find_element_by_xpath('//*[@id="zpPassportWidgetContainer"]/div/div/div/div[2]/div/div['
                                  '1]/div/zp-submit/button').click()
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '/html/body/div[2]/div/div/div[2]/button[2]')))
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/button[2]').click()
    t.insert("end", '登陆成功\n')
    time.sleep(1.5)


def dealOneCity(number):  # 获取一个城市的所有招聘信息，形参是城市对应的编号
    t.insert("end", '开始爬取编号为' + str(number) + '的城市的招聘信息 (530:北京 538:上海 763:广州 765:深圳 801:成都)\n')
    t.update()
    browser = webdriver.Firefox()  # 用GeckoDriver驱动火狐浏览器
    browser.maximize_window()  # 窗口最大化
    browser.implicitly_wait(15)  # 隐性等待时间，即网页加载不好时最多等待到15秒
    wait = WebDriverWait(browser, 30, 0.4)  # 显示等待时间，定位界面元素时0.4秒搜索一次，直到搜索成功
    url = 'https://sou.zhaopin.com/?p=1&jl=' + str(number) + '&in=100050000&sf=0&st=0'
    browser.get(url)  # 获取网页
    time.sleep(0.5)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div/div/button')))  # 等待警告信息出现
    browser.find_element_by_xpath('/html/body/div[2]/div/div/button').click()  # 等待信息出现后点击使其消失
    t.insert("end", '点击了警告信息\n')
    t.update()
    time.sleep(1)
    i = 0
    while True:
        i = i + 1
        t.insert("end", '当前爬取的网址为:' + browser.current_url + '\n')
        t.update()
        browser.execute_script("window.scrollBy(0,20000)")  # 模拟滚轮滚到底部，解决懒加载问题并使翻页按钮可见
        soup = BeautifulSoup(browser.page_source, "html.parser")  # 解析网页
        try:  # 这里寻找的元素就是我们需要的元素，但偶尔会因特殊原因查找不到，这时候转而处理下一页而不是直接退出
            jobList = soup.find(attrs={'id': 'listContent'}).find_all(
                attrs={'class': 'contentpile__content__wrapper clearfix'})
        except AttributeError:
            break
        length = len(jobList)
        getAndSaveOnePageInfo(jobList, length)  # 爬取一页的信息
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagination_content"]/div/button[2]')))
        # 等待翻页按钮可见
        next_page = browser.find_element_by_xpath('//*[@id="pagination_content"]/div/button[2]')  # 暂存翻页按钮
        if next_page.is_enabled():  # 可点击时翻页
            next_page.click()
            t.insert("end", '第' + str(i) + '页爬取成功，翻到第' + str(i + 1) + '页\n')
            t.update()
        else:  # 不可点击时说明已经到了最后一页，直接返回
            t.insert("end", '第' + str(i) + '页爬取成功，已经是最后一页\n')
            t.update()
            browser.quit()
            return
        time.sleep(1.5)
        if i == 3:  # 第3页翻到第4页时需要登陆，这里采用模拟登陆
            login(browser)
    browser.close()


def startSpider():
    # 通过编号调用dealOneCity就可以爬取一个城市的信息，多次调用就可以获得多个城市的信息
    dealOneCity(530)  # 获取北京招聘信息
    dealOneCity(538)  # 获取上海招聘信息
    dealOneCity(763)  # 获取广州招聘信息
    dealOneCity(765)  # 获取深圳招聘信息
    dealOneCity(801)  # 获取成都招聘信息
    t.insert("end", '成功爬取\n')


def quitSpider():  # 界面上退出按钮对应的事件，即退出该程序
    sys.exit()


if __name__ == '__main__':
    # 连接本地数据库
    db = pymysql.connect(host='localhost', user='root', password='123', port=3306, db='spiders')
    cursor = db.cursor()
    # 界面的搭建
    top = tkinter.Tk()
    top.title("jobSpider")
    top.minsize(600, 620)
    b1 = tkinter.Button(top, text='开始', font=('KaiTi', 15, 'bold'), bg='white', fg='black', bd=2, width=10,
                        command=startSpider)
    b1.grid(row=7, column=1, pady=3)
    b2 = tkinter.Button(top, text='退出', font=('KaiTi', 15, 'bold'), bg='white', fg='black', bd=2, width=10,
                        command=quitSpider)
    b2.grid(row=7, column=6, pady=3)
    t = tkinter.Text(top, width=100, height=40)
    t.grid(row=1, column=1, rowspan=6, columnspan=6, padx=20, pady=20)
    # 界面显示，程序开始
    top.mainloop()
