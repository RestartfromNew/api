# API Frontend Integration Spec
## Login successful 登陆成功后统一规则
所有请求service服务的接口都要携带
```
Authorization: Bearer <access_token>
```
## User(已在云端部署)

### User Register API
用户注册接口，用于创建新用户账号。

#### Endpoints

```http
POST /register
```

#### Headers

```http
Content-Type: application/json
```

#### Body

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | ✅ | 用户名 |
| email | string | ✅ | 邮箱 |
| password | string | ✅ | 密码 |

#### Body 示例

```json
{
  "username": "test_user",
  "email": "test@example.com",
  "password": "Password123!"
}
```

#### 请求示例

```http
POST /register
Content-Type: application/json

{
  "username": "test_user",
  "email": "test@example.com",
  "password": "Password123!"
}
```

#### Response 返回

注册成功 `201`

```json
{
  "message": "success"
}
```

注册失败 `400`

```json
{
  "error": "Invalid email format"
}
```

```json
{
  "error": "Invalid password format"
}
```

```json
{
  "error": "Email already registered"
}
```

```json
{
  "error": "Username already registered"
}
```

服务器错误 `500`

```json
{
  "error": "internal server error"
}
```
---
### User Login API
用户登录接口，返回 access_token 和 refresh_token。

#### Endpoints

```http
POST /login
```

#### Headers

```http
Content-Type: application/json
```

#### Body

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_info | string | ✅ | 用户名或邮箱 |
| password | string | ✅ | 密码 |

#### Body 示例

```json
{
  "user_info": "test@example.com",
  "password": "Password123!"
}
```

#### 请求示例

```http
POST /login
Content-Type: application/json

{
  "user_info": "test@example.com",
  "password": "Password123!"
}
```

#### Response 返回

登录成功 `200`

```json
{
  "message": "success",
  "data": {
    "access_token": "access_xxx",
    "refresh_token": "refresh_xxx",
    "user": {
      "id": "bbc38909-28a2-4a97-95c0-ce9ad56fb7bb",
      "username": "test_user",
      "email": "test@example.com"
    }
  }
}
```

登录失败 `400`

```json
{
  "error": "No such user"
}
```

```json
{
  "error": "Incorrect password"
}
```

服务器错误 `500`

```json
{
  "error": "internal server error"
}
```
---
### Get User Talk API
获取当前用户信息，需要携带 access_token。测试是否能正确验证access token

#### Endpoints

```http
GET /get_user_talk
```

#### Headers

```http
Authorization: Bearer <access_token>
```

#### 请求示例

```http
GET /get_user_talk
Authorization: Bearer <access_token>
```

#### Response 返回

请求成功 `200`

```json
{
  "user_id": "bbc38909-28a2-4a97-95c0-ce9ad56fb7bb"
}
```



---

### `Refresh Token API`
使用 refresh_token 获取新的 access_token。

#### Endpoints

```http
POST /refresh
```

#### Headers

```http
Content-Type: application/json
```

#### Body

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| refresh_token | string | ✅ | 登录返回的 refresh_token |

#### Body 示例

```json
{
  "refresh_token": "refresh_xxx"
}
```

#### 请求示例

```http
POST /refresh
Content-Type: application/json

{
  "refresh_token": "refresh_xxx"
}
```

#### Response 返回

刷新成功 `200`

```json
{
  "message": "success",
  "access_token": "new_access_xxx",
  "expires_at": "2026-03-22T12:00:00+00:00"
}
```

请求体缺失 `400`

```json
{
  "error": "Missing request body"
}
```

缺少 refresh_token `400`

```json
{
  "error": "Missing refresh token"
}
```

refresh token 不存在 `404`

```json
{
  "error": "Refresh token not found"
}
```

refresh token 已撤销 `401`

```json
{
  "error": "Refresh token revoked"
}
```

refresh token 过期，需要重新登录 `401`

```json
{
  "error": "Refresh token expired, please login again"
}
```

refresh token 已过期 `401`

```json
{
  "error": "Refresh token expired"
}
```

---

### Token 使用流程

```text
1. register → 创建账号
2. login → 获取 access_token 和 refresh_token
3. 调用受保护接口时，在 Header 中携带 Authorization: Bearer <access_token>
4. access_token 失效后，调用 /refresh 获取新的 access_token
```


