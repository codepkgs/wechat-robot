# 功能

- 发送消息到企业微信机器人。
- 支持所有企业微信机器人消息类型。
- [企业微信机器人](https://work.weixin.qq.com/api/doc/90000/90136/91770)

# 安装

```bash
1. 安装该模块
pip install wechatrobot
```

# 使用

- 获取微信机器人的 `key`

  创建机器人时，会返回一个 `webhook` 的地址，如 `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5cb94c2b-1238-4414-b830-a521523d7a`，则 `key` 为 `5cb94c2b-1238-4414-b830-a521523d7a`

* 使用

  ```python
  key = '5cb94c2b-1238-4414-b830-a521523d7a'

  import wechatrobot
  wxrobot = wechatrobot.WechatRobot(key)
  ```

* 发送文本消息

  ```python
  # 签名
  wxrobot.send_text(content, at_mobiles=None)

  # content 为要发送的文本内容
  # at_mobiles 需要 @ 人的手机号，可以是列表或字符串。如果要 @所有人，则设置 at_mobiles='all'。@ 多个人时，指定 at_mobiles=['18600000000', '18600000001']
  ```

* 发送 `markdown` 消息

  ```python
  # 签名
  wxrobot.send_markdown(contents)

  # contents 为可迭代对象，如列表、元组等。每一行为一个 markdown格式的字符串。
  # 支持的格式参考：https://work.weixin.qq.com/api/doc/90000/90136/91770#markdown%E7%B1%BB%E5%9E%8B
  ```

* 发送图片

  ```python
  # 签名
  wxrobot.send_image(image_path)

  # image_path 支持 HTTP、HTTPS、FTP，互联网上的图片URL。也支持本地的图片路径。
  # 如 wxrobot.send_image('https://img1.maka.im/template/T_G29KRHKN_t1.jpg')
  ```

* 发送图文类型

  ```python
  # 签名
  wxrobot.send_news(news_title, jump_url, picurl=None, news_description=None)

  # news_title          消息标题
  # jump_url            跳转url
  # picurl              图片的url
  # news_description    消息描述
  ```

* 发送文件

  ```python
  # 签名
  wxrobot.send_file(file_path)

  # file_path   要创建的本地文件路径。大小不能超过20M
  ```
