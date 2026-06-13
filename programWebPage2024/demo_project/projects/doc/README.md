请帮我用Django 写一个web应用，可以注册Project，管理Project 状态。 

Project 包括如下属性
id,      # int, not null
LoB,     # string 
Site,    # string 
DRI,     # email not null
Creator, # email not null
Description # text
Created_time, # date time
Updated_time, # date time 

Project_Stage 包括如下属性
id, # int not null
project_id, # int not null
Updated_time, # date time
State,  # enumerate [init, data_collection, model_training, under_deployment, control_run_on_production, OK2ML, Pause, Cancelled, Completed]

Project and Project_stage 是 1对多关系。

要求这个Web应用可以注册新的项目，显示所有的项目。

