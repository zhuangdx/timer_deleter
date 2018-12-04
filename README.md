# 本工具用于清理指定文件夹下超过时间的特定类型文件  

文件目录
```
timer_deleter   # 文件夹名   
├── conf        # 配置目录  
    ├──	config.json     # 配置文件-清理指定哪些文件夹下多少天前的什么格式的文件   
    └── log.conf        # 配置文件-logging日志模块配置
├── readme.md           # 说明文档  
├── add_cron_td_job.sh  # 添加cron定时任务脚本  
├── handle.py           # 执行脚本  
└── run.log             # 运行时日志log  
```

# 注意配置
1. 所需环境：    
    * Linux系统   
    * cron环境          （运行 crontab -l 查看是否支持）  
    * python3 以上      （运行 python3 -V 查看版本是否支持）    

2. 因不同的文件的权限不同，定时清理脚本将以root权限运行

3. config.json中规则的格式如下，多个规则用`,`隔开    
    ```
    {   
        "路径": "",   
        "文件类型": "*.log",    
        "过期时间": "7"     
    }     
    ```
    "路径"即是需要清理的文件所在目录；  
    "文件类型"需要清理的文件类型；  如 *.log | * | *.png  
    "过期时间"单位为天，即多少天前的文件 ;
    
	
# 使用说明	
1. 配置config.json文件, 添加规则

2. 根据需要运行不同命令  
    * 第一种是直接运行，清理一次    
    ```shell
    sudo python3 handle.py
    ```
    
    * 第二种，添加cron定时任务，定时清理。当前每天5点运行，如需修改参见cronb文档，add_cron_td_job.sh第6行
    ```shell
    sudo sh add_cron_td_job.sh
    ```

	