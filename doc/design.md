# 设计文档

## mongodb数据库设计
### stockholder结构
```json
{
    _id:,
    code:,
    name:,
    holders:[
        {
            date:,
            holdername:,
            rate:,
            change:
        },
        ...
    ]
}
```
