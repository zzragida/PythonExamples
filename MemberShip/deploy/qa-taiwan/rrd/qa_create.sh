#!/bin/bash
LANG=C

if [ ! -f "/neowiz/msh/rrd/QA5_load.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/QA5_load.rrd" \
		--step 60 \
		"DS:1min:GAUGE:600:0:U" \
		"DS:5min:GAUGE:600:0:U" \
		"DS:15min:GAUGE:600:0:U" \
		"RRA:LAST:0.5:1:144000" \
		"RRA:MAX:0.5:60:12"
fi


if [ ! -f "/neowiz/msh/rrd/QA5_mem.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/QA5_mem.rrd" \
        --step 60 \
        "DS:usage:GAUGE:600:0:U" \
        "DS:free:GAUGE:600:0:U" \
        "RRA:LAST:0.5:1:144000" \
        "RRA:MAX:0.5:60:12"
fi

if [ ! -f "/neowiz/msh/rrd/QA5_dsk.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/QA5_dsk.rrd" \
        --step 60 \
        "DS:usage:GAUGE:600:0:U" \
        "DS:free:GAUGE:600:0:U" \
        "RRA:LAST:0.5:1:144000" \
        "RRA:MAX:0.5:60:12"
fi

if [ ! -f "/neowiz/msh/rrd/QA5_redis.rrd" ]; then
/usr/bin/rrdtool create "/neowiz/msh/rrd/QA5_redis.rrd" \
        --step 60 \
        "DS:used_memory:GAUGE:600:0:U" \
        "RRA:LAST:0.5:1:144000" \
        "RRA:MAX:0.5:60:12"
fi
