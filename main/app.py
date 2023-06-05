from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import folium
from folium.plugins import MarkerCluster
from branca.colormap import linear

app = Flask(__name__)

# セッションの設定
app.config['SECRET_KEY'] = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# 都道府県の情報
prefectures=[
    [ '北海道',  43.064167,  141.346944,  0],
    [ '青森県',  40.824444,  140.74,  0],
    [ '岩手県',  39.703611,  141.1525,  0],
    [ '宮城県',  38.268889,  140.871944,  0],
    [ '秋田県',  39.718611,  140.1025,  0],
    [ '山形県',  38.240556,  140.363333,  0],
    [ '福島県',  37.75,  140.467778,  0],
    [ '茨城県',  36.341389,  140.446667,  0],
    [ '栃木県',  36.565833,  139.883611,  0],
    [ '群馬県',  36.391111,  139.060833,  0],
    [ '埼玉県',  35.856944,  139.648889,  0],
    [ '千葉県',  35.604722,  140.123333,  0],
    [ '東京都',  35.689444,  139.691667,  0],
    [ '神奈川県',  35.447778,  139.6425,  0],
    [ '新潟県',  37.902222,  139.023611,  0],
    [ '富山県',  36.695278,  137.211389,  0],
    [ '石川県',  36.594444,  136.625556,  0],
    [ '福井県',  36.065278,  136.221944,  0],
    [ '山梨県',  35.663889,  138.568333,  0],
    [ '長野県',  36.651389,  138.181111,  0],
    [ '岐阜県',  35.391111,  136.722222,  0],
    [ '静岡県',  34.976944,  138.383056,  0],
    [ '愛知県',  35.180278,  136.906389,  0],
    [ '三重県',  34.730278,  136.508611,  0],
    [ '滋賀県',  35.004444,  135.868333,  0],
    [ '京都府',  35.021389,  135.755556,  0],
    [ '大阪府',  34.686389,  135.52,  0],
    [ '兵庫県',  34.691389,  135.183056,  0],
    [ '奈良県',  34.685278,  135.832778,  0],
    [ '和歌山県',  34.226111,  135.1675,  0],
    [ '鳥取県',  35.503611,  134.238333,  0],
    [ '島根県',  35.472222,  133.050556,  0],
    [ '岡山県',  34.661667,  133.935,  0],
    [ '広島県',  34.396389,  132.459444,  0],
    [ '山口県',  34.185833,  131.471389,  0],
    [ '徳島県',  34.065833,  134.559444,  0],
    [ '香川県',  34.340278,  134.043333,  0],
    [ '愛媛県',  33.841667,  132.766111,  0],
    [ '高知県',  33.559722,  133.531111,  0],
    [ '福岡県',  33.606389,  130.418056,  0],
    [ '佐賀県',  33.249722,  130.298889,  0],
    [ '長崎県', 32.744722, 129.873611, 0],
    [ '熊本県',  32.789722,  130.741667,  0],
    [ '大分県',  33.238056,  131.6125,  0],
    [ '宮崎県',  31.911111,  131.423889,  0],
    [ '鹿児島県',  31.560278,  130.558056,  0],
    [ '沖縄県',  26.2125,  127.681111,  0]
]

@app.route('/')
def index():
    return redirect(url_for('login'))

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('vote'))
    return render_template('login.html')

#投票ページ
@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        for place in prefectures:
            place[3] += int(request.form.get(place[0], 0))
        session['voted'] = True
        # 投票が完了したら、resultページにリダイレクトする
        return redirect(url_for('result'))
    return render_template('vote.html', prefectures=prefectures)

# 結果ページ
@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'voted' not in session:
        return redirect(url_for('vote'))
    for place in prefectures:
        place[3] += int(request.form.get(place[0], 0))
    place_scores = [prefectures[i][3] for i in range(len(prefectures))]
    sort_place=sorted(prefectures, key = lambda x:x[3], reverse = True)
    sort_place=[(i, place) for i, place in enumerate(sort_place)]
    
    # 地図に反映
    kanto_lat = 36.2048
    kanto_lon = 138.2529
    colormap = linear.YlOrRd_09.scale(1, max(place_scores))
    map_japan = folium.Map(location=[kanto_lat, kanto_lon], zoom_start=5)

    for place in prefectures:    
        if place[3]<=0:
            pass
        else:
            folium.Marker(
                location=[place[1], place[2]],
                tooltip=place[0] + ': ' + str(place[3]) + '点',
                icon=folium.Icon(icon='flag', color="blue", icon_color=colormap(place[3])),
            ).add_to(map_japan)

    return render_template('result.html', sort_place=sort_place, map=map_japan._repr_html_())

    
if __name__ == '__main__':
    app.run(debug=True)
