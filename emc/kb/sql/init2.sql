create database if not exists parameters;
use parameters;
-- Model型号信息(型号代码，型号名称)
create table if not exists model (
    modelId integer unsigned not null auto_increment primary key,
    xhdm char(8) not null unique key,
    xhmc varchar(32) not null,
    index model_xhdm(xhdm)
) engine=InnoDB DEFAULT CHARSET=utf8;
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

-- fashetx 发射天线(丛属设备代码，发射天线名称，状态批次代码，位置，增益，极化，方位波速带宽，俯仰波速带宽，天线指向角)
create table if not exists fashetx (
    fashetxId integer unsigned not null auto_increment primary key,
    cssbdm char(16) not null unique key,
    cssbmc varchar(32) not null,
    pcdm char(32) not null,
    location varchar(32) not null,
    gain float(16,4) not null,
    polarization char(16) not null,
    fwbskd float(16,4) not null,
    fybskd float(16,4) not null,
    txzxj float(16,4) not null,
    index fashetx_cssbdm(cssbdm)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- jieshouj 接收机(设备代码，接收机名称，状态批次代码,位置，频段上限，频段下限，工作频率，上边频,下边频,接收机带宽，接收机灵敏度，中频符号，中频频率，本振频率)
create table if not exists jieshouj (
    jieshoujId integer unsigned not null auto_increment primary key,
    sbdm char(16) not null unique key,
    sbmc varchar(32) not null,
    pcdm char(32) not null,
    location varchar(32) not null,
    fb_upper float(16,4) not null,
    fb_lower float(16,4) not null,
    freq float(16,4),
    f_upper float(16,4),
    f_lower float(16,4),
    bw_receiver float(16,4) not null,
    sen_receiver float(16,4) not null,
    mf_freq_sign varchar(16) not null,
    mf_freq float(16,4) not null,
    lo_freq float(16,4) not null,
    index jieshouj_sbdm(sbdm)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- jieshoutx 接收天线(丛属设备代码，接收天线名称，状态批次代码，位置,增益，极化，方位波束宽度，俯仰波束宽度， 天线指向角)
create table if not exists jieshoutx (
    jieshoutxId integer unsigned not null auto_increment primary key,
    cssbdm char(16) not null unique key,
    cssbmc varchar(32) not null,
    pcdm char(32) not null,
    location varchar(32) not null,
    gain float(16,4) not null,
    polarization char(16) not null,
    fwbskd float(9,4) not null,
    fybskd float(9,4) not null,
    txzxj float(9,4) not null,
    index jieshoutx_cssbdm(cssbdm)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- lvboq滤波器(从属设备代码，滤波器名称，状态批次代码，位置，工作频率，上边频，下边频，滤波器级数，滤波器插损)
create table if not exists lvboq (
    lvboqId integer unsigned not null auto_increment primary key,
    cssbdm char(16) not null unique key,
    cssbmc varchar(32) not null,
    pcdm char(32) not null,
    location varchar(32) not null,
    -- fb_upper float(16,4) not null,
    -- fb_lower float(16,4) not null,
    freq float(16,4),
    f_upper float(16,4),
    f_lower float(16,4),
    order1 float(16,4) not null,
    s21 float(16,4) not null,
    index lvboq_cssbdm(cssbdm)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- dianxingtxzyzk 典型天线增益子库(天线类型，增益)
create table if not exists dianxingtxzyzk (
    dianxingtxzyzkId integer unsigned not null auto_increment primary key,
    type_antennas char(30) not null unique key,
    gain integer not null,
    index dianxingtxzyzk_type_antennas(type_antennas)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- tianxianzk 天线子库(子库代码，子库名)
create table if not exists tianxianzk (
    tianxianzkId integer unsigned not null auto_increment primary key,
    lib_code char(16) not null unique key,
    lib_name varchar(32) not null,
    index tianxianzk_lib_code(lib_code)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- jieshoujzk 接收机子库(子库代码，子库名)
create table if not exists jieshoujzk (
    dianxingtxzyzkId integer unsigned not null auto_increment primary key,
    lib_code char(16) not null unique key,
    lib_name varchar(32) not null,
    index jieshoujzk_lib_code(lib_code)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- fashejzk发射机子库(子库代码，子库名)
create table if not exists fashejzk (
    fashejzkId integer unsigned not null auto_increment primary key,
    lib_code char(16) not null unique key,
    lib_name varchar(32) not null,
    index fashejzk_lib_code(lib_code)
) engine=InnoDB DEFAULT CHARSET=utf8;
-- ceshishysh测试实验室(名称，单位，级别，概况)
create table if not exists ceshishysh (
    ceshishyshId integer unsigned not null auto_increment primary key,
    name char(32) not null unique key,
    unit varchar(32) not null,
    level1 char(16) not null,
    survey varchar(32) not null,
    index ceshishysh_name(name)
) engine=InnoDB DEFAULT CHARSET=utf8;
-- ceshiry测试人员(姓名，性别，年龄，学历，职称，证书编号，单位)
create table if not exists ceshiry (
    ceshishyshId integer unsigned not null auto_increment primary key,
    name char(16) not null,
    sex char(2) not null,
    age integer not null,
    edu_level char(8) not null,
    post char(16) not null,
    certificate_code char(16) not null unique key,
    unit varchar(32) not null,
    index ceshiry_name(name,certificate_code)
) engine=InnoDB DEFAULT CHARSET=utf8;
-- ceshiff测试方法(方法编号，方法标题，适用范围，仪器设备，测试框图，测试步骤，附注)
create table if not exists ceshiff (
    ceshiffId integer unsigned not null auto_increment primary key,
    m_id char(16) not null unique key,
    m_title char(32) not null,
    range1 varchar(16) not null,
    device varchar(16) not null,
    diagram char(16) not null,
    step varchar(16) not null,
    annotation varchar(32) not null,
    index ceshiff(m_id)
) engine=InnoDB DEFAULT CHARSET=utf8;
-- ceshibg测试报告(测试证书编号，委托方，委托方地址，被测件，EUT编号，EUT型号，制造商，测试日期，
-- 测试地点，测试设备，测试设备型号，测试设备编号，测试依据，温度，湿度，测试人员，签发人，审核人，测试结果)
create table if not exists ceshibg (
    ceshibgId integer unsigned not null auto_increment primary key,
    t_id char(16) not null unique key,
    bailor char(32) not null,
    address varchar(32) not null,
    device varchar(32) not null,
    eut_id char(16) not null,
    eut_type char(16) not null,
    manufacturor varchar(32) not null,
    t_date  date not null,
    t_address varchar(32) not null,
    t_device varchar(32) not null,
    t_device_type char(16) not null,
    t_device_id char(16) not null,
    reference varchar(16) not null,
    temp float(3,1) not null,
    huminitily float(2,1) not null,
    t_man char(10) not null,
    signer char(10) not null,
    assessor char(10) not null,
    t_result varchar(32) not null,
    index ceshibg(t_id)
) engine=InnoDB DEFAULT CHARSET=utf8;
-- ceshixm 测试项目 （被测件，项目名称，示意图，测试说明，测试仪器，测试数据，测试结果）
create table if not exists ceshixm (
    ceshixmId integer unsigned not null auto_increment primary key,
    project_id integer unsigned not null unique key,
    device char(32) not null,
    name char(32)  not null,
    diagram varchar(32)  not null,
    t_remark varchar(16) not null,
    t_strument varchar(16) not null,
    t_value  varchar(64) not null,
    t_result varchar(16) not null,
    index (project_id)
) engine=InnoDB DEFAULT CHARSET=utf8;
