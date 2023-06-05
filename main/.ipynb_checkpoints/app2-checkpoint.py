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
    [ '福島県',  37.75,  140.467778,  0]
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
