# git操作指南

#### 基础操作
1. 克隆github或者码云上代码到本地 **git clone 地址**
1. 创建自己的分支 **git branch 分支名**
1. 查看当前所有分支 **git branch**
1. 查看当前修改文件的状态 **git status**
1. 添加要上传的文件 **git add 修改后的文件**
1. 添加文件的注解 **git commit -m '注解'**
1. 推送到服务器上 **git push origin zcj**
1. 下拉远程自己分支到本地自己分支 **git pull origin zcj**

#### 代码分支合并，tag提交
1. 将自己代码合并到测试分支，先切换到要合并到的分支 **git checkout dev**
1. 在当前dev分支合并zcj分支 **git merge zcj**
1. **上线代码**需要打tag，在master分支打tag，版本号 **git tag -a 版本号 -m '注解'**
1. 提交版本v1.0.0 **git push origin v1.0.0**

#### 分支版本处理
1. 删除本地分支 **git branch -d zcj**
1. 删除git远程分支 **git push origin --delete zcj**
1. 删除本地版本号 **git tag -d v1.0.0**
1. 删除git远程版本号 **git push origin --delete tag v1.0.0**

#### 缓存机制
在某一个分支修改了代码，但是不想提交，需要到另外一个分支修改相同的代码时就需要用到缓存。<br>

1. 缓存修改的代码 **git stash**
1. 查看缓存的片段 **git stash list**
1. 还原缓存的代码 **git stash apply stash@{0}**

#### 查看某次提交的详情，返回代码到某一次的提交
1. 查看提交的日志记录 **git log**
1. 查看某次提交的内容 **git show id**
1. 退回代码到某一版本 **git reset --hard id**