#!/bin/bash
LANG=C

/usr/bin/uptime | /bin/sed -e 's/^.*load average.*: //' -e 's/ //g' | /bin/awk -F, "{ printf(\"%f:%f:%f\", \$1, \$2, \$3)}" > /tmp/rrdtool
DATA=`cat /tmp/rrdtool`
#echo $DATA
 
/usr/bin/rrdtool update "/home/m3/dev/rrd/test1_load.rrd" N:$DATA

/usr/bin/rrdtool update "/home/m3/dev/rrd/test1_mem.rrd" N:`free -b |grep cache:|cut -d":" -f2|awk '{print $1 ":" $2}'`

/usr/bin/rrdtool update "/home/m3/dev/rrd/test1_dsk.rrd" N:`df -B 1 |grep /dev/sda2|awk '{print $3 ":" $4}'`


/sbin/pidof m3_gateway > /tmp/gateway_pid
/sbin/pidof m3_room > /tmp/room_pid
/sbin/pidof m3_stage1 > /tmp/stage1_pid
/sbin/pidof m3_stage2 > /tmp/stage2_pid
/sbin/pidof m3_stage3 > /tmp/stage3_pid
/sbin/pidof m3_stage4 > /tmp/stage4_pid

GATEWAY_PID=`cat /tmp/gateway_pid`
ROOM_PID=`cat /tmp/room_pid`
STAGE1_PID=`cat /tmp/stage1_pid`
STAGE2_PID=`cat /tmp/stage2_pid`
STAGE3_PID=`cat /tmp/stage3_pid`
STAGE4_PID=`cat /tmp/stage4_pid`

cat /proc/$GATEWAY_PID/status | grep VmRSS: | cut -d ":" -f2 | awk '{print $1}' > /tmp/gateway_mem
cat /proc/$ROOM_PID/status | grep VmRSS: | cut -d ":" -f2 | awk '{print $1}' > /tmp/room_mem
cat /proc/$STAGE1_PID/status | grep VmRSS: | cut -d ":" -f2 | awk '{print $1}' > /tmp/stage1_mem
cat /proc/$STAGE2_PID/status | grep VmRSS: | cut -d ":" -f2 | awk '{print $1}' > /tmp/stage2_mem
cat /proc/$STAGE3_PID/status | grep VmRSS: | cut -d ":" -f2 | awk '{print $1}' > /tmp/stage3_mem
cat /proc/$STAGE4_PID/status | grep VmRSS: | cut -d ":" -f2 | awk '{print $1}' > /tmp/stage4_mem

GATEWAY_MEMORY=`cat /tmp/gateway_mem`
ROOM_MEMORY=`cat /tmp/room_mem`
STAGE1_MEMORY=`cat /tmp/stage1_mem`
STAGE2_MEMORY=`cat /tmp/stage2_mem`
STAGE3_MEMORY=`cat /tmp/stage3_mem`
STAGE4_MEMORY=`cat /tmp/stage4_mem`

echo $GATEWAY_MEMORY
echo $ROOM_MEMORY
echo $STAGE1_MEMORY
echo $STAGE2_MEMORY
echo $STAGE3_MEMORY
echo $STAGE4_MEMORY

/usr/bin/rrdtool update "/home/m3/dev/rrd/test1_process.rrd" N:$GATEWAY_MEMORY:$ROOM_MEMORY:$STAGE1_MEMORY:$STAGE2_MEMORY:$STAGE3_MEMORY:$STAGE4_MEMORY
