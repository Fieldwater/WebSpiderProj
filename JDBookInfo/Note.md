
# [Scrapy_Redis] 京东图书信息爬虫
#Python/Spiders/Scrapy_Redis

URL = book.jd.com/booksort.html

## 步骤：
1. 创建爬虫项目
`scrapy startproject JDBookInfo`
`scrapy genspider jd jd.com`

2. 查看URL，确定`start_url` -> 可以提取有效数据
	- 判断源码与element是否存在差异
	- 分析标签及内容，编写spider文件

3. 大类分组列表 `dt_list` -> `xpath`得到名称

4. 小类分组列表 `em_list` -> 名称、URL（补全地址）；此处需要设定函数间传递参数`item={}`

5. 当URL不为空时，发送请求：`yield scrapy.Request()`

6. 解析具体列表页内容函数`def parse_book_list()`
	1. 分析源码和element差异 -> 对比 (element & Network)
	2. 传参 `item`
	3. 遍历此页所有书，获取info；！价格内容需要解析`js`后获取
		https://p.3.cn/prices/mgets?&skuIds=J_12475106
		- 取JSON数据：`import json`
			`a = json.loads(response.body.decode())[0]["op"]`
		- `decode()` 返回解码后的字符串
	4. 当前页请求循环结束后，翻页

7. 修改`settings.py` 文件
	- 加入分布式爬虫设置
```python
# Scrapy_redis setting
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
REDIS_URL = "redis://127.0.0.1:6379"
```
	- 修改常规`USER_AGENT`
	- 调整`ROBOTSTXT_OBEY = False`

8. Redis 
	- 清空redis：`flushdb`


---

Note：
1. HTTP状态码：
	- 重定向：300/301/302/303 ，表示浏览器需要进一步操作才能完成请求
	- Scrapy 可以完成重定向请求

2. 使用deep_copy
	- 因为一个大分类下的所有小分类都使用一个item字典，需要deep_copy每次改变小分类的info
	- 简单来说：deepcopy可以使每个值的改变与原来变量无关联；创建新项；如果不用deepcopy，后面的结果会覆盖前一步结果，scrapy异步操作会出错
[Python-copy()与deepcopy()区别 - 枕2畔雪的博客 - CSDN博客](https://blog.csdn.net/qq_32907349/article/details/52190796)

3. 当访问不同网站时，记得`allow_domain`添加域名

4. 写`xpath`时，一定要先确定URL的response中存在标签
	- 在Network中的response中查看；或者在源代码中查看



