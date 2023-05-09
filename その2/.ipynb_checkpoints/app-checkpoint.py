from flask import Flask, render_template, request

app = Flask(__name__)

# データを保存するリスト
locations = []

# トップページを表示する
@app.route('/')
def index():
    return render_template('index.html', locations=locations)

# ロケーションを追加する
@app.route('/add_location', methods=['POST'])
def add_location():
    name = request.form['name']
    category = request.form['category']
    locations.append((name, category))
    return '', 204

# ロケーションを削除する
@app.route('/delete_location', methods=['POST'])
def delete_location():
    index = int(request.form['index'])
    if 0 <= index < len(locations):
        locations.pop(index)
    return '', 204

# プランを作成する
@app.route('/create_plan', methods=['POST'])
def create_plan():
    # カテゴリごとにロケーションをグループ化する
    location_dict = {}
    for location in locations:
        name, category = location
        if category not in location_dict:
            location_dict[category] = []
        location_dict[category].append(name)
    return render_template('plan.html', location_dict=location_dict)

if __name__ == '__main__':
    app.run(debug=True)
