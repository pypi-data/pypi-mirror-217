#!/bin/bash

# 获取所有进程的CPU使用情况和进程用户
cpu_usage=$(ps -e -o pid,comm,user,%cpu --no-headers | awk '{ print "cpu_usage{process_name=" $2 ",user=" $3 "} " $4 }')

# 获取所有进程的内存使用情况和进程用户
mem_usage=$(ps -e -o pid,comm,user,%mem --no-headers | awk '{ print "mem_usage{process_name=" $2 ",user=" $3 "} " $4 }')

# 将结果输出为Prometheus格式
echo -e "$cpu_usage\n$mem_usage"
