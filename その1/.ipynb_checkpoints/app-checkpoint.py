from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)

candidates = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", 
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", 
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", 
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", 
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", 
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", 
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]
prefectures = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", 
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", 
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", 
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", 
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", 
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", 
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]
votes_per_candidate = {candidate: 0 for candidate in candidates}

@app.route("/")
def index():
    return render_template("index.html", candidates=candidates)


@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        selected_candidate = request.form.get("vote")
        prefecture = request.form.get("prefecture")
        if selected_candidate and prefecture:
            # 投票用のディレクトリを作成する
            if not os.path.exists("votes"):
                os.makedirs("votes")
            
            # 都道府県別の投票結果を保存する
            filename = f"votes/{prefecture}.txt"
            with open(filename, "a") as f:
                f.write(selected_candidate + "\n")
            
            return redirect("/thanks")
    return render_template("vote.html", candidates=candidates, prefectures=prefectures)


@app.route("/results")
def show_results():
    prefecture_results = {}
    for prefecture in prefectures:
        filename = f"votes/{prefecture}.txt"
        if not os.path.exists(filename):
            continue
        
        with open(filename, "r") as f:
            results = f.read().splitlines()
            score_sum = sum(map(int, results))
            prefecture_results[prefecture] = {}
            for candidate, score in zip(candidates, scores):
                count = results.count(candidate)
                prefecture_results[prefecture][candidate] = count * score
    
    return render_template("results.html", prefecture_results=prefecture_results)



if __name__ == "__main__":
    app.run(debug=True)
