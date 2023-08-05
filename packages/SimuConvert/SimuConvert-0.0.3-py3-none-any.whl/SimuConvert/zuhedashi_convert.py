"""
组合大师净值下载格式转换
------------------------------------------

Created by Yanzhong Huang
Email: yanzhong.huang@outlook.com


"""


import pandas as pd



def _read_simupaipai_csv(path: str) -> pd.DataFrame:
    """
    读取私募排排csv, encoding='gbk'
    : param path: 文件路径
    : return: DataFrame
    
    删除了第一行，单位净值，复权净值，累计净值
    """
    df = pd.read_csv(path, encoding='gbk', index_col=0, low_memory=False, parse_dates=True)  # type: ignore
    # type: ignore 文件除表头外的第一行，显示的是单位净值，复权净值，累计净值，删除
    df.drop(df.index[0], inplace=True)
    return df.dropna(axis=1, how='all')  # type: ignore
    

def convert_simupaipai(path: str) -> pd.DataFrame:
    """
    转换私募排排数据格式
    : param path: 文件路径
    : return: DataFrame
    """
    raw_data = _read_simupaipai_csv(path)
    
    # 分为每三列为一组，数据为一个基金
    funds: list[pd.DataFrame] = []
    for i in range(0, len(raw_data.columns), 3):
        df = raw_data.iloc[:, i:i+3].copy()
        fund_name = df.columns[0]
        df.dropna(inplace=True)  # type: ignore 删除空行
        df.columns = ['nav', 'nav_adj', 'nav_acc']  # 重命名列名        
        df['fund_name'] = fund_name  # 增加基金名称列
        funds.append(df)
    funds_df = pd.concat(funds, axis=0)  # type: ignore
    funds_df.index.name = 'trade_date'
    funds_df.reset_index(inplace=True)
    funds_df.index.name = 'id'
    return funds_df[['trade_date', 'fund_name', 'nav', 'nav_adj', 'nav_acc']]
    

def convert_simupaipai_to_excel(raw_data_path: str, result_path: str) -> None:
    """
    转换私募排排数据格式并保存为excel
    : param raw_data_path: 原始数据路径
    : param result_path: 结果保存路径
    """
    df = convert_simupaipai(raw_data_path)
    df.to_excel(result_path, index=True)  # type: ignore


def convert_simupaipai_to_csv(raw_data_path: str, result_path: str) -> None:
    """
    转换私募排排数据格式并保存为csv
    : param raw_data_path: 原始数据路径
    : param result_path: 结果保存路径
    """
    df = convert_simupaipai(raw_data_path)
    df.to_csv(result_path, index=True)  # type: ignore


if __name__ == '__main__':
    convert_simupaipai_to_csv('SimuConvert/reference_data/zuhedashi.csv', 'test.csv')
