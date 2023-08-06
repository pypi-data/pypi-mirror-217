import re


class EH:
    def __init__(self, html):
        self.html = html

    def 查找标签(self, 标签名):
        pattern = r"<{}>(.*?)</{}>".format(标签名, 标签名)
        结果 = re.findall(pattern, self.html, re.S)
        return 结果

    def 查找类名(self, 类名):
        pattern = r'class="{}">(.*?)</'.format(类名)
        结果 = re.findall(pattern, self.html, re.S)
        return 结果

    def 查找链接(self):
        pattern = r'<a .*?href="(.*?)".*?>(.*?)</a>'
        结果 = re.findall(pattern, self.html, re.S)
        return 结果

    def 查找属性(self, 属性名):
        pattern = r'{}="(.*?)"'.format(属性名)
        属性值 = re.findall(pattern, self.html, re.S)
        return 属性值

    def 获得文本(self, html):
        pattern = r'>\s*(.*?)\s*</'
        结果 = re.findall(pattern, html, re.S)
        text = ' '.join(结果).strip()
        return text
