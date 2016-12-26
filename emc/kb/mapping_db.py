#-*- coding: UTF-8 -*-
import sqlalchemy.types
import sqlalchemy.schema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from five import grok
from zope import schema
from zope.interface import Interface,implements
from emc.kb import ORMBase
from emc.kb import _

class IModel(Interface):
    """编号number 记录表
    """
    modelId = schema.Int(
            title=_(u"model table primary key"),
        )   
    # 型号代码
    xhdm = schema.TextLine(
            title=_(u"model code"),
        )    
    #型号名称
    xhmc = schema.TextLine(
            title=_(u"model name"),
        )

class Model(ORMBase):
    """Database-backed implementation of IModel
    """
    implements(IModel)
    
    __tablename__ = 'model'
    
    modelId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
        
    xhdm = sqlalchemy.schema.Column(sqlalchemy.types.String(8),
            nullable=False,
        )
    xhmc = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )

class Modeltest(ORMBase):
    """Database-backed implementation of IModel
    """
#     implements(IModel)
    
    __tablename__ = 'modeltest2'
    
    ID = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
                                       primary_key=True,)
    XHDM = sqlalchemy.schema.Column(sqlalchemy.types.String(8))
    XHMC = sqlalchemy.schema.Column(sqlalchemy.types.String(32))    

class IFashej(Interface):
    """发射机 
    """
    fashejId = schema.Int(
            title=_(u"table primary key"),
        )
    sbdm = schema.TextLine(
            title=_(u"she bei dai ma"),
        )      
    sbmc = schema.TextLine(
            title=_(u"fa she ji ming cheng"),
        )       
    # 分系统代码
    pcdm = schema.TextLine(
            title=_(u"zhuang tai pi ci dai ma"),
        )    
    #分系统名称
    location = schema.TextLine(
            title=_(u"wei zhi"),
        )
    #分系统类别
    freq = schema.Float(
            title=_(u"gongzuo pinlv"),
        )
    pd_upper = schema.Float(
            title=_(u"shang bian pin"),
        )
    pd_lower = schema.Float(
            title=_(u"xia bian pin"),
        )
    num = schema.Int(
            title=_(u"pinlv dian shu"),
        )
    freq_upper = schema.Float(
            title=_(u"pinlv shang xian"),
        )
    freq_lower = schema.Float(
            title=_(u"pinlv xia xian"),
        )
    bw = schema.Float(
            title=_(u"fashe dai kuan"),
        )
    base_power = schema.Float(
            title=_(u"ji pin gong lv"),
        )
    tzlx = schema.TextLine(
            title=_(u"tiao zhi lei xing"),
        )
    bzf = schema.Float(
            title=_(u"ben zhen pin lv"),
        )
    mid_freq = schema.Float(
            title=_(u"zhong pin"),
        )
    comment1 = schema.TextLine(
            title=_(u"bei zhu"),
        )                                            
class Fashej(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IFashej)
    
    __tablename__ = 'fashej'
    
    fashejId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
   
    sbdm = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )
    sbmc = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    pcdm = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
#     model = sqlalchemy.orm.relation(Model,primaryjoin=Model.modelId==modelId,)             
    location = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    freq = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        ) 
    pd_upper = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )        
    pd_lower = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    bw = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
        )
    base_power = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    tzlx = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )
    bzf = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    mid_freq = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    comment1 = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )                        
