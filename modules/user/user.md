# User Module
Project: Multi-AI intergration system

Version: 1.0

Author: Beining Yang

Update Date: 2026-0

## 1.Overview
### 1.1 Purpose 
This document describes User module.
It defines tables, relationships, constraints, and security rules.

### 1.2 Scope
This version includes:
+ User authentication
+ Log in authorization and token

## 2.Entity Relationship Overview
+ User
+ Role 
+ User_Role

## 3
### 3.1 Register

```Javascript 
{
  "username": "cin",
  "email": "cin@example.com",
  "password": "123456"
}
```
业务流程
1 验证参数
2 检查 email 是否存在
3 检查 username 是否存在
4 hash password
5 创建用户
6 返回结果

### 3.2 refresh_tokens Table
| Field Name   |     Type    |                      Constraint                      | Description                                                      |
|:----:|:----:|:----:|:----:|
|     id     |     UUID    |   Primary Key; Not Null; Default gen_random_uuid()   | Unique identifier for each refresh token                         |
|   user_id  |     UUID    | Foreign Key → users(id); On Delete Cascade; Not Null | References the user who owns this token                          |
| token_hash |     TEXT    |                       Not Null                       | Hashed version of the refresh token (never store raw token)      |
| expires_at | TIMESTAMPTZ |                       Not Null                       | Expiration timestamp of the refresh token                        |
|   revoked  |   BOOLEAN   |                     Default FALSE                    | Indicates whether the token has been revoked (logout / rotation) |
| created_at | TIMESTAMPTZ |                     Default NOW()                    | Timestamp when the token was created                             |

```SQL
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```
 