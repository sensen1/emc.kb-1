-- Create some test data in the parameters database
-- Note that since the UI logic only shows things in the near future,
-- you may need to run this every few days :)

use parameters;



insert into model (xhdm, xhmc) 
values 
       -- model 
       ('C11', '电信手机');
       
insert into fashej (sbdm, sbmc,pcdm,location,freq,pd_upper,pd_lower,num,freq_upper,
freq_lower,bw,base_power,tzlx,bzf,mid_freq,comment1) 
values 
       -- fashej 
       ('333333002','发射机01','asd2w23sds212211111','m',2.4,0,2.8,10,0,2.8,20,1.1,'AM-V',2,1,' 常用发射机1'),
       ('333333003','发射机03','asd2w23sds212211222','m',2.4,0,2.8,20,0,2.8,30,1.2,'Pulse',2,1,'带滤波'),
       ('111102005','发射机05','asd2w23sds212211223','m',5,5,5,30,5,5,40,1.3,'AM-C',5,2,'高功率'),
       ('111102006','发射机06','asd2w23sds212213554','m',2.4,0,2.8,40,0,2.8,50,1.4,'Pulse',2,1,'常用发射机4'),
       ('111103008','中继通信站','asd2w23sds212216975','m',5,0,8,50,0,8,60,1.5,'FM',5,2,'中频'),
       ('111103009','手机','asd2w23sds218816975','m',1,0,2,60,0,2,70,1.6,'AM-C',1,0.5,'中频'),
       ('333333001','发射机1','asd2w23sds212458175','m',0,0,0,70,0,0,80,1.7,'FM',0,0,'基带');


