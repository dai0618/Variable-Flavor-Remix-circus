import threading
import os
import urllib.request

import ssl
import firebase_admin
from firebase_admin import credentials, firestore

from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder
import loopcreator4
import json
import datetime

ssl._create_default_https_context = ssl._create_unverified_context

# firebase
API_KEY = "AIzaSyBaYp3h050YNtdCCKP8v1hKKer2C9CGOSQ"
# firebase init
cred = credentials.Certificate(
    "vfr-for-icc-firebase-adminsdk-ed36f-1aa8ce8fad.json"
)
firebase_admin.initialize_app(cred)
db = firestore.client()

# venue_id, IP, Port
venue_id = "D9AN6WFLYpEdGDVOfSa5"
IP = '127.0.0.1'
MAX_PORT = 7400
OF_PORT = 8000

track_count = 1

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    global track_count
    need_initial_loops = True

    # loading initial 10 songs
    # if need_initial_loops and len(changes) > 8:
    #     track_changes = changes[0:8]
    #     need_initial_loops = False
    # else:
    #     track_changes = changes

    # loading all songs
    track_changes = changes

    # process for each added track
    for change in track_changes:
        if change.type.name == 'ADDED':
            try:
                track = change.document.to_dict()

                track_title = track['title'].replace(" ","")
                track_title = track_title.replace("/","")
                track_id = track['spotify_track_id']
                bpm = track['bpm']
                key = track['key']

                print('-----')
                print(f"title: {track_title}, key: {key} added")


                # check for duplicate preview file
                saved_track = f"{preview_dir}/{track_title}.mp3"
                saved_track_path = "./" + saved_track

                preview_files = os.listdir('tmp/preview_tracks')
                if f"{track_id}.mp3" not in preview_files:
                    # downloading preview_track
                    preview_url = track['preview_url']
                    urllib.request.urlretrieve(preview_url, saved_track_path)

                # create loops from preview track
                output = loopcreator4.create_loop(saved_track_path, track_title, key)

                # download artwork
                artwork_url = track['artwork_url_lg']
                artwork_path = f"{artworks_dir}/{track_title}.jpeg"
                urllib.request.urlretrieve(artwork_url, artwork_path)
                artwork_abs_path = os.path.abspath(artwork_path)

                # saving to json
                track_data = {
                    'title': track_title,
                    'artist': track['artist'],
                    'coverArt': artwork_abs_path,
                    'trackNum': track_count,
                    'key': key
                }

                # track_data_json = json.dumps(track_data)
                json_path = f"{json_dir}/{datetime.datetime.now()}.json"
                print(datetime.datetime.now())
                with open(json_path, 'w') as outfile:
                    json.dump(track_data, outfile, ensure_ascii=False)

                client = udp_client.UDPClient('127.0.0.1', 9999)

                # for stem in ['bass', 'drums', 'other', 'vocals']:
                #     msg = OscMessageBuilder(address=f"/{track_count}/{stem}")
                #     msg.add_arg(f"/Users/dai/Desktop/project/vfr-performance-reciever-main-icc/reciever/tmp/separated_loops_stem/{stem}/{stem}_{track_title}.wav")
                #     m = msg.build()

                #     client.send(m)

                # bpm_msg = OscMessageBuilder(address=f"/{track_count}/bpm")
                # bpm_msg.add_arg(bpm)
                # client.send(bpm_msg.build())

                msg = OscMessageBuilder(address=f"/get_song")
                msg.add_arg(output)
                m = msg.build()

                client.send(m)

                # of_msg = OscMessageBuilder(address="/new_json")  # この数字を1から4でループするで大丈夫ですかね？
                # of_msg.add_arg(os.path.abspath(json_path))
                # of_client.send(of_msg.build())

                # of_track_num_msg = OscMessageBuilder(address='/nextTrackNum')
                # of_track_num_msg.add_arg(track_count)
                # of_client.send(of_track_num_msg.build())

                # # counting numbers of tracks
                # if track_count != 4:
                #     track_count += 1
                # else:
                #     track_count = 1
            except:
                pass

    event.set()


# watch the collection
tracks_ref = db.collection('venues').document(venue_id).collection("tracks")
query_watch = tracks_ref.on_snapshot(on_snapshot)
of_client = udp_client.UDPClient(IP, OF_PORT)

event = threading.Event()

# --- main ---
# root directories
loops_root_dir = './tmp/loops'
separated_loops_root_dir = "./tmp/separated_loops"
wav_preview_dir = './tmp/wav_preview'

artworks_dir = 'tmp/artworks'
json_dir = 'tmp/json'
preview_dir = 'tmp/preview_tracks'

# making directory
os.makedirs(wav_preview_dir, exist_ok=True)
os.makedirs(loops_root_dir, exist_ok=True)
os.makedirs(separated_loops_root_dir, exist_ok=True)
os.makedirs(artworks_dir, exist_ok=True)
os.makedirs(json_dir, exist_ok=True)
os.makedirs(preview_dir, exist_ok=True)


while True:
    print('-----Listening-----')
    event.wait()
    event.clear()
