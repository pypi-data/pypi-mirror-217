# EasyHTML 中文的python HTML解析提取器！
>如果程序错了，请报告给534047068@qq.com。
****
输入首字母快速输入，不用切换输入法。按下Tab键补全。<br>
（我用的pycharm）
****
```python
# 假设有以下 HTML 代码
from Easy_HTML_2023 import EH
html = '''
<html>
<body>
    <div class="container">
        <h1>标题</h1>
        <p>段落文本</p>
        <a href="https://example.com">链接1</a>
        <a href="https://example.com">链接2</a>
    </div>
    <div class="box">
        <h2>副标题</h2>
        <p>其他文本</p>
        <a href="https://example.com">链接3</a>
    </div>
</body>
</html>
'''

# 创建美丽汤对象
soup = EH(html)

# 获取所有的 div 标签内容
div内容 = soup.查找标签('div')
for 内容 in div内容:
    文本内容 = soup.获得文本(内容)
    print(文本内容)

# 获取类名为 "container" 的元素内容
container内容 = soup.查找类名('container')
for 内容 in container内容:
    文本内容 = soup.获得文本(内容)
    print(文本内容)

# 获取所有的链接及其网址
链接列表 = soup.查找链接()

```
运行上述代码将输出以下结果：
```
标题 段落文本 链接1 链接2
标题 段落文本 链接1 链接2
链接1
链接2
https://example.com
https://example.com
```
>使用方法相当于beautifulsoup，不过也略有不同。（可以去看源代码）。