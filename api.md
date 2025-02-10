# Healer Backend API 文檔

## 基本信息
- Base URL: `https://[YOUR-APP-URL]`
- Content-Type: `application/json`

## API 端點

### 推薦科別
根據症狀推薦適合的醫療科別，並返回相關醫療機構的位置資訊。

#### 請求
- Method: `POST`
- Path: `/api/recommend-departments`
- Content-Type: `application/json`

##### 請求體格式
```json
{
    "symptoms": string[]  // 症狀列表
}
```

##### 參數說明
| 參數 | 類型 | 必填 | 說明 | 範例 |
|------|------|------|------|------|
| symptoms | array | 是 | 症狀列表 | ["頭暈", "發燒40度"] |

#### 響應
##### 成功響應 (200 OK)
```json
[
    {
        "name": string,        // 科別名稱
        "coordinates": [       // 醫療機構位置列表
            {
                "name": string,   // 醫療機構名稱
                "x": number,   // 經度
                "y": number    // 緯度
            }
        ]
    }
]
```

##### 響應字段說明
| 字段 | 類型 | 說明 | 範例 |
|------|------|------|------|
| name | string | 科別名稱 | "內科" |
| coordinates | array | 醫療機構位置列表 | - |
| coordinates[].name | string | 醫療機構名稱 | "仁愛醫院" |
| coordinates[].x | number | 經度 | 121.5598 |
| coordinates[].y | number | 緯度 | 25.0338 |

##### 錯誤響應
```json
{
    "error": string  // 錯誤訊息
}
```

##### 錯誤代碼
| HTTP 狀態碼 | 說明 | 可能原因 |
|------------|------|----------|
| 400 | 請求參數錯誤 | symptoms 為空或格式錯誤 |
| 404 | 未找到結果 | 沒有符合條件的醫療機構 |
| 500 | 服務器錯誤 | API 調用失敗或其他內部錯誤 |

#### 使用範例

##### 請求範例
```bash
curl -X POST https://[YOUR-APP-URL]/api/recommend-departments \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["頭暈", "發燒40度"]
  }'
```

##### 成功響應範例
```json
[
    {
        "name": "急診科",
        "coordinates": [
            {
                "name": "台北醫學大學附設醫院",
                "x": 121.5598,
                "y": 25.0338
            },
            {
                "name": "仁愛醫院",
                "x": 121.5234,
                "y": 25.0532
            }
        ]
    },
    {
        "name": "內科",
        "coordinates": [
            {
                "name": "臺大醫院",
                "x": 121.5432,
                "y": 25.0445
            },
            {
                "name": "馬偕醫院",
                "x": 121.5123,
                "y": 25.0234
            }
        ]
    }
]
```

##### 錯誤響應範例
```json
{
    "error": "Symptoms must be a non-empty list"
}
```

## 注意事項
1. 返回的醫療機構位置已經過篩選：
   - 評分 >= 4.0
   - 評論數 >= 50
   - 每個科別最多返回 5 個位置
2. 科別列表按照推薦優先順序排序
3. 所有請求都需要使用 HTTPS
4. 所有響應都使用 UTF-8 編碼

## 限制
1. API 請求頻率限制：尚未實施
2. 每個科別最多返回 5 個醫療機構位置
3. 請求體大小限制：10KB

## 更新日誌
### v1.0.0 (2024-03-21)
- 初始版本發布
- 實現科別推薦功能
- 整合 Google Maps 位置搜索
