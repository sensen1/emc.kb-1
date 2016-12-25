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

-- fashetx 发射天线(丛属设备代码，发射天线名称，状态批次代码，位置，增益，极化，方位波速带宽，俯仰波速带宽，天线指向角)
create table if not exists fashetx (
    fashetxId integer unsigned not null auto_increment primary key,
    cssbdm char(16) not null unique key,
    cssbmc varchar(32) not null,
    pcdm char(32) not null,
    location varchar(32) not null,
    gain float(16,4) not null,
    polarization float(16,4) not null,
    fwbskd float(16,4) not null,
    fybskd float(16,4) not null,
    txzxj float(16,4) not null
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
    polarization float(16,4) not null,
    fwbskd float(9,4) not null,
    fybskd float(9,4) not null,
    txzxj float(9,4) not null
    index jieshoutx_cssbdm(cssbdm)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- lvboq滤波器(从属设备代码，滤波器名称，状态批次代码，位置，工作频率，上边频，下边频，滤波器级数，滤波器插损)
create table if not exists lvboq (
    lvboqId integer unsigned not null auto_increment primary key,
    cssbdm char(16) not null unique key,
    cssbmc varchar(32) not null,
    pcdm char(32) not null,
    location varchar(32) not null,
    fb_upper float(16,4) not null,
    fb_lower float(16,4) not null,
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
    range varchar(16) not null,
    device varchar(16) not null,
    diagram char(16) not null,
    step varchar(16) not null,
    annotation varchar(32) not null,
    index ceshiff(m_id,m_title)
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
    t_value  varchar(16) not null,
    t_result varchar(16) not null,
    index ceshixm_device(device)
) engine=InnoDB DEFAULT CHARSET=utf8;
-- cixingcljbcsh 磁性材料基本参数（工作频率，初始磁导率，居里温度，比重，损耗因子，初始磁导率的温度系数）
create table if not exists cixingcljbcsh (
    cixingcljbcshId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    gongzuopl float(16,4) not null,
    chushicdl float(10,2) not null,
    juliwd float(10,2) not null,
    bizhong float(10,2)  not null,
    sunhaoyz float(10,2) not null,
    chushicdlwdxsh float(10,2) not null,
    index cixingcljbcsh(cailiao_id)
) engine=InnoDB DEFAULT CHARSET=utf8;
-- emixishouch EMI吸收磁环 （外径，内经，长度）
create table if not exists emixishouch (
    emixishouchId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    waijing float(10,2)  not null,
    neijing float(10,2  not null,
    changdu float(10,2) not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- emixishouczh EMI吸收磁珠 （阻抗-频率响应，材料，规格，外径，内径，长度）
create table if not exists emixishouczh (
    emixishouczhId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    zukang float(10,2) not null,
    cailiao varchar(32) not null,
    guige float(10,2) not null,
    waijing float(10,2)  not null,
    neijing float(10,2  not null,
    changdu float(10,2) not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- pingbitfch 屏蔽通风窗 （屏蔽效能，材料）
create table if not exists pingbitfch (
    emixishouchId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    pingbixn float(10,2)  not null,
    cailiao float(10,2  not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- pingbitfb 屏蔽通风板 （屏蔽效能，温度特性）
create table if not exists pingbitfb (
    pingbitfbId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    pingbixn float(10,2)  not null,
    wendutx float(10,2  not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- pingbibl屏蔽玻璃 （屏蔽效能，透光率，工作温度）
create table if not exists pingbitfb (
    pingbitfbId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    pingbixn float(10,2)  not null,
    touguangl float(10,2)  not null,
    gongzuowd float(10,2)  not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- cichangpbcl 磁场屏蔽材料 （最大磁导率，电阻率，最低工作温度，20℃时热导率，弹性系数，膨胀系数）
create table if not exists cichangpbcl (
    cichangpbclId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    zuodacdl float(10,2)  not null,
    dianzul float(10,2)  not null,
    zuidigzwd float(10,2)  not null,
    redaol float(10,2)  not null,
    tanxingxsh float(10,2)  not null,
    pengzhangxsh float(10,2)  not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- jinshuswpbt 金属丝网屏蔽条 （H场（14KHZ），电场（10KHZ），平面波（1GHZ），额定电压，高压测试，绝缘阻抗）
create table if not exists jinshuswpbt (
    jinshuswpbtId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    hchang float(10,2)  not null,
    dianchang float(10,2)  not null,
    pingmianb float(10,2)  not null,
    edingdy float(10,2)  not null,
    gaoyacsh float(10,2)  not null,
    jueyuanzk float(10,2)  not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- fangleilbzj 防雷滤波组件 （型号，电容值，额定电流，放电电流，额定电压，钳位电压，温度特性）
create table if not exists jinshuswpbt (
    jinshuswpbtId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    xinghao char(10)  not null,
    dianrongzh float(10,2)  not null,
    edingdl float(10,2)  not null,
    fangdiandl float(10,2)  not null,
    edingdy float(10,2)  not null,
    qianweidy float(10,2)  not null,
    wendutex float(10,2)  not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- emipianzhuanglbq EMI片状滤波器 （型号，电容值，额定电流，额定电压，插入损耗，温度特性）
create table if not exists emipianzhuanglbq (
    jinshuswpbtId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    xinghao char(10)  not null,
    dianrongzh float(10,2)  not null,
    edingdl float(10,2)  not null,
    edingdy float(10,2)  not null,
    charush float(10,2)  not null,
    wendutex float(10,2)  not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
-- daodiantl 导电涂料 （屏蔽效能，表面接触电阻，体积电阻）
create table if not exists daodiantl (
    daodiantlId integer unsigned not null auto_increment primary key,
    cailiao_id integer unsigned not null unique key,
    pingbixn float(10,2)  not null,
    jiechudz float(10,2  not null,
    tijidz float(10,2) not null,
    index (cailiao_id),
    foreign key(cailiao_id)
        references cixingcljbcsh(cailiao_id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;

-- huitucsh 绘图参数 （输出名称，图表标题，图表宽度，图表高度，x轴类型，x轴名称，y轴名称）
create table if not exists huitucsh (
    huitucshId integer unsigned not null auto_increment primary key,
    diagram_id integer unsigned not null unique key,
    shuchumch varchar(32)  not null,
    tubiaobt varchar(32)  not null,
    x_axis_type char(10) not null,
    y_axis_type char(10) not null,
    x_axis_name char(16) not null,
    y_axis_name char(16) not null,
    index (diagram_id)
) engine=InnoDB DEFAULT CHARSET=utf8;
