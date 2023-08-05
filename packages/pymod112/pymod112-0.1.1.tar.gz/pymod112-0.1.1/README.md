# pymod112

一个基于Python开发的公民身份号码检验与地区代码查找程序

## 安装 Installation

[PyPi](https://pypi.org/project/pymod112/) 使用pip安装

```sh
pip install pymod112
```

## 使用 Usage

身份证号码校验

```python
import pymod112

pymod112.mod112('11010519491231002X', details=True)
'''返回值为(dict)
{'id': '11010519491231002X', 
 'province': ['11', '北京市'], 
 'city': ['01', ''], 
 'county': ['05', '朝阳区'], 
 'birth_date': ['1949', '12', '31'], 
 'gender': 0, 
 'result': True, 
 'problem': '000'}
'''

```

查询地区代码对应的地区名

```python
import pymod112

pymod112.code_to_location(['51', '01', '06'])
'''返回值为(list)
['四川省', '成都市', '金牛区']
'''
```

返回全部错误代码及其对应内容

```python
import pymod112

pymod112.code_to_error
'''dict
{'000':'不存在问题',
'001':'<未定义>',
'002':'<未定义>',
'003':'<未定义>',
'004':'参数id长度错误',
'005':'参数id内容包含非法字符',
'006':'参数id不合法',
'007':'参数id中包含不存在的地区',
'008':'参数id中包含不存在的时间'
}
'''
```

## 许可证 License
BSD 3-Clause License

## 更新日志 Changelog
### **0.1.1**
 - 加入参数类型检查
 - 优化错误代码（停用001 002 003）
 - 删除函数problem()

### **0.1.0(2023-6-24)**
- 这是第一个正式发行版