class IJieshouj(Interface):
    """接收机 
    """
    jishoujId = schema.Int(
            title=_(u"table primary key"),
        )
    sbdm = schema.TextLine(
            title=_(u"she bei dai ma"),
        )      
    sbmc = schema.TextLine(
            title=_(u"jie shou ji ming cheng"),
        )       
    pcdm = schema.TextLine(
            title=_(u"zhuang tai pi ci dai ma"),
        )    
    location = schema.TextLine(
            title=_(u"wei zhi"),
        )
    fb_upper = schema.Float(
            title=_(u"pin duan shang xian"),
        )    
    fb_lower = schema.Float(
            title=_(u"pin duan xia xian"),
        )
    freq = schema.Float(
            title=_(u"gongzuo pinlv"),
        )
    f_upper = schema.Float(
            title=_(u"shang bian pin"),
        )
    f_lower = schema.Float(
            title=_(u"xia bian pin"),
        )
    bw_receiver = schema.Float(
            title=_(u"jie shou ji dai kuan"),
        )
    sen_receiver = schema.Float(
            title=_(u"jie shou ji lin ming du"),
        )
    mf_freq_sign = schema.TextLine(
            title=_(u"zhong pin fu hao"),
        )
    mf_freq = schema.Float(
            title=_(u"zhong pin pin lv"),
        )    
    lo_freq = schema.Float(
            title=_(u"ben zhen pin lv"),
        )
                                           
class Jieshouj(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IJieshouj)
    
    __tablename__ = 'jieshouj'
    
    jieshoujId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
   
    sbdm = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )
    sbmc = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    pcdm = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    location = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    fb_upper = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )        
    fb_lower = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )    
    freq = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        ) 
    f_upper = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )        
    f_lower = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    bw_receiver = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    sen_receiver = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )    
    mf_freq_sign = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )
    mf_freq = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    lo_freq = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
class IFashetx(Interface):
    """发射天线 
    """
    fashetxId = schema.Int(
            title=_(u"table primary key"),
        )
    cssbdm = schema.TextLine(
            title=_(u"cong shu she bei dai ma"),
        )      
    cssbmc = schema.TextLine(
            title=_(u"cong shu she bei ming cheng"),
        )       
    pcdm = schema.TextLine(
            title=_(u"zhuang tai pi ci dai ma"),
        )    
    location = schema.TextLine(
            title=_(u"wei zhi"),
        )
    gain = schema.Float(
            title=_(u"zeng yi"),
        )    
    polarization = schema.TextLine(
            title=_(u"ji hua"),
        )
    fwbskd = schema.Float(
            title=_(u"fang wei bo su dai kuan"),
        )
    fybskd = schema.Float(
            title=_(u"fu yang bo su dai kuan"),
        )
    txzxj = schema.Float(
            title=_(u"tian xian zhi xiang jiao"),
        )

                                           
class Fashetx(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IFashetx)
    
    __tablename__ = 'fashetx'
    
    fashetxId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
   
    cssbdm = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )
    cssbmc = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    pcdm = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    location = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    gain = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )        
    polarization = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )    
    fwbskd = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        ) 
    fybskd = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )        
    txzxj = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
class IJieshoutx(Interface):
    """接收天线 
    """
    jieshoutxId = schema.Int(
            title=_(u"table primary key"),
        )
    cssbdm = schema.TextLine(
            title=_(u"cong shu she bei dai ma"),
        )      
    cssbmc = schema.TextLine(
            title=_(u"jie shou tian xian ming cheng"),
        )       
    pcdm = schema.TextLine(
            title=_(u"zhuang tai pi ci dai ma"),
        )    
    location = schema.TextLine(
            title=_(u"wei zhi"),
        )
    gain = schema.Float(
            title=_(u"zeng yi"),
        )    
    polarization = schema.TextLine(
            title=_(u"ji hua"),
        )
    fwbskd = schema.Float(
            title=_(u"fang wei bo su dai kuan"),
        )
    fybskd = schema.Float(
            title=_(u"fu yang bo su dai kuan"),
        )
    txzxj = schema.Float(
            title=_(u"tian xian zhi xiang jiao"),
        )

                                           
class Jieshoutx(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IJieshoutx)
    
    __tablename__ = 'jieshoutx'
    
    jieshoutxId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
   
    cssbdm = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )
    cssbmc = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    pcdm = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    location = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    gain = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )        
    polarization = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )    
    fwbskd = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        ) 
    fybskd = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )        
    txzxj = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
