# 后端测试说明

## 一、测试覆盖范围

当前自动化测试覆盖以下核心流程：
- 注册成功 + 登录成功
- 重复账号注册失败
- 密码错误登录失败
- 昵称修改成功 + 昵称长度校验失败

测试文件：
- `backend_fastapi/tests/test_auth_user_flow.py`

## 二、如何运行

在 `backend_fastapi` 目录执行：

```powershell
python -m pytest -q
```

## 三、测试设计说明

- 使用内存 SQLite（`sqlite:///:memory:`），不会污染本地业务库。
- 测试重点放在认证与用户资料闭环，属于上线前高风险路径。

## 四、当前已知注意事项

- 若提示 `No module named pytest`，先安装依赖：

```powershell
python -m pip install -r .\requirements.txt
```

- 密码已改为 `passlib + bcrypt` 哈希存储。
- 历史明文密码账号在首次登录成功后会自动升级为哈希存储。
