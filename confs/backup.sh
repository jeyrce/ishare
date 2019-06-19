#!/usr/bin/env bash

#useradd -m backup
#passwd backup # 回车
#
#chown -R backup /home/backup
#
#vim /etc/ssh/ssh_config # 放开下面两行注释
#
#RSAAuthentication yes
#PubkeyAuthentication yes
#
#ssh-copy-id <另一个主机的backup用户>@主机ip或域名


source /root/venvs/ljx/bin/activate

cd /root/apps/ljx

d=`date +%y%m%d`

tar_name='ljx-'${d}'.tar.gz'

tar -cvzf ${tar_name} ./media ./db.sqlite3

mv ${tar_name} /tmp

scp /tmp/${tar_name} backup@120.78.239.198:/home/backup

echo tar_name > /tmp/backup.log

exit 0

