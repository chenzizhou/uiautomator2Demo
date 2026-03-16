# uiautomator2Demo
echo "# uiautomator2Demo" >> README.md
git init
git add README.md
git commit -m "first commit"

# 重命名当前分支为 main
-M 是 --move --force 的缩写。
--move：用于重命名分支。
--force：如果目标名称的分支已经存在，则强制覆盖它。
git branch -M main 

#用于将本地仓库与远程仓库关联起来
#git remote add - 添加一个新的远程仓库
#origin - 这是远程仓库的默认名称（你可以使用其他名称，但origin是约定俗成的标准名称）
https://github.com/chenzizhou/uiautomator2Demo.git - 这是远程仓库的URL地址
git remote add origin https://github.com/chenzizhou/uiautomator2Demo.git

**这条命令 git push -u origin main 是 Git 中用于将本地代码推送到远程仓库的重要命令。让我为您详细解释：
命令分解：
git push - 将本地提交推送到远程仓库
-u (或 --set-upstream) - 设置上游分支，建立本地分支与远程分支的跟踪关系
origin - 远程仓库的名称（通常是默认名称）
main - 要推送的本地分支名称
命令作用：
将本地的 main 分支推送到名为 origin 的远程仓库
-u 参数会在推送的同时建立本地分支与远程分支的关联关系，这样以后在这个分支上只需使用 git push 或 git pull 而不需要再指定远程仓库和分支名**
git push -u origin main

学习文档
https://github.com/openatx/uiautomator2
https://github.com/openatx/uiautomator2/blob/master/README_CN.md
安装
前置安装：
        - pip install pbr
        - pip install pywin32
        - pip install humanize

1. pip 安装
            pip install uiautomator2==2.7.3， 或者下载源码安装 ，本人使用 2.7.3版本（其他版本可能会有各种异常）
            pip install weditor==0.4.3,  安装页面元素定位工具
            创建快捷方式: weditor --shortcut
2. 其他依赖工具(华为手机）
            官方文档有自动化配置：python -m uiautomator2 init, 可是公司网络不支持下载，下面附件中我给出已配置好的脚本和安装文件，连上手机下载解压install.rar后, 直接执行install_ua2.cmd命令即可将往手机中push所有依赖包,并启动必要服务。
            这部分包括： app-uiautomator.apk， app-uiautomator-test.apk, atx-agent, minicap, minitouch, 
4. 修改源码，防止在线下载导致启动失败
       修改源文件：`venv\Lib\sit-packages\uiautomator2\__init__.py`, 注释掉如下几行
   #initer =Initer(ad)
   #...
   #initer.install()
   
元素定位
pip install weditor
xpath
层级
页面相对位置
点击操作

