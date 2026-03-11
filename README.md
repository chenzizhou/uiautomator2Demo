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
