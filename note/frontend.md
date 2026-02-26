# Frontend
## Vue
### Popular Questions

## React
### Popular Questions

## Webpack
### Popular Questions

## 状态管理
### 客户端状态存储/持久化
用 localStorage/sessionStorage 来记录用户的活动状态和登录信息，目的是做状态管理

#### localStorage VS sessionStorage
localStorage：数据永久保存，除非你手动清除或用代码删除。
- 关闭浏览器、关机重启，数据都还在。适合存"记住我"的登录 token、用户偏好设置等。

sessionStorage：数据只在当前标签页会话中存在，关闭标签页就没了。
- 同一个浏览器开两个标签页，它们的 sessionStorage 是互相隔离的。适合存临时状态。