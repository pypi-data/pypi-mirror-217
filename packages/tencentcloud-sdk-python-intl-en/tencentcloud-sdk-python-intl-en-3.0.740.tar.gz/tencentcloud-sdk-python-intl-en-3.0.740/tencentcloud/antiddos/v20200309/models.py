# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class AnycastOutPackRelation(AbstractModel):
    """Details of the Anycast package

    """

    def __init__(self):
        r"""
        :param NormalBandwidth: Application bandwidth (in Mbps).
Note: This field may return null, indicating that no valid values can be obtained.
        :type NormalBandwidth: int
        :param ForwardRulesLimit: Number of forwarding rules
Note: This field may return null, indicating that no valid values can be obtained.
        :type ForwardRulesLimit: int
        :param AutoRenewFlag: Auto-renewal flag
Note: This field may return null, indicating that no valid values can be obtained.
        :type AutoRenewFlag: int
        :param CurDeadline: Expiration date
Note: This field may return null, indicating that no valid values can be obtained.
        :type CurDeadline: str
        """
        self.NormalBandwidth = None
        self.ForwardRulesLimit = None
        self.AutoRenewFlag = None
        self.CurDeadline = None


    def _deserialize(self, params):
        self.NormalBandwidth = params.get("NormalBandwidth")
        self.ForwardRulesLimit = params.get("ForwardRulesLimit")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.CurDeadline = params.get("CurDeadline")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociateDDoSEipAddressRequest(AbstractModel):
    """AssociateDDoSEipAddress request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID (only Anti-DDoS Advanced). For example, `bgpip-0000011x`.
        :type InstanceId: str
        :param Eip: EIP of the Anti-DDoS instance ID
        :type Eip: str
        :param CvmInstanceID: Instance ID to bind. For example, `ins-11112222`. It can be queried in the console or obtained from `InstanceId` returned by `DescribeInstances`.
        :type CvmInstanceID: str
        :param CvmRegion: Region of the CVM instance. For example, `ap-hongkong`.
        :type CvmRegion: str
        """
        self.InstanceId = None
        self.Eip = None
        self.CvmInstanceID = None
        self.CvmRegion = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Eip = params.get("Eip")
        self.CvmInstanceID = params.get("CvmInstanceID")
        self.CvmRegion = params.get("CvmRegion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociateDDoSEipAddressResponse(AbstractModel):
    """AssociateDDoSEipAddress response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AssociateDDoSEipLoadBalancerRequest(AbstractModel):
    """AssociateDDoSEipLoadBalancer request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID (only Anti-DDoS Advanced). For example, `bgpip-0000011x`.
        :type InstanceId: str
        :param Eip: EIP of the Anti-DDoS instance ID.
        :type Eip: str
        :param LoadBalancerID: ID of the CLB to bind, such as `lb-0000002i`. It can be queried in the console or obtained from `LoadBalancerId` returned by the `DescribeLoadBalancers` API.
        :type LoadBalancerID: str
        :param LoadBalancerRegion: Region of the CLB instance, such as `ap-hongkong`.
        :type LoadBalancerRegion: str
        :param Vip: CLB private IP
        :type Vip: str
        """
        self.InstanceId = None
        self.Eip = None
        self.LoadBalancerID = None
        self.LoadBalancerRegion = None
        self.Vip = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Eip = params.get("Eip")
        self.LoadBalancerID = params.get("LoadBalancerID")
        self.LoadBalancerRegion = params.get("LoadBalancerRegion")
        self.Vip = params.get("Vip")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociateDDoSEipLoadBalancerResponse(AbstractModel):
    """AssociateDDoSEipLoadBalancer response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class BGPIPInstance(AbstractModel):
    """Anti-DDoS Advanced instance details

    """

    def __init__(self):
        r"""
        :param InstanceDetail: Anti-DDoS instance details
        :type InstanceDetail: :class:`tencentcloud.antiddos.v20200309.models.InstanceRelation`
        :param SpecificationLimit: Anti-DDoS instance specifications
        :type SpecificationLimit: :class:`tencentcloud.antiddos.v20200309.models.BGPIPInstanceSpecification`
        :param Usage: Anti-DDoS instance usage statistics
        :type Usage: :class:`tencentcloud.antiddos.v20200309.models.BGPIPInstanceUsages`
        :param Region: Region of the Anti-DDoS instance
        :type Region: :class:`tencentcloud.antiddos.v20200309.models.RegionInfo`
        :param Status: Status of the Anti-DDoS instance. Valid values:
`idle`: running
`attacking`: under attacks
`blocking`: blocked
`creating`: creating
`deblocking`: unblocking
`isolate`: reprocessed and isolated
        :type Status: str
        :param ExpiredTime: Purchase time
        :type ExpiredTime: str
        :param CreatedTime: Expired At
        :type CreatedTime: str
        :param Name: Name of the Anti-DDoS instance
        :type Name: str
        :param PackInfo: Package details of the Anti-DDoS instance.
Note: This field is `null` for an Anti-DDoS instance without using a package.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type PackInfo: :class:`tencentcloud.antiddos.v20200309.models.PackInfo`
        :param StaticPackRelation: Non-BGP package details of the Anti-DDoS instance.
Note: This field is `null` for an Anti-DDoS instance without using a non-BGP package.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type StaticPackRelation: :class:`tencentcloud.antiddos.v20200309.models.StaticPackRelation`
        :param ZoneId: Specifies the ISP. `0`: Chinese mainland ISPs (default); `1`：Radware；`2`: Tencent; `3`: NSFOCUS. Note that `1`, `2` and `3` are used for services outside the Chinese mainland.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ZoneId: int
        :param Tgw: Used to differentiate clusters
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type Tgw: int
        :param EipAddressStatus: EIP states: `CREATING`, `BINDING`, `BIND`, `UNBINDING`, `UNBIND`, `OFFLINING`, and `BIND_ENI`. The EIP must be bound to an Anti-DDoS Advanced instance.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type EipAddressStatus: str
        :param EipFlag: Whether it is an Anti-DDoS EIP instance. `1`: Yes; `0`: No.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type EipFlag: int
        :param EipAddressPackRelation: EIP package details of the Anti-DDoS Advanced instance.
Note: This field is `null` for an Anti-DDoS Advanced instance without using an EIP package.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type EipAddressPackRelation: :class:`tencentcloud.antiddos.v20200309.models.EipAddressPackRelation`
        :param EipAddressInfo: Details of the Anti-DDoS Advanced instance bound to the EIP.
Note: This field is `null` if the EIP is not bound to an Anti-DDoS Advanced instance.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type EipAddressInfo: :class:`tencentcloud.antiddos.v20200309.models.EipAddressRelation`
        :param Domain: Recommended domain name for clients to access.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Domain: str
        :param DamDDoSStatus: Whether to enable Sec-MCA. Valid values: `1` (enabled) and `0` (disabled).
        :type DamDDoSStatus: int
        :param V6Flag: Whether it’s an IPv6 address. `1`: Yes; `0`: No.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type V6Flag: int
        :param BGPIPChannelFlag: Whether it’s an Anti-DDoS Advanced instance from Tencent Cloud channels. `1`: Yes; `0`: No.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type BGPIPChannelFlag: int
        :param TagInfoList: Tag that the Anti-DDoS Advanced instance is associated with
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type TagInfoList: list of TagInfo
        :param AnycastOutPackRelation: All-out package details of the instance
When an all-out package is not used by the instance, this field is `null`.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type AnycastOutPackRelation: :class:`tencentcloud.antiddos.v20200309.models.AnycastOutPackRelation`
        :param InstanceVersion: Edition of the instance
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type InstanceVersion: int
        :param ConvoyId: Convoy instance ID
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ConvoyId: str
        :param ElasticBandwidth: Pay-as-you-go bandwidth
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ElasticBandwidth: int
        :param EOFlag: Whether it’s the IP broadcasted by EdgeOne. Values: `1` (yes), `0` (no)
Note: This field may return null, indicating that no valid values can be obtained.
        :type EOFlag: int
        """
        self.InstanceDetail = None
        self.SpecificationLimit = None
        self.Usage = None
        self.Region = None
        self.Status = None
        self.ExpiredTime = None
        self.CreatedTime = None
        self.Name = None
        self.PackInfo = None
        self.StaticPackRelation = None
        self.ZoneId = None
        self.Tgw = None
        self.EipAddressStatus = None
        self.EipFlag = None
        self.EipAddressPackRelation = None
        self.EipAddressInfo = None
        self.Domain = None
        self.DamDDoSStatus = None
        self.V6Flag = None
        self.BGPIPChannelFlag = None
        self.TagInfoList = None
        self.AnycastOutPackRelation = None
        self.InstanceVersion = None
        self.ConvoyId = None
        self.ElasticBandwidth = None
        self.EOFlag = None


    def _deserialize(self, params):
        if params.get("InstanceDetail") is not None:
            self.InstanceDetail = InstanceRelation()
            self.InstanceDetail._deserialize(params.get("InstanceDetail"))
        if params.get("SpecificationLimit") is not None:
            self.SpecificationLimit = BGPIPInstanceSpecification()
            self.SpecificationLimit._deserialize(params.get("SpecificationLimit"))
        if params.get("Usage") is not None:
            self.Usage = BGPIPInstanceUsages()
            self.Usage._deserialize(params.get("Usage"))
        if params.get("Region") is not None:
            self.Region = RegionInfo()
            self.Region._deserialize(params.get("Region"))
        self.Status = params.get("Status")
        self.ExpiredTime = params.get("ExpiredTime")
        self.CreatedTime = params.get("CreatedTime")
        self.Name = params.get("Name")
        if params.get("PackInfo") is not None:
            self.PackInfo = PackInfo()
            self.PackInfo._deserialize(params.get("PackInfo"))
        if params.get("StaticPackRelation") is not None:
            self.StaticPackRelation = StaticPackRelation()
            self.StaticPackRelation._deserialize(params.get("StaticPackRelation"))
        self.ZoneId = params.get("ZoneId")
        self.Tgw = params.get("Tgw")
        self.EipAddressStatus = params.get("EipAddressStatus")
        self.EipFlag = params.get("EipFlag")
        if params.get("EipAddressPackRelation") is not None:
            self.EipAddressPackRelation = EipAddressPackRelation()
            self.EipAddressPackRelation._deserialize(params.get("EipAddressPackRelation"))
        if params.get("EipAddressInfo") is not None:
            self.EipAddressInfo = EipAddressRelation()
            self.EipAddressInfo._deserialize(params.get("EipAddressInfo"))
        self.Domain = params.get("Domain")
        self.DamDDoSStatus = params.get("DamDDoSStatus")
        self.V6Flag = params.get("V6Flag")
        self.BGPIPChannelFlag = params.get("BGPIPChannelFlag")
        if params.get("TagInfoList") is not None:
            self.TagInfoList = []
            for item in params.get("TagInfoList"):
                obj = TagInfo()
                obj._deserialize(item)
                self.TagInfoList.append(obj)
        if params.get("AnycastOutPackRelation") is not None:
            self.AnycastOutPackRelation = AnycastOutPackRelation()
            self.AnycastOutPackRelation._deserialize(params.get("AnycastOutPackRelation"))
        self.InstanceVersion = params.get("InstanceVersion")
        self.ConvoyId = params.get("ConvoyId")
        self.ElasticBandwidth = params.get("ElasticBandwidth")
        self.EOFlag = params.get("EOFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BGPIPInstanceSpecification(AbstractModel):
    """Anti-DDoS Advanced instance specifications

    """

    def __init__(self):
        r"""
        :param ProtectBandwidth: Base protection bandwidth (in Mbps)
        :type ProtectBandwidth: int
        :param ProtectCCQPS: CC protection bandwidth (in QPS)
        :type ProtectCCQPS: int
        :param NormalBandwidth: Normal application bandwidth (in Mbps)
        :type NormalBandwidth: int
        :param ForwardRulesLimit: Number of forwarding rules
        :type ForwardRulesLimit: int
        :param AutoRenewFlag: Auto-renewal status. Valid values:
`0`: disabled
`1`: enabled
]
        :type AutoRenewFlag: int
        :param Line: Anti-DDoS Advanced line. Valid values:
`1`: BGP
`2`: China Telecom
`3`: China Unicom
`4`: China Mobile
`99`: third-party line
]
        :type Line: int
        :param ElasticBandwidth: Elastic protection bandwidth (in Mbps)
        :type ElasticBandwidth: int
        """
        self.ProtectBandwidth = None
        self.ProtectCCQPS = None
        self.NormalBandwidth = None
        self.ForwardRulesLimit = None
        self.AutoRenewFlag = None
        self.Line = None
        self.ElasticBandwidth = None


    def _deserialize(self, params):
        self.ProtectBandwidth = params.get("ProtectBandwidth")
        self.ProtectCCQPS = params.get("ProtectCCQPS")
        self.NormalBandwidth = params.get("NormalBandwidth")
        self.ForwardRulesLimit = params.get("ForwardRulesLimit")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.Line = params.get("Line")
        self.ElasticBandwidth = params.get("ElasticBandwidth")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BGPIPInstanceUsages(AbstractModel):
    """Anti-DDoS Advanced instance usage statistics

    """

    def __init__(self):
        r"""
        :param PortRulesUsage: Number of used port rules
        :type PortRulesUsage: int
        :param DomainRulesUsage: Number of used domain name rules
        :type DomainRulesUsage: int
        :param Last7DayAttackCount: Number of attack times in the last 7 days
        :type Last7DayAttackCount: int
        """
        self.PortRulesUsage = None
        self.DomainRulesUsage = None
        self.Last7DayAttackCount = None


    def _deserialize(self, params):
        self.PortRulesUsage = params.get("PortRulesUsage")
        self.DomainRulesUsage = params.get("DomainRulesUsage")
        self.Last7DayAttackCount = params.get("Last7DayAttackCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BGPInstance(AbstractModel):
    """Details of the Anti-DDoS Pro instance

    """

    def __init__(self):
        r"""
        :param InstanceDetail: Details of the Anti-DDoS Pro instance
        :type InstanceDetail: :class:`tencentcloud.antiddos.v20200309.models.InstanceRelation`
        :param SpecificationLimit: Specifications of the Anti-DDoS Pro instance
        :type SpecificationLimit: :class:`tencentcloud.antiddos.v20200309.models.BGPInstanceSpecification`
        :param Usage: Usage statistics of the Anti-DDoS Pro instance
        :type Usage: :class:`tencentcloud.antiddos.v20200309.models.BGPInstanceUsages`
        :param Region: Region of the Anti-DDoS Pro instance
        :type Region: :class:`tencentcloud.antiddos.v20200309.models.RegionInfo`
        :param Status: Status of the Anti-DDoS Pro instance. Valid values:
`idle`: The instance is running normally.
`attacking`: The instance is under attack.
`blocking`: The instance is blocked.
`creating`: The instance is being created.
`deblocking`: Unblocking the instance
`isolate`: The instance is being isolated.
        :type Status: str
        :param CreatedTime: Purchase time
        :type CreatedTime: str
        :param ExpiredTime: Expiration time
        :type ExpiredTime: str
        :param Name: Name of the Anti-DDoS Pro instance
        :type Name: str
        :param PackInfo: Details of the package to which the Anti-DDoS Pro instance belongs.
When the package provided is not used by the instance, this field is `null`.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type PackInfo: :class:`tencentcloud.antiddos.v20200309.models.PackInfo`
        :param EipProductInfos: Details of the cloud product used by the EIP bound to the Anti-DDoS Pro instance
        :type EipProductInfos: list of EipProductInfo
        :param BoundStatus: Binding status of the Anti-DDoS Pro instance
`idle`: The instance is bound.
 `bounding`: Binding the instance.
`failed`: Failed to bind
]
        :type BoundStatus: str
        :param DDoSLevel: Layer-4 protection level
        :type DDoSLevel: str
        :param CCEnable: Status of CC protection
        :type CCEnable: int
        :param TagInfoList: Tags associated with the resource
        :type TagInfoList: list of TagInfo
        :param IpCountNewFlag: New edition of Anti-DDoS Pro
        :type IpCountNewFlag: int
        :param VitalityVersion: The version of attack defense package
        :type VitalityVersion: int
        :param Line: Network line
Note: This field may return null, indicating that no valid values can be obtained.
        :type Line: int
        :param ElasticServiceBandwidth: Whether to enable elastic bandwidth
        :type ElasticServiceBandwidth: int
        :param GiftServiceBandWidth: Bandwidth quota given away by Tencent Cloud
        :type GiftServiceBandWidth: int
        """
        self.InstanceDetail = None
        self.SpecificationLimit = None
        self.Usage = None
        self.Region = None
        self.Status = None
        self.CreatedTime = None
        self.ExpiredTime = None
        self.Name = None
        self.PackInfo = None
        self.EipProductInfos = None
        self.BoundStatus = None
        self.DDoSLevel = None
        self.CCEnable = None
        self.TagInfoList = None
        self.IpCountNewFlag = None
        self.VitalityVersion = None
        self.Line = None
        self.ElasticServiceBandwidth = None
        self.GiftServiceBandWidth = None


    def _deserialize(self, params):
        if params.get("InstanceDetail") is not None:
            self.InstanceDetail = InstanceRelation()
            self.InstanceDetail._deserialize(params.get("InstanceDetail"))
        if params.get("SpecificationLimit") is not None:
            self.SpecificationLimit = BGPInstanceSpecification()
            self.SpecificationLimit._deserialize(params.get("SpecificationLimit"))
        if params.get("Usage") is not None:
            self.Usage = BGPInstanceUsages()
            self.Usage._deserialize(params.get("Usage"))
        if params.get("Region") is not None:
            self.Region = RegionInfo()
            self.Region._deserialize(params.get("Region"))
        self.Status = params.get("Status")
        self.CreatedTime = params.get("CreatedTime")
        self.ExpiredTime = params.get("ExpiredTime")
        self.Name = params.get("Name")
        if params.get("PackInfo") is not None:
            self.PackInfo = PackInfo()
            self.PackInfo._deserialize(params.get("PackInfo"))
        if params.get("EipProductInfos") is not None:
            self.EipProductInfos = []
            for item in params.get("EipProductInfos"):
                obj = EipProductInfo()
                obj._deserialize(item)
                self.EipProductInfos.append(obj)
        self.BoundStatus = params.get("BoundStatus")
        self.DDoSLevel = params.get("DDoSLevel")
        self.CCEnable = params.get("CCEnable")
        if params.get("TagInfoList") is not None:
            self.TagInfoList = []
            for item in params.get("TagInfoList"):
                obj = TagInfo()
                obj._deserialize(item)
                self.TagInfoList.append(obj)
        self.IpCountNewFlag = params.get("IpCountNewFlag")
        self.VitalityVersion = params.get("VitalityVersion")
        self.Line = params.get("Line")
        self.ElasticServiceBandwidth = params.get("ElasticServiceBandwidth")
        self.GiftServiceBandWidth = params.get("GiftServiceBandWidth")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BGPInstanceSpecification(AbstractModel):
    """Anti-DDoS Pro instance specifications

    """

    def __init__(self):
        r"""
        :param ProtectBandwidth: Base protection bandwidth (in Gbps)
        :type ProtectBandwidth: int
        :param ProtectCountLimit: Number of protection chances
        :type ProtectCountLimit: int
        :param ProtectIPNumberLimit: Number of protected IPs
        :type ProtectIPNumberLimit: int
        :param AutoRenewFlag: Auto-renewal status. Values:
`0`: Disabled
`1`: Enabled
]
        :type AutoRenewFlag: int
        :param UnionPackFlag: Protection type of Anti-DDoS Pro. Valid values: `0` (general protection) and `1` (Lighthouse-based protection).
Note: This field may return null, indicating that no valid values can be obtained.
        :type UnionPackFlag: int
        :param ServiceBandWidth: Application bandwidth
Note: This field may return null, indicating that no valid values can be obtained.
        :type ServiceBandWidth: int
        :param BattleEditionFlag: Whether it’s an Anti-DDoS Pro Premium edition. Values: `0` (General edition); `1` (Premium edition).
Note: This field may return null, indicating that no valid values can be obtained.
        :type BattleEditionFlag: int
        :param ChannelEditionFlag: Whether it’s an Anti-DDoS Pro Standard edition. Values: `0` (General edition); `1` (Standard edition).
Note: This field may return null, indicating that no valid values can be obtained.
        :type ChannelEditionFlag: int
        :param EnterpriseFlag: Whether it’s an Anti-DDoS Pro Enterprise edition. Values: `0` (General edition); `1` (Enterprise edition).
Note: This field may return null, indicating that no valid values can be obtained.
        :type EnterpriseFlag: int
        :param ElasticLimit: Elastic bandwidth threshold of the Anti-DDoS Pro Enterprise edition.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ElasticLimit: int
        :param DownGradeProtect: Protection bandwidth after the plan downgrade, in Gbps. 
Note: This field may return `null`, indicating that no valid value was found.
        :type DownGradeProtect: int
        """
        self.ProtectBandwidth = None
        self.ProtectCountLimit = None
        self.ProtectIPNumberLimit = None
        self.AutoRenewFlag = None
        self.UnionPackFlag = None
        self.ServiceBandWidth = None
        self.BattleEditionFlag = None
        self.ChannelEditionFlag = None
        self.EnterpriseFlag = None
        self.ElasticLimit = None
        self.DownGradeProtect = None


    def _deserialize(self, params):
        self.ProtectBandwidth = params.get("ProtectBandwidth")
        self.ProtectCountLimit = params.get("ProtectCountLimit")
        self.ProtectIPNumberLimit = params.get("ProtectIPNumberLimit")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.UnionPackFlag = params.get("UnionPackFlag")
        self.ServiceBandWidth = params.get("ServiceBandWidth")
        self.BattleEditionFlag = params.get("BattleEditionFlag")
        self.ChannelEditionFlag = params.get("ChannelEditionFlag")
        self.EnterpriseFlag = params.get("EnterpriseFlag")
        self.ElasticLimit = params.get("ElasticLimit")
        self.DownGradeProtect = params.get("DownGradeProtect")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BGPInstanceUsages(AbstractModel):
    """Anti-DDoS Pro instance usage statistics

    """

    def __init__(self):
        r"""
        :param ProtectCountUsage: Number of used protection chances
        :type ProtectCountUsage: int
        :param ProtectIPNumberUsage: Number of protected IPs
        :type ProtectIPNumberUsage: int
        :param Last7DayAttackCount: Number of attack times in the last 7 days
        :type Last7DayAttackCount: int
        """
        self.ProtectCountUsage = None
        self.ProtectIPNumberUsage = None
        self.Last7DayAttackCount = None


    def _deserialize(self, params):
        self.ProtectCountUsage = params.get("ProtectCountUsage")
        self.ProtectIPNumberUsage = params.get("ProtectIPNumberUsage")
        self.Last7DayAttackCount = params.get("Last7DayAttackCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BlackWhiteIpRelation(AbstractModel):
    """IP blocklist/allowlist

    """

    def __init__(self):
        r"""
        :param Ip: IP address
        :type Ip: str
        :param Type: IP type. Valid values: `black` (blocklisted IP), `white`(allowlisted IP).
        :type Type: str
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        :param Mask: IP mask. `0` indicates a 32-bit IP.
        :type Mask: int
        :param ModifyTime: Modification time
        :type ModifyTime: str
        """
        self.Ip = None
        self.Type = None
        self.InstanceDetailList = None
        self.Mask = None
        self.ModifyTime = None


    def _deserialize(self, params):
        self.Ip = params.get("Ip")
        self.Type = params.get("Type")
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        self.Mask = params.get("Mask")
        self.ModifyTime = params.get("ModifyTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BoundIpInfo(AbstractModel):
    """IP bound to the Anti-DDoS Pro instance

    """

    def __init__(self):
        r"""
        :param Ip: IP address
        :type Ip: str
        :param BizType: Category of product that can be bound. Valid values: `public` (CVM and CLB), `bm` (BM), `eni` (ENI), `vpngw` (VPN gateway), `natgw` (NAT gateway), `waf` (WAF), `fpc` (financial products), `gaap` (GAAP), and `other` (hosted IP). This field is required when you perform binding.
        :type BizType: str
        :param InstanceId: Anti-DDoS instance ID of the IP. This field is required only when the instance is bound to an IP. For example, this field InstanceId will be `eni-*` if the instance ID is bound to an ENI IP; `none` if there is no instance to bind to a managed IP.
        :type InstanceId: str
        :param DeviceType: Sub-product category. Valid values: `cvm` (CVM), `lb` (Load balancer), `eni` (ENI), `vpngw` (VPN gateway), `natgw` (NAT gateway), `waf` (WAF), `fpc` (financial products), `gaap` (GAAP), `eip` (BM EIP) and `other` (managed IP). This field is required when you perform binding.
        :type DeviceType: str
        :param IspCode: ISP. Valid values: `0` (China Telecom), `1` (China Unicom), `2` (China Mobile), and `5` (BGP). This field is required when you perform binding.
        :type IspCode: int
        """
        self.Ip = None
        self.BizType = None
        self.InstanceId = None
        self.DeviceType = None
        self.IspCode = None


    def _deserialize(self, params):
        self.Ip = params.get("Ip")
        self.BizType = params.get("BizType")
        self.InstanceId = params.get("InstanceId")
        self.DeviceType = params.get("DeviceType")
        self.IspCode = params.get("IspCode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CCLevelPolicy(AbstractModel):
    """The level-defining policy of CC attacks

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: Ip
        :type Ip: str
        :param Protocol: Protocol
        :type Protocol: str
        :param Domain: Domain name
        :type Domain: str
        :param Level: Protection level. Values: `default`, `loose` and `strict`.
        :type Level: str
        :param CreateTime: Creation time
        :type CreateTime: str
        :param ModifyTime: Modification time
        :type ModifyTime: str
        """
        self.InstanceId = None
        self.Ip = None
        self.Protocol = None
        self.Domain = None
        self.Level = None
        self.CreateTime = None
        self.ModifyTime = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Protocol = params.get("Protocol")
        self.Domain = params.get("Domain")
        self.Level = params.get("Level")
        self.CreateTime = params.get("CreateTime")
        self.ModifyTime = params.get("ModifyTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CCPrecisionPlyRecord(AbstractModel):
    """CC precise protection configuration fields

    """

    def __init__(self):
        r"""
        :param FieldType: Type of the configuration field. Only `value` is supported.
        :type FieldType: str
        :param FieldName: Configuration field. Valid values: `cgi`, `ua`, `cookie`, `referer`, `accept`, and `srcip`.
        :type FieldName: str
        :param Value: Value of the configuration field
        :type Value: str
        :param ValueOperator: Filters values of configuration fields. `equal`: The value matches the configuration field. `not_equal`: The value does not match the configuration field. `include`: The value is included.
        :type ValueOperator: str
        """
        self.FieldType = None
        self.FieldName = None
        self.Value = None
        self.ValueOperator = None


    def _deserialize(self, params):
        self.FieldType = params.get("FieldType")
        self.FieldName = params.get("FieldName")
        self.Value = params.get("Value")
        self.ValueOperator = params.get("ValueOperator")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CCPrecisionPolicy(AbstractModel):
    """CC precise protection policy information

    """

    def __init__(self):
        r"""
        :param PolicyId: Policy ID
        :type PolicyId: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP address
        :type Ip: str
        :param Protocol: Protocol
        :type Protocol: str
        :param Domain: Domain name
        :type Domain: str
        :param PolicyAction: Action of limiting request frequency. Valid values: `alg` (limit request frequency via verification codes) and `drop`(drop requests).
        :type PolicyAction: str
        :param PolicyList: List of policies
        :type PolicyList: list of CCPrecisionPlyRecord
        :param CreateTime: Creation time
        :type CreateTime: str
        :param ModifyTime: Modification time
        :type ModifyTime: str
        """
        self.PolicyId = None
        self.InstanceId = None
        self.Ip = None
        self.Protocol = None
        self.Domain = None
        self.PolicyAction = None
        self.PolicyList = None
        self.CreateTime = None
        self.ModifyTime = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Protocol = params.get("Protocol")
        self.Domain = params.get("Domain")
        self.PolicyAction = params.get("PolicyAction")
        if params.get("PolicyList") is not None:
            self.PolicyList = []
            for item in params.get("PolicyList"):
                obj = CCPrecisionPlyRecord()
                obj._deserialize(item)
                self.PolicyList.append(obj)
        self.CreateTime = params.get("CreateTime")
        self.ModifyTime = params.get("ModifyTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CCReqLimitPolicyRecord(AbstractModel):
    """Configuration fields of CC frequency limit policies

    """

    def __init__(self):
        r"""
        :param Period: Sampling interval (in seconds). Valid values: `1`, `10`, `30`, and `60`.
        :type Period: int
        :param RequestNum: Number of requests. Value range: 1-2000.
        :type RequestNum: int
        :param Action: Action of limiting request frequency. Valid values: `alg` (limit request frequency via verification codes) and `drop`(drop requests).
        :type Action: str
        :param ExecuteDuration: Sets an interval of the frequency limit policy. Value range: 1-86400 (in seconds).
        :type ExecuteDuration: int
        :param Mode: Filters values of configuration fields. `include`: The value is included. `equal`: The value matches the configuration field.
        :type Mode: str
        :param Uri: URI, which cannot be used together with `User-Agent` and `Cookie`.
        :type Uri: str
        :param UserAgent: User-Agent, which cannot be used together with `Uri` and `Cookie`.
        :type UserAgent: str
        :param Cookie: Cookie, which cannot be used together with `Uri` and `User-Agent`.
        :type Cookie: str
        """
        self.Period = None
        self.RequestNum = None
        self.Action = None
        self.ExecuteDuration = None
        self.Mode = None
        self.Uri = None
        self.UserAgent = None
        self.Cookie = None


    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RequestNum = params.get("RequestNum")
        self.Action = params.get("Action")
        self.ExecuteDuration = params.get("ExecuteDuration")
        self.Mode = params.get("Mode")
        self.Uri = params.get("Uri")
        self.UserAgent = params.get("UserAgent")
        self.Cookie = params.get("Cookie")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CCThresholdPolicy(AbstractModel):
    """CC cleansing threshold policy

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP address
        :type Ip: str
        :param Protocol: Protocol
        :type Protocol: str
        :param Domain: Domain name
        :type Domain: str
        :param Threshold: Cleansing threshold
        :type Threshold: int
        :param CreateTime: Creation time
        :type CreateTime: str
        :param ModifyTime: Modification time
        :type ModifyTime: str
        """
        self.InstanceId = None
        self.Ip = None
        self.Protocol = None
        self.Domain = None
        self.Threshold = None
        self.CreateTime = None
        self.ModifyTime = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Protocol = params.get("Protocol")
        self.Domain = params.get("Domain")
        self.Threshold = params.get("Threshold")
        self.CreateTime = params.get("CreateTime")
        self.ModifyTime = params.get("ModifyTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CcBlackWhiteIpPolicy(AbstractModel):
    """Layer-4 access control list

    """

    def __init__(self):
        r"""
        :param PolicyId: Policy ID
        :type PolicyId: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP address
        :type Ip: str
        :param Domain: Domain name
        :type Domain: str
        :param Protocol: Protocol
        :type Protocol: str
        :param Type: IP type. Valid values: `black` (blocklisted IP), `white`(allowlisted IP).
        :type Type: str
        :param BlackWhiteIp: Blocklist/Allowlist IP address
        :type BlackWhiteIp: str
        :param Mask: Mask
        :type Mask: int
        :param CreateTime: Creation time
        :type CreateTime: str
        :param ModifyTime: Modification time
        :type ModifyTime: str
        """
        self.PolicyId = None
        self.InstanceId = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None
        self.Type = None
        self.BlackWhiteIp = None
        self.Mask = None
        self.CreateTime = None
        self.ModifyTime = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        self.Type = params.get("Type")
        self.BlackWhiteIp = params.get("BlackWhiteIp")
        self.Mask = params.get("Mask")
        self.CreateTime = params.get("CreateTime")
        self.ModifyTime = params.get("ModifyTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CcGeoIPBlockConfig(AbstractModel):
    """Anti-DDoS regional blocking configuration

    """

    def __init__(self):
        r"""
        :param RegionType: Region type. Valid values:
`oversea`: Outside the Chinese mainland.
`china`: The Chinese mainland.
`customized`: User-specified region.
]
        :type RegionType: str
        :param Action: Blocking action. Valid values:
`drop`: Block the request.
`alg`: Verify the request via CAPTCHA.
]
        :type Action: str
        :param Id: Configuration ID, which is generated after a configuration is added. This field is only required to modify or delete a configuration.
        :type Id: str
        :param AreaList: This field is required when RegionType is `customized`; it can be left empty when RegionType is `china` or `oversea`.
        :type AreaList: list of int
        """
        self.RegionType = None
        self.Action = None
        self.Id = None
        self.AreaList = None


    def _deserialize(self, params):
        self.RegionType = params.get("RegionType")
        self.Action = params.get("Action")
        self.Id = params.get("Id")
        self.AreaList = params.get("AreaList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CcGeoIpPolicyNew(AbstractModel):
    """Information of the policy list

    """

    def __init__(self):
        r"""
        :param PolicyId: Policy ID
        :type PolicyId: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP address
        :type Ip: str
        :param Domain: 
        :type Domain: str
        :param Protocol: Protocol. Valid values: `HTTP` and `HTTPS`.
        :type Protocol: str
        :param Action: Action. Valid values: `drop` and `alg`.
        :type Action: str
        :param RegionType: Region type. Valid values: `china`, `oversea` and `customized`.
        :type RegionType: str
        :param AreaList: ID list of regions to be blocked
        :type AreaList: list of int non-negative
        :param CreateTime: Creation time
        :type CreateTime: str
        :param ModifyTime: Modification time
        :type ModifyTime: str
        """
        self.PolicyId = None
        self.InstanceId = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None
        self.Action = None
        self.RegionType = None
        self.AreaList = None
        self.CreateTime = None
        self.ModifyTime = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        self.Action = params.get("Action")
        self.RegionType = params.get("RegionType")
        self.AreaList = params.get("AreaList")
        self.CreateTime = params.get("CreateTime")
        self.ModifyTime = params.get("ModifyTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CertIdInsL7Rules(AbstractModel):
    """Set of rules configured for certificates

    """

    def __init__(self):
        r"""
        :param L7Rules: List of rules configured for certificates
        :type L7Rules: list of InsL7Rules
        :param CertId: Certificate ID
        :type CertId: str
        """
        self.L7Rules = None
        self.CertId = None


    def _deserialize(self, params):
        if params.get("L7Rules") is not None:
            self.L7Rules = []
            for item in params.get("L7Rules"):
                obj = InsL7Rules()
                obj._deserialize(item)
                self.L7Rules.append(obj)
        self.CertId = params.get("CertId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBlackWhiteIpListRequest(AbstractModel):
    """CreateBlackWhiteIpList request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param IpList: List of IPs
        :type IpList: list of str
        :param Type: IP type. Valid values: `black` (blocklisted IP), `white`(allowlisted IP).
        :type Type: str
        """
        self.InstanceId = None
        self.IpList = None
        self.Type = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.IpList = params.get("IpList")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBlackWhiteIpListResponse(AbstractModel):
    """CreateBlackWhiteIpList response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateBoundIPRequest(AbstractModel):
    """CreateBoundIP request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type. `bgp`: Anti-DDoS Pro (Single IP); `bgp-multip`: Anti-DDoS Pro (Multi-IP)
        :type Business: str
        :param Id: Anti-DDoS instance ID
        :type Id: str
        :param BoundDevList: Array of IPs to bind to the Anti-DDoS instance. For Anti-DDoS Pro Single IP instance, the array contains only one IP. If there are no IPs to bind, it is empty; however, either `BoundDevList` or `UnBoundDevList` must not be empty.
        :type BoundDevList: list of BoundIpInfo
        :param UnBoundDevList: Array of IPs to unbind from the Anti-DDoS instance. For Anti-DDoS Pro Single IP instance, the array contains only one IP; if there are no IPs to unbind, it is empty; however, either `BoundDevList` or `UnBoundDevList` must not be empty.
        :type UnBoundDevList: list of BoundIpInfo
        :param CopyPolicy: Disused
        :type CopyPolicy: str
        """
        self.Business = None
        self.Id = None
        self.BoundDevList = None
        self.UnBoundDevList = None
        self.CopyPolicy = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.Id = params.get("Id")
        if params.get("BoundDevList") is not None:
            self.BoundDevList = []
            for item in params.get("BoundDevList"):
                obj = BoundIpInfo()
                obj._deserialize(item)
                self.BoundDevList.append(obj)
        if params.get("UnBoundDevList") is not None:
            self.UnBoundDevList = []
            for item in params.get("UnBoundDevList"):
                obj = BoundIpInfo()
                obj._deserialize(item)
                self.UnBoundDevList.append(obj)
        self.CopyPolicy = params.get("CopyPolicy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBoundIPResponse(AbstractModel):
    """CreateBoundIP response structure.

    """

    def __init__(self):
        r"""
        :param Success: Success code
        :type Success: :class:`tencentcloud.antiddos.v20200309.models.SuccessCode`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Success = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Success") is not None:
            self.Success = SuccessCode()
            self.Success._deserialize(params.get("Success"))
        self.RequestId = params.get("RequestId")


class CreateCCPrecisionPolicyRequest(AbstractModel):
    """CreateCCPrecisionPolicy request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP address
        :type Ip: str
        :param Protocol: Protocol. Valid values: `HTTP` and `HTTPS`.
        :type Protocol: str
        :param Domain: Domain name
        :type Domain: str
        :param PolicyAction: Action of limiting request frequency. Valid values: `alg` (limit request frequency via verification codes) and `drop`(drop requests).
        :type PolicyAction: str
        :param PolicyList: Policy records
        :type PolicyList: list of CCPrecisionPlyRecord
        """
        self.InstanceId = None
        self.Ip = None
        self.Protocol = None
        self.Domain = None
        self.PolicyAction = None
        self.PolicyList = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Protocol = params.get("Protocol")
        self.Domain = params.get("Domain")
        self.PolicyAction = params.get("PolicyAction")
        if params.get("PolicyList") is not None:
            self.PolicyList = []
            for item in params.get("PolicyList"):
                obj = CCPrecisionPlyRecord()
                obj._deserialize(item)
                self.PolicyList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCCPrecisionPolicyResponse(AbstractModel):
    """CreateCCPrecisionPolicy response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateCCReqLimitPolicyRequest(AbstractModel):
    """CreateCCReqLimitPolicy request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP address
        :type Ip: str
        :param Protocol: Protocol. Valid values: `HTTP` and `HTTPS`.
        :type Protocol: str
        :param Domain: Domain name
        :type Domain: str
        :param Policy: Configuration field
        :type Policy: :class:`tencentcloud.antiddos.v20200309.models.CCReqLimitPolicyRecord`
        :param IsGlobal: Whether it’s a global CC frequency limit
        :type IsGlobal: int
        """
        self.InstanceId = None
        self.Ip = None
        self.Protocol = None
        self.Domain = None
        self.Policy = None
        self.IsGlobal = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Protocol = params.get("Protocol")
        self.Domain = params.get("Domain")
        if params.get("Policy") is not None:
            self.Policy = CCReqLimitPolicyRecord()
            self.Policy._deserialize(params.get("Policy"))
        self.IsGlobal = params.get("IsGlobal")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCCReqLimitPolicyResponse(AbstractModel):
    """CreateCCReqLimitPolicy response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateCcBlackWhiteIpListRequest(AbstractModel):
    """CreateCcBlackWhiteIpList request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param IpList: List of IPs
        :type IpList: list of IpSegment
        :param Type: IP permission. Valid values: `black` (blocked IP), `white` (allowed IP).
        :type Type: str
        :param Ip: IP address
        :type Ip: str
        :param Domain: Domain name
        :type Domain: str
        :param Protocol: Protocol
        :type Protocol: str
        """
        self.InstanceId = None
        self.IpList = None
        self.Type = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("IpList") is not None:
            self.IpList = []
            for item in params.get("IpList"):
                obj = IpSegment()
                obj._deserialize(item)
                self.IpList.append(obj)
        self.Type = params.get("Type")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCcBlackWhiteIpListResponse(AbstractModel):
    """CreateCcBlackWhiteIpList response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateCcGeoIPBlockConfigRequest(AbstractModel):
    """CreateCcGeoIPBlockConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param IP: IP address
        :type IP: str
        :param Domain: Domain name
        :type Domain: str
        :param Protocol: Protocol type
        :type Protocol: str
        :param CcGeoIPBlockConfig: CC regional blocking configuration
        :type CcGeoIPBlockConfig: :class:`tencentcloud.antiddos.v20200309.models.CcGeoIPBlockConfig`
        """
        self.InstanceId = None
        self.IP = None
        self.Domain = None
        self.Protocol = None
        self.CcGeoIPBlockConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.IP = params.get("IP")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        if params.get("CcGeoIPBlockConfig") is not None:
            self.CcGeoIPBlockConfig = CcGeoIPBlockConfig()
            self.CcGeoIPBlockConfig._deserialize(params.get("CcGeoIPBlockConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCcGeoIPBlockConfigResponse(AbstractModel):
    """CreateCcGeoIPBlockConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDDoSAIRequest(AbstractModel):
    """CreateDDoSAI request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIdList: List of Anti-DDoS instance IDs
        :type InstanceIdList: list of str
        :param DDoSAI: AI protection switch. Valid values:
`on`: enabled
`off`: disabled
]
        :type DDoSAI: str
        """
        self.InstanceIdList = None
        self.DDoSAI = None


    def _deserialize(self, params):
        self.InstanceIdList = params.get("InstanceIdList")
        self.DDoSAI = params.get("DDoSAI")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDDoSAIResponse(AbstractModel):
    """CreateDDoSAI response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDDoSGeoIPBlockConfigRequest(AbstractModel):
    """CreateDDoSGeoIPBlockConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param DDoSGeoIPBlockConfig: Region blocking configuration. The configuration ID should be cleared when you set this parameter.
        :type DDoSGeoIPBlockConfig: :class:`tencentcloud.antiddos.v20200309.models.DDoSGeoIPBlockConfig`
        """
        self.InstanceId = None
        self.DDoSGeoIPBlockConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DDoSGeoIPBlockConfig") is not None:
            self.DDoSGeoIPBlockConfig = DDoSGeoIPBlockConfig()
            self.DDoSGeoIPBlockConfig._deserialize(params.get("DDoSGeoIPBlockConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDDoSGeoIPBlockConfigResponse(AbstractModel):
    """CreateDDoSGeoIPBlockConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDDoSSpeedLimitConfigRequest(AbstractModel):
    """CreateDDoSSpeedLimitConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param DDoSSpeedLimitConfig: Access rate limit configuration. The configuration ID should be cleared when you set this parameter.
        :type DDoSSpeedLimitConfig: :class:`tencentcloud.antiddos.v20200309.models.DDoSSpeedLimitConfig`
        """
        self.InstanceId = None
        self.DDoSSpeedLimitConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DDoSSpeedLimitConfig") is not None:
            self.DDoSSpeedLimitConfig = DDoSSpeedLimitConfig()
            self.DDoSSpeedLimitConfig._deserialize(params.get("DDoSSpeedLimitConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDDoSSpeedLimitConfigResponse(AbstractModel):
    """CreateDDoSSpeedLimitConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDefaultAlarmThresholdRequest(AbstractModel):
    """CreateDefaultAlarmThreshold request structure.

    """

    def __init__(self):
        r"""
        :param DefaultAlarmConfig: Default alarm threshold configuration
        :type DefaultAlarmConfig: :class:`tencentcloud.antiddos.v20200309.models.DefaultAlarmThreshold`
        :param InstanceType: Product category. Valid values:
`bgp`: Anti-DDoS Pro
`bgpip`: Anti-DDoS Advanced
]
        :type InstanceType: str
        """
        self.DefaultAlarmConfig = None
        self.InstanceType = None


    def _deserialize(self, params):
        if params.get("DefaultAlarmConfig") is not None:
            self.DefaultAlarmConfig = DefaultAlarmThreshold()
            self.DefaultAlarmConfig._deserialize(params.get("DefaultAlarmConfig"))
        self.InstanceType = params.get("InstanceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDefaultAlarmThresholdResponse(AbstractModel):
    """CreateDefaultAlarmThreshold response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateIPAlarmThresholdConfigRequest(AbstractModel):
    """CreateIPAlarmThresholdConfig request structure.

    """

    def __init__(self):
        r"""
        :param IpAlarmThresholdConfigList: List of IP alarm threshold configurations
        :type IpAlarmThresholdConfigList: list of IPAlarmThresholdRelation
        """
        self.IpAlarmThresholdConfigList = None


    def _deserialize(self, params):
        if params.get("IpAlarmThresholdConfigList") is not None:
            self.IpAlarmThresholdConfigList = []
            for item in params.get("IpAlarmThresholdConfigList"):
                obj = IPAlarmThresholdRelation()
                obj._deserialize(item)
                self.IpAlarmThresholdConfigList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateIPAlarmThresholdConfigResponse(AbstractModel):
    """CreateIPAlarmThresholdConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateL7RuleCertsRequest(AbstractModel):
    """CreateL7RuleCerts request structure.

    """

    def __init__(self):
        r"""
        :param CertId: SSL certificate ID
        :type CertId: str
        :param L7Rules: List of Layer-7 domain name forwarding rules
        :type L7Rules: list of InsL7Rules
        """
        self.CertId = None
        self.L7Rules = None


    def _deserialize(self, params):
        self.CertId = params.get("CertId")
        if params.get("L7Rules") is not None:
            self.L7Rules = []
            for item in params.get("L7Rules"):
                obj = InsL7Rules()
                obj._deserialize(item)
                self.L7Rules.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateL7RuleCertsResponse(AbstractModel):
    """CreateL7RuleCerts response structure.

    """

    def __init__(self):
        r"""
        :param Success: Success code
        :type Success: :class:`tencentcloud.antiddos.v20200309.models.SuccessCode`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Success = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Success") is not None:
            self.Success = SuccessCode()
            self.Success._deserialize(params.get("Success"))
        self.RequestId = params.get("RequestId")


class CreateNewL7RulesRequest(AbstractModel):
    """CreateNewL7Rules request structure.

    """

    def __init__(self):
        r"""
        :param Rules: List of rules
        :type Rules: list of L7RuleEntry
        :param Business: Anti-DDoS service type (`bgpip`: Anti-DDoS Advanced)
        :type Business: str
        :param IdList: List of resource IDs
        :type IdList: list of str
        :param VipList: List of resource IPs
        :type VipList: list of str
        """
        self.Rules = None
        self.Business = None
        self.IdList = None
        self.VipList = None


    def _deserialize(self, params):
        if params.get("Rules") is not None:
            self.Rules = []
            for item in params.get("Rules"):
                obj = L7RuleEntry()
                obj._deserialize(item)
                self.Rules.append(obj)
        self.Business = params.get("Business")
        self.IdList = params.get("IdList")
        self.VipList = params.get("VipList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateNewL7RulesResponse(AbstractModel):
    """CreateNewL7Rules response structure.

    """

    def __init__(self):
        r"""
        :param Success: Success code
        :type Success: :class:`tencentcloud.antiddos.v20200309.models.SuccessCode`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Success = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Success") is not None:
            self.Success = SuccessCode()
            self.Success._deserialize(params.get("Success"))
        self.RequestId = params.get("RequestId")


class CreatePacketFilterConfigRequest(AbstractModel):
    """CreatePacketFilterConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param PacketFilterConfig: Feature filtering rules
        :type PacketFilterConfig: :class:`tencentcloud.antiddos.v20200309.models.PacketFilterConfig`
        """
        self.InstanceId = None
        self.PacketFilterConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("PacketFilterConfig") is not None:
            self.PacketFilterConfig = PacketFilterConfig()
            self.PacketFilterConfig._deserialize(params.get("PacketFilterConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePacketFilterConfigResponse(AbstractModel):
    """CreatePacketFilterConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateProtocolBlockConfigRequest(AbstractModel):
    """CreateProtocolBlockConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param ProtocolBlockConfig: Protocol blocking configuration
        :type ProtocolBlockConfig: :class:`tencentcloud.antiddos.v20200309.models.ProtocolBlockConfig`
        """
        self.InstanceId = None
        self.ProtocolBlockConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("ProtocolBlockConfig") is not None:
            self.ProtocolBlockConfig = ProtocolBlockConfig()
            self.ProtocolBlockConfig._deserialize(params.get("ProtocolBlockConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateProtocolBlockConfigResponse(AbstractModel):
    """CreateProtocolBlockConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateSchedulingDomainRequest(AbstractModel):
    """CreateSchedulingDomain request structure.

    """

    def __init__(self):
        r"""
        :param Product: Indicates whether a hybrid cloud product is used.
`hybrid`: Anti-DDoS Service Platform
For other products, leave this field empty.
        :type Product: str
        """
        self.Product = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSchedulingDomainResponse(AbstractModel):
    """CreateSchedulingDomain response structure.

    """

    def __init__(self):
        r"""
        :param Domain: Created domain name
        :type Domain: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Domain = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Domain = params.get("Domain")
        self.RequestId = params.get("RequestId")


class CreateWaterPrintConfigRequest(AbstractModel):
    """CreateWaterPrintConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param WaterPrintConfig: Watermark configuration
        :type WaterPrintConfig: :class:`tencentcloud.antiddos.v20200309.models.WaterPrintConfig`
        """
        self.InstanceId = None
        self.WaterPrintConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("WaterPrintConfig") is not None:
            self.WaterPrintConfig = WaterPrintConfig()
            self.WaterPrintConfig._deserialize(params.get("WaterPrintConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateWaterPrintConfigResponse(AbstractModel):
    """CreateWaterPrintConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateWaterPrintKeyRequest(AbstractModel):
    """CreateWaterPrintKey request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateWaterPrintKeyResponse(AbstractModel):
    """CreateWaterPrintKey response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DDoSAIRelation(AbstractModel):
    """Anti-DDoS AI protection switch

    """

    def __init__(self):
        r"""
        :param DDoSAI: AI protection switch. Valid values:
`on`: enabled
`off`: disabled
]
        :type DDoSAI: str
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        """
        self.DDoSAI = None
        self.InstanceDetailList = None


    def _deserialize(self, params):
        self.DDoSAI = params.get("DDoSAI")
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DDoSGeoIPBlockConfig(AbstractModel):
    """Anti-DDoS region blocking configuration

    """

    def __init__(self):
        r"""
        :param RegionType: Region type. Valid values:
`oversea`: Outside the Chinese mainland
`china`: The Chinese mainland
`customized`: User-specified region
]
        :type RegionType: str
        :param Action: Blocking action. Valid values:
`drop`: the request is blocked.
`trans`: the request is allowed.
]
        :type Action: str
        :param Id: Configuration ID, which is generated after a configuration is added. This field is only required to modify or delete a configuration.
        :type Id: str
        :param AreaList: When `RegionType = customized`, AreaList is required and contains up to 128 areas.
        :type AreaList: list of int
        """
        self.RegionType = None
        self.Action = None
        self.Id = None
        self.AreaList = None


    def _deserialize(self, params):
        self.RegionType = params.get("RegionType")
        self.Action = params.get("Action")
        self.Id = params.get("Id")
        self.AreaList = params.get("AreaList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DDoSGeoIPBlockConfigRelation(AbstractModel):
    """Anti-DDoS region blocking configuration details

    """

    def __init__(self):
        r"""
        :param GeoIPBlockConfig: Anti-DDoS region blocking configuration
        :type GeoIPBlockConfig: :class:`tencentcloud.antiddos.v20200309.models.DDoSGeoIPBlockConfig`
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        """
        self.GeoIPBlockConfig = None
        self.InstanceDetailList = None


    def _deserialize(self, params):
        if params.get("GeoIPBlockConfig") is not None:
            self.GeoIPBlockConfig = DDoSGeoIPBlockConfig()
            self.GeoIPBlockConfig._deserialize(params.get("GeoIPBlockConfig"))
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DDoSSpeedLimitConfig(AbstractModel):
    """Anti-DDoS access rate limit configuration

    """

    def __init__(self):
        r"""
        :param Mode: Rate limit mode. Valid values:
`1`: rate limit based on the real server IP
`2`: rate limit based on the destination port
]
        :type Mode: int
        :param SpeedValues: Rate limit value. This field contains at least one valid rate limit type. Note that only up to one value of each type is supported.
        :type SpeedValues: list of SpeedValue
        :param DstPortScopes: This field is replaced with a new field DstPortList.
        :type DstPortScopes: list of PortSegment
        :param Id: 
        :type Id: str
        :param ProtocolList: IP protocol number. Valid values:
`ALL`: all protocols
`TCP`: TCP protocol
`UDP`: UDP protocol
`SMP`: SMP protocol
`1;2–100`: user-defined protocol with up to 8 ranges
]
Note: For custom protocol ranges, only protocol number is supported. Multiple ranges are separated by ";". If the value is `ALL`, any other protocol or protocol number should be excluded.
        :type ProtocolList: str
        :param DstPortList: Port range list, which contains up to 8 ranges. Use ";" to separate multiple ports and "–" to indicate a range of ports, as described in the following formats: `0–65535`, `80;443;1000–2000`.
        :type DstPortList: str
        """
        self.Mode = None
        self.SpeedValues = None
        self.DstPortScopes = None
        self.Id = None
        self.ProtocolList = None
        self.DstPortList = None


    def _deserialize(self, params):
        self.Mode = params.get("Mode")
        if params.get("SpeedValues") is not None:
            self.SpeedValues = []
            for item in params.get("SpeedValues"):
                obj = SpeedValue()
                obj._deserialize(item)
                self.SpeedValues.append(obj)
        if params.get("DstPortScopes") is not None:
            self.DstPortScopes = []
            for item in params.get("DstPortScopes"):
                obj = PortSegment()
                obj._deserialize(item)
                self.DstPortScopes.append(obj)
        self.Id = params.get("Id")
        self.ProtocolList = params.get("ProtocolList")
        self.DstPortList = params.get("DstPortList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DDoSSpeedLimitConfigRelation(AbstractModel):
    """DDoS access rate limit configuration details

    """

    def __init__(self):
        r"""
        :param SpeedLimitConfig: Anti-DDoS access rate limit configuration
        :type SpeedLimitConfig: :class:`tencentcloud.antiddos.v20200309.models.DDoSSpeedLimitConfig`
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        """
        self.SpeedLimitConfig = None
        self.InstanceDetailList = None


    def _deserialize(self, params):
        if params.get("SpeedLimitConfig") is not None:
            self.SpeedLimitConfig = DDoSSpeedLimitConfig()
            self.SpeedLimitConfig._deserialize(params.get("SpeedLimitConfig"))
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DefaultAlarmThreshold(AbstractModel):
    """Default alarm threshold configuration of an IP

    """

    def __init__(self):
        r"""
        :param AlarmType: Alarm threshold type. Valid values:
`1`: alarm threshold for inbound traffic
`2`: alarm threshold for cleansing attack traffic
]
        :type AlarmType: int
        :param AlarmThreshold: Alarm threshold (Mbps). The value should be greater than or equal to 0. Note that the alarm threshold configuration will be removed if you pass the parameter for input and set it to 0.
        :type AlarmThreshold: int
        """
        self.AlarmType = None
        self.AlarmThreshold = None


    def _deserialize(self, params):
        self.AlarmType = params.get("AlarmType")
        self.AlarmThreshold = params.get("AlarmThreshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCCLevelPolicyRequest(AbstractModel):
    """DeleteCCLevelPolicy request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: Target IP of the policy
        :type Ip: str
        :param Domain: Domain name
        :type Domain: str
        :param Protocol: Value: `http`
        :type Protocol: str
        """
        self.InstanceId = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCCLevelPolicyResponse(AbstractModel):
    """DeleteCCLevelPolicy response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCCPrecisionPolicyRequest(AbstractModel):
    """DeleteCCPrecisionPolicy request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param PolicyId: Policy ID
        :type PolicyId: str
        """
        self.InstanceId = None
        self.PolicyId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.PolicyId = params.get("PolicyId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCCPrecisionPolicyResponse(AbstractModel):
    """DeleteCCPrecisionPolicy response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCCThresholdPolicyRequest(AbstractModel):
    """DeleteCCThresholdPolicy request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: Target IP of the policy
        :type Ip: str
        :param Domain: Domain name
        :type Domain: str
        :param Protocol: Value: `http`
        :type Protocol: str
        """
        self.InstanceId = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCCThresholdPolicyResponse(AbstractModel):
    """DeleteCCThresholdPolicy response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCcBlackWhiteIpListRequest(AbstractModel):
    """DeleteCcBlackWhiteIpList request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param PolicyId: Policy ID
        :type PolicyId: str
        """
        self.InstanceId = None
        self.PolicyId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.PolicyId = params.get("PolicyId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCcBlackWhiteIpListResponse(AbstractModel):
    """DeleteCcBlackWhiteIpList response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCcGeoIPBlockConfigRequest(AbstractModel):
    """DeleteCcGeoIPBlockConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param CcGeoIPBlockConfig: Region blocking configuration. The configuration ID cannot be empty when you set this parameter.
        :type CcGeoIPBlockConfig: :class:`tencentcloud.antiddos.v20200309.models.CcGeoIPBlockConfig`
        """
        self.InstanceId = None
        self.CcGeoIPBlockConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("CcGeoIPBlockConfig") is not None:
            self.CcGeoIPBlockConfig = CcGeoIPBlockConfig()
            self.CcGeoIPBlockConfig._deserialize(params.get("CcGeoIPBlockConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCcGeoIPBlockConfigResponse(AbstractModel):
    """DeleteCcGeoIPBlockConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDDoSGeoIPBlockConfigRequest(AbstractModel):
    """DeleteDDoSGeoIPBlockConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param DDoSGeoIPBlockConfig: Region blocking configuration. The configuration ID cannot be empty when you set this parameter.
        :type DDoSGeoIPBlockConfig: :class:`tencentcloud.antiddos.v20200309.models.DDoSGeoIPBlockConfig`
        """
        self.InstanceId = None
        self.DDoSGeoIPBlockConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DDoSGeoIPBlockConfig") is not None:
            self.DDoSGeoIPBlockConfig = DDoSGeoIPBlockConfig()
            self.DDoSGeoIPBlockConfig._deserialize(params.get("DDoSGeoIPBlockConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDDoSGeoIPBlockConfigResponse(AbstractModel):
    """DeleteDDoSGeoIPBlockConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDDoSSpeedLimitConfigRequest(AbstractModel):
    """DeleteDDoSSpeedLimitConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param DDoSSpeedLimitConfig: Access rate limit configuration. The configuration ID cannot be empty when you set this parameter.
        :type DDoSSpeedLimitConfig: :class:`tencentcloud.antiddos.v20200309.models.DDoSSpeedLimitConfig`
        """
        self.InstanceId = None
        self.DDoSSpeedLimitConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DDoSSpeedLimitConfig") is not None:
            self.DDoSSpeedLimitConfig = DDoSSpeedLimitConfig()
            self.DDoSSpeedLimitConfig._deserialize(params.get("DDoSSpeedLimitConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDDoSSpeedLimitConfigResponse(AbstractModel):
    """DeleteDDoSSpeedLimitConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeletePacketFilterConfigRequest(AbstractModel):
    """DeletePacketFilterConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param PacketFilterConfig: Feature filtering configuration
        :type PacketFilterConfig: :class:`tencentcloud.antiddos.v20200309.models.PacketFilterConfig`
        """
        self.InstanceId = None
        self.PacketFilterConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("PacketFilterConfig") is not None:
            self.PacketFilterConfig = PacketFilterConfig()
            self.PacketFilterConfig._deserialize(params.get("PacketFilterConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePacketFilterConfigResponse(AbstractModel):
    """DeletePacketFilterConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteWaterPrintConfigRequest(AbstractModel):
    """DeleteWaterPrintConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteWaterPrintConfigResponse(AbstractModel):
    """DeleteWaterPrintConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteWaterPrintKeyRequest(AbstractModel):
    """DeleteWaterPrintKey request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param KeyId: Watermark key ID
        :type KeyId: str
        """
        self.InstanceId = None
        self.KeyId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.KeyId = params.get("KeyId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteWaterPrintKeyResponse(AbstractModel):
    """DeleteWaterPrintKey response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeBasicDeviceStatusRequest(AbstractModel):
    """DescribeBasicDeviceStatus request structure.

    """

    def __init__(self):
        r"""
        :param IpList: List of IP resources
        :type IpList: list of str
        """
        self.IpList = None


    def _deserialize(self, params):
        self.IpList = params.get("IpList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBasicDeviceStatusResponse(AbstractModel):
    """DescribeBasicDeviceStatus response structure.

    """

    def __init__(self):
        r"""
        :param Data: Status of the specified Anti-DDoS resource. Valid values:
`1`: The IP is blocked.
`2`: The P is normal.
`3`: The IP is being attacked.
        :type Data: list of KeyValue
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = KeyValue()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBgpBizTrendRequest(AbstractModel):
    """DescribeBgpBizTrend request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service code. `bgp-multip` indicates Anti-DDos Pro.
        :type Business: str
        :param StartTime: Beginning of the time range for the query, such as `2020-09-22 00:00:00`.
        :type StartTime: str
        :param EndTime: End of the time range for the query, such as `2020-09-22 00:00:00`.
        :type EndTime: str
        :param MetricName: Statistical metric. Values: `intraffic`, `outtraffic`, `inpkg`, and `outpkg`.
        :type MetricName: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Flag: `0`: Fixed time. `1`: Custom time.
        :type Flag: int
        """
        self.Business = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None
        self.InstanceId = None
        self.Flag = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")
        self.InstanceId = params.get("InstanceId")
        self.Flag = params.get("Flag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBgpBizTrendResponse(AbstractModel):
    """DescribeBgpBizTrend response structure.

    """

    def __init__(self):
        r"""
        :param DataList: Values of the samples
        :type DataList: list of int non-negative
        :param Total: Number of samples
        :type Total: int
        :param MetricName: Statistical metric
        :type MetricName: str
        :param MaxData: Maximum value of the arrays returned
        :type MaxData: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DataList = None
        self.Total = None
        self.MetricName = None
        self.MaxData = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DataList = params.get("DataList")
        self.Total = params.get("Total")
        self.MetricName = params.get("MetricName")
        self.MaxData = params.get("MaxData")
        self.RequestId = params.get("RequestId")


class DescribeBizHttpStatusRequest(AbstractModel):
    """DescribeBizHttpStatus request structure.

    """

    def __init__(self):
        r"""
        :param Statistics: Statistical mode. Value: `sum`.
        :type Statistics: str
        :param Business: Anti-DDoS service type (`bgpip`: Anti-DDoS Advanced)
        :type Business: str
        :param Period: Statistical period in seconds. Valid values: `60`, `300`, `1800`, `3600`, `21600`, and `86400`.
        :type Period: int
        :param StartTime: Statistics start time, such as `2020-02-01 12:04:12`
        :type StartTime: str
        :param EndTime: Statistics end time, such as `2020-02-03 18:03:23`
        :type EndTime: str
        :param Id: The resource ID.
        :type Id: str
        :param Domain: Specific domain name query
        :type Domain: str
        :param ProtoInfo: Protocol and port list, which is valid when the metric is `connum`, `new_conn` or `inactive_conn`. Valid protocols: `TCP`, `UDP`, `HTTP`, `HTTPS`
        :type ProtoInfo: list of ProtocolPort
        """
        self.Statistics = None
        self.Business = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None
        self.Id = None
        self.Domain = None
        self.ProtoInfo = None


    def _deserialize(self, params):
        self.Statistics = params.get("Statistics")
        self.Business = params.get("Business")
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Id = params.get("Id")
        self.Domain = params.get("Domain")
        if params.get("ProtoInfo") is not None:
            self.ProtoInfo = []
            for item in params.get("ProtoInfo"):
                obj = ProtocolPort()
                obj._deserialize(item)
                self.ProtoInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBizHttpStatusResponse(AbstractModel):
    """DescribeBizHttpStatus response structure.

    """

    def __init__(self):
        r"""
        :param HttpStatusMap: Statistics on the HTTP status codes of business traffic
        :type HttpStatusMap: :class:`tencentcloud.antiddos.v20200309.models.HttpStatusMap`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.HttpStatusMap = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("HttpStatusMap") is not None:
            self.HttpStatusMap = HttpStatusMap()
            self.HttpStatusMap._deserialize(params.get("HttpStatusMap"))
        self.RequestId = params.get("RequestId")


class DescribeBizTrendRequest(AbstractModel):
    """DescribeBizTrend request structure.

    """

    def __init__(self):
        r"""
        :param Statistics: Statistical method. Valid values: `max`, `min`, `avg`, `sum`. It can only be `max` if the statistical dimension is traffic rate or packet rate.
        :type Statistics: str
        :param Business: Anti-DDoS service type (`bgpip`: Anti-DDoS Advanced)
        :type Business: str
        :param Period: Sampling interval in seconds. Valid values: `60`, `300`, `1800`, `3600`, `21600`, `86400`
        :type Period: int
        :param StartTime: Beginning of the time range for the query, such as `2020-09-22 00:00:00`.
        :type StartTime: str
        :param EndTime: End of the time range for the query, such as `2020-09-22 00:00:00`.
        :type EndTime: str
        :param Id: Instance ID
        :type Id: str
        :param MetricName: Metric. Valid values: `connum`, `new_conn`, `inactive_conn`, `intraffic`, `outtraffic`, `inpkg`, `outpkg`, `qps`
        :type MetricName: str
        :param Domain: You can query data by specifying a domain name when the metric is `qps`.
        :type Domain: str
        :param ProtoInfo: Protocol and port list, which is valid when the metric is `connum`, `new_conn` or `inactive_conn`. Valid protocols: `TCP`, `UDP`, `HTTP`, `HTTPS`
        :type ProtoInfo: list of ProtocolPort
        """
        self.Statistics = None
        self.Business = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None
        self.Id = None
        self.MetricName = None
        self.Domain = None
        self.ProtoInfo = None


    def _deserialize(self, params):
        self.Statistics = params.get("Statistics")
        self.Business = params.get("Business")
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Id = params.get("Id")
        self.MetricName = params.get("MetricName")
        self.Domain = params.get("Domain")
        if params.get("ProtoInfo") is not None:
            self.ProtoInfo = []
            for item in params.get("ProtoInfo"):
                obj = ProtocolPort()
                obj._deserialize(item)
                self.ProtoInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBizTrendResponse(AbstractModel):
    """DescribeBizTrend response structure.

    """

    def __init__(self):
        r"""
        :param DataList: Value at a time point on the curve
        :type DataList: list of float
        :param MetricName: Statistical dimension
        :type MetricName: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DataList = None
        self.MetricName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DataList = params.get("DataList")
        self.MetricName = params.get("MetricName")
        self.RequestId = params.get("RequestId")


class DescribeBlackWhiteIpListRequest(AbstractModel):
    """DescribeBlackWhiteIpList request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBlackWhiteIpListResponse(AbstractModel):
    """DescribeBlackWhiteIpList response structure.

    """

    def __init__(self):
        r"""
        :param BlackIpList: IP blocklist
        :type BlackIpList: list of str
        :param WhiteIpList: IP allowlist
        :type WhiteIpList: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BlackIpList = None
        self.WhiteIpList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BlackIpList = params.get("BlackIpList")
        self.WhiteIpList = params.get("WhiteIpList")
        self.RequestId = params.get("RequestId")


class DescribeCCLevelListRequest(AbstractModel):
    """DescribeCCLevelList request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service code. `bgp-multip` indicates Anti-DDos Pro.
        :type Business: str
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of results returned in one page
        :type Limit: int
        :param InstanceId: ID of the specified instance
        :type InstanceId: str
        """
        self.Business = None
        self.Offset = None
        self.Limit = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCCLevelListResponse(AbstractModel):
    """DescribeCCLevelList response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of level-defining policies
        :type Total: int
        :param LevelList: Total number of level-defining policies
        :type LevelList: list of CCLevelPolicy
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.LevelList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("LevelList") is not None:
            self.LevelList = []
            for item in params.get("LevelList"):
                obj = CCLevelPolicy()
                obj._deserialize(item)
                self.LevelList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCCLevelPolicyRequest(AbstractModel):
    """DescribeCCLevelPolicy request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP
        :type Ip: str
        :param Domain: Domain name
        :type Domain: str
        :param Protocol: Protocol. Values: `HTTP`，`HTTPS`
        :type Protocol: str
        """
        self.InstanceId = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCCLevelPolicyResponse(AbstractModel):
    """DescribeCCLevelPolicy response structure.

    """

    def __init__(self):
        r"""
        :param Level: CC protection level. Vaules: `loose`, `strict`, `normal`, `emergency`, `sup_loose` (super loose), `default` (used when the frequency limit is not configured) and `customized`
        :type Level: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Level = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Level = params.get("Level")
        self.RequestId = params.get("RequestId")


class DescribeCCPrecisionPlyListRequest(AbstractModel):
    """DescribeCCPrecisionPlyList request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type. Valid values: `bgpip-multip` (Anti-DDoS Pro) and `bgpip` (Anti-DDoS Advanced).
        :type Business: str
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of results returned in one page
        :type Limit: int
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP address, which is required when an Anti-DDoS Advanced instance is used.
        :type Ip: str
        :param Domain: Domain name, which is required when an Anti-DDoS Advanced instance is used.
        :type Domain: str
        :param Protocol: Protocol, which is required when an Anti-DDoS Advanced instance is used.
        :type Protocol: str
        """
        self.Business = None
        self.Offset = None
        self.Limit = None
        self.InstanceId = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCCPrecisionPlyListResponse(AbstractModel):
    """DescribeCCPrecisionPlyList response structure.

    """

    def __init__(self):
        r"""
        :param Total: Number of policy lists
        :type Total: int
        :param PrecisionPolicyList: Information of the policy list
        :type PrecisionPolicyList: list of CCPrecisionPolicy
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.PrecisionPolicyList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("PrecisionPolicyList") is not None:
            self.PrecisionPolicyList = []
            for item in params.get("PrecisionPolicyList"):
                obj = CCPrecisionPolicy()
                obj._deserialize(item)
                self.PrecisionPolicyList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCCThresholdListRequest(AbstractModel):
    """DescribeCCThresholdList request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service code. `bgp-multip` indicates Anti-DDos Pro.
        :type Business: str
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of results returned in one page
        :type Limit: int
        :param InstanceId: ID of the specified instance
        :type InstanceId: str
        """
        self.Business = None
        self.Offset = None
        self.Limit = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCCThresholdListResponse(AbstractModel):
    """DescribeCCThresholdList response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of cleansing threshold policies
        :type Total: int
        :param ThresholdList: Details of cleansing threshold policies
        :type ThresholdList: list of CCThresholdPolicy
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ThresholdList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ThresholdList") is not None:
            self.ThresholdList = []
            for item in params.get("ThresholdList"):
                obj = CCThresholdPolicy()
                obj._deserialize(item)
                self.ThresholdList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCCTrendRequest(AbstractModel):
    """DescribeCCTrend request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type. `bgpip`: Anti-DDoS Advanced; `bgp`: Anti-DDoS Pro (Single IP); `bgp-multip`: Anti-DDoS Pro (Multi-IP); `net`: Anti-DDoS Ultimate; `basic`: Anti-DDoS Basic
        :type Business: str
        :param Ip: Instance IP
        :type Ip: str
        :param Period: Sampling period. Valid values: `300` (5 minutes), `3600` (one hour), `86400` (one day)
        :type Period: int
        :param StartTime: Beginning of the time range for the query
        :type StartTime: str
        :param EndTime: End of the time range for the query
        :type EndTime: str
        :param MetricName: Metric. Valid values: `inqps` (total QPS peaks), `dropqps` (attack QPS peaks), `incount` (total number of requests), and `dropcount` (number of attack requests).
        :type MetricName: str
        :param Domain: (Optional) Domain name
        :type Domain: str
        :param Id: Instance ID. Leave this field empty when `Business` is `basic`, as basic protection does not require an instance.
        :type Id: str
        """
        self.Business = None
        self.Ip = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None
        self.Domain = None
        self.Id = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.Ip = params.get("Ip")
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")
        self.Domain = params.get("Domain")
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCCTrendResponse(AbstractModel):
    """DescribeCCTrend response structure.

    """

    def __init__(self):
        r"""
        :param Count: Number of values returned
        :type Count: int
        :param Business: Anti-DDoS service type. `bgpip`: Anti-DDoS Advanced; `bgp`: Anti-DDoS Pro (Single IP); `bgp-multip`: Anti-DDoS Pro (Multi-IP); `net`: Anti-DDoS Ultimate; `basic`: Anti-DDoS Basic
        :type Business: str
        :param Ip: Instance IP
        :type Ip: str
        :param Period: Sampling period. Valid values: `300` (5 minutes), `3600` (one hour), `86400` (one day)
        :type Period: int
        :param StartTime: Beginning of the time range for the query
        :type StartTime: str
        :param EndTime: End of the time range for the query
        :type EndTime: str
        :param Data: Value array
        :type Data: list of int non-negative
        :param Id: Instance ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Id: str
        :param MetricName: Metric. Valid values: `inqps` (total QPS peaks), `dropqps` (attack QPS peaks), `incount` (total number of requests), and `dropcount` (number of attack requests).
        :type MetricName: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Count = None
        self.Business = None
        self.Ip = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None
        self.Data = None
        self.Id = None
        self.MetricName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.Business = params.get("Business")
        self.Ip = params.get("Ip")
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Data = params.get("Data")
        self.Id = params.get("Id")
        self.MetricName = params.get("MetricName")
        self.RequestId = params.get("RequestId")


class DescribeCcBlackWhiteIpListRequest(AbstractModel):
    """DescribeCcBlackWhiteIpList request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type. Valid values: `bgpip-multip` (Anti-DDoS Pro) and `bgpip` (Anti-DDoS Advanced).
        :type Business: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of results returned in one page
        :type Limit: int
        :param Ip: IP address, which is required when an Anti-DDoS Advanced instance is used.
        :type Ip: str
        :param Domain: Domain name, which is required when an Anti-DDoS Advanced instance is used.
        :type Domain: str
        :param Protocol: Protocol, which is required when an Anti-DDoS Advanced instance is used.
        :type Protocol: str
        :param FilterIp: Specifies a blocklist/allowlist IP.
        :type FilterIp: str
        :param FilterType: Specifies whether is an IP blocklist or IP allowlist.
        :type FilterType: str
        """
        self.Business = None
        self.InstanceId = None
        self.Offset = None
        self.Limit = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None
        self.FilterIp = None
        self.FilterType = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.InstanceId = params.get("InstanceId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        self.FilterIp = params.get("FilterIp")
        self.FilterType = params.get("FilterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCcBlackWhiteIpListResponse(AbstractModel):
    """DescribeCcBlackWhiteIpList response structure.

    """

    def __init__(self):
        r"""
        :param Total: Number of policy lists
        :type Total: int
        :param CcBlackWhiteIpList: Information of the policy list
        :type CcBlackWhiteIpList: list of CcBlackWhiteIpPolicy
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.CcBlackWhiteIpList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("CcBlackWhiteIpList") is not None:
            self.CcBlackWhiteIpList = []
            for item in params.get("CcBlackWhiteIpList"):
                obj = CcBlackWhiteIpPolicy()
                obj._deserialize(item)
                self.CcBlackWhiteIpList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCcGeoIPBlockConfigListRequest(AbstractModel):
    """DescribeCcGeoIPBlockConfigList request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type. Valid values: `bgpip-multip` (Anti-DDoS Pro) and `bgpip` (Anti-DDoS Advanced).
        :type Business: str
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of results returned in one page
        :type Limit: int
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Ip: IP address, which is required when an Anti-DDoS Advanced instance is used.
        :type Ip: str
        :param Domain: Domain name, which is required when an Anti-DDoS Advanced instance is used.
        :type Domain: str
        :param Protocol: Protocol, which is required when an Anti-DDoS Advanced instance is used.
        :type Protocol: str
        """
        self.Business = None
        self.Offset = None
        self.Limit = None
        self.InstanceId = None
        self.Ip = None
        self.Domain = None
        self.Protocol = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InstanceId = params.get("InstanceId")
        self.Ip = params.get("Ip")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCcGeoIPBlockConfigListResponse(AbstractModel):
    """DescribeCcGeoIPBlockConfigList response structure.

    """

    def __init__(self):
        r"""
        :param Total: Number of policy lists
        :type Total: int
        :param CcGeoIpPolicyList: Information of the policy list
        :type CcGeoIpPolicyList: list of CcGeoIpPolicyNew
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.CcGeoIpPolicyList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("CcGeoIpPolicyList") is not None:
            self.CcGeoIpPolicyList = []
            for item in params.get("CcGeoIpPolicyList"):
                obj = CcGeoIpPolicyNew()
                obj._deserialize(item)
                self.CcGeoIpPolicyList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDDoSTrendRequest(AbstractModel):
    """DescribeDDoSTrend request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type. `bgpip`: Anti-DDoS Advanced; `bgp`: Anti-DDoS Pro (Single IP); `bgp-multip`: Anti-DDoS Pro (Multi-IP); `net`: Anti-DDoS Ultimate; `basic`: Anti-DDoS Basic
        :type Business: str
        :param Ip: Instance IP
        :type Ip: str
        :param Period: Sampling period. Valid values: `300` (5 minutes), `3600` (one hour), `86400` (one day)
        :type Period: int
        :param StartTime: Beginning of the time range for the query
        :type StartTime: str
        :param EndTime: End of the time range for the query
        :type EndTime: str
        :param MetricName: Metric. Valid values: `bps`: attack traffic bandwidth; `pps`: attack packet rate
        :type MetricName: str
        :param Id: Instance ID. Leave this field empty when `Business` is `basic`, as basic protection does not require an instance.
        :type Id: str
        """
        self.Business = None
        self.Ip = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None
        self.Id = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.Ip = params.get("Ip")
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDDoSTrendResponse(AbstractModel):
    """DescribeDDoSTrend response structure.

    """

    def __init__(self):
        r"""
        :param Count: Number of values returned
        :type Count: int
        :param Business: Anti-DDoS service type. `bgpip`: Anti-DDoS Advanced; `bgp`: Anti-DDoS Pro (Single IP); `bgp-multip`: Anti-DDoS Pro (Multi-IP); `net`: Anti-DDoS Ultimate; `basic`: Anti-DDoS Basic
        :type Business: str
        :param Ip: Instance IP
        :type Ip: str
        :param Period: Sampling period. Valid values: `300` (5 minutes), `3600` (one hour), `86400` (one day)
        :type Period: int
        :param StartTime: Beginning of the time range for the query
        :type StartTime: str
        :param EndTime: End of the time range for the query
        :type EndTime: str
        :param Data: Value array. The unit for attack traffic bandwidth is Mbps, and that for the packet rate is pps.
        :type Data: list of int non-negative
        :param Id: Instance ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Id: str
        :param MetricName: Metric. Valid values: `bps`: attack traffic bandwidth; `pps`: attack packet rate
        :type MetricName: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Count = None
        self.Business = None
        self.Ip = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None
        self.Data = None
        self.Id = None
        self.MetricName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.Business = params.get("Business")
        self.Ip = params.get("Ip")
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Data = params.get("Data")
        self.Id = params.get("Id")
        self.MetricName = params.get("MetricName")
        self.RequestId = params.get("RequestId")


class DescribeDefaultAlarmThresholdRequest(AbstractModel):
    """DescribeDefaultAlarmThreshold request structure.

    """

    def __init__(self):
        r"""
        :param InstanceType: Product category. Valid values:
`bgp`: Anti-DDoS Pro
`bgpip`: Anti-DDoS Advanced
]
        :type InstanceType: str
        :param FilterAlarmType: Alarm threshold type filter. Valid values:
`1`: alarm threshold for inbound traffic
`2`: alarm threshold for cleansing attack traffic
]
        :type FilterAlarmType: int
        """
        self.InstanceType = None
        self.FilterAlarmType = None


    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        self.FilterAlarmType = params.get("FilterAlarmType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDefaultAlarmThresholdResponse(AbstractModel):
    """DescribeDefaultAlarmThreshold response structure.

    """

    def __init__(self):
        r"""
        :param DefaultAlarmConfigList: Default alarm threshold configuration
        :type DefaultAlarmConfigList: list of DefaultAlarmThreshold
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DefaultAlarmConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DefaultAlarmConfigList") is not None:
            self.DefaultAlarmConfigList = []
            for item in params.get("DefaultAlarmConfigList"):
                obj = DefaultAlarmThreshold()
                obj._deserialize(item)
                self.DefaultAlarmConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeL7RulesBySSLCertIdRequest(AbstractModel):
    """DescribeL7RulesBySSLCertId request structure.

    """

    def __init__(self):
        r"""
        :param Status: Domain name status. Valid values: `bindable`, `binded`, `opened`, `closed`, `all` (all states).
        :type Status: str
        :param CertIds: List of certificate IDs
        :type CertIds: list of str
        """
        self.Status = None
        self.CertIds = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.CertIds = params.get("CertIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeL7RulesBySSLCertIdResponse(AbstractModel):
    """DescribeL7RulesBySSLCertId response structure.

    """

    def __init__(self):
        r"""
        :param CertSet: Certificate rule set
        :type CertSet: list of CertIdInsL7Rules
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.CertSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CertSet") is not None:
            self.CertSet = []
            for item in params.get("CertSet"):
                obj = CertIdInsL7Rules()
                obj._deserialize(item)
                self.CertSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListBGPIPInstancesRequest(AbstractModel):
    """DescribeListBGPIPInstances request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when `Limit = 0`. The maximum value is 100.
        :type Limit: int
        :param FilterIp: IP filter
        :type FilterIp: str
        :param FilterInstanceId: Anti-DDoS instance ID filter. For example, you can filter the Anti-DDoS Advanced instance ID by `bgpip-00000001`.
        :type FilterInstanceId: str
        :param FilterLine: Anti-DDoS Advanced line filter. Valid values:
`1`: BGP line
`2`: China Telecom
`3`: China Unicom
`4`: China Mobile
`99`: third-party line
]
        :type FilterLine: int
        :param FilterRegion: Region filter. For example, `ap-guangzhou`.
        :type FilterRegion: str
        :param FilterName: Name filter
        :type FilterName: str
        :param FilterEipType: Whether to obtain only Anti-DDoS EIP instances. `1`: Yes; `0`: No.
        :type FilterEipType: int
        :param FilterEipEipAddressStatus: Anti-DDoS Advanced instance binding status filter. Valid values: `BINDING`, `BIND`, `UNBINDING`, `UNBIND`. This filter is only valid when `FilterEipType = 1`.
        :type FilterEipEipAddressStatus: list of str
        :param FilterDamDDoSStatus: Whether to obtain only Anti-DDoS instances with Sec-MCA enabled. Valid values: `1` (only obtain Anti-DDoS instances with Sec-MCA enabled) and `0` (obtain other Anti-DDoS instances).
        :type FilterDamDDoSStatus: int
        :param FilterStatus: Filters by the status of bound resources. Values: `idle` (normal), `attacking` (being attacked), `blocking` (being blocked), `trial` (in trial)
        :type FilterStatus: str
        :param FilterCname: Filters by the instance CNAME
        :type FilterCname: str
        :param FilterInstanceIdList: Filters by the instance ID
        :type FilterInstanceIdList: list of str
        :param FilterTag: Searches by tag
        :type FilterTag: :class:`tencentcloud.antiddos.v20200309.models.TagFilter`
        :param FilterPackType: Filters by package type.
        :type FilterPackType: list of str
        :param FilterConvoy: Filters out Convoy instances
        :type FilterConvoy: int
        """
        self.Offset = None
        self.Limit = None
        self.FilterIp = None
        self.FilterInstanceId = None
        self.FilterLine = None
        self.FilterRegion = None
        self.FilterName = None
        self.FilterEipType = None
        self.FilterEipEipAddressStatus = None
        self.FilterDamDDoSStatus = None
        self.FilterStatus = None
        self.FilterCname = None
        self.FilterInstanceIdList = None
        self.FilterTag = None
        self.FilterPackType = None
        self.FilterConvoy = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterIp = params.get("FilterIp")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterLine = params.get("FilterLine")
        self.FilterRegion = params.get("FilterRegion")
        self.FilterName = params.get("FilterName")
        self.FilterEipType = params.get("FilterEipType")
        self.FilterEipEipAddressStatus = params.get("FilterEipEipAddressStatus")
        self.FilterDamDDoSStatus = params.get("FilterDamDDoSStatus")
        self.FilterStatus = params.get("FilterStatus")
        self.FilterCname = params.get("FilterCname")
        self.FilterInstanceIdList = params.get("FilterInstanceIdList")
        if params.get("FilterTag") is not None:
            self.FilterTag = TagFilter()
            self.FilterTag._deserialize(params.get("FilterTag"))
        self.FilterPackType = params.get("FilterPackType")
        self.FilterConvoy = params.get("FilterConvoy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListBGPIPInstancesResponse(AbstractModel):
    """DescribeListBGPIPInstances response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param InstanceList: List of Anti-DDoS Advanced instances
        :type InstanceList: list of BGPIPInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.InstanceList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("InstanceList") is not None:
            self.InstanceList = []
            for item in params.get("InstanceList"):
                obj = BGPIPInstance()
                obj._deserialize(item)
                self.InstanceList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListBGPInstancesRequest(AbstractModel):
    """DescribeListBGPInstances request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when `Limit = 0`. The maximum value is 100.
        :type Limit: int
        :param FilterIp: Filters by IP.
        :type FilterIp: str
        :param FilterInstanceId: Anti-DDoS instance ID filter. For example, `bgp-00000001`.
        :type FilterInstanceId: str
        :param FilterRegion: Filters by region. For example, `ap-guangzhou`.
        :type FilterRegion: str
        :param FilterName: Filters by name.
        :type FilterName: str
        :param FilterLine: Line filter. Valid values: 1: BGP; 2: Non-BGP.
        :type FilterLine: int
        :param FilterStatus: Filters by instance status. `idle`: Running; `attacking`: Being attacked; `blocking`: Being blocked.
        :type FilterStatus: str
        :param FilterBoundStatus: Filters by binding status. `bounding`: The instance is bound; `failed`: The binding failed.
        :type FilterBoundStatus: str
        :param FilterInstanceIdList: Array of instance IDs
        :type FilterInstanceIdList: list of str
        :param FilterEnterpriseFlag: Enterprise edition. Values: `1` (the Convoy package included), `2` (the Convoy package not included)
        :type FilterEnterpriseFlag: int
        :param FilterLightFlag: Whether it’s a Lighthouse edition
        :type FilterLightFlag: int
        :param FilterChannelFlag: Whether it’s a Channel edition
        :type FilterChannelFlag: int
        :param FilterTag: Filters by tag
        :type FilterTag: :class:`tencentcloud.antiddos.v20200309.models.TagFilter`
        :param FilterTrialFlag: Filters out trial instances. Values: `1` (emergency protection instances), `2` (PLG instances)
        :type FilterTrialFlag: int
        :param FilterConvoy: Filters out Convoy instances
        :type FilterConvoy: int
        :param ExcludeAdvancedInfo: Whether to exclude the advanced information (such as `InstanceList[0].Usage`). Values: `true` (exclude), `false` (do not exclude). The default value is `false`.
        :type ExcludeAdvancedInfo: bool
        """
        self.Offset = None
        self.Limit = None
        self.FilterIp = None
        self.FilterInstanceId = None
        self.FilterRegion = None
        self.FilterName = None
        self.FilterLine = None
        self.FilterStatus = None
        self.FilterBoundStatus = None
        self.FilterInstanceIdList = None
        self.FilterEnterpriseFlag = None
        self.FilterLightFlag = None
        self.FilterChannelFlag = None
        self.FilterTag = None
        self.FilterTrialFlag = None
        self.FilterConvoy = None
        self.ExcludeAdvancedInfo = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterIp = params.get("FilterIp")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterRegion = params.get("FilterRegion")
        self.FilterName = params.get("FilterName")
        self.FilterLine = params.get("FilterLine")
        self.FilterStatus = params.get("FilterStatus")
        self.FilterBoundStatus = params.get("FilterBoundStatus")
        self.FilterInstanceIdList = params.get("FilterInstanceIdList")
        self.FilterEnterpriseFlag = params.get("FilterEnterpriseFlag")
        self.FilterLightFlag = params.get("FilterLightFlag")
        self.FilterChannelFlag = params.get("FilterChannelFlag")
        if params.get("FilterTag") is not None:
            self.FilterTag = TagFilter()
            self.FilterTag._deserialize(params.get("FilterTag"))
        self.FilterTrialFlag = params.get("FilterTrialFlag")
        self.FilterConvoy = params.get("FilterConvoy")
        self.ExcludeAdvancedInfo = params.get("ExcludeAdvancedInfo")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListBGPInstancesResponse(AbstractModel):
    """DescribeListBGPInstances response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of Anti-DDoS Pro instances
        :type Total: int
        :param InstanceList: List of Anti-DDoS Pro instances
        :type InstanceList: list of BGPInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.InstanceList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("InstanceList") is not None:
            self.InstanceList = []
            for item in params.get("InstanceList"):
                obj = BGPInstance()
                obj._deserialize(item)
                self.InstanceList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListBlackWhiteIpListRequest(AbstractModel):
    """DescribeListBlackWhiteIpList request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when Limit = 0. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterIp: IP filter
        :type FilterIp: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterIp = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterIp = params.get("FilterIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListBlackWhiteIpListResponse(AbstractModel):
    """DescribeListBlackWhiteIpList response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param IpList: IP blocklist/allowlist
        :type IpList: list of BlackWhiteIpRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.IpList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("IpList") is not None:
            self.IpList = []
            for item in params.get("IpList"):
                obj = BlackWhiteIpRelation()
                obj._deserialize(item)
                self.IpList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListDDoSAIRequest(AbstractModel):
    """DescribeListDDoSAI request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when Limit = 0. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterIp: IP filter
        :type FilterIp: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterIp = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterIp = params.get("FilterIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListDDoSAIResponse(AbstractModel):
    """DescribeListDDoSAI response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param ConfigList: List of AI protection switches
        :type ConfigList: list of DDoSAIRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ConfigList") is not None:
            self.ConfigList = []
            for item in params.get("ConfigList"):
                obj = DDoSAIRelation()
                obj._deserialize(item)
                self.ConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListDDoSGeoIPBlockConfigRequest(AbstractModel):
    """DescribeListDDoSGeoIPBlockConfig request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when Limit = 0. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterIp: IP filter
        :type FilterIp: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterIp = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterIp = params.get("FilterIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListDDoSGeoIPBlockConfigResponse(AbstractModel):
    """DescribeListDDoSGeoIPBlockConfig response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param ConfigList: List of Anti-DDoS region blocking configurations
        :type ConfigList: list of DDoSGeoIPBlockConfigRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ConfigList") is not None:
            self.ConfigList = []
            for item in params.get("ConfigList"):
                obj = DDoSGeoIPBlockConfigRelation()
                obj._deserialize(item)
                self.ConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListDDoSSpeedLimitConfigRequest(AbstractModel):
    """DescribeListDDoSSpeedLimitConfig request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when Limit = 0. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterIp: IP filter
        :type FilterIp: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterIp = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterIp = params.get("FilterIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListDDoSSpeedLimitConfigResponse(AbstractModel):
    """DescribeListDDoSSpeedLimitConfig response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param ConfigList: List of access rate limit configurations
        :type ConfigList: list of DDoSSpeedLimitConfigRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ConfigList") is not None:
            self.ConfigList = []
            for item in params.get("ConfigList"):
                obj = DDoSSpeedLimitConfigRelation()
                obj._deserialize(item)
                self.ConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListIPAlarmConfigRequest(AbstractModel):
    """DescribeListIPAlarmConfig request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when Limit = 0. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterAlarmType: Alarm threshold type filter. Valid values:
`1`: alarm threshold for inbound traffic
`2`: alarm threshold for cleansing attack traffic
]
        :type FilterAlarmType: int
        :param FilterIp: IP filter
        :type FilterIp: str
        :param FilterCname: CNAME of the Anti-DDoS Advanced instance
        :type FilterCname: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterAlarmType = None
        self.FilterIp = None
        self.FilterCname = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterAlarmType = params.get("FilterAlarmType")
        self.FilterIp = params.get("FilterIp")
        self.FilterCname = params.get("FilterCname")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListIPAlarmConfigResponse(AbstractModel):
    """DescribeListIPAlarmConfig response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param ConfigList: List of IP alarm threshold configurations
        :type ConfigList: list of IPAlarmThresholdRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ConfigList") is not None:
            self.ConfigList = []
            for item in params.get("ConfigList"):
                obj = IPAlarmThresholdRelation()
                obj._deserialize(item)
                self.ConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListListenerRequest(AbstractModel):
    """DescribeListListener request structure.

    """


class DescribeListListenerResponse(AbstractModel):
    """DescribeListListener response structure.

    """

    def __init__(self):
        r"""
        :param Layer4Listeners: List of layer-4 forwarding listeners
        :type Layer4Listeners: list of Layer4Rule
        :param Layer7Listeners: List of layer-7 forwarding listeners
        :type Layer7Listeners: list of Layer7Rule
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Layer4Listeners = None
        self.Layer7Listeners = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Layer4Listeners") is not None:
            self.Layer4Listeners = []
            for item in params.get("Layer4Listeners"):
                obj = Layer4Rule()
                obj._deserialize(item)
                self.Layer4Listeners.append(obj)
        if params.get("Layer7Listeners") is not None:
            self.Layer7Listeners = []
            for item in params.get("Layer7Listeners"):
                obj = Layer7Rule()
                obj._deserialize(item)
                self.Layer7Listeners.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListPacketFilterConfigRequest(AbstractModel):
    """DescribeListPacketFilterConfig request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when Limit = 0. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterIp: IP filter
        :type FilterIp: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterIp = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterIp = params.get("FilterIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListPacketFilterConfigResponse(AbstractModel):
    """DescribeListPacketFilterConfig response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param ConfigList: Feature filtering configuration
        :type ConfigList: list of PacketFilterRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ConfigList") is not None:
            self.ConfigList = []
            for item in params.get("ConfigList"):
                obj = PacketFilterRelation()
                obj._deserialize(item)
                self.ConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListProtectThresholdConfigRequest(AbstractModel):
    """DescribeListProtectThresholdConfig request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when `Limit = 0`. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterIp: IP filter
        :type FilterIp: str
        :param FilterDomain: Domain name filter for querying CC protection thresholds of domain names and protocols
        :type FilterDomain: str
        :param FilterProtocol: Protocol filter for querying CC protection thresholds of domain names and protocols
        :type FilterProtocol: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterIp = None
        self.FilterDomain = None
        self.FilterProtocol = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterIp = params.get("FilterIp")
        self.FilterDomain = params.get("FilterDomain")
        self.FilterProtocol = params.get("FilterProtocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListProtectThresholdConfigResponse(AbstractModel):
    """DescribeListProtectThresholdConfig response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param ConfigList: List of protection threshold configurations
        :type ConfigList: list of ProtectThresholdRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ConfigList") is not None:
            self.ConfigList = []
            for item in params.get("ConfigList"):
                obj = ProtectThresholdRelation()
                obj._deserialize(item)
                self.ConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListProtocolBlockConfigRequest(AbstractModel):
    """DescribeListProtocolBlockConfig request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when `Limit = 0`. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterIp: IP filter
        :type FilterIp: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterIp = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterIp = params.get("FilterIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListProtocolBlockConfigResponse(AbstractModel):
    """DescribeListProtocolBlockConfig response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param ConfigList: Protocol blocking configuration
        :type ConfigList: list of ProtocolBlockRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ConfigList") is not None:
            self.ConfigList = []
            for item in params.get("ConfigList"):
                obj = ProtocolBlockRelation()
                obj._deserialize(item)
                self.ConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListSchedulingDomainRequest(AbstractModel):
    """DescribeListSchedulingDomain request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when `Limit = 0`. The maximum value is 100.
        :type Limit: int
        :param FilterDomain: Scheduling domain name filter
        :type FilterDomain: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterDomain = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterDomain = params.get("FilterDomain")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListSchedulingDomainResponse(AbstractModel):
    """DescribeListSchedulingDomain response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param DomainList: List of scheduling domain names
        :type DomainList: list of SchedulingDomainInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.DomainList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("DomainList") is not None:
            self.DomainList = []
            for item in params.get("DomainList"):
                obj = SchedulingDomainInfo()
                obj._deserialize(item)
                self.DomainList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeListWaterPrintConfigRequest(AbstractModel):
    """DescribeListWaterPrintConfig request structure.

    """

    def __init__(self):
        r"""
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param Limit: Number of items per page. The default value is 20 when `Limit = 0`. The maximum value is 100.
        :type Limit: int
        :param FilterInstanceId: Anti-DDoS instance ID filter. Anti-DDoS instance prefix wildcard search is supported. For example, you can filter Anti-DDoS Pro instances by `bgp-*`.
        :type FilterInstanceId: str
        :param FilterIp: IP filter
        :type FilterIp: str
        """
        self.Offset = None
        self.Limit = None
        self.FilterInstanceId = None
        self.FilterIp = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.FilterInstanceId = params.get("FilterInstanceId")
        self.FilterIp = params.get("FilterIp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeListWaterPrintConfigResponse(AbstractModel):
    """DescribeListWaterPrintConfig response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of lists
        :type Total: int
        :param ConfigList: List of watermark configurations
        :type ConfigList: list of WaterPrintRelation
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.ConfigList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ConfigList") is not None:
            self.ConfigList = []
            for item in params.get("ConfigList"):
                obj = WaterPrintRelation()
                obj._deserialize(item)
                self.ConfigList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeNewL7RulesErrHealthRequest(AbstractModel):
    """DescribeNewL7RulesErrHealth request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type (`bgpip`: Anti-DDoS Advanced)
        :type Business: str
        :param RuleIdList: List of rule IDs
        :type RuleIdList: list of str
        """
        self.Business = None
        self.RuleIdList = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.RuleIdList = params.get("RuleIdList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNewL7RulesErrHealthResponse(AbstractModel):
    """DescribeNewL7RulesErrHealth response structure.

    """

    def __init__(self):
        r"""
        :param ErrHealths: List of rules with exceptions. `Key`: Rule ID, `Value`: Exception IPs and error message. 
        :type ErrHealths: list of KeyValue
        :param Total: Total number of rules with exceptions
        :type Total: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ErrHealths = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ErrHealths") is not None:
            self.ErrHealths = []
            for item in params.get("ErrHealths"):
                obj = KeyValue()
                obj._deserialize(item)
                self.ErrHealths.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeNewL7RulesRequest(AbstractModel):
    """DescribeNewL7Rules request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type (`bgpip`: Anti-DDoS Advanced)
        :type Business: str
        :param StatusList: (Optional) Searches by rule status. Valid values: `0` (Successfully configured), `1` (Being configured), `2` (Configuration failed), `3` (Being deleted), `5` (Deletion failed), `6` (awaiting configuration), `7` (awaiting deletion), and `8` (awaiting certificate configuration).
        :type StatusList: list of int non-negative
        :param Domain: (Optional) Searches by domain name.
        :type Domain: str
        :param Ip: (Optional) Searches by IP.
        :type Ip: str
        :param Limit: Number of items in a page. Returned results are not paged if you enter “0”.
        :type Limit: int
        :param Offset: Starting offset of the page. Value: (number of pages – 1) * items per page.
        :type Offset: int
        :param ProtocolList: (Optional) Searches by forwarding protocol. Values: [http, https, http/https]
        :type ProtocolList: list of str
        :param Cname: CNAME of the Anti-DDoS Advanced instance
        :type Cname: str
        """
        self.Business = None
        self.StatusList = None
        self.Domain = None
        self.Ip = None
        self.Limit = None
        self.Offset = None
        self.ProtocolList = None
        self.Cname = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.StatusList = params.get("StatusList")
        self.Domain = params.get("Domain")
        self.Ip = params.get("Ip")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.ProtocolList = params.get("ProtocolList")
        self.Cname = params.get("Cname")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNewL7RulesResponse(AbstractModel):
    """DescribeNewL7Rules response structure.

    """

    def __init__(self):
        r"""
        :param Rules: List of forwarding rules
        :type Rules: list of NewL7RuleEntry
        :param Healths: List of health check settings
        :type Healths: list of L7RuleHealth
        :param Total: Total number of rules
        :type Total: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Rules = None
        self.Healths = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Rules") is not None:
            self.Rules = []
            for item in params.get("Rules"):
                obj = NewL7RuleEntry()
                obj._deserialize(item)
                self.Rules.append(obj)
        if params.get("Healths") is not None:
            self.Healths = []
            for item in params.get("Healths"):
                obj = L7RuleHealth()
                obj._deserialize(item)
                self.Healths.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeOverviewDDoSEventListRequest(AbstractModel):
    """DescribeOverviewDDoSEventList request structure.

    """

    def __init__(self):
        r"""
        :param StartTime: Start time
        :type StartTime: str
        :param EndTime: End time
        :type EndTime: str
        :param AttackStatus: Filters by the attack status. `start`: The attack is ongoing; `end`: The attack ends.
        :type AttackStatus: str
        :param Offset: The offset value
        :type Offset: int
        :param Limit: Total number of records
        :type Limit: int
        """
        self.StartTime = None
        self.EndTime = None
        self.AttackStatus = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.AttackStatus = params.get("AttackStatus")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeOverviewDDoSEventListResponse(AbstractModel):
    """DescribeOverviewDDoSEventList response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of records
        :type Total: int
        :param EventList: Event list
        :type EventList: list of OverviewDDoSEvent
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.EventList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("EventList") is not None:
            self.EventList = []
            for item in params.get("EventList"):
                obj = OverviewDDoSEvent()
                obj._deserialize(item)
                self.EventList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribePendingRiskInfoRequest(AbstractModel):
    """DescribePendingRiskInfo request structure.

    """


class DescribePendingRiskInfoResponse(AbstractModel):
    """DescribePendingRiskInfo response structure.

    """

    def __init__(self):
        r"""
        :param IsPaidUsr: Whether the user is a paid user. Values: `true`, `false`.
        :type IsPaidUsr: bool
        :param AttackingCount: Number of resources being attacked
        :type AttackingCount: int
        :param BlockingCount: Number of resource blocked
        :type BlockingCount: int
        :param ExpiredCount: Number of expired resources
        :type ExpiredCount: int
        :param Total: Total pending risk events
        :type Total: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.IsPaidUsr = None
        self.AttackingCount = None
        self.BlockingCount = None
        self.ExpiredCount = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsPaidUsr = params.get("IsPaidUsr")
        self.AttackingCount = params.get("AttackingCount")
        self.BlockingCount = params.get("BlockingCount")
        self.ExpiredCount = params.get("ExpiredCount")
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DisassociateDDoSEipAddressRequest(AbstractModel):
    """DisassociateDDoSEipAddress request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID (only Anti-DDoS Advanced). For example, `bgpip-0000011x`.
        :type InstanceId: str
        :param Eip: EIP of the Anti-DDoS instance ID
        :type Eip: str
        """
        self.InstanceId = None
        self.Eip = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Eip = params.get("Eip")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisassociateDDoSEipAddressResponse(AbstractModel):
    """DisassociateDDoSEipAddress response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EipAddressPackRelation(AbstractModel):
    """Details of the Anycast package

    """

    def __init__(self):
        r"""
        :param IpCount: Number of package IPs
        :type IpCount: int
        :param AutoRenewFlag: Auto-renewal flag
        :type AutoRenewFlag: int
        :param CurDeadline: Current expiration time
        :type CurDeadline: str
        """
        self.IpCount = None
        self.AutoRenewFlag = None
        self.CurDeadline = None


    def _deserialize(self, params):
        self.IpCount = params.get("IpCount")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.CurDeadline = params.get("CurDeadline")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EipAddressRelation(AbstractModel):
    """EIP association details

    """

    def __init__(self):
        r"""
        :param EipAddressRegion: Region of the Anti-DDoS instance bound to the EIP. For example, hk indicates Hong Kong.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type EipAddressRegion: str
        :param EipBoundRscIns: ID of the bound resource. For example, an ID may be bound to an CVM instance.
Note: This is field may return `null`, indicating that no valid value can be obtained.
        :type EipBoundRscIns: str
        :param EipBoundRscEni: ID of the bound ENI
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type EipBoundRscEni: str
        :param EipBoundRscVip: Private IP of the bound resource
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type EipBoundRscVip: str
        :param ModifyTime: Modification time
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ModifyTime: str
        """
        self.EipAddressRegion = None
        self.EipBoundRscIns = None
        self.EipBoundRscEni = None
        self.EipBoundRscVip = None
        self.ModifyTime = None


    def _deserialize(self, params):
        self.EipAddressRegion = params.get("EipAddressRegion")
        self.EipBoundRscIns = params.get("EipBoundRscIns")
        self.EipBoundRscEni = params.get("EipBoundRscEni")
        self.EipBoundRscVip = params.get("EipBoundRscVip")
        self.ModifyTime = params.get("ModifyTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EipProductInfo(AbstractModel):
    """Details of the cloud product used by the EIP

    """

    def __init__(self):
        r"""
        :param Ip: IP address
        :type Ip: str
        :param BizType: Cloud product category. Valid values:
`public`: CVM
`bm`: BM
`eni`: ENI
`vpngw`: VPN gateway
 `natgw`: NAT gateway
`waf`: WAF
`fpc`: financial products
`gaap`: GAAP 
`other`: hosted IP
]
        :type BizType: str
        :param DeviceType: Cloud sub-product category. Valid values: `cvm` (CVM), `lb` (Load balancer), `eni` (ENI), `vpngw` (VPN gateway), `natgw` (NAT gateway), `waf` (WAF), `fpc` (financial products), `gaap` (GAAP), `eip` (BM EIP) and `other` (hosted IP).
        :type DeviceType: str
        :param InstanceId: Cloud instance ID of the IP. This field InstanceId will be `eni-*` if the instance ID is bound to an ENI IP; `none` if there is no instance ID to bind to a hosted IP.
        :type InstanceId: str
        """
        self.Ip = None
        self.BizType = None
        self.DeviceType = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.Ip = params.get("Ip")
        self.BizType = params.get("BizType")
        self.DeviceType = params.get("DeviceType")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ForwardListener(AbstractModel):
    """Forwarding listener

    """

    def __init__(self):
        r"""
        :param FrontendPort: The starting port for listener forwarding. Value range: 1 to 65535.
        :type FrontendPort: int
        :param ForwardProtocol: Forwarding protocol. Valid values:
`TCP`
`UDP`
]
        :type ForwardProtocol: str
        :param FrontendPortEnd: The ending port for listener forwarding. Value range: 1 to 65535.
        :type FrontendPortEnd: int
        """
        self.FrontendPort = None
        self.ForwardProtocol = None
        self.FrontendPortEnd = None


    def _deserialize(self, params):
        self.FrontendPort = params.get("FrontendPort")
        self.ForwardProtocol = params.get("ForwardProtocol")
        self.FrontendPortEnd = params.get("FrontendPortEnd")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HttpStatusMap(AbstractModel):
    """Aggregated data on the HTTP status codes of business traffic

    """

    def __init__(self):
        r"""
        :param SourceHttp2xx: HTTP 2xx Forwarding status code
        :type SourceHttp2xx: list of float
        :param Http5xx: HTTP 5xx Status code
        :type Http5xx: list of float
        :param SourceHttp5xx: HTTP 5xx Forwarding status code
        :type SourceHttp5xx: list of float
        :param SourceHttp404: HTTP 404 Forwarding status code
        :type SourceHttp404: list of float
        :param Http4xx: HTTP 4xx Status code
        :type Http4xx: list of float
        :param SourceHttp4xx: HTTP 4xx Forwarding status code
        :type SourceHttp4xx: list of float
        :param Http2xx: HTTP 2xx Status code
        :type Http2xx: list of float
        :param Http404: HTTP 404 Status code
        :type Http404: list of float
        :param SourceHttp3xx: HTTP 3xx Forwarding status code
        :type SourceHttp3xx: list of float
        :param Http3xx: HTTP 3xx Status code
        :type Http3xx: list of float
        """
        self.SourceHttp2xx = None
        self.Http5xx = None
        self.SourceHttp5xx = None
        self.SourceHttp404 = None
        self.Http4xx = None
        self.SourceHttp4xx = None
        self.Http2xx = None
        self.Http404 = None
        self.SourceHttp3xx = None
        self.Http3xx = None


    def _deserialize(self, params):
        self.SourceHttp2xx = params.get("SourceHttp2xx")
        self.Http5xx = params.get("Http5xx")
        self.SourceHttp5xx = params.get("SourceHttp5xx")
        self.SourceHttp404 = params.get("SourceHttp404")
        self.Http4xx = params.get("Http4xx")
        self.SourceHttp4xx = params.get("SourceHttp4xx")
        self.Http2xx = params.get("Http2xx")
        self.Http404 = params.get("Http404")
        self.SourceHttp3xx = params.get("SourceHttp3xx")
        self.Http3xx = params.get("Http3xx")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IPAlarmThresholdRelation(AbstractModel):
    """Single IP alarm threshold configuration

    """

    def __init__(self):
        r"""
        :param AlarmType: Alarm threshold type. Valid values:
`1`: alarm threshold for inbound traffic
`2`: alarm threshold for cleansing attack traffic
]
        :type AlarmType: int
        :param AlarmThreshold: Alarm threshold (Mbps). The value should be greater than or equal to 0. Note that the alarm threshold configuration will be removed if you pass the parameter for input and set it to 0.
        :type AlarmThreshold: int
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        """
        self.AlarmType = None
        self.AlarmThreshold = None
        self.InstanceDetailList = None


    def _deserialize(self, params):
        self.AlarmType = params.get("AlarmType")
        self.AlarmThreshold = params.get("AlarmThreshold")
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IPLineInfo(AbstractModel):
    """IP line information

    """

    def __init__(self):
        r"""
        :param Type: IP line type. Valid values:
`bgp`: BGP IP
`ctcc`: CTCC IP
`cucc`: CUCC IP
`cmcc`: CMCC IP
`abroad`: IP outside the Chinese mainland
]
        :type Type: str
        :param Eip: 
        :type Eip: str
        :param Cname: CNAME of the instance
        :type Cname: str
        :param ResourceFlag: Flag of the instance. `0`: Anti-DDoS Pro instance; `1`: Anti-DDoS Advanced instance; `2`: Non-Anti-DDoS Advanced instance.
        :type ResourceFlag: int
        """
        self.Type = None
        self.Eip = None
        self.Cname = None
        self.ResourceFlag = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Eip = params.get("Eip")
        self.Cname = params.get("Cname")
        self.ResourceFlag = params.get("ResourceFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InsL7Rules(AbstractModel):
    """Layer-7 instance rules

    """

    def __init__(self):
        r"""
        :param Status: Rules can only be modified when the status is `0`, `2`, or `8`.
Rule status. Values: `0` (Normal), `1` (Being configured), `2` (Configuration failed), `3` (Being deleted), `5` (Failed to be deleted), `6` (Pending add), `7` (Pending delete), `8` (Pending certificate upload), `9` (Associated resource not exist), `10` (Pending modify), `11` (Being modified).
        :type Status: int
        :param Domain: Domain name
        :type Domain: str
        :param Protocol: Protocol
        :type Protocol: str
        :param InsId: Instance ID
        :type InsId: str
        :param AppId: User App ID
        :type AppId: str
        :param VirtualPort: High-defense port
        :type VirtualPort: str
        :param SSLId: Certificate ID
        :type SSLId: str
        """
        self.Status = None
        self.Domain = None
        self.Protocol = None
        self.InsId = None
        self.AppId = None
        self.VirtualPort = None
        self.SSLId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        self.InsId = params.get("InsId")
        self.AppId = params.get("AppId")
        self.VirtualPort = params.get("VirtualPort")
        self.SSLId = params.get("SSLId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceRelation(AbstractModel):
    """Instance IP information

    """

    def __init__(self):
        r"""
        :param EipList: Instance IP
        :type EipList: list of str
        :param InstanceId: Instance ID
        :type InstanceId: str
        """
        self.EipList = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.EipList = params.get("EipList")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IpSegment(AbstractModel):
    """Structure of IP range

    """

    def __init__(self):
        r"""
        :param Ip: IP address
        :type Ip: str
        :param Mask: IP mask. For a 32-bit IP address, enter `0`.
        :type Mask: int
        """
        self.Ip = None
        self.Mask = None


    def _deserialize(self, params):
        self.Ip = params.get("Ip")
        self.Mask = params.get("Mask")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KeyValue(AbstractModel):
    """Status of the IP

    """

    def __init__(self):
        r"""
        :param Key: IP
        :type Key: str
        :param Value: Status of the IP. Values: `1` (blocked); `2` (normal); `3` (being attacked)
        :type Value: str
        """
        self.Key = None
        self.Value = None


    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class L4RuleSource(AbstractModel):
    """List of layer-4 forwarding rules

    """

    def __init__(self):
        r"""
        :param Source: IP or domain name for forwarding.
        :type Source: str
        :param Weight: Weight. Value range: [0,100].
        :type Weight: int
        :param Port: 8000
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Port: int
        :param Backup: Secondary origin server. `1`: secondary origin server; `0`: general origin server.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type Backup: int
        """
        self.Source = None
        self.Weight = None
        self.Port = None
        self.Backup = None


    def _deserialize(self, params):
        self.Source = params.get("Source")
        self.Weight = params.get("Weight")
        self.Port = params.get("Port")
        self.Backup = params.get("Backup")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class L7RuleEntry(AbstractModel):
    """Layer-7 forwarding rule.

    """

    def __init__(self):
        r"""
        :param KeepTime: Session persistence duration, in seconds.
        :type KeepTime: int
        :param Domain: Forwarding domain name.
        :type Domain: str
        :param Protocol: Forwarding protocol. Valid values: `http` and `https`.
        :type Protocol: str
        :param SourceType: Forwarding method. Valid values: `1` (by domain name); `2` (by IP).
        :type SourceType: int
        :param LbType: Load balancing method. Valid value: `1` (weighed polling).
        :type LbType: int
        :param SourceList: List of origins
        :type SourceList: list of L4RuleSource
        :param KeepEnable: Whether session persistence is enabled. Valid values: `0` (disabled) and `1` (enabled).
        :type KeepEnable: int
        :param Status: Rule status. Valid values: `0` (the rule was successfully configured), `1` (configuring the rule), `2` (rule configuration failed), `3` (deleting the rule), `5` (failed to delete rule), `6` (rule awaiting configuration), `7` (rule awaiting deletion), and `8` (rule awaiting certificate configuration).
        :type Status: int
        :param RuleId: Rule ID. This field is not required for adding a rule, but is required for modifying or deleting a rule.
        :type RuleId: str
        :param CCThreshold: CC protection threshold based on HTTPS.
        :type CCThreshold: int
        :param PrivateKey: [Disused] When the certificate is an external certificate, the certificate key should be provided here. 
        :type PrivateKey: str
        :param CCEnable: CC protection status based on HTTPS. Valid values: `0` (disabled) and `1` (enabled).
        :type CCEnable: int
        :param HttpsToHttpEnable: Whether to enable **Forward HTTPS requests via HTTP**. Valid values: `0` (disable) and `1` (enable). It defaults to `0`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type HttpsToHttpEnable: int
        :param CertType: Certificate source. When the forwarding protocol is HTTPS, this field must be set to `2` (Tencent Cloud managed certificate), and for HTTP protocol, it can be set to `0`.
        :type CertType: int
        :param Cert: [Disused] When the certificate is an external certificate, the certificate content should be provided here. 
        :type Cert: str
        :param CCLevel: CC protection level based on HTTPS.
        :type CCLevel: str
        :param RuleName: Rule description.
        :type RuleName: str
        :param CCStatus: CC protection status. Valid values: `0` (disabled) and `1` (enabled).
        :type CCStatus: int
        :param VirtualPort: Access port number.
Note: This field may return null, indicating that no valid values can be obtained.
        :type VirtualPort: int
        :param SSLId: When the certificate is managed by Tencent Cloud, this field must be set to the ID of the managed certificate.
        :type SSLId: str
        :param Id: ID of the rule
        :type Id: str
        :param CCAIEnable: Intelligent CC protection status. Valid values: `0` (disabled) and `1` (enabled).
        :type CCAIEnable: int
        """
        self.KeepTime = None
        self.Domain = None
        self.Protocol = None
        self.SourceType = None
        self.LbType = None
        self.SourceList = None
        self.KeepEnable = None
        self.Status = None
        self.RuleId = None
        self.CCThreshold = None
        self.PrivateKey = None
        self.CCEnable = None
        self.HttpsToHttpEnable = None
        self.CertType = None
        self.Cert = None
        self.CCLevel = None
        self.RuleName = None
        self.CCStatus = None
        self.VirtualPort = None
        self.SSLId = None
        self.Id = None
        self.CCAIEnable = None


    def _deserialize(self, params):
        self.KeepTime = params.get("KeepTime")
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        self.SourceType = params.get("SourceType")
        self.LbType = params.get("LbType")
        if params.get("SourceList") is not None:
            self.SourceList = []
            for item in params.get("SourceList"):
                obj = L4RuleSource()
                obj._deserialize(item)
                self.SourceList.append(obj)
        self.KeepEnable = params.get("KeepEnable")
        self.Status = params.get("Status")
        self.RuleId = params.get("RuleId")
        self.CCThreshold = params.get("CCThreshold")
        self.PrivateKey = params.get("PrivateKey")
        self.CCEnable = params.get("CCEnable")
        self.HttpsToHttpEnable = params.get("HttpsToHttpEnable")
        self.CertType = params.get("CertType")
        self.Cert = params.get("Cert")
        self.CCLevel = params.get("CCLevel")
        self.RuleName = params.get("RuleName")
        self.CCStatus = params.get("CCStatus")
        self.VirtualPort = params.get("VirtualPort")
        self.SSLId = params.get("SSLId")
        self.Id = params.get("Id")
        self.CCAIEnable = params.get("CCAIEnable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class L7RuleHealth(AbstractModel):
    """Health check parameters of layer-7 forwarding rules

    """

    def __init__(self):
        r"""
        :param Status: Configuration status. Values: `0` (normal), `1` (configuration in progress) and `2` (configuration failed).
        :type Status: int
        :param Enable: Switch. Values: `1`: Enable; `0`: Disable.
        :type Enable: int
        :param RuleId: ID of the rule
        :type RuleId: str
        :param Url: HTTP request path. The default value is /.
        :type Url: str
        :param Interval: Health check interval. Unit: second.
        :type Interval: int
        :param AliveNum: Healthy threshold, which specifies the number of consecutive successful health checks.
        :type AliveNum: int
        :param KickNum: Unhealthy threshold, which specifies the number of consecutive failed health checks.
        :type KickNum: int
        :param Method: HTTP request method. Values: `HEAD` and `GET`.
        :type Method: str
        :param StatusCode: Status code that signifies a normal state. Values: `1` (1xx), `2` (2xx), `4` (3xx), `8` (4xx), and `16` (5xx).
        :type StatusCode: int
        :param ProtocolFlag: Whether to deploy both HTTP and HTTPS health check rules
        :type ProtocolFlag: int
        :param PassiveEnable: Enables passive detection. Values: `1` (enable) and `0` (disable).
        :type PassiveEnable: int
        :param BlockInter: Blocking period in the passive detection configuration
        :type BlockInter: int
        :param FailedCountInter: Time interval between passive detections
        :type FailedCountInter: int
        :param FailedThreshold: Unhealthy threshold in the passive detection configuration
        :type FailedThreshold: int
        :param PassiveStatusCode: Status code that signals that the passive detection considers the status normal. Values: `1` (1xx), `2` (2xx), `4` (3xx), `8` (4xx), and `16` (5xx).
        :type PassiveStatusCode: int
        :param PassiveStatus: Configuration status of the passive health check. Values: `0` (Normal), `1` (configuration in progress) and `2` (configuration failed).
        :type PassiveStatus: int
        """
        self.Status = None
        self.Enable = None
        self.RuleId = None
        self.Url = None
        self.Interval = None
        self.AliveNum = None
        self.KickNum = None
        self.Method = None
        self.StatusCode = None
        self.ProtocolFlag = None
        self.PassiveEnable = None
        self.BlockInter = None
        self.FailedCountInter = None
        self.FailedThreshold = None
        self.PassiveStatusCode = None
        self.PassiveStatus = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Enable = params.get("Enable")
        self.RuleId = params.get("RuleId")
        self.Url = params.get("Url")
        self.Interval = params.get("Interval")
        self.AliveNum = params.get("AliveNum")
        self.KickNum = params.get("KickNum")
        self.Method = params.get("Method")
        self.StatusCode = params.get("StatusCode")
        self.ProtocolFlag = params.get("ProtocolFlag")
        self.PassiveEnable = params.get("PassiveEnable")
        self.BlockInter = params.get("BlockInter")
        self.FailedCountInter = params.get("FailedCountInter")
        self.FailedThreshold = params.get("FailedThreshold")
        self.PassiveStatusCode = params.get("PassiveStatusCode")
        self.PassiveStatus = params.get("PassiveStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Layer4Rule(AbstractModel):
    """Layer-4 forwarding rule

    """

    def __init__(self):
        r"""
        :param BackendPort: Real server port. Value range: 1–65535.
        :type BackendPort: int
        :param FrontendPort: Forwarding port. Value range: 1–65535.
        :type FrontendPort: int
        :param Protocol: Forwarding rule. Valid values:
TCP
UDP
]
        :type Protocol: str
        :param RealServers: List of real servers
        :type RealServers: list of SourceServer
        :param InstanceDetails: Information of the Anti-DDoS instance
        :type InstanceDetails: list of InstanceRelation
        :param InstanceDetailRule: Information of the Anti-DDoS instance configured
        :type InstanceDetailRule: list of RuleInstanceRelation
        """
        self.BackendPort = None
        self.FrontendPort = None
        self.Protocol = None
        self.RealServers = None
        self.InstanceDetails = None
        self.InstanceDetailRule = None


    def _deserialize(self, params):
        self.BackendPort = params.get("BackendPort")
        self.FrontendPort = params.get("FrontendPort")
        self.Protocol = params.get("Protocol")
        if params.get("RealServers") is not None:
            self.RealServers = []
            for item in params.get("RealServers"):
                obj = SourceServer()
                obj._deserialize(item)
                self.RealServers.append(obj)
        if params.get("InstanceDetails") is not None:
            self.InstanceDetails = []
            for item in params.get("InstanceDetails"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetails.append(obj)
        if params.get("InstanceDetailRule") is not None:
            self.InstanceDetailRule = []
            for item in params.get("InstanceDetailRule"):
                obj = RuleInstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailRule.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Layer7Rule(AbstractModel):
    """Layer-7 forwarding rule

    """

    def __init__(self):
        r"""
        :param Domain: Domain name
        :type Domain: str
        :param ProxyTypeList: List of forwarding types
        :type ProxyTypeList: list of ProxyTypeInfo
        :param RealServers: List of real servers
        :type RealServers: list of SourceServer
        :param InstanceDetails: Information of the Anti-DDoS instance
        :type InstanceDetails: list of InstanceRelation
        :param InstanceDetailRule: Information of the Anti-DDoS instance configured
        :type InstanceDetailRule: list of RuleInstanceRelation
        :param Protocol: Protocol
        :type Protocol: str
        :param Vport: Port number
        :type Vport: int
        """
        self.Domain = None
        self.ProxyTypeList = None
        self.RealServers = None
        self.InstanceDetails = None
        self.InstanceDetailRule = None
        self.Protocol = None
        self.Vport = None


    def _deserialize(self, params):
        self.Domain = params.get("Domain")
        if params.get("ProxyTypeList") is not None:
            self.ProxyTypeList = []
            for item in params.get("ProxyTypeList"):
                obj = ProxyTypeInfo()
                obj._deserialize(item)
                self.ProxyTypeList.append(obj)
        if params.get("RealServers") is not None:
            self.RealServers = []
            for item in params.get("RealServers"):
                obj = SourceServer()
                obj._deserialize(item)
                self.RealServers.append(obj)
        if params.get("InstanceDetails") is not None:
            self.InstanceDetails = []
            for item in params.get("InstanceDetails"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetails.append(obj)
        if params.get("InstanceDetailRule") is not None:
            self.InstanceDetailRule = []
            for item in params.get("InstanceDetailRule"):
                obj = RuleInstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailRule.append(obj)
        self.Protocol = params.get("Protocol")
        self.Vport = params.get("Vport")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListenerCcThreholdConfig(AbstractModel):
    """CC protection thresholds of the domain name and protocol

    """

    def __init__(self):
        r"""
        :param Domain: Domain name
        :type Domain: str
        :param Protocol: Protocol. Value: `https`.
        :type Protocol: str
        :param CCEnable: Status. Valid values: `0` (disabled), `1` (enabled).
        :type CCEnable: int
        :param CCThreshold: CC protection threshold
        :type CCThreshold: int
        """
        self.Domain = None
        self.Protocol = None
        self.CCEnable = None
        self.CCThreshold = None


    def _deserialize(self, params):
        self.Domain = params.get("Domain")
        self.Protocol = params.get("Protocol")
        self.CCEnable = params.get("CCEnable")
        self.CCThreshold = params.get("CCThreshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCCPrecisionPolicyRequest(AbstractModel):
    """ModifyCCPrecisionPolicy request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param PolicyId: Policy ID
        :type PolicyId: str
        :param PolicyAction: Specifies the action. `alg`: Verify the access request via CAPTCHA; `drop`: Drop the access request.
        :type PolicyAction: str
        :param PolicyList: Policy records
        :type PolicyList: list of CCPrecisionPlyRecord
        """
        self.InstanceId = None
        self.PolicyId = None
        self.PolicyAction = None
        self.PolicyList = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.PolicyId = params.get("PolicyId")
        self.PolicyAction = params.get("PolicyAction")
        if params.get("PolicyList") is not None:
            self.PolicyList = []
            for item in params.get("PolicyList"):
                obj = CCPrecisionPlyRecord()
                obj._deserialize(item)
                self.PolicyList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCCPrecisionPolicyResponse(AbstractModel):
    """ModifyCCPrecisionPolicy response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyCcBlackWhiteIpListRequest(AbstractModel):
    """ModifyCcBlackWhiteIpList request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param IpList: List of IPs
        :type IpList: list of IpSegment
        :param Type: IP type. Valid values: `black` (blocklisted IP), `white`(allowlisted IP).
        :type Type: str
        :param PolicyId: Policy ID
        :type PolicyId: str
        """
        self.InstanceId = None
        self.IpList = None
        self.Type = None
        self.PolicyId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("IpList") is not None:
            self.IpList = []
            for item in params.get("IpList"):
                obj = IpSegment()
                obj._deserialize(item)
                self.IpList.append(obj)
        self.Type = params.get("Type")
        self.PolicyId = params.get("PolicyId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCcBlackWhiteIpListResponse(AbstractModel):
    """ModifyCcBlackWhiteIpList response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDDoSGeoIPBlockConfigRequest(AbstractModel):
    """ModifyDDoSGeoIPBlockConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param DDoSGeoIPBlockConfig: Region blocking configuration. The configuration ID cannot be empty when you set this parameter.
        :type DDoSGeoIPBlockConfig: :class:`tencentcloud.antiddos.v20200309.models.DDoSGeoIPBlockConfig`
        """
        self.InstanceId = None
        self.DDoSGeoIPBlockConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DDoSGeoIPBlockConfig") is not None:
            self.DDoSGeoIPBlockConfig = DDoSGeoIPBlockConfig()
            self.DDoSGeoIPBlockConfig._deserialize(params.get("DDoSGeoIPBlockConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDDoSGeoIPBlockConfigResponse(AbstractModel):
    """ModifyDDoSGeoIPBlockConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDDoSSpeedLimitConfigRequest(AbstractModel):
    """ModifyDDoSSpeedLimitConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param DDoSSpeedLimitConfig: Access rate limit configuration. The configuration ID cannot be empty when you set this parameter.
        :type DDoSSpeedLimitConfig: :class:`tencentcloud.antiddos.v20200309.models.DDoSSpeedLimitConfig`
        """
        self.InstanceId = None
        self.DDoSSpeedLimitConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DDoSSpeedLimitConfig") is not None:
            self.DDoSSpeedLimitConfig = DDoSSpeedLimitConfig()
            self.DDoSSpeedLimitConfig._deserialize(params.get("DDoSSpeedLimitConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDDoSSpeedLimitConfigResponse(AbstractModel):
    """ModifyDDoSSpeedLimitConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDomainUsrNameRequest(AbstractModel):
    """ModifyDomainUsrName request structure.

    """

    def __init__(self):
        r"""
        :param DomainName: User CNAME
        :type DomainName: str
        :param DomainUserName: Domain name
        :type DomainUserName: str
        """
        self.DomainName = None
        self.DomainUserName = None


    def _deserialize(self, params):
        self.DomainName = params.get("DomainName")
        self.DomainUserName = params.get("DomainUserName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDomainUsrNameResponse(AbstractModel):
    """ModifyDomainUsrName response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNewDomainRulesRequest(AbstractModel):
    """ModifyNewDomainRules request structure.

    """

    def __init__(self):
        r"""
        :param Business: Anti-DDoS service type (`bgpip`: Anti-DDoS Advanced).
        :type Business: str
        :param Id: Anti-DDoS instance ID.
        :type Id: str
        :param Rule: Domain name forwarding rule.
        :type Rule: :class:`tencentcloud.antiddos.v20200309.models.NewL7RuleEntry`
        """
        self.Business = None
        self.Id = None
        self.Rule = None


    def _deserialize(self, params):
        self.Business = params.get("Business")
        self.Id = params.get("Id")
        if params.get("Rule") is not None:
            self.Rule = NewL7RuleEntry()
            self.Rule._deserialize(params.get("Rule"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNewDomainRulesResponse(AbstractModel):
    """ModifyNewDomainRules response structure.

    """

    def __init__(self):
        r"""
        :param Success: Success code.
        :type Success: :class:`tencentcloud.antiddos.v20200309.models.SuccessCode`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Success = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Success") is not None:
            self.Success = SuccessCode()
            self.Success._deserialize(params.get("Success"))
        self.RequestId = params.get("RequestId")


class ModifyPacketFilterConfigRequest(AbstractModel):
    """ModifyPacketFilterConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param PacketFilterConfig: Feature filtering configuration
        :type PacketFilterConfig: :class:`tencentcloud.antiddos.v20200309.models.PacketFilterConfig`
        """
        self.InstanceId = None
        self.PacketFilterConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("PacketFilterConfig") is not None:
            self.PacketFilterConfig = PacketFilterConfig()
            self.PacketFilterConfig._deserialize(params.get("PacketFilterConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPacketFilterConfigResponse(AbstractModel):
    """ModifyPacketFilterConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class NewL7RuleEntry(AbstractModel):
    """Layer-7 rule.

    """

    def __init__(self):
        r"""
        :param Protocol: Forwarding protocol. Valid values: `http` and `https`.
        :type Protocol: str
        :param Domain: Forwarding domain name.
        :type Domain: str
        :param LbType: Load balancing method. Valid value: `1` (weighed polling).
        :type LbType: int
        :param KeepEnable: Whether session persistence is enabled. Valid values: `0` (disabled) and `1` (enabled).
        :type KeepEnable: int
        :param KeepTime: Session persistence duration, in seconds.
        :type KeepTime: int
        :param SourceType: Forwarding method. Valid values: `1` (by domain name); `2` (by IP).
        :type SourceType: int
        :param SourceList: List of origins
        :type SourceList: list of L4RuleSource
        :param Region: Region code.
        :type Region: int
        :param Id: Resource ID.
        :type Id: str
        :param Ip: Anti-DDoS instance IP address.
        :type Ip: str
        :param RuleId: Rule ID. This field is not required for adding a rule, but is required for modifying or deleting a rule.
        :type RuleId: str
        :param RuleName: Rule description.
        :type RuleName: str
        :param CertType: Certificate source. When the forwarding protocol is HTTPS, this field must be set to `2` (Tencent Cloud managed certificate), and for HTTP protocol, it can be set to `0`.
        :type CertType: int
        :param SSLId: When the certificate is managed by Tencent Cloud, this field must be set to the ID of the managed certificate.
        :type SSLId: str
        :param Cert: [Disused] When the certificate is an external certificate, the certificate content should be provided here. 
        :type Cert: str
        :param PrivateKey: [Disused] When the certificate is an external certificate, the certificate key should be provided here. 
        :type PrivateKey: str
        :param Status: Rule status. Valid values: `0` (the rule was successfully configured), `1` (configuring the rule), `2` (rule configuration failed), `3` (deleting the rule), `5` (failed to delete rule), `6` (rule awaiting configuration), `7` (rule awaiting deletion), and `8` (rule awaiting certificate configuration).
        :type Status: int
        :param CCStatus: CC protection status. Valid values: `0` (disabled) and `1` (enabled).
        :type CCStatus: int
        :param CCEnable: CC protection status based on HTTPS. Valid values: `0` (disabled) and `1` (enabled).
        :type CCEnable: int
        :param CCThreshold: CC protection threshold based on HTTPS.
        :type CCThreshold: int
        :param CCLevel: CC protection level based on HTTPS.
        :type CCLevel: str
        :param ModifyTime: Modification time.
        :type ModifyTime: str
        :param HttpsToHttpEnable: Whether to enable **Forward HTTPS requests via HTTP**. Valid values: `0` (disabled) and `1` (enabled). It defaults to `0`.
        :type HttpsToHttpEnable: int
        :param VirtualPort: Access port number.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type VirtualPort: int
        :param RewriteHttps: Specifies whether to forcibly redirect HTTP to HTTPS. `1`: Enable. `0`: Disable.
        :type RewriteHttps: int
        :param ErrCode: Returns an error code when the rule configuration fails (only valid when `Status=2`). `1001`: The certificate does not exist. `1002`: Failed to obtain the certificate. `1003`: Failed to upload the certificate. `1004`: The certificate has expired.
        :type ErrCode: int
        :param Version: Version
Note: This field may return null, indicating that no valid values can be obtained.
        :type Version: int
        """
        self.Protocol = None
        self.Domain = None
        self.LbType = None
        self.KeepEnable = None
        self.KeepTime = None
        self.SourceType = None
        self.SourceList = None
        self.Region = None
        self.Id = None
        self.Ip = None
        self.RuleId = None
        self.RuleName = None
        self.CertType = None
        self.SSLId = None
        self.Cert = None
        self.PrivateKey = None
        self.Status = None
        self.CCStatus = None
        self.CCEnable = None
        self.CCThreshold = None
        self.CCLevel = None
        self.ModifyTime = None
        self.HttpsToHttpEnable = None
        self.VirtualPort = None
        self.RewriteHttps = None
        self.ErrCode = None
        self.Version = None


    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.Domain = params.get("Domain")
        self.LbType = params.get("LbType")
        self.KeepEnable = params.get("KeepEnable")
        self.KeepTime = params.get("KeepTime")
        self.SourceType = params.get("SourceType")
        if params.get("SourceList") is not None:
            self.SourceList = []
            for item in params.get("SourceList"):
                obj = L4RuleSource()
                obj._deserialize(item)
                self.SourceList.append(obj)
        self.Region = params.get("Region")
        self.Id = params.get("Id")
        self.Ip = params.get("Ip")
        self.RuleId = params.get("RuleId")
        self.RuleName = params.get("RuleName")
        self.CertType = params.get("CertType")
        self.SSLId = params.get("SSLId")
        self.Cert = params.get("Cert")
        self.PrivateKey = params.get("PrivateKey")
        self.Status = params.get("Status")
        self.CCStatus = params.get("CCStatus")
        self.CCEnable = params.get("CCEnable")
        self.CCThreshold = params.get("CCThreshold")
        self.CCLevel = params.get("CCLevel")
        self.ModifyTime = params.get("ModifyTime")
        self.HttpsToHttpEnable = params.get("HttpsToHttpEnable")
        self.VirtualPort = params.get("VirtualPort")
        self.RewriteHttps = params.get("RewriteHttps")
        self.ErrCode = params.get("ErrCode")
        self.Version = params.get("Version")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OverviewDDoSEvent(AbstractModel):
    """DDoS events recorded

    """

    def __init__(self):
        r"""
        :param Id: Event ID
        :type Id: str
        :param Vip: IP
        :type Vip: str
        :param StartTime: Start time
        :type StartTime: str
        :param EndTime: End time
        :type EndTime: str
        :param AttackType: Attack type
        :type AttackType: str
        :param AttackStatus: Attack status. `0`: The attack is ongoing; `1`: The attack ends.
        :type AttackStatus: int
        :param Mbps: Attack traffic, in Mbps
        :type Mbps: int
        :param Pps: Attack packets, in PPS
        :type Pps: int
        :param Business: Anti-DDoS service type. `bgp-multip`: Anti-DDoS Pro; `bgpip`: Anti-DDoS Advanced; `basic`: Anti-DDoS Basic.
        :type Business: str
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param InstanceName: Anti-DDoS instance name
        :type InstanceName: str
        """
        self.Id = None
        self.Vip = None
        self.StartTime = None
        self.EndTime = None
        self.AttackType = None
        self.AttackStatus = None
        self.Mbps = None
        self.Pps = None
        self.Business = None
        self.InstanceId = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Vip = params.get("Vip")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.AttackType = params.get("AttackType")
        self.AttackStatus = params.get("AttackStatus")
        self.Mbps = params.get("Mbps")
        self.Pps = params.get("Pps")
        self.Business = params.get("Business")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PackInfo(AbstractModel):
    """Package information

    """

    def __init__(self):
        r"""
        :param PackType: Package type. Valid values:
`staticpack`: non-BGP package
`insurance`: guarantee package
]
        :type PackType: str
        :param PackId: Package ID
        :type PackId: str
        """
        self.PackType = None
        self.PackId = None


    def _deserialize(self, params):
        self.PackType = params.get("PackType")
        self.PackId = params.get("PackId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PacketFilterConfig(AbstractModel):
    """Feature filtering configuration

    """

    def __init__(self):
        r"""
        :param Protocol: Protocol. Valid values: `tcp`, `udp`, `icmp`, `all`.
        :type Protocol: str
        :param SportStart: Start source port. Value range: 0–65535.
        :type SportStart: int
        :param SportEnd: End source port. Value range: 0–65535. The value also should be greater than or equal to that of the start source port.
        :type SportEnd: int
        :param DportStart: Start destination port
        :type DportStart: int
        :param DportEnd: End destination port. Value range: 1–65535. The value also should be greater than or equal to that of the start source port.
        :type DportEnd: int
        :param PktlenMin: Minimum message length. Value range: 1–1500.
        :type PktlenMin: int
        :param PktlenMax: Maximum message length. Value range: 1–1500. The value also should be greater than or equal to that of the minimum message length.
        :type PktlenMax: int
        :param Action: Action. Valid values:
`drop`: discards the request.
`transmit`: allows the request.
`drop_black`: discards the request and adds the IP to blocklist.
`drop_rst`: blocks the request.
`drop_black_rst`: blocks the request and adds the IP to blocklist.
`forward`: continues protection.
]
        :type Action: str
        :param MatchBegin: Detection location:
`begin_l3`: IP header
`begin_l4`: TCP/UDP header
`begin_l5`: T load
`no_match`: no match
]
        :type MatchBegin: str
        :param MatchType: Detection type:
`sunday`: keyword
`pcre`: regular expression
]
        :type MatchType: str
        :param Str: Detection value. Should be in key string or regular expression. 
When the `MatchType` is `sunday`, enter a string or a string in hexadecimal byte code representation. For example, a string "123" corresponds to the hexadecimal byte code "\x313233".
When the `MatchType` is `pcre`, enter a regular expression.
]
        :type Str: str
        :param Depth: Detection depth starting from the detection position. Value range: [0, 1500].
        :type Depth: int
        :param Offset: Offset starting from the detection position. Value range: [0, Depth].
        :type Offset: int
        :param IsNot: Whether the detection value is included:
`0`: included
`1`: excluded
]
        :type IsNot: int
        :param MatchLogic: Relationship between the first and second detection conditions:
`and`: under both the first and second detection conditions
`none`: under only the first detection condition
]
        :type MatchLogic: str
        :param MatchBegin2: The second detection position:
`begin_l5`: load
`no_match`: no match
]
        :type MatchBegin2: str
        :param MatchType2: The second detection type:
`sunday`: keyword
`pcre`: regular expression
]
        :type MatchType2: str
        :param Str2: The second detection value. Should be in key string or regular expression.
When the `MatchType` is `sunday`, enter a string or a string in hexadecimal byte code representation. For example, a string "123" corresponds to the hexadecimal byte code "\x313233".
When the `MatchType` is `pcre`, enter a regular expression.
]
        :type Str2: str
        :param Depth2: Detection depth starting from the second detection position. Value range: [0, 1500].
        :type Depth2: int
        :param Offset2: Offset starting from the second detection position. Value range: [0, Depth2].
        :type Offset2: int
        :param IsNot2: Whether the second detection value is included:
`0`: included
`1`: excluded
]
        :type IsNot2: int
        :param Id: A rule ID is generated after a feature filtering configuration is added successfully. Leave this field empty when adding a new feature filtering configuration.
        :type Id: str
        :param PktLenGT: Byte threshold of the packet. Packets larger than the specified size are not returned. It must be an integer larger than 1.
        :type PktLenGT: int
        """
        self.Protocol = None
        self.SportStart = None
        self.SportEnd = None
        self.DportStart = None
        self.DportEnd = None
        self.PktlenMin = None
        self.PktlenMax = None
        self.Action = None
        self.MatchBegin = None
        self.MatchType = None
        self.Str = None
        self.Depth = None
        self.Offset = None
        self.IsNot = None
        self.MatchLogic = None
        self.MatchBegin2 = None
        self.MatchType2 = None
        self.Str2 = None
        self.Depth2 = None
        self.Offset2 = None
        self.IsNot2 = None
        self.Id = None
        self.PktLenGT = None


    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.SportStart = params.get("SportStart")
        self.SportEnd = params.get("SportEnd")
        self.DportStart = params.get("DportStart")
        self.DportEnd = params.get("DportEnd")
        self.PktlenMin = params.get("PktlenMin")
        self.PktlenMax = params.get("PktlenMax")
        self.Action = params.get("Action")
        self.MatchBegin = params.get("MatchBegin")
        self.MatchType = params.get("MatchType")
        self.Str = params.get("Str")
        self.Depth = params.get("Depth")
        self.Offset = params.get("Offset")
        self.IsNot = params.get("IsNot")
        self.MatchLogic = params.get("MatchLogic")
        self.MatchBegin2 = params.get("MatchBegin2")
        self.MatchType2 = params.get("MatchType2")
        self.Str2 = params.get("Str2")
        self.Depth2 = params.get("Depth2")
        self.Offset2 = params.get("Offset2")
        self.IsNot2 = params.get("IsNot2")
        self.Id = params.get("Id")
        self.PktLenGT = params.get("PktLenGT")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PacketFilterRelation(AbstractModel):
    """Feature filtering information

    """

    def __init__(self):
        r"""
        :param PacketFilterConfig: Feature filtering configuration
        :type PacketFilterConfig: :class:`tencentcloud.antiddos.v20200309.models.PacketFilterConfig`
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        :param ModifyTime: Modification time
        :type ModifyTime: str
        """
        self.PacketFilterConfig = None
        self.InstanceDetailList = None
        self.ModifyTime = None


    def _deserialize(self, params):
        if params.get("PacketFilterConfig") is not None:
            self.PacketFilterConfig = PacketFilterConfig()
            self.PacketFilterConfig._deserialize(params.get("PacketFilterConfig"))
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        self.ModifyTime = params.get("ModifyTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PortSegment(AbstractModel):
    """Port range information

    """

    def __init__(self):
        r"""
        :param BeginPort: Start port. Value range: 1–65535.
        :type BeginPort: int
        :param EndPort: End port. The value should be in the range 1–65535 and cannot be less than that of the start port.
        :type EndPort: int
        """
        self.BeginPort = None
        self.EndPort = None


    def _deserialize(self, params):
        self.BeginPort = params.get("BeginPort")
        self.EndPort = params.get("EndPort")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProtectThresholdRelation(AbstractModel):
    """Protection threshold configuration information

    """

    def __init__(self):
        r"""
        :param DDoSLevel: DDoS protection level:
`low`: loose protection
`middle`: medium protection
`high`: strict protection
]
        :type DDoSLevel: str
        :param DDoSThreshold: DDoS cleansing threshold (in Mbps)
        :type DDoSThreshold: int
        :param DDoSAI: DDoS AI protection switch:
`on`: enabled
`off`: disabled
]
        :type DDoSAI: str
        :param CCEnable: CC cleansing switch
`0`: disabled
`1`: enabled
]
        :type CCEnable: int
        :param CCThreshold: CC cleansing threshold (in QPS)
        :type CCThreshold: int
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        :param ListenerCcThresholdList: Domain name and protocol protection thresholds
        :type ListenerCcThresholdList: list of ListenerCcThreholdConfig
        :param SynFloodThreshold: SYN traffic threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type SynFloodThreshold: int
        :param SynFloodPktThreshold: SYN packet threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type SynFloodPktThreshold: int
        :param UdpFloodThreshold: UDP traffic threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type UdpFloodThreshold: int
        :param UdpFloodPktThreshold: UDP packet threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type UdpFloodPktThreshold: int
        :param AckFloodThreshold: ACK traffic threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type AckFloodThreshold: int
        :param AckFloodPktThreshold: ACK packet threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type AckFloodPktThreshold: int
        :param SynAckFloodThreshold: SYNACK traffic threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type SynAckFloodThreshold: int
        :param SynAckFloodPktThreshold: SYNACK packet threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type SynAckFloodPktThreshold: int
        :param RstFloodThreshold: RST traffic threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type RstFloodThreshold: int
        :param RstFloodPktThreshold: RST packet threshold
Note: This field may return null, indicating that no valid values can be obtained.
        :type RstFloodPktThreshold: int
        """
        self.DDoSLevel = None
        self.DDoSThreshold = None
        self.DDoSAI = None
        self.CCEnable = None
        self.CCThreshold = None
        self.InstanceDetailList = None
        self.ListenerCcThresholdList = None
        self.SynFloodThreshold = None
        self.SynFloodPktThreshold = None
        self.UdpFloodThreshold = None
        self.UdpFloodPktThreshold = None
        self.AckFloodThreshold = None
        self.AckFloodPktThreshold = None
        self.SynAckFloodThreshold = None
        self.SynAckFloodPktThreshold = None
        self.RstFloodThreshold = None
        self.RstFloodPktThreshold = None


    def _deserialize(self, params):
        self.DDoSLevel = params.get("DDoSLevel")
        self.DDoSThreshold = params.get("DDoSThreshold")
        self.DDoSAI = params.get("DDoSAI")
        self.CCEnable = params.get("CCEnable")
        self.CCThreshold = params.get("CCThreshold")
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        if params.get("ListenerCcThresholdList") is not None:
            self.ListenerCcThresholdList = []
            for item in params.get("ListenerCcThresholdList"):
                obj = ListenerCcThreholdConfig()
                obj._deserialize(item)
                self.ListenerCcThresholdList.append(obj)
        self.SynFloodThreshold = params.get("SynFloodThreshold")
        self.SynFloodPktThreshold = params.get("SynFloodPktThreshold")
        self.UdpFloodThreshold = params.get("UdpFloodThreshold")
        self.UdpFloodPktThreshold = params.get("UdpFloodPktThreshold")
        self.AckFloodThreshold = params.get("AckFloodThreshold")
        self.AckFloodPktThreshold = params.get("AckFloodPktThreshold")
        self.SynAckFloodThreshold = params.get("SynAckFloodThreshold")
        self.SynAckFloodPktThreshold = params.get("SynAckFloodPktThreshold")
        self.RstFloodThreshold = params.get("RstFloodThreshold")
        self.RstFloodPktThreshold = params.get("RstFloodPktThreshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProtocolBlockConfig(AbstractModel):
    """Protocol blocking configuration

    """

    def __init__(self):
        r"""
        :param DropTcp: TCP blocking. Valid values: `0` (disabled), `1`(enabled).
        :type DropTcp: int
        :param DropUdp: UDP blocking. Valid values: `0` (disabled), `1`(enabled).
        :type DropUdp: int
        :param DropIcmp: ICMP blocking. Valid values: `0` (disabled), `1`(enabled).
        :type DropIcmp: int
        :param DropOther: Other protocol blocking. Valid values: `0` (disabled), `1`(enabled).
        :type DropOther: int
        :param CheckExceptNullConnect: Null connection protection. Valid values: `0` (disabled), `1` (enabled).
        :type CheckExceptNullConnect: int
        :param PingOfDeath: PoD protection. Values: `0` (disable), `1` (enable).
        :type PingOfDeath: int
        :param TearDrop: Teardrop protection. Values: `0` (disable), `1` (enable).
        :type TearDrop: int
        """
        self.DropTcp = None
        self.DropUdp = None
        self.DropIcmp = None
        self.DropOther = None
        self.CheckExceptNullConnect = None
        self.PingOfDeath = None
        self.TearDrop = None


    def _deserialize(self, params):
        self.DropTcp = params.get("DropTcp")
        self.DropUdp = params.get("DropUdp")
        self.DropIcmp = params.get("DropIcmp")
        self.DropOther = params.get("DropOther")
        self.CheckExceptNullConnect = params.get("CheckExceptNullConnect")
        self.PingOfDeath = params.get("PingOfDeath")
        self.TearDrop = params.get("TearDrop")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProtocolBlockRelation(AbstractModel):
    """Protocol blocking information

    """

    def __init__(self):
        r"""
        :param ProtocolBlockConfig: Protocol blocking configuration
        :type ProtocolBlockConfig: :class:`tencentcloud.antiddos.v20200309.models.ProtocolBlockConfig`
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        """
        self.ProtocolBlockConfig = None
        self.InstanceDetailList = None


    def _deserialize(self, params):
        if params.get("ProtocolBlockConfig") is not None:
            self.ProtocolBlockConfig = ProtocolBlockConfig()
            self.ProtocolBlockConfig._deserialize(params.get("ProtocolBlockConfig"))
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProtocolPort(AbstractModel):
    """"Protocol" and "Port" parameters

    """

    def __init__(self):
        r"""
        :param Protocol: Protocol. Valid values: `tcp`, `udp`
        :type Protocol: str
        :param Port: Port
        :type Port: int
        """
        self.Protocol = None
        self.Port = None


    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProxyTypeInfo(AbstractModel):
    """Forwarding type

    """

    def __init__(self):
        r"""
        :param ProxyPorts: List of forwarding listening ports. Value range: 1–65535.
        :type ProxyPorts: list of int
        :param ProxyType: Forwarding protocol:
`http`: HTTP protocol
`https`: HTTPS protocol
]
        :type ProxyType: str
        """
        self.ProxyPorts = None
        self.ProxyType = None


    def _deserialize(self, params):
        self.ProxyPorts = params.get("ProxyPorts")
        self.ProxyType = params.get("ProxyType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RegionInfo(AbstractModel):
    """Region information.

    """

    def __init__(self):
        r"""
        :param Region: Region name, such as `ap-guangzhou`
        :type Region: str
        """
        self.Region = None


    def _deserialize(self, params):
        self.Region = params.get("Region")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RuleInstanceRelation(AbstractModel):
    """Information of the Anti-DDoS instance using layer-4/7 forwarding rules

    """

    def __init__(self):
        r"""
        :param EipList: Instance IP
        :type EipList: list of str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Cname: Instance CNAME
        :type Cname: str
        """
        self.EipList = None
        self.InstanceId = None
        self.Cname = None


    def _deserialize(self, params):
        self.EipList = params.get("EipList")
        self.InstanceId = params.get("InstanceId")
        self.Cname = params.get("Cname")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SchedulingDomainInfo(AbstractModel):
    """Scheduling domain name details

    """

    def __init__(self):
        r"""
        :param Domain: Scheduling domain name
        :type Domain: str
        :param LineIPList: List of line IPs
        :type LineIPList: list of IPLineInfo
        :param Method: Scheduling mode. Valid value: `priority` (priority scheduling).
        :type Method: str
        :param TTL: TTL value recorded from the scheduling domain name resolution
        :type TTL: int
        :param Status: Running status. Valid values:
`0`: not running
`1`: running
`2`: abnormal
]
        :type Status: int
        :param CreatedTime: Creation time
        :type CreatedTime: str
        :param ModifyTime: Last modification time
        :type ModifyTime: str
        :param UsrDomainName: Domain name
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type UsrDomainName: str
        """
        self.Domain = None
        self.LineIPList = None
        self.Method = None
        self.TTL = None
        self.Status = None
        self.CreatedTime = None
        self.ModifyTime = None
        self.UsrDomainName = None


    def _deserialize(self, params):
        self.Domain = params.get("Domain")
        if params.get("LineIPList") is not None:
            self.LineIPList = []
            for item in params.get("LineIPList"):
                obj = IPLineInfo()
                obj._deserialize(item)
                self.LineIPList.append(obj)
        self.Method = params.get("Method")
        self.TTL = params.get("TTL")
        self.Status = params.get("Status")
        self.CreatedTime = params.get("CreatedTime")
        self.ModifyTime = params.get("ModifyTime")
        self.UsrDomainName = params.get("UsrDomainName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SourceServer(AbstractModel):
    """Real server details

    """

    def __init__(self):
        r"""
        :param RealServer: Types of the real server address, such as IP or domain name.
        :type RealServer: str
        :param RsType: Types of the real server address:
`1`: domain name
`2`: IP
]
        :type RsType: int
        :param Weight: Forward weight of the real server. Value range: 1–100.
        :type Weight: int
        :param Port: Port number. Value range: 0-65535.
        :type Port: int
        """
        self.RealServer = None
        self.RsType = None
        self.Weight = None
        self.Port = None


    def _deserialize(self, params):
        self.RealServer = params.get("RealServer")
        self.RsType = params.get("RsType")
        self.Weight = params.get("Weight")
        self.Port = params.get("Port")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SpeedValue(AbstractModel):
    """Rate limit value types, such as pps and bps.

    """

    def __init__(self):
        r"""
        :param Type: Rate limit value types:
`1`: packets per second (pps)
`2`: bits per second (bps)
]
        :type Type: int
        :param Value: Value
        :type Value: int
        """
        self.Type = None
        self.Value = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StaticPackRelation(AbstractModel):
    """Non-BGP package details

    """

    def __init__(self):
        r"""
        :param ProtectBandwidth: Base protection bandwidth
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ProtectBandwidth: int
        :param NormalBandwidth: Application bandwidth
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type NormalBandwidth: int
        :param ForwardRulesLimit: Forwarding rules
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ForwardRulesLimit: int
        :param AutoRenewFlag: Auto-renewal flag
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type AutoRenewFlag: int
        :param CurDeadline: Expiration time
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type CurDeadline: str
        """
        self.ProtectBandwidth = None
        self.NormalBandwidth = None
        self.ForwardRulesLimit = None
        self.AutoRenewFlag = None
        self.CurDeadline = None


    def _deserialize(self, params):
        self.ProtectBandwidth = params.get("ProtectBandwidth")
        self.NormalBandwidth = params.get("NormalBandwidth")
        self.ForwardRulesLimit = params.get("ForwardRulesLimit")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.CurDeadline = params.get("CurDeadline")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SuccessCode(AbstractModel):
    """Return code, only used to report success.

    """

    def __init__(self):
        r"""
        :param Message: Description
        :type Message: str
        :param Code: Success/Error code
        :type Code: str
        """
        self.Message = None
        self.Code = None


    def _deserialize(self, params):
        self.Message = params.get("Message")
        self.Code = params.get("Code")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchWaterPrintConfigRequest(AbstractModel):
    """SwitchWaterPrintConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Anti-DDoS instance ID
        :type InstanceId: str
        :param OpenStatus: Watermark status. `1`: enabled; `0`: disabled.
        :type OpenStatus: int
        :param CloudSdkProxy: Whether to enable proxy. Values: `1` (Enable proxy and ignore IP+port verification), `0` (Do not enable proxy and IP+port verification is required)
        :type CloudSdkProxy: int
        """
        self.InstanceId = None
        self.OpenStatus = None
        self.CloudSdkProxy = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.OpenStatus = params.get("OpenStatus")
        self.CloudSdkProxy = params.get("CloudSdkProxy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchWaterPrintConfigResponse(AbstractModel):
    """SwitchWaterPrintConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class TagFilter(AbstractModel):
    """Tag type

    """

    def __init__(self):
        r"""
        :param TagKey: Tag key
        :type TagKey: str
        :param TagValue: Tag value
        :type TagValue: list of str
        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TagInfo(AbstractModel):
    """Tag information, which is used to return the tag of the associated instance

    """

    def __init__(self):
        r"""
        :param TagKey: Tag key
        :type TagKey: str
        :param TagValue: Tag value
        :type TagValue: str
        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WaterPrintConfig(AbstractModel):
    """Watermark configuration

    """

    def __init__(self):
        r"""
        :param Offset: Watermark offset. Value range: [0, 100).
        :type Offset: int
        :param OpenStatus: Start status. Valid values:
`0`: manual start
`1`: instant start
]
        :type OpenStatus: int
        :param Listeners: List of forwarding listeners configured
        :type Listeners: list of ForwardListener
        :param Keys: A list of watermark keys is generated after a watermark is added successfully. Each watermark can have up to 2 keys. When there is only one valid key, it cannot be deleted.
        :type Keys: list of WaterPrintKey
        :param Verify: Watermark checking mode, which can be:
`checkall`: normal mode
`shortfpcheckall`: compact mode
]
        :type Verify: str
        :param CloudSdkProxy: Whether to enable proxy. Values: `1` (Enable proxy and ignore IP+port verification), `0` (Do not enable proxy and IP+port verification is required)
Note: This field may return null, indicating that no valid values can be obtained.
        :type CloudSdkProxy: int
        """
        self.Offset = None
        self.OpenStatus = None
        self.Listeners = None
        self.Keys = None
        self.Verify = None
        self.CloudSdkProxy = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.OpenStatus = params.get("OpenStatus")
        if params.get("Listeners") is not None:
            self.Listeners = []
            for item in params.get("Listeners"):
                obj = ForwardListener()
                obj._deserialize(item)
                self.Listeners.append(obj)
        if params.get("Keys") is not None:
            self.Keys = []
            for item in params.get("Keys"):
                obj = WaterPrintKey()
                obj._deserialize(item)
                self.Keys.append(obj)
        self.Verify = params.get("Verify")
        self.CloudSdkProxy = params.get("CloudSdkProxy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WaterPrintKey(AbstractModel):
    """Created watermark key

    """

    def __init__(self):
        r"""
        :param KeyVersion: Key version
        :type KeyVersion: str
        :param KeyContent: Key content
        :type KeyContent: str
        :param KeyId: Key ID
        :type KeyId: str
        :param KeyOpenStatus: Key status. Valid value: `1` (enabled).
        :type KeyOpenStatus: int
        :param CreateTime: Key creation time
        :type CreateTime: str
        """
        self.KeyVersion = None
        self.KeyContent = None
        self.KeyId = None
        self.KeyOpenStatus = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.KeyVersion = params.get("KeyVersion")
        self.KeyContent = params.get("KeyContent")
        self.KeyId = params.get("KeyId")
        self.KeyOpenStatus = params.get("KeyOpenStatus")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WaterPrintRelation(AbstractModel):
    """Watermark configuration details

    """

    def __init__(self):
        r"""
        :param WaterPrintConfig: Watermark configuration
        :type WaterPrintConfig: :class:`tencentcloud.antiddos.v20200309.models.WaterPrintConfig`
        :param InstanceDetailList: Anti-DDoS instance configured
        :type InstanceDetailList: list of InstanceRelation
        """
        self.WaterPrintConfig = None
        self.InstanceDetailList = None


    def _deserialize(self, params):
        if params.get("WaterPrintConfig") is not None:
            self.WaterPrintConfig = WaterPrintConfig()
            self.WaterPrintConfig._deserialize(params.get("WaterPrintConfig"))
        if params.get("InstanceDetailList") is not None:
            self.InstanceDetailList = []
            for item in params.get("InstanceDetailList"):
                obj = InstanceRelation()
                obj._deserialize(item)
                self.InstanceDetailList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        