class ILvboq(Interface):
    """滤波器 
    """
    lvboqId = schema.Int(
            title=_(u"table primary key"),
        )
    cssbdm = schema.TextLine(
            title=_(u"cong shu she bei dai ma"),
        )      
    cssbmc = schema.TextLine(
            title=_(u"lv bo qi ming cheng"),
        )       
    pcdm = schema.TextLine(
            title=_(u"zhuang tai pi ci dai ma"),
        )    
    location = schema.TextLine(
            title=_(u"wei zhi"),
        )
    freq = schema.Float(
            title=_(u"gong zuo pin lv"),
        )
    f_upper = schema.Float(
            title=_(u"shang bian pin"),
        )    
    f_lower = schema.Float(
            title=_(u"xia bian pin"),
        )        
    order1 = schema.Float(
            title=_(u"lv bo qi ji shu"),
        )
    s21 = schema.Float(
            title=_(u"lv bo qi cha sun"),
        )
                                           
class Lvboq(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(ILvboq)
    
    __tablename__ = 'lvboq'
    
    lvboqId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
   
    cssbdm = sqlalchemy.schema.Column(sqlalchemy.types.String(16),
            nullable=False,
        )
    cssbmc = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )    
    pcdm = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )
    location = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )   
    freq = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        ) 
    f_upper = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )        
    f_lower = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    order1 = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        ) 
    s21 = sqlalchemy.schema.Column(sqlalchemy.types.Float(precision='16,4'),
            nullable=False,
        )
    
    
class IDianxingtxzyzk(Interface):
    """典型天线增益子库 
    """
    dianxingtxzyzkId = schema.Int(
            title=_(u"table primary key"),
        )
    type_antennas = schema.TextLine(
            title=_(u"tian xian lei xing"),
        )      
    gain = schema.Int(
            title=_(u"zeng yi"),
        )


class Dianxingtxzyzk(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IDianxingtxzyzk)
    
    __tablename__ = 'dianxingtxzyzk'
    
    dianxingtxzyzkId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
   
    type_antennas = sqlalchemy.schema.Column(sqlalchemy.types.String(30),
            nullable=False,
        )
    gain = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
        )

    
class ITianxianzyzk(Interface):
    """天线子库 
    """
    tianxianzyzkId = schema.Int(
            title=_(u"table primary key"),
        )
    lib_code = schema.TextLine(
            title=_(u"zi ku dai ma"),
        )      
    lib_name = schema.TextLine(
            title=_(u"zi ku ming cheng"),
        )


class Tianxianzyzk(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IDianxingtxzyzk)
    
    __tablename__ = 'tianxianzyzk'
    
    tianxianzyzkId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )   
    lib_code = sqlalchemy.schema.Column(sqlalchemy.types.String(10),
            nullable=False,
        )
    lib_name = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )

    
class IJieshoujzk(Interface):
    """接收机子库 
    """
    jieshoujzkId = schema.Int(
            title=_(u"table primary key"),
        )
    lib_code = schema.TextLine(
            title=_(u"zi ku dai ma"),
        )      
    lib_name = schema.TextLine(
            title=_(u"zi ku ming cheng"),
        )


class Jieshoujzk(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IJieshoujzk)
    
    __tablename__ = 'jieshoujzk'
    
    jieshoujzkId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )   
    lib_code = sqlalchemy.schema.Column(sqlalchemy.types.String(10),
            nullable=False,
        )
    lib_name = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )

    
class IFashejzk(Interface):
    """发射机子库 
    """
    fashejzkId = schema.Int(
            title=_(u"table primary key"),
        )
    lib_code = schema.TextLine(
            title=_(u"zi ku dai ma"),
        )      
    lib_name = schema.TextLine(
            title=_(u"zi ku ming cheng"),
        )


class Fashejzk(ORMBase):
    """Database-backed implementation of IFashej
    """
    implements(IFashejzk)
    
    __tablename__ = 'fashejzk'
    
    fashejzkId = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )   
    lib_code = sqlalchemy.schema.Column(sqlalchemy.types.String(10),
            nullable=False,
        )
    lib_name = sqlalchemy.schema.Column(sqlalchemy.types.String(32),
            nullable=False,
        )                                 