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


class AddUsersForUserManagerRequest(AbstractModel):
    """AddUsersForUserManager request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Cluster string ID
        :type InstanceId: str
        :param UserManagerUserList: User information list
        :type UserManagerUserList: list of UserInfoForUserManager
        """
        self.InstanceId = None
        self.UserManagerUserList = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("UserManagerUserList") is not None:
            self.UserManagerUserList = []
            for item in params.get("UserManagerUserList"):
                obj = UserInfoForUserManager()
                obj._deserialize(item)
                self.UserManagerUserList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddUsersForUserManagerResponse(AbstractModel):
    """AddUsersForUserManager response structure.

    """

    def __init__(self):
        r"""
        :param SuccessUserList: The user list that is successfully added
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type SuccessUserList: list of str
        :param FailedUserList: The user list that is not successfully added
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type FailedUserList: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SuccessUserList = None
        self.FailedUserList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SuccessUserList = params.get("SuccessUserList")
        self.FailedUserList = params.get("FailedUserList")
        self.RequestId = params.get("RequestId")


class AllNodeResourceSpec(AbstractModel):
    """Resource description

    """

    def __init__(self):
        r"""
        :param MasterResourceSpec: The description of master nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type MasterResourceSpec: :class:`tencentcloud.emr.v20190103.models.NodeResourceSpec`
        :param CoreResourceSpec: The description of core nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CoreResourceSpec: :class:`tencentcloud.emr.v20190103.models.NodeResourceSpec`
        :param TaskResourceSpec: The description of task nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type TaskResourceSpec: :class:`tencentcloud.emr.v20190103.models.NodeResourceSpec`
        :param CommonResourceSpec: The description of common nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CommonResourceSpec: :class:`tencentcloud.emr.v20190103.models.NodeResourceSpec`
        :param MasterCount: The number of master nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type MasterCount: int
        :param CoreCount: The number of core nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CoreCount: int
        :param TaskCount: The number of task nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type TaskCount: int
        :param CommonCount: The number of common nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CommonCount: int
        """
        self.MasterResourceSpec = None
        self.CoreResourceSpec = None
        self.TaskResourceSpec = None
        self.CommonResourceSpec = None
        self.MasterCount = None
        self.CoreCount = None
        self.TaskCount = None
        self.CommonCount = None


    def _deserialize(self, params):
        if params.get("MasterResourceSpec") is not None:
            self.MasterResourceSpec = NodeResourceSpec()
            self.MasterResourceSpec._deserialize(params.get("MasterResourceSpec"))
        if params.get("CoreResourceSpec") is not None:
            self.CoreResourceSpec = NodeResourceSpec()
            self.CoreResourceSpec._deserialize(params.get("CoreResourceSpec"))
        if params.get("TaskResourceSpec") is not None:
            self.TaskResourceSpec = NodeResourceSpec()
            self.TaskResourceSpec._deserialize(params.get("TaskResourceSpec"))
        if params.get("CommonResourceSpec") is not None:
            self.CommonResourceSpec = NodeResourceSpec()
            self.CommonResourceSpec._deserialize(params.get("CommonResourceSpec"))
        self.MasterCount = params.get("MasterCount")
        self.CoreCount = params.get("CoreCount")
        self.TaskCount = params.get("TaskCount")
        self.CommonCount = params.get("CommonCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ApplicationStatics(AbstractModel):
    """Yarn application statistics

    """

    def __init__(self):
        r"""
        :param Queue: Queue name
        :type Queue: str
        :param User: Username
        :type User: str
        :param ApplicationType: Application type
        :type ApplicationType: str
        :param SumMemorySeconds: `SumMemorySeconds` meaning
        :type SumMemorySeconds: int
        :param SumVCoreSeconds: 
        :type SumVCoreSeconds: int
        :param SumHDFSBytesWritten: SumHDFSBytesWritten (with unit)
        :type SumHDFSBytesWritten: str
        :param SumHDFSBytesRead: SumHDFSBytesRead (with unit)
        :type SumHDFSBytesRead: str
        :param CountApps: Application count
        :type CountApps: int
        """
        self.Queue = None
        self.User = None
        self.ApplicationType = None
        self.SumMemorySeconds = None
        self.SumVCoreSeconds = None
        self.SumHDFSBytesWritten = None
        self.SumHDFSBytesRead = None
        self.CountApps = None


    def _deserialize(self, params):
        self.Queue = params.get("Queue")
        self.User = params.get("User")
        self.ApplicationType = params.get("ApplicationType")
        self.SumMemorySeconds = params.get("SumMemorySeconds")
        self.SumVCoreSeconds = params.get("SumVCoreSeconds")
        self.SumHDFSBytesWritten = params.get("SumHDFSBytesWritten")
        self.SumHDFSBytesRead = params.get("SumHDFSBytesRead")
        self.CountApps = params.get("CountApps")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class COSSettings(AbstractModel):
    """COS-related configuration

    """

    def __init__(self):
        r"""
        :param CosSecretId: COS `SecretId`
        :type CosSecretId: str
        :param CosSecretKey: COS `SecrectKey`
        :type CosSecretKey: str
        :param LogOnCosPath: COS path to log
        :type LogOnCosPath: str
        """
        self.CosSecretId = None
        self.CosSecretKey = None
        self.LogOnCosPath = None


    def _deserialize(self, params):
        self.CosSecretId = params.get("CosSecretId")
        self.CosSecretKey = params.get("CosSecretKey")
        self.LogOnCosPath = params.get("LogOnCosPath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CdbInfo(AbstractModel):
    """Output parameters

    """

    def __init__(self):
        r"""
        :param InstanceName: Database instance
Note: this field may return null, indicating that no valid values can be obtained.
        :type InstanceName: str
        :param Ip: Database IP
Note: this field may return null, indicating that no valid values can be obtained.
        :type Ip: str
        :param Port: Database port
Note: this field may return null, indicating that no valid values can be obtained.
        :type Port: int
        :param MemSize: Database memory specification
Note: this field may return null, indicating that no valid values can be obtained.
        :type MemSize: int
        :param Volume: Database disk specification
Note: this field may return null, indicating that no valid values can be obtained.
        :type Volume: int
        :param Service: Service flag
Note: this field may return null, indicating that no valid values can be obtained.
        :type Service: str
        :param ExpireTime: Expiration time
Note: this field may return null, indicating that no valid values can be obtained.
        :type ExpireTime: str
        :param ApplyTime: Application time
Note: this field may return null, indicating that no valid values can be obtained.
        :type ApplyTime: str
        :param PayType: Payment type
Note: this field may return null, indicating that no valid values can be obtained.
        :type PayType: int
        :param ExpireFlag: Expiration flag
Note: this field may return null, indicating that no valid values can be obtained.
        :type ExpireFlag: bool
        :param Status: Database status
Note: this field may return null, indicating that no valid values can be obtained.
        :type Status: int
        :param IsAutoRenew: Renewal flag
Note: this field may return null, indicating that no valid values can be obtained.
        :type IsAutoRenew: int
        :param SerialNo: Database string
Note: this field may return null, indicating that no valid values can be obtained.
        :type SerialNo: str
        :param ZoneId: ZoneId
Note: this field may return null, indicating that no valid values can be obtained.
        :type ZoneId: int
        :param RegionId: RegionId
Note: this field may return null, indicating that no valid values can be obtained.
        :type RegionId: int
        """
        self.InstanceName = None
        self.Ip = None
        self.Port = None
        self.MemSize = None
        self.Volume = None
        self.Service = None
        self.ExpireTime = None
        self.ApplyTime = None
        self.PayType = None
        self.ExpireFlag = None
        self.Status = None
        self.IsAutoRenew = None
        self.SerialNo = None
        self.ZoneId = None
        self.RegionId = None


    def _deserialize(self, params):
        self.InstanceName = params.get("InstanceName")
        self.Ip = params.get("Ip")
        self.Port = params.get("Port")
        self.MemSize = params.get("MemSize")
        self.Volume = params.get("Volume")
        self.Service = params.get("Service")
        self.ExpireTime = params.get("ExpireTime")
        self.ApplyTime = params.get("ApplyTime")
        self.PayType = params.get("PayType")
        self.ExpireFlag = params.get("ExpireFlag")
        self.Status = params.get("Status")
        self.IsAutoRenew = params.get("IsAutoRenew")
        self.SerialNo = params.get("SerialNo")
        self.ZoneId = params.get("ZoneId")
        self.RegionId = params.get("RegionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterExternalServiceInfo(AbstractModel):
    """Relationship between shared components and the current cluster

    """

    def __init__(self):
        r"""
        :param DependType: Dependency. `0`: Other clusters depend on the current cluster. `1`: The current cluster depends on other clusters.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type DependType: int
        :param Service: Shared component
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type Service: str
        :param ClusterId: Sharing cluster
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type ClusterId: str
        :param ClusterStatus: Sharing cluster status
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type ClusterStatus: int
        """
        self.DependType = None
        self.Service = None
        self.ClusterId = None
        self.ClusterStatus = None


    def _deserialize(self, params):
        self.DependType = params.get("DependType")
        self.Service = params.get("Service")
        self.ClusterId = params.get("ClusterId")
        self.ClusterStatus = params.get("ClusterStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClusterInstancesInfo(AbstractModel):
    """Cluster instance information

    """

    def __init__(self):
        r"""
        :param Id: ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type Id: int
        :param ClusterId: Cluster ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type ClusterId: str
        :param Ftitle: Title
Note: this field may return null, indicating that no valid values can be obtained.
        :type Ftitle: str
        :param ClusterName: Cluster name
Note: this field may return null, indicating that no valid values can be obtained.
        :type ClusterName: str
        :param RegionId: Region ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type RegionId: int
        :param ZoneId: Region ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type ZoneId: int
        :param AppId: User APPID
Note: this field may return null, indicating that no valid values can be obtained.
        :type AppId: int
        :param Uin: User UIN
Note: this field may return null, indicating that no valid values can be obtained.
        :type Uin: str
        :param ProjectId: Project ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type ProjectId: int
        :param VpcId: Cluster `VPCID`
Note: this field may return null, indicating that no valid values can be obtained.
        :type VpcId: int
        :param SubnetId: Subnet ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type SubnetId: int
        :param Status: Instance status code. Value range:
<li>2: cluster running</li>
<li>3: creating cluster.</li>
<li>4: scaling out cluster.</li>
<li>5: adding router node in cluster.</li>
<li>6: installing component in cluster.</li>
<li>7: cluster executing command.</li>
<li>8: restarting service.</li>
<li>9: entering maintenance.</li>
<li>10: suspending service.</li>
<li>11: exiting maintenance.</li>
<li>12: exiting suspension.</li>
<li>13: delivering configuration.</li>
<li>14: terminating cluster.</li>
<li>15: terminating core node.</li>
<li>16: terminating task node.</li>
<li>17: terminating router node.</li>
<li>18: changing webproxy password.</li>
<li>19: isolating cluster.</li>
<li>20: resuming cluster.</li>
<li>21: repossessing cluster.</li>
<li>22: waiting for configuration adjustment.</li>
<li>23: cluster isolated.</li>
<li>24: removing node.</li>
<li>33: waiting for refund.</li>
<li>34: refunded.</li>
<li>301: creation failed.</li>
<li>302: scale-out failed.</li>
Note: this field may return null, indicating that no valid values can be obtained.
        :type Status: int
        :param AddTime: Creation time
Note: this field may return null, indicating that no valid values can be obtained.
        :type AddTime: str
        :param RunTime: Execution duration
Note: this field may return null, indicating that no valid values can be obtained.
        :type RunTime: str
        :param Config: Cluster product configuration information
Note: this field may return null, indicating that no valid values can be obtained.
        :type Config: :class:`tencentcloud.emr.v20190103.models.EmrProductConfigOutter`
        :param MasterIp: Public IP of master node
Note: this field may return null, indicating that no valid values can be obtained.
        :type MasterIp: str
        :param EmrVersion: EMR version
Note: this field may return null, indicating that no valid values can be obtained.
        :type EmrVersion: str
        :param ChargeType: Billing mode
Note: this field may return null, indicating that no valid values can be obtained.
        :type ChargeType: int
        :param TradeVersion: Transaction version
Note: this field may return null, indicating that no valid values can be obtained.
        :type TradeVersion: int
        :param ResourceOrderId: Resource order ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type ResourceOrderId: int
        :param IsTradeCluster: Whether this is a paid cluster
Note: this field may return null, indicating that no valid values can be obtained.
        :type IsTradeCluster: int
        :param AlarmInfo: Alarm information for cluster error
Note: this field may return null, indicating that no valid values can be obtained.
        :type AlarmInfo: str
        :param IsWoodpeckerCluster: Whether the new architecture is used
Note: this field may return null, indicating that no valid values can be obtained.
        :type IsWoodpeckerCluster: int
        :param MetaDb: Metadatabase information
Note: this field may return null, indicating that no valid values can be obtained.
        :type MetaDb: str
        :param Tags: Tag information
Note: this field may return null, indicating that no valid values can be obtained.
        :type Tags: list of Tag
        :param HiveMetaDb: Hive metadata
Note: this field may return null, indicating that no valid values can be obtained.
        :type HiveMetaDb: str
        :param ServiceClass: Cluster type: EMR, CLICKHOUSE, DRUID
Note: this field may return null, indicating that no valid values can be obtained.
        :type ServiceClass: str
        :param AliasInfo: Alias serialization of all nodes in cluster
Note: this field may return null, indicating that no valid values can be obtained.
        :type AliasInfo: str
        :param ProductId: Cluster version ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type ProductId: int
        :param Zone: Availability zone
Note: this field may return `null`, indicating that no valid value can be obtained.
        :type Zone: str
        :param SceneName: Scenario name
Note: This field may return `null`, indicating that no valid value was found.
        :type SceneName: str
        :param SceneServiceClass: Scenario-based cluster type
Note: This field may return `null`, indicating that no valid value was found.
        :type SceneServiceClass: str
        :param SceneEmrVersion: Scenario-based EMR version
Note: This field may return `null`, indicating that no valid value was found.
        :type SceneEmrVersion: str
        :param DisplayName: Scenario-based cluster type
Note: This field may return `null`, indicating that no valid value was found.
        :type DisplayName: str
        :param VpcName: VPC name
Note: This field may return `null`, indicating that no valid value was found.
        :type VpcName: str
        :param SubnetName: Subnet name
Note: This field may return `null`, indicating that no valid value was found.
        :type SubnetName: str
        :param ClusterExternalServiceInfo: Cluster dependency
Note: This field may return `null`, indicating that no valid value was found.
        :type ClusterExternalServiceInfo: list of ClusterExternalServiceInfo
        :param UniqVpcId: The VPC ID string type of the cluster
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type UniqVpcId: str
        :param UniqSubnetId: The subnet ID string type of the cluster
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type UniqSubnetId: str
        :param TopologyInfoList: Node information
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type TopologyInfoList: list of TopologyInfo
        :param IsMultiZoneCluster: Multi-AZ cluster
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type IsMultiZoneCluster: bool
        :param IsCvmReplace: Whether the feature of automatic abnormal node replacement is enabled.
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsCvmReplace: bool
        """
        self.Id = None
        self.ClusterId = None
        self.Ftitle = None
        self.ClusterName = None
        self.RegionId = None
        self.ZoneId = None
        self.AppId = None
        self.Uin = None
        self.ProjectId = None
        self.VpcId = None
        self.SubnetId = None
        self.Status = None
        self.AddTime = None
        self.RunTime = None
        self.Config = None
        self.MasterIp = None
        self.EmrVersion = None
        self.ChargeType = None
        self.TradeVersion = None
        self.ResourceOrderId = None
        self.IsTradeCluster = None
        self.AlarmInfo = None
        self.IsWoodpeckerCluster = None
        self.MetaDb = None
        self.Tags = None
        self.HiveMetaDb = None
        self.ServiceClass = None
        self.AliasInfo = None
        self.ProductId = None
        self.Zone = None
        self.SceneName = None
        self.SceneServiceClass = None
        self.SceneEmrVersion = None
        self.DisplayName = None
        self.VpcName = None
        self.SubnetName = None
        self.ClusterExternalServiceInfo = None
        self.UniqVpcId = None
        self.UniqSubnetId = None
        self.TopologyInfoList = None
        self.IsMultiZoneCluster = None
        self.IsCvmReplace = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.ClusterId = params.get("ClusterId")
        self.Ftitle = params.get("Ftitle")
        self.ClusterName = params.get("ClusterName")
        self.RegionId = params.get("RegionId")
        self.ZoneId = params.get("ZoneId")
        self.AppId = params.get("AppId")
        self.Uin = params.get("Uin")
        self.ProjectId = params.get("ProjectId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Status = params.get("Status")
        self.AddTime = params.get("AddTime")
        self.RunTime = params.get("RunTime")
        if params.get("Config") is not None:
            self.Config = EmrProductConfigOutter()
            self.Config._deserialize(params.get("Config"))
        self.MasterIp = params.get("MasterIp")
        self.EmrVersion = params.get("EmrVersion")
        self.ChargeType = params.get("ChargeType")
        self.TradeVersion = params.get("TradeVersion")
        self.ResourceOrderId = params.get("ResourceOrderId")
        self.IsTradeCluster = params.get("IsTradeCluster")
        self.AlarmInfo = params.get("AlarmInfo")
        self.IsWoodpeckerCluster = params.get("IsWoodpeckerCluster")
        self.MetaDb = params.get("MetaDb")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.HiveMetaDb = params.get("HiveMetaDb")
        self.ServiceClass = params.get("ServiceClass")
        self.AliasInfo = params.get("AliasInfo")
        self.ProductId = params.get("ProductId")
        self.Zone = params.get("Zone")
        self.SceneName = params.get("SceneName")
        self.SceneServiceClass = params.get("SceneServiceClass")
        self.SceneEmrVersion = params.get("SceneEmrVersion")
        self.DisplayName = params.get("DisplayName")
        self.VpcName = params.get("VpcName")
        self.SubnetName = params.get("SubnetName")
        if params.get("ClusterExternalServiceInfo") is not None:
            self.ClusterExternalServiceInfo = []
            for item in params.get("ClusterExternalServiceInfo"):
                obj = ClusterExternalServiceInfo()
                obj._deserialize(item)
                self.ClusterExternalServiceInfo.append(obj)
        self.UniqVpcId = params.get("UniqVpcId")
        self.UniqSubnetId = params.get("UniqSubnetId")
        if params.get("TopologyInfoList") is not None:
            self.TopologyInfoList = []
            for item in params.get("TopologyInfoList"):
                obj = TopologyInfo()
                obj._deserialize(item)
                self.TopologyInfoList.append(obj)
        self.IsMultiZoneCluster = params.get("IsMultiZoneCluster")
        self.IsCvmReplace = params.get("IsCvmReplace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ComponentBasicRestartInfo(AbstractModel):
    """Target processes

    """

    def __init__(self):
        r"""
        :param ComponentName: The process name (required), such as NameNode.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ComponentName: str
        :param IpList: The target IP list.
