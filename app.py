from flask import Flask, request, jsonify
from api.dify_api import get_recommended_departments
from api.google_maps_api import get_places_for_department
from api.exceptions import APIError, ValidationError

app = Flask(__name__)

# 設置 JSON 編碼
app.config['JSON_AS_ASCII'] = False

@app.route('/api/recommend-departments', methods=['POST'])
def recommend_departments():
    try:
        symptoms = request.json.get('symptoms', [])
        
        # 獲取推薦科別
        departments = get_recommended_departments(symptoms)
        
        # 獲取每個科別的地點資訊
        result = []
        for dept in departments:
            try:
                coordinates = get_places_for_department(dept)
                if coordinates:  # 只有當有符合條件的地點時才加入結果
                    result.append({
                        "name": dept,
                        "coordinates": coordinates
                    })
            except APIError as e:
                # 記錄錯誤但繼續處理其他科別
                print(f"Error processing department {dept}: {str(e)}")
                continue

        if not result:
            return jsonify({"error": "No results found for any department"}), 404

        return jsonify(result)

    except ValidationError as e:
        return jsonify({"error": str(e)}), e.status_code
    except APIError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 