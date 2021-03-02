# Crawler Experiment: Automatic Clock In
# 爬虫实验： 自动打卡程序

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

闲的没事做的一个小小的爬虫方面的实验程序

这个程序主要是对爬虫领域的知识进行练习，使用一些小技巧实现一个小功能。
该程序可以实现兰大学生个人工作台的自动登录，并根据指定时间自动进行健康打卡。


## Table of Contents

- [Time](#time)
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [License](#license)


## Time

记录了一下时间：
- 分析：1 hour
- 编写: 30 min
- 封装：30 min
- 文档: 未完成


## Background

在这个程序中，主要用到下列知识：

- 抓包分析
- 账户登录模拟
- cookies获取及处理
- 请求头构建
- 面向对象封装小知识

## Install

### 环境

暂无python2支持
- python == 3.9
- conda == 4.9.2

### 安装依赖

`
pip install -r requirements.txt
`
- requests == 2.25.1
- beautifulsoup4 == 4.9.3

### 下载

由于该程序的主体仅一个函数，将代码下载至本地即可

```
git clone https://github.com/FishAndWasabi/CrawlerExperiment-AutomaticClockIn.git
cd CrawlerExperiment-AutomaticClockIn
```

### 配置信息

在正式运行之前，需要准备两个文件 （名字可以不同）

#### 1. config.info **(必要)**

该文件为打卡的具体信息，具体格式为 `XXX: XXXX`（中间为英文引号+一个空格)

需要的信息：

- **账号**  <u>必要</u>
- **密码**  <u>必要</u>
- **卡号**  <u>必要</u>（校园卡号）
- **姓名**  <u>必要</u>
- **是否在校** <u>选填</u>
- **省**: <u>选填</u>
- **市**: <u>选填</u>
- **县**: <u>选填</u>
- **打卡时间h**: <u>必要</u> （打卡时间的小时，数字 **[0,23]**）
- **打卡时间m**: <u>必要</u> （打卡时间的分钟，数字 **[0,59]**）




#### 2. header.json (备选）


该文件为请求头信息，可用默认的，也可以自己构造

```JSON
{
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
  "Accept-Encoding": "gzip, deflate",
  "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
  "Cache-Control": "max-age=0",
  "Upgrade-Insecure-Requests": "1",
  "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36 Edg/88.0.705.68"
}
```


## Usage

cd 到项目文件所在的目录中

`
python clock_out.py --path XXXXX --header_path XXXXX
`

### 参数说明

- path： 配置文件地址 （默认值为`config.info`)
- header_path: 请求头文件地址,json文件 （默认值为`header.json`)

## Maintainers

[@FishAndWasabi](https://github.com/FishAndWasabi).



## License

[MIT](LICENSE) © Yuming Chen