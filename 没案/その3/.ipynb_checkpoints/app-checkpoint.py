from flask import Flask, render_template, request
import folium
from folium.plugins import MarkerCluster
from branca.colormap import linear

app = Flask(__name__)

kanto_places = ['東京都', '神奈川県', '埼玉県', '千葉県', '茨城県', '栃木県', '群馬県']

vote_results = [0] * len(kanto_places)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    
    for i, place in enumerate(kanto_places):
        vote_results[i] = vote_results[i] + int(request.form.get(place, 0))

    total_votes = sum(vote_results)
    if total_votes == 0:
        return "誰も投票していません"

    place_scores = [vote_results[i]/total_votes for i in range(len(kanto_places))]
    max_score_index = place_scores.index(max(place_scores))
    chosen_place = kanto_places[max_score_index]

    # 地図に反映
    kanto_lat = 36.2048
    kanto_lon = 138.2529
    colormap = linear.YlOrRd_09.scale(min(vote_results), max(vote_results))
    map_kanto = folium.Map(location=[kanto_lat, kanto_lon], zoom_start=8)

    for i, place in enumerate(kanto_places):    
        if vote_results[i]<0:
            pass
        else:
            folium.Marker(
                location=[get_lat(place), get_lon(place)],
                tooltip=place + ': ' + str(vote_results[i]) + '票',
                icon=folium.Icon(icon='flag', color="blue", icon_color=colormap(vote_results[i])),
            ).add_to(map_kanto)

    return render_template('result.html', chosen_place=chosen_place, map=map_kanto._repr_html_())

def get_lat(place):
    if place == '東京都':
        return 35.6762
    elif place == '神奈川県':
        return 35.4478
    elif place == '埼玉県':
        return 36.1447
    elif place == '千葉県':
        return 35.6073
    elif place == '茨城県':
        return 36.3418
    elif place == '栃木県':
        return 36.5658
    elif place == '群馬県':
        return 36.3912
    else:
        return None

def get_lon(place):
    if place == '東京都':
        return 139.6503
    elif place == '神奈川県':
        return 139.6425
    elif place == '埼玉県':
        return 139.3831
    elif place == '千葉県':
        return 140.2100
    elif place == '茨城県':
        return 140.4468
    elif place == '栃木県':
        return 139.8836
    elif place == '群馬県':
        return 139.0600
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
