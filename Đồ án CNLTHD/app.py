from flask import Flask, render_template, request
import requests
import pyodbc
import re

app = Flask(__name__)

# Kết nối SQL Server
def connect_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=YONORIKOMANA\\QUOCDUONG;'
        'DATABASE=test;'
        'UID=sa;PWD=1234;Encrypt=no'
    )
    return conn

# Tách câu SQL đầu tiên từ phản hồi Ollama
def extract_sql_from_response(response_text):
    sql_pattern = r"(SELECT|INSERT|UPDATE|DELETE|WITH)[\s\S]+?;"
    match = re.search(sql_pattern, response_text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    else:
        raise Exception("\u274c Kh\u00f4ng t\u00ecm th\u1ea5y c\u00e2u SQL trong ph\u1ea3n h\u1ed3i:\n" + response_text)

# Gọi mô hình Ollama (local)
import re

def call_ollama(prompt):
    url = 'http://localhost:11434/api/generate'
    payload = {
        "model": "sqlcoder",  # hoặc llama3 nếu bạn tinh chỉnh
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    full_response = response.json()["response"]

    # 🧠 Sử dụng regex để tìm đoạn SQL (chỉ lấy phần đầu tiên có dạng SQL)
    match = re.search(r"(SELECT|INSERT|UPDATE|DELETE|WITH)\s.+", full_response, re.IGNORECASE | re.DOTALL)
    if not match:
        raise Exception("❌ Không tìm thấy câu SQL trong phản hồi: \n" + full_response)

    sql = match.group(0).strip()

    return sql


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    sql_query = None
    error = None

    if request.method == "POST":
        user_question = request.form.get("question", "")

        try:
            # B1: Tạo prompt
            prompt = f"""
            You are an expert in SQL Server. Convert the following question into a valid SQL Server query.

            Use this table: SanPham(id, ten, mo_ta, gia, so_luong_ton, danh_muc_id, ngay_tao, trang_thai).
            Return only the SQL, no explanation, no extra characters.

            Question: {user_question}
            """


            sql_query = call_ollama(prompt)

            # ✅ Sửa câu SQL nếu có LIMIT hoặc NULLS LAST
            if "LIMIT" in sql_query.upper():
                try:
                    limit_value = int(sql_query.split("LIMIT")[-1].strip('; ').strip())
                    sql_query = sql_query.replace("NULLS LAST", "")
                    sql_query = sql_query.split("LIMIT")[0].strip()
                    sql_query += f" OFFSET 0 ROWS FETCH NEXT {limit_value} ROWS ONLY"
                except:
                    pass

            # B2: Kết nối DB và thực thi SQL
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]

        except Exception as e:
            error = str(e)

    return render_template("index.html", result=result, sql=sql_query, error=error)

if __name__ == '__main__':
    app.run(debug=True)
