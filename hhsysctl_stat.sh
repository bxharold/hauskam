#!/bin/bash
# hsysctl_stat.sh  Only for RPi
#    bash script to report status of hauskam services
#    wifipi_info.py uses this script

hname=$(hostname)
ip=$(hostname -I)
os="$(cat /etc/os-release | head -1 | cut -c13-)"

hsaus=$(systemctl is-enabled hsauskam.service)
hsaus="$hsaus"" / "$(systemctl is-active hsauskam.service)
hsaus="hsauskam.service is : ${hsaus}" ; #echo $hsaus

hvaus=$(systemctl is-enabled hvauskam.service)
hvaus="$hvaus"" / "$(systemctl is-active hvauskam.service)
hvaus="hvauskam.service is : ${hvaus}" ; #echo $hvaus

hcron=$(systemctl is-enabled cron-fake.service)
hcron="$hcron"" / "$(systemctl is-active cron-fake.service)
hcron="cron-fake.service is : ${hcron}" ; #echo $hcron

h5656=$(systemctl is-enabled h5656vauskam.service)
h5656="$h5656"" / "$(systemctl is-active h5656vauskam.service)
h5656="h5656vauskam.service is : ${h5656}" ; #echo $h5656

hpicf=$(systemctl is-enabled hpicfilename.service)
hpicf="$hpicf"" / "$(systemctl is-active hpicfilename.service)
hpicf="hpicfilename.service is : ${hpicf}" ; #echo $hpicf

status=$hname"\n"$ip"\n"$os"\n"$hsaus"\n"$hvaus"\n"$hcron"\n"$h5656"\n"$hpicf"\n"
#echo    "$status"
echo -e "$status"

