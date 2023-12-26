## co2センサー
初期セットアップとして、
NASをdocker volumeにマウントする必要がある

コマンド：
   ```
    docker volume create --driver local --opt type=cifs --opt device=//nas/data --opt o=vers=3.0,username=akihiro,password=${PASSWORD},uid=1000,gid=1000 nas-data
   ```