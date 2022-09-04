import os
from textwrap import dedent

import requests
from bs4 import BeautifulSoup
import subprocess

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
}


def request(url: str, headers=None, timeout: int = 0) -> requests.Response:
    """ 进一步封装requests的请求，捕获异常 """
    if headers is None:
        headers = HEADERS
    res = None
    try:
        res = requests.get(url, headers=headers, verify=False)
    except requests.RequestException:
        raise "请求错误"

    return res


class Engine:
    """ 获取、解析、返回目标html """

    def __init__(self):
        # 目标网页的 html 代码
        self.html_code = None
        self.html_dom = None
        pass

    def req_source_page(self, url):
        """ 获取url的源代码 """
        self.html_code = request(url).text
        # print(f"{self.html_code=}")
        # 使用 bs4 将 html 转成 dom 对象，便于提取节点
        self.html_dom = BeautifulSoup(self.html_code, 'lxml')   # 指定 xml 解析器
        return

    def get_content(self) -> str:
        """ 解析源代码，提取目标正文 html 源码 """
        content_dom_lis = self.html_dom.find_all('article',
                                                 class_='Post-NormalMain')
        # print(content_html[0])
        new_content = self.deal_content(content_dom_lis[0])
        print(new_content)
        return str(new_content)

    def deal_content(self, content_dom):
        """ 优化 html的结构：补齐图片懒加载链接、等等 """

        # 1、图片懒加载情况
        image_lis = content_dom.find_all('img', class_='origin_image')
        for item in image_lis:
            item['src'] = item['data-original']
            # item.replaceWith(p)  # Put it where the A element is
        # print(content_dom)

        # 2、网页中的以知乎作为跳转的链接
        # https://link.zhihu.com/?target=
        return content_dom

    def get_css(self) -> str:
        """ 获取css样式 """
        css_1 = '<style type="text/css">.h1{font-size: 10px}</style>'
        css_2 = '<link rel="stylesheet" type="text/css" href="https://...">'

        return css_1 + '\n' + css_2


class Convert:
    def __init__(self):
        pass

    def html2pdf(self, f_path, f_out_name, config):
        """ """
        command_lis = [
            '/Users/jiaozhuzhang/exe_file/wkhtmltopdf',
            '--encoding utf8',
            '--minimum-font-size 18',
            '--load-error-handling ignore',
            '--stop-slow-scripts',
            # '--lowquality',
            '--image-dpi 100',
            # '--image-quality 100',
            # '--disable-smart-shrinking',   # 智能
        ]
        if config.get('css'):
            command_lis.append('--user-style-sheet ' + config['css'])
        f_dir_path = os.path.dirname(f_path)
        f_out_path = os.path.join(f_dir_path, f_out_name)
        print(f_path, f_out_path)
        command_lis.extend((f_path, f_out_path))

        popen = subprocess.Popen(' '.join(command_lis), shell=True,
                                 # stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 # stderr=subprocess.PIPE,
                                 )
        popen.communicate()  # 阻塞直到该进程结束！
        # print(popen.returncode)
        return f_out_path

    def str2html(self, content: str) -> str:
        # 暂存，后期整理
        f_dir_path = './tests'
        f_name = 'test.html'
        f_path = os.path.join(f_dir_path, f_name)
        # 使用 dedent 去除左侧的空白缩进
        standard_html = dedent(f"""
            <html>
            <body>
                {content}
            </body>
            </html>
            """)
        with open(f_path, mode='w', encoding='utf8') as fp:
            fp.write(standard_html)

        return f_path

    def else_(self):
        pass


def zhihu():
    engine_obj = Engine()
    engine_obj.req_source_page('https://zhuanlan.zhihu.com/p/538466362')
    target_content_html = engine_obj.get_content()

    convert_obj = Convert()
    f_path = convert_obj.str2html(target_content_html)
    config = {'css': './components/zhihu/content.css'}
    convert_obj.html2pdf(f_path, 'test.pdf', config)


def write_tmp_html():
    pass


if __name__ == '__main__':
    zhihu()
    pass
