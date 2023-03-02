# 广州某大学经典诵读脚本
## 简介

- 脚本使用Github Actions每天自动运行经典诵读小程序

- 将在北京时间09点00分自动运行

- 支持pushplus 推送加 推送消息

- 建议在高峰期的时候进行脚本, 否则匹配可能无法获得对手

## 使用方法
### 0、必要设置
- 点击右上角的Star，使其变亮
- 点击fork，创建项目分支到你的仓库

### 1、抓取该小程序请求的key参数，并记录下来（抓包方法自行解决）

- 提示：可用HttpCanary

### 2、点进Settings——Secrets and variables——Actions的菜单

- 要创建的第一个Secret的Name为KEY，注意KEY要大写
- Value是你抓包获得的key
- 全部输入完成后点击图中圈起来的绿色按钮Add secrect来创建

### 3、开始每天运行
- 点击上方菜单栏里的Actions
- 点击左边的clock-in
- 点击黄色框里的Enable workflow
- 点击Run workflow（用来测试一下是否能运行）


## （可选功能）推送打卡成功与否的消息

- 关注pushplus 推送加 微信公众号
- 创建一个Repository secret，Name是PUSHPLUS，注意PUSHPLUS要大写。
- Value是pushplus 推送加 的token


毕业了没啥风险了放出来交流学习，如引用请标注出处，仅用作学习，不承担任何风险。

