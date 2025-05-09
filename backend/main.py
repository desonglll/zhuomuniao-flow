from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
DEEPSEEK_API_URL = os.getenv(
    "DEEPSEEK_API_URL", "http://25.41.34.249:8008/api/ai/qwen/72b/v1"
)
APP_ID = os.getenv("APP_ID", "XXXXX")
SECRET_KEY = os.getenv("SECRET_KEY", "XXXXX")


@app.route("/api/analyze", methods=["POST"])
def analyze_traffic():
    """
    Analyze traffic data by sending it to the Deepseek API
    """
    try:
        # Get data from request
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Prepare the request to Deepseek API
        headers = {
            "Content-Type": "application/json",
            "APP_ID": APP_ID,
            "SECRET_KEY": SECRET_KEY,
        }

        # Construct the payload according to the Deepseek API structure
        payload = {
            "model": "deepseek_r1_dis",
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "你是网络安全专家，擅长分析网络流量日志和检测异常行为。以下是“啄木鸟网络流量分析平台”导出的日志数据，请你从行为模式、端口使用、通信频率、包大小等维度综合判断是否存在异常流量。\n\n"
                        "请按以下要求输出：\n"
                        "1. 是否存在异常行为（如：DDoS、端口扫描、数据泄露、木马通信等）\n"
                        "2. 明确指出异常类型、关联 IP、可疑端口、通信时间段、具体异常行为\n"
                        "3. 最终以结构化表格形式输出，包含如下字段：\n"
                        "| 异常类型 | 源 IP | 目标 IP | 可疑端口 | 时间段 | 简要原因 |\n"
                        "4. 如无异常，也请明确说明“未发现明显异常流量”。\n\n"
                        "以下是用户查询：\n"
                        f"{data.get('query', '请分析以下流量数据')}\n\n"
                        "分析要求：\n"
                        f"{data.get('prompt', '')}\n\n"
                        "流量日志样本数据如下：\n"
                        f"{data.get('sampleTraffic', '')}"
                    )
                }
            ],
            "stop": "<|end__of__sentence|>",
            "stream": False
        }

        print(payload)
        if data.get("query") == "test":
            return jsonify({"result": data.get("query")})

        # Make the request to Deepseek API
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)

        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            return jsonify(result['choices'][0]['message']['content'])
        else:
            return (
                jsonify(
                    {
                        "error": f"API request failed with status code {response.status_code}",
                        "details": response.text,
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
