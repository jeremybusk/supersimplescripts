#!/usr/bin/env bash
set -e
if [[ -z $1 ]]; then
  echo "Usage: $0 <username for nopass sudo>"
  echo "ssh <myhost> "bash -s" -- < ./$0"
  exit 1
else
  username=$1
fi

if [[ -z $2 ]]; then
  userpass=$(openssl passwd -6 -salt xyz $username)
else
  userpass=$(openssl passwd -6 -salt xyz $2)
fi

userdel -rf $username || echo "skip"
useradd -c "Test User" -p $userpass $username -s /bin/bash -m -d /home/$username
echo "$username     ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$username
sudo -u $username -- sudo whoami
echo "Finish"
# ssh sandbox1 "bash -s" -- < ./uadd




# echo "username:password" | chpasswd
# https://unix.stackexchange.com/questions/81240/manually-generate-password-for-etc-shadow
# echo "username:encryptedPassWd" | chpasswd -e
# mkpasswd --method=SHA-512 --stdin
