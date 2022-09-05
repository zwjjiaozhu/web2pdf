


1、转成pdf命令
/Users/jiaozhuzhang/exe_file/wkhtmltopdf --encoding utf8 main.html main_test.pdf


# wkhtmltopdf 知识

1）加载本地css
--user-style-sheet \User\...\style.css

2）设置最小字体
--minimum-font-size 20

3）开启加载本地文件
如：本地图片、css文件等
```bash
--enable-local-file-access
```
或者
```bash
--disable-local-file-access --allow <path>
```


# 其他

1）url decode、encode
from urllib.parse import quote, unquote
+ quote：编码，转成utf-8字符
+ unquote：解码，转成字符