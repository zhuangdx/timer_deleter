#!/bin/bash
export LANG=en_US.utf8

cur_dir=$(cd `dirname $0`;pwd)
job_cmd_info="\n# 每天凌晨5点运行定时删除工具\n"
job_time="0 5 * * * "
job_cmd="cd ${cur_dir} && PYTHONIOENCODING=utf-8 python3 handle.py > /dev/null 2>&1"

cd ${cur_dir}


if [ `crontab -l | grep "${job_cmd}" |wc -l`  -gt 0 ];then
echo 当前用户已经有cron任务
else
crontab -l > _cron.job
echo 运行命令。添加cron定时任务
echo "$job_cmd_info$job_time$job_cmd"
echo "$job_cmd_info$job_time$job_cmd" >> _cron.job 
crontab _cron.job 
rm -f _cron.job

if [ `crontab -l | grep "${job_cmd}" |wc -l`  -gt 0 ];then
echo 已添加cron任务
fi
fi
