/* This file contains table definitions for the emc.kb.
 */

create database if not exists parameters;
use parameters;
-- fashej 发射机(设备代码，发射机名称，状态批次代码，位置，工作频率，上边频,下边频，频率点数,频率上限，频率下限，发射带宽，基频功率，调制类型，本振频率，中频，备注)
create table if not exists fashej (
    fashejId integer unsigned not null auto_increment primary key,
    sbdm char(16) not null unique key,
    sbmc varchar(32) not null,
    pcdm char(32)  not null,
    location varchar(32) not null,
    freq float(16,4) not null,
    pd_upper float(16,4) not null,
    pd_lower float(16,4) not null,
    num integer not null,
    freq_upper float(16,4) ,
    freq_lower float(16,4) ,
    bw float not null,
    base_power float(16,4) not null,
    tzlx char(16) not null,
    bzf float(16,4) not null,
    mid_freq float(16,4) not null,
    comment1 varchar(32),
    index fashej_sbdm(sbdm)
) engine=InnoDB DEFAULT CHARSET=utf8;