Note: This field may return null, indicating that no valid values can be obtained.
        :type IpList: list of str
        """
        self.ComponentName = None
        self.IpList = None


    def _deserialize(self, params):
        self.ComponentName = params.get("ComponentName")
        self.IpList = params.get("IpList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterRequest(AbstractModel):
    """CreateCluster request structure.

    """

    def __init__(self):
        r"""
        :param ProductVersion: The EMR version, such as `EMR-V2.3.0` that indicates the version 2.3.0 of EMR. You can query the EMR version [here](https://intl.cloud.tencent.com/document/product/589/66338?from_cn_redirect=1).
        :type ProductVersion: str
        :param EnableSupportHAFlag: Whether to enable high availability for nodes. Valid values:
<li>`true`: Enable</li>
<li>`false`: Disable</li>
        :type EnableSupportHAFlag: bool
        :param InstanceName: The instance name.
<li>Length limit: 6–36 characters.</li>
<li>Can contain only Chinese characters, letters, digits, hyphens (-), and underscores (_).</li>
        :type InstanceName: str
        :param InstanceChargeType: The instance billing mode. Valid values:
<li>`POSTPAID_BY_HOUR`: The postpaid mode by hour.</li>
        :type InstanceChargeType: str
        :param LoginSettings: The instance login setting. This parameter allows you to set a login password or key for your purchased node.
<li>If a key is set, the password will be used for login to the native component WebUI only.</li>
<li>If no key is set, the password will be used for login to all purchased nodes and the native component WebUI.</li>
        :type LoginSettings: :class:`tencentcloud.emr.v20190103.models.LoginSettings`
        :param SceneSoftwareConfig: The configuration of cluster application scenario and supported components.
        :type SceneSoftwareConfig: :class:`tencentcloud.emr.v20190103.models.SceneSoftwareConfig`
        :param InstanceChargePrepaid: The details of the monthly subscription, including the instance period and auto-renewal. It is required if `InstanceChargeType` is `PREPAID`.
        :type InstanceChargePrepaid: :class:`tencentcloud.emr.v20190103.models.InstanceChargePrepaid`
        :param SecurityGroupIds: The ID of the security group to which the instance belongs, in the format of `sg-xxxxxxxx`. You can call the [DescribeSecurityGroups](https://intl.cloud.tencent.com/document/api/215/15808?from_cn_redirect=1) API and obtain this parameter from the `SecurityGroupId` field in the response.
        :type SecurityGroupIds: list of str
        :param ScriptBootstrapActionConfig: The [Bootstrap action](https://intl.cloud.tencent.com/document/product/589/35656?from_cn_redirect=1) script settings.
        :type ScriptBootstrapActionConfig: list of ScriptBootstrapActionConfig
        :param ClientToken: A unique random token, which is valid for 5 minutes and needs to be specified by the caller to prevent the client from repeatedly creating resources. An example value is `a9a90aa6-751a-41b6-aad6-fae360632808`.
        :type ClientToken: str
        :param NeedMasterWan: Whether to enable public IP access for master nodes. Valid values:
<li>`NEED_MASTER_WAN`: Enable public IP for master nodes.</li>
<li>`NOT_NEED_MASTER_WAN`: Disable.</li>The public IP is enabled for master nodes by default.
        :type NeedMasterWan: str
        :param EnableRemoteLoginFlag: Whether to enable remote login over the public network. It is invalid if `SecurityGroupId` is passed in. It is disabled by default. Valid values:
<li>`true`: Enable</li>
<li>`false`: Disable</li>
        :type EnableRemoteLoginFlag: bool
        :param EnableKerberosFlag: Whether to enable Kerberos authentication. Valid values:
<li>`true`: Enable</li>
<li>`false` (default): Disable</li>
        :type EnableKerberosFlag: bool
        :param CustomConf: [Custom software configuration](https://intl.cloud.tencent.com/document/product/589/35655?from_cn_redirect=1?from_cn_redirect=1)
        :type CustomConf: str
        :param Tags: The tag description list. This parameter is used to bind a tag to a resource instance.
        :type Tags: list of Tag
        :param DisasterRecoverGroupIds: The list of spread placement group IDs. Only one can be specified.
You can call the [DescribeDisasterRecoverGroups](https://intl.cloud.tencent.com/document/product/213/17810?from_cn_redirect=1) API and obtain this parameter from the `DisasterRecoverGroupId` field in the response.
        :type DisasterRecoverGroupIds: list of str
        :param EnableCbsEncryptFlag: Whether to enable the cluster-level CBS encryption. Valid values:
<li>`true`: Enable</li>
<li>`false` (default): Disable</li>
        :type EnableCbsEncryptFlag: bool
        :param MetaDBInfo: The metadatabase information. If `MetaType` is `EMR_NEW_META`, `MetaDataJdbcUrl`, `MetaDataUser`, `MetaDataPass`, and `UnifyMetaInstanceId` are not required.
If `MetaType` is `EMR_EXIT_META`, `UnifyMetaInstanceId` is required.
If `MetaType` is `USER_CUSTOM_META`, `MetaDataJdbcUrl`, `MetaDataUser`, and `MetaDataPass` are required.
        :type MetaDBInfo: :class:`tencentcloud.emr.v20190103.models.CustomMetaDBInfo`
        :param DependService: The shared component information.
        :type DependService: list of DependService
        :param ZoneResourceConfiguration: The node resource specs. A spec is specified for each AZ, with the first spec for the primary AZ, the second for the backup AZ, and the third for the arbitrator AZ. If the multi-AZ mode is not enabled, only one spec is required.
        :type ZoneResourceConfiguration: list of ZoneResourceConfiguration
        """
        self.ProductVersion = None
        self.EnableSupportHAFlag = None
        self.InstanceName = None
        self.InstanceChargeType = None
        self.LoginSettings = None
        self.SceneSoftwareConfig = None
        self.InstanceChargePrepaid = None
        self.SecurityGroupIds = None
        self.ScriptBootstrapActionConfig = None
        self.ClientToken = None
        self.NeedMasterWan = None
        self.EnableRemoteLoginFlag = None
        self.EnableKerberosFlag = None
        self.CustomConf = None
        self.Tags = None
        self.DisasterRecoverGroupIds = None
        self.EnableCbsEncryptFlag = None
        self.MetaDBInfo = None
        self.DependService = None
        self.ZoneResourceConfiguration = None


    def _deserialize(self, params):
        self.ProductVersion = params.get("ProductVersion")
        self.EnableSupportHAFlag = params.get("EnableSupportHAFlag")
        self.InstanceName = params.get("InstanceName")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        if params.get("SceneSoftwareConfig") is not None:
            self.SceneSoftwareConfig = SceneSoftwareConfig()
            self.SceneSoftwareConfig._deserialize(params.get("SceneSoftwareConfig"))
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("ScriptBootstrapActionConfig") is not None:
            self.ScriptBootstrapActionConfig = []
            for item in params.get("ScriptBootstrapActionConfig"):
                obj = ScriptBootstrapActionConfig()
                obj._deserialize(item)
                self.ScriptBootstrapActionConfig.append(obj)
        self.ClientToken = params.get("ClientToken")
        self.NeedMasterWan = params.get("NeedMasterWan")
        self.EnableRemoteLoginFlag = params.get("EnableRemoteLoginFlag")
        self.EnableKerberosFlag = params.get("EnableKerberosFlag")
        self.CustomConf = params.get("CustomConf")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")
        self.EnableCbsEncryptFlag = params.get("EnableCbsEncryptFlag")
        if params.get("MetaDBInfo") is not None:
            self.MetaDBInfo = CustomMetaDBInfo()
            self.MetaDBInfo._deserialize(params.get("MetaDBInfo"))
        if params.get("DependService") is not None:
            self.DependService = []
            for item in params.get("DependService"):
                obj = DependService()
                obj._deserialize(item)
                self.DependService.append(obj)
        if params.get("ZoneResourceConfiguration") is not None:
            self.ZoneResourceConfiguration = []
            for item in params.get("ZoneResourceConfiguration"):
                obj = ZoneResourceConfiguration()
                obj._deserialize(item)
                self.ZoneResourceConfiguration.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClusterResponse(AbstractModel):
    """CreateCluster response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: The instance ID.
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class CreateInstanceRequest(AbstractModel):
    """CreateInstance request structure.

    """

    def __init__(self):
        r"""
        :param ProductId: The product ID. Different product IDs represent different EMR product versions. Valid values:
<li>16: EMR v2.3.0</li>
<li>20: EMR v2.5.0</li>
<li>25: EMR v3.1.0</li>
<li>27: Kafka v1.0.0</li>
<li>30: EMR v2.6.0</li>
<li>33: EMR v3.2.1</li>
<li>34: EMR v3.3.0</li>
<li>36: StarRocks v1.0.0</li>
<li>37: EMR v3.4.0</li>
<li>38: EMR v2.7.0</li>
<li>39: StarRocks v1.1.0</li>
<li>41: Druid v1.1.0</li>
        :type ProductId: int
        :param Software: List of deployed components. The list of component options varies by EMR product ID (i.e., `ProductId`; for specific meanings, please see the `ProductId` input parameter). For more information, please see [Component Version](https://intl.cloud.tencent.com/document/product/589/20279?from_cn_redirect=1).
Enter an instance value: `hive` or `flink`.
        :type Software: list of str
        :param SupportHA: Whether to enable high node availability. Valid values:
<li>0: does not enable high availability of node.</li>
<li>1: enables high availability of node.</li>
        :type SupportHA: int
        :param InstanceName: Instance name.
<li>Length limit: 6-36 characters.</li>
<li>Only letters, numbers, dashes (-), and underscores (_) are supported.</li>
        :type InstanceName: str
        :param PayMode: Instance billing mode. Valid values:
<li>0: pay-as-you-go.</li>
        :type PayMode: int
        :param TimeSpan: Purchase duration of instance, which needs to be used together with `TimeUnit`.
<li>When `TimeUnit` is `s`, this parameter can only be filled with 3600, indicating a pay-as-you-go instance.</li>
<li>When `TimeUnit` is `m`, the number entered in this parameter indicates the purchase duration of the monthly-subscription instance; for example, 1 means one month</li>
        :type TimeSpan: int
        :param TimeUnit: Time unit of instance purchase duration. Valid values:
<li>s: seconds. When `PayMode` is 0, `TimeUnit` can only be `s`.</li>
<li>m: month. When `PayMode` is 1, `TimeUnit` can only be `m`.</li>
        :type TimeUnit: str
        :param LoginSettings: Instance login settings. This parameter allows you to set the login password or key for your purchased node.
<li>If the key is set, the password will be only used for login to the native component WebUI.</li>
<li>If the key is not set, the password will be used for login to all purchased nodes and the native component WebUI.</li>
        :type LoginSettings: :class:`tencentcloud.emr.v20190103.models.LoginSettings`
        :param VPCSettings: Configuration information of VPC. This parameter is used to specify the VPC ID, subnet ID, etc.
        :type VPCSettings: :class:`tencentcloud.emr.v20190103.models.VPCSettings`
        :param ResourceSpec: Node resource specification.
        :type ResourceSpec: :class:`tencentcloud.emr.v20190103.models.NewResourceSpec`
        :param COSSettings: Parameter required for enabling COS access.
        :type COSSettings: :class:`tencentcloud.emr.v20190103.models.COSSettings`
        :param Placement: Instance location. This parameter is used to specify the AZ, project, and other attributes of the instance.
        :type Placement: :class:`tencentcloud.emr.v20190103.models.Placement`
        :param SgId: Security group to which an instance belongs in the format of `sg-xxxxxxxx`. This parameter can be obtained from the `SecurityGroupId` field in the return value of the [DescribeSecurityGroups](https://intl.cloud.tencent.com/document/api/215/15808) API.
        :type SgId: str
        :param PreExecutedFileSettings: [Bootstrap action](https://intl.cloud.tencent.com/document/product/589/35656?from_cn_redirect=1) script settings
        :type PreExecutedFileSettings: list of PreExecuteFileSettings
        :param AutoRenew: Whether auto-renewal is enabled. Valid values:
<li>0: auto-renewal not enabled.</li>
<li>1: auto-renewal enabled.</li>
        :type AutoRenew: int
        :param ClientToken: Client token.
        :type ClientToken: str
        :param NeedMasterWan: Whether to enable public IP access for master node. Valid values:
<li>NEED_MASTER_WAN: enables public IP for master node.</li>
<li>NOT_NEED_MASTER_WAN: does not enable.</li>Public IP is enabled for master node by default.
        :type NeedMasterWan: str
        :param RemoteLoginAtCreate: Whether to enable remote public network login, i.e., port 22. When `SgId` is not empty, this parameter does not take effect.
        :type RemoteLoginAtCreate: int
        :param CheckSecurity: Whether to enable secure cluster. 0: no; other values: yes.
        :type CheckSecurity: int
        :param ExtendFsField: Accesses to external file system.
        :type ExtendFsField: str
        :param Tags: Tag description list. This parameter is used to bind a tag to a resource instance.
        :type Tags: list of Tag
        :param DisasterRecoverGroupIds: List of spread placement group IDs. Only one can be specified currently.
This parameter can be obtained in the `SecurityGroupId` field in the return value of the [DescribeSecurityGroups](https://intl.cloud.tencent.com/document/product/213/15486?from_cn_redirect=1) API.
        :type DisasterRecoverGroupIds: list of str
        :param CbsEncrypt: CBS disk encryption at the cluster level. 0: not encrypted, 1: encrypted
        :type CbsEncrypt: int
        :param MetaType: Hive-shared metadatabase type. Valid values:
<li>EMR_DEFAULT_META: the cluster creates one by default.</li>
<li>EMR_EXIST_META: the cluster uses the specified EMR-MetaDB instance.</li>
<li>USER_CUSTOM_META: the cluster uses a custom MetaDB instance.</li>
        :type MetaType: str
        :param UnifyMetaInstanceId: EMR-MetaDB instance
        :type UnifyMetaInstanceId: str
        :param MetaDBInfo: Custom MetaDB instance information
        :type MetaDBInfo: :class:`tencentcloud.emr.v20190103.models.CustomMetaInfo`
        :param ApplicationRole: Custom application role.
        :type ApplicationRole: str
        :param SceneName: Scenario-based values:
Hadoop-Kudu
Hadoop-Zookeeper
Hadoop-Presto
Hadoop-Hbase
        :type SceneName: str
        :param ExternalService: Shared component information
        :type ExternalService: list of ExternalService
        :param VersionID: 
        :type VersionID: int
        :param MultiZone: `true` indicates that the multi-AZ deployment mode is enabled. This parameter is available only in cluster creation and cannot be changed after setting.
        :type MultiZone: bool
        :param MultiZoneSettings: Node resource specs. The actual number of AZs is set, with the first AZ as the primary AZ, the second as the backup AZ, and the third as the arbitrator AZ. If the multi-AZ mode is not enabled, set the value to `1`.
        :type MultiZoneSettings: list of MultiZoneSetting
        """
        self.ProductId = None
        self.Software = None
        self.SupportHA = None
        self.InstanceName = None
        self.PayMode = None
        self.TimeSpan = None
        self.TimeUnit = None
        self.LoginSettings = None
        self.VPCSettings = None
        self.ResourceSpec = None
        self.COSSettings = None
        self.Placement = None
        self.SgId = None
        self.PreExecutedFileSettings = None
        self.AutoRenew = None
        self.ClientToken = None
        self.NeedMasterWan = None
        self.RemoteLoginAtCreate = None
        self.CheckSecurity = None
        self.ExtendFsField = None
        self.Tags = None
        self.DisasterRecoverGroupIds = None
        self.CbsEncrypt = None
        self.MetaType = None
        self.UnifyMetaInstanceId = None
        self.MetaDBInfo = None
        self.ApplicationRole = None
        self.SceneName = None
        self.ExternalService = None
        self.VersionID = None
        self.MultiZone = None
        self.MultiZoneSettings = None


    def _deserialize(self, params):
        self.ProductId = params.get("ProductId")
        self.Software = params.get("Software")
        self.SupportHA = params.get("SupportHA")
        self.InstanceName = params.get("InstanceName")
        self.PayMode = params.get("PayMode")
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        if params.get("VPCSettings") is not None:
            self.VPCSettings = VPCSettings()
            self.VPCSettings._deserialize(params.get("VPCSettings"))
        if params.get("ResourceSpec") is not None:
            self.ResourceSpec = NewResourceSpec()
            self.ResourceSpec._deserialize(params.get("ResourceSpec"))
        if params.get("COSSettings") is not None:
            self.COSSettings = COSSettings()
            self.COSSettings._deserialize(params.get("COSSettings"))
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.SgId = params.get("SgId")
        if params.get("PreExecutedFileSettings") is not None:
            self.PreExecutedFileSettings = []
            for item in params.get("PreExecutedFileSettings"):
                obj = PreExecuteFileSettings()
                obj._deserialize(item)
                self.PreExecutedFileSettings.append(obj)
        self.AutoRenew = params.get("AutoRenew")
        self.ClientToken = params.get("ClientToken")
        self.NeedMasterWan = params.get("NeedMasterWan")
        self.RemoteLoginAtCreate = params.get("RemoteLoginAtCreate")
        self.CheckSecurity = params.get("CheckSecurity")
        self.ExtendFsField = params.get("ExtendFsField")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")
        self.CbsEncrypt = params.get("CbsEncrypt")
        self.MetaType = params.get("MetaType")
        self.UnifyMetaInstanceId = params.get("UnifyMetaInstanceId")
        if params.get("MetaDBInfo") is not None:
            self.MetaDBInfo = CustomMetaInfo()
            self.MetaDBInfo._deserialize(params.get("MetaDBInfo"))
        self.ApplicationRole = params.get("ApplicationRole")
        self.SceneName = params.get("SceneName")
        if params.get("ExternalService") is not None:
            self.ExternalService = []
            for item in params.get("ExternalService"):
                obj = ExternalService()
                obj._deserialize(item)
                self.ExternalService.append(obj)
        self.VersionID = params.get("VersionID")
        self.MultiZone = params.get("MultiZone")
        if params.get("MultiZoneSettings") is not None:
            self.MultiZoneSettings = []
            for item in params.get("MultiZoneSettings"):
                obj = MultiZoneSetting()
                obj._deserialize(item)
                self.MultiZoneSettings.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateInstanceResponse(AbstractModel):
    """CreateInstance response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type InstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class CustomMetaDBInfo(AbstractModel):
    """The user-created Hive-MetaDB instance information.

    """

    def __init__(self):
        r"""
        :param MetaDataJdbcUrl: The JDBC URL of the custom metadatabase instance. Example: jdbc:mysql://10.10.10.10:3306/dbname
        :type MetaDataJdbcUrl: str
        :param MetaDataUser: The custom metadatabase instance username.
        :type MetaDataUser: str
        :param MetaDataPass: The custom metadatabase instance password.
        :type MetaDataPass: str
        :param MetaType: The Hive-shared metadatabase type. Valid values:
<li>`EMR_DEFAULT_META`: The cluster creates one by default.</li>
<li>`EMR_EXIST_META`: The cluster uses the specified EMR metadatabase instance.</li>
<li>`USER_CUSTOM_META`: The cluster uses a custom metadatabase instance.</li>
        :type MetaType: str
        :param UnifyMetaInstanceId: The EMR-MetaDB instance.
        :type UnifyMetaInstanceId: str
        """
        self.MetaDataJdbcUrl = None
        self.MetaDataUser = None
        self.MetaDataPass = None
        self.MetaType = None
        self.UnifyMetaInstanceId = None


    def _deserialize(self, params):
        self.MetaDataJdbcUrl = params.get("MetaDataJdbcUrl")
        self.MetaDataUser = params.get("MetaDataUser")
        self.MetaDataPass = params.get("MetaDataPass")
        self.MetaType = params.get("MetaType")
        self.UnifyMetaInstanceId = params.get("UnifyMetaInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CustomMetaInfo(AbstractModel):
    """User-created Hive-MetaDB instance information

    """

    def __init__(self):
        r"""
        :param MetaDataJdbcUrl: JDBC connection to custom MetaDB instance beginning with `jdbc:mysql://`
        :type MetaDataJdbcUrl: str
        :param MetaDataUser: Custom MetaDB instance username
        :type MetaDataUser: str
        :param MetaDataPass: Custom MetaDB instance password
        :type MetaDataPass: str
        """
        self.MetaDataJdbcUrl = None
        self.MetaDataUser = None
        self.MetaDataPass = None


    def _deserialize(self, params):
        self.MetaDataJdbcUrl = params.get("MetaDataJdbcUrl")
        self.MetaDataUser = params.get("MetaDataUser")
        self.MetaDataPass = params.get("MetaDataPass")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CustomServiceDefine(AbstractModel):
    """Shared self-built component parameters

    """

    def __init__(self):
        r"""
        :param Name: Custom parameter key
        :type Name: str
        :param Value: Custom parameter value
        :type Value: str
        """
        self.Name = None
        self.Value = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DependService(AbstractModel):
    """Shared component information

    """

    def __init__(self):
        r"""
        :param ServiceName: The shared component name.
        :type ServiceName: str
        :param InstanceId: The cluster to which the shared component belongs.
        :type InstanceId: str
        """
        self.ServiceName = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.ServiceName = params.get("ServiceName")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterNodesRequest(AbstractModel):
    """DescribeClusterNodes request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Cluster instance ID in the format of emr-xxxxxxxx
        :type InstanceId: str
        :param NodeFlag: Node flag. Valid values:
<li>all: gets the information of nodes in all types except TencentDB information.</li>
<li>master: gets master node information.</li>
<li>core: gets core node information.</li>
<li>task: gets task node information.</li>
<li>common: gets common node information.</li>
<li>router: gets router node information.</li>
<li>db: gets TencentDB information in normal status.</li>
Note: only the above values are supported for the time being. Entering other values will cause errors.
        :type NodeFlag: str
        :param Offset: Page number. Default value: 0, indicating the first page.
        :type Offset: int
        :param Limit: Number of returned results per page. Default value: 100. Maximum value: 100
        :type Limit: int
        :param HardwareResourceType: Resource type. Valid values: all, host, pod. Default value: all
        :type HardwareResourceType: str
        :param SearchFields: Searchable field
        :type SearchFields: list of SearchItem
        :param OrderField: None
        :type OrderField: str
        :param Asc: None
        :type Asc: int
        """
        self.InstanceId = None
        self.NodeFlag = None
        self.Offset = None
        self.Limit = None
        self.HardwareResourceType = None
        self.SearchFields = None
        self.OrderField = None
        self.Asc = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.NodeFlag = params.get("NodeFlag")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.HardwareResourceType = params.get("HardwareResourceType")
        if params.get("SearchFields") is not None:
            self.SearchFields = []
            for item in params.get("SearchFields"):
                obj = SearchItem()
                obj._deserialize(item)
                self.SearchFields.append(obj)
        self.OrderField = params.get("OrderField")
        self.Asc = params.get("Asc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterNodesResponse(AbstractModel):
    """DescribeClusterNodes response structure.

    """

    def __init__(self):
        r"""
        :param TotalCnt: Total number of queried nodes
        :type TotalCnt: int
        :param NodeList: List of node details
Note: this field may return null, indicating that no valid values can be obtained.
        :type NodeList: list of NodeHardwareInfo
        :param TagKeys: List of tag keys owned by user
Note: this field may return null, indicating that no valid values can be obtained.
        :type TagKeys: list of str
        :param HardwareResourceTypeList: Resource type list
Note: this field may return null, indicating that no valid values can be obtained.
        :type HardwareResourceTypeList: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCnt = None
        self.NodeList = None
        self.TagKeys = None
        self.HardwareResourceTypeList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCnt = params.get("TotalCnt")
        if params.get("NodeList") is not None:
            self.NodeList = []
            for item in params.get("NodeList"):
                obj = NodeHardwareInfo()
                obj._deserialize(item)
                self.NodeList.append(obj)
        self.TagKeys = params.get("TagKeys")
        self.HardwareResourceTypeList = params.get("HardwareResourceTypeList")
        self.RequestId = params.get("RequestId")


class DescribeEmrApplicationStaticsRequest(AbstractModel):
    """DescribeEmrApplicationStatics request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Cluster ID
        :type InstanceId: str
        :param StartTime: Start time in the format of timestamp. Unit: seconds.
        :type StartTime: int
        :param EndTime: End time in the format of timestamp. Unit: seconds.
        :type EndTime: int
        :param Queues: Queue name used for filtering
        :type Queues: list of str
        :param Users: Username used for filtering
        :type Users: list of str
        :param ApplicationTypes: Application type used for filtering
        :type ApplicationTypes: list of str
        :param GroupBy: Group field. Valid values: `queue`, `user`, and `applicationType`.
        :type GroupBy: list of str
        :param OrderBy: Sorting field. Valid values: `sumMemorySeconds`, `sumVCoreSeconds`, `sumHDFSBytesWritten`, and `sumHDFSBytesRead`.
        :type OrderBy: str
        :param IsAsc: Order type. Valid values: `0` (descending) and `1`(ascending).
        :type IsAsc: int
        :param Offset: Page number
        :type Offset: int
        :param Limit: Page limit
        :type Limit: int
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Queues = None
        self.Users = None
        self.ApplicationTypes = None
        self.GroupBy = None
        self.OrderBy = None
        self.IsAsc = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Queues = params.get("Queues")
        self.Users = params.get("Users")
        self.ApplicationTypes = params.get("ApplicationTypes")
        self.GroupBy = params.get("GroupBy")
        self.OrderBy = params.get("OrderBy")
        self.IsAsc = params.get("IsAsc")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEmrApplicationStaticsResponse(AbstractModel):
    """DescribeEmrApplicationStatics response structure.

    """

    def __init__(self):
        r"""
        :param Statics: Application statistics
        :type Statics: list of ApplicationStatics
        :param TotalCount: Total count
        :type TotalCount: int
        :param Queues: Available queue name
        :type Queues: list of str
        :param Users: Available usernames
        :type Users: list of str
        :param ApplicationTypes: Available application type
        :type ApplicationTypes: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Statics = None
        self.TotalCount = None
        self.Queues = None
        self.Users = None
        self.ApplicationTypes = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Statics") is not None:
            self.Statics = []
            for item in params.get("Statics"):
                obj = ApplicationStatics()
                obj._deserialize(item)
                self.Statics.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.Queues = params.get("Queues")
        self.Users = params.get("Users")
        self.ApplicationTypes = params.get("ApplicationTypes")
        self.RequestId = params.get("RequestId")


class DescribeInstancesListRequest(AbstractModel):
    """DescribeInstancesList request structure.

    """

    def __init__(self):
        r"""
        :param DisplayStrategy: Cluster filtering policy. Valid values: <li>clusterList: Queries the list of clusters excluding terminated ones.</li><li>monitorManage: Queries the list of clusters excluding those terminated, under creation and not successfully created.</li><li>cloudHardwareManage/componentManage: Two reserved values, which have the same implications as those of `monitorManage`.</li>
        :type DisplayStrategy: str
        :param Offset: Page number. Default value: `0`, indicating the first page.
        :type Offset: int
        :param Limit: Number of returned results per page. Default value: `10`; maximum value: `100`.
        :type Limit: int
        :param OrderField: Sorting field. Valid values: <li>clusterId: Sorting by instance ID. </li><li>addTime: Sorting by instance creation time.</li><li>status: Sorting by instance status code.</li>
        :type OrderField: str
        :param Asc: Sort ascending or descending based on `OrderField`. Valid values:<li>0: Descending.</li><li>1: Ascending.</li>Default value: `0`.
        :type Asc: int
        :param Filters: Custom query
        :type Filters: list of Filters
        """
        self.DisplayStrategy = None
        self.Offset = None
        self.Limit = None
        self.OrderField = None
        self.Asc = None
        self.Filters = None


    def _deserialize(self, params):
        self.DisplayStrategy = params.get("DisplayStrategy")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderField = params.get("OrderField")
        self.Asc = params.get("Asc")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filters()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstancesListResponse(AbstractModel):
    """DescribeInstancesList response structure.

    """

    def __init__(self):
        r"""
        :param TotalCnt: Number of eligible instances.
        :type TotalCnt: int
        :param InstancesList: Cluster instance list.
        :type InstancesList: list of EmrListInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCnt = None
        self.InstancesList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCnt = params.get("TotalCnt")
        if params.get("InstancesList") is not None:
            self.InstancesList = []
            for item in params.get("InstancesList"):
                obj = EmrListInstance()
                obj._deserialize(item)
                self.InstancesList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesRequest(AbstractModel):
    """DescribeInstances request structure.

    """

    def __init__(self):
        r"""
        :param DisplayStrategy: Cluster filtering policy. Valid values:
<li>clusterList: queries the list of clusters except terminated ones.</li>
<li>monitorManage: queries the list of clusters except those that have been terminated, are being created, or failed to be created.</li>
<li>cloudHardwareManage/componentManage: reserved fields with the same meaning as `monitorManage`.</li>
        :type DisplayStrategy: str
        :param InstanceIds: Queries by one or more instance IDs in the format of `emr-xxxxxxxx`. For the format of this parameter, please see the `id.N` section in [API Overview](https://intl.cloud.tencent.com/document/api/213/15688). If no instance ID is entered, the list of all instances under this `APPID` will be returned.
        :type InstanceIds: list of str
        :param Offset: Page number. Default value: 0, indicating the first page.
        :type Offset: int
        :param Limit: Number of returned results per page. Default value: 10. Maximum value: 100
        :type Limit: int
        :param ProjectId: ID of the project to which the instance belongs. This parameter can be obtained from the `projectId` field in the return value of the `DescribeProject` API. If this value is -1, the list of all instances will be returned.
        :type ProjectId: int
        :param OrderField: Sorting field. Valid values:
<li>clusterId: sorts by cluster ID.</li>
<li>addTime: sorts by instance creation time.</li>
<li>status: sorts by instance status code.</li>
        :type OrderField: str
        :param Asc: Sorts according to `OrderField` in ascending or descending order. Valid values:
<li>0: descending order.</li>
<li>1: ascending order.</li>Default value: 0.
        :type Asc: int
        """
        self.DisplayStrategy = None
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None
        self.ProjectId = None
        self.OrderField = None
        self.Asc = None


    def _deserialize(self, params):
        self.DisplayStrategy = params.get("DisplayStrategy")
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.ProjectId = params.get("ProjectId")
        self.OrderField = params.get("OrderField")
        self.Asc = params.get("Asc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstancesResponse(AbstractModel):
    """DescribeInstances response structure.

    """

    def __init__(self):
        r"""
        :param TotalCnt: Number of eligible instances.
        :type TotalCnt: int
        :param ClusterList: List of EMR instance details.
Note: this field may return null, indicating that no valid values can be obtained.
        :type ClusterList: list of ClusterInstancesInfo
        :param TagKeys: List of tag keys associated to an instance.
Note: this field may return null, indicating that no valid values can be obtained.
        :type TagKeys: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCnt = None
        self.ClusterList = None
        self.TagKeys = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCnt = params.get("TotalCnt")
        if params.get("ClusterList") is not None:
            self.ClusterList = []
            for item in params.get("ClusterList"):
                obj = ClusterInstancesInfo()
                obj._deserialize(item)
                self.ClusterList.append(obj)
        self.TagKeys = params.get("TagKeys")
        self.RequestId = params.get("RequestId")


class DescribeResourceScheduleRequest(AbstractModel):
    """DescribeResourceSchedule request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: EMR cluster ID
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
        


class DescribeResourceScheduleResponse(AbstractModel):
    """DescribeResourceSchedule response structure.

    """

    def __init__(self):
        r"""
        :param OpenSwitch: Whether to enable the resource scheduling feature
        :type OpenSwitch: bool
        :param Scheduler: The resource scheduler in service
        :type Scheduler: str
        :param FSInfo: Fair Scheduler information
        :type FSInfo: str
        :param CSInfo: Capacity Scheduler information
        :type CSInfo: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OpenSwitch = None
        self.Scheduler = None
        self.FSInfo = None
        self.CSInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OpenSwitch = params.get("OpenSwitch")
        self.Scheduler = params.get("Scheduler")
        self.FSInfo = params.get("FSInfo")
        self.CSInfo = params.get("CSInfo")
        self.RequestId = params.get("RequestId")


class DescribeUsersForUserManagerRequest(AbstractModel):
    """DescribeUsersForUserManager request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Cluster instance ID
        :type InstanceId: str
        :param PageNo: Page number
        :type PageNo: int
        :param PageSize: Page size
        :type PageSize: int
        :param UserManagerFilter: User list query filter
        :type UserManagerFilter: :class:`tencentcloud.emr.v20190103.models.UserManagerFilter`
        :param NeedKeytabInfo: Whether the Keytab file information is required. This field is only valid for clusters with Kerberos enabled and defaults to `false`.
        :type NeedKeytabInfo: bool
        """
        self.InstanceId = None
        self.PageNo = None
        self.PageSize = None
        self.UserManagerFilter = None
        self.NeedKeytabInfo = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.PageNo = params.get("PageNo")
        self.PageSize = params.get("PageSize")
        if params.get("UserManagerFilter") is not None:
            self.UserManagerFilter = UserManagerFilter()
            self.UserManagerFilter._deserialize(params.get("UserManagerFilter"))
        self.NeedKeytabInfo = params.get("NeedKeytabInfo")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUsersForUserManagerResponse(AbstractModel):
    """DescribeUsersForUserManager response structure.

    """

    def __init__(self):
        r"""
        :param TotalCnt: Total number
        :type TotalCnt: int
        :param UserManagerUserList: User information list
Note: This field may return null, indicating that no valid value can be obtained.
        :type UserManagerUserList: list of UserManagerUserBriefInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCnt = None
        self.UserManagerUserList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCnt = params.get("TotalCnt")
        if params.get("UserManagerUserList") is not None:
            self.UserManagerUserList = []
            for item in params.get("UserManagerUserList"):
                obj = UserManagerUserBriefInfo()
                obj._deserialize(item)
                self.UserManagerUserList.append(obj)
        self.RequestId = params.get("RequestId")


class DiskSpecInfo(AbstractModel):
    """Node disk information

    """

    def __init__(self):
        r"""
        :param Count: The number of disks.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Count: int
        :param DiskType: The system disk type. Valid values:
<li>`CLOUD_SSD`: Cloud SSD</li>
<li>`CLOUD_PREMIUM`: Premium cloud disk</li>
<li>`CLOUD_BASIC`: Cloud HDD</li>
<li>`LOCAL_BASIC`: Local disk</li>
<li>`LOCAL_SSD`: Local SSD</li>

The data disk type. Valid values:
<li>`CLOUD_SSD`: Cloud SSD</li>
<li>`CLOUD_PREMIUM`: Premium cloud disk</li>
<li>`CLOUD_BASIC`: Cloud HDD</li>
<li>`LOCAL_BASIC`: Local disk</li>
<li>`LOCAL_SSD`: Local SSD</li>
<li>`CLOUD_HSSD`: Enhanced SSD</li>
<li>`CLOUD_THROUGHPUT`: Throughput HDD</li>
<li>CLOUD_TSSD: ulTra SSD</li>
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskType: str
        :param DiskSize: The disk capacity in GB.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskSize: int
        """
        self.Count = None
        self.DiskType = None
        self.DiskSize = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.DiskType = params.get("DiskType")
        self.DiskSize = params.get("DiskSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DynamicPodSpec(AbstractModel):
    """Pod floating specification

    """

    def __init__(self):
        r"""
        :param RequestCpu: Minimum number of CPUs
        :type RequestCpu: float
        :param LimitCpu: Maximum number of CPUs
        :type LimitCpu: float
        :param RequestMemory: Minimum memory in MB
        :type RequestMemory: float
        :param LimitMemory: Maximum memory in MB
        :type LimitMemory: float
        """
        self.RequestCpu = None
        self.LimitCpu = None
        self.RequestMemory = None
        self.LimitMemory = None


    def _deserialize(self, params):
        self.RequestCpu = params.get("RequestCpu")
        self.LimitCpu = params.get("LimitCpu")
        self.RequestMemory = params.get("RequestMemory")
        self.LimitMemory = params.get("LimitMemory")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EmrListInstance(AbstractModel):
    """Returned cluster list sample

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param StatusDesc: Status description
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type StatusDesc: str
        :param ClusterName: Cluster name
        :type ClusterName: str
        :param ZoneId: Cluster region
        :type ZoneId: int
        :param AppId: User APPID
        :type AppId: int
        :param AddTime: Creation time
        :type AddTime: str
        :param RunTime: Running time
        :type RunTime: str
        :param MasterIp: Cluster IP
        :type MasterIp: str
        :param EmrVersion: Cluster version
        :type EmrVersion: str
        :param ChargeType: Cluster billing mode
        :type ChargeType: int
        :param Id: EMR ID
        :type Id: int
        :param ProductId: Product ID
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ProductId: int
        :param ProjectId: Project ID
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ProjectId: int
        :param RegionId: Region
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type RegionId: int
        :param SubnetId: Subnet ID
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type SubnetId: int
        :param VpcId: VPC ID
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type VpcId: int
        :param Zone: Region
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type Zone: str
        :param Status: Status code
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type Status: int
        :param Tags: Instance tag
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type Tags: list of Tag
        :param AlarmInfo: Alarm information
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type AlarmInfo: str
        :param IsWoodpeckerCluster: Whether it is a Woodpecker cluster
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type IsWoodpeckerCluster: int
        :param VpcName: VPC name
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type VpcName: str
        :param SubnetName: Subnet name
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type SubnetName: str
        :param UniqVpcId: VPC ID string
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type UniqVpcId: str
        :param UniqSubnetId: Subnet ID string
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type UniqSubnetId: str
        :param ClusterClass: Cluster type
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ClusterClass: str
        :param IsMultiZoneCluster: Whether it is a multi-AZ cluster
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type IsMultiZoneCluster: bool
        :param IsHandsCluster: Whether it is a manually deployed cluster
Note: This field may return null, indicating that no valid value can be obtained. 
        :type IsHandsCluster: bool
        :param OutSideSoftInfo: Client component information.
Note: This field may return null, indicating that no valid values can be obtained.
        :type OutSideSoftInfo: list of SoftDependInfo
        :param IsSupportOutsideCluster: Whether the current cluster supports external clients.
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsSupportOutsideCluster: bool
        """
        self.ClusterId = None
        self.StatusDesc = None
        self.ClusterName = None
        self.ZoneId = None
        self.AppId = None
        self.AddTime = None
        self.RunTime = None
        self.MasterIp = None
        self.EmrVersion = None
        self.ChargeType = None
        self.Id = None
        self.ProductId = None
        self.ProjectId = None
        self.RegionId = None
        self.SubnetId = None
        self.VpcId = None
        self.Zone = None
        self.Status = None
        self.Tags = None
        self.AlarmInfo = None
        self.IsWoodpeckerCluster = None
        self.VpcName = None
        self.SubnetName = None
        self.UniqVpcId = None
        self.UniqSubnetId = None
        self.ClusterClass = None
        self.IsMultiZoneCluster = None
        self.IsHandsCluster = None
        self.OutSideSoftInfo = None
        self.IsSupportOutsideCluster = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.StatusDesc = params.get("StatusDesc")
        self.ClusterName = params.get("ClusterName")
        self.ZoneId = params.get("ZoneId")
        self.AppId = params.get("AppId")
        self.AddTime = params.get("AddTime")
        self.RunTime = params.get("RunTime")
        self.MasterIp = params.get("MasterIp")
        self.EmrVersion = params.get("EmrVersion")
        self.ChargeType = params.get("ChargeType")
        self.Id = params.get("Id")
        self.ProductId = params.get("ProductId")
        self.ProjectId = params.get("ProjectId")
        self.RegionId = params.get("RegionId")
        self.SubnetId = params.get("SubnetId")
        self.VpcId = params.get("VpcId")
        self.Zone = params.get("Zone")
        self.Status = params.get("Status")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.AlarmInfo = params.get("AlarmInfo")
        self.IsWoodpeckerCluster = params.get("IsWoodpeckerCluster")
        self.VpcName = params.get("VpcName")
        self.SubnetName = params.get("SubnetName")
        self.UniqVpcId = params.get("UniqVpcId")
        self.UniqSubnetId = params.get("UniqSubnetId")
        self.ClusterClass = params.get("ClusterClass")
        self.IsMultiZoneCluster = params.get("IsMultiZoneCluster")
        self.IsHandsCluster = params.get("IsHandsCluster")
        if params.get("OutSideSoftInfo") is not None:
            self.OutSideSoftInfo = []
            for item in params.get("OutSideSoftInfo"):
                obj = SoftDependInfo()
                obj._deserialize(item)
                self.OutSideSoftInfo.append(obj)
        self.IsSupportOutsideCluster = params.get("IsSupportOutsideCluster")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EmrPrice(AbstractModel):
    """EMR inquiry description

    """

    def __init__(self):
        r"""
        :param OriginalCost: The published price.
Note: This field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: str
        :param DiscountCost: The discounted price.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiscountCost: str
        :param Unit: The unit of the billable item.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Unit: str
        :param PriceSpec: The queried spec.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PriceSpec: :class:`tencentcloud.emr.v20190103.models.PriceResource`
        :param SupportSpotPaid: Whether spot instances are supported.
Note: This field may return null, indicating that no valid values can be obtained.
        :type SupportSpotPaid: bool
        """
        self.OriginalCost = None
        self.DiscountCost = None
        self.Unit = None
        self.PriceSpec = None
        self.SupportSpotPaid = None


    def _deserialize(self, params):
        self.OriginalCost = params.get("OriginalCost")
        self.DiscountCost = params.get("DiscountCost")
        self.Unit = params.get("Unit")
        if params.get("PriceSpec") is not None:
            self.PriceSpec = PriceResource()
            self.PriceSpec._deserialize(params.get("PriceSpec"))
        self.SupportSpotPaid = params.get("SupportSpotPaid")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EmrProductConfigOutter(AbstractModel):
    """EMR product configuration

    """

    def __init__(self):
        r"""
        :param SoftInfo: Software information
Note: this field may return null, indicating that no valid values can be obtained.
        :type SoftInfo: list of str
        :param MasterNodeSize: Number of master nodes
Note: this field may return null, indicating that no valid values can be obtained.
        :type MasterNodeSize: int
        :param CoreNodeSize: Number of core nodes
Note: this field may return null, indicating that no valid values can be obtained.
        :type CoreNodeSize: int
        :param TaskNodeSize: Number of task nodes
Note: this field may return null, indicating that no valid values can be obtained.
        :type TaskNodeSize: int
        :param ComNodeSize: Number of common nodes
Note: this field may return null, indicating that no valid values can be obtained.
        :type ComNodeSize: int
        :param MasterResource: Master node resource
Note: this field may return null, indicating that no valid values can be obtained.
        :type MasterResource: :class:`tencentcloud.emr.v20190103.models.OutterResource`
        :param CoreResource: Core node resource
Note: this field may return null, indicating that no valid values can be obtained.
        :type CoreResource: :class:`tencentcloud.emr.v20190103.models.OutterResource`
        :param TaskResource: Task node resource
Note: this field may return null, indicating that no valid values can be obtained.
        :type TaskResource: :class:`tencentcloud.emr.v20190103.models.OutterResource`
        :param ComResource: Common node resource
Note: this field may return null, indicating that no valid values can be obtained.
        :type ComResource: :class:`tencentcloud.emr.v20190103.models.OutterResource`
        :param OnCos: Whether COS is used
Note: this field may return null, indicating that no valid values can be obtained.
        :type OnCos: bool
        :param ChargeType: Billing mode
Note: this field may return null, indicating that no valid values can be obtained.
        :type ChargeType: int
        :param RouterNodeSize: Number of router nodes
Note: this field may return null, indicating that no valid values can be obtained.
        :type RouterNodeSize: int
        :param SupportHA: Whether HA is supported
Note: this field may return null, indicating that no valid values can be obtained.
        :type SupportHA: bool
        :param SecurityOn: Whether secure mode is supported
Note: this field may return null, indicating that no valid values can be obtained.
        :type SecurityOn: bool
        :param SecurityGroup: Security group name
Note: this field may return null, indicating that no valid values can be obtained.
        :type SecurityGroup: str
        :param CbsEncrypt: Whether to enable CBS encryption
Note: this field may return null, indicating that no valid values can be obtained.
        :type CbsEncrypt: int
        :param ApplicationRole: Custom application role
Note: this field may return `null`, indicating that no valid value can be obtained.
        :type ApplicationRole: str
        :param SecurityGroups: Security groups
Note: this field may return `null`, indicating that no valid value can be obtained.
        :type SecurityGroups: list of str
        :param PublicKeyId: SSH key ID
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type PublicKeyId: str
        """
        self.SoftInfo = None
        self.MasterNodeSize = None
        self.CoreNodeSize = None
        self.TaskNodeSize = None
        self.ComNodeSize = None
        self.MasterResource = None
        self.CoreResource = None
        self.TaskResource = None
        self.ComResource = None
        self.OnCos = None
        self.ChargeType = None
        self.RouterNodeSize = None
        self.SupportHA = None
        self.SecurityOn = None
        self.SecurityGroup = None
        self.CbsEncrypt = None
        self.ApplicationRole = None
        self.SecurityGroups = None
        self.PublicKeyId = None


    def _deserialize(self, params):
        self.SoftInfo = params.get("SoftInfo")
        self.MasterNodeSize = params.get("MasterNodeSize")
        self.CoreNodeSize = params.get("CoreNodeSize")
        self.TaskNodeSize = params.get("TaskNodeSize")
        self.ComNodeSize = params.get("ComNodeSize")
        if params.get("MasterResource") is not None:
            self.MasterResource = OutterResource()
            self.MasterResource._deserialize(params.get("MasterResource"))
        if params.get("CoreResource") is not None:
            self.CoreResource = OutterResource()
            self.CoreResource._deserialize(params.get("CoreResource"))
        if params.get("TaskResource") is not None:
            self.TaskResource = OutterResource()
            self.TaskResource._deserialize(params.get("TaskResource"))
        if params.get("ComResource") is not None:
            self.ComResource = OutterResource()
            self.ComResource._deserialize(params.get("ComResource"))
        self.OnCos = params.get("OnCos")
        self.ChargeType = params.get("ChargeType")
        self.RouterNodeSize = params.get("RouterNodeSize")
        self.SupportHA = params.get("SupportHA")
        self.SecurityOn = params.get("SecurityOn")
        self.SecurityGroup = params.get("SecurityGroup")
        self.CbsEncrypt = params.get("CbsEncrypt")
        self.ApplicationRole = params.get("ApplicationRole")
        self.SecurityGroups = params.get("SecurityGroups")
        self.PublicKeyId = params.get("PublicKeyId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExternalService(AbstractModel):
    """Shared component information

    """

    def __init__(self):
        r"""
        :param ShareType: Shared component type, which can be EMR or CUSTOM
        :type ShareType: str
        :param CustomServiceDefineList: Custom parameters
        :type CustomServiceDefineList: list of CustomServiceDefine
        :param Service: Shared component name
        :type Service: str
        :param InstanceId: Shared component cluster
        :type InstanceId: str
        """
        self.ShareType = None
        self.CustomServiceDefineList = None
        self.Service = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.ShareType = params.get("ShareType")
        if params.get("CustomServiceDefineList") is not None:
            self.CustomServiceDefineList = []
            for item in params.get("CustomServiceDefineList"):
                obj = CustomServiceDefine()
                obj._deserialize(item)
                self.CustomServiceDefineList.append(obj)
        self.Service = params.get("Service")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Filters(AbstractModel):
    """Custom query filter of the EMR cluster instance list

    """

    def __init__(self):
        r"""
        :param Name: Field name
        :type Name: str
        :param Values: Filters by the field value
        :type Values: list of str
        """
        self.Name = None
        self.Values = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HostVolumeContext(AbstractModel):
    """Description of `HostPath` mounting method in the pod

    """

    def __init__(self):
        r"""
        :param VolumePath: The directory for mounting the host in the pod, which is the mount point of the host in the resource. A specified mount point corresponds to the host path and is used as the data storage directory in the pod.
Note: This field may return null, indicating that no valid values can be obtained.
        :type VolumePath: str
        """
        self.VolumePath = None


    def _deserialize(self, params):
        self.VolumePath = params.get("VolumePath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceCreateInstanceRequest(AbstractModel):
    """InquiryPriceCreateInstance request structure.

    """

    def __init__(self):
        r"""
        :param TimeUnit: Time unit of instance purchase duration. Valid values:
<li>s: seconds. When `PayMode` is 0, `TimeUnit` can only be `s`.</li>
        :type TimeUnit: str
        :param TimeSpan: Purchase duration of instance, which needs to be used together with `TimeUnit`.
<li>When `TimeUnit` is `s`, this parameter can only be filled with 3600, indicating a pay-as-you-go instance.</li>
<li>When `TimeUnit` is `m`, the number entered in this parameter indicates the purchase duration of the monthly-subscription instance; for example, 1 means one month</li>
        :type TimeSpan: int
        :param Currency: Currency.
        :type Currency: str
        :param PayMode: Instance billing mode. Valid values:
<li>0: pay-as-you-go.</li>
        :type PayMode: int
        :param SupportHA: Whether to enable high availability of node. Valid values:
<li>0: does not enable high availability of node.</li>
<li>1: enables high availability of node.</li>
        :type SupportHA: int
        :param Software: List of deployed components. Different required components need to be selected for different EMR product IDs (i.e., `ProductId`; for specific meanings, please see the `ProductId` field in the input parameter):
<li>When `ProductId` is 1, the required components include hadoop-2.7.3, knox-1.2.0, and zookeeper-3.4.9</li>
<li>When `ProductId` is 2, the required components include hadoop-2.7.3, knox-1.2.0, and zookeeper-3.4.9</li>
<li>When `ProductId` is 4, the required components include hadoop-2.8.4, knox-1.2.0, and zookeeper-3.4.9</li>
<li>When `ProductId` is 7, the required components include hadoop-3.1.2, knox-1.2.0, and zookeeper-3.4.9</li>
        :type Software: list of str
        :param ResourceSpec: Node specification queried for price.
        :type ResourceSpec: :class:`tencentcloud.emr.v20190103.models.NewResourceSpec`
        :param Placement: Instance location. This parameter is used to specify the AZ, project, and other attributes of the instance.
        :type Placement: :class:`tencentcloud.emr.v20190103.models.Placement`
        :param VPCSettings: Configuration information of VPC. This parameter is used to specify the VPC ID, subnet ID, etc.
        :type VPCSettings: :class:`tencentcloud.emr.v20190103.models.VPCSettings`
        :param MetaType: Hive-shared metadatabase type. Valid values:
<li>EMR_DEFAULT_META: the cluster creates one by default.</li>
<li>EMR_EXIST_META: the cluster uses the specified EMR-MetaDB instance.</li>
<li>USER_CUSTOM_META: the cluster uses a custom MetaDB instance.</li>
        :type MetaType: str
        :param UnifyMetaInstanceId: EMR-MetaDB instance
        :type UnifyMetaInstanceId: str
        :param MetaDBInfo: Custom MetaDB instance information
        :type MetaDBInfo: :class:`tencentcloud.emr.v20190103.models.CustomMetaInfo`
        :param ProductId: Product ID. Different product IDs represent different EMR product versions. Valid values:
<li>1: EMR v1.3.1.</li>
<li>2: EMR v2.0.1.</li>
<li>4: EMR v2.1.0.</li>
<li>7: EMR v3.0.0.</li>
        :type ProductId: int
        :param SceneName: Scenario-based values:
Hadoop-Kudu
Hadoop-Zookeeper
Hadoop-Presto
Hadoop-Hbase
        :type SceneName: str
        :param ExternalService: Shared component information
        :type ExternalService: list of ExternalService
        :param VersionID: 
        :type VersionID: int
        :param MultiZoneSettings: AZ specs
        :type MultiZoneSettings: list of MultiZoneSetting
        """
        self.TimeUnit = None
        self.TimeSpan = None
        self.Currency = None
        self.PayMode = None
        self.SupportHA = None
        self.Software = None
        self.ResourceSpec = None
        self.Placement = None
        self.VPCSettings = None
        self.MetaType = None
        self.UnifyMetaInstanceId = None
        self.MetaDBInfo = None
        self.ProductId = None
        self.SceneName = None
        self.ExternalService = None
        self.VersionID = None
        self.MultiZoneSettings = None


    def _deserialize(self, params):
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        self.Currency = params.get("Currency")
        self.PayMode = params.get("PayMode")
        self.SupportHA = params.get("SupportHA")
        self.Software = params.get("Software")
        if params.get("ResourceSpec") is not None:
            self.ResourceSpec = NewResourceSpec()
            self.ResourceSpec._deserialize(params.get("ResourceSpec"))
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        if params.get("VPCSettings") is not None:
            self.VPCSettings = VPCSettings()
            self.VPCSettings._deserialize(params.get("VPCSettings"))
        self.MetaType = params.get("MetaType")
        self.UnifyMetaInstanceId = params.get("UnifyMetaInstanceId")
        if params.get("MetaDBInfo") is not None:
            self.MetaDBInfo = CustomMetaInfo()
            self.MetaDBInfo._deserialize(params.get("MetaDBInfo"))
        self.ProductId = params.get("ProductId")
        self.SceneName = params.get("SceneName")
        if params.get("ExternalService") is not None:
            self.ExternalService = []
            for item in params.get("ExternalService"):
                obj = ExternalService()
                obj._deserialize(item)
                self.ExternalService.append(obj)
        self.VersionID = params.get("VersionID")
        if params.get("MultiZoneSettings") is not None:
            self.MultiZoneSettings = []
            for item in params.get("MultiZoneSettings"):
                obj = MultiZoneSetting()
                obj._deserialize(item)
                self.MultiZoneSettings.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceCreateInstanceResponse(AbstractModel):
    """InquiryPriceCreateInstance response structure.

    """

    def __init__(self):
        r"""
        :param OriginalCost: Original price.
Note: this field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: float
        :param DiscountCost: Discounted price.
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiscountCost: float
        :param TimeUnit: Time unit of instance purchase duration. Valid values:
<li>s: seconds.</li>
Note: this field may return null, indicating that no valid values can be obtained.
        :type TimeUnit: str
        :param TimeSpan: Purchase duration of instance.
Note: this field may return null, indicating that no valid values can be obtained.
        :type TimeSpan: int
        :param PriceList: The price list.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PriceList: list of ZoneDetailPriceResult
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OriginalCost = None
        self.DiscountCost = None
        self.TimeUnit = None
        self.TimeSpan = None
        self.PriceList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OriginalCost = params.get("OriginalCost")
        self.DiscountCost = params.get("DiscountCost")
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        if params.get("PriceList") is not None:
            self.PriceList = []
            for item in params.get("PriceList"):
                obj = ZoneDetailPriceResult()
                obj._deserialize(item)
                self.PriceList.append(obj)
        self.RequestId = params.get("RequestId")


class InquiryPriceRenewInstanceRequest(AbstractModel):
    """InquiryPriceRenewInstance request structure.

    """

    def __init__(self):
        r"""
        :param TimeSpan: How long the instance will be renewed for, which needs to be used together with `TimeUnit`.
        :type TimeSpan: int
        :param ResourceIds: List of resource IDs of the node to be renewed. The resource ID is in the format of `emr-vm-xxxxxxxx`. A valid resource ID can be queried in the [console](https://console.cloud.tencent.com/emr/static/hardware).
        :type ResourceIds: list of str
        :param Placement: Location of the instance. This parameter is used to specify the AZ, project, and other attributes of the instance.
        :type Placement: :class:`tencentcloud.emr.v20190103.models.Placement`
        :param PayMode: Instance billing mode.
        :type PayMode: int
        :param TimeUnit: Unit of time for instance renewal.
        :type TimeUnit: str
        :param Currency: Currency.
        :type Currency: str
        :param ModifyPayMode: Whether to change from pay-as-you-go billing to monthly subscription billing. `0`: no; `1`: yes
        :type ModifyPayMode: int
        """
        self.TimeSpan = None
        self.ResourceIds = None
        self.Placement = None
        self.PayMode = None
        self.TimeUnit = None
        self.Currency = None
        self.ModifyPayMode = None


    def _deserialize(self, params):
        self.TimeSpan = params.get("TimeSpan")
        self.ResourceIds = params.get("ResourceIds")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.PayMode = params.get("PayMode")
        self.TimeUnit = params.get("TimeUnit")
        self.Currency = params.get("Currency")
        self.ModifyPayMode = params.get("ModifyPayMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceRenewInstanceResponse(AbstractModel):
    """InquiryPriceRenewInstance response structure.

    """

    def __init__(self):
        r"""
        :param OriginalCost: Original price.
Note: this field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: float
        :param DiscountCost: Discounted price.
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiscountCost: float
        :param TimeUnit: Unit of time for instance renewal.
Note: this field may return null, indicating that no valid values can be obtained.
        :type TimeUnit: str
        :param TimeSpan: How long the instance will be renewed for.
Note: this field may return null, indicating that no valid values can be obtained.
        :type TimeSpan: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OriginalCost = None
        self.DiscountCost = None
        self.TimeUnit = None
        self.TimeSpan = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OriginalCost = params.get("OriginalCost")
        self.DiscountCost = params.get("DiscountCost")
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        self.RequestId = params.get("RequestId")


class InquiryPriceScaleOutInstanceRequest(AbstractModel):
    """InquiryPriceScaleOutInstance request structure.

    """

    def __init__(self):
        r"""
        :param TimeUnit: Time unit of scale-out. Valid value:
<li>s: Second. When `PayMode` is 0, `TimeUnit` can only be `s`.</li>
        :type TimeUnit: str
        :param TimeSpan: Time span of scale-out, which needs to be used together with `TimeUnit`.
<li>When `PayMode` is 0, `TimeSpan` can only be 3,600.</li>
        :type TimeSpan: int
        :param ZoneId: ID of the AZ where an instance resides.
        :type ZoneId: int
        :param PayMode: Instance billing mode. Valid value:
<li>0: Pay-as-you-go.</li>
        :type PayMode: int
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param CoreCount: Number of core nodes to be added.
        :type CoreCount: int
        :param TaskCount: Number of task nodes to be added.
        :type TaskCount: int
        :param Currency: Currency.
        :type Currency: str
        :param RouterCount: Number of router nodes to be added.
        :type RouterCount: int
        :param MasterCount: Number of master nodes to be added.
        :type MasterCount: int
        """
        self.TimeUnit = None
        self.TimeSpan = None
        self.ZoneId = None
        self.PayMode = None
        self.InstanceId = None
        self.CoreCount = None
        self.TaskCount = None
        self.Currency = None
        self.RouterCount = None
        self.MasterCount = None


    def _deserialize(self, params):
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        self.ZoneId = params.get("ZoneId")
        self.PayMode = params.get("PayMode")
        self.InstanceId = params.get("InstanceId")
        self.CoreCount = params.get("CoreCount")
        self.TaskCount = params.get("TaskCount")
        self.Currency = params.get("Currency")
        self.RouterCount = params.get("RouterCount")
        self.MasterCount = params.get("MasterCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceScaleOutInstanceResponse(AbstractModel):
    """InquiryPriceScaleOutInstance response structure.

    """

    def __init__(self):
        r"""
        :param OriginalCost: Original price.
Note: This field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: str
        :param DiscountCost: Discounted price.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiscountCost: str
        :param Unit: Time unit of scale-out. Valid value:
<li>s: Second.</li>
Note: This field may return null, indicating that no valid values can be obtained.
        :type Unit: str
        :param PriceSpec: Node spec queried for price.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PriceSpec: :class:`tencentcloud.emr.v20190103.models.PriceResource`
        :param MultipleEmrPrice: The inquiry results corresponding to the specs specified by the input parameter `MultipleResources`, with the result of the first spec returned by other output parameters.
Note: This field may return null, indicating that no valid values can be obtained.
        :type MultipleEmrPrice: list of EmrPrice
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OriginalCost = None
        self.DiscountCost = None
        self.Unit = None
        self.PriceSpec = None
        self.MultipleEmrPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OriginalCost = params.get("OriginalCost")
        self.DiscountCost = params.get("DiscountCost")
        self.Unit = params.get("Unit")
        if params.get("PriceSpec") is not None:
            self.PriceSpec = PriceResource()
            self.PriceSpec._deserialize(params.get("PriceSpec"))
        if params.get("MultipleEmrPrice") is not None:
            self.MultipleEmrPrice = []
            for item in params.get("MultipleEmrPrice"):
                obj = EmrPrice()
                obj._deserialize(item)
                self.MultipleEmrPrice.append(obj)
        self.RequestId = params.get("RequestId")


class InquiryPriceUpdateInstanceRequest(AbstractModel):
    """InquiryPriceUpdateInstance request structure.

    """

    def __init__(self):
        r"""
        :param TimeUnit: Time unit of scaling. Valid values:
<li>s: seconds. When `PayMode` is 0, `TimeUnit` can only be `s`.</li>
        :type TimeUnit: str
        :param TimeSpan: Duration of scaling, which needs to be used together with `TimeUnit`.
<li>When `PayMode` is 0, `TimeSpan` can only be 3,600.</li>
        :type TimeSpan: int
        :param UpdateSpec: Target node specification.
        :type UpdateSpec: :class:`tencentcloud.emr.v20190103.models.UpdateInstanceSettings`
        :param PayMode: Instance billing mode. Valid values:
<li>0: pay-as-you-go.</li>
        :type PayMode: int
        :param Placement: Instance location. This parameter is used to specify the AZ, project, and other attributes of the instance.
        :type Placement: :class:`tencentcloud.emr.v20190103.models.Placement`
        :param Currency: Currency.
        :type Currency: str
        :param ResourceIdList: The resource ID list for batch configuration change.
        :type ResourceIdList: list of str
        """
        self.TimeUnit = None
        self.TimeSpan = None
        self.UpdateSpec = None
        self.PayMode = None
        self.Placement = None
        self.Currency = None
        self.ResourceIdList = None


    def _deserialize(self, params):
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        if params.get("UpdateSpec") is not None:
            self.UpdateSpec = UpdateInstanceSettings()
            self.UpdateSpec._deserialize(params.get("UpdateSpec"))
        self.PayMode = params.get("PayMode")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.Currency = params.get("Currency")
        self.ResourceIdList = params.get("ResourceIdList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceUpdateInstanceResponse(AbstractModel):
    """InquiryPriceUpdateInstance response structure.

    """

    def __init__(self):
        r"""
        :param OriginalCost: Original price.
Note: this field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: float
        :param DiscountCost: Discounted price.
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiscountCost: float
        :param TimeUnit: Time unit of scaling. Valid values:
<li>s: seconds.</li>
Note: this field may return null, indicating that no valid values can be obtained.
        :type TimeUnit: str
        :param TimeSpan: Duration of scaling.
Note: this field may return null, indicating that no valid values can be obtained.
        :type TimeSpan: int
        :param PriceDetail: Pricing details
Note: This field may return null, indicating that no valid values can be obtained.
        :type PriceDetail: list of PriceDetail
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OriginalCost = None
        self.DiscountCost = None
        self.TimeUnit = None
        self.TimeSpan = None
        self.PriceDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OriginalCost = params.get("OriginalCost")
        self.DiscountCost = params.get("DiscountCost")
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        if params.get("PriceDetail") is not None:
            self.PriceDetail = []
            for item in params.get("PriceDetail"):
                obj = PriceDetail()
                obj._deserialize(item)
                self.PriceDetail.append(obj)
        self.RequestId = params.get("RequestId")


class InstanceChargePrepaid(AbstractModel):
    """The instance prepayment parameter. It applies only when the billing type is `PREPAID`.

    """

    def __init__(self):
        r"""
        :param Period: The period of monthly subscription, which defaults to 1 and is expressed in month.
Valid values: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36, 48, 60.
        :type Period: int
        :param RenewFlag: Whether to enable auto-renewal. Valid values:
<li>`true`: Enable</li>
<li>`false` (default): Disable</li>
        :type RenewFlag: bool
        """
        self.Period = None
        self.RenewFlag = None


    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LoginSettings(AbstractModel):
    """Login settings

    """

    def __init__(self):
        r"""
        :param Password: The login password of the instance, which contains 8 to 16 uppercase letters, lowercase letters, digits, and special characters (only !@%^*) and cannot start with a special character.
        :type Password: str
        :param PublicKeyId: The key ID. After an instance is associated with a key, you can access it with the private key in the key pair. You can call [DescribeKeyPairs](https://intl.cloud.tencent.com/document/api/213/15699?from_cn_redirect=1) to obtain `PublicKeyId`.
        :type PublicKeyId: str
        """
        self.Password = None
        self.PublicKeyId = None


    def _deserialize(self, params):
        self.Password = params.get("Password")
        self.PublicKeyId = params.get("PublicKeyId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyResourceScheduleConfigRequest(AbstractModel):
    """ModifyResourceScheduleConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: EMR cluster ID
        :type InstanceId: str
        :param Key: Business identifier. `fair`: Edit fair configuration items; `fairPlan`: Edit the execution plan; `capacity`: Edit capacity configuration items.
        :type Key: str
        :param Value: Modified module information
        :type Value: str
        """
        self.InstanceId = None
        self.Key = None
        self.Value = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Key = params.get("Key")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyResourceScheduleConfigResponse(AbstractModel):
    """ModifyResourceScheduleConfig response structure.

    """

    def __init__(self):
        r"""
        :param IsDraft: `true`: Draft, indicating the resource pool is not refreshed.
        :type IsDraft: bool
        :param ErrorMsg: Verification error information. If it is not null, the verification fails and thus the configuration fails.
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ErrorMsg: str
        :param Data: The response data.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Data: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.IsDraft = None
        self.ErrorMsg = None
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsDraft = params.get("IsDraft")
        self.ErrorMsg = params.get("ErrorMsg")
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class ModifyResourceSchedulerRequest(AbstractModel):
    """ModifyResourceScheduler request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: EMR cluster ID
        :type InstanceId: str
        :param OldValue: The original scheduler: `fair`
        :type OldValue: str
        :param NewValue: The new scheduler: `capacity`
        :type NewValue: str
        """
        self.InstanceId = None
        self.OldValue = None
        self.NewValue = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.OldValue = params.get("OldValue")
        self.NewValue = params.get("NewValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyResourceSchedulerResponse(AbstractModel):
    """ModifyResourceScheduler response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class MultiDisk(AbstractModel):
    """Multi-cloud disk parameters

    """

    def __init__(self):
        r"""
        :param DiskType: Cloud disk type
<li>`CLOUD_SSD`: SSD</li>
<li>`CLOUD_PREMIUM`: Premium Cloud Storage</li>
<li>`CLOUD_HSSD`: Enhanced SSD</li>
        :type DiskType: str
        :param Volume: Cloud disk size
        :type Volume: int
        :param Count: Number of cloud disks of this type
        :type Count: int
        """
        self.DiskType = None
        self.Volume = None
        self.Count = None


    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.Volume = params.get("Volume")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MultiDiskMC(AbstractModel):
    """Multi-cloud disk parameters

    """

    def __init__(self):
        r"""
        :param Count: Number of cloud disks in this type
Note: this field may return null, indicating that no valid values can be obtained.
        :type Count: int
        :param Type: Disk type
Note: this field may return null, indicating that no valid values can be obtained.
        :type Type: int
        :param Volume: Cloud disk size
Note: this field may return null, indicating that no valid values can be obtained.
        :type Volume: int
        """
        self.Count = None
        self.Type = None
        self.Volume = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.Type = params.get("Type")
        self.Volume = params.get("Volume")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MultiZoneSetting(AbstractModel):
    """Parameter information of each AZ

    """

    def __init__(self):
        r"""
        :param ZoneTag: "master", "standby", "third-party"
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ZoneTag: str
        :param VPCSettings: None
        :type VPCSettings: :class:`tencentcloud.emr.v20190103.models.VPCSettings`
        :param Placement: None
        :type Placement: :class:`tencentcloud.emr.v20190103.models.Placement`
        :param ResourceSpec: None
        :type ResourceSpec: :class:`tencentcloud.emr.v20190103.models.NewResourceSpec`
        """
        self.ZoneTag = None
        self.VPCSettings = None
        self.Placement = None
        self.ResourceSpec = None


    def _deserialize(self, params):
        self.ZoneTag = params.get("ZoneTag")
        if params.get("VPCSettings") is not None:
            self.VPCSettings = VPCSettings()
            self.VPCSettings._deserialize(params.get("VPCSettings"))
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        if params.get("ResourceSpec") is not None:
            self.ResourceSpec = NewResourceSpec()
            self.ResourceSpec._deserialize(params.get("ResourceSpec"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NewResourceSpec(AbstractModel):
    """Resource description

    """

    def __init__(self):
        r"""
        :param MasterResourceSpec: Describes master node resource
        :type MasterResourceSpec: :class:`tencentcloud.emr.v20190103.models.Resource`
        :param CoreResourceSpec: Describes core node resource
        :type CoreResourceSpec: :class:`tencentcloud.emr.v20190103.models.Resource`
        :param TaskResourceSpec: Describes task node resource
        :type TaskResourceSpec: :class:`tencentcloud.emr.v20190103.models.Resource`
        :param MasterCount: Number of master nodes
        :type MasterCount: int
        :param CoreCount: Number of core nodes
        :type CoreCount: int
        :param TaskCount: Number of task nodes
        :type TaskCount: int
        :param CommonResourceSpec: Describes common node resource
        :type CommonResourceSpec: :class:`tencentcloud.emr.v20190103.models.Resource`
        :param CommonCount: Number of common nodes
        :type CommonCount: int
        """
        self.MasterResourceSpec = None
        self.CoreResourceSpec = None
        self.TaskResourceSpec = None
        self.MasterCount = None
        self.CoreCount = None
        self.TaskCount = None
        self.CommonResourceSpec = None
        self.CommonCount = None


    def _deserialize(self, params):
        if params.get("MasterResourceSpec") is not None:
            self.MasterResourceSpec = Resource()
            self.MasterResourceSpec._deserialize(params.get("MasterResourceSpec"))
        if params.get("CoreResourceSpec") is not None:
            self.CoreResourceSpec = Resource()
            self.CoreResourceSpec._deserialize(params.get("CoreResourceSpec"))
        if params.get("TaskResourceSpec") is not None:
            self.TaskResourceSpec = Resource()
            self.TaskResourceSpec._deserialize(params.get("TaskResourceSpec"))
        self.MasterCount = params.get("MasterCount")
        self.CoreCount = params.get("CoreCount")
        self.TaskCount = params.get("TaskCount")
        if params.get("CommonResourceSpec") is not None:
            self.CommonResourceSpec = Resource()
            self.CommonResourceSpec._deserialize(params.get("CommonResourceSpec"))
        self.CommonCount = params.get("CommonCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodeDetailPriceResult(AbstractModel):
    """Price details by node, used for creating the cluster price list

    """

    def __init__(self):
        r"""
        :param NodeType: The node type. Valid values: `master`, `core`, `task`, `common`, `router`, `mysql`
Note: This field may return null, indicating that no valid values can be obtained.
        :type NodeType: str
        :param PartDetailPrice: Price details by node part
        :type PartDetailPrice: list of PartDetailPriceItem
        """
        self.NodeType = None
        self.PartDetailPrice = None


    def _deserialize(self, params):
        self.NodeType = params.get("NodeType")
        if params.get("PartDetailPrice") is not None:
            self.PartDetailPrice = []
            for item in params.get("PartDetailPrice"):
                obj = PartDetailPriceItem()
                obj._deserialize(item)
                self.PartDetailPrice.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodeHardwareInfo(AbstractModel):
    """Node hardware information

    """

    def __init__(self):
        r"""
        :param AppId: User `APPID`
Note: this field may return null, indicating that no valid values can be obtained.
        :type AppId: int
        :param SerialNo: Serial number
Note: this field may return null, indicating that no valid values can be obtained.
        :type SerialNo: str
        :param OrderNo: Machine instance ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type OrderNo: str
        :param WanIp: Public IP bound to master node
Note: this field may return null, indicating that no valid values can be obtained.
        :type WanIp: str
        :param Flag: Node type. 0: common node; 1: master node;
2: core node; 3: task node
Note: this field may return null, indicating that no valid values can be obtained.
        :type Flag: int
        :param Spec: Node specification
Note: this field may return null, indicating that no valid values can be obtained.
        :type Spec: str
        :param CpuNum: Number of node cores
Note: this field may return null, indicating that no valid values can be obtained.
        :type CpuNum: int
        :param MemSize: Node memory size
Note: this field may return null, indicating that no valid values can be obtained.
        :type MemSize: int
        :param MemDesc: Node memory description
Note: this field may return null, indicating that no valid values can be obtained.
        :type MemDesc: str
        :param RegionId: Node region
Note: this field may return null, indicating that no valid values can be obtained.
        :type RegionId: int
        :param ZoneId: Node AZ
Note: this field may return null, indicating that no valid values can be obtained.
        :type ZoneId: int
        :param ApplyTime: Application time
Note: this field may return null, indicating that no valid values can be obtained.
        :type ApplyTime: str
        :param FreeTime: Release time
Note: this field may return null, indicating that no valid values can be obtained.
        :type FreeTime: str
        :param DiskSize: Disk size
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiskSize: str
        :param NameTag: Node description
Note: this field may return null, indicating that no valid values can be obtained.
        :type NameTag: str
        :param Services: Services deployed on node
Note: this field may return null, indicating that no valid values can be obtained.
        :type Services: str
        :param StorageType: Disk type
Note: this field may return null, indicating that no valid values can be obtained.
        :type StorageType: int
        :param RootSize: System disk size
Note: this field may return null, indicating that no valid values can be obtained.
        :type RootSize: int
        :param ChargeType: Payment type
Note: this field may return null, indicating that no valid values can be obtained.
        :type ChargeType: int
        :param CdbIp: Database IP
Note: this field may return null, indicating that no valid values can be obtained.
        :type CdbIp: str
        :param CdbPort: Database port
Note: this field may return null, indicating that no valid values can be obtained.
        :type CdbPort: int
        :param HwDiskSize: Disk capacity
Note: this field may return null, indicating that no valid values can be obtained.
        :type HwDiskSize: int
        :param HwDiskSizeDesc: Disk capacity description
Note: this field may return null, indicating that no valid values can be obtained.
        :type HwDiskSizeDesc: str
        :param HwMemSize: Memory capacity
Note: this field may return null, indicating that no valid values can be obtained.
        :type HwMemSize: int
        :param HwMemSizeDesc: Memory capacity description
Note: this field may return null, indicating that no valid values can be obtained.
        :type HwMemSizeDesc: str
        :param ExpireTime: Expiration time
Note: this field may return null, indicating that no valid values can be obtained.
        :type ExpireTime: str
        :param EmrResourceId: Node resource ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type EmrResourceId: str
        :param IsAutoRenew: Renewal flag
Note: this field may return null, indicating that no valid values can be obtained.
        :type IsAutoRenew: int
        :param DeviceClass: Device flag
Note: this field may return null, indicating that no valid values can be obtained.
        :type DeviceClass: str
        :param Mutable: Support for configuration adjustment
Note: this field may return null, indicating that no valid values can be obtained.
        :type Mutable: int
        :param MCMultiDisk: Multi-cloud disk
Note: this field may return null, indicating that no valid values can be obtained.
        :type MCMultiDisk: list of MultiDiskMC
        :param CdbNodeInfo: Database information
Note: this field may return null, indicating that no valid values can be obtained.
        :type CdbNodeInfo: :class:`tencentcloud.emr.v20190103.models.CdbInfo`
        :param Ip: Private IP
Note: this field may return null, indicating that no valid values can be obtained.
        :type Ip: str
        :param Destroyable: Whether this node can be terminated. 1: yes, 0: no
Note: this field may return null, indicating that no valid values can be obtained.
        :type Destroyable: int
        :param Tags: Tags bound to node
Note: this field may return null, indicating that no valid values can be obtained.
        :type Tags: list of Tag
        :param AutoFlag: Wether the node is auto-scaling. 0 means common node. 1 means auto-scaling node.
        :type AutoFlag: int
        :param HardwareResourceType: Resource type. Valid values: host, pod
Note: this field may return null, indicating that no valid values can be obtained.
        :type HardwareResourceType: str
        :param IsDynamicSpec: Whether floating specification is used. `1`: yes; `0`: no
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type IsDynamicSpec: int
        :param DynamicPodSpec: Floating specification in JSON string
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DynamicPodSpec: str
        :param SupportModifyPayMode: Whether to support billing mode change. `0`: no; `1`: yes
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type SupportModifyPayMode: int
        :param RootStorageType: System disk type
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type RootStorageType: int
        :param Zone: AZ information
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Zone: str
        :param SubnetInfo: Subnet
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type SubnetInfo: :class:`tencentcloud.emr.v20190103.models.SubnetInfo`
        :param Clients: Client
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type Clients: str
        :param CurrentTime: The current system time.
Note: This field may return null, indicating that no valid values can be obtained.
        :type CurrentTime: str
        :param IsFederation: Whether it is used in a federation. Valid values: `0` (no), `1` (yes).
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsFederation: int
        :param DeviceName: Device name
Note: This field may return null, indicating that no valid values can be obtained.
        :type DeviceName: str
        :param ServiceClient: Service
Note: This field may return null, indicating that no valid values can be obtained.
        :type ServiceClient: str
        :param DisableApiTermination: Enabling instance protection for this instance. Valid values: `true` (enable) and `false` (disable).
Note: This field may return null, indicating that no valid values can be obtained.
        :type DisableApiTermination: bool
        :param TradeVersion: The billing version. Valid values: `0` (original billing) and `1` (new billing)
Note: This field may return null, indicating that no valid values can be obtained.
        :type TradeVersion: int
        """
        self.AppId = None
        self.SerialNo = None
        self.OrderNo = None
        self.WanIp = None
        self.Flag = None
        self.Spec = None
        self.CpuNum = None
        self.MemSize = None
        self.MemDesc = None
        self.RegionId = None
        self.ZoneId = None
        self.ApplyTime = None
        self.FreeTime = None
        self.DiskSize = None
        self.NameTag = None
        self.Services = None
        self.StorageType = None
        self.RootSize = None
        self.ChargeType = None
        self.CdbIp = None
        self.CdbPort = None
        self.HwDiskSize = None
        self.HwDiskSizeDesc = None
        self.HwMemSize = None
        self.HwMemSizeDesc = None
        self.ExpireTime = None
        self.EmrResourceId = None
        self.IsAutoRenew = None
        self.DeviceClass = None
        self.Mutable = None
        self.MCMultiDisk = None
        self.CdbNodeInfo = None
        self.Ip = None
        self.Destroyable = None
        self.Tags = None
        self.AutoFlag = None
        self.HardwareResourceType = None
        self.IsDynamicSpec = None
        self.DynamicPodSpec = None
        self.SupportModifyPayMode = None
        self.RootStorageType = None
        self.Zone = None
        self.SubnetInfo = None
        self.Clients = None
        self.CurrentTime = None
        self.IsFederation = None
        self.DeviceName = None
        self.ServiceClient = None
        self.DisableApiTermination = None
        self.TradeVersion = None


    def _deserialize(self, params):
        self.AppId = params.get("AppId")
        self.SerialNo = params.get("SerialNo")
        self.OrderNo = params.get("OrderNo")
        self.WanIp = params.get("WanIp")
        self.Flag = params.get("Flag")
        self.Spec = params.get("Spec")
        self.CpuNum = params.get("CpuNum")
        self.MemSize = params.get("MemSize")
        self.MemDesc = params.get("MemDesc")
        self.RegionId = params.get("RegionId")
        self.ZoneId = params.get("ZoneId")
        self.ApplyTime = params.get("ApplyTime")
        self.FreeTime = params.get("FreeTime")
        self.DiskSize = params.get("DiskSize")
        self.NameTag = params.get("NameTag")
        self.Services = params.get("Services")
        self.StorageType = params.get("StorageType")
        self.RootSize = params.get("RootSize")
        self.ChargeType = params.get("ChargeType")
        self.CdbIp = params.get("CdbIp")
        self.CdbPort = params.get("CdbPort")
        self.HwDiskSize = params.get("HwDiskSize")
        self.HwDiskSizeDesc = params.get("HwDiskSizeDesc")
        self.HwMemSize = params.get("HwMemSize")
        self.HwMemSizeDesc = params.get("HwMemSizeDesc")
        self.ExpireTime = params.get("ExpireTime")
        self.EmrResourceId = params.get("EmrResourceId")
        self.IsAutoRenew = params.get("IsAutoRenew")
        self.DeviceClass = params.get("DeviceClass")
        self.Mutable = params.get("Mutable")
        if params.get("MCMultiDisk") is not None:
            self.MCMultiDisk = []
            for item in params.get("MCMultiDisk"):
                obj = MultiDiskMC()
                obj._deserialize(item)
                self.MCMultiDisk.append(obj)
        if params.get("CdbNodeInfo") is not None:
            self.CdbNodeInfo = CdbInfo()
            self.CdbNodeInfo._deserialize(params.get("CdbNodeInfo"))
        self.Ip = params.get("Ip")
        self.Destroyable = params.get("Destroyable")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.AutoFlag = params.get("AutoFlag")
        self.HardwareResourceType = params.get("HardwareResourceType")
        self.IsDynamicSpec = params.get("IsDynamicSpec")
        self.DynamicPodSpec = params.get("DynamicPodSpec")
        self.SupportModifyPayMode = params.get("SupportModifyPayMode")
        self.RootStorageType = params.get("RootStorageType")
        self.Zone = params.get("Zone")
        if params.get("SubnetInfo") is not None:
            self.SubnetInfo = SubnetInfo()
            self.SubnetInfo._deserialize(params.get("SubnetInfo"))
        self.Clients = params.get("Clients")
        self.CurrentTime = params.get("CurrentTime")
        self.IsFederation = params.get("IsFederation")
        self.DeviceName = params.get("DeviceName")
        self.ServiceClient = params.get("ServiceClient")
        self.DisableApiTermination = params.get("DisableApiTermination")
        self.TradeVersion = params.get("TradeVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodeResourceSpec(AbstractModel):
    """Resource details

    """

    def __init__(self):
        r"""
        :param InstanceType: The spec type, such as `S2.MEDIUM8`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceType: str
        :param SystemDisk: The system disk, which can be up to 1 PCS.
Note: This field may return null, indicating that no valid values can be obtained.
        :type SystemDisk: list of DiskSpecInfo
        :param Tags: The list of tags to be bound.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Tags: list of Tag
        :param DataDisk: The cloud data disk, which can be up to 15 PCS.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DataDisk: list of DiskSpecInfo
        :param LocalDataDisk: The local data disk.
Note: This field may return null, indicating that no valid values can be obtained.
        :type LocalDataDisk: list of DiskSpecInfo
        """
        self.InstanceType = None
        self.SystemDisk = None
        self.Tags = None
        self.DataDisk = None
        self.LocalDataDisk = None


    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = []
            for item in params.get("SystemDisk"):
                obj = DiskSpecInfo()
                obj._deserialize(item)
                self.SystemDisk.append(obj)
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        if params.get("DataDisk") is not None:
            self.DataDisk = []
            for item in params.get("DataDisk"):
                obj = DiskSpecInfo()
                obj._deserialize(item)
                self.DataDisk.append(obj)
        if params.get("LocalDataDisk") is not None:
            self.LocalDataDisk = []
            for item in params.get("LocalDataDisk"):
                obj = DiskSpecInfo()
                obj._deserialize(item)
                self.LocalDataDisk.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OpScope(AbstractModel):
    """Operation scope

    """

    def __init__(self):
        r"""
        :param ServiceInfoList: The information of the services to operate on.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ServiceInfoList: list of ServiceBasicRestartInfo
        """
        self.ServiceInfoList = None


    def _deserialize(self, params):
        if params.get("ServiceInfoList") is not None:
            self.ServiceInfoList = []
            for item in params.get("ServiceInfoList"):
                obj = ServiceBasicRestartInfo()
                obj._deserialize(item)
                self.ServiceInfoList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OutterResource(AbstractModel):
    """Resource details

    """

    def __init__(self):
        r"""
        :param Spec: Specification
Note: this field may return null, indicating that no valid values can be obtained.
        :type Spec: str
        :param SpecName: Specification name
Note: this field may return null, indicating that no valid values can be obtained.
        :type SpecName: str
        :param StorageType: Disk type
Note: this field may return null, indicating that no valid values can be obtained.
        :type StorageType: int
        :param DiskType: Disk type
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiskType: str
        :param RootSize: System disk size
Note: this field may return null, indicating that no valid values can be obtained.
        :type RootSize: int
        :param MemSize: Memory size
Note: this field may return null, indicating that no valid values can be obtained.
        :type MemSize: int
        :param Cpu: Number of CPUs
Note: this field may return null, indicating that no valid values can be obtained.
        :type Cpu: int
        :param DiskSize: Disk size
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiskSize: int
        :param InstanceType: Specification
Note: this field may return null, indicating that no valid values can be obtained.
        :type InstanceType: str
        """
        self.Spec = None
        self.SpecName = None
        self.StorageType = None
        self.DiskType = None
        self.RootSize = None
        self.MemSize = None
        self.Cpu = None
        self.DiskSize = None
        self.InstanceType = None


    def _deserialize(self, params):
        self.Spec = params.get("Spec")
        self.SpecName = params.get("SpecName")
        self.StorageType = params.get("StorageType")
        self.DiskType = params.get("DiskType")
        self.RootSize = params.get("RootSize")
        self.MemSize = params.get("MemSize")
        self.Cpu = params.get("Cpu")
        self.DiskSize = params.get("DiskSize")
        self.InstanceType = params.get("InstanceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PartDetailPriceItem(AbstractModel):
    """Price details by node part, used for creating the cluster price list

    """

    def __init__(self):
        r"""
        :param InstanceType: The type. Valid values: `node` (node); `rootDisk` (system disk); `dataDisk` and `metaDB` (cloud data disk)
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceType: str
        :param Price: Rate (original)
Note: This field may return null, indicating that no valid values can be obtained.
        :type Price: float
        :param RealCost: Rate (discounted)
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealCost: float
        :param RealTotalCost: Total price (discounted)
Note: This field may return null, indicating that no valid values can be obtained.
        :type RealTotalCost: float
        :param Policy: Discount
Note: This field may return null, indicating that no valid values can be obtained.
        :type Policy: float
        :param GoodsNum: Quantity
Note: This field may return null, indicating that no valid values can be obtained.
        :type GoodsNum: int
        """
        self.InstanceType = None
        self.Price = None
        self.RealCost = None
        self.RealTotalCost = None
        self.Policy = None
        self.GoodsNum = None


    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        self.Price = params.get("Price")
        self.RealCost = params.get("RealCost")
        self.RealTotalCost = params.get("RealTotalCost")
        self.Policy = params.get("Policy")
        self.GoodsNum = params.get("GoodsNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PersistentVolumeContext(AbstractModel):
    """Description of Pod `PVC` storage method

    """

    def __init__(self):
        r"""
        :param DiskSize: Disk size in GB.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskSize: int
        :param DiskType: Disk type. Valid values: `CLOUD_PREMIUM` and `CLOUD_SSD`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskType: str
        :param DiskNum: Number of disks.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskNum: int
        """
        self.DiskSize = None
        self.DiskType = None
        self.DiskNum = None


    def _deserialize(self, params):
        self.DiskSize = params.get("DiskSize")
        self.DiskType = params.get("DiskType")
        self.DiskNum = params.get("DiskNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Placement(AbstractModel):
    """Location information of cluster instance

    """

    def __init__(self):
        r"""
        :param Zone: The ID of the availability zone where the instance resides, such as `ap-guangzhou-1`. You can call the [DescribeZones](https://intl.cloud.tencent.com/document/product/213/15707?from_cn_redirect=1) API and obtain this ID from the `Zone` field in the response.
        :type Zone: str
        :param ProjectId: Project ID of the instance. If no ID is passed in, the default project ID is used.
        :type ProjectId: int
        """
        self.Zone = None
        self.ProjectId = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ProjectId = params.get("ProjectId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PodNewParameter(AbstractModel):
    """The custom pod permission and parameter.

    """

    def __init__(self):
        r"""
        :param InstanceId: The TKE or EKS cluster ID.
        :type InstanceId: str
        :param Config: Custom permissions
Examples:
{
  "apiVersion": "v1",
  "clusters": [
    {
      "cluster": {
        "certificate-authority-data": "xxxxxx==",
        "server": "https://xxxxx.com"
      },
      "name": "cls-xxxxx"
    }
  ],
  "contexts": [
    {
      "context": {
        "cluster": "cls-xxxxx",
        "user": "100014xxxxx"
      },
      "name": "cls-a44yhcxxxxxxxxxx"
    }
  ],
  "current-context": "cls-a4xxxx-context-default",
  "kind": "Config",
  "preferences": {},
  "users": [
    {
      "name": "100014xxxxx",
      "user": {
        "client-certificate-data": "xxxxxx",
        "client-key-data": "xxxxxx"
      }
    }
  ]
}
        :type Config: str
        :param Parameter: Custom parameters
Examples:
{
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
      "name": "test-deployment",
      "labels": {
        "app": "test"
      }
    },
    "spec": {
      "replicas": 3,
      "selector": {
        "matchLabels": {
          "app": "test-app"
        }
      },
      "template": {
        "metadata": {
          "annotations": {
            "your-organization.com/department-v1": "test-example-v1",
            "your-organization.com/department-v2": "test-example-v2"
          },
          "labels": {
            "app": "test-app",
            "environment": "production"
          }
        },
        "spec": {
          "nodeSelector": {
            "your-organization/node-test": "test-node"
          },
          "containers": [
            {
              "name": "nginx",
              "image": "nginx:1.14.2",
              "ports": [
                {
                  "containerPort": 80
                }
              ]
            }
          ],
          "affinity": {
            "nodeAffinity": {
              "requiredDuringSchedulingIgnoredDuringExecution": {
                "nodeSelectorTerms": [
                  {
                    "matchExpressions": [
                      {
                        "key": "disk-type",
                        "operator": "In",
                        "values": [
                          "ssd",
                          "sas"
                        ]
                      },
                      {
                        "key": "cpu-num",
                        "operator": "Gt",
                        "values": [
                          "6"
                        ]
                      }
                    ]
                  }
                ]
              }
            }
          }
        }
      }
    }
  }
        :type Parameter: str
        """
        self.InstanceId = None
        self.Config = None
        self.Parameter = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Config = params.get("Config")
        self.Parameter = params.get("Parameter")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PodNewSpec(AbstractModel):
    """Resource descriptions for container resource scale-out

    """

    def __init__(self):
        r"""
        :param ResourceProviderIdentifier: The identifier of an external resource provider, such as "cls-a1cd23fa".
        :type ResourceProviderIdentifier: str
        :param ResourceProviderType: The type of the external resource provider, such as "tke". Currently, only "tke" is supported.
        :type ResourceProviderType: str
        :param NodeFlag: The purpose of the resource, which means the node type and can only be "TASK".
        :type NodeFlag: str
        :param Cpu: The number of CPUs.
        :type Cpu: int
        :param Memory: The memory size in GB.
        :type Memory: int
        :param CpuType: The EKS cluster - CPU type. Valid values: `intel` and `amd`.
        :type CpuType: str
        :param PodVolumes: The data directory mounting information of the pod node.
        :type PodVolumes: list of PodVolume
        :param EnableDynamicSpecFlag: Whether the dynamic spec is used. Valid values:
<li>`true`: Yes</li>
<li>`false` (default): No</li>
        :type EnableDynamicSpecFlag: bool
        :param DynamicPodSpec: The dynamic spec.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DynamicPodSpec: :class:`tencentcloud.emr.v20190103.models.DynamicPodSpec`
        :param VpcId: The unique VPC ID.
Note: This field may return null, indicating that no valid values can be obtained.
        :type VpcId: str
        :param SubnetId: The unique VPC subnet ID.
Note: This field may return null, indicating that no valid values can be obtained.
        :type SubnetId: str
        :param PodName: The pod name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PodName: str
        """
        self.ResourceProviderIdentifier = None
        self.ResourceProviderType = None
        self.NodeFlag = None
        self.Cpu = None
        self.Memory = None
        self.CpuType = None
        self.PodVolumes = None
        self.EnableDynamicSpecFlag = None
        self.DynamicPodSpec = None
        self.VpcId = None
        self.SubnetId = None
        self.PodName = None


    def _deserialize(self, params):
        self.ResourceProviderIdentifier = params.get("ResourceProviderIdentifier")
        self.ResourceProviderType = params.get("ResourceProviderType")
        self.NodeFlag = params.get("NodeFlag")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.CpuType = params.get("CpuType")
        if params.get("PodVolumes") is not None:
            self.PodVolumes = []
            for item in params.get("PodVolumes"):
                obj = PodVolume()
                obj._deserialize(item)
                self.PodVolumes.append(obj)
        self.EnableDynamicSpecFlag = params.get("EnableDynamicSpecFlag")
        if params.get("DynamicPodSpec") is not None:
            self.DynamicPodSpec = DynamicPodSpec()
            self.DynamicPodSpec._deserialize(params.get("DynamicPodSpec"))
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.PodName = params.get("PodName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PodParameter(AbstractModel):
    """Custom pod permission and parameter

    """

    def __init__(self):
        r"""
        :param ClusterId: ID of TKE or EKS cluster
        :type ClusterId: str
        :param Config: Custom permissions
Example:
{
  "apiVersion": "v1",
  "Clusters": [
    {
      "cluster": {
        "certificate-authority-data": "xxxxxx==",
        "server": "https://xxxxx.com"
      },
      "name": "cls-xxxxx"
    }
  ],
  "contexts": [
    {
      "context": {
        "cluster": "cls-xxxxx",
        "user": "100014xxxxx"
      },
      "name": "cls-a44yhcxxxxxxxxxx"
    }
  ],
  "current-context": "cls-a4xxxx-context-default",
  "kind": "Config",
  "preferences": {},
  "users": [
    {
      "name": "100014xxxxx",
      "user": {
        "client-certificate-data": "xxxxxx",
        "client-key-data": "xxxxxx"
      }
    }
  ]
}
        :type Config: str
        :param Parameter: Custom parameters
Example:
{
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
      "name": "test-deployment",
      "labels": {
        "app": "test"
      }
    },
    "spec": {
      "replicas": 3,
      "selector": {
        "matchLabels": {
          "app": "test-app"
        }
      },
      "template": {
        "metadata": {
          "annotations": {
            "your-organization.com/department-v1": "test-example-v1",
            "your-organization.com/department-v2": "test-example-v2"
          },
          "labels": {
            "app": "test-app",
            "environment": "production"
          }
        },
        "spec": {
          "nodeSelector": {
            "your-organization/node-test": "test-node"
          },
          "containers": [
            {
              "name": "nginx",
              "image": "nginx:1.14.2",
              "ports": [
                {
                  "containerPort": 80
                }
              ]
            }
          ],
          "affinity": {
            "nodeAffinity": {
              "requiredDuringSchedulingIgnoredDuringExecution": {
                "nodeSelectorTerms": [
                  {
                    "matchExpressions": [
                      {
                        "key": "disk-type",
                        "operator": "In",
                        "values": [
                          "ssd",
                          "sas"
                        ]
                      },
                      {
                        "key": "cpu-num",
                        "operator": "Gt",
                        "values": [
                          "6"
                        ]
                      }
                    ]
                  }
                ]
              }
            }
          }
        }
      }
    }
  }
        :type Parameter: str
        """
        self.ClusterId = None
        self.Config = None
        self.Parameter = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Config = params.get("Config")
        self.Parameter = params.get("Parameter")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PodSpec(AbstractModel):
    """Resource description for container resource scale-out

    """

    def __init__(self):
        r"""
        :param ResourceProviderIdentifier: Identifier of external resource provider, such as "cls-a1cd23fa".
        :type ResourceProviderIdentifier: str
        :param ResourceProviderType: Type of external resource provider, such as "tke". Currently, only "tke" is supported.
        :type ResourceProviderType: str
        :param NodeType: Purpose of the resource, which means the node type and can only be "TASK".
        :type NodeType: str
        :param Cpu: Number of CPUs
        :type Cpu: int
        :param Memory: Memory size in GB.
        :type Memory: int
        :param DataVolumes: Mount point of resources for the host. A specified mount point corresponds to the host path and is used as the data storage directory in the pod. (This parameter has been disused)
        :type DataVolumes: list of str
        :param CpuType: EKS cluster - CPU type. Valid values: `intel` and `amd`.
        :type CpuType: str
        :param PodVolumes: Data directory mounting information of the pod node.
        :type PodVolumes: list of PodVolume
        :param IsDynamicSpec: Whether floating specification is used. `1`: Yes; `0`: No.
        :type IsDynamicSpec: int
        :param DynamicPodSpec: Floating specification
Note: This field may return null, indicating that no valid values can be obtained.
        :type DynamicPodSpec: :class:`tencentcloud.emr.v20190103.models.DynamicPodSpec`
        :param VpcId: Unique VPC ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type VpcId: str
        :param SubnetId: Unique VPC subnet ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type SubnetId: str
        :param PodName: pod name
Note: This field may return null, indicating that no valid values can be obtained.
        :type PodName: str
        """
        self.ResourceProviderIdentifier = None
        self.ResourceProviderType = None
        self.NodeType = None
        self.Cpu = None
        self.Memory = None
        self.DataVolumes = None
        self.CpuType = None
        self.PodVolumes = None
        self.IsDynamicSpec = None
        self.DynamicPodSpec = None
        self.VpcId = None
        self.SubnetId = None
        self.PodName = None


    def _deserialize(self, params):
        self.ResourceProviderIdentifier = params.get("ResourceProviderIdentifier")
        self.ResourceProviderType = params.get("ResourceProviderType")
        self.NodeType = params.get("NodeType")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.DataVolumes = params.get("DataVolumes")
        self.CpuType = params.get("CpuType")
        if params.get("PodVolumes") is not None:
            self.PodVolumes = []
            for item in params.get("PodVolumes"):
                obj = PodVolume()
                obj._deserialize(item)
                self.PodVolumes.append(obj)
        self.IsDynamicSpec = params.get("IsDynamicSpec")
        if params.get("DynamicPodSpec") is not None:
            self.DynamicPodSpec = DynamicPodSpec()
            self.DynamicPodSpec._deserialize(params.get("DynamicPodSpec"))
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.PodName = params.get("PodName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PodSpecInfo(AbstractModel):
    """Other pod information.

    """

    def __init__(self):
        r"""
        :param PodSpec: The specified information such as pod spec and source for scale-out with pod resources.
        :type PodSpec: :class:`tencentcloud.emr.v20190103.models.PodNewSpec`
        :param PodParameter: The custom pod permission and parameter.
        :type PodParameter: :class:`tencentcloud.emr.v20190103.models.PodNewParameter`
        """
        self.PodSpec = None
        self.PodParameter = None


    def _deserialize(self, params):
        if params.get("PodSpec") is not None:
            self.PodSpec = PodNewSpec()
            self.PodSpec._deserialize(params.get("PodSpec"))
        if params.get("PodParameter") is not None:
            self.PodParameter = PodNewParameter()
            self.PodParameter._deserialize(params.get("PodParameter"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PodVolume(AbstractModel):
    """Description of Pod storage.

    """

    def __init__(self):
        r"""
        :param VolumeType: Storage type. Valid values: `pvc` and `hostpath`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type VolumeType: str
        :param PVCVolume: This field will take effect if `VolumeType` is `pvc`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PVCVolume: :class:`tencentcloud.emr.v20190103.models.PersistentVolumeContext`
        :param HostVolume: This field will take effect if `VolumeType` is `hostpath`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type HostVolume: :class:`tencentcloud.emr.v20190103.models.HostVolumeContext`
        """
        self.VolumeType = None
        self.PVCVolume = None
        self.HostVolume = None


    def _deserialize(self, params):
        self.VolumeType = params.get("VolumeType")
        if params.get("PVCVolume") is not None:
            self.PVCVolume = PersistentVolumeContext()
            self.PVCVolume._deserialize(params.get("PVCVolume"))
        if params.get("HostVolume") is not None:
            self.HostVolume = HostVolumeContext()
            self.HostVolume._deserialize(params.get("HostVolume"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PreExecuteFileSettings(AbstractModel):
    """Pre-execution script configuration

    """

    def __init__(self):
        r"""
        :param Path: COS path to script, which has been disused
        :type Path: str
        :param Args: Execution script parameter
        :type Args: list of str
        :param Bucket: COS bucket name, which has been disused
        :type Bucket: str
        :param Region: COS region name, which has been disused
        :type Region: str
        :param Domain: COS domain data, which has been disused
        :type Domain: str
        :param RunOrder: Execution sequence
        :type RunOrder: int
        :param WhenRun: `resourceAfter` or `clusterAfter`
        :type WhenRun: str
        :param CosFileName: Script name, which has been disused
        :type CosFileName: str
        :param CosFileURI: COS address of script
        :type CosFileURI: str
        :param CosSecretId: COS `SecretId`
        :type CosSecretId: str
        :param CosSecretKey: COS `SecretKey`
        :type CosSecretKey: str
        :param AppId: COS `appid`, which has been disused
        :type AppId: str
        """
        self.Path = None
        self.Args = None
        self.Bucket = None
        self.Region = None
        self.Domain = None
        self.RunOrder = None
        self.WhenRun = None
        self.CosFileName = None
        self.CosFileURI = None
        self.CosSecretId = None
        self.CosSecretKey = None
        self.AppId = None


    def _deserialize(self, params):
        self.Path = params.get("Path")
        self.Args = params.get("Args")
        self.Bucket = params.get("Bucket")
        self.Region = params.get("Region")
        self.Domain = params.get("Domain")
        self.RunOrder = params.get("RunOrder")
        self.WhenRun = params.get("WhenRun")
        self.CosFileName = params.get("CosFileName")
        self.CosFileURI = params.get("CosFileURI")
        self.CosSecretId = params.get("CosSecretId")
        self.CosSecretKey = params.get("CosSecretKey")
        self.AppId = params.get("AppId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PriceDetail(AbstractModel):
    """Pricing details

    """

    def __init__(self):
        r"""
        :param ResourceId: The node ID
        :type ResourceId: str
        :param Formula: The price formula
        :type Formula: str
        :param OriginalCost: The original price
        :type OriginalCost: float
        :param DiscountCost: The discount price
        :type DiscountCost: float
        """
        self.ResourceId = None
        self.Formula = None
        self.OriginalCost = None
        self.DiscountCost = None


    def _deserialize(self, params):
        self.ResourceId = params.get("ResourceId")
        self.Formula = params.get("Formula")
        self.OriginalCost = params.get("OriginalCost")
        self.DiscountCost = params.get("DiscountCost")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PriceResource(AbstractModel):
    """Resource queried for price

    """

    def __init__(self):
        r"""
        :param Spec: Target specification
Note: This field may return null, indicating that no valid values can be obtained.
        :type Spec: str
        :param StorageType: Disk type.
Note: This field may return null, indicating that no valid values can be obtained.
        :type StorageType: int
        :param DiskType: Disk type.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskType: str
        :param RootSize: System disk size
Note: This field may return null, indicating that no valid values can be obtained.
        :type RootSize: int
        :param MemSize: Memory size.
Note: This field may return null, indicating that no valid values can be obtained.
        :type MemSize: int
        :param Cpu: Number of CPUs.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Cpu: int
        :param DiskSize: Disk size.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskSize: int
        :param MultiDisks: List of cloud disks.
Note: This field may return null, indicating that no valid values can be obtained.
        :type MultiDisks: list of MultiDisk
        :param DiskCnt: Number of disks.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskCnt: int
        :param InstanceType: Specification
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceType: str
        :param Tags: Tag
Note: This field may return null, indicating that no valid values can be obtained.
        :type Tags: list of Tag
        :param DiskNum: Number of disks.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiskNum: int
        :param LocalDiskNum: Number of local disks.
Note: This field may return null, indicating that no valid values can be obtained.
        :type LocalDiskNum: int
        """
        self.Spec = None
        self.StorageType = None
        self.DiskType = None
        self.RootSize = None
        self.MemSize = None
        self.Cpu = None
        self.DiskSize = None
        self.MultiDisks = None
        self.DiskCnt = None
        self.InstanceType = None
        self.Tags = None
        self.DiskNum = None
        self.LocalDiskNum = None


    def _deserialize(self, params):
        self.Spec = params.get("Spec")
        self.StorageType = params.get("StorageType")
        self.DiskType = params.get("DiskType")
        self.RootSize = params.get("RootSize")
        self.MemSize = params.get("MemSize")
        self.Cpu = params.get("Cpu")
        self.DiskSize = params.get("DiskSize")
        if params.get("MultiDisks") is not None:
            self.MultiDisks = []
            for item in params.get("MultiDisks"):
                obj = MultiDisk()
                obj._deserialize(item)
                self.MultiDisks.append(obj)
        self.DiskCnt = params.get("DiskCnt")
        self.InstanceType = params.get("InstanceType")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.DiskNum = params.get("DiskNum")
        self.LocalDiskNum = params.get("LocalDiskNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Resource(AbstractModel):
    """Resource details

    """

    def __init__(self):
        r"""
        :param Spec: Node specification description, such as CVM.SA2
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Spec: str
        :param StorageType: Storage type
Valid values:
<li>4: SSD</li>
<li>5: Premium Cloud Storage</li>
<li>6: Enhanced SSD</li>
<li>11: High-Throughput cloud disk</li>
<li>12: Tremendous SSD</li>
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type StorageType: int
        :param DiskType: Disk type
Valid values:
<li>`CLOUD_SSD`: SSD</li>
<li>`CLOUD_PREMIUM`: Premium Cloud Storage</li>
<li>`CLOUD_BASIC`: HDD</li>
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DiskType: str
        :param MemSize: Memory capacity in MB
Note: this field may return null, indicating that no valid values can be obtained.
        :type MemSize: int
        :param Cpu: Number of CPU cores
Note: this field may return null, indicating that no valid values can be obtained.
        :type Cpu: int
        :param DiskSize: Data disk capacity
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiskSize: int
        :param RootSize: System disk capacity
Note: this field may return null, indicating that no valid values can be obtained.
        :type RootSize: int
        :param MultiDisks: List of cloud disks. When the data disk is a cloud disk, `DiskType` and `DiskSize` are used directly; `MultiDisks` will be used for the excessive part
Note: this field may return null, indicating that no valid values can be obtained.
        :type MultiDisks: list of MultiDisk
        :param Tags: List of tags to be bound
Note: this field may return null, indicating that no valid values can be obtained.
        :type Tags: list of Tag
        :param InstanceType: Specification type, such as S2.MEDIUM8
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type InstanceType: str
        :param LocalDiskNum: Number of local disks. This field has been disused.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type LocalDiskNum: int
        :param DiskNum: Number of local disks, such as 2
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DiskNum: int
        """
        self.Spec = None
        self.StorageType = None
        self.DiskType = None
        self.MemSize = None
        self.Cpu = None
        self.DiskSize = None
        self.RootSize = None
        self.MultiDisks = None
        self.Tags = None
        self.InstanceType = None
        self.LocalDiskNum = None
        self.DiskNum = None


    def _deserialize(self, params):
        self.Spec = params.get("Spec")
        self.StorageType = params.get("StorageType")
        self.DiskType = params.get("DiskType")
        self.MemSize = params.get("MemSize")
        self.Cpu = params.get("Cpu")
        self.DiskSize = params.get("DiskSize")
        self.RootSize = params.get("RootSize")
        if params.get("MultiDisks") is not None:
            self.MultiDisks = []
            for item in params.get("MultiDisks"):
                obj = MultiDisk()
                obj._deserialize(item)
                self.MultiDisks.append(obj)
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.InstanceType = params.get("InstanceType")
        self.LocalDiskNum = params.get("LocalDiskNum")
        self.DiskNum = params.get("DiskNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScaleOutClusterRequest(AbstractModel):
    """ScaleOutCluster request structure.

    """

    def __init__(self):
        r"""
        :param InstanceChargeType: The node billing mode. Valid values:
<li>`POSTPAID_BY_HOUR`: The postpaid mode by hour.</li>
<li>`SPOTPAID`: The spot instance mode (for task nodes only).</li>
        :type InstanceChargeType: str
        :param InstanceId: The cluster instance ID.
        :type InstanceId: str
        :param ScaleOutNodeConfig: The type and number of nodes to be added.
        :type ScaleOutNodeConfig: :class:`tencentcloud.emr.v20190103.models.ScaleOutNodeConfig`
        :param ClientToken: A unique random token, which is valid for 5 minutes and needs to be specified by the caller to prevent the client from repeatedly creating resources. An example value is `a9a90aa6-751a-41b6-aad6-fae36063280`.
        :type ClientToken: str
        :param InstanceChargePrepaid: The details of the monthly subscription, including the instance period and auto-renewal. It is required if the `InstanceChargeType` is `PREPAID`.
        :type InstanceChargePrepaid: :class:`tencentcloud.emr.v20190103.models.InstanceChargePrepaid`
        :param ScriptBootstrapActionConfig: The [Bootstrap action](https://intl.cloud.tencent.com/document/product/589/35656?from_cn_redirect=1) script settings.
        :type ScriptBootstrapActionConfig: list of ScriptBootstrapActionConfig
        :param SoftDeployInfo: The services to be deployed for new nodes. By default, new nodes will inherit all services deployed for the current node type. Deployed services include default optional services. This parameter only supports optional services. For example, if `HDFS`, `YARN`, and `Impala` have been deployed for existing task nodes, only `HDFS` and `YARN` are passed in with this parameter if `Impala` is not deployed during the task node scale-out with API.
        :type SoftDeployInfo: list of int
        :param ServiceNodeInfo: The processes to be deployed. All processes for services to be added are deployed by default. Deployed processes can be changed. For example, `HDFS`, `YARN`, and `Impala` have been deployed for current task nodes, and default services are `DataNode`, `NodeManager`, and `ImpalaServer`; if you want to change deployed processes, you can set this parameter to `DataNode,NodeManager,ImpalaServerCoordinator` or `DataNode,NodeManager,ImpalaServerExecutor`.
        :type ServiceNodeInfo: list of int
        :param DisasterRecoverGroupIds: The list of spread placement group IDs. Only one can be specified.
You can call the [DescribeDisasterRecoverGroups](https://intl.cloud.tencent.com/document/product/213/17810?from_cn_redirect=1) API and obtain this parameter from the `DisasterRecoverGroupId` field in the response.
        :type DisasterRecoverGroupIds: list of str
        :param Tags: The list of tags bound to added nodes.
        :type Tags: list of Tag
        :param HardwareSourceType: The type of resources to add. Valid values: `host` (general CVM resources) and `pod` (resources provided by a TKE or EKS cluster).
        :type HardwareSourceType: str
        :param PodSpecInfo: The pod resource information.
        :type PodSpecInfo: :class:`tencentcloud.emr.v20190103.models.PodSpecInfo`
        :param ClickHouseClusterName: The server group name selected for ClickHouse cluster scale-out.
        :type ClickHouseClusterName: str
        :param ClickHouseClusterType: The server group type selected for ClickHouse cluster scale-out. Valid values: `new` (create a group) and `old` (select an existing group).
        :type ClickHouseClusterType: str
        :param YarnNodeLabel: The YARN node label specified for scale-out.
        :type YarnNodeLabel: str
        :param EnableStartServiceFlag: Whether to start services after scale-out.
<li>`true`: Yes</li>
<li>`false` (default): No</li>
        :type EnableStartServiceFlag: bool
        :param ResourceSpec: The spec settings.
        :type ResourceSpec: :class:`tencentcloud.emr.v20190103.models.NodeResourceSpec`
        :param Zone: The ID of the AZ where the instance resides, such as `ap-guangzhou-1`. You can call the [DescribeZones](https://intl.cloud.tencent.com/document/product/213/15707?from_cn_redirect=1) API and obtain this ID from the `Zone` field in the response.
        :type Zone: str
        :param SubnetId: The subnet, which defaults to the subnet used when the cluster is created.
        :type SubnetId: str
        """
        self.InstanceChargeType = None
        self.InstanceId = None
        self.ScaleOutNodeConfig = None
        self.ClientToken = None
        self.InstanceChargePrepaid = None
        self.ScriptBootstrapActionConfig = None
        self.SoftDeployInfo = None
        self.ServiceNodeInfo = None
        self.DisasterRecoverGroupIds = None
        self.Tags = None
        self.HardwareSourceType = None
        self.PodSpecInfo = None
        self.ClickHouseClusterName = None
        self.ClickHouseClusterType = None
        self.YarnNodeLabel = None
        self.EnableStartServiceFlag = None
        self.ResourceSpec = None
        self.Zone = None
        self.SubnetId = None


    def _deserialize(self, params):
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.InstanceId = params.get("InstanceId")
        if params.get("ScaleOutNodeConfig") is not None:
            self.ScaleOutNodeConfig = ScaleOutNodeConfig()
            self.ScaleOutNodeConfig._deserialize(params.get("ScaleOutNodeConfig"))
        self.ClientToken = params.get("ClientToken")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        if params.get("ScriptBootstrapActionConfig") is not None:
            self.ScriptBootstrapActionConfig = []
            for item in params.get("ScriptBootstrapActionConfig"):
                obj = ScriptBootstrapActionConfig()
                obj._deserialize(item)
                self.ScriptBootstrapActionConfig.append(obj)
        self.SoftDeployInfo = params.get("SoftDeployInfo")
        self.ServiceNodeInfo = params.get("ServiceNodeInfo")
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.HardwareSourceType = params.get("HardwareSourceType")
        if params.get("PodSpecInfo") is not None:
            self.PodSpecInfo = PodSpecInfo()
            self.PodSpecInfo._deserialize(params.get("PodSpecInfo"))
        self.ClickHouseClusterName = params.get("ClickHouseClusterName")
        self.ClickHouseClusterType = params.get("ClickHouseClusterType")
        self.YarnNodeLabel = params.get("YarnNodeLabel")
        self.EnableStartServiceFlag = params.get("EnableStartServiceFlag")
        if params.get("ResourceSpec") is not None:
            self.ResourceSpec = NodeResourceSpec()
            self.ResourceSpec._deserialize(params.get("ResourceSpec"))
        self.Zone = params.get("Zone")
        self.SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScaleOutClusterResponse(AbstractModel):
    """ScaleOutCluster response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: The instance ID.
        :type InstanceId: str
        :param ClientToken: The client token.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClientToken: str
        :param FlowId: The scale-out workflow ID.
Note: This field may return null, indicating that no valid values can be obtained.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.ClientToken = None
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ClientToken = params.get("ClientToken")
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ScaleOutInstanceRequest(AbstractModel):
    """ScaleOutInstance request structure.

    """

    def __init__(self):
        r"""
        :param TimeUnit: Time unit of scale-out. Valid values:
<li>s: Second. When `PayMode` is 0, `TimeUnit` can only be `s`.</li>
<li>m: Month. When `PayMode` is 1, `TimeUnit` can only be `m`.</li>
        :type TimeUnit: str
        :param TimeSpan: Time span of scale-out, which needs to be used together with `TimeUnit`.
        :type TimeSpan: int
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param PayMode: Instance billing mode. Valid value:
<li>0: Pay-as-you-go.</li>
        :type PayMode: int
        :param ClientToken: Client token.
        :type ClientToken: str
        :param PreExecutedFileSettings: Bootstrap script settings.
        :type PreExecutedFileSettings: list of PreExecuteFileSettings
        :param TaskCount: Number of task nodes to be added.
        :type TaskCount: int
        :param CoreCount: Number of core nodes to be added.
        :type CoreCount: int
        :param UnNecessaryNodeList: Processes unnecessary for scale-out.
        :type UnNecessaryNodeList: list of int non-negative
        :param RouterCount: Number of router nodes to be added.
        :type RouterCount: int
        :param SoftDeployInfo: Deployed service.
<li>`SoftDeployInfo` and `ServiceNodeInfo` are in the same group and mutually exclusive with `UnNecessaryNodeList`.</li>
<li>The combination of `SoftDeployInfo` and `ServiceNodeInfo` is recommended.</li>
        :type SoftDeployInfo: list of int non-negative
        :param ServiceNodeInfo: Started process.
        :type ServiceNodeInfo: list of int non-negative
        :param DisasterRecoverGroupIds: List of spread placement group IDs. Only one can be specified currently.
        :type DisasterRecoverGroupIds: list of str
        :param Tags: List of tags bound to added nodes.
        :type Tags: list of Tag
        :param HardwareResourceType: Resource type selected for scaling. Valid values: `host` (general CVM resource) and `pod` (resource provided by TKE or EKS cluster).
        :type HardwareResourceType: str
        :param PodSpec: Specified information such as pod specification and source for scale-out with pod resources.
        :type PodSpec: :class:`tencentcloud.emr.v20190103.models.PodSpec`
        :param ClickHouseClusterName: Server group name selected for ClickHouse cluster scale-out.
        :type ClickHouseClusterName: str
        :param ClickHouseClusterType: Server group type selected for ClickHouse cluster scale-out. Valid values: `new` (create a group) and `old` (select an existing group).
        :type ClickHouseClusterType: str
        :param YarnNodeLabel: Yarn node label specified for rule-based scale-out.
        :type YarnNodeLabel: str
        :param PodParameter: Custom pod permission and parameter
        :type PodParameter: :class:`tencentcloud.emr.v20190103.models.PodParameter`
        :param MasterCount: Number of master nodes to be added.
When a ClickHouse cluster is scaled, this parameter does not take effect.
When a Kafka cluster is scaled, this parameter does not take effect.
When `HardwareResourceType` is `pod`, this parameter does not take effect.
        :type MasterCount: int
        :param StartServiceAfterScaleOut: Whether to start the service after scale-out. `true`: Yes; `false`: No.
        :type StartServiceAfterScaleOut: str
        :param ZoneId: AZ, which defaults to the primary AZ of the cluster.
        :type ZoneId: int
        :param SubnetId: Subnet, which defaults to the subnet used when the cluster is created.
        :type SubnetId: str
        :param ScaleOutServiceConfAssign: Pre-defined configuration set
        :type ScaleOutServiceConfAssign: str
        :param AutoRenew: Whether to enable auto-renewal. Valid values: `0` (no), `1` (yes).
        :type AutoRenew: int
        """
        self.TimeUnit = None
        self.TimeSpan = None
        self.InstanceId = None
        self.PayMode = None
        self.ClientToken = None
        self.PreExecutedFileSettings = None
        self.TaskCount = None
        self.CoreCount = None
        self.UnNecessaryNodeList = None
        self.RouterCount = None
        self.SoftDeployInfo = None
        self.ServiceNodeInfo = None
        self.DisasterRecoverGroupIds = None
        self.Tags = None
        self.HardwareResourceType = None
        self.PodSpec = None
        self.ClickHouseClusterName = None
        self.ClickHouseClusterType = None
        self.YarnNodeLabel = None
        self.PodParameter = None
        self.MasterCount = None
        self.StartServiceAfterScaleOut = None
        self.ZoneId = None
        self.SubnetId = None
        self.ScaleOutServiceConfAssign = None
        self.AutoRenew = None


    def _deserialize(self, params):
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        self.InstanceId = params.get("InstanceId")
        self.PayMode = params.get("PayMode")
        self.ClientToken = params.get("ClientToken")
        if params.get("PreExecutedFileSettings") is not None:
            self.PreExecutedFileSettings = []
            for item in params.get("PreExecutedFileSettings"):
                obj = PreExecuteFileSettings()
                obj._deserialize(item)
                self.PreExecutedFileSettings.append(obj)
        self.TaskCount = params.get("TaskCount")
        self.CoreCount = params.get("CoreCount")
        self.UnNecessaryNodeList = params.get("UnNecessaryNodeList")
        self.RouterCount = params.get("RouterCount")
        self.SoftDeployInfo = params.get("SoftDeployInfo")
        self.ServiceNodeInfo = params.get("ServiceNodeInfo")
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.HardwareResourceType = params.get("HardwareResourceType")
        if params.get("PodSpec") is not None:
            self.PodSpec = PodSpec()
            self.PodSpec._deserialize(params.get("PodSpec"))
        self.ClickHouseClusterName = params.get("ClickHouseClusterName")
        self.ClickHouseClusterType = params.get("ClickHouseClusterType")
        self.YarnNodeLabel = params.get("YarnNodeLabel")
        if params.get("PodParameter") is not None:
            self.PodParameter = PodParameter()
            self.PodParameter._deserialize(params.get("PodParameter"))
        self.MasterCount = params.get("MasterCount")
        self.StartServiceAfterScaleOut = params.get("StartServiceAfterScaleOut")
        self.ZoneId = params.get("ZoneId")
        self.SubnetId = params.get("SubnetId")
        self.ScaleOutServiceConfAssign = params.get("ScaleOutServiceConfAssign")
        self.AutoRenew = params.get("AutoRenew")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScaleOutInstanceResponse(AbstractModel):
    """ScaleOutInstance response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param DealNames: Order number.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DealNames: list of str
        :param ClientToken: Client token.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClientToken: str
        :param FlowId: Scale-out workflow ID.
Note: This field may return null, indicating that no valid values can be obtained.
        :type FlowId: int
        :param BillId: Big order ID.
Note: This field may return null, indicating that no valid values can be obtained.
        :type BillId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.DealNames = None
        self.ClientToken = None
        self.FlowId = None
        self.BillId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DealNames = params.get("DealNames")
        self.ClientToken = params.get("ClientToken")
        self.FlowId = params.get("FlowId")
        self.BillId = params.get("BillId")
        self.RequestId = params.get("RequestId")


class ScaleOutNodeConfig(AbstractModel):
    """The type and number of nodes to be added.

    """

    def __init__(self):
        r"""
        :param NodeFlag: Valid values of node type:
  <li>MASTER</li>
  <li>TASK</li>
  <li>CORE</li>
  <li>ROUTER</li>
        :type NodeFlag: str
        :param NodeCount: The number of nodes.
        :type NodeCount: int
        """
        self.NodeFlag = None
        self.NodeCount = None


    def _deserialize(self, params):
        self.NodeFlag = params.get("NodeFlag")
        self.NodeCount = params.get("NodeCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SceneSoftwareConfig(AbstractModel):
    """The configuration of cluster application scenario and supported components.

    """

    def __init__(self):
        r"""
        :param Software: The list of deployed components. The list of component options varies by `ProductVersion` (EMR version). For more information, see [Component Version](https://intl.cloud.tencent.com/document/product/589/20279?from_cn_redirect=1).
The instance type, `hive` or `flink`.
        :type Software: list of str
        :param SceneName: The scenario name, which defaults to `Hadoop-Default`. For more details, see [here](https://intl.cloud.tencent.com/document/product/589/14624?from_cn_redirect=1). Valid values:
Hadoop-Kudu
Hadoop-Zookeeper
Hadoop-Presto
Hadoop-Hbase
Hadoop-Default
        :type SceneName: str
        """
        self.Software = None
        self.SceneName = None


    def _deserialize(self, params):
        self.Software = params.get("Software")
        self.SceneName = params.get("SceneName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScriptBootstrapActionConfig(AbstractModel):
    """The bootstrap action.

    """

    def __init__(self):
        r"""
        :param CosFileURI: The COS URL of the script, in the format of `https://beijing-111111.cos.ap-beijing.myqcloud.com/data/test.sh`. For the COS bucket list, see [Bucket List](https://console.cloud.tencent.com/cos/bucket).
        :type CosFileURI: str
        :param ExecutionMoment: The execution time of the bootstrap action script. Valid values:
<li>`resourceAfter`: After node initialization</li>
<li>`clusterAfter`: After cluster start</li>
<li>`clusterBefore`: Before cluster start</li>
        :type ExecutionMoment: str
        :param Args: The execution script parameter. The parameter format must comply with standard shell specifications.
        :type Args: list of str
        :param CosFileName: The script file name.
        :type CosFileName: str
        """
        self.CosFileURI = None
        self.ExecutionMoment = None
        self.Args = None
        self.CosFileName = None


    def _deserialize(self, params):
        self.CosFileURI = params.get("CosFileURI")
        self.ExecutionMoment = params.get("ExecutionMoment")
        self.Args = params.get("Args")
        self.CosFileName = params.get("CosFileName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SearchItem(AbstractModel):
    """Search field

    """

    def __init__(self):
        r"""
        :param SearchType: Searchable type
        :type SearchType: str
        :param SearchValue: Searchable value
        :type SearchValue: str
        """
        self.SearchType = None
        self.SearchValue = None


    def _deserialize(self, params):
        self.SearchType = params.get("SearchType")
        self.SearchValue = params.get("SearchValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServiceBasicRestartInfo(AbstractModel):
    """The services to operate on

    """

    def __init__(self):
        r"""
        :param ServiceName: The service name (required), such as HDFS.
        :type ServiceName: str
        :param ComponentInfoList: If it is left empty, all processes will be operated on.
        :type ComponentInfoList: list of ComponentBasicRestartInfo
        """
        self.ServiceName = None
        self.ComponentInfoList = None


    def _deserialize(self, params):
        self.ServiceName = params.get("ServiceName")
        if params.get("ComponentInfoList") is not None:
            self.ComponentInfoList = []
            for item in params.get("ComponentInfoList"):
                obj = ComponentBasicRestartInfo()
                obj._deserialize(item)
                self.ComponentInfoList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ShortNodeInfo(AbstractModel):
    """Node information

    """

    def __init__(self):
        r"""
        :param NodeType: Node type: Master/Core/Task/Router/Common
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type NodeType: str
        :param NodeSize: Number of nodes
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type NodeSize: int
        """
        self.NodeType = None
        self.NodeSize = None


    def _deserialize(self, params):
        self.NodeType = params.get("NodeType")
        self.NodeSize = params.get("NodeSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SoftDependInfo(AbstractModel):
    """Client component dependencies

    """

    def __init__(self):
        r"""
        :param SoftName: The component name.
        :type SoftName: str
        :param Required: Whether the component is required.
        :type Required: bool
        """
        self.SoftName = None
        self.Required = None


    def _deserialize(self, params):
        self.SoftName = params.get("SoftName")
        self.Required = params.get("Required")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartStopServiceOrMonitorRequest(AbstractModel):
    """StartStopServiceOrMonitor request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: The cluster ID.
        :type InstanceId: str
        :param OpType: The operation type. Valid values:
<li>StartService: Start service</li>
<li>StopService: Stop service</li>
<li>StartMonitor: Start maintenance</li>
<li>StopMonitor: Stop maintenance</li>
<li>RestartService: Restart service. If this type is selected, "StrategyConfig" is required.</li>
        :type OpType: str
        :param OpScope: The operation scope.
        :type OpScope: :class:`tencentcloud.emr.v20190103.models.OpScope`
        :param StrategyConfig: The operation policy.
        :type StrategyConfig: :class:`tencentcloud.emr.v20190103.models.StrategyConfig`
        """
        self.InstanceId = None
        self.OpType = None
        self.OpScope = None
        self.StrategyConfig = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.OpType = params.get("OpType")
        if params.get("OpScope") is not None:
            self.OpScope = OpScope()
            self.OpScope._deserialize(params.get("OpScope"))
        if params.get("StrategyConfig") is not None:
            self.StrategyConfig = StrategyConfig()
            self.StrategyConfig._deserialize(params.get("StrategyConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartStopServiceOrMonitorResponse(AbstractModel):
    """StartStopServiceOrMonitor response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StrategyConfig(AbstractModel):
    """Restart, stop, or start of service/monitoring configurations

    """

    def __init__(self):
        r"""
        :param RollingRestartSwitch: `0`: Disable rolling restart
`1`: Enable rolling restart
Note: This field may return null, indicating that no valid values can be obtained.
        :type RollingRestartSwitch: int
        :param BatchSize: The number of nodes to be restarted per batch in rolling restart, with a maximum value of 99,999.
Note: This field may return null, indicating that no valid values can be obtained.
        :type BatchSize: int
        :param TimeWait: The wait time (in seconds) per batch in rolling restart, with a maximum value of 5 minutes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type TimeWait: int
        :param DealOnFail: The failure handling policy. Valid values: `0` (blocks the process) and `1` (skips).
Note: This field may return null, indicating that no valid values can be obtained.
        :type DealOnFail: int
        """
        self.RollingRestartSwitch = None
        self.BatchSize = None
        self.TimeWait = None
        self.DealOnFail = None


    def _deserialize(self, params):
        self.RollingRestartSwitch = params.get("RollingRestartSwitch")
        self.BatchSize = params.get("BatchSize")
        self.TimeWait = params.get("TimeWait")
        self.DealOnFail = params.get("DealOnFail")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubnetInfo(AbstractModel):
    """Subnet information

    """

    def __init__(self):
        r"""
        :param SubnetName: Subnet information (name)
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type SubnetName: str
        :param SubnetId: Subnet information (ID)
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type SubnetId: str
        """
        self.SubnetName = None
        self.SubnetId = None


    def _deserialize(self, params):
        self.SubnetName = params.get("SubnetName")
        self.SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Tag(AbstractModel):
    """Tag

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
        


class TerminateClusterNodesRequest(AbstractModel):
    """TerminateClusterNodes request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: The instance ID.
        :type InstanceId: str
        :param CvmInstanceIds: The list of resources to be terminated.
        :type CvmInstanceIds: list of str
        :param NodeFlag: Valid values of node type:
  <li>MASTER</li>
  <li>TASK</li>
  <li>CORE</li>
  <li>ROUTER</li>
        :type NodeFlag: str
        :param GraceDownFlag: The graceful scale-in feature. Valid values:
  <li>`true`: Enabled.</li>
  <li>`false`: Disabled.</li>
        :type GraceDownFlag: bool
        :param GraceDownTime: The graceful scale-in wait time in seconds. Value range: 60–1800.
        :type GraceDownTime: int
        """
        self.InstanceId = None
        self.CvmInstanceIds = None
        self.NodeFlag = None
        self.GraceDownFlag = None
        self.GraceDownTime = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.CvmInstanceIds = params.get("CvmInstanceIds")
        self.NodeFlag = params.get("NodeFlag")
        self.GraceDownFlag = params.get("GraceDownFlag")
        self.GraceDownTime = params.get("GraceDownTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateClusterNodesResponse(AbstractModel):
    """TerminateClusterNodes response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: The scale-in process ID.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class TerminateInstanceRequest(AbstractModel):
    """TerminateInstance request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param ResourceIds: ID of terminated node. This parameter is reserved and does not need to be configured.
        :type ResourceIds: list of str
        """
        self.InstanceId = None
        self.ResourceIds = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ResourceIds = params.get("ResourceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateInstanceResponse(AbstractModel):
    """TerminateInstance response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class TerminateTasksRequest(AbstractModel):
    """TerminateTasks request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param ResourceIds: List of resource IDs of the node to be terminated. The resource ID is in the format of `emr-vm-xxxxxxxx`. A valid resource ID can be queried in the [console](https://console.cloud.tencent.com/emr/static/hardware).
        :type ResourceIds: list of str
        """
        self.InstanceId = None
        self.ResourceIds = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ResourceIds = params.get("ResourceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateTasksResponse(AbstractModel):
    """TerminateTasks response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class TopologyInfo(AbstractModel):
    """Cluster node topology information

    """

    def __init__(self):
        r"""
        :param ZoneId: AZ ID
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type ZoneId: int
        :param Zone: AZ information
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type Zone: str
        :param SubnetInfoList: Subnet information
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type SubnetInfoList: list of SubnetInfo
        :param NodeInfoList: Node information
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type NodeInfoList: list of ShortNodeInfo
        """
        self.ZoneId = None
        self.Zone = None
        self.SubnetInfoList = None
        self.NodeInfoList = None


    def _deserialize(self, params):
        self.ZoneId = params.get("ZoneId")
        self.Zone = params.get("Zone")
        if params.get("SubnetInfoList") is not None:
            self.SubnetInfoList = []
            for item in params.get("SubnetInfoList"):
                obj = SubnetInfo()
                obj._deserialize(item)
                self.SubnetInfoList.append(obj)
        if params.get("NodeInfoList") is not None:
            self.NodeInfoList = []
            for item in params.get("NodeInfoList"):
                obj = ShortNodeInfo()
                obj._deserialize(item)
                self.NodeInfoList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateInstanceSettings(AbstractModel):
    """Target resource specification

    """

    def __init__(self):
        r"""
        :param Memory: Memory capacity in GB
        :type Memory: int
        :param CPUCores: Number of CPU cores
        :type CPUCores: int
        :param ResourceId: Machine resource ID (EMR resource identifier)
        :type ResourceId: str
        :param InstanceType: Target machine specification
        :type InstanceType: str
        """
        self.Memory = None
        self.CPUCores = None
        self.ResourceId = None
        self.InstanceType = None


    def _deserialize(self, params):
        self.Memory = params.get("Memory")
        self.CPUCores = params.get("CPUCores")
        self.ResourceId = params.get("ResourceId")
        self.InstanceType = params.get("InstanceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserInfoForUserManager(AbstractModel):
    """Added user information list

    """

    def __init__(self):
        r"""
        :param UserName: Username
        :type UserName: str
        :param UserGroup: The group to which the user belongs
        :type UserGroup: str
        :param PassWord: 
        :type PassWord: str
        :param ReMark: 
        :type ReMark: str
        """
        self.UserName = None
        self.UserGroup = None
        self.PassWord = None
        self.ReMark = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.UserGroup = params.get("UserGroup")
        self.PassWord = params.get("PassWord")
        self.ReMark = params.get("ReMark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserManagerFilter(AbstractModel):
    """User management list filter

    """

    def __init__(self):
        r"""
        :param UserName: Username
Note: This field may return null, indicating that no valid value can be obtained.
        :type UserName: str
        """
        self.UserName = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserManagerUserBriefInfo(AbstractModel):
    """Brief user information in user management

    """

    def __init__(self):
        r"""
        :param UserName: Username
        :type UserName: str
        :param UserGroup: The group to which the user belongs
        :type UserGroup: str
        :param UserType: `Manager` represents an admin, and `NormalUser` represents a general user.
        :type UserType: str
        :param CreateTime: Account creation time
Note: This field may return null, indicating that no valid value can be obtained.
        :type CreateTime: str
        :param SupportDownLoadKeyTab: Whether the corresponding Keytab file of the user is available for download. This parameter applies only to a Kerberos-enabled cluster.
        :type SupportDownLoadKeyTab: bool
        :param DownLoadKeyTabUrl: Download link of the Keytab file
Note: This field may return null, indicating that no valid value can be obtained.
        :type DownLoadKeyTabUrl: str
        """
        self.UserName = None
        self.UserGroup = None
        self.UserType = None
        self.CreateTime = None
        self.SupportDownLoadKeyTab = None
        self.DownLoadKeyTabUrl = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.UserGroup = params.get("UserGroup")
        self.UserType = params.get("UserType")
        self.CreateTime = params.get("CreateTime")
        self.SupportDownLoadKeyTab = params.get("SupportDownLoadKeyTab")
        self.DownLoadKeyTabUrl = params.get("DownLoadKeyTabUrl")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VPCSettings(AbstractModel):
    """VPC parameters

    """

    def __init__(self):
        r"""
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: Subnet ID
        :type SubnetId: str
        """
        self.VpcId = None
        self.SubnetId = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VirtualPrivateCloud(AbstractModel):
    """VPC parameters

    """

    def __init__(self):
        r"""
        :param VpcId: The VPC ID.
        :type VpcId: str
        :param SubnetId: The subnet ID.
        :type SubnetId: str
        """
        self.VpcId = None
        self.SubnetId = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ZoneDetailPriceResult(AbstractModel):
    """Price details by AZ, used for creating the cluster price list

    """

    def __init__(self):
        r"""
        :param ZoneId: AZ ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type ZoneId: str
        :param NodeDetailPrice: Price details by node
        :type NodeDetailPrice: list of NodeDetailPriceResult
        """
        self.ZoneId = None
        self.NodeDetailPrice = None


    def _deserialize(self, params):
        self.ZoneId = params.get("ZoneId")
        if params.get("NodeDetailPrice") is not None:
            self.NodeDetailPrice = []
            for item in params.get("NodeDetailPrice"):
                obj = NodeDetailPriceResult()
                obj._deserialize(item)
                self.NodeDetailPrice.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ZoneResourceConfiguration(AbstractModel):
    """AZ configurations

    """

    def __init__(self):
        r"""
        :param VirtualPrivateCloud: The VPC configuration information. This parameter is used to specify the VPC ID, subnet ID and other information.
Note: This field may return null, indicating that no valid values can be obtained.
        :type VirtualPrivateCloud: :class:`tencentcloud.emr.v20190103.models.VirtualPrivateCloud`
        :param Placement: The instance location. This parameter is used to specify the AZ, project, and other attributes of the instance.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Placement: :class:`tencentcloud.emr.v20190103.models.Placement`
        :param AllNodeResourceSpec: The specs of all nodes.
Note: This field may return null, indicating that no valid values can be obtained.
        :type AllNodeResourceSpec: :class:`tencentcloud.emr.v20190103.models.AllNodeResourceSpec`
        :param ZoneTag: For a single AZ, `ZoneTag` can be left out. For a double-AZ mode, `ZoneTag` is set to `master` and `standby` for the first and second AZs, respectively. If there are three AZs, `ZoneTag` is set to `master`, `standby`, and `third-party` for the first, second, and third AZs, respectively. Valid values:
  <li>master</li>
  <li>standby</li>
  <li>third-party</li>
Note: This field may return null, indicating that no valid values can be obtained.
        :type ZoneTag: str
        """
        self.VirtualPrivateCloud = None
        self.Placement = None
        self.AllNodeResourceSpec = None
        self.ZoneTag = None


    def _deserialize(self, params):
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        if params.get("AllNodeResourceSpec") is not None:
            self.AllNodeResourceSpec = AllNodeResourceSpec()
            self.AllNodeResourceSpec._deserialize(params.get("AllNodeResourceSpec"))
        self.ZoneTag = params.get("ZoneTag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        