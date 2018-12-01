### 抓取目标
我们要爬取的目标是必胜客中国。打开必胜客中国首页，进入“餐厅查询”页面。[here](http://www.pizzahut.com.cn/StoreList#)

我们要爬取的数据内容有城市、餐厅名字、餐厅地址以及餐厅联系电话。因为我看到页面中有地图，所以页面一定有餐厅地址的经纬度。因此，餐厅的经纬度也是我们需要爬取的数据。

### 分析页面

我们使用浏览器的开发者工具对页面结构进行简单分析。

我们在 StoreList 页面中能找到我们所需的数据。这个能确定数据提取的 xpath 语法。

StoreList 页面的 Response 内容比较长，往下看看，最后我们找到调用获取餐厅列表信息的 JavaScript 函数代码。

我们接着搜索下 GetStoreList 函数，看看浏览器如何获取餐厅列表信息的。

最后，我们发现页面以 POST 方式请求[地址](http://www.pizzahut.com.cn/StoreList)。同时请求还携带参数 pageIndex 和 pageSize。

