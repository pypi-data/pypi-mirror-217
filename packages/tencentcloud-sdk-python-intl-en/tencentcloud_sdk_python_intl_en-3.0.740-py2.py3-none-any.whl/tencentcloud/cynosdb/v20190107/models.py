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


class Ability(AbstractModel):
    """Features supported by the cluster

    """

    def __init__(self):
        r"""
        :param IsSupportSlaveZone: Whether secondary AZ is supported
        :type IsSupportSlaveZone: str
        :param NonsupportSlaveZoneReason: The reason why secondary AZ is not supported
Note: This field may return null, indicating that no valid values can be obtained.
        :type NonsupportSlaveZoneReason: str
        :param IsSupportRo: Whether read-only instance is supported
        :type IsSupportRo: str
        :param NonsupportRoReason: The reason why read-only instance is not supported
Note: This field may return null, indicating that no valid values can be obtained.
        :type NonsupportRoReason: str
        """
        self.IsSupportSlaveZone = None
        self.NonsupportSlaveZoneReason = None
        self.IsSupportRo = None
        self.NonsupportRoReason = None


    def _deserialize(self, params):
        self.IsSupportSlaveZone = params.get("IsSupportSlaveZone")
        self.NonsupportSlaveZoneReason = params.get("NonsupportSlaveZoneReason")
        self.IsSupportRo = params.get("IsSupportRo")
        self.NonsupportRoReason = params.get("NonsupportRoReason")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Account(AbstractModel):
    """Database account information

    """

    def __init__(self):
        r"""
        :param AccountName: Database account name
        :type AccountName: str
        :param Description: Database account description
        :type Description: str
        :param CreateTime: Creation time
        :type CreateTime: str
        :param UpdateTime: Update time
        :type UpdateTime: str
        :param Host: Host
        :type Host: str
        :param MaxUserConnections: The max connections
        :type MaxUserConnections: int
        """
        self.AccountName = None
        self.Description = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Host = None
        self.MaxUserConnections = None


    def _deserialize(self, params):
        self.AccountName = params.get("AccountName")
        self.Description = params.get("Description")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Host = params.get("Host")
        self.MaxUserConnections = params.get("MaxUserConnections")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActivateInstanceRequest(AbstractModel):
    """ActivateInstance request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param InstanceIdList: List of instance IDs in the format of `cynosdbmysql-ins-n7ocdslw` as displayed in the TDSQL-C for MySQL console. You can use the instance list querying API to query the ID, i.e., the `InstanceId` value in the output parameters.
        :type InstanceIdList: list of str
        """
        self.ClusterId = None
        self.InstanceIdList = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIdList = params.get("InstanceIdList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActivateInstanceResponse(AbstractModel):
    """ActivateInstance response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task flow ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class AddClusterSlaveZoneRequest(AbstractModel):
    """AddClusterSlaveZone request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param SlaveZone: Replica AZ
        :type SlaveZone: str
        """
        self.ClusterId = None
        self.SlaveZone = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.SlaveZone = params.get("SlaveZone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddClusterSlaveZoneResponse(AbstractModel):
    """AddClusterSlaveZone response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async FlowId
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class AddInstancesRequest(AbstractModel):
    """AddInstances request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param Cpu: Number of CPU cores
        :type Cpu: int
        :param Memory: Memory in GB
        :type Memory: int
        :param ReadOnlyCount: Number of added read-only instances. Value range: (0,16].
        :type ReadOnlyCount: int
        :param InstanceGrpId: Instance group ID, which will be used when you add an instance in an existing RO group. If this parameter is left empty, an RO group will be created. But it is not recommended to pass in this parameter for the current version, as this version has been disused.
        :type InstanceGrpId: str
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: Subnet ID. If `VpcId` is set, `SubnetId` is required.
        :type SubnetId: str
        :param Port: The port used when adding an RO group. Value range: [0,65535).
        :type Port: int
        :param InstanceName: Instance name. String length range: [0,64).
        :type InstanceName: str
        :param AutoVoucher: Whether to automatically select a voucher. 1: yes; 0: no. Default value: 0
        :type AutoVoucher: int
        :param DbType: Database type. Valid values: 
<li> MYSQL </li>
        :type DbType: str
        :param OrderSource: Order source. String length range: [0,64).
        :type OrderSource: str
        :param DealMode: Transaction mode. Valid values: `0` (place and pay for an order), `1` (place an order)
        :type DealMode: int
        :param ParamTemplateId: Parameter template ID
        :type ParamTemplateId: int
        :param InstanceParams: Parameter list, which is valid only if `InstanceParams` is passed in to `ParamTemplateId`.
        :type InstanceParams: list of ModifyParamItem
        :param SecurityGroupIds: Security group ID. You can specify an security group when creating a read-only instance.
        :type SecurityGroupIds: list of str
        """
        self.ClusterId = None
        self.Cpu = None
        self.Memory = None
        self.ReadOnlyCount = None
        self.InstanceGrpId = None
        self.VpcId = None
        self.SubnetId = None
        self.Port = None
        self.InstanceName = None
        self.AutoVoucher = None
        self.DbType = None
        self.OrderSource = None
        self.DealMode = None
        self.ParamTemplateId = None
        self.InstanceParams = None
        self.SecurityGroupIds = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.ReadOnlyCount = params.get("ReadOnlyCount")
        self.InstanceGrpId = params.get("InstanceGrpId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Port = params.get("Port")
        self.InstanceName = params.get("InstanceName")
        self.AutoVoucher = params.get("AutoVoucher")
        self.DbType = params.get("DbType")
        self.OrderSource = params.get("OrderSource")
        self.DealMode = params.get("DealMode")
        self.ParamTemplateId = params.get("ParamTemplateId")
        if params.get("InstanceParams") is not None:
            self.InstanceParams = []
            for item in params.get("InstanceParams"):
                obj = ModifyParamItem()
                obj._deserialize(item)
                self.InstanceParams.append(obj)
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddInstancesResponse(AbstractModel):
    """AddInstances response structure.

    """

    def __init__(self):
        r"""
        :param TranId: Freezing transaction. One freezing transaction ID is generated each time an instance is added.
Note: this field may return null, indicating that no valid values can be obtained.
        :type TranId: str
        :param DealNames: Pay-as-You-Go order ID.
Note: this field may return null, indicating that no valid values can be obtained.
        :type DealNames: list of str
        :param ResourceIds: List of IDs of delivered resources
Note: this field may return null, indicating that no valid values can be obtained.
        :type ResourceIds: list of str
        :param BigDealIds: Big order ID.
Note: this field may return null, indicating that no valid values can be obtained.
        :type BigDealIds: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TranId = None
        self.DealNames = None
        self.ResourceIds = None
        self.BigDealIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TranId = params.get("TranId")
        self.DealNames = params.get("DealNames")
        self.ResourceIds = params.get("ResourceIds")
        self.BigDealIds = params.get("BigDealIds")
        self.RequestId = params.get("RequestId")


class Addr(AbstractModel):
    """Database address

    """

    def __init__(self):
        r"""
        :param IP: IP
        :type IP: str
        :param Port: Port
        :type Port: int
        """
        self.IP = None
        self.Port = None


    def _deserialize(self, params):
        self.IP = params.get("IP")
        self.Port = params.get("Port")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AuditRuleFilters(AbstractModel):
    """Filter of rule audit

    """

    def __init__(self):
        r"""
        :param RuleFilters: Audit rule
        :type RuleFilters: list of RuleFilters
        """
        self.RuleFilters = None


    def _deserialize(self, params):
        if params.get("RuleFilters") is not None:
            self.RuleFilters = []
            for item in params.get("RuleFilters"):
                obj = RuleFilters()
                obj._deserialize(item)
                self.RuleFilters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AuditRuleTemplateInfo(AbstractModel):
    """Details of an audit rule template

    """

    def __init__(self):
        r"""
        :param RuleTemplateId: Rule template ID
        :type RuleTemplateId: str
        :param RuleTemplateName: Rule template name
        :type RuleTemplateName: str
        :param RuleFilters: Filter of the rule template
        :type RuleFilters: list of RuleFilters
        :param Description: Description of a rule template
Note: This field may return null, indicating that no valid values can be obtained.
        :type Description: str
        :param CreateAt: Creation time of a rule template
        :type CreateAt: str
        """
        self.RuleTemplateId = None
        self.RuleTemplateName = None
        self.RuleFilters = None
        self.Description = None
        self.CreateAt = None


    def _deserialize(self, params):
        self.RuleTemplateId = params.get("RuleTemplateId")
        self.RuleTemplateName = params.get("RuleTemplateName")
        if params.get("RuleFilters") is not None:
            self.RuleFilters = []
            for item in params.get("RuleFilters"):
                obj = RuleFilters()
                obj._deserialize(item)
                self.RuleFilters.append(obj)
        self.Description = params.get("Description")
        self.CreateAt = params.get("CreateAt")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BackupFileInfo(AbstractModel):
    """Backup file information

    """

    def __init__(self):
        r"""
        :param SnapshotId: Snapshot file ID, which is deprecated. You need to use `BackupId`.
        :type SnapshotId: int
        :param FileName: Backup file name
        :type FileName: str
        :param FileSize: Backup file size
        :type FileSize: int
        :param StartTime: Backup start time
        :type StartTime: str
        :param FinishTime: Backup end time
        :type FinishTime: str
        :param BackupType: Backup type. Valid values: `snapshot` (snapshot backup), `logic` (logic backup).
        :type BackupType: str
        :param BackupMethod: Back mode. auto: auto backup; manual: manual backup
        :type BackupMethod: str
        :param BackupStatus: Backup file status. success: backup succeeded; fail: backup failed; creating: creating backup file; deleting: deleting backup file
        :type BackupStatus: str
        :param SnapshotTime: Backup file time
        :type SnapshotTime: str
        :param BackupId: Backup ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type BackupId: int
        :param SnapShotType: 
        :type SnapShotType: str
        :param BackupName: Backup file alias
Note: This field may return null, indicating that no valid values can be obtained.
        :type BackupName: str
        """
        self.SnapshotId = None
        self.FileName = None
        self.FileSize = None
        self.StartTime = None
        self.FinishTime = None
        self.BackupType = None
        self.BackupMethod = None
        self.BackupStatus = None
        self.SnapshotTime = None
        self.BackupId = None
        self.SnapShotType = None
        self.BackupName = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.FileName = params.get("FileName")
        self.FileSize = params.get("FileSize")
        self.StartTime = params.get("StartTime")
        self.FinishTime = params.get("FinishTime")
        self.BackupType = params.get("BackupType")
        self.BackupMethod = params.get("BackupMethod")
        self.BackupStatus = params.get("BackupStatus")
        self.SnapshotTime = params.get("SnapshotTime")
        self.BackupId = params.get("BackupId")
        self.SnapShotType = params.get("SnapShotType")
        self.BackupName = params.get("BackupName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BillingResourceInfo(AbstractModel):
    """Billable resource information

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param InstanceIds: Instance ID list
        :type InstanceIds: list of str
        :param DealName: Order ID
        :type DealName: str
        """
        self.ClusterId = None
        self.InstanceIds = None
        self.DealName = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIds = params.get("InstanceIds")
        self.DealName = params.get("DealName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BinlogItem(AbstractModel):
    """Binlog description

    """

    def __init__(self):
        r"""
        :param FileName: Binlog filename
        :type FileName: str
        :param FileSize: File size in bytes
        :type FileSize: int
        :param StartTime: Transaction start time
        :type StartTime: str
        :param FinishTime: Transaction end time
        :type FinishTime: str
        :param BinlogId: Binlog file ID
        :type BinlogId: int
        """
        self.FileName = None
        self.FileSize = None
        self.StartTime = None
        self.FinishTime = None
        self.BinlogId = None


    def _deserialize(self, params):
        self.FileName = params.get("FileName")
        self.FileSize = params.get("FileSize")
        self.StartTime = params.get("StartTime")
        self.FinishTime = params.get("FinishTime")
        self.BinlogId = params.get("BinlogId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CloseAuditServiceRequest(AbstractModel):
    """CloseAuditService request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
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
        


class CloseAuditServiceResponse(AbstractModel):
    """CloseAuditService response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ClusterInstanceDetail(AbstractModel):
    """Cluster instance information

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param InstanceName: Instance name
        :type InstanceName: str
        :param InstanceType: Engine type
        :type InstanceType: str
        :param InstanceStatus: Instance status
        :type InstanceStatus: str
        :param InstanceStatusDesc: Instance status description
        :type InstanceStatusDesc: str
        :param InstanceCpu: Number of CPU cores
        :type InstanceCpu: int
        :param InstanceMemory: Memory
        :type InstanceMemory: int
        :param InstanceStorage: Disk
        :type InstanceStorage: int
        :param InstanceRole: Instance role
        :type InstanceRole: str
        """
        self.InstanceId = None
        self.InstanceName = None
        self.InstanceType = None
        self.InstanceStatus = None
        self.InstanceStatusDesc = None
        self.InstanceCpu = None
        self.InstanceMemory = None
        self.InstanceStorage = None
        self.InstanceRole = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.InstanceType = params.get("InstanceType")
        self.InstanceStatus = params.get("InstanceStatus")
        self.InstanceStatusDesc = params.get("InstanceStatusDesc")
        self.InstanceCpu = params.get("InstanceCpu")
        self.InstanceMemory = params.get("InstanceMemory")
        self.InstanceStorage = params.get("InstanceStorage")
        self.InstanceRole = params.get("InstanceRole")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAccountsRequest(AbstractModel):
    """CreateAccounts request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param Accounts: List of new accounts
        :type Accounts: list of NewAccount
        """
        self.ClusterId = None
        self.Accounts = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        if params.get("Accounts") is not None:
            self.Accounts = []
            for item in params.get("Accounts"):
                obj = NewAccount()
                obj._deserialize(item)
                self.Accounts.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAccountsResponse(AbstractModel):
    """CreateAccounts response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateAuditRuleTemplateRequest(AbstractModel):
    """CreateAuditRuleTemplate request structure.

    """

    def __init__(self):
        r"""
        :param RuleFilters: Audit rule
        :type RuleFilters: list of RuleFilters
        :param RuleTemplateName: Rule template name
        :type RuleTemplateName: str
        :param Description: Rule template description.
        :type Description: str
        """
        self.RuleFilters = None
        self.RuleTemplateName = None
        self.Description = None


    def _deserialize(self, params):
        if params.get("RuleFilters") is not None:
            self.RuleFilters = []
            for item in params.get("RuleFilters"):
                obj = RuleFilters()
                obj._deserialize(item)
                self.RuleFilters.append(obj)
        self.RuleTemplateName = params.get("RuleTemplateName")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAuditRuleTemplateResponse(AbstractModel):
    """CreateAuditRuleTemplate response structure.

    """

    def __init__(self):
        r"""
        :param RuleTemplateId: The generated rule template ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type RuleTemplateId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RuleTemplateId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.RuleTemplateId = params.get("RuleTemplateId")
        self.RequestId = params.get("RequestId")


class CreateBackupRequest(AbstractModel):
    """CreateBackup request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param BackupType: Backup type. Valid values: `logic` (logic backup), `snapshot` (physical backup)
        :type BackupType: str
        :param BackupDatabases: Backup database, which is valid when `BackupType` is `logic`.
        :type BackupDatabases: list of str
        :param BackupTables: Backup table, which is valid when `BackupType` is `logic`.
        :type BackupTables: list of DatabaseTables
        :param BackupName: Backup name
        :type BackupName: str
        """
        self.ClusterId = None
        self.BackupType = None
        self.BackupDatabases = None
        self.BackupTables = None
        self.BackupName = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.BackupType = params.get("BackupType")
        self.BackupDatabases = params.get("BackupDatabases")
        if params.get("BackupTables") is not None:
            self.BackupTables = []
            for item in params.get("BackupTables"):
                obj = DatabaseTables()
                obj._deserialize(item)
                self.BackupTables.append(obj)
        self.BackupName = params.get("BackupName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBackupResponse(AbstractModel):
    """CreateBackup response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task flow ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class CreateClustersRequest(AbstractModel):
    """CreateClusters request structure.

    """

    def __init__(self):
        r"""
        :param Zone: AZ
        :type Zone: str
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: Subnet ID
        :type SubnetId: str
        :param DbType: Database type. Valid values: 
<li> MYSQL </li>
        :type DbType: str
        :param DbVersion: Database version. Valid values: 
<li> Valid values for `MYSQL`: 5.7 and 8.0 </li>
        :type DbVersion: str
        :param ProjectId: Project ID.
        :type ProjectId: int
        :param Cpu: It is required when `DbMode` is set to `NORMAL` or left empty.
Number of CPU cores of normal instance
        :type Cpu: int
        :param Memory: It is required when `DbMode` is set to `NORMAL` or left empty.
Memory of a non-serverless instance in GB
        :type Memory: int
        :param Storage: This parameter has been deprecated.
Storage capacity in GB
        :type Storage: int
        :param ClusterName: Cluster name, which can contain less than 64 letters, digits, or symbols (-_.).
        :type ClusterName: str
        :param AdminPassword: Account password, which must contain 8-64 characters in at least three of the following four types: uppercase letters, lowercase letters, digits, and symbols (~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/).
        :type AdminPassword: str
        :param Port: Port. Valid range: [0, 65535). Default value: 3306
        :type Port: int
        :param PayMode: Billing mode. `0`: pay-as-you-go; `1`: monthly subscription. Default value: `0`
        :type PayMode: int
        :param Count: Number of purchased clusters. Valid range: [1,50]. Default value: 1
        :type Count: int
        :param RollbackStrategy: Rollback type:
noneRollback: no rollback;
snapRollback: rollback by snapshot;
timeRollback: rollback by time point
        :type RollbackStrategy: str
        :param RollbackId: `snapshotId` for snapshot rollback or `queryId` for time point rollback. 0 indicates to determine whether the time point is valid
        :type RollbackId: int
        :param OriginalClusterId: The source cluster ID passed in during rollback to find the source `poolId`
        :type OriginalClusterId: str
        :param ExpectTime: Specified time for time point rollback or snapshot time for snapshot rollback
        :type ExpectTime: str
        :param ExpectTimeThresh: This parameter has been deprecated.
Specified allowed time range for time point rollback
        :type ExpectTimeThresh: int
        :param StorageLimit: Storage upper limit of normal instance in GB
If `DbType` is `MYSQL` and the storage billing mode is monthly subscription, the parameter value can’t exceed the maximum storage corresponding to the CPU and memory specifications.
        :type StorageLimit: int
        :param InstanceCount: Number of Instances. Valid range: (0,16]
        :type InstanceCount: int
        :param TimeSpan: Purchase duration of monthly subscription plan
        :type TimeSpan: int
        :param TimeUnit: Duration unit of monthly subscription. Valid values: `s`, `d`, `m`, `y`
        :type TimeUnit: str
        :param AutoRenewFlag: Whether auto-renewal is enabled for monthly subscription plan. Default value: `0`
        :type AutoRenewFlag: int
        :param AutoVoucher: Whether to automatically select a voucher. `1`: yes; `0`: no. Default value: `0`
        :type AutoVoucher: int
        :param HaCount: Number of instances (this parameter has been disused and is retained only for compatibility with existing instances)
        :type HaCount: int
        :param OrderSource: Order source
        :type OrderSource: str
        :param ResourceTags: Array of tags to be bound to the created cluster
        :type ResourceTags: list of Tag
        :param DbMode: Database type
Valid values when `DbType` is `MYSQL` (default value: `NORMAL`):
<li>NORMAL</li>
<li>SERVERLESS</li>
        :type DbMode: str
        :param MinCpu: This parameter is required if `DbMode` is `SERVERLESS`.
Minimum number of CPU cores. For the value range, see the returned result of `DescribeServerlessInstanceSpecs`.
        :type MinCpu: float
        :param MaxCpu: This parameter is required if `DbMode` is `SERVERLESS`.
Maximum number of CPU cores. For the value range, see the returned result of `DescribeServerlessInstanceSpecs`.
        :type MaxCpu: float
        :param AutoPause: This parameter specifies whether the cluster will be automatically paused if `DbMode` is `SERVERLESS`. Valid values:
<li>yes</li>
<li>no</li>
Default value: yes
        :type AutoPause: str
        :param AutoPauseDelay: This parameter specifies the delay for automatic cluster pause in seconds if `DbMode` is `SERVERLESS`. Value range: [600,691200]
Default value: `600`
        :type AutoPauseDelay: int
        :param StoragePayMode: The billing mode of cluster storage. Valid values: `0` (pay-as-you-go), `1` (monthly subscription). Default value: `0`.
If `DbType` is `MYSQL` and the billing mode of cluster compute is pay-as-you-go (or the `DbMode` is `SERVERLESS`), the billing mode of cluster storage must be pay-as-you-go.
Clusters with storage billed in monthly subscription can’t be cloned or rolled back.
        :type StoragePayMode: int
        :param SecurityGroupIds: Array of security group IDs
        :type SecurityGroupIds: list of str
        :param AlarmPolicyIds: Array of alarm policy IDs
        :type AlarmPolicyIds: list of str
        :param ClusterParams: Array of parameters. Valid values: `character_set_server` (utf8｜latin1｜gbk｜utf8mb4), `lower_case_table_names`. 0: case-sensitive; 1: case-insensitive).
        :type ClusterParams: list of ParamItem
        :param DealMode: Transaction mode. Valid values: `0` (place and pay for an order), `1` (place an order)
        :type DealMode: int
        :param ParamTemplateId: Parameter template ID, which can be obtained by querying parameter template information “DescribeParamTemplates”
        :type ParamTemplateId: int
        :param SlaveZone: Multi-AZ address
        :type SlaveZone: str
        :param InstanceInitInfos: Instance initialization configuration information, which is used to select instances with different specifications when purchasing a cluster.
        :type InstanceInitInfos: list of InstanceInitInfo
        """
        self.Zone = None
        self.VpcId = None
        self.SubnetId = None
        self.DbType = None
        self.DbVersion = None
        self.ProjectId = None
        self.Cpu = None
        self.Memory = None
        self.Storage = None
        self.ClusterName = None
        self.AdminPassword = None
        self.Port = None
        self.PayMode = None
        self.Count = None
        self.RollbackStrategy = None
        self.RollbackId = None
        self.OriginalClusterId = None
        self.ExpectTime = None
        self.ExpectTimeThresh = None
        self.StorageLimit = None
        self.InstanceCount = None
        self.TimeSpan = None
        self.TimeUnit = None
        self.AutoRenewFlag = None
        self.AutoVoucher = None
        self.HaCount = None
        self.OrderSource = None
        self.ResourceTags = None
        self.DbMode = None
        self.MinCpu = None
        self.MaxCpu = None
        self.AutoPause = None
        self.AutoPauseDelay = None
        self.StoragePayMode = None
        self.SecurityGroupIds = None
        self.AlarmPolicyIds = None
        self.ClusterParams = None
        self.DealMode = None
        self.ParamTemplateId = None
        self.SlaveZone = None
        self.InstanceInitInfos = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.DbType = params.get("DbType")
        self.DbVersion = params.get("DbVersion")
        self.ProjectId = params.get("ProjectId")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.ClusterName = params.get("ClusterName")
        self.AdminPassword = params.get("AdminPassword")
        self.Port = params.get("Port")
        self.PayMode = params.get("PayMode")
        self.Count = params.get("Count")
        self.RollbackStrategy = params.get("RollbackStrategy")
        self.RollbackId = params.get("RollbackId")
        self.OriginalClusterId = params.get("OriginalClusterId")
        self.ExpectTime = params.get("ExpectTime")
        self.ExpectTimeThresh = params.get("ExpectTimeThresh")
        self.StorageLimit = params.get("StorageLimit")
        self.InstanceCount = params.get("InstanceCount")
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.AutoVoucher = params.get("AutoVoucher")
        self.HaCount = params.get("HaCount")
        self.OrderSource = params.get("OrderSource")
        if params.get("ResourceTags") is not None:
            self.ResourceTags = []
            for item in params.get("ResourceTags"):
                obj = Tag()
                obj._deserialize(item)
                self.ResourceTags.append(obj)
        self.DbMode = params.get("DbMode")
        self.MinCpu = params.get("MinCpu")
        self.MaxCpu = params.get("MaxCpu")
        self.AutoPause = params.get("AutoPause")
        self.AutoPauseDelay = params.get("AutoPauseDelay")
        self.StoragePayMode = params.get("StoragePayMode")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.AlarmPolicyIds = params.get("AlarmPolicyIds")
        if params.get("ClusterParams") is not None:
            self.ClusterParams = []
            for item in params.get("ClusterParams"):
                obj = ParamItem()
                obj._deserialize(item)
                self.ClusterParams.append(obj)
        self.DealMode = params.get("DealMode")
        self.ParamTemplateId = params.get("ParamTemplateId")
        self.SlaveZone = params.get("SlaveZone")
        if params.get("InstanceInitInfos") is not None:
            self.InstanceInitInfos = []
            for item in params.get("InstanceInitInfos"):
                obj = InstanceInitInfo()
                obj._deserialize(item)
                self.InstanceInitInfos.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateClustersResponse(AbstractModel):
    """CreateClusters response structure.

    """

    def __init__(self):
        r"""
        :param TranId: Freezing transaction ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type TranId: str
        :param DealNames: Order ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type DealNames: list of str
        :param ResourceIds: List of resource IDs (This field has been deprecated. You need to use `dealNames` in the `DescribeResourcesByDealName` API to get resource IDs.)
Note: This field may return null, indicating that no valid values can be obtained.
        :type ResourceIds: list of str
        :param ClusterIds: List of cluster IDs (This field has been deprecated. You need to use `dealNames` in the `DescribeResourcesByDealName` API to get cluster IDs.)
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClusterIds: list of str
        :param BigDealIds: Big order ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type BigDealIds: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TranId = None
        self.DealNames = None
        self.ResourceIds = None
        self.ClusterIds = None
        self.BigDealIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TranId = params.get("TranId")
        self.DealNames = params.get("DealNames")
        self.ResourceIds = params.get("ResourceIds")
        self.ClusterIds = params.get("ClusterIds")
        self.BigDealIds = params.get("BigDealIds")
        self.RequestId = params.get("RequestId")


class CynosdbCluster(AbstractModel):
    """Cluster information

    """

    def __init__(self):
        r"""
        :param Status: Cluster status. Valid values are as follows:
creating
running
isolating
isolated
activating (removing isolation)
offlining (deactivating)
offlined (deactivated)
deleting
deleted
        :type Status: str
        :param UpdateTime: Update time
        :type UpdateTime: str
        :param Zone: AZ
        :type Zone: str
        :param ClusterName: Cluster name
        :type ClusterName: str
        :param Region: Region
        :type Region: str
        :param DbVersion: Database version
        :type DbVersion: str
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param InstanceNum: Number of instances
        :type InstanceNum: int
        :param Uin: User UIN
Note: This field may return null, indicating that no valid values can be obtained.
        :type Uin: str
        :param DbType: Engine type
Note: This field may return null, indicating that no valid values can be obtained.
        :type DbType: str
        :param AppId: User `appid`
Note: This field may return null, indicating that no valid values can be obtained.
        :type AppId: int
        :param StatusDesc: Cluster status description
Note: This field may return null, indicating that no valid values can be obtained.
        :type StatusDesc: str
        :param CreateTime: Cluster creation time
Note: This field may return null, indicating that no valid values can be obtained.
        :type CreateTime: str
        :param PayMode: Billing mode. `0`: Pay-as-you-go; `1`: Monthly subscription.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PayMode: int
        :param PeriodEndTime: End time
Note: This field may return null, indicating that no valid values can be obtained.
        :type PeriodEndTime: str
        :param Vip: Cluster read-write VIP
Note: This field may return null, indicating that no valid values can be obtained.
        :type Vip: str
        :param Vport: Cluster read-write vport
Note: This field may return null, indicating that no valid values can be obtained.
        :type Vport: int
        :param ProjectID: Project ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProjectID: int
        :param VpcId: VPC ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type VpcId: str
        :param SubnetId: Subnet ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type SubnetId: str
        :param CynosVersion: TDSQL-C kernel version
Note: This field may return null, indicating that no valid values can be obtained.
        :type CynosVersion: str
        :param StorageLimit: Storage capacity
Note: This field may return null, indicating that no valid values can be obtained.
        :type StorageLimit: int
        :param RenewFlag: Renewal flag
Note: This field may return null, indicating that no valid values can be obtained.
        :type RenewFlag: int
        :param ProcessingTask: Task in progress
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProcessingTask: str
        :param Tasks: Array of tasks in the cluster
Note: This field may return null, indicating that no valid values can be obtained.
        :type Tasks: list of ObjectTask
        :param ResourceTags: Array of tags bound to the cluster
Note: This field may return null, indicating that no valid values can be obtained.
        :type ResourceTags: list of Tag
        :param DbMode: Database type. Valid values: `NORMAL`, `SERVERLESS`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DbMode: str
        :param ServerlessStatus: Serverless cluster status when the database type is `SERVERLESS`. Valid values:
`resume`
`pause`
Note: This field may return null, indicating that no valid values can be obtained.
        :type ServerlessStatus: str
        :param Storage: Prepaid cluster storage capacity
Note: This field may return null, indicating that no valid values can be obtained.
        :type Storage: int
        :param StorageId: Cluster storage ID used in prepaid storage modification
Note: This field may return null, indicating that no valid values can be obtained.
        :type StorageId: str
        :param StoragePayMode: Billing mode of cluster storage. Valid values: `0` (pay-as-you-go), `1` (monthly subscription).
Note: This field may return null, indicating that no valid values can be obtained.
        :type StoragePayMode: int
        :param MinStorageSize: The minimum storage corresponding to the compute specification of the cluster
Note: This field may return null, indicating that no valid values can be obtained.
        :type MinStorageSize: int
        :param MaxStorageSize: The maximum storage corresponding to the compute specification of the cluster
Note: This field may return null, indicating that no valid values can be obtained.
        :type MaxStorageSize: int
        :param NetAddrs: Network information of the cluster
Note: This field may return null, indicating that no valid values can be obtained.
        :type NetAddrs: list of NetAddr
        :param PhysicalZone: Physical AZ
Note: This field may return null, indicating that no valid values can be obtained.
        :type PhysicalZone: str
        :param MasterZone: Primary AZ
Note: This field may return null, indicating that no valid values can be obtained.
        :type MasterZone: str
        :param HasSlaveZone: Whether there is a secondary AZ
Note: This field may return null, indicating that no valid values can be obtained.
        :type HasSlaveZone: str
        :param SlaveZones: Secondary AZ
Note: This field may return null, indicating that no valid values can be obtained.
        :type SlaveZones: list of str
        :param BusinessType: Business type
Note: This field may return null, indicating that no valid values can be obtained.
        :type BusinessType: str
        :param IsFreeze: Whether to freeze
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsFreeze: str
        :param OrderSource: Order source
Note: This field may return null, indicating that no valid values can be obtained.
        :type OrderSource: str
        :param Ability: Capability
Note: This field may return null, indicating that no valid values can be obtained.
        :type Ability: :class:`tencentcloud.cynosdb.v20190107.models.Ability`
        """
        self.Status = None
        self.UpdateTime = None
        self.Zone = None
        self.ClusterName = None
        self.Region = None
        self.DbVersion = None
        self.ClusterId = None
        self.InstanceNum = None
        self.Uin = None
        self.DbType = None
        self.AppId = None
        self.StatusDesc = None
        self.CreateTime = None
        self.PayMode = None
        self.PeriodEndTime = None
        self.Vip = None
        self.Vport = None
        self.ProjectID = None
        self.VpcId = None
        self.SubnetId = None
        self.CynosVersion = None
        self.StorageLimit = None
        self.RenewFlag = None
        self.ProcessingTask = None
        self.Tasks = None
        self.ResourceTags = None
        self.DbMode = None
        self.ServerlessStatus = None
        self.Storage = None
        self.StorageId = None
        self.StoragePayMode = None
        self.MinStorageSize = None
        self.MaxStorageSize = None
        self.NetAddrs = None
        self.PhysicalZone = None
        self.MasterZone = None
        self.HasSlaveZone = None
        self.SlaveZones = None
        self.BusinessType = None
        self.IsFreeze = None
        self.OrderSource = None
        self.Ability = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.UpdateTime = params.get("UpdateTime")
        self.Zone = params.get("Zone")
        self.ClusterName = params.get("ClusterName")
        self.Region = params.get("Region")
        self.DbVersion = params.get("DbVersion")
        self.ClusterId = params.get("ClusterId")
        self.InstanceNum = params.get("InstanceNum")
        self.Uin = params.get("Uin")
        self.DbType = params.get("DbType")
        self.AppId = params.get("AppId")
        self.StatusDesc = params.get("StatusDesc")
        self.CreateTime = params.get("CreateTime")
        self.PayMode = params.get("PayMode")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.ProjectID = params.get("ProjectID")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.CynosVersion = params.get("CynosVersion")
        self.StorageLimit = params.get("StorageLimit")
        self.RenewFlag = params.get("RenewFlag")
        self.ProcessingTask = params.get("ProcessingTask")
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = ObjectTask()
                obj._deserialize(item)
                self.Tasks.append(obj)
        if params.get("ResourceTags") is not None:
            self.ResourceTags = []
            for item in params.get("ResourceTags"):
                obj = Tag()
                obj._deserialize(item)
                self.ResourceTags.append(obj)
        self.DbMode = params.get("DbMode")
        self.ServerlessStatus = params.get("ServerlessStatus")
        self.Storage = params.get("Storage")
        self.StorageId = params.get("StorageId")
        self.StoragePayMode = params.get("StoragePayMode")
        self.MinStorageSize = params.get("MinStorageSize")
        self.MaxStorageSize = params.get("MaxStorageSize")
        if params.get("NetAddrs") is not None:
            self.NetAddrs = []
            for item in params.get("NetAddrs"):
                obj = NetAddr()
                obj._deserialize(item)
                self.NetAddrs.append(obj)
        self.PhysicalZone = params.get("PhysicalZone")
        self.MasterZone = params.get("MasterZone")
        self.HasSlaveZone = params.get("HasSlaveZone")
        self.SlaveZones = params.get("SlaveZones")
        self.BusinessType = params.get("BusinessType")
        self.IsFreeze = params.get("IsFreeze")
        self.OrderSource = params.get("OrderSource")
        if params.get("Ability") is not None:
            self.Ability = Ability()
            self.Ability._deserialize(params.get("Ability"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CynosdbClusterDetail(AbstractModel):
    """Cluster details

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param ClusterName: Cluster name
        :type ClusterName: str
        :param Region: Region
        :type Region: str
        :param Status: Status
        :type Status: str
        :param StatusDesc: Status description
        :type StatusDesc: str
        :param VpcName: VPC name
        :type VpcName: str
        :param VpcId: Unique VPC ID
        :type VpcId: str
        :param SubnetName: Subnet name
        :type SubnetName: str
        :param SubnetId: Subnet ID
        :type SubnetId: str
        :param Charset: Character set
        :type Charset: str
        :param CreateTime: Creation time
        :type CreateTime: str
        :param DbType: Database type
        :type DbType: str
        :param DbVersion: Database version
        :type DbVersion: str
        :param UsedStorage: Used capacity
        :type UsedStorage: int
        :param RoAddr: vport for read/write separation
        :type RoAddr: list of Addr
        :param InstanceSet: Instance information
        :type InstanceSet: list of ClusterInstanceDetail
        :param PayMode: Billing mode
        :type PayMode: int
        :param PeriodEndTime: Expiration time
        :type PeriodEndTime: str
        :param Vip: VIP
        :type Vip: str
        :param Vport: vport
        :type Vport: int
        :param ProjectID: Project ID
        :type ProjectID: int
        :param Zone: AZ
        :type Zone: str
        :param ResourceTags: Array of tags bound to instance
        :type ResourceTags: list of Tag
        :param ServerlessStatus: Serverless cluster status when the database type is `SERVERLESS`. Valid values:
resume
resuming
pause
pausing
        :type ServerlessStatus: str
        :param LogBin: Binlog switch. Valid values: `ON`, `OFF`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type LogBin: str
        :param PitrType: PITR type. Valid values: `normal`, `redo_pitr`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type PitrType: str
        :param PhysicalZone: Physical AZ
Note: This field may return null, indicating that no valid values can be obtained.
        :type PhysicalZone: str
        :param StorageId: Storage ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type StorageId: str
        :param Storage: Storage capacity in GB
Note: This field may return null, indicating that no valid values can be obtained.
        :type Storage: int
        :param MaxStorageSize: Maximum storage specification in GB
Note: This field may return null, indicating that no valid values can be obtained.
        :type MaxStorageSize: int
        :param MinStorageSize: Minimum storage specification in GB
Note: This field may return null, indicating that no valid values can be obtained.
        :type MinStorageSize: int
        :param StoragePayMode: Storage billing mode. Valid values: `1` (monthly subscription), `0` (pay-as-you-go).
Note: This field may return null, indicating that no valid values can be obtained.
        :type StoragePayMode: int
        :param DbMode: Database type. Valid values: `normal`, `serverless`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DbMode: str
        :param StorageLimit: Maximum storage space
Note: This field may return null, indicating that no valid values can be obtained.
        :type StorageLimit: int
        :param Ability: Features supported by the cluster
Note: This field may return null, indicating that no valid values can be obtained.
        :type Ability: :class:`tencentcloud.cynosdb.v20190107.models.Ability`
        :param CynosVersion: TDSQL-C version
Note: This field may return null, indicating that no valid values can be obtained.
        :type CynosVersion: str
        :param BusinessType: Business type
Note: This field may return null, indicating that no valid values can be obtained.
        :type BusinessType: str
        :param HasSlaveZone: Whether there is a secondary AZ
Note: This field may return null, indicating that no valid values can be obtained.
        :type HasSlaveZone: str
        :param IsFreeze: Whether to freeze
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsFreeze: str
        :param Tasks: Task list
Note: This field may return null, indicating that no valid values can be obtained.
        :type Tasks: list of ObjectTask
        :param MasterZone: Primary AZ
Note: This field may return null, indicating that no valid values can be obtained.
        :type MasterZone: str
        :param SlaveZones: Secondary AZ list
Note: This field may return null, indicating that no valid values can be obtained.
        :type SlaveZones: list of str
        :param ProxyStatus: Proxy status
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProxyStatus: str
        :param IsSkipTrade: Whether to skip the transaction
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsSkipTrade: str
        :param IsOpenPasswordComplexity: Whether to enable password complexity
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsOpenPasswordComplexity: str
        :param NetworkStatus: Network type
Note: This field may return null, indicating that no valid values can be obtained.
        :type NetworkStatus: str
        """
        self.ClusterId = None
        self.ClusterName = None
        self.Region = None
        self.Status = None
        self.StatusDesc = None
        self.VpcName = None
        self.VpcId = None
        self.SubnetName = None
        self.SubnetId = None
        self.Charset = None
        self.CreateTime = None
        self.DbType = None
        self.DbVersion = None
        self.UsedStorage = None
        self.RoAddr = None
        self.InstanceSet = None
        self.PayMode = None
        self.PeriodEndTime = None
        self.Vip = None
        self.Vport = None
        self.ProjectID = None
        self.Zone = None
        self.ResourceTags = None
        self.ServerlessStatus = None
        self.LogBin = None
        self.PitrType = None
        self.PhysicalZone = None
        self.StorageId = None
        self.Storage = None
        self.MaxStorageSize = None
        self.MinStorageSize = None
        self.StoragePayMode = None
        self.DbMode = None
        self.StorageLimit = None
        self.Ability = None
        self.CynosVersion = None
        self.BusinessType = None
        self.HasSlaveZone = None
        self.IsFreeze = None
        self.Tasks = None
        self.MasterZone = None
        self.SlaveZones = None
        self.ProxyStatus = None
        self.IsSkipTrade = None
        self.IsOpenPasswordComplexity = None
        self.NetworkStatus = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ClusterName = params.get("ClusterName")
        self.Region = params.get("Region")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.VpcName = params.get("VpcName")
        self.VpcId = params.get("VpcId")
        self.SubnetName = params.get("SubnetName")
        self.SubnetId = params.get("SubnetId")
        self.Charset = params.get("Charset")
        self.CreateTime = params.get("CreateTime")
        self.DbType = params.get("DbType")
        self.DbVersion = params.get("DbVersion")
        self.UsedStorage = params.get("UsedStorage")
        if params.get("RoAddr") is not None:
            self.RoAddr = []
            for item in params.get("RoAddr"):
                obj = Addr()
                obj._deserialize(item)
                self.RoAddr.append(obj)
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = ClusterInstanceDetail()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.PayMode = params.get("PayMode")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.ProjectID = params.get("ProjectID")
        self.Zone = params.get("Zone")
        if params.get("ResourceTags") is not None:
            self.ResourceTags = []
            for item in params.get("ResourceTags"):
                obj = Tag()
                obj._deserialize(item)
                self.ResourceTags.append(obj)
        self.ServerlessStatus = params.get("ServerlessStatus")
        self.LogBin = params.get("LogBin")
        self.PitrType = params.get("PitrType")
        self.PhysicalZone = params.get("PhysicalZone")
        self.StorageId = params.get("StorageId")
        self.Storage = params.get("Storage")
        self.MaxStorageSize = params.get("MaxStorageSize")
        self.MinStorageSize = params.get("MinStorageSize")
        self.StoragePayMode = params.get("StoragePayMode")
        self.DbMode = params.get("DbMode")
        self.StorageLimit = params.get("StorageLimit")
        if params.get("Ability") is not None:
            self.Ability = Ability()
            self.Ability._deserialize(params.get("Ability"))
        self.CynosVersion = params.get("CynosVersion")
        self.BusinessType = params.get("BusinessType")
        self.HasSlaveZone = params.get("HasSlaveZone")
        self.IsFreeze = params.get("IsFreeze")
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = ObjectTask()
                obj._deserialize(item)
                self.Tasks.append(obj)
        self.MasterZone = params.get("MasterZone")
        self.SlaveZones = params.get("SlaveZones")
        self.ProxyStatus = params.get("ProxyStatus")
        self.IsSkipTrade = params.get("IsSkipTrade")
        self.IsOpenPasswordComplexity = params.get("IsOpenPasswordComplexity")
        self.NetworkStatus = params.get("NetworkStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CynosdbInstance(AbstractModel):
    """Instance information

    """

    def __init__(self):
        r"""
        :param Uin: User `Uin`
        :type Uin: str
        :param AppId: User `AppId`
        :type AppId: int
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param ClusterName: Cluster name
        :type ClusterName: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param InstanceName: Instance name
        :type InstanceName: str
        :param ProjectId: Project ID
        :type ProjectId: int
        :param Region: Region
        :type Region: str
        :param Zone: AZ
        :type Zone: str
        :param Status: Instance status
        :type Status: str
        :param StatusDesc: Instance status description
        :type StatusDesc: str
        :param DbType: Database type
        :type DbType: str
        :param DbVersion: Database version
        :type DbVersion: str
        :param Cpu: Number of CPU cores
        :type Cpu: int
        :param Memory: Memory in GB
        :type Memory: int
        :param Storage: Storage capacity in GB
        :type Storage: int
        :param InstanceType: Instance type
        :type InstanceType: str
        :param InstanceRole: Current instance role
        :type InstanceRole: str
        :param UpdateTime: Update time
        :type UpdateTime: str
        :param CreateTime: Creation time
        :type CreateTime: str
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: Subnet ID
        :type SubnetId: str
        :param Vip: Private IP of instance
        :type Vip: str
        :param Vport: Private port of instance
        :type Vport: int
        :param PayMode: Billing mode
        :type PayMode: int
        :param PeriodEndTime: Instance expiration time
        :type PeriodEndTime: str
        :param DestroyDeadlineText: Termination deadline
        :type DestroyDeadlineText: str
        :param IsolateTime: Isolation time
        :type IsolateTime: str
        :param NetType: Network type
        :type NetType: int
        :param WanDomain: Public domain name
        :type WanDomain: str
        :param WanIP: Public IP
        :type WanIP: str
        :param WanPort: Public port
        :type WanPort: int
        :param WanStatus: Public network status
        :type WanStatus: str
        :param DestroyTime: Instance termination time
        :type DestroyTime: str
        :param CynosVersion: TDSQL-C kernel version
        :type CynosVersion: str
        :param ProcessingTask: Task in progress
        :type ProcessingTask: str
        :param RenewFlag: Renewal flag
        :type RenewFlag: int
        :param MinCpu: Minimum number of CPU cores for serverless instance
        :type MinCpu: float
        :param MaxCpu: Maximum number of CPU cores for serverless instance
        :type MaxCpu: float
        :param ServerlessStatus: Serverless instance status. Valid values:
resume
pause
        :type ServerlessStatus: str
        :param StorageId: Prepaid storage ID
Note: this field may return `null`, indicating that no valid value can be obtained.
        :type StorageId: str
        :param StoragePayMode: Storage billing mode
        :type StoragePayMode: int
        :param PhysicalZone: Physical zone
        :type PhysicalZone: str
        :param BusinessType: Business type
Note: This field may return null, indicating that no valid value can be obtained.
        :type BusinessType: str
        :param Tasks: Task
Note: This field may return null, indicating that no valid values can be obtained.
        :type Tasks: list of ObjectTask
        :param IsFreeze: Whether to freeze
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsFreeze: str
        :param ResourceTags: The resource tag
Note: This field may return null, indicating that no valid values can be obtained.
        :type ResourceTags: list of Tag
        :param MasterZone: Source AZ
Note: This field may return null, indicating that no valid value can be obtained.
        :type MasterZone: str
        :param SlaveZones: Replica AZ
Note: This field may return null, indicating that no valid value can be obtained.
        :type SlaveZones: list of str
        :param InstanceNetInfo: Instance network information
Note: This field may return null, indicating that no valid value can be obtained.
        :type InstanceNetInfo: list of InstanceNetInfo
        """
        self.Uin = None
        self.AppId = None
        self.ClusterId = None
        self.ClusterName = None
        self.InstanceId = None
        self.InstanceName = None
        self.ProjectId = None
        self.Region = None
        self.Zone = None
        self.Status = None
        self.StatusDesc = None
        self.DbType = None
        self.DbVersion = None
        self.Cpu = None
        self.Memory = None
        self.Storage = None
        self.InstanceType = None
        self.InstanceRole = None
        self.UpdateTime = None
        self.CreateTime = None
        self.VpcId = None
        self.SubnetId = None
        self.Vip = None
        self.Vport = None
        self.PayMode = None
        self.PeriodEndTime = None
        self.DestroyDeadlineText = None
        self.IsolateTime = None
        self.NetType = None
        self.WanDomain = None
        self.WanIP = None
        self.WanPort = None
        self.WanStatus = None
        self.DestroyTime = None
        self.CynosVersion = None
        self.ProcessingTask = None
        self.RenewFlag = None
        self.MinCpu = None
        self.MaxCpu = None
        self.ServerlessStatus = None
        self.StorageId = None
        self.StoragePayMode = None
        self.PhysicalZone = None
        self.BusinessType = None
        self.Tasks = None
        self.IsFreeze = None
        self.ResourceTags = None
        self.MasterZone = None
        self.SlaveZones = None
        self.InstanceNetInfo = None


    def _deserialize(self, params):
        self.Uin = params.get("Uin")
        self.AppId = params.get("AppId")
        self.ClusterId = params.get("ClusterId")
        self.ClusterName = params.get("ClusterName")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.ProjectId = params.get("ProjectId")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.DbType = params.get("DbType")
        self.DbVersion = params.get("DbVersion")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.InstanceType = params.get("InstanceType")
        self.InstanceRole = params.get("InstanceRole")
        self.UpdateTime = params.get("UpdateTime")
        self.CreateTime = params.get("CreateTime")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.PayMode = params.get("PayMode")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.DestroyDeadlineText = params.get("DestroyDeadlineText")
        self.IsolateTime = params.get("IsolateTime")
        self.NetType = params.get("NetType")
        self.WanDomain = params.get("WanDomain")
        self.WanIP = params.get("WanIP")
        self.WanPort = params.get("WanPort")
        self.WanStatus = params.get("WanStatus")
        self.DestroyTime = params.get("DestroyTime")
        self.CynosVersion = params.get("CynosVersion")
        self.ProcessingTask = params.get("ProcessingTask")
        self.RenewFlag = params.get("RenewFlag")
        self.MinCpu = params.get("MinCpu")
        self.MaxCpu = params.get("MaxCpu")
        self.ServerlessStatus = params.get("ServerlessStatus")
        self.StorageId = params.get("StorageId")
        self.StoragePayMode = params.get("StoragePayMode")
        self.PhysicalZone = params.get("PhysicalZone")
        self.BusinessType = params.get("BusinessType")
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = ObjectTask()
                obj._deserialize(item)
                self.Tasks.append(obj)
        self.IsFreeze = params.get("IsFreeze")
        if params.get("ResourceTags") is not None:
            self.ResourceTags = []
            for item in params.get("ResourceTags"):
                obj = Tag()
                obj._deserialize(item)
                self.ResourceTags.append(obj)
        self.MasterZone = params.get("MasterZone")
        self.SlaveZones = params.get("SlaveZones")
        if params.get("InstanceNetInfo") is not None:
            self.InstanceNetInfo = []
            for item in params.get("InstanceNetInfo"):
                obj = InstanceNetInfo()
                obj._deserialize(item)
                self.InstanceNetInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CynosdbInstanceDetail(AbstractModel):
    """Instance details

    """

    def __init__(self):
        r"""
        :param Uin: User `Uin`
        :type Uin: str
        :param AppId: User `AppId`
        :type AppId: int
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param ClusterName: Cluster name
        :type ClusterName: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param InstanceName: Instance name
        :type InstanceName: str
        :param ProjectId: Project ID
        :type ProjectId: int
        :param Region: Region
        :type Region: str
        :param Zone: AZ
        :type Zone: str
        :param Status: Instance status
        :type Status: str
        :param StatusDesc: Instance status description
        :type StatusDesc: str
        :param DbType: Database type
        :type DbType: str
        :param DbVersion: Database version
        :type DbVersion: str
        :param Cpu: Number of CPU cores
        :type Cpu: int
        :param Memory: Memory in GB
        :type Memory: int
        :param Storage: Storage capacity in GB
        :type Storage: int
        :param InstanceType: Instance type
        :type InstanceType: str
        :param InstanceRole: Current instance role
        :type InstanceRole: str
        :param UpdateTime: Update time
        :type UpdateTime: str
        :param CreateTime: Creation time
        :type CreateTime: str
        :param PayMode: Billing mode
        :type PayMode: int
        :param PeriodEndTime: Instance expiration time
        :type PeriodEndTime: str
        :param NetType: Network type
        :type NetType: int
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: Subnet ID
        :type SubnetId: str
        :param Vip: Private IP of instance
        :type Vip: str
        :param Vport: Private port of instance
        :type Vport: int
        :param WanDomain: Public domain name of instance
        :type WanDomain: str
        :param Charset: Character set
        :type Charset: str
        :param CynosVersion: TDSQL-C kernel version
        :type CynosVersion: str
        :param RenewFlag: Renewal flag
        :type RenewFlag: int
        :param MinCpu: The minimum number of CPU cores for a serverless instance
        :type MinCpu: float
        :param MaxCpu: The maximum number of CPU cores for a serverless instance
        :type MaxCpu: float
        :param ServerlessStatus: Serverless instance status. Valid values:
resume
pause
        :type ServerlessStatus: str
        """
        self.Uin = None
        self.AppId = None
        self.ClusterId = None
        self.ClusterName = None
        self.InstanceId = None
        self.InstanceName = None
        self.ProjectId = None
        self.Region = None
        self.Zone = None
        self.Status = None
        self.StatusDesc = None
        self.DbType = None
        self.DbVersion = None
        self.Cpu = None
        self.Memory = None
        self.Storage = None
        self.InstanceType = None
        self.InstanceRole = None
        self.UpdateTime = None
        self.CreateTime = None
        self.PayMode = None
        self.PeriodEndTime = None
        self.NetType = None
        self.VpcId = None
        self.SubnetId = None
        self.Vip = None
        self.Vport = None
        self.WanDomain = None
        self.Charset = None
        self.CynosVersion = None
        self.RenewFlag = None
        self.MinCpu = None
        self.MaxCpu = None
        self.ServerlessStatus = None


    def _deserialize(self, params):
        self.Uin = params.get("Uin")
        self.AppId = params.get("AppId")
        self.ClusterId = params.get("ClusterId")
        self.ClusterName = params.get("ClusterName")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.ProjectId = params.get("ProjectId")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.DbType = params.get("DbType")
        self.DbVersion = params.get("DbVersion")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.InstanceType = params.get("InstanceType")
        self.InstanceRole = params.get("InstanceRole")
        self.UpdateTime = params.get("UpdateTime")
        self.CreateTime = params.get("CreateTime")
        self.PayMode = params.get("PayMode")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.NetType = params.get("NetType")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.WanDomain = params.get("WanDomain")
        self.Charset = params.get("Charset")
        self.CynosVersion = params.get("CynosVersion")
        self.RenewFlag = params.get("RenewFlag")
        self.MinCpu = params.get("MinCpu")
        self.MaxCpu = params.get("MaxCpu")
        self.ServerlessStatus = params.get("ServerlessStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CynosdbInstanceGrp(AbstractModel):
    """Instance group information

    """

    def __init__(self):
        r"""
        :param AppId: User `appId`
        :type AppId: int
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param CreatedTime: Creation time
        :type CreatedTime: str
        :param DeletedTime: Deletion time
        :type DeletedTime: str
        :param InstanceGrpId: Instance group ID
        :type InstanceGrpId: str
        :param Status: Status
        :type Status: str
        :param Type: Instance group type. ha: HA group; ro: RO group
        :type Type: str
        :param UpdatedTime: Update time
        :type UpdatedTime: str
        :param Vip: Private IP
        :type Vip: str
        :param Vport: Private port
        :type Vport: int
        :param WanDomain: Public domain name
        :type WanDomain: str
        :param WanIP: Public IP
        :type WanIP: str
        :param WanPort: Public port
        :type WanPort: int
        :param WanStatus: Public network status
        :type WanStatus: str
        :param InstanceSet: Information of instances contained in instance group
        :type InstanceSet: list of CynosdbInstance
        :param UniqVpcId: VPC ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type UniqVpcId: str
        :param UniqSubnetId: Subnet ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type UniqSubnetId: str
        :param OldAddrInfo: Information of the old IP
Note: This field may return null, indicating that no valid values can be obtained.
        :type OldAddrInfo: :class:`tencentcloud.cynosdb.v20190107.models.OldAddrInfo`
        :param ProcessingTasks: Task in progress
        :type ProcessingTasks: list of str
        :param Tasks: Task list
        :type Tasks: list of ObjectTask
        :param NetServiceId: biz_net_service table ID
        :type NetServiceId: int
        """
        self.AppId = None
        self.ClusterId = None
        self.CreatedTime = None
        self.DeletedTime = None
        self.InstanceGrpId = None
        self.Status = None
        self.Type = None
        self.UpdatedTime = None
        self.Vip = None
        self.Vport = None
        self.WanDomain = None
        self.WanIP = None
        self.WanPort = None
        self.WanStatus = None
        self.InstanceSet = None
        self.UniqVpcId = None
        self.UniqSubnetId = None
        self.OldAddrInfo = None
        self.ProcessingTasks = None
        self.Tasks = None
        self.NetServiceId = None


    def _deserialize(self, params):
        self.AppId = params.get("AppId")
        self.ClusterId = params.get("ClusterId")
        self.CreatedTime = params.get("CreatedTime")
        self.DeletedTime = params.get("DeletedTime")
        self.InstanceGrpId = params.get("InstanceGrpId")
        self.Status = params.get("Status")
        self.Type = params.get("Type")
        self.UpdatedTime = params.get("UpdatedTime")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.WanDomain = params.get("WanDomain")
        self.WanIP = params.get("WanIP")
        self.WanPort = params.get("WanPort")
        self.WanStatus = params.get("WanStatus")
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = CynosdbInstance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.UniqVpcId = params.get("UniqVpcId")
        self.UniqSubnetId = params.get("UniqSubnetId")
        if params.get("OldAddrInfo") is not None:
            self.OldAddrInfo = OldAddrInfo()
            self.OldAddrInfo._deserialize(params.get("OldAddrInfo"))
        self.ProcessingTasks = params.get("ProcessingTasks")
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = ObjectTask()
                obj._deserialize(item)
                self.Tasks.append(obj)
        self.NetServiceId = params.get("NetServiceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatabaseTables(AbstractModel):
    """Database table information

    """

    def __init__(self):
        r"""
        :param Database: Database name
Note: This field may return null, indicating that no valid values can be obtained.
        :type Database: str
        :param Tables: Table name list
Note: This field may return null, indicating that no valid values can be obtained.
        :type Tables: list of str
        """
        self.Database = None
        self.Tables = None


    def _deserialize(self, params):
        self.Database = params.get("Database")
        self.Tables = params.get("Tables")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAuditRuleTemplatesRequest(AbstractModel):
    """DeleteAuditRuleTemplates request structure.

    """

    def __init__(self):
        r"""
        :param RuleTemplateIds: Audit rule template ID
        :type RuleTemplateIds: list of str
        """
        self.RuleTemplateIds = None


    def _deserialize(self, params):
        self.RuleTemplateIds = params.get("RuleTemplateIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAuditRuleTemplatesResponse(AbstractModel):
    """DeleteAuditRuleTemplates response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteBackupRequest(AbstractModel):
    """DeleteBackup request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param SnapshotIdList: Backup file ID. This field is used by legacy versions and thus not recommended.
        :type SnapshotIdList: list of int
        :param BackupIds: Backup file ID. This field is recommended.
        :type BackupIds: list of int
        """
        self.ClusterId = None
        self.SnapshotIdList = None
        self.BackupIds = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.SnapshotIdList = params.get("SnapshotIdList")
        self.BackupIds = params.get("BackupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBackupResponse(AbstractModel):
    """DeleteBackup response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAccountsRequest(AbstractModel):
    """DescribeAccounts request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param AccountNames: List of accounts to be filtered
        :type AccountNames: list of str
        :param DbType: Database type. Valid values: 
<li> MYSQL </li>
This parameter has been disused.
        :type DbType: str
        :param Hosts: List of accounts to be filtered
        :type Hosts: list of str
        :param Limit: Maximum entries returned per page
        :type Limit: int
        :param Offset: Offset
        :type Offset: int
        """
        self.ClusterId = None
        self.AccountNames = None
        self.DbType = None
        self.Hosts = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.AccountNames = params.get("AccountNames")
        self.DbType = params.get("DbType")
        self.Hosts = params.get("Hosts")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAccountsResponse(AbstractModel):
    """DescribeAccounts response structure.

    """

    def __init__(self):
        r"""
        :param AccountSet: Database account list
Note: This field may return null, indicating that no valid values can be obtained.
        :type AccountSet: list of Account
        :param TotalCount: Total number of accounts
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AccountSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AccountSet") is not None:
            self.AccountSet = []
            for item in params.get("AccountSet"):
                obj = Account()
                obj._deserialize(item)
                self.AccountSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeAuditRuleTemplatesRequest(AbstractModel):
    """DescribeAuditRuleTemplates request structure.

    """

    def __init__(self):
        r"""
        :param RuleTemplateIds: Rule template ID
        :type RuleTemplateIds: list of str
        :param RuleTemplateNames: Rule template name
        :type RuleTemplateNames: list of str
        :param Limit: Number of results returned per request. Default value: `20`.
        :type Limit: int
        :param Offset: Offset. Default value: `0`.
        :type Offset: int
        """
        self.RuleTemplateIds = None
        self.RuleTemplateNames = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.RuleTemplateIds = params.get("RuleTemplateIds")
        self.RuleTemplateNames = params.get("RuleTemplateNames")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAuditRuleTemplatesResponse(AbstractModel):
    """DescribeAuditRuleTemplates response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible instances
        :type TotalCount: int
        :param Items: List of rule template details
Note: This field may return null, indicating that no valid values can be obtained.
        :type Items: list of AuditRuleTemplateInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Items = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = AuditRuleTemplateInfo()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAuditRuleWithInstanceIdsRequest(AbstractModel):
    """DescribeAuditRuleWithInstanceIds request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID. Currently, only one single instance can be queried.
        :type InstanceIds: list of str
        """
        self.InstanceIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAuditRuleWithInstanceIdsResponse(AbstractModel):
    """DescribeAuditRuleWithInstanceIds response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: None
        :type TotalCount: int
        :param Items: Audit rule information of the instance
Note: This field may return null, indicating that no valid values can be obtained.
        :type Items: list of InstanceAuditRule
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Items = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = InstanceAuditRule()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBackupConfigRequest(AbstractModel):
    """DescribeBackupConfig request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        """
        self.ClusterId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupConfigResponse(AbstractModel):
    """DescribeBackupConfig response structure.

    """

    def __init__(self):
        r"""
        :param BackupTimeBeg: Full backup start time. Value range: [0-24*3600]. For example, 0:00 AM, 1:00 AM, and 2:00 AM are represented by 0, 3600, and 7200, respectively
        :type BackupTimeBeg: int
        :param BackupTimeEnd: Full backup end time. Value range: [0-24*3600]. For example, 0:00 AM, 1:00 AM, and 2:00 AM are represented by 0, 3600, and 7200, respectively
        :type BackupTimeEnd: int
        :param ReserveDuration: Backup retention period in seconds. Backups will be cleared after this period elapses. 7 days is represented by 3600*24*7 = 604800
        :type ReserveDuration: int
        :param BackupFreq: Backup frequency. It is an array of 7 elements corresponding to Monday through Sunday. full: full backup; increment: incremental backup
Note: this field may return null, indicating that no valid values can be obtained.
        :type BackupFreq: list of str
        :param BackupType: Backup mode. logic: logic backup; snapshot: snapshot backup
Note: this field may return null, indicating that no valid values can be obtained.
        :type BackupType: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BackupTimeBeg = None
        self.BackupTimeEnd = None
        self.ReserveDuration = None
        self.BackupFreq = None
        self.BackupType = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BackupTimeBeg = params.get("BackupTimeBeg")
        self.BackupTimeEnd = params.get("BackupTimeEnd")
        self.ReserveDuration = params.get("ReserveDuration")
        self.BackupFreq = params.get("BackupFreq")
        self.BackupType = params.get("BackupType")
        self.RequestId = params.get("RequestId")


class DescribeBackupDownloadUrlRequest(AbstractModel):
    """DescribeBackupDownloadUrl request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param BackupId: Backup ID
        :type BackupId: int
        """
        self.ClusterId = None
        self.BackupId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.BackupId = params.get("BackupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupDownloadUrlResponse(AbstractModel):
    """DescribeBackupDownloadUrl response structure.

    """

    def __init__(self):
        r"""
        :param DownloadUrl: Backup download address
        :type DownloadUrl: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DownloadUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DownloadUrl = params.get("DownloadUrl")
        self.RequestId = params.get("RequestId")


class DescribeBackupListRequest(AbstractModel):
    """DescribeBackupList request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param Limit: The number of results to be returned. Value range: (0,100]
        :type Limit: int
        :param Offset: Record offset. Value range: [0,INF)
        :type Offset: int
        :param DbType: Database type. Valid values: 
<li> MYSQL </li>
        :type DbType: str
        :param BackupIds: Backup ID
        :type BackupIds: list of int
        :param BackupType: Backup type. Valid values: `snapshot` (snapshot backup), `logic` (logic backup).
        :type BackupType: str
        :param BackupMethod: Back mode. Valid values: `auto` (automatic backup), `manual` (manual backup)
        :type BackupMethod: str
        :param SnapShotType: 
        :type SnapShotType: str
        :param StartTime: Backup start time
        :type StartTime: str
        :param EndTime: Backup end time
        :type EndTime: str
        :param FileNames: 
        :type FileNames: list of str
        :param BackupNames: Backup alias, which supports fuzzy query.
        :type BackupNames: list of str
        :param SnapshotIdList: ID list of the snapshot backup
        :type SnapshotIdList: list of int
        """
        self.ClusterId = None
        self.Limit = None
        self.Offset = None
        self.DbType = None
        self.BackupIds = None
        self.BackupType = None
        self.BackupMethod = None
        self.SnapShotType = None
        self.StartTime = None
        self.EndTime = None
        self.FileNames = None
        self.BackupNames = None
        self.SnapshotIdList = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.DbType = params.get("DbType")
        self.BackupIds = params.get("BackupIds")
        self.BackupType = params.get("BackupType")
        self.BackupMethod = params.get("BackupMethod")
        self.SnapShotType = params.get("SnapShotType")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.FileNames = params.get("FileNames")
        self.BackupNames = params.get("BackupNames")
        self.SnapshotIdList = params.get("SnapshotIdList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupListResponse(AbstractModel):
    """DescribeBackupList response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of backup files
        :type TotalCount: int
        :param BackupList: Backup file list
        :type BackupList: list of BackupFileInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.BackupList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("BackupList") is not None:
            self.BackupList = []
            for item in params.get("BackupList"):
                obj = BackupFileInfo()
                obj._deserialize(item)
                self.BackupList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBinlogDownloadUrlRequest(AbstractModel):
    """DescribeBinlogDownloadUrl request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param BinlogId: Binlog file ID
        :type BinlogId: int
        """
        self.ClusterId = None
        self.BinlogId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.BinlogId = params.get("BinlogId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBinlogDownloadUrlResponse(AbstractModel):
    """DescribeBinlogDownloadUrl response structure.

    """

    def __init__(self):
        r"""
        :param DownloadUrl: Download address
        :type DownloadUrl: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DownloadUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DownloadUrl = params.get("DownloadUrl")
        self.RequestId = params.get("RequestId")


class DescribeBinlogSaveDaysRequest(AbstractModel):
    """DescribeBinlogSaveDays request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        """
        self.ClusterId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBinlogSaveDaysResponse(AbstractModel):
    """DescribeBinlogSaveDays response structure.

    """

    def __init__(self):
        r"""
        :param BinlogSaveDays: Binlog retention period in days
        :type BinlogSaveDays: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BinlogSaveDays = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BinlogSaveDays = params.get("BinlogSaveDays")
        self.RequestId = params.get("RequestId")


class DescribeBinlogsRequest(AbstractModel):
    """DescribeBinlogs request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param StartTime: Start time
        :type StartTime: str
        :param EndTime: End time
        :type EndTime: str
        :param Offset: Offset
        :type Offset: int
        :param Limit: Maximum number
        :type Limit: int
        """
        self.ClusterId = None
        self.StartTime = None
        self.EndTime = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBinlogsResponse(AbstractModel):
    """DescribeBinlogs response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of records
        :type TotalCount: int
        :param Binlogs: Binlog list
Note: This field may return null, indicating that no valid values can be obtained.
        :type Binlogs: list of BinlogItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Binlogs = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Binlogs") is not None:
            self.Binlogs = []
            for item in params.get("Binlogs"):
                obj = BinlogItem()
                obj._deserialize(item)
                self.Binlogs.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterDetailRequest(AbstractModel):
    """DescribeClusterDetail request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        """
        self.ClusterId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterDetailResponse(AbstractModel):
    """DescribeClusterDetail response structure.

    """

    def __init__(self):
        r"""
        :param Detail: Cluster details
        :type Detail: :class:`tencentcloud.cynosdb.v20190107.models.CynosdbClusterDetail`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Detail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Detail") is not None:
            self.Detail = CynosdbClusterDetail()
            self.Detail._deserialize(params.get("Detail"))
        self.RequestId = params.get("RequestId")


class DescribeClusterInstanceGrpsRequest(AbstractModel):
    """DescribeClusterInstanceGrps request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        """
        self.ClusterId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterInstanceGrpsResponse(AbstractModel):
    """DescribeClusterInstanceGrps response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of instance groups
        :type TotalCount: int
        :param InstanceGrpInfoList: Instance group list
        :type InstanceGrpInfoList: list of CynosdbInstanceGrp
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceGrpInfoList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceGrpInfoList") is not None:
            self.InstanceGrpInfoList = []
            for item in params.get("InstanceGrpInfoList"):
                obj = CynosdbInstanceGrp()
                obj._deserialize(item)
                self.InstanceGrpInfoList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterParamsRequest(AbstractModel):
    """DescribeClusterParams request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param ParamName: Parameter name
        :type ParamName: str
        """
        self.ClusterId = None
        self.ParamName = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ParamName = params.get("ParamName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClusterParamsResponse(AbstractModel):
    """DescribeClusterParams response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of parameters
        :type TotalCount: int
        :param Items: Instance parameter list
Note: This field may return null, indicating that no valid values can be obtained.
        :type Items: list of ParamInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Items = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = ParamInfo()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClustersRequest(AbstractModel):
    """DescribeClusters request structure.

    """

    def __init__(self):
        r"""
        :param DbType: Engine type. Currently, `MYSQL` is supported.
        :type DbType: str
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100
        :type Limit: int
        :param Offset: Record offset. Default value: 0
        :type Offset: int
        :param OrderBy: Sort by field. Valid values:
<li> CREATETIME: creation time</li>
<li> PERIODENDTIME: expiration time</li>
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values:
<li> ASC: ascending</li>
<li> DESC: descending</li>
        :type OrderByType: str
        :param Filters: Filter. If more than one filter exists, the logical relationship between these filters is `AND`.
        :type Filters: list of QueryFilter
        """
        self.DbType = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None
        self.Filters = None


    def _deserialize(self, params):
        self.DbType = params.get("DbType")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = QueryFilter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClustersResponse(AbstractModel):
    """DescribeClusters response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of clusters
        :type TotalCount: int
        :param ClusterSet: Cluster list
        :type ClusterSet: list of CynosdbCluster
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ClusterSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ClusterSet") is not None:
            self.ClusterSet = []
            for item in params.get("ClusterSet"):
                obj = CynosdbCluster()
                obj._deserialize(item)
                self.ClusterSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBSecurityGroupsRequest(AbstractModel):
    """DescribeDBSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance group ID
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
        


class DescribeDBSecurityGroupsResponse(AbstractModel):
    """DescribeDBSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param Groups: Security group information
        :type Groups: list of SecurityGroup
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Groups = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Groups") is not None:
            self.Groups = []
            for item in params.get("Groups"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self.Groups.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeFlowRequest(AbstractModel):
    """DescribeFlow request structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task flow ID
        :type FlowId: int
        """
        self.FlowId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeFlowResponse(AbstractModel):
    """DescribeFlow response structure.

    """

    def __init__(self):
        r"""
        :param Status: Task flow status. Valid values: `0` (succeeded), `1` (failed), `2` (Processing).
        :type Status: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeInstanceDetailRequest(AbstractModel):
    """DescribeInstanceDetail request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
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
        


class DescribeInstanceDetailResponse(AbstractModel):
    """DescribeInstanceDetail response structure.

    """

    def __init__(self):
        r"""
        :param Detail: Instance details
        :type Detail: :class:`tencentcloud.cynosdb.v20190107.models.CynosdbInstanceDetail`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Detail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Detail") is not None:
            self.Detail = CynosdbInstanceDetail()
            self.Detail._deserialize(params.get("Detail"))
        self.RequestId = params.get("RequestId")


class DescribeInstanceSlowQueriesRequest(AbstractModel):
    """DescribeInstanceSlowQueries request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param StartTime: Transaction start time
        :type StartTime: str
        :param EndTime: Transaction end time
        :type EndTime: str
        :param Limit: Maximum number
        :type Limit: int
        :param Offset: Offset
        :type Offset: int
        :param Username: Username
        :type Username: str
        :param Host: Client host
        :type Host: str
        :param Database: Database name
        :type Database: str
        :param OrderBy: Sorting field. Valid values: QueryTime, LockTime, RowsExamined, RowsSent.
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: asc, desc.
        :type OrderByType: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Limit = None
        self.Offset = None
        self.Username = None
        self.Host = None
        self.Database = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Username = params.get("Username")
        self.Host = params.get("Host")
        self.Database = params.get("Database")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstanceSlowQueriesResponse(AbstractModel):
    """DescribeInstanceSlowQueries response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number
        :type TotalCount: int
        :param SlowQueries: Slow query record
        :type SlowQueries: list of SlowQueriesItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.SlowQueries = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("SlowQueries") is not None:
            self.SlowQueries = []
            for item in params.get("SlowQueries"):
                obj = SlowQueriesItem()
                obj._deserialize(item)
                self.SlowQueries.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceSpecsRequest(AbstractModel):
    """DescribeInstanceSpecs request structure.

    """

    def __init__(self):
        r"""
        :param DbType: Database type. Valid values: 
<li> MYSQL </li>
        :type DbType: str
        :param IncludeZoneStocks: Whether to return the AZ information.
        :type IncludeZoneStocks: bool
        """
        self.DbType = None
        self.IncludeZoneStocks = None


    def _deserialize(self, params):
        self.DbType = params.get("DbType")
        self.IncludeZoneStocks = params.get("IncludeZoneStocks")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstanceSpecsResponse(AbstractModel):
    """DescribeInstanceSpecs response structure.

    """

    def __init__(self):
        r"""
        :param InstanceSpecSet: Specification information
        :type InstanceSpecSet: list of InstanceSpec
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceSpecSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("InstanceSpecSet") is not None:
            self.InstanceSpecSet = []
            for item in params.get("InstanceSpecSet"):
                obj = InstanceSpec()
                obj._deserialize(item)
                self.InstanceSpecSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesRequest(AbstractModel):
    """DescribeInstances request structure.

    """

    def __init__(self):
        r"""
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100
        :type Limit: int
        :param Offset: Record offset. Default value: 0
        :type Offset: int
        :param OrderBy: Sort by field. Valid values:
<li> CREATETIME: creation time</li>
<li> PERIODENDTIME: expiration time</li>
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values:
<li> ASC: ascending</li>
<li> DESC: descending</li>
        :type OrderByType: str
        :param Filters: Filter. If more than one filter exists, the logical relationship between these filters is `AND`.
        :type Filters: list of QueryFilter
        :param DbType: Engine type. Currently, `MYSQL` is supported.
        :type DbType: str
        :param Status: Instance status. Valid values:
creating
running
isolating
isolated
activating: Removing the instance from isolation
offlining: Eliminating the instance
offlined: Instance eliminated
        :type Status: str
        :param InstanceIds: Instance ID list
        :type InstanceIds: list of str
        """
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None
        self.Filters = None
        self.DbType = None
        self.Status = None
        self.InstanceIds = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = QueryFilter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.DbType = params.get("DbType")
        self.Status = params.get("Status")
        self.InstanceIds = params.get("InstanceIds")
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
        :param TotalCount: Number of instances
        :type TotalCount: int
        :param InstanceSet: Instance list
        :type InstanceSet: list of CynosdbInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = CynosdbInstance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeMaintainPeriodRequest(AbstractModel):
    """DescribeMaintainPeriod request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
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
        


class DescribeMaintainPeriodResponse(AbstractModel):
    """DescribeMaintainPeriod response structure.

    """

    def __init__(self):
        r"""
        :param MaintainWeekDays: Maintenance days of the week
        :type MaintainWeekDays: list of str
        :param MaintainStartTime: Maintenance start time in seconds
        :type MaintainStartTime: int
        :param MaintainDuration: Maintenance duration in seconds
        :type MaintainDuration: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.MaintainWeekDays = None
        self.MaintainStartTime = None
        self.MaintainDuration = None
        self.RequestId = None


    def _deserialize(self, params):
        self.MaintainWeekDays = params.get("MaintainWeekDays")
        self.MaintainStartTime = params.get("MaintainStartTime")
        self.MaintainDuration = params.get("MaintainDuration")
        self.RequestId = params.get("RequestId")


class DescribeParamTemplatesRequest(AbstractModel):
    """DescribeParamTemplates request structure.

    """

    def __init__(self):
        r"""
        :param EngineVersions: Database engine version number
        :type EngineVersions: list of str
        :param TemplateNames: Template name
        :type TemplateNames: list of str
        :param TemplateIds: Template ID
        :type TemplateIds: list of int
        :param DbModes: Database Type. Valid values: `NORMAL`, `SERVERLESS`.
        :type DbModes: list of str
        :param Offset: Offset for query
        :type Offset: int
        :param Limit: Limit on queries
        :type Limit: int
        :param Products: Product type of the queried template
        :type Products: list of str
        :param TemplateTypes: Template type
        :type TemplateTypes: list of str
        :param EngineTypes: Version type
        :type EngineTypes: list of str
        :param OrderBy: The sorting order of the returned results
        :type OrderBy: str
        :param OrderDirection: Sorting order. Valid values: `desc`, `asc `.
        :type OrderDirection: str
        """
        self.EngineVersions = None
        self.TemplateNames = None
        self.TemplateIds = None
        self.DbModes = None
        self.Offset = None
        self.Limit = None
        self.Products = None
        self.TemplateTypes = None
        self.EngineTypes = None
        self.OrderBy = None
        self.OrderDirection = None


    def _deserialize(self, params):
        self.EngineVersions = params.get("EngineVersions")
        self.TemplateNames = params.get("TemplateNames")
        self.TemplateIds = params.get("TemplateIds")
        self.DbModes = params.get("DbModes")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Products = params.get("Products")
        self.TemplateTypes = params.get("TemplateTypes")
        self.EngineTypes = params.get("EngineTypes")
        self.OrderBy = params.get("OrderBy")
        self.OrderDirection = params.get("OrderDirection")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeParamTemplatesResponse(AbstractModel):
    """DescribeParamTemplates response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of parameter templates
        :type TotalCount: int
        :param Items: Parameter template information
        :type Items: list of ParamTemplateListInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Items = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = ParamTemplateListInfo()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProjectSecurityGroupsRequest(AbstractModel):
    """DescribeProjectSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param ProjectId: Project ID
        :type ProjectId: int
        :param Limit: Maximum entries returned per page
        :type Limit: int
        :param Offset: Offset
        :type Offset: int
        :param SearchKey: Search by keyword
        :type SearchKey: str
        """
        self.ProjectId = None
        self.Limit = None
        self.Offset = None
        self.SearchKey = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.SearchKey = params.get("SearchKey")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeProjectSecurityGroupsResponse(AbstractModel):
    """DescribeProjectSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param Groups: Security group details
        :type Groups: list of SecurityGroup
        :param Total: The total number of groups
        :type Total: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Groups = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Groups") is not None:
            self.Groups = []
            for item in params.get("Groups"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self.Groups.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeResourcesByDealNameRequest(AbstractModel):
    """DescribeResourcesByDealName request structure.

    """

    def __init__(self):
        r"""
        :param DealName: Order ID. (If the cluster is not delivered yet, the `DescribeResourcesByDealName` API may return the `InvalidParameterValue.DealNameNotFound` error. Call the API again until it succeeds.)
        :type DealName: str
        :param DealNames: Order ID, which can be used to query the resource information of multiple orders ID (If the cluster is not delivered yet, the `DescribeResourcesByDealName` API may return the `InvalidParameterValue.DealNameNotFound` error. Call the API again until it succeeds.)
        :type DealNames: list of str
        """
        self.DealName = None
        self.DealNames = None


    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.DealNames = params.get("DealNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeResourcesByDealNameResponse(AbstractModel):
    """DescribeResourcesByDealName response structure.

    """

    def __init__(self):
        r"""
        :param BillingResourceInfos: Billable resource ID information array
        :type BillingResourceInfos: list of BillingResourceInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BillingResourceInfos = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("BillingResourceInfos") is not None:
            self.BillingResourceInfos = []
            for item in params.get("BillingResourceInfos"):
                obj = BillingResourceInfo()
                obj._deserialize(item)
                self.BillingResourceInfos.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRollbackTimeRangeRequest(AbstractModel):
    """DescribeRollbackTimeRange request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        """
        self.ClusterId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeRollbackTimeRangeResponse(AbstractModel):
    """DescribeRollbackTimeRange response structure.

    """

    def __init__(self):
        r"""
        :param TimeRangeStart: Start time of valid rollback time range (disused)
Note: This field may return null, indicating that no valid values can be obtained.
        :type TimeRangeStart: str
        :param TimeRangeEnd: End time of valid rollback time range (disused)
Note: This field may return null, indicating that no valid values can be obtained.
        :type TimeRangeEnd: str
        :param RollbackTimeRanges: Time range available for rollback
        :type RollbackTimeRanges: list of RollbackTimeRange
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TimeRangeStart = None
        self.TimeRangeEnd = None
        self.RollbackTimeRanges = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TimeRangeStart = params.get("TimeRangeStart")
        self.TimeRangeEnd = params.get("TimeRangeEnd")
        if params.get("RollbackTimeRanges") is not None:
            self.RollbackTimeRanges = []
            for item in params.get("RollbackTimeRanges"):
                obj = RollbackTimeRange()
                obj._deserialize(item)
                self.RollbackTimeRanges.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRollbackTimeValidityRequest(AbstractModel):
    """DescribeRollbackTimeValidity request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param ExpectTime: Expected time point to roll back to
        :type ExpectTime: str
        :param ExpectTimeThresh: Error tolerance range for rollback time point
        :type ExpectTimeThresh: int
        """
        self.ClusterId = None
        self.ExpectTime = None
        self.ExpectTimeThresh = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ExpectTime = params.get("ExpectTime")
        self.ExpectTimeThresh = params.get("ExpectTimeThresh")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeRollbackTimeValidityResponse(AbstractModel):
    """DescribeRollbackTimeValidity response structure.

    """

    def __init__(self):
        r"""
        :param PoolId: Storage `poolID`
        :type PoolId: int
        :param QueryId: Rollback task ID, which needs to be passed in when rolling back to this time point
        :type QueryId: int
        :param Status: Whether the time point is valid. pass: check passed; fail: check failed
        :type Status: str
        :param SuggestTime: Suggested time point. This value takes effect only if `Status` is `fail`
        :type SuggestTime: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.PoolId = None
        self.QueryId = None
        self.Status = None
        self.SuggestTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.PoolId = params.get("PoolId")
        self.QueryId = params.get("QueryId")
        self.Status = params.get("Status")
        self.SuggestTime = params.get("SuggestTime")
        self.RequestId = params.get("RequestId")


class DescribeZonesRequest(AbstractModel):
    """DescribeZones request structure.

    """

    def __init__(self):
        r"""
        :param IncludeVirtualZones: Whether the virtual zone is included.–
        :type IncludeVirtualZones: bool
        :param ShowPermission: Whether to display all AZs in a region and the user’s permissions in each AZ.
        :type ShowPermission: bool
        """
        self.IncludeVirtualZones = None
        self.ShowPermission = None


    def _deserialize(self, params):
        self.IncludeVirtualZones = params.get("IncludeVirtualZones")
        self.ShowPermission = params.get("ShowPermission")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeZonesResponse(AbstractModel):
    """DescribeZones response structure.

    """

    def __init__(self):
        r"""
        :param RegionSet: Region information
        :type RegionSet: list of SaleRegion
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RegionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("RegionSet") is not None:
            self.RegionSet = []
            for item in params.get("RegionSet"):
                obj = SaleRegion()
                obj._deserialize(item)
                self.RegionSet.append(obj)
        self.RequestId = params.get("RequestId")


class ExportInstanceSlowQueriesRequest(AbstractModel):
    """ExportInstanceSlowQueries request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param StartTime: Transaction start time
        :type StartTime: str
        :param EndTime: Transaction end time
        :type EndTime: str
        :param Limit: Maximum number
        :type Limit: int
        :param Offset: Offset
        :type Offset: int
        :param Username: Username
        :type Username: str
        :param Host: Client host
        :type Host: str
        :param Database: Database name
        :type Database: str
        :param FileType: File type. Valid values: csv, original.
        :type FileType: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Limit = None
        self.Offset = None
        self.Username = None
        self.Host = None
        self.Database = None
        self.FileType = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Username = params.get("Username")
        self.Host = params.get("Host")
        self.Database = params.get("Database")
        self.FileType = params.get("FileType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExportInstanceSlowQueriesResponse(AbstractModel):
    """ExportInstanceSlowQueries response structure.

    """

    def __init__(self):
        r"""
        :param FileContent: Slow query export content
        :type FileContent: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FileContent = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.RequestId = params.get("RequestId")


class InquirePriceCreateRequest(AbstractModel):
    """InquirePriceCreate request structure.

    """

    def __init__(self):
        r"""
        :param Zone: AZ
        :type Zone: str
        :param GoodsNum: Number of compute node to purchase
        :type GoodsNum: int
        :param InstancePayMode: Instance type for purchase. Valid values: `PREPAID`, `POSTPAID`, `SERVERLESS`.
        :type InstancePayMode: str
        :param StoragePayMode: Storage type for purchase. Valid values: `PREPAID`, `POSTPAID`.
        :type StoragePayMode: str
        :param Cpu: Number of CPU cores, which is required when `InstancePayMode` is `PREPAID` or `POSTPAID`.
        :type Cpu: int
        :param Memory: Memory size in GB, which is required when `InstancePayMode` is `PREPAID` or `POSTPAID`.
        :type Memory: int
        :param Ccu: CCU size, which is required when `InstancePayMode` is `SERVERLESS`.
        :type Ccu: float
        :param StorageLimit: Storage size, which is required when `StoragePayMode` is `PREPAID`.
        :type StorageLimit: int
        :param TimeSpan: Validity period, which is required when `InstancePayMode` is `PREPAID`.
        :type TimeSpan: int
        :param TimeUnit: Duration unit, which is required when `InstancePayMode` is `PREPAID`. Valid values: `m` (month), `d` (day).
        :type TimeUnit: str
        """
        self.Zone = None
        self.GoodsNum = None
        self.InstancePayMode = None
        self.StoragePayMode = None
        self.Cpu = None
        self.Memory = None
        self.Ccu = None
        self.StorageLimit = None
        self.TimeSpan = None
        self.TimeUnit = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.GoodsNum = params.get("GoodsNum")
        self.InstancePayMode = params.get("InstancePayMode")
        self.StoragePayMode = params.get("StoragePayMode")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Ccu = params.get("Ccu")
        self.StorageLimit = params.get("StorageLimit")
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceCreateResponse(AbstractModel):
    """InquirePriceCreate response structure.

    """

    def __init__(self):
        r"""
        :param InstancePrice: Instance price
        :type InstancePrice: :class:`tencentcloud.cynosdb.v20190107.models.TradePrice`
        :param StoragePrice: Storage price
        :type StoragePrice: :class:`tencentcloud.cynosdb.v20190107.models.TradePrice`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstancePrice = None
        self.StoragePrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("InstancePrice") is not None:
            self.InstancePrice = TradePrice()
            self.InstancePrice._deserialize(params.get("InstancePrice"))
        if params.get("StoragePrice") is not None:
            self.StoragePrice = TradePrice()
            self.StoragePrice._deserialize(params.get("StoragePrice"))
        self.RequestId = params.get("RequestId")


class InquirePriceRenewRequest(AbstractModel):
    """InquirePriceRenew request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param TimeSpan: Validity period, which needs to be used together with `TimeUnit`.
        :type TimeSpan: int
        :param TimeUnit: Unit of validity period, which needs to be used together with `TimeSpan`. Valid values: `d` (day), `m` (month).
        :type TimeUnit: str
        """
        self.ClusterId = None
        self.TimeSpan = None
        self.TimeUnit = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceRenewResponse(AbstractModel):
    """InquirePriceRenew response structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param InstanceIds: Instance ID list
        :type InstanceIds: list of str
        :param Prices: Price of instance specification in array
        :type Prices: list of TradePrice
        :param InstanceRealTotalPrice: Total renewal price of compute node
        :type InstanceRealTotalPrice: int
        :param StorageRealTotalPrice: Total renewal price of storage node
        :type StorageRealTotalPrice: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ClusterId = None
        self.InstanceIds = None
        self.Prices = None
        self.InstanceRealTotalPrice = None
        self.StorageRealTotalPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIds = params.get("InstanceIds")
        if params.get("Prices") is not None:
            self.Prices = []
            for item in params.get("Prices"):
                obj = TradePrice()
                obj._deserialize(item)
                self.Prices.append(obj)
        self.InstanceRealTotalPrice = params.get("InstanceRealTotalPrice")
        self.StorageRealTotalPrice = params.get("StorageRealTotalPrice")
        self.RequestId = params.get("RequestId")


class InstanceAuditRule(AbstractModel):
    """Audit rule details of the instance, which is an output parameter of the `DescribeAuditRuleWithInstanceIds` API.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param AuditRule: Whether the audit is rule audit. Valid values: `true` (rule audit), `false` (full audit).
Note: This field may return null, indicating that no valid values can be obtained.
        :type AuditRule: bool
        :param AuditRuleFilters: Audit rule details, which is valid only when `AuditRule` is `true`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type AuditRuleFilters: list of AuditRuleFilters
        """
        self.InstanceId = None
        self.AuditRule = None
        self.AuditRuleFilters = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.AuditRule = params.get("AuditRule")
        if params.get("AuditRuleFilters") is not None:
            self.AuditRuleFilters = []
            for item in params.get("AuditRuleFilters"):
                obj = AuditRuleFilters()
                obj._deserialize(item)
                self.AuditRuleFilters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceInitInfo(AbstractModel):
    """Instance initialization configuration information

    """

    def __init__(self):
        r"""
        :param Cpu: Instance CPU
        :type Cpu: int
        :param Memory: Instance memory
        :type Memory: int
        :param InstanceType: Instance type. Valid values:`rw`, `ro`.
        :type InstanceType: str
        :param InstanceCount: Number of the instances. Value range: 1-15.
        :type InstanceCount: int
        """
        self.Cpu = None
        self.Memory = None
        self.InstanceType = None
        self.InstanceCount = None


    def _deserialize(self, params):
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.InstanceType = params.get("InstanceType")
        self.InstanceCount = params.get("InstanceCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceNetInfo(AbstractModel):
    """Instance network information

    """

    def __init__(self):
        r"""
        :param InstanceGroupType: Network type
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceGroupType: str
        :param InstanceGroupId: Instance group ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceGroupId: str
        :param VpcId: VPC ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type VpcId: str
        :param SubnetId: Subnet ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type SubnetId: str
        :param NetType: Network type
Note: This field may return null, indicating that no valid values can be obtained.
        :type NetType: int
        :param Vip: VPC IP
Note: This field may return null, indicating that no valid values can be obtained.
        :type Vip: str
        :param Vport: VPC port
Note: This field may return null, indicating that no valid values can be obtained.
        :type Vport: int
        :param WanDomain: Public network domain name
Note: This field may return null, indicating that no valid values can be obtained.
        :type WanDomain: str
        :param WanIP: 
        :type WanIP: str
        :param WanPort: Public network port
Note: This field may return null, indicating that no valid values can be obtained.
        :type WanPort: int
        :param WanStatus: Public network status
Note: This field may return null, indicating that no valid values can be obtained.
        :type WanStatus: str
        """
        self.InstanceGroupType = None
        self.InstanceGroupId = None
        self.VpcId = None
        self.SubnetId = None
        self.NetType = None
        self.Vip = None
        self.Vport = None
        self.WanDomain = None
        self.WanIP = None
        self.WanPort = None
        self.WanStatus = None


    def _deserialize(self, params):
        self.InstanceGroupType = params.get("InstanceGroupType")
        self.InstanceGroupId = params.get("InstanceGroupId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.NetType = params.get("NetType")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.WanDomain = params.get("WanDomain")
        self.WanIP = params.get("WanIP")
        self.WanPort = params.get("WanPort")
        self.WanStatus = params.get("WanStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceSpec(AbstractModel):
    """Details of purchasable instance specifications. `Cpu` and `Memory` determine the instance specification during instance creation. The value range of the storage capacity is [MinStorageSize,MaxStorageSize]

    """

    def __init__(self):
        r"""
        :param Cpu: Number of instance CPU cores
        :type Cpu: int
        :param Memory: Instance memory in GB
        :type Memory: int
        :param MaxStorageSize: Maximum instance storage capacity GB
        :type MaxStorageSize: int
        :param MinStorageSize: Minimum instance storage capacity GB
        :type MinStorageSize: int
        :param HasStock: Whether there is an inventory.
        :type HasStock: bool
        :param MachineType: Machine type
        :type MachineType: str
        :param MaxIops: Maximum IOPS
        :type MaxIops: int
        :param MaxIoBandWidth: Maximum bandwidth
        :type MaxIoBandWidth: int
        :param ZoneStockInfos: Inventory information in a region
Note: This field may return null, indicating that no valid values can be obtained.
        :type ZoneStockInfos: list of ZoneStockInfo
        :param StockCount: Quantity in stock
Note: This field may return null, indicating that no valid values can be obtained.
        :type StockCount: int
        """
        self.Cpu = None
        self.Memory = None
        self.MaxStorageSize = None
        self.MinStorageSize = None
        self.HasStock = None
        self.MachineType = None
        self.MaxIops = None
        self.MaxIoBandWidth = None
        self.ZoneStockInfos = None
        self.StockCount = None


    def _deserialize(self, params):
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.MaxStorageSize = params.get("MaxStorageSize")
        self.MinStorageSize = params.get("MinStorageSize")
        self.HasStock = params.get("HasStock")
        self.MachineType = params.get("MachineType")
        self.MaxIops = params.get("MaxIops")
        self.MaxIoBandWidth = params.get("MaxIoBandWidth")
        if params.get("ZoneStockInfos") is not None:
            self.ZoneStockInfos = []
            for item in params.get("ZoneStockInfos"):
                obj = ZoneStockInfo()
                obj._deserialize(item)
                self.ZoneStockInfos.append(obj)
        self.StockCount = params.get("StockCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateClusterRequest(AbstractModel):
    """IsolateCluster request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param DbType: This parameter has been disused.
        :type DbType: str
        """
        self.ClusterId = None
        self.DbType = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.DbType = params.get("DbType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateClusterResponse(AbstractModel):
    """IsolateCluster response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task flow ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type FlowId: int
        :param DealNames: Refund order ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type DealNames: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.DealNames = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.DealNames = params.get("DealNames")
        self.RequestId = params.get("RequestId")


class IsolateInstanceRequest(AbstractModel):
    """IsolateInstance request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param InstanceIdList: Instance ID array
        :type InstanceIdList: list of str
        :param DbType: This parameter has been disused.
        :type DbType: str
        """
        self.ClusterId = None
        self.InstanceIdList = None
        self.DbType = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIdList = params.get("InstanceIdList")
        self.DbType = params.get("DbType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateInstanceResponse(AbstractModel):
    """IsolateInstance response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task flow ID
        :type FlowId: int
        :param DealNames: Order ID for isolated instance (prepaid instance)
Note: this field may return null, indicating that no valid values can be obtained.
        :type DealNames: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.DealNames = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.DealNames = params.get("DealNames")
        self.RequestId = params.get("RequestId")


class ModifiableInfo(AbstractModel):
    """Details of whether the parameter can be modified

    """


class ModifyAuditRuleTemplatesRequest(AbstractModel):
    """ModifyAuditRuleTemplates request structure.

    """

    def __init__(self):
        r"""
        :param RuleTemplateIds: Audit rule template ID
        :type RuleTemplateIds: list of str
        :param RuleFilters: Audit rule after modification
        :type RuleFilters: list of RuleFilters
        :param RuleTemplateName: New name of the rule template
        :type RuleTemplateName: str
        :param Description: New description of the rule template
        :type Description: str
        """
        self.RuleTemplateIds = None
        self.RuleFilters = None
        self.RuleTemplateName = None
        self.Description = None


    def _deserialize(self, params):
        self.RuleTemplateIds = params.get("RuleTemplateIds")
        if params.get("RuleFilters") is not None:
            self.RuleFilters = []
            for item in params.get("RuleFilters"):
                obj = RuleFilters()
                obj._deserialize(item)
                self.RuleFilters.append(obj)
        self.RuleTemplateName = params.get("RuleTemplateName")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAuditRuleTemplatesResponse(AbstractModel):
    """ModifyAuditRuleTemplates response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAuditServiceRequest(AbstractModel):
    """ModifyAuditService request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param LogExpireDay: Log retention period
        :type LogExpireDay: int
        :param HighLogExpireDay: Frequent log retention period
        :type HighLogExpireDay: int
        :param AuditAll: The parameter used to change the audit rule of the instance to full audit
        :type AuditAll: bool
        :param AuditRuleFilters: Rule audit
        :type AuditRuleFilters: list of AuditRuleFilters
        :param RuleTemplateIds: Rule template ID
        :type RuleTemplateIds: list of str
        """
        self.InstanceId = None
        self.LogExpireDay = None
        self.HighLogExpireDay = None
        self.AuditAll = None
        self.AuditRuleFilters = None
        self.RuleTemplateIds = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.LogExpireDay = params.get("LogExpireDay")
        self.HighLogExpireDay = params.get("HighLogExpireDay")
        self.AuditAll = params.get("AuditAll")
        if params.get("AuditRuleFilters") is not None:
            self.AuditRuleFilters = []
            for item in params.get("AuditRuleFilters"):
                obj = AuditRuleFilters()
                obj._deserialize(item)
                self.AuditRuleFilters.append(obj)
        self.RuleTemplateIds = params.get("RuleTemplateIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAuditServiceResponse(AbstractModel):
    """ModifyAuditService response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBackupConfigRequest(AbstractModel):
    """ModifyBackupConfig request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param BackupTimeBeg: Full backup start time. Value range: [0-24*3600]. For example, 0:00 AM, 1:00 AM, and 2:00 AM are represented by 0, 3600, and 7200, respectively
        :type BackupTimeBeg: int
        :param BackupTimeEnd: Full backup end time. Value range: [0-24*3600]. For example, 0:00 AM, 1:00 AM, and 2:00 AM are represented by 0, 3600, and 7200, respectively.
        :type BackupTimeEnd: int
        :param ReserveDuration: Backup retention period in seconds. Backups will be cleared after this period elapses. 7 days is represented by 3600*24*7 = 604800. Maximum value: 158112000.
        :type ReserveDuration: int
        :param BackupFreq: Backup frequency. It is an array of 7 elements corresponding to Monday through Sunday. full: full backup; increment: incremental backup. This parameter cannot be modified currently and doesn't need to be entered.
        :type BackupFreq: list of str
        :param BackupType: Backup mode. logic: logic backup; snapshot: snapshot backup. This parameter cannot be modified currently and doesn't need to be entered.
        :type BackupType: str
        """
        self.ClusterId = None
        self.BackupTimeBeg = None
        self.BackupTimeEnd = None
        self.ReserveDuration = None
        self.BackupFreq = None
        self.BackupType = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.BackupTimeBeg = params.get("BackupTimeBeg")
        self.BackupTimeEnd = params.get("BackupTimeEnd")
        self.ReserveDuration = params.get("ReserveDuration")
        self.BackupFreq = params.get("BackupFreq")
        self.BackupType = params.get("BackupType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBackupConfigResponse(AbstractModel):
    """ModifyBackupConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBackupNameRequest(AbstractModel):
    """ModifyBackupName request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param BackupId: Backup file ID
        :type BackupId: int
        :param BackupName: Backup name, which can contain up to 60 characters.
        :type BackupName: str
        """
        self.ClusterId = None
        self.BackupId = None
        self.BackupName = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.BackupId = params.get("BackupId")
        self.BackupName = params.get("BackupName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBackupNameResponse(AbstractModel):
    """ModifyBackupName response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyClusterNameRequest(AbstractModel):
    """ModifyClusterName request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param ClusterName: Cluster name
        :type ClusterName: str
        """
        self.ClusterId = None
        self.ClusterName = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ClusterName = params.get("ClusterName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterNameResponse(AbstractModel):
    """ModifyClusterName response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyClusterParamRequest(AbstractModel):
    """ModifyClusterParam request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param ParamList: List of the parameters to be modified. Each element in the list is a combination of `ParamName`, `CurrentValue`, and `OldValue`. `ParamName` is the parameter name; `CurrentValue` is the current value; `OldValue` is the old value that doesn’t need to be verified.
        :type ParamList: list of ParamItem
        :param IsInMaintainPeriod: Valid values: `yes` (execute during maintenance time), `no` (execute now)
        :type IsInMaintainPeriod: str
        """
        self.ClusterId = None
        self.ParamList = None
        self.IsInMaintainPeriod = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        if params.get("ParamList") is not None:
            self.ParamList = []
            for item in params.get("ParamList"):
                obj = ParamItem()
                obj._deserialize(item)
                self.ParamList.append(obj)
        self.IsInMaintainPeriod = params.get("IsInMaintainPeriod")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterParamResponse(AbstractModel):
    """ModifyClusterParam response structure.

    """

    def __init__(self):
        r"""
        :param AsyncRequestId: Async request ID used to query the result
        :type AsyncRequestId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AsyncRequestId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.RequestId = params.get("RequestId")


class ModifyClusterSlaveZoneRequest(AbstractModel):
    """ModifyClusterSlaveZone request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param OldSlaveZone: Old replica AZ
        :type OldSlaveZone: str
        :param NewSlaveZone: New replica AZ
        :type NewSlaveZone: str
        """
        self.ClusterId = None
        self.OldSlaveZone = None
        self.NewSlaveZone = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.OldSlaveZone = params.get("OldSlaveZone")
        self.NewSlaveZone = params.get("NewSlaveZone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyClusterSlaveZoneResponse(AbstractModel):
    """ModifyClusterSlaveZone response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async FlowId
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceSecurityGroupsRequest(AbstractModel):
    """ModifyDBInstanceSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance group ID
        :type InstanceId: str
        :param SecurityGroupIds: List of IDs of security groups to be modified, which is an array of one or more security group IDs.
        :type SecurityGroupIds: list of str
        :param Zone: AZ
        :type Zone: str
        """
        self.InstanceId = None
        self.SecurityGroupIds = None
        self.Zone = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.Zone = params.get("Zone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceSecurityGroupsResponse(AbstractModel):
    """ModifyDBInstanceSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstanceNameRequest(AbstractModel):
    """ModifyInstanceName request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param InstanceName: Instance name
        :type InstanceName: str
        """
        self.InstanceId = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyInstanceNameResponse(AbstractModel):
    """ModifyInstanceName response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyMaintainPeriodConfigRequest(AbstractModel):
    """ModifyMaintainPeriodConfig request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param MaintainStartTime: Maintenance start time in seconds. For example, 03:00 AM is represented by 10800
        :type MaintainStartTime: int
        :param MaintainDuration: Maintenance duration in seconds. For example, one hour is represented by 3600
        :type MaintainDuration: int
        :param MaintainWeekDays: Maintenance days of the week. Valid values: [Mon, Tue, Wed, Thu, Fri, Sat, Sun].
        :type MaintainWeekDays: list of str
        """
        self.InstanceId = None
        self.MaintainStartTime = None
        self.MaintainDuration = None
        self.MaintainWeekDays = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.MaintainStartTime = params.get("MaintainStartTime")
        self.MaintainDuration = params.get("MaintainDuration")
        self.MaintainWeekDays = params.get("MaintainWeekDays")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyMaintainPeriodConfigResponse(AbstractModel):
    """ModifyMaintainPeriodConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyParamItem(AbstractModel):
    """Information of the modified instance parameter

    """

    def __init__(self):
        r"""
        :param ParamName: Parameter name
        :type ParamName: str
        :param CurrentValue: Current parameter value
        :type CurrentValue: str
        :param OldValue: Old parameter value, which is used only in output parameters.
Note: This field may return null, indicating that no valid values can be obtained.
        :type OldValue: str
        """
        self.ParamName = None
        self.CurrentValue = None
        self.OldValue = None


    def _deserialize(self, params):
        self.ParamName = params.get("ParamName")
        self.CurrentValue = params.get("CurrentValue")
        self.OldValue = params.get("OldValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyVipVportRequest(AbstractModel):
    """ModifyVipVport request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param InstanceGrpId: Instance group ID
        :type InstanceGrpId: str
        :param Vip: Target IP to be modified
        :type Vip: str
        :param Vport: Target port to be modified
        :type Vport: int
        :param DbType: Database type. Valid values: 
<li> MYSQL </li>
        :type DbType: str
        :param OldIpReserveHours: Valid hours of old IPs. If it is set to `0` hours, the IPs will be released immediately.
        :type OldIpReserveHours: int
        """
        self.ClusterId = None
        self.InstanceGrpId = None
        self.Vip = None
        self.Vport = None
        self.DbType = None
        self.OldIpReserveHours = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceGrpId = params.get("InstanceGrpId")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.DbType = params.get("DbType")
        self.OldIpReserveHours = params.get("OldIpReserveHours")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyVipVportResponse(AbstractModel):
    """ModifyVipVport response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class Module(AbstractModel):
    """Modules supported by the system

    """

    def __init__(self):
        r"""
        :param IsDisable: Whether it is supported. Valid values: `yes`, `no`.
        :type IsDisable: str
        :param ModuleName: Module name
        :type ModuleName: str
        """
        self.IsDisable = None
        self.ModuleName = None


    def _deserialize(self, params):
        self.IsDisable = params.get("IsDisable")
        self.ModuleName = params.get("ModuleName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NetAddr(AbstractModel):
    """Network information

    """

    def __init__(self):
        r"""
        :param Vip: Private network IP
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Vip: str
        :param Vport: Private network port number
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Vport: int
        :param WanDomain: Public network domain name
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type WanDomain: str
        :param WanPort: Public network port number
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type WanPort: int
        :param NetType: Network type. Valid values: `ro` (read-only), `rw` or `ha` (read-write)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type NetType: str
        :param UniqSubnetId: Subnet ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type UniqSubnetId: str
        :param UniqVpcId: VPC ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type UniqVpcId: str
        :param Description: Description
Note: This field may return null, indicating that no valid values can be obtained.
        :type Description: str
        :param WanIP: Public IP
Note: This field may return null, indicating that no valid values can be obtained.
        :type WanIP: str
        :param WanStatus: Public network status
Note: This field may return null, indicating that no valid values can be obtained.
        :type WanStatus: str
        """
        self.Vip = None
        self.Vport = None
        self.WanDomain = None
        self.WanPort = None
        self.NetType = None
        self.UniqSubnetId = None
        self.UniqVpcId = None
        self.Description = None
        self.WanIP = None
        self.WanStatus = None


    def _deserialize(self, params):
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.WanDomain = params.get("WanDomain")
        self.WanPort = params.get("WanPort")
        self.NetType = params.get("NetType")
        self.UniqSubnetId = params.get("UniqSubnetId")
        self.UniqVpcId = params.get("UniqVpcId")
        self.Description = params.get("Description")
        self.WanIP = params.get("WanIP")
        self.WanStatus = params.get("WanStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NewAccount(AbstractModel):
    """The newly created x08 account

    """

    def __init__(self):
        r"""
        :param AccountName: Account name, which can contain 1-16 letters, digits, and underscores. It must begin with a letter and end with a letter or digit.
        :type AccountName: str
        :param AccountPassword: Password, which can contain 8-64 characters.
        :type AccountPassword: str
        :param Host: Host
        :type Host: str
        :param Description: Description
        :type Description: str
        :param MaxUserConnections: Maximum number of user connections, which cannot be above 10,240.
        :type MaxUserConnections: int
        """
        self.AccountName = None
        self.AccountPassword = None
        self.Host = None
        self.Description = None
        self.MaxUserConnections = None


    def _deserialize(self, params):
        self.AccountName = params.get("AccountName")
        self.AccountPassword = params.get("AccountPassword")
        self.Host = params.get("Host")
        self.Description = params.get("Description")
        self.MaxUserConnections = params.get("MaxUserConnections")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ObjectTask(AbstractModel):
    """Task information

    """

    def __init__(self):
        r"""
        :param TaskId: Auto-Incrementing task ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type TaskId: int
        :param TaskType: Task type
Note: this field may return null, indicating that no valid values can be obtained.
        :type TaskType: str
        :param TaskStatus: Task status
Note: this field may return null, indicating that no valid values can be obtained.
        :type TaskStatus: str
        :param ObjectId: Task ID (cluster ID | instance group ID | instance ID)
Note: this field may return null, indicating that no valid values can be obtained.
        :type ObjectId: str
        :param ObjectType: Task type
Note: this field may return null, indicating that no valid values can be obtained.
        :type ObjectType: str
        """
        self.TaskId = None
        self.TaskType = None
        self.TaskStatus = None
        self.ObjectId = None
        self.ObjectType = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.TaskType = params.get("TaskType")
        self.TaskStatus = params.get("TaskStatus")
        self.ObjectId = params.get("ObjectId")
        self.ObjectType = params.get("ObjectType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OfflineClusterRequest(AbstractModel):
    """OfflineCluster request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        """
        self.ClusterId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OfflineClusterResponse(AbstractModel):
    """OfflineCluster response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task flow ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class OfflineInstanceRequest(AbstractModel):
    """OfflineInstance request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param InstanceIdList: Instance ID array
        :type InstanceIdList: list of str
        """
        self.ClusterId = None
        self.InstanceIdList = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIdList = params.get("InstanceIdList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OfflineInstanceResponse(AbstractModel):
    """OfflineInstance response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task flow ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class OldAddrInfo(AbstractModel):
    """Database address

    """

    def __init__(self):
        r"""
        :param Vip: IP
Note: This field may return null, indicating that no valid values can be obtained.
        :type Vip: str
        :param Vport: Port
Note: This field may return null, indicating that no valid values can be obtained.
        :type Vport: int
        :param ReturnTime: Expected valid hours of old IPs
Note: This field may return null, indicating that no valid values can be obtained.
        :type ReturnTime: str
        """
        self.Vip = None
        self.Vport = None
        self.ReturnTime = None


    def _deserialize(self, params):
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.ReturnTime = params.get("ReturnTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OpenAuditServiceRequest(AbstractModel):
    """OpenAuditService request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param LogExpireDay: Log retention period
        :type LogExpireDay: int
        :param HighLogExpireDay: Frequent log retention period
        :type HighLogExpireDay: int
        :param AuditRuleFilters: Audit rule. If both this parameter and `RuleTemplateIds` are left empty, full audit will be applied.
        :type AuditRuleFilters: list of AuditRuleFilters
        :param RuleTemplateIds: Rule template ID. If both this parameter and `AuditRuleFilters` are left empty, full audit will be applied.
        :type RuleTemplateIds: list of str
        """
        self.InstanceId = None
        self.LogExpireDay = None
        self.HighLogExpireDay = None
        self.AuditRuleFilters = None
        self.RuleTemplateIds = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.LogExpireDay = params.get("LogExpireDay")
        self.HighLogExpireDay = params.get("HighLogExpireDay")
        if params.get("AuditRuleFilters") is not None:
            self.AuditRuleFilters = []
            for item in params.get("AuditRuleFilters"):
                obj = AuditRuleFilters()
                obj._deserialize(item)
                self.AuditRuleFilters.append(obj)
        self.RuleTemplateIds = params.get("RuleTemplateIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OpenAuditServiceResponse(AbstractModel):
    """OpenAuditService response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ParamInfo(AbstractModel):
    """Parameter information

    """

    def __init__(self):
        r"""
        :param CurrentValue: Current value
        :type CurrentValue: str
        :param Default: Default value
        :type Default: str
        :param EnumValue: List of valid values when parameter type is `enum`, `string` or `bool`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type EnumValue: list of str
        :param Max: Maximum value when parameter type is `float` or `integer`.
        :type Max: str
        :param Min: Minimum value when parameter type is `float` or `integer`.
        :type Min: str
        :param ParamName: Parameter name
        :type ParamName: str
        :param NeedReboot: Whether to restart the instance for the modified parameters to take effect.
        :type NeedReboot: int
        :param ParamType: Parameter type: `integer`, `float`, `string`, `enum`, `bool`.
        :type ParamType: str
        :param MatchType: Match type. Regex can be used when parameter type is `string`. Valid value: `multiVal`.
        :type MatchType: str
        :param MatchValue: Match values, which will be separated by semicolon when match type is `multiVal`.
        :type MatchValue: str
        :param Description: Parameter description
        :type Description: str
        :param IsGlobal: Whether it is global parameter
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsGlobal: int
        :param ModifiableInfo: Whether the parameter can be modified
Note: This field may return null, indicating that no valid values can be obtained.
        :type ModifiableInfo: :class:`tencentcloud.cynosdb.v20190107.models.ModifiableInfo`
        :param IsFunc: Whether it is a function
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsFunc: bool
        :param Func: Function
Note: This field may return null, indicating that no valid values can be obtained.
        :type Func: str
        """
        self.CurrentValue = None
        self.Default = None
        self.EnumValue = None
        self.Max = None
        self.Min = None
        self.ParamName = None
        self.NeedReboot = None
        self.ParamType = None
        self.MatchType = None
        self.MatchValue = None
        self.Description = None
        self.IsGlobal = None
        self.ModifiableInfo = None
        self.IsFunc = None
        self.Func = None


    def _deserialize(self, params):
        self.CurrentValue = params.get("CurrentValue")
        self.Default = params.get("Default")
        self.EnumValue = params.get("EnumValue")
        self.Max = params.get("Max")
        self.Min = params.get("Min")
        self.ParamName = params.get("ParamName")
        self.NeedReboot = params.get("NeedReboot")
        self.ParamType = params.get("ParamType")
        self.MatchType = params.get("MatchType")
        self.MatchValue = params.get("MatchValue")
        self.Description = params.get("Description")
        self.IsGlobal = params.get("IsGlobal")
        if params.get("ModifiableInfo") is not None:
            self.ModifiableInfo = ModifiableInfo()
            self.ModifiableInfo._deserialize(params.get("ModifiableInfo"))
        self.IsFunc = params.get("IsFunc")
        self.Func = params.get("Func")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParamItem(AbstractModel):
    """Parameter to be modified

    """

    def __init__(self):
        r"""
        :param ParamName: Parameter name
        :type ParamName: str
        :param CurrentValue: New value
        :type CurrentValue: str
        :param OldValue: Original value
        :type OldValue: str
        """
        self.ParamName = None
        self.CurrentValue = None
        self.OldValue = None


    def _deserialize(self, params):
        self.ParamName = params.get("ParamName")
        self.CurrentValue = params.get("CurrentValue")
        self.OldValue = params.get("OldValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParamTemplateListInfo(AbstractModel):
    """Parameter template information

    """

    def __init__(self):
        r"""
        :param Id: Parameter template ID
        :type Id: int
        :param TemplateName: Parameter template name
        :type TemplateName: str
        :param TemplateDescription: Parameter template description
        :type TemplateDescription: str
        :param EngineVersion: Engine version
        :type EngineVersion: str
        :param DbMode: Database Type. Valid values: `NORMAL`, `SERVERLESS`.
        :type DbMode: str
        :param ParamInfoSet: Parameter template details
Note: This field may return null, indicating that no valid values can be obtained.
        :type ParamInfoSet: list of TemplateParamInfo
        """
        self.Id = None
        self.TemplateName = None
        self.TemplateDescription = None
        self.EngineVersion = None
        self.DbMode = None
        self.ParamInfoSet = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.TemplateName = params.get("TemplateName")
        self.TemplateDescription = params.get("TemplateDescription")
        self.EngineVersion = params.get("EngineVersion")
        self.DbMode = params.get("DbMode")
        if params.get("ParamInfoSet") is not None:
            self.ParamInfoSet = []
            for item in params.get("ParamInfoSet"):
                obj = TemplateParamInfo()
                obj._deserialize(item)
                self.ParamInfoSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PauseServerlessRequest(AbstractModel):
    """PauseServerless request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param ForcePause: Whether to pause forcibly and ignore the current user connections. Valid values: `0` (no), `1` (yes). Default value: `1`
        :type ForcePause: int
        """
        self.ClusterId = None
        self.ForcePause = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ForcePause = params.get("ForcePause")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PauseServerlessResponse(AbstractModel):
    """PauseServerless response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class PolicyRule(AbstractModel):
    """Security group rule

    """

    def __init__(self):
        r"""
        :param Action: Policy, which can be `ACCEPT` or `DROP`
        :type Action: str
        :param CidrIp: Source IP or IP range, such as 192.168.0.0/16
        :type CidrIp: str
        :param PortRange: Port
        :type PortRange: str
        :param IpProtocol: Network protocol, such as UDP and TCP
        :type IpProtocol: str
        :param ServiceModule: Protocol port ID or protocol port group ID.
        :type ServiceModule: str
        :param AddressModule: IP address ID or IP address group ID.
        :type AddressModule: str
        :param Id: id
        :type Id: str
        :param Desc: Description
        :type Desc: str
        """
        self.Action = None
        self.CidrIp = None
        self.PortRange = None
        self.IpProtocol = None
        self.ServiceModule = None
        self.AddressModule = None
        self.Id = None
        self.Desc = None


    def _deserialize(self, params):
        self.Action = params.get("Action")
        self.CidrIp = params.get("CidrIp")
        self.PortRange = params.get("PortRange")
        self.IpProtocol = params.get("IpProtocol")
        self.ServiceModule = params.get("ServiceModule")
        self.AddressModule = params.get("AddressModule")
        self.Id = params.get("Id")
        self.Desc = params.get("Desc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryFilter(AbstractModel):
    """Query filter

    """

    def __init__(self):
        r"""
        :param Names: Search field. Valid values: "InstanceId", "ProjectId", "InstanceName", "Vip"
        :type Names: list of str
        :param Values: Search string
        :type Values: list of str
        :param ExactMatch: Whether to use exact match
        :type ExactMatch: bool
        :param Name: Search field
        :type Name: str
        :param Operator: Operator
        :type Operator: str
        """
        self.Names = None
        self.Values = None
        self.ExactMatch = None
        self.Name = None
        self.Operator = None


    def _deserialize(self, params):
        self.Names = params.get("Names")
        self.Values = params.get("Values")
        self.ExactMatch = params.get("ExactMatch")
        self.Name = params.get("Name")
        self.Operator = params.get("Operator")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RemoveClusterSlaveZoneRequest(AbstractModel):
    """RemoveClusterSlaveZone request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param SlaveZone: Replica AZ
        :type SlaveZone: str
        """
        self.ClusterId = None
        self.SlaveZone = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.SlaveZone = params.get("SlaveZone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RemoveClusterSlaveZoneResponse(AbstractModel):
    """RemoveClusterSlaveZone response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async FlowId
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ResetAccountPasswordRequest(AbstractModel):
    """ResetAccountPassword request structure.

    """

    def __init__(self):
        r"""
        :param AccountName: Database account name
        :type AccountName: str
        :param AccountPassword: New password of the database account
        :type AccountPassword: str
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param Host: Host. Default value: `%`
        :type Host: str
        """
        self.AccountName = None
        self.AccountPassword = None
        self.ClusterId = None
        self.Host = None


    def _deserialize(self, params):
        self.AccountName = params.get("AccountName")
        self.AccountPassword = params.get("AccountPassword")
        self.ClusterId = params.get("ClusterId")
        self.Host = params.get("Host")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetAccountPasswordResponse(AbstractModel):
    """ResetAccountPassword response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RestartInstanceRequest(AbstractModel):
    """RestartInstance request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
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
        


class RestartInstanceResponse(AbstractModel):
    """RestartInstance response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ResumeServerlessRequest(AbstractModel):
    """ResumeServerless request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        """
        self.ClusterId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResumeServerlessResponse(AbstractModel):
    """ResumeServerless response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class RollbackTimeRange(AbstractModel):
    """Rollback time range

    """

    def __init__(self):
        r"""
        :param TimeRangeStart: Start time
        :type TimeRangeStart: str
        :param TimeRangeEnd: End time
        :type TimeRangeEnd: str
        """
        self.TimeRangeStart = None
        self.TimeRangeEnd = None


    def _deserialize(self, params):
        self.TimeRangeStart = params.get("TimeRangeStart")
        self.TimeRangeEnd = params.get("TimeRangeEnd")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RuleFilters(AbstractModel):
    """Filter of the audit rule

    """

    def __init__(self):
        r"""
        :param Type: Filter parameter name of the audit rule. Valid values: `host` (client IP), `user` (database account), `dbName` (database name), `sqlType` (SQL type), `sql` (SQL statement).
        :type Type: str
        :param Compare: Filter match type of the audit rule. Valid values: `INC` (including), `EXC` (excluding), `EQS` (equal to), `NEQ` (not equal to).
        :type Compare: str
        :param Value: Filter match value of the audit rule
        :type Value: list of str
        """
        self.Type = None
        self.Compare = None
        self.Value = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Compare = params.get("Compare")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SaleRegion(AbstractModel):
    """Information of a purchasable region

    """

    def __init__(self):
        r"""
        :param Region: Region name
        :type Region: str
        :param RegionId: Numeric ID of a region
        :type RegionId: int
        :param RegionZh: Region name
        :type RegionZh: str
        :param ZoneSet: List of purchasable AZs
        :type ZoneSet: list of SaleZone
        :param DbType: Engine type
        :type DbType: str
        :param Modules: Supported modules in a region
        :type Modules: list of Module
        """
        self.Region = None
        self.RegionId = None
        self.RegionZh = None
        self.ZoneSet = None
        self.DbType = None
        self.Modules = None


    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionId = params.get("RegionId")
        self.RegionZh = params.get("RegionZh")
        if params.get("ZoneSet") is not None:
            self.ZoneSet = []
            for item in params.get("ZoneSet"):
                obj = SaleZone()
                obj._deserialize(item)
                self.ZoneSet.append(obj)
        self.DbType = params.get("DbType")
        if params.get("Modules") is not None:
            self.Modules = []
            for item in params.get("Modules"):
                obj = Module()
                obj._deserialize(item)
                self.Modules.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SaleZone(AbstractModel):
    """Information of a purchasable AZ

    """

    def __init__(self):
        r"""
        :param Zone: AZ name
        :type Zone: str
        :param ZoneId: Numeric ID of an AZ
        :type ZoneId: int
        :param ZoneZh: AZ name
        :type ZoneZh: str
        :param IsSupportServerless: Whether serverless cluster is supported. Valid values: <br>
`0`: No<br>
`1`: Yes
        :type IsSupportServerless: int
        :param IsSupportNormal: Whether standard cluster is supported. Valid values: <br>
`0`: No<br>
`1`: Yes
        :type IsSupportNormal: int
        :param PhysicalZone: Physical zone
        :type PhysicalZone: str
        :param HasPermission: Whether the user has AZ permission
Note: This field may return null, indicating that no valid values can be obtained.
        :type HasPermission: bool
        :param IsWholeRdmaZone: Whether it is a full-linkage RDMA AZ.
        :type IsWholeRdmaZone: str
        """
        self.Zone = None
        self.ZoneId = None
        self.ZoneZh = None
        self.IsSupportServerless = None
        self.IsSupportNormal = None
        self.PhysicalZone = None
        self.HasPermission = None
        self.IsWholeRdmaZone = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneId = params.get("ZoneId")
        self.ZoneZh = params.get("ZoneZh")
        self.IsSupportServerless = params.get("IsSupportServerless")
        self.IsSupportNormal = params.get("IsSupportNormal")
        self.PhysicalZone = params.get("PhysicalZone")
        self.HasPermission = params.get("HasPermission")
        self.IsWholeRdmaZone = params.get("IsWholeRdmaZone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SearchClusterDatabasesRequest(AbstractModel):
    """SearchClusterDatabases request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: The cluster ID
        :type ClusterId: str
        :param Database: Database name
        :type Database: str
        :param MatchType: Whether to search exactly
Valid values: `0` (fuzzy search), `1` (exact search). 
Default value: `0`.
        :type MatchType: int
        """
        self.ClusterId = None
        self.Database = None
        self.MatchType = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Database = params.get("Database")
        self.MatchType = params.get("MatchType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SearchClusterDatabasesResponse(AbstractModel):
    """SearchClusterDatabases response structure.

    """

    def __init__(self):
        r"""
        :param Databases: Database List
Note: This field may return null, indicating that no valid values can be obtained.
        :type Databases: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Databases = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Databases = params.get("Databases")
        self.RequestId = params.get("RequestId")


class SearchClusterTablesRequest(AbstractModel):
    """SearchClusterTables request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param Database: Database name
        :type Database: str
        :param Table: Data table name
        :type Table: str
        :param TableType: Data table type. Valid values:
`view`: Only return to view,
`base_table`: Only return to basic table,
`all`: Return to view and table.
        :type TableType: str
        """
        self.ClusterId = None
        self.Database = None
        self.Table = None
        self.TableType = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Database = params.get("Database")
        self.Table = params.get("Table")
        self.TableType = params.get("TableType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SearchClusterTablesResponse(AbstractModel):
    """SearchClusterTables response structure.

    """

    def __init__(self):
        r"""
        :param Tables: Data table list
Note: This field may return null, indicating that no valid values can be obtained.
        :type Tables: list of DatabaseTables
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Tables = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Tables") is not None:
            self.Tables = []
            for item in params.get("Tables"):
                obj = DatabaseTables()
                obj._deserialize(item)
                self.Tables.append(obj)
        self.RequestId = params.get("RequestId")


class SecurityGroup(AbstractModel):
    """Security group details

    """

    def __init__(self):
        r"""
        :param ProjectId: Project ID
        :type ProjectId: int
        :param CreateTime: Creation time in the format of yyyy-mm-dd hh:mm:ss
        :type CreateTime: str
        :param Inbound: Inbound rule
        :type Inbound: list of PolicyRule
        :param Outbound: Outbound rule
        :type Outbound: list of PolicyRule
        :param SecurityGroupId: Security group ID
        :type SecurityGroupId: str
        :param SecurityGroupName: Security group name
        :type SecurityGroupName: str
        :param SecurityGroupRemark: Security group remarks
        :type SecurityGroupRemark: str
        """
        self.ProjectId = None
        self.CreateTime = None
        self.Inbound = None
        self.Outbound = None
        self.SecurityGroupId = None
        self.SecurityGroupName = None
        self.SecurityGroupRemark = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.CreateTime = params.get("CreateTime")
        if params.get("Inbound") is not None:
            self.Inbound = []
            for item in params.get("Inbound"):
                obj = PolicyRule()
                obj._deserialize(item)
                self.Inbound.append(obj)
        if params.get("Outbound") is not None:
            self.Outbound = []
            for item in params.get("Outbound"):
                obj = PolicyRule()
                obj._deserialize(item)
                self.Outbound.append(obj)
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.SecurityGroupName = params.get("SecurityGroupName")
        self.SecurityGroupRemark = params.get("SecurityGroupRemark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetRenewFlagRequest(AbstractModel):
    """SetRenewFlag request structure.

    """

    def __init__(self):
        r"""
        :param ResourceIds: ID of the instance to be manipulated
        :type ResourceIds: list of str
        :param AutoRenewFlag: Auto-renewal flag. 0: normal renewal, 1: auto-renewal, 2: no renewal.
        :type AutoRenewFlag: int
        """
        self.ResourceIds = None
        self.AutoRenewFlag = None


    def _deserialize(self, params):
        self.ResourceIds = params.get("ResourceIds")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetRenewFlagResponse(AbstractModel):
    """SetRenewFlag response structure.

    """

    def __init__(self):
        r"""
        :param Count: Number of successfully manipulated instances
        :type Count: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Count = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.RequestId = params.get("RequestId")


class SlowQueriesItem(AbstractModel):
    """Slow query information of the instance

    """

    def __init__(self):
        r"""
        :param Timestamp: Execution timestamp
        :type Timestamp: int
        :param QueryTime: Execution duration in seconds
        :type QueryTime: float
        :param SqlText: SQL statement
        :type SqlText: str
        :param UserHost: Client host
        :type UserHost: str
        :param UserName: Username
        :type UserName: str
        :param Database: Database name
        :type Database: str
        :param LockTime: Lock duration in seconds
        :type LockTime: float
        :param RowsExamined: Number of scanned rows
        :type RowsExamined: int
        :param RowsSent: Number of returned rows
        :type RowsSent: int
        :param SqlTemplate: SQL template
        :type SqlTemplate: str
        :param SqlMd5: MD5 value of the SQL statement
        :type SqlMd5: str
        """
        self.Timestamp = None
        self.QueryTime = None
        self.SqlText = None
        self.UserHost = None
        self.UserName = None
        self.Database = None
        self.LockTime = None
        self.RowsExamined = None
        self.RowsSent = None
        self.SqlTemplate = None
        self.SqlMd5 = None


    def _deserialize(self, params):
        self.Timestamp = params.get("Timestamp")
        self.QueryTime = params.get("QueryTime")
        self.SqlText = params.get("SqlText")
        self.UserHost = params.get("UserHost")
        self.UserName = params.get("UserName")
        self.Database = params.get("Database")
        self.LockTime = params.get("LockTime")
        self.RowsExamined = params.get("RowsExamined")
        self.RowsSent = params.get("RowsSent")
        self.SqlTemplate = params.get("SqlTemplate")
        self.SqlMd5 = params.get("SqlMd5")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchClusterVpcRequest(AbstractModel):
    """SwitchClusterVpc request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param UniqVpcId: VPC ID in string
        :type UniqVpcId: str
        :param UniqSubnetId: Subnet ID in string
        :type UniqSubnetId: str
        :param OldIpReserveHours: Valid hours of old IP
        :type OldIpReserveHours: int
        """
        self.ClusterId = None
        self.UniqVpcId = None
        self.UniqSubnetId = None
        self.OldIpReserveHours = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.UniqVpcId = params.get("UniqVpcId")
        self.UniqSubnetId = params.get("UniqSubnetId")
        self.OldIpReserveHours = params.get("OldIpReserveHours")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchClusterVpcResponse(AbstractModel):
    """SwitchClusterVpc response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class SwitchClusterZoneRequest(AbstractModel):
    """SwitchClusterZone request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param OldZone: The current AZ
        :type OldZone: str
        :param NewZone: New AZ
        :type NewZone: str
        :param IsInMaintainPeriod: Valid values: `yes` (execute during maintenance time), `no` (execute now)
        :type IsInMaintainPeriod: str
        """
        self.ClusterId = None
        self.OldZone = None
        self.NewZone = None
        self.IsInMaintainPeriod = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.OldZone = params.get("OldZone")
        self.NewZone = params.get("NewZone")
        self.IsInMaintainPeriod = params.get("IsInMaintainPeriod")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchClusterZoneResponse(AbstractModel):
    """SwitchClusterZone response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async FlowId
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class SwitchProxyVpcRequest(AbstractModel):
    """SwitchProxyVpc request structure.

    """

    def __init__(self):
        r"""
        :param ClusterId: Cluster ID
        :type ClusterId: str
        :param UniqVpcId: VPC ID in string
        :type UniqVpcId: str
        :param UniqSubnetId: Subnet ID in string
        :type UniqSubnetId: str
        :param OldIpReserveHours: Valid hours of old IP
        :type OldIpReserveHours: int
        :param ProxyGroupId: Database proxy group ID (required), which can be obtained through the `DescribeProxies` API.
        :type ProxyGroupId: str
        """
        self.ClusterId = None
        self.UniqVpcId = None
        self.UniqSubnetId = None
        self.OldIpReserveHours = None
        self.ProxyGroupId = None


    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.UniqVpcId = params.get("UniqVpcId")
        self.UniqSubnetId = params.get("UniqSubnetId")
        self.OldIpReserveHours = params.get("OldIpReserveHours")
        self.ProxyGroupId = params.get("ProxyGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchProxyVpcResponse(AbstractModel):
    """SwitchProxyVpc response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class Tag(AbstractModel):
    """Information of tags associated with cluster, including `TagKey` and `TagValue`

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
        


class TemplateParamInfo(AbstractModel):
    """Parameter template details

    """

    def __init__(self):
        r"""
        :param CurrentValue: Current value
        :type CurrentValue: str
        :param Default: Default value
        :type Default: str
        :param EnumValue: The collection of valid value types when parameter type is `enum`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type EnumValue: list of str
        :param Max: Maximum value when parameter type is `float` or `integer`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Max: str
        :param Min: Minimum value when parameter type is `float` or `integer`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Min: str
        :param ParamName: Parameter name
        :type ParamName: str
        :param NeedReboot: Whether to restart the instance for the parameter to take effect
        :type NeedReboot: int
        :param Description: Parameter description
        :type Description: str
        :param ParamType: Parameter type. Valid value: `integer`, `float`, `string`, `enum`.
        :type ParamType: str
        """
        self.CurrentValue = None
        self.Default = None
        self.EnumValue = None
        self.Max = None
        self.Min = None
        self.ParamName = None
        self.NeedReboot = None
        self.Description = None
        self.ParamType = None


    def _deserialize(self, params):
        self.CurrentValue = params.get("CurrentValue")
        self.Default = params.get("Default")
        self.EnumValue = params.get("EnumValue")
        self.Max = params.get("Max")
        self.Min = params.get("Min")
        self.ParamName = params.get("ParamName")
        self.NeedReboot = params.get("NeedReboot")
        self.Description = params.get("Description")
        self.ParamType = params.get("ParamType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TradePrice(AbstractModel):
    """Billing details

    """

    def __init__(self):
        r"""
        :param TotalPrice: The non-discounted total price of monthly subscribed resources (unit: US cent)
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalPrice: int
        :param Discount: Total discount. `100` means no discount.
        :type Discount: float
        :param TotalPriceDiscount: The discounted total price of monthly subscribed resources (unit: US cent). If a discount is applied, `TotalPriceDiscount` will be the product of `TotalPrice` and `Discount`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalPriceDiscount: int
        :param UnitPrice: The non-discounted unit price of pay-as-you-go resources (unit: US cent)
Note: This field may return null, indicating that no valid values can be obtained.
        :type UnitPrice: int
        :param UnitPriceDiscount: The discounted unit price of pay-as-you-go resources (unit: US cent). If a discount is applied, `UnitPriceDiscount` will be the product of `UnitPrice` and `Discount`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type UnitPriceDiscount: int
        :param ChargeUnit: Price unit
        :type ChargeUnit: str
        """
        self.TotalPrice = None
        self.Discount = None
        self.TotalPriceDiscount = None
        self.UnitPrice = None
        self.UnitPriceDiscount = None
        self.ChargeUnit = None


    def _deserialize(self, params):
        self.TotalPrice = params.get("TotalPrice")
        self.Discount = params.get("Discount")
        self.TotalPriceDiscount = params.get("TotalPriceDiscount")
        self.UnitPrice = params.get("UnitPrice")
        self.UnitPriceDiscount = params.get("UnitPriceDiscount")
        self.ChargeUnit = params.get("ChargeUnit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpgradeInstanceRequest(AbstractModel):
    """UpgradeInstance request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Cpu: Database CPU
        :type Cpu: int
        :param Memory: Database memory in GB
        :type Memory: int
        :param UpgradeType: Upgrade type. Valid values: upgradeImmediate, upgradeInMaintain
        :type UpgradeType: str
        :param StorageLimit: This parameter has been disused.
        :type StorageLimit: int
        :param AutoVoucher: Whether to automatically select a voucher. 1: yes; 0: no. Default value: 0
        :type AutoVoucher: int
        :param DbType: This parameter has been disused.
        :type DbType: str
        :param DealMode: Transaction mode. Valid values: `0` (place and pay for an order), `1` (place an order)
        :type DealMode: int
        :param UpgradeMode: Valid values: `NormalUpgrade` (Normal mode), `FastUpgrade` (QuickChange). If the system detects that the configuration modification process will cause a momentary disconnection, the process will be terminated.
        :type UpgradeMode: str
        """
        self.InstanceId = None
        self.Cpu = None
        self.Memory = None
        self.UpgradeType = None
        self.StorageLimit = None
        self.AutoVoucher = None
        self.DbType = None
        self.DealMode = None
        self.UpgradeMode = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.UpgradeType = params.get("UpgradeType")
        self.StorageLimit = params.get("StorageLimit")
        self.AutoVoucher = params.get("AutoVoucher")
        self.DbType = params.get("DbType")
        self.DealMode = params.get("DealMode")
        self.UpgradeMode = params.get("UpgradeMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpgradeInstanceResponse(AbstractModel):
    """UpgradeInstance response structure.

    """

    def __init__(self):
        r"""
        :param TranId: Freezing transaction ID
Note: this field may return null, indicating that no valid values can be obtained.
        :type TranId: str
        :param BigDealIds: Big order ID.
Note: this field may return null, indicating that no valid values can be obtained.
        :type BigDealIds: list of str
        :param DealNames: Order ID
        :type DealNames: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TranId = None
        self.BigDealIds = None
        self.DealNames = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TranId = params.get("TranId")
        self.BigDealIds = params.get("BigDealIds")
        self.DealNames = params.get("DealNames")
        self.RequestId = params.get("RequestId")


class ZoneStockInfo(AbstractModel):
    """Inventory information in an AZ

    """

    def __init__(self):
        r"""
        :param Zone: AZ
        :type Zone: str
        :param HasStock: Whether there is an inventory.
        :type HasStock: bool
        :param StockCount: Quantity in stock
        :type StockCount: int
        """
        self.Zone = None
        self.HasStock = None
        self.StockCount = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.HasStock = params.get("HasStock")
        self.StockCount = params.get("StockCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        