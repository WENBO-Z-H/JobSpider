jobSpider程序用来爬取智联招聘网站的计算机软件类招聘信息https://sou.zhaopin.com/?p=1&jl=' + str(number) + '&in=100050000&sf=0&st=0。
其中str(number)是城市对应的代号

智联招聘网站中需要爬取的主体内容是动态加载的，无法直接用requests获取，因此采用selenium的相关方法，模拟浏览器（这里模拟的是火狐浏览器，但要修改也非常方便，只是必须在运行代码的计算机中安装相应的浏览器驱动）直接访问，这样可以获取动态内容加载后的网页，即网页的全部信息。

程序中的各个函数功能说明：
1、getAndSaveOnePageInfo(jobList, length)函数解析一页网页的内容并存入MySQL数据库中
2、login(browser)函数模拟登陆网站，因为爬取时从第三页换到第四页时需要换页。
3、dealOneCity(number)函数获取一个城市的所有招聘信息，在其中会调用getAndSaveOnePageInfo和login函数。
4、startSpider()函数是GUI中开始按钮对应的事件，正式开始爬取。
5、quitSpider()函数是GUI中退出按钮对应的事件，直接退出程序。
6、if __name__ == '__main__'是程序的入口，在其中连接本地MySQL数据库并创建简单的GUI，然后调用mainloop()使GUI显示，程序开始运行。
