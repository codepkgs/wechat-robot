import base64
import hashlib
import json
from pathlib import Path

import requests


class FileUploadError(Exception): pass


class WechatRobot:
    def __init__(self, robot_key):
        self.key = robot_key
        self.webhook_address = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + self.key

    def _do_request(self, data):
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        resp = requests.post(self.webhook_address, headers=headers, data=json.dumps(data))
        return resp.json()

    @staticmethod
    def _for_image(image_path):
        support_url_prefix = ('http://', 'https://', 'ftp://')
        remote = False

        for i in support_url_prefix:
            if image_path.startswith(i):
                remote = True
                break

        if remote:
            r = requests.get(image_path)
            if r.ok:
                b64_value = base64.b64encode(r.content).decode('utf-8')
                md5_value = hashlib.md5(r.content).hexdigest()
                return b64_value, md5_value
            else:
                return None, None
        else:
            with open(image_path, 'rb') as f:
                content = f.read()
                b64_value = base64.b64encode(content).decode('utf-8')
                md5_value = hashlib.md5(content).hexdigest()
                return b64_value, md5_value

    def send_text(self, content, at_mobiles=None):
        at_mobiles_list = []
        if at_mobiles:
            if isinstance(at_mobiles, str):
                at_mobiles = at_mobiles.split(',')

            at_mobiles = list(at_mobiles)
        else:
            at_mobiles = []

        for member in at_mobiles:
            if member.lower() == 'all':
                at_mobiles_list.append('@all')
            else:
                at_mobiles_list.append(member)

        data = {
            'msgtype': 'text',
            'text': {
                'content': content,
                'mentioned_mobile_list': at_mobiles_list
            }
        }

        return self._do_request(data)

    def send_markdown(self, contents):
        send_contents = ''
        for content in contents:
            if content.startswith('>'):
                send_contents += '\n' + content
            else:
                send_contents += '\n\n' + content

        data = {
            'msgtype': 'markdown',
            'markdown': {
                'content': send_contents
            }
        }
        return self._do_request(data)

    def send_image(self, image_path):
        image_base64, image_md5 = self._for_image(image_path)
        data = {
            'msgtype': 'image',
            'image': {
                'base64': image_base64,
                'md5': image_md5
            }
        }
        return self._do_request(data)

    def send_news(self, news_title, jump_url, picurl=None, news_description=None):
        data = {
            'msgtype': 'news',
            'news': {
                'articles': [
                    {
                        'title': news_title,
                        'url': jump_url,
                        'description': news_description,
                        'picurl': picurl
                    }
                ]
            }
        }

        return self._do_request(data)

    def _put_file(self, file_path):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError('the file <{}> not found'.format(file_path))

        put_file_address = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={}&type=file'.format(self.key)

        resp = requests.post(put_file_address,
                             files=[('media', (path.name, open(file_path, 'rb'), 'application/octet-stream'))])
        return resp.json()

    def send_file(self, file_path):
        resp = self._put_file(file_path)
        if resp['errcode'] == 0:
            media_id = resp['media_id']
        else:
            raise FileUploadError(resp)
        data = {
            'msgtype': 'file',
            'file': {
                'media_id': media_id
            }
        }

        return self._do_request(data)
