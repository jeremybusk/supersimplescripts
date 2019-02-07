#!/usr/bin/env bash
# Simple script to sync http artifacts to folder and push somewhere.
DST_REPO="repo.example.io:/var/www/html/project/downloads/"
INCOMING_CD_ARTIFACTS_BASE_DIR="/home/inbound/cd/artifacts"

folders=$(find ${INCOMING_CD_ARTIFACTS_BASE_DIR} ! -path ${INCOMING_CD_ARTIFACTS_BASE_DIR} -type d)

for folder in ${folders}; do
    echo $folder
    latest_version=$(ls -t $folder | head -n 1 | grep -o -P "(\ *[0-9]{1,3}\.)[0-9]{1,3}\.[0-9]{1,3}")
    for file in $(find ${folder} -type f -not -name "*${latest_version}*" -not -name "*dontwant*"); do
        echo "Removing old version file ${file}"
        rm ${file}
    done
done


# sync downloads
rsync -avrz --delete --exclude misc -e "ssh -p 22 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" ${INCOMING_CD_ARTIFACTS_BASE_DIR}/* ${DST_REPO}
