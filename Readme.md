## co2センサー
初期セットアップとして、
NASをdocker volumeにマウントする必要がある

コマンド：
   ```
 docker volume create --driver local --opt type=cifs --opt device=//192.168.0.61/main/raspi/co2monitor --opt o=vers=3.0,username=akihiro,password=${PASSWORD},uid=1000,gid=1000 nas-co2
   ```