## Characters route (测试中，未上线)
### Upload character assets api
创建角色时，在角色创建成功前应该隐式请求该api，上传文件并写入数据库记录，api返回创建成功后的asset_id，角色正式创建时发回声音和image的asset_id,完成assets和角色的绑定
#### Endpoints
```
POST /characters/upload_character_assets
```
#### Headers
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```
#### Body
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | binary | ✅ | 上传的文件 |
| data | string (JSON) | ✅ | 资源信息 |

Data内容 ```asset_type```为```image```，```voice```或者 ```avatar```中的一种
```json
{
  "asset_type": "avatar"
}
```
#### 请求示例
```json
POST /characters/upload_character_assets
Authorization: Bearer <access_token>

FormData:
- file: (binary file)
- data: "{"asset_type":"voice"}"
```
#### Response返回

上传assets成功
```json
{
  "asset_id": "asset_xxx"
}
```
上传失败
```json
{"error": "no file"}, 400
```

### Create character api
创建角色，并绑定已上传的 assets（image / voice）。在调用该接口前，前端应先调用 `upload_character_assets` 获取对应的 `asset_id`，再在本接口中传入完成绑定。

#### Endpoints

```http
POST /characters/create_character
```

#### Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Body

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 角色名称 |
| gender | string | ❌ | 性别 |
| relationship | string | ❌ | 与用户关系 |
| personality | string | ❌ | 性格描述 |
| background_story | string | ❌ | 背景故事 |
| speak_style | string | ❌ | 说话风格 |
| do_rules | string (JSON) | ❌ | 行为规则（JSON 字符串） |
| dont_rules | string (JSON) | ❌ | 禁止规则（JSON 字符串） |
| image_asset_id | string | ❌ | 图片资源 ID |
| voice_asset_id | string | ❌ | 语音资源 ID |

#### Body 内容示例

```json
{
  "name": "Alice",
  "gender": "female",
  "relationship": "friend",
  "personality": "kind and cheerful",
  "background_story": "A virtual assistant",
  "speak_style": "casual",
  "do_rules": "Be friendly",
  "dont_rules": "Be friendly",
  "image_asset_id": "asset_img_123",
  "voice_asset_id": "asset_voice_456"
}
```

#### 请求示例

```http
POST /characters/create_character
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Alice",
  "gender": "female",
  "relationship": "friend",
  "personality": "kind and cheerful",
  "background_story": "A virtual assistant",
  "speak_style": "casual",
  "do_rules": "Be friendly",
  "dont_rules": "Do not say you are ai",
  "image_asset_id": "asset_img_123",
  "voice_asset_id": "asset_voice_456"
}
```

#### Response 返回

创建成功

```json
{
  "message": "success"
}
```

创建失败

```json
{
  "message": "error detail"
}
```

---
### Get Basic character informations
After login, Get basic character information

#### Endpoints

```http
POST /characters/get_character_list
```

#### Headers

```http
Authorization: Bearer <access_token>
```

#### 请求示例

```http json
POST /characters/get_character_list
Authorization: Bearer <access_token>

```

#### Response 返回

请求成功 `200`

```json
{
  "message": "success",
  "data": {
    "characters": [
      {
        "id": "c7b35b8a-06e7-45e0-9db5-9f9eed54b856",
        "name": "AI女友",
        "gender": "female",
        "relationship": "friend",
        "image_url": "assets/image/101.png"
      },
      {
        "id": "3c8e0a2c-a574-4547-8011-21f963c43479",
        "name": "助手",
        "gender": "male",
        "relationship": "assistant",
        "image_url": "assets/image/102.png"
      },
    ]
  }
}
```

返回空列表
```json
{
  "data": {
    "characters": []
  },
  "message": "success"
}
```



---

### Get or Create Chat Session API
获取或创建用户的聊天会话。如果已存在对应 session，则返回已有 session；否则创建新的 session 并返回。

#### Endpoints

```http
POST /characters/get_or_create_chat_session
```

#### Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Body

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| character_id | string | ✅ | 角色ID（用于区分不同角色会话） |

#### Body 示例

```json
{
  "character_id": "3c8e0a2c-a574-4547-8011-21f963c43479",
}
```

#### 请求示例

```http
POST /characters/get_or_create_chat_session
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "character_id": "3c8e0a2c-a574-4547-8011-21f963c43479",
}
```

#### Response 返回

创建新会话或返回已有会话 `200`

```json
{
  "message": "New chat session created",
  "session_id": "9dc0a43b-cfd8-4746-944b-5f36bea3890f"
}
```

或

```json
{
  "message": "Success,Session Linked",
  "data":{
    
  }
}
```

服务器错误 `500`

```json
{
  "message": "error detail"
}
```