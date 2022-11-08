# 广州某大学经典诵读脚本

依赖: Python3, requests

建议在高峰期的时候进行脚本, 否则匹配可能无法获得对手

## 使用方法
抓取该小程序请求总的key参数, 填入程序key变量内（抓包方法自行解决）
点进Settings——Secrets——Actions的菜单

- 要创建的第一个Secret的Name为KEY，注意KEY要大写
- Value是你抓包获得的key
- 全部输入完成后点击图中圈起来的绿色按钮Add secrect来创建

---

## 推送打卡成功与否的消息（可选功能）

### pushplus 推送加 微信公众号

- 创建一个Repository secret，Name是PUSHPLUS，注意PUSHPLUS要大写。
- Value是pushplus 推送加 的token


毕业了没啥风险了放出来交流学习，如引用请标注出处，仅用作学习，不承担任何风险。

What you want is in the test branch
