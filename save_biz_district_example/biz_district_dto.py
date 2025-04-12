from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

'''
商圈导入类

@author XieChen
@date 2025/04/12 14:50:51
'''
@dataclass
class biz_district_dto:
    business_district_name: Optional[str] = None  # 商圈名称
    business_district_id: Optional[int] = None  # 商圈id
    location: Optional[str] = None  # 地址坐标集，示例："112.969029,28.193397";"112.96895,28.192156"
    user_id: Optional[int] = None  # 操作人id
    city_code: Optional[str] = None  # 城市编码
    city: Optional[str] = None  # 城市
    province: Optional[str] = None  # 省
    province_code: Optional[str] = None  # 省编码
    district: Optional[str] = None  # 区
    district_code: Optional[str] = None  # 区编码
    area_square_meters: Optional[int] = None  # 面积(平方米)
    weight: Optional[int] = None  # 评分
    bd_type: Optional[str] = None  # 类别
    cluster: Optional[str] = None  # 等级:S|A|B|C
    level: Optional[str] = None  # 等级
    passenger_flow: Optional[int] = None  # 客流指数
    unit_passenger_flow: Optional[Decimal] = None  # 单位客流
    first_longitude: Optional[str] = None  # 商圈第一个点坐标经度
    first_latitude: Optional[str] = None  # 商圈第一个点坐标纬度
    inlet_outlet: Optional[str] = None  # 出入口
    entrance_address: Optional[str] = None  # 出入口地址
    nodal_point: Optional[str] = None  # 集散点
    point_location_num: Optional[int] = None  # 点位数
    business_district_state: Optional[int] = None  # 商圈状态(0/1)
    business_district_type: Optional[str] = None  # 商圈类型
    competitor_count: Optional[int] = None  # 竞品店数
    