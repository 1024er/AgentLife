import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


drop_words = [
    '他', '她', '《', '》', '并', '里', '还', '将', '后', '次', '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '王', '俊', '三'
]
log_file = "/Users/hezhi/Downloads/TempPython/threejs_journey/agent_life/py_server/logs/徐磊_05.log"


def extract_tech_articles(log_content: str) -> tuple[list[str], list[str]]:
    pattern = r'你读了一篇技术帖，帖子名为：(.*?)，\n内容为：(.*?)(?=\n\n|$)'
    
    # 查找所有匹配项
    matches = re.finditer(pattern, log_content, re.DOTALL)
    
    titles = []
    contents = []
    
    # 提取标题和内容
    for match in matches:
        title = match.group(1)
        content = match.group(2).strip()
        titles.append(title)
        contents.append(content)
    
    return titles, contents


def extract_news(log_content: str) -> tuple[list[str], list[str]]:
    pattern = r'你正在看一条新闻，新闻标题是：(.*?)，内容是：(.*?)(?=\n\n|$)'
    
    # 查找所有匹配项
    matches = re.finditer(pattern, log_content, re.DOTALL)
    
    titles = []
    contents = []
    
    # 提取标题和内容
    for match in matches:
        title = match.group(1)
        content = match.group(2).strip()
        titles.append(title)
        contents.append(content)
    
    return titles, contents


def extract_serach_results(log_content: str) -> tuple[list[str], list[str]]:
    pattern = r'你搜索了关于 `(.*?)` 的信息'
    matches = re.finditer(pattern, log_content, re.DOTALL)
    
    queries = []
    for match in matches:
        res = match.group(1)
        queries.append(res)
    
    return queries


all_titles, all_contents, all_queries = [],  [], []
with open(log_file, 'r') as f:
    log_content = f.read()
    titles, contents = extract_tech_articles(log_content)
    all_titles.extend(titles)
    all_contents.extend(contents)
    
    titles, contents = extract_news(log_content)
    all_titles.extend(titles)
    all_contents.extend(contents)

    queries = extract_serach_results(log_content)
    all_queries.extend(queries)


# 将所有内容合并成一个字符串
text = ' '.join(all_contents)
# text = ' '.join(all_queries)

# 使用jieba进行分词
words = jieba.cut(text)
words = [word for word in words if word not in drop_words]

# 创建词频字典
from collections import Counter
word_freq = Counter(words)

# 生成词云
wc = WordCloud(
    font_path='/System/Library/Fonts/PingFang.ttc',
    width=800,
    height=400,
    background_color='white'
)

# 使用词频字典生成词云
wordcloud = wc.generate_from_frequencies(word_freq)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
