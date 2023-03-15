# Reciever 

## 概要
Variable Flavor Remixのパフォーマンス用リポジトリ

## 実行
```python
reciever.pyを実行
```

## OSC

| server           | port | ip        |
| :--------------: | :--: | :-------: |
| state controller | 9999 | 127.0.0.1 |
| max              | 8888 | 127.0.0.1 |
| Visual           | 6666 | 127.0.0.1 |

| address                | from             | to               | content       | memo                             | 
| :--------------------: | :--------------: | :--------------: | :-----------: | :------------------------------: | 
| /loop_path             | receiver         | state controller | strings       | ループ抽出された曲の名前         | 
| /select_loops/{1-12}   | state controller | max              | file abs path | ループ抽出された曲のファイルパス | 
| /select_artwork/{1-12} | state controller | max              | file abs path | カバーアートのファイルパス | 
| /select_title/{1-12}   | state controller | max              | string        | ループ抽出された曲のタイトル | 
| /selected_loops        | max              | state controller | int           | 1-12  | 
| /track_move            | M4L              | state controller | strings       | 曲のタイトル | 
| /cover_art             | state controller | visual           | file abs path | カバーアートのファイルパス |
