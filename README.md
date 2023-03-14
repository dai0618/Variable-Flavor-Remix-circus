# Reciever 

reciever.pyを実行

| address              | from             | to               | content       | memo                             | 
| :------------------: | :--------------: | :--------------: | :-----------: | :------------------------------: | 
| /loop_path           | receiver         | state controller | strings       | ループ抽出された曲の名前         | 
| /select_loops/{1-12} | state controller | max              | file abs path | ループ抽出された曲のファイルパス | 
| /selected_loops      | max              | state controller | int           | 1-12                             | 
| /cover_art           | M4L              | Visual           | url           | カバーアートダウンロードのurl    | 
