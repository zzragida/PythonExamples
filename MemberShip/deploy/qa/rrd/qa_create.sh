#!/bin/bash
LANG=C

if [ ! -f "/neowiz/msh/rrd/mox623_load.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/mox623_load.rrd" \
		--step 60 \
		"DS:1min:GAUGE:600:0:U" \
		"DS:5min:GAUGE:600:0:U" \
		"DS:15min:GAUGE:600:0:U" \
		"RRA:LAST:0.5:1:144000" \
		"RRA:MAX:0.5:60:12"
fi


if [ ! -f "/neowiz/msh/rrd/mox623_gateway.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/mox623_gateway.rrd" \
		--step 60 \
		"DS:ActiveUser:GAUGE:600:0:U" \
	  "DS:InputPacket:GAUGE:600:0:U" \
		"DS:OutputPacket:GAUGE:600:0:U" \
		"DS:MaxResponseTime:GAUGE:600:0:U" \
		"DS:AverageResponseTime:GAUGE:600:0:U" \
		"DS:RedisCommand:GAUGE:600:0:U" \
		"DS:SqlQuery:GAUGE:600:0:U" \
		"DS:SingleGame:GAUGE:600:0:U" \
		"DS:MultiGame:GAUGE:600:0:U" \
		"DS:EnterUser:GAUGE:600:0:U" \
		"DS:ExitUser:GAUGE:600:0:U" \
		"RRA:LAST:0.5:1:144000" \
		"RRA:MAX:0.5:60:12"
fi


if [ ! -f "/neowiz/msh/rrd/mox623_room.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/mox623_room.rrd" \
		--step 60 \
		"DS:TotalRoom:GAUGE:600:0:U" \
		"DS:InputPacket:GAUGE:600:0:U" \
		"DS:OutputPacket:GAUGE:600:0:U" \
		"DS:GameRoom:GAUGE:600:0:U" \
		"DS:WaitingRoom:GAUGE:600:0:U" \
		"DS:RedisCommand:GAUGE:600:0:U" \
		"DS:SqlQuery:GAUGE:600:0:U" \
		"RRA:LAST:0.5:1:144000" \
		"RRA:MAX:0.5:60:12"
fi


  for PROCESS in "stage1" "stage2" "stage3" "stage4"
  do
    if [ ! -f "/neowiz/msh/rrd/mox623_"$PROCESS".rrd" ]; then
    /usr/bin/rrdtool create "/neowiz/msh/rrd/mox623_"$PROCESS".rrd" \
        --step 60 \
        "DS:Game:GAUGE:600:0:U" \
        "DS:Play:GAUGE:600:0:U" \
        "DS:User:GAUGE:600:0:U" \
        "DS:Object:GAUGE:600:0:U" \
        "DS:Component:GAUGE:600:0:U" \
        "DS:FPS:GAUGE:600:0:U" \
        "DS:BytesSent:GAUGE:600:0:U" \
        "DS:BytesRecv:GAUGE:600:0:U" \
        "RRA:LAST:0.5:1:144000" \
        "RRA:MAX:0.5:60:12"
    fi
  done


if [ ! -f "/neowiz/msh/rrd/mox623_mem.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/mox623_mem.rrd" \
        --step 60 \
        "DS:usage:GAUGE:600:0:U" \
        "DS:free:GAUGE:600:0:U" \
        "RRA:LAST:0.5:1:144000" \
        "RRA:MAX:0.5:60:12"
fi

if [ ! -f "/neowiz/msh/rrd/mox623_dsk.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/mox623_dsk.rrd" \
        --step 60 \
        "DS:usage:GAUGE:600:0:U" \
        "DS:free:GAUGE:600:0:U" \
        "RRA:LAST:0.5:1:144000" \
        "RRA:MAX:0.5:60:12"
fi

if [ ! -f "/neowiz/msh/rrd/mox623_redis.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/mox623_redis.rrd" \
        --step 60 \
        "DS:used_memory:GAUGE:600:0:U" \
        "RRA:LAST:0.5:1:144000" \
        "RRA:MAX:0.5:60:12"
fi

if [ ! -f "/neowiz/msh/rrd/mox623_process.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/mox623_process.rrd" \
        --step 60 \
        "DS:gateway:GAUGE:600:0:U" \
        "DS:room:GAUGE:600:0:U" \
        "DS:stage1:GAUGE:600:0:U" \
        "DS:stage2:GAUGE:600:0:U" \
        "DS:stage3:GAUGE:600:0:U" \
        "DS:stage4:GAUGE:600:0:U" \
        "RRA:LAST:0.5:1:144000" \
        "RRA:MAX:0.5:60:12"
fi
