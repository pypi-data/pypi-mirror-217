# SimuConvert

净值转换小工具，将净值数据转换为如下格式：

| id | trade_date | fund_name | nav | nav_adj | nav_acc |
| -- | ---------- | --------- | --- | ------- | ------- |
|    |            |           |     |         |         |
|    |            |           |     |         |         |

### 输出格式为：

- pd.DataFrame
- .xlsx
- .csv

### 输入参考格式：

- 组合大师净值导出格式
  - 参考 SimuConvert/reference_data/zuhedashi.csv
