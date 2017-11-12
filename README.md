# ShouquCloudBookmarks|收趣云书签
Alfred版收趣云书签，仿[Alfred-Workflow tutorial's Pinboard Workflow](http://www.deanishe.net/alfred-workflow/tutorial.html)

## 一、功能

### 1、显示最近保存的云书签
关键词：**shouqu**

### 2、关键词搜索（搜索范围仅限标题和简介）
关键词：**shouqu** keyword

### 3、指定书签上ENTER可跳转网页，SHIFT可预览网页

### 4、添加链接为书签
关键词：**sqsave** url

### 5、设置userId
关键词：**sqsetid** userId

## 二、userId
如何获取userId：

1. 首先登陆[收趣网页版](http://shouqu.me)
2. 打开浏览器的网页检查器，进入网络选项栏
3. 登陆收趣，在检查器中找到getInfo
4. 根据getInfo?userId=xxxxxx或从返回的json数据中找到"id": xxxxxx

## 三、使用库

http://www.deanishe.net/alfred-workflow/index.html
