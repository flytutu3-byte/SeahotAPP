from typing import Any

# path 为校验路径，默认是检验response的data字段下的字段
def validate_schema(data: Any, schema: Any, path: str = "data") -> None:
    """校验响应字段结构。

    支持三种写法：
    - {"items": list, "has_more": bool}
    - {"status": {"code": int}}
    - {"field": (str, type(None))}
    - {"code": 10000, "msg": "success"}
    """

    if isinstance(schema, dict):
        assert isinstance(data, dict), f"{path} 应该是 dict，实际是 {type(data).__name__}"

        for key, child_schema in schema.items():
            # schema 字段名以 ? 结尾，表示这个字段可以不返回。
            # 例如 "images?": [...]，没有 images 时跳过，有 images 时继续校验类型。
            optional = key.endswith("?")
            field_name = key[:-1] if optional else key

            if optional and field_name not in data:
                continue

            assert field_name in data, f"{path} 缺少字段: {field_name}"
            validate_schema(data[field_name], child_schema, f"{path}.{field_name}")
        return

    if isinstance(schema, list):
        assert isinstance(data, list), f"{path} 应该是 list，实际是 {type(data).__name__}"

        if schema:
            # [POST_ITEM_SCHEMA] 这种写法表示：列表里的每一个元素都要按 POST_ITEM_SCHEMA 校验。
            for index, item in enumerate(data):
                validate_schema(item, schema[0], f"{path}[{index}]")
        return

    if isinstance(schema, tuple):
        # (str, type(None)) 这种写法表示：允许多个类型，比如字符串或 null。
        assert isinstance(data, schema), f"{path} 类型错误，期望 {schema}，实际是 {type(data).__name__}"
        return

    if isinstance(schema, type):
        assert isinstance(data, schema), f"{path} 类型错误，期望 {schema.__name__}，实际是 {type(data).__name__}"
        return

    # 其他普通值表示固定值校验。
    # 例如 {"code": 10000, "msg": "success"} 会要求接口返回值完全相等。
    assert data == schema, f"{path} 值错误，期望 {schema!r}，实际是 {data!r}"
