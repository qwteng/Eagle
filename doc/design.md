# 设计文档
本项目从互联网网站采集A股股票信息，进行数据加工、存储,然后基于加工后的数据进行数据分析。

本文档描述了本项目数据处理流程、数据结构、数据分析等相关设计。


## 数据处理流程

```flow
st=>start: start
e=>end
op=>operatioin: My Op1
op1=>operatioin: My Op2
cond=>condition: Yes or No?

st->op->cond
st->op1
cond(yes)->e
cond(no)->op
```

## 数据结构设计
### stockholder数据结构定义
```json
{
    code:,
    name:,
    holder:
        {
            date:,
            holdername:,
            number:,
            rate:,
            change:
        }
}
```
