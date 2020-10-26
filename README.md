# EE4211-Project

## Deadline
- Q1: 25 October 23:59
- Q2: 1 November 23:59
- Q3: 10 November 23:59

## Changelog
- add plot_month to plot monthly value readings by calling function select_data and hourly_data_by_group by Zhang
- add data analyzation in 1.1 by Pan
- set higher display resolution
- add weekly_usage to analyze weekday/weekend usage

To-do: add more analyzation, 1.3 part1 part2

## Discussion
关于Q1， 判断坏掉的主要依据：

1. 读数随着时间的增长反而减少
2. 读数很久没有更新 （可能是wifi的问题，不作为主要的考量依据）
3. 偶现的骤减可以不作为故障
4. 

关于Q2

Q2.1
why you may want to forecast the gas consumption in the future?   
回答：   
In the recently years, gas has begun to be widely used in power generation in both manufacturing and commercial.Accurate prediction of the gas consumpotioin could benefit us on several aspects:   
(1). Energy Saving.Knowing the gas demand could drive us to product the energy sources more efficiently. Unneceaasry waste could be reduced.       
(2). Energy Security.It allows the gas company to prevent and detect if there is any gas leakage during the transporting.      
(3). Urban Planning.The accurate and reasonable prediction of natural gas consumption is significant for the government to formulate the urban planning and infrastructure constructing.       


Who would find this information valuable?    
回答：     
Government, gas user, gas company, gos distribution company,gas production countries and even our environment will benefit from it.     


What can you do if you have a good forecasting model?     
回答：      
With the good forecasting model, we could:     
(1).Cooperate with gas industry to improve the efficiency.     
(2).Propose reasonable gas price according to the demand relation.     
(3).Analyse and improve the transporting security if the leakage happens regularly.      

关于Q3的proposal：     

We may choose one of the following:

1,Find out the malfunctioning meter       
  (a).Base on the decreasing value 
  (b).Base on the stagnant frequency         
     
2,Leakage detection      
  Base on the forecast value, we can set a threshold to determine the possibility of gas leakage.

3,Set a reasonable report reading value.     
  Currently the meter report a reading when the last marginal 2 cubic foot (or higher) of natural gas passes through the meter.     
  We could 
  (a).set a larger meter report reading during peak hour (maybe 4 cubic foot) to reduce the processing and bandwidth requirements.
  (b).ser a smaller mater report reading during off-peak hour (maybe 1 cubic foot). If the meter is keep reporting the     
      reading during the night off-peak hour(especially 11pm to 5am), then there is a possibility of gas leakage.
      
      

## GitHub 101
1. 新成员通过fork dev分支得到一个自己的repo
2. 将自己的repo clone到本地
3. 修改 - git add - git commit - git push：
    - git clone https://github.com/YOUR_NAME/EE4211-Project.git
    - cd EE4211-Project
    - git add .
    - git status
    - git commit -m "Some description here"
    - git push origin main
4. Pull request
   PR到dev分支
5. 关于更新自己已fork的repo：
   https://www.cnblogs.com/hzhhhbb/p/11488861.html

加油💪为了寒假的火锅  嗯嗯~ 吃火锅~


