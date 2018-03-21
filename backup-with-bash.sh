#!/usr/env/bin bash
# Ultra simple starter script to backup a host via ssh. Directories and database.
# Requires rsync and rdiff-backup
# Add script for hosts in /etc/cron.daily with backup command
# please copy private/public key in /backup/.ssh/id_rsa and id_rsa.pub 
if [ "$#" -ne 2 ];then
    echo "missing args"
    echo "<hostname/ipaddr> <tcp-port>"
    echo "$0 yourhost.example.com 22"
    exit 1
fi

username="root"
hostname="$1"
ssh_port=$2
app_dir="/backup"
current_dir="${app_dir}/current"
#artifact_dir="${app_dir}/artifacts"
artifact_dir="${current_dir}/${hostname}/artifacts"
time_series_dir="${app_dir}/time_series_backups/"
src_dirs="/var/www/html /etc/nginx"
echo "Begin backup on:" 
echo $hostname
echo $ssh_port
sleep 3
# TODO Add some checking with host and exit on failure to connect. 


if [ ! -d "${current_dir}" ]; then
    mkdir ${current_dir}
fi
if [ ! -d "${artifact_dir}" ]; then
    mkdir ${artifact_dir}
fi
if [ ! -d "${time_series_dir}" ]; then
    mkdir ${time_series_dir}
fi


if [ ! -d "${current_dir}/${hostname}" ]; then
    mkdir -p ${current_dir}/${hostname} 
fi


for src_dir in ${src_dirs}; do
echo $src_dir
rsync -avz --relative --delete -e "ssh -i $app_dir/.ssh/id_rsa -p ${ssh_port} -C -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress ${username}@${hostname}:${src_dir} ${current_dir}/${hostname}/
done
rdiff-backup ${current_dir}/${hostname} ${time_series_dir}/${hostname}

timestamp=$(date "+%Y%m%d%M%H%S")
echo $timestamp
ssh -C -p ${ssh_port} -l root ${hostname} "mysqldump --all-databases | gzip -3 -c" > ${artifact_dir}/all.sql.${timestamp}.gz
