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


class AccountInfo(AbstractModel):
    """Account information

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-lnp6j617
        :type DBInstanceId: str
        :param UserName: Account
        :type UserName: str
        :param Remark: Account remarks
        :type Remark: str
        :param Status: Account status. 1: creating, 2: normal, 3: modifying, 4: resetting password, -1: deleting
        :type Status: int
        :param CreateTime: Account creation time
        :type CreateTime: str
        :param UpdateTime: Account last modified time
        :type UpdateTime: str
        """
        self.DBInstanceId = None
        self.UserName = None
        self.Remark = None
        self.Status = None
        self.CreateTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.UserName = params.get("UserName")
        self.Remark = params.get("Remark")
        self.Status = params.get("Status")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddDBInstanceToReadOnlyGroupRequest(AbstractModel):
    """AddDBInstanceToReadOnlyGroup request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param ReadOnlyGroupId: RO group ID
        :type ReadOnlyGroupId: str
        """
        self.DBInstanceId = None
        self.ReadOnlyGroupId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddDBInstanceToReadOnlyGroupResponse(AbstractModel):
    """AddDBInstanceToReadOnlyGroup response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class AnalysisItems(AbstractModel):
    """Detailed analysis of a slow query statement with abstract parameter values, which is returned by the `DescribeSlowQueryAnalysis` API

    """

    def __init__(self):
        r"""
        :param DatabaseName: The name of the database queried by the slow query statement
        :type DatabaseName: str
        :param UserName: The name of the user who executes the slow query statement
        :type UserName: str
        :param NormalQuery: The slow query statement whose parameter values are abstracted
        :type NormalQuery: str
        :param ClientAddr: The address of the client that executes the slow query statement
        :type ClientAddr: str
        :param CallNum: The number of executions of the slow query statement during the specified period of time
        :type CallNum: int
        :param CallPercent: The ratio (in decimal form) of the number of executions of the slow query statement to that of all slow query statements during the specified period of time
        :type CallPercent: float
        :param CostTime: The total execution time of the slow query statement during the specified period of time
        :type CostTime: float
        :param CostPercent: The ratio (in decimal form) of the total execution time of the slow query statement to that of all slow query statements during the specified period of time
        :type CostPercent: float
        :param MinCostTime: The shortest execution time (in ms) of the slow query statement during the specified period of time
        :type MinCostTime: float
        :param MaxCostTime: The longest execution time (in ms) of the slow query statement during the specified period of time
        :type MaxCostTime: float
        :param AvgCostTime: The average execution time (in ms) of the slow query statement during the specified period of time
        :type AvgCostTime: float
        :param FirstTime: The timestamp when the slow query statement starts to execute for the first time during the specified period of time
        :type FirstTime: str
        :param LastTime: The timestamp when the slow query statement starts to execute for the last time during the specified period of time
        :type LastTime: str
        """
        self.DatabaseName = None
        self.UserName = None
        self.NormalQuery = None
        self.ClientAddr = None
        self.CallNum = None
        self.CallPercent = None
        self.CostTime = None
        self.CostPercent = None
        self.MinCostTime = None
        self.MaxCostTime = None
        self.AvgCostTime = None
        self.FirstTime = None
        self.LastTime = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.UserName = params.get("UserName")
        self.NormalQuery = params.get("NormalQuery")
        self.ClientAddr = params.get("ClientAddr")
        self.CallNum = params.get("CallNum")
        self.CallPercent = params.get("CallPercent")
        self.CostTime = params.get("CostTime")
        self.CostPercent = params.get("CostPercent")
        self.MinCostTime = params.get("MinCostTime")
        self.MaxCostTime = params.get("MaxCostTime")
        self.AvgCostTime = params.get("AvgCostTime")
        self.FirstTime = params.get("FirstTime")
        self.LastTime = params.get("LastTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BackupDownloadRestriction(AbstractModel):
    """Restriction information for downloading a backup

    """

    def __init__(self):
        r"""
        :param RestrictionType: Type of the network restrictions for downloading backup files. Valid values: `NONE` (backups can be downloaded over both private and public networks), `INTRANET` (backups can only be downloaded over the private network), `CUSTOMIZE` (backups can be downloaded over specified VPCs or at specified IPs).
        :type RestrictionType: str
        :param VpcRestrictionEffect: Whether VPC is allowed. Valid values: `ALLOW` (allow), `DENY` (deny).
        :type VpcRestrictionEffect: str
        :param VpcIdSet: Whether it is allowed to download the VPC ID list of the backup files.
        :type VpcIdSet: list of str
        :param IpRestrictionEffect: Whether IP is allowed. Valid values: `ALLOW` (allow), `DENY` (deny).
        :type IpRestrictionEffect: str
        :param IpSet: Whether it is allowed to download IP list of the backup files.
        :type IpSet: list of str
        """
        self.RestrictionType = None
        self.VpcRestrictionEffect = None
        self.VpcIdSet = None
        self.IpRestrictionEffect = None
        self.IpSet = None


    def _deserialize(self, params):
        self.RestrictionType = params.get("RestrictionType")
        self.VpcRestrictionEffect = params.get("VpcRestrictionEffect")
        self.VpcIdSet = params.get("VpcIdSet")
        self.IpRestrictionEffect = params.get("IpRestrictionEffect")
        self.IpSet = params.get("IpSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BackupPlan(AbstractModel):
    """Backup plan

    """

    def __init__(self):
        r"""
        :param BackupPeriod: Backup cycle
        :type BackupPeriod: str
        :param BaseBackupRetentionPeriod: Retention period of basic backups
        :type BaseBackupRetentionPeriod: int
        :param MinBackupStartTime: The earliest time to start a backup
        :type MinBackupStartTime: str
        :param MaxBackupStartTime: The latest time to start a backup
        :type MaxBackupStartTime: str
        """
        self.BackupPeriod = None
        self.BaseBackupRetentionPeriod = None
        self.MinBackupStartTime = None
        self.MaxBackupStartTime = None


    def _deserialize(self, params):
        self.BackupPeriod = params.get("BackupPeriod")
        self.BaseBackupRetentionPeriod = params.get("BaseBackupRetentionPeriod")
        self.MinBackupStartTime = params.get("MinBackupStartTime")
        self.MaxBackupStartTime = params.get("MaxBackupStartTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BackupSummary(AbstractModel):
    """Instance backup statistics

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param LogBackupCount: Number of log backups of an instance
        :type LogBackupCount: int
        :param LogBackupSize: Size of log backups of an instance
        :type LogBackupSize: int
        :param ManualBaseBackupCount: Number of manually created full backups of an instance
        :type ManualBaseBackupCount: int
        :param ManualBaseBackupSize: Size of manually created full backups of an instance
        :type ManualBaseBackupSize: int
        :param AutoBaseBackupCount: Number of automatically created full backups of an instance
        :type AutoBaseBackupCount: int
        :param AutoBaseBackupSize: Size of automatically created full backups of an instance
        :type AutoBaseBackupSize: int
        :param TotalBackupCount: Total number of backups
        :type TotalBackupCount: int
        :param TotalBackupSize: Total backup size
        :type TotalBackupSize: int
        """
        self.DBInstanceId = None
        self.LogBackupCount = None
        self.LogBackupSize = None
        self.ManualBaseBackupCount = None
        self.ManualBaseBackupSize = None
        self.AutoBaseBackupCount = None
        self.AutoBaseBackupSize = None
        self.TotalBackupCount = None
        self.TotalBackupSize = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.LogBackupCount = params.get("LogBackupCount")
        self.LogBackupSize = params.get("LogBackupSize")
        self.ManualBaseBackupCount = params.get("ManualBaseBackupCount")
        self.ManualBaseBackupSize = params.get("ManualBaseBackupSize")
        self.AutoBaseBackupCount = params.get("AutoBaseBackupCount")
        self.AutoBaseBackupSize = params.get("AutoBaseBackupSize")
        self.TotalBackupCount = params.get("TotalBackupCount")
        self.TotalBackupSize = params.get("TotalBackupSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BaseBackup(AbstractModel):
    """Full backup information of a database

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param Id: Unique ID of a backup file
        :type Id: str
        :param Name: Backup file name.
        :type Name: str
        :param BackupMethod: Backup method, including physical and logical.
        :type BackupMethod: str
        :param BackupMode: Backup mode, including automatic and manual.
        :type BackupMode: str
        :param State: Backup task status
        :type State: str
        :param Size: Backup set size in bytes
        :type Size: int
        :param StartTime: Backup start time
        :type StartTime: str
        :param FinishTime: Backup end time
        :type FinishTime: str
        :param ExpireTime: Backup expiration time
        :type ExpireTime: str
        """
        self.DBInstanceId = None
        self.Id = None
        self.Name = None
        self.BackupMethod = None
        self.BackupMode = None
        self.State = None
        self.Size = None
        self.StartTime = None
        self.FinishTime = None
        self.ExpireTime = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.BackupMethod = params.get("BackupMethod")
        self.BackupMode = params.get("BackupMode")
        self.State = params.get("State")
        self.Size = params.get("Size")
        self.StartTime = params.get("StartTime")
        self.FinishTime = params.get("FinishTime")
        self.ExpireTime = params.get("ExpireTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ClassInfo(AbstractModel):
    """Database instance specification

    """

    def __init__(self):
        r"""
        :param SpecCode: Specification ID
        :type SpecCode: str
        :param CPU: Number of CPU cores
        :type CPU: int
        :param Memory: Memory size in MB
        :type Memory: int
        :param MaxStorage: Maximum storage capacity in GB supported by this specification
        :type MaxStorage: int
        :param MinStorage: Minimum storage capacity in GB supported by this specification
        :type MinStorage: int
        :param QPS: Estimated QPS for this specification
        :type QPS: int
        """
        self.SpecCode = None
        self.CPU = None
        self.Memory = None
        self.MaxStorage = None
        self.MinStorage = None
        self.QPS = None


    def _deserialize(self, params):
        self.SpecCode = params.get("SpecCode")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")
        self.MaxStorage = params.get("MaxStorage")
        self.MinStorage = params.get("MinStorage")
        self.QPS = params.get("QPS")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CloneDBInstanceRequest(AbstractModel):
    """CloneDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: ID of the original instance to be cloned.
        :type DBInstanceId: str
        :param SpecCode: Purchasable specification ID, which can be obtained through the `SpecCode` field in the returned value of the `DescribeProductConfig` API.
        :type SpecCode: str
        :param Storage: Instance storage capacity in GB.
        :type Storage: int
        :param Period: Valid period in months of the purchased instance. Valid values: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `24`, `36`. This parameter is set to `1` when the pay-as-you-go billing mode is used.
        :type Period: int
        :param AutoRenewFlag: Renewal flag. Valid values: `0` (manual renewal), `1` (auto-renewal). Default value: `0`.
        :type AutoRenewFlag: int
        :param VpcId: VPC ID.
        :type VpcId: str
        :param SubnetId: ID of a subnet in the VPC specified by `VpcId`.
        :type SubnetId: str
        :param Name: Name of the purchased instance.
        :type Name: str
        :param InstanceChargeType: Instance billing mode. Valid values: `PREPAID` (monthly subscription), `POSTPAID_BY_HOUR` (pay-as-you-go).
        :type InstanceChargeType: str
        :param SecurityGroupIds: Security group ID.
        :type SecurityGroupIds: list of str
        :param ProjectId: Project ID.
        :type ProjectId: int
        :param TagList: The information of tags to be bound with the purchased instance. This parameter is left empty by default.
        :type TagList: list of Tag
        :param DBNodeSet: This parameter is required if you purchase a multi-AZ deployed instance.
        :type DBNodeSet: list of DBNode
        :param AutoVoucher: Whether to automatically use vouchers. Valid values: `1` (yes), `0` (no). Default value: `0`.
        :type AutoVoucher: int
        :param VoucherIds: Voucher ID list.
        :type VoucherIds: str
        :param ActivityId: Campaign ID.
        :type ActivityId: int
        :param BackupSetId: Basic backup set ID.
        :type BackupSetId: str
        :param RecoveryTargetTime: Restoration point in time.
        :type RecoveryTargetTime: str
        """
        self.DBInstanceId = None
        self.SpecCode = None
        self.Storage = None
        self.Period = None
        self.AutoRenewFlag = None
        self.VpcId = None
        self.SubnetId = None
        self.Name = None
        self.InstanceChargeType = None
        self.SecurityGroupIds = None
        self.ProjectId = None
        self.TagList = None
        self.DBNodeSet = None
        self.AutoVoucher = None
        self.VoucherIds = None
        self.ActivityId = None
        self.BackupSetId = None
        self.RecoveryTargetTime = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.SpecCode = params.get("SpecCode")
        self.Storage = params.get("Storage")
        self.Period = params.get("Period")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Name = params.get("Name")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.ProjectId = params.get("ProjectId")
        if params.get("TagList") is not None:
            self.TagList = []
            for item in params.get("TagList"):
                obj = Tag()
                obj._deserialize(item)
                self.TagList.append(obj)
        if params.get("DBNodeSet") is not None:
            self.DBNodeSet = []
            for item in params.get("DBNodeSet"):
                obj = DBNode()
                obj._deserialize(item)
                self.DBNodeSet.append(obj)
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        self.ActivityId = params.get("ActivityId")
        self.BackupSetId = params.get("BackupSetId")
        self.RecoveryTargetTime = params.get("RecoveryTargetTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CloneDBInstanceResponse(AbstractModel):
    """CloneDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param DealName: Order ID.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DealName: str
        :param BillId: Bill ID.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type BillId: str
        :param DBInstanceId: ID of the cloned instance, which will be returned only when the instance is pay-as-you-go.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DBInstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealName = None
        self.BillId = None
        self.DBInstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.BillId = params.get("BillId")
        self.DBInstanceId = params.get("DBInstanceId")
        self.RequestId = params.get("RequestId")


class CloseDBExtranetAccessRequest(AbstractModel):
    """CloseDBExtranetAccess request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-6r233v55
        :type DBInstanceId: str
        :param IsIpv6: Whether to disable public network access over IPv6 address. Valid values: 1 (yes), 0 (no)
        :type IsIpv6: int
        """
        self.DBInstanceId = None
        self.IsIpv6 = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.IsIpv6 = params.get("IsIpv6")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CloseDBExtranetAccessResponse(AbstractModel):
    """CloseDBExtranetAccess response structure.

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


class CloseServerlessDBExtranetAccessRequest(AbstractModel):
    """CloseServerlessDBExtranetAccess request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Unique ID of an instance
        :type DBInstanceId: str
        :param DBInstanceName: Instance name
        :type DBInstanceName: str
        """
        self.DBInstanceId = None
        self.DBInstanceName = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.DBInstanceName = params.get("DBInstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CloseServerlessDBExtranetAccessResponse(AbstractModel):
    """CloseServerlessDBExtranetAccess response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateBaseBackupRequest(AbstractModel):
    """CreateBaseBackup request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBaseBackupResponse(AbstractModel):
    """CreateBaseBackup response structure.

    """

    def __init__(self):
        r"""
        :param BaseBackupId: Full backup set ID
        :type BaseBackupId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BaseBackupId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BaseBackupId = params.get("BaseBackupId")
        self.RequestId = params.get("RequestId")


class CreateDBInstanceNetworkAccessRequest(AbstractModel):
    """CreateDBInstanceNetworkAccess request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-6bwgamo3.
        :type DBInstanceId: str
        :param VpcId: Unified VPC ID.
        :type VpcId: str
        :param SubnetId: Subnet ID.
        :type SubnetId: str
        :param IsAssignVip: Whether to manually assign the VIP. Valid values: `true` (manually assign), `false` (automatically assign).
        :type IsAssignVip: bool
        :param Vip: Target VIP.
        :type Vip: str
        """
        self.DBInstanceId = None
        self.VpcId = None
        self.SubnetId = None
        self.IsAssignVip = None
        self.Vip = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.IsAssignVip = params.get("IsAssignVip")
        self.Vip = params.get("Vip")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDBInstanceNetworkAccessResponse(AbstractModel):
    """CreateDBInstanceNetworkAccess response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class CreateDBInstancesRequest(AbstractModel):
    """CreateDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param SpecCode: Purchasable specification ID, which can be obtained through the `SpecCode` field in the returned value of the `DescribeProductConfig` API.
        :type SpecCode: str
        :param Storage: Instance capacity size in GB.
        :type Storage: int
        :param InstanceCount: Number of instances purchased at a time. Value range: 1-100.
        :type InstanceCount: int
        :param Period: Length of purchase in months. Currently, only 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, and 36 are supported.
        :type Period: int
        :param Zone: AZ ID, which can be obtained through the `Zone` field in the returned value of the `DescribeZones` API.
        :type Zone: str
        :param ProjectId: Project ID.
        :type ProjectId: int
        :param DBVersion: PostgreSQL version. If it is specified, an instance running the latest kernel of PostgreSQL `DBVersion` will be created. You must pass in at least one of the following parameters: DBVersion, DBMajorVersion, DBKernelVersion.
        :type DBVersion: str
        :param InstanceChargeType: Instance billing type.
        :type InstanceChargeType: str
        :param AutoVoucher: Whether to automatically use vouchers. 1: yes, 0: no. Default value: no.
        :type AutoVoucher: int
        :param VoucherIds: Voucher ID list (only one voucher can be specified currently).
        :type VoucherIds: list of str
        :param VpcId: VPC ID.
        :type VpcId: str
        :param SubnetId: VPC subnet ID.
        :type SubnetId: str
        :param AutoRenewFlag: Renewal flag. 0: normal renewal (default), 1: auto-renewal.
        :type AutoRenewFlag: int
        :param ActivityId: Activity ID
        :type ActivityId: int
        :param Name: Instance name (which will be supported in the future)
        :type Name: str
        :param NeedSupportIpv6: Whether to support IPv6 address access. Valid values: 1 (yes), 0 (no)
        :type NeedSupportIpv6: int
        :param TagList: The information of tags to be associated with instances. This parameter is left empty by default.
        :type TagList: list of Tag
        :param SecurityGroupIds: Security group ID
        :type SecurityGroupIds: list of str
        :param DBMajorVersion: PostgreSQL major version. If it is specified, an instance running the latest kernel of PostgreSQL `DBMajorVersion` will be created. You must pass in at least one of the following parameters: DBMajorVersion, DBVersion, DBKernelVersion.
        :type DBMajorVersion: str
        :param DBKernelVersion: PostgreSQL kernel version. If it is specified, an instance running the latest kernel of PostgreSQL `DBKernelVersion` will be created. You must pass in one of the following parameters: DBKernelVersion, DBVersion, DBMajorVersion.
        :type DBKernelVersion: str
        """
        self.SpecCode = None
        self.Storage = None
        self.InstanceCount = None
        self.Period = None
        self.Zone = None
        self.ProjectId = None
        self.DBVersion = None
        self.InstanceChargeType = None
        self.AutoVoucher = None
        self.VoucherIds = None
        self.VpcId = None
        self.SubnetId = None
        self.AutoRenewFlag = None
        self.ActivityId = None
        self.Name = None
        self.NeedSupportIpv6 = None
        self.TagList = None
        self.SecurityGroupIds = None
        self.DBMajorVersion = None
        self.DBKernelVersion = None


    def _deserialize(self, params):
        self.SpecCode = params.get("SpecCode")
        self.Storage = params.get("Storage")
        self.InstanceCount = params.get("InstanceCount")
        self.Period = params.get("Period")
        self.Zone = params.get("Zone")
        self.ProjectId = params.get("ProjectId")
        self.DBVersion = params.get("DBVersion")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.ActivityId = params.get("ActivityId")
        self.Name = params.get("Name")
        self.NeedSupportIpv6 = params.get("NeedSupportIpv6")
        if params.get("TagList") is not None:
            self.TagList = []
            for item in params.get("TagList"):
                obj = Tag()
                obj._deserialize(item)
                self.TagList.append(obj)
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.DBMajorVersion = params.get("DBMajorVersion")
        self.DBKernelVersion = params.get("DBKernelVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDBInstancesResponse(AbstractModel):
    """CreateDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param DealNames: Order number list. Each instance corresponds to an order number.
        :type DealNames: list of str
        :param BillId: Bill ID of frozen fees
        :type BillId: str
        :param DBInstanceIdSet: ID set of instances which have been created successfully. The parameter value will be returned only when the billing mode is postpaid.
        :type DBInstanceIdSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealNames = None
        self.BillId = None
        self.DBInstanceIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealNames = params.get("DealNames")
        self.BillId = params.get("BillId")
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        self.RequestId = params.get("RequestId")


class CreateInstancesRequest(AbstractModel):
    """CreateInstances request structure.

    """

    def __init__(self):
        r"""
        :param SpecCode: Purchasable specification ID, which can be obtained through the `SpecCode` field in the returned value of the `DescribeProductConfig` API.
        :type SpecCode: str
        :param Storage: Instance storage capacity in GB
        :type Storage: int
        :param InstanceCount: The number of instances purchased at a time. Value range: 1-10.
        :type InstanceCount: int
        :param Period: Valid period in months of purchased instances. Valid values: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `24`, `36`. This parameter is set to `1` when the pay-as-you-go billing mode is used.
        :type Period: int
        :param Zone: Availability zone ID, which can be obtained through the `Zone` field in the returned value of the `DescribeZones` API.
        :type Zone: str
        :param Charset: Instance character set. Valid values: `UTF8`, `LATIN1`.
        :type Charset: str
        :param AdminName: Instance root account name
        :type AdminName: str
        :param AdminPassword: Instance root account password
        :type AdminPassword: str
        :param ProjectId: Project ID
        :type ProjectId: int
        :param DBVersion: PostgreSQL version. If it is specified, an instance running the latest kernel of PostgreSQL `DBVersion` will be created. You must pass in at least one of the following parameters: DBVersion, DBMajorVersion, DBKernelVersion.
        :type DBVersion: str
        :param InstanceChargeType: Instance billing mode. Valid values: `PREPAID` (monthly subscription), `POSTPAID_BY_HOUR` (pay-as-you-go).
        :type InstanceChargeType: str
        :param AutoVoucher: Whether to automatically use vouchers. Valid values: `1` (yes), `0` (no). Default value: `0`.
        :type AutoVoucher: int
        :param VoucherIds: Voucher ID list. Currently, you can specify only one voucher.
        :type VoucherIds: list of str
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: ID of a subnet in the VPC specified by `VpcId`
        :type SubnetId: str
        :param AutoRenewFlag: Renewal flag. Valid values: `0` (manual renewal), `1` (auto-renewal). Default value: `0`.
        :type AutoRenewFlag: int
        :param ActivityId: Campaign ID
        :type ActivityId: int
        :param Name: Instance name
        :type Name: str
        :param NeedSupportIpv6: Whether to support IPv6 address access. Valid values: `1` (yes), `0` (no). Default value: `0`
        :type NeedSupportIpv6: int
        :param TagList: The information of tags to be associated with instances. This parameter is left empty by default.
        :type TagList: list of Tag
        :param SecurityGroupIds: Security group IDs
        :type SecurityGroupIds: list of str
        :param DBMajorVersion: PostgreSQL major version. Valid values: `10`, `11`, `12`, `13`. If it is specified, an instance running the latest kernel of PostgreSQL `DBMajorVersion` will be created. You must pass in at least one of the following parameters: DBMajorVersion, DBVersion, DBKernelVersion.
        :type DBMajorVersion: str
        :param DBKernelVersion: PostgreSQL kernel version. If it is specified, an instance running the latest kernel of PostgreSQL `DBKernelVersion` will be created. You must pass in one of the following parameters: DBKernelVersion, DBVersion, DBMajorVersion.
        :type DBKernelVersion: str
        :param DBNodeSet: Instance node information, which is required if you purchase a multi-AZ deployed instance.
        :type DBNodeSet: list of DBNode
        :param NeedSupportTDE: Whether to support transparent data encryption. Valid values: 1 (yes), 0 (no). Default value: 0.
        :type NeedSupportTDE: int
        :param KMSKeyId: KeyId of custom key, which is required if you select custom key encryption. It is also the unique CMK identifier.
        :type KMSKeyId: str
        :param KMSRegion: The region where the KMS service is enabled. When `KMSRegion` is left empty, the KMS of the current region will be enabled by default. If the current region is not supported, you need to select another region supported by KMS.
        :type KMSRegion: str
        :param DBEngine: Database engine. Valid values:
1. `postgresql` (TencentDB for PostgreSQL)
2. `mssql_compatible`（MSSQL compatible-TencentDB for PostgreSQL)
Default value: `postgresql`
        :type DBEngine: str
        :param DBEngineConfig: Configuration information of database engine in the following format:
{"$key1":"$value1", "$key2":"$value2"}

Valid values:
1. mssql_compatible engine：
`migrationMode`: Database mode. Valid values: `single-db` (single-database mode), `multi-db` (multi-database mode). Default value: `single-db`.
`defaultLocale`: Default locale, which can’t be modified after the initialization. Default value: `en_US`. Valid values:
"af_ZA", "sq_AL", "ar_DZ", "ar_BH", "ar_EG", "ar_IQ", "ar_JO", "ar_KW", "ar_LB", "ar_LY", "ar_MA", "ar_OM", "ar_QA", "ar_SA", "ar_SY", "ar_TN", "ar_AE", "ar_YE", "hy_AM", "az_Cyrl_AZ", "az_Latn_AZ", "eu_ES", "be_BY", "bg_BG", "ca_ES", "zh_HK", "zh_MO", "zh_CN", "zh_SG", "zh_TW", "hr_HR", "cs_CZ", "da_DK", "nl_BE", "nl_NL", "en_AU", "en_BZ", "en_CA", "en_IE", "en_JM", "en_NZ", "en_PH", "en_ZA", "en_TT", "en_GB", "en_US", "en_ZW", "et_EE", "fo_FO", "fa_IR", "fi_FI", "fr_BE", "fr_CA", "fr_FR", "fr_LU", "fr_MC", "fr_CH", "mk_MK", "ka_GE", "de_AT", "de_DE", "de_LI", "de_LU", "de_CH", "el_GR", "gu_IN", "he_IL", "hi_IN", "hu_HU", "is_IS", "id_ID", "it_IT", "it_CH", "ja_JP", "kn_IN", "kok_IN", "ko_KR", "ky_KG", "lv_LV", "lt_LT", "ms_BN", "ms_MY", "mr_IN", "mn_MN", "nb_NO", "nn_NO", "pl_PL", "pt_BR", "pt_PT", "pa_IN", "ro_RO", "ru_RU", "sa_IN", "sr_Cyrl_RS", "sr_Latn_RS", "sk_SK", "sl_SI", "es_AR", "es_BO", "es_CL", "es_CO", "es_CR", "es_DO", "es_EC", "es_SV", "es_GT", "es_HN", "es_MX", "es_NI", "es_PA", "es_PY","es_PE", "es_PR", "es_ES", "es_TRADITIONAL", "es_UY", "es_VE", "sw_KE", "sv_FI", "sv_SE", "tt_RU", "te_IN", "th_TH", "tr_TR", "uk_UA", "ur_IN", "ur_PK", "uz_Cyrl_UZ", "uz_Latn_UZ", "vi_VN".
`serverCollationName`: Name of collation rule, which can’t be modified after the initialization. Default value: `sql_latin1_general_cp1_ci_as`. Valid values:
"bbf_unicode_general_ci_as", "bbf_unicode_cp1_ci_as", "bbf_unicode_CP1250_ci_as", "bbf_unicode_CP1251_ci_as", "bbf_unicode_cp1253_ci_as", "bbf_unicode_cp1254_ci_as", "bbf_unicode_cp1255_ci_as", "bbf_unicode_cp1256_ci_as", "bbf_unicode_cp1257_ci_as", "bbf_unicode_cp1258_ci_as", "bbf_unicode_cp874_ci_as", "sql_latin1_general_cp1250_ci_as", "sql_latin1_general_cp1251_ci_as", "sql_latin1_general_cp1_ci_as", "sql_latin1_general_cp1253_ci_as", "sql_latin1_general_cp1254_ci_as", "sql_latin1_general_cp1255_ci_as","sql_latin1_general_cp1256_ci_as", "sql_latin1_general_cp1257_ci_as", "sql_latin1_general_cp1258_ci_as", "chinese_prc_ci_as", "cyrillic_general_ci_as", "finnish_swedish_ci_as", "french_ci_as", "japanese_ci_as", "korean_wansung_ci_as", "latin1_general_ci_as", "modern_spanish_ci_as", "polish_ci_as", "thai_ci_as", "traditional_spanish_ci_as", "turkish_ci_as", "ukrainian_ci_as", "vietnamese_ci_as".
        :type DBEngineConfig: str
        """
        self.SpecCode = None
        self.Storage = None
        self.InstanceCount = None
        self.Period = None
        self.Zone = None
        self.Charset = None
        self.AdminName = None
        self.AdminPassword = None
        self.ProjectId = None
        self.DBVersion = None
        self.InstanceChargeType = None
        self.AutoVoucher = None
        self.VoucherIds = None
        self.VpcId = None
        self.SubnetId = None
        self.AutoRenewFlag = None
        self.ActivityId = None
        self.Name = None
        self.NeedSupportIpv6 = None
        self.TagList = None
        self.SecurityGroupIds = None
        self.DBMajorVersion = None
        self.DBKernelVersion = None
        self.DBNodeSet = None
        self.NeedSupportTDE = None
        self.KMSKeyId = None
        self.KMSRegion = None
        self.DBEngine = None
        self.DBEngineConfig = None


    def _deserialize(self, params):
        self.SpecCode = params.get("SpecCode")
        self.Storage = params.get("Storage")
        self.InstanceCount = params.get("InstanceCount")
        self.Period = params.get("Period")
        self.Zone = params.get("Zone")
        self.Charset = params.get("Charset")
        self.AdminName = params.get("AdminName")
        self.AdminPassword = params.get("AdminPassword")
        self.ProjectId = params.get("ProjectId")
        self.DBVersion = params.get("DBVersion")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.ActivityId = params.get("ActivityId")
        self.Name = params.get("Name")
        self.NeedSupportIpv6 = params.get("NeedSupportIpv6")
        if params.get("TagList") is not None:
            self.TagList = []
            for item in params.get("TagList"):
                obj = Tag()
                obj._deserialize(item)
                self.TagList.append(obj)
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.DBMajorVersion = params.get("DBMajorVersion")
        self.DBKernelVersion = params.get("DBKernelVersion")
        if params.get("DBNodeSet") is not None:
            self.DBNodeSet = []
            for item in params.get("DBNodeSet"):
                obj = DBNode()
                obj._deserialize(item)
                self.DBNodeSet.append(obj)
        self.NeedSupportTDE = params.get("NeedSupportTDE")
        self.KMSKeyId = params.get("KMSKeyId")
        self.KMSRegion = params.get("KMSRegion")
        self.DBEngine = params.get("DBEngine")
        self.DBEngineConfig = params.get("DBEngineConfig")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateInstancesResponse(AbstractModel):
    """CreateInstances response structure.

    """

    def __init__(self):
        r"""
        :param DealNames: Order number list. Each instance corresponds to an order number.
        :type DealNames: list of str
        :param BillId: Bill ID of frozen fees
        :type BillId: str
        :param DBInstanceIdSet: ID set of instances which have been created successfully. The parameter value will be returned only when the pay-as-you-go billing mode is used.
        :type DBInstanceIdSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealNames = None
        self.BillId = None
        self.DBInstanceIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealNames = params.get("DealNames")
        self.BillId = params.get("BillId")
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        self.RequestId = params.get("RequestId")


class CreateParameterTemplateRequest(AbstractModel):
    """CreateParameterTemplate request structure.

    """

    def __init__(self):
        r"""
        :param TemplateName: Template name, which can contain 1-60 letters, digits, and symbols (-_./()[]()+=:@).
        :type TemplateName: str
        :param DBMajorVersion: The major database version number, such as 11, 12, 13.
        :type DBMajorVersion: str
        :param DBEngine: Database engine, such as postgresql, mssql_compatible.
        :type DBEngine: str
        :param TemplateDescription: Parameter template description, which can contain 1-60 letters, digits, and symbols (-_./()[]()+=:@).
        :type TemplateDescription: str
        """
        self.TemplateName = None
        self.DBMajorVersion = None
        self.DBEngine = None
        self.TemplateDescription = None


    def _deserialize(self, params):
        self.TemplateName = params.get("TemplateName")
        self.DBMajorVersion = params.get("DBMajorVersion")
        self.DBEngine = params.get("DBEngine")
        self.TemplateDescription = params.get("TemplateDescription")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateParameterTemplateResponse(AbstractModel):
    """CreateParameterTemplate response structure.

    """

    def __init__(self):
        r"""
        :param TemplateId: Parameter template ID, which uniquely identifies a parameter template.
        :type TemplateId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TemplateId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TemplateId = params.get("TemplateId")
        self.RequestId = params.get("RequestId")


class CreateReadOnlyDBInstanceRequest(AbstractModel):
    """CreateReadOnlyDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param SpecCode: Purchasable specification ID, which can be obtained through the `SpecCode` field in the returned value of the `DescribeProductConfig` API.
        :type SpecCode: str
        :param Storage: Instance storage capacity in GB
        :type Storage: int
        :param InstanceCount: Number of instances purchased at a time. Value range: 1–100.
        :type InstanceCount: int
        :param Period: Valid period in months of purchased instances. Valid values: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `24`, `36`. This parameter is set to `1` when the pay-as-you-go billing mode is used.
        :type Period: int
        :param MasterDBInstanceId: ID of the primary instance to which the read-only replica belongs
        :type MasterDBInstanceId: str
        :param Zone: Availability zone ID, which can be obtained through the `Zone` field in the returned value of the `DescribeZones` API.
        :type Zone: str
        :param ProjectId: Project ID
        :type ProjectId: int
        :param DBVersion: (Disused) You don’t need to specify a version, as the kernel version is as the same as that of the instance.
        :type DBVersion: str
        :param InstanceChargeType: Instance billing mode. Valid value: `POSTPAID_BY_HOUR` (pay-as-you-go). If the source instance is pay-as-you-go, so is the read-only instance.
        :type InstanceChargeType: str
        :param AutoVoucher: Whether to automatically use vouchers. Valid values: `1` (yes), `0` (no). Default value: `0`.
        :type AutoVoucher: int
        :param VoucherIds: Voucher ID list. Currently, you can specify only one voucher.
        :type VoucherIds: list of str
        :param AutoRenewFlag: Renewal flag. Valid values: `0` (manual renewal), `1` (auto-renewal). Default value: `0`.
        :type AutoRenewFlag: int
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: VPC subnet ID
        :type SubnetId: str
        :param ActivityId: Special offer ID
        :type ActivityId: int
        :param Name: Instance name (which will be supported in the future)
        :type Name: str
        :param NeedSupportIpv6: Whether to support IPv6 address access. Valid values: `1` (yes), `0` (no).
        :type NeedSupportIpv6: int
        :param ReadOnlyGroupId: RO group ID
        :type ReadOnlyGroupId: str
        :param TagList: The information of tags to be bound with the purchased instance, which is left empty by default (type: tag array).
        :type TagList: :class:`tencentcloud.postgres.v20170312.models.Tag`
        :param SecurityGroupIds: Security group ID
        :type SecurityGroupIds: list of str
        """
        self.SpecCode = None
        self.Storage = None
        self.InstanceCount = None
        self.Period = None
        self.MasterDBInstanceId = None
        self.Zone = None
        self.ProjectId = None
        self.DBVersion = None
        self.InstanceChargeType = None
        self.AutoVoucher = None
        self.VoucherIds = None
        self.AutoRenewFlag = None
        self.VpcId = None
        self.SubnetId = None
        self.ActivityId = None
        self.Name = None
        self.NeedSupportIpv6 = None
        self.ReadOnlyGroupId = None
        self.TagList = None
        self.SecurityGroupIds = None


    def _deserialize(self, params):
        self.SpecCode = params.get("SpecCode")
        self.Storage = params.get("Storage")
        self.InstanceCount = params.get("InstanceCount")
        self.Period = params.get("Period")
        self.MasterDBInstanceId = params.get("MasterDBInstanceId")
        self.Zone = params.get("Zone")
        self.ProjectId = params.get("ProjectId")
        self.DBVersion = params.get("DBVersion")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.ActivityId = params.get("ActivityId")
        self.Name = params.get("Name")
        self.NeedSupportIpv6 = params.get("NeedSupportIpv6")
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        if params.get("TagList") is not None:
            self.TagList = Tag()
            self.TagList._deserialize(params.get("TagList"))
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateReadOnlyDBInstanceResponse(AbstractModel):
    """CreateReadOnlyDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param DealNames: Order number list. Each instance corresponds to an order number.
        :type DealNames: list of str
        :param BillId: Bill ID of frozen fees
        :type BillId: str
        :param DBInstanceIdSet: ID set of instances which have been created successfully. The parameter value will be returned only when the pay-as-you-go billing mode is used.
        :type DBInstanceIdSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealNames = None
        self.BillId = None
        self.DBInstanceIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealNames = params.get("DealNames")
        self.BillId = params.get("BillId")
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        self.RequestId = params.get("RequestId")


class CreateReadOnlyGroupNetworkAccessRequest(AbstractModel):
    """CreateReadOnlyGroupNetworkAccess request structure.

    """

    def __init__(self):
        r"""
        :param ReadOnlyGroupId: RO group ID in the format of pgro-4t9c6g7k.
        :type ReadOnlyGroupId: str
        :param VpcId: Unified VPC ID.
        :type VpcId: str
        :param SubnetId: Subnet ID.
        :type SubnetId: str
        :param IsAssignVip: Whether to manually assign the VIP. Valid values: `true` (manually assign), `false` (automatically assign).
        :type IsAssignVip: bool
        :param Vip: Target VIP.
        :type Vip: str
        """
        self.ReadOnlyGroupId = None
        self.VpcId = None
        self.SubnetId = None
        self.IsAssignVip = None
        self.Vip = None


    def _deserialize(self, params):
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.IsAssignVip = params.get("IsAssignVip")
        self.Vip = params.get("Vip")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateReadOnlyGroupNetworkAccessResponse(AbstractModel):
    """CreateReadOnlyGroupNetworkAccess response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class CreateReadOnlyGroupRequest(AbstractModel):
    """CreateReadOnlyGroup request structure.

    """

    def __init__(self):
        r"""
        :param MasterDBInstanceId: Primary instance ID
        :type MasterDBInstanceId: str
        :param Name: RO group name
        :type Name: str
        :param ProjectId: Project ID
        :type ProjectId: int
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: Subnet ID
        :type SubnetId: str
        :param ReplayLagEliminate: Whether to remove a read-only replica from an RO group if the delay between the read-only replica and the primary instance exceeds the threshold. Valid values: `0` (no), `1` (yes).
        :type ReplayLagEliminate: int
        :param ReplayLatencyEliminate: Whether to remove a read-only replica from an RO group if the sync log size difference between the read-only replica and the primary instance exceeds the threshold. Valid values: `0` (no), `1` (yes).
        :type ReplayLatencyEliminate: int
        :param MaxReplayLag: Delay threshold in ms
        :type MaxReplayLag: int
        :param MaxReplayLatency: Delayed log size threshold in MB
        :type MaxReplayLatency: int
        :param MinDelayEliminateReserve: The minimum number of read-only replicas that must be retained in an RO group
        :type MinDelayEliminateReserve: int
        :param SecurityGroupIds: Security group ID
        :type SecurityGroupIds: list of str
        """
        self.MasterDBInstanceId = None
        self.Name = None
        self.ProjectId = None
        self.VpcId = None
        self.SubnetId = None
        self.ReplayLagEliminate = None
        self.ReplayLatencyEliminate = None
        self.MaxReplayLag = None
        self.MaxReplayLatency = None
        self.MinDelayEliminateReserve = None
        self.SecurityGroupIds = None


    def _deserialize(self, params):
        self.MasterDBInstanceId = params.get("MasterDBInstanceId")
        self.Name = params.get("Name")
        self.ProjectId = params.get("ProjectId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.ReplayLagEliminate = params.get("ReplayLagEliminate")
        self.ReplayLatencyEliminate = params.get("ReplayLatencyEliminate")
        self.MaxReplayLag = params.get("MaxReplayLag")
        self.MaxReplayLatency = params.get("MaxReplayLatency")
        self.MinDelayEliminateReserve = params.get("MinDelayEliminateReserve")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateReadOnlyGroupResponse(AbstractModel):
    """CreateReadOnlyGroup response structure.

    """

    def __init__(self):
        r"""
        :param ReadOnlyGroupId: RO group ID
        :type ReadOnlyGroupId: str
        :param FlowId: Task ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ReadOnlyGroupId = None
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class CreateServerlessDBInstanceRequest(AbstractModel):
    """CreateServerlessDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param Zone: Availability zone ID. Only ap-shanghai-2, ap-beijing-1, and ap-guangzhou-2 are supported during the beta test.
        :type Zone: str
        :param DBInstanceName: Instance name. The value must be unique for the same account.
        :type DBInstanceName: str
        :param DBVersion: Kernel version of a PostgreSQL instance. Currently, only 10.4 is supported.
        :type DBVersion: str
        :param DBCharset: Database character set of a PostgreSQL instance. Currently, only UTF-8 is supported.
        :type DBCharset: str
        :param ProjectId: Project ID.
        :type ProjectId: int
        :param VpcId: VPC ID.
        :type VpcId: str
        :param SubnetId: VPC subnet ID.
        :type SubnetId: str
        :param TagList: Array of tags to be bound with the instance
        :type TagList: list of Tag
        """
        self.Zone = None
        self.DBInstanceName = None
        self.DBVersion = None
        self.DBCharset = None
        self.ProjectId = None
        self.VpcId = None
        self.SubnetId = None
        self.TagList = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.DBInstanceName = params.get("DBInstanceName")
        self.DBVersion = params.get("DBVersion")
        self.DBCharset = params.get("DBCharset")
        self.ProjectId = params.get("ProjectId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        if params.get("TagList") is not None:
            self.TagList = []
            for item in params.get("TagList"):
                obj = Tag()
                obj._deserialize(item)
                self.TagList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateServerlessDBInstanceResponse(AbstractModel):
    """CreateServerlessDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID, such as "postgres-xxxxx". The value must be globally unique.
        :type DBInstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DBInstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.RequestId = params.get("RequestId")


class DBBackup(AbstractModel):
    """Database backup information

    """

    def __init__(self):
        r"""
        :param Id: Unique backup file ID
        :type Id: int
        :param StartTime: File generation start time
        :type StartTime: str
        :param EndTime: File generation end time
        :type EndTime: str
        :param Size: File size in KB
        :type Size: int
        :param Strategy: Policy (0: instance backup, 1: multi-database backup)
        :type Strategy: int
        :param Way: Type (0: scheduled)
        :type Way: int
        :param Type: Backup mode (1: full)
        :type Type: int
        :param Status: Status (1: creating, 2: success, 3: failure)
        :type Status: int
        :param DbList: DB list
        :type DbList: list of str
        :param InternalAddr: Download address on private network
        :type InternalAddr: str
        :param ExternalAddr: Download address on public network
        :type ExternalAddr: str
        :param SetId: Backup set ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type SetId: str
        """
        self.Id = None
        self.StartTime = None
        self.EndTime = None
        self.Size = None
        self.Strategy = None
        self.Way = None
        self.Type = None
        self.Status = None
        self.DbList = None
        self.InternalAddr = None
        self.ExternalAddr = None
        self.SetId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Size = params.get("Size")
        self.Strategy = params.get("Strategy")
        self.Way = params.get("Way")
        self.Type = params.get("Type")
        self.Status = params.get("Status")
        self.DbList = params.get("DbList")
        self.InternalAddr = params.get("InternalAddr")
        self.ExternalAddr = params.get("ExternalAddr")
        self.SetId = params.get("SetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DBInstance(AbstractModel):
    """Instance details

    """

    def __init__(self):
        r"""
        :param Region: Instance region such as ap-guangzhou, which corresponds to the `Region` field of `RegionSet`
        :type Region: str
        :param Zone: Instance AZ such as ap-guangzhou-3, which corresponds to the `Zone` field of `ZoneSet`
        :type Zone: str
        :param ProjectId: Project ID
        :type ProjectId: int
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: SubnetId
        :type SubnetId: str
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param DBInstanceName: Instance name
        :type DBInstanceName: str
        :param DBInstanceStatus: Instance status.  Valid values: `applying`, `init` (to be initialized), `initing` (initializing), `running`, `limited run`, `isolating`, `isolated`, `recycling`, `recycled`, `job running`, `offline`, `migrating`, `expanding`, `waitSwitch` (waiting for switch), `switching`, `readonly`, `restarting`, `network changing`, `upgrading` (upgrading kernel version).
        :type DBInstanceStatus: str
        :param DBInstanceMemory: Assigned instance memory size in GB
        :type DBInstanceMemory: int
        :param DBInstanceStorage: Assigned instance storage capacity in GB
        :type DBInstanceStorage: int
        :param DBInstanceCpu: Number of assigned CPUs
        :type DBInstanceCpu: int
        :param DBInstanceClass: Purchasable specification ID
        :type DBInstanceClass: str
        :param DBInstanceType: Instance type. 1: primary (master instance), 2: readonly (read-only instance), 3: guard (disaster recovery instance), 4: temp (temp instance)
        :type DBInstanceType: str
        :param DBInstanceVersion: Instance edition. Currently, only `standard` edition (dual-server high-availability one-master-one-slave edition) is supported
        :type DBInstanceVersion: str
        :param DBCharset: Instance database character set
        :type DBCharset: str
        :param DBVersion: PostgreSQL version number
        :type DBVersion: str
        :param CreateTime: Instance creation time
        :type CreateTime: str
        :param UpdateTime: Instance last modified time
        :type UpdateTime: str
        :param ExpireTime: Instance expiration time
        :type ExpireTime: str
        :param IsolatedTime: Instance isolation time
        :type IsolatedTime: str
        :param PayType: Billing mode. postpaid: pay-as-you-go
        :type PayType: str
        :param AutoRenew: Whether to renew automatically. 1: yes, 0: no
        :type AutoRenew: int
        :param DBInstanceNetInfo: Instance network connection information
        :type DBInstanceNetInfo: list of DBInstanceNetInfo
        :param Type: Machine type
        :type Type: str
        :param AppId: User `AppId`
        :type AppId: int
        :param Uid: Instance `Uid`
        :type Uid: int
        :param SupportIpv6: Whether the instance supports IPv6 address access. Valid values: 1 (yes), 0 (no)
        :type SupportIpv6: int
        :param TagList: The information of tags associated with instances.
Note: this field may return null, indicating that no valid values can be obtained.
        :type TagList: list of Tag
        :param MasterDBInstanceId: Primary instance information, which is returned only when the instance is read-only
Note: this field may return null, indicating that no valid values can be obtained.
        :type MasterDBInstanceId: str
        :param ReadOnlyInstanceNum: Number of read-only instances
Note: this field may return null, indicating that no valid values can be obtained.
        :type ReadOnlyInstanceNum: int
        :param StatusInReadonlyGroup: The status of a instance in a read-only group
Note: this field may return null, indicating that no valid values can be obtained.
        :type StatusInReadonlyGroup: str
        :param OfflineTime: Elimination time
Note: this field may return null, indicating that no valid values can be obtained.
        :type OfflineTime: str
        :param DBKernelVersion: Database kernel version
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBKernelVersion: str
        :param NetworkAccessList: Network access list of the instance (this field has been deprecated)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type NetworkAccessList: list of NetworkAccess
        :param DBMajorVersion: PostgreSQL major version number
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBMajorVersion: str
        :param DBNodeSet: Instance node information
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBNodeSet: list of DBNode
        :param IsSupportTDE: Whether the instance supports TDE data encryption. Valid values: 0 (no), 1 (yes)
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type IsSupportTDE: int
        :param DBEngine: 
        :type DBEngine: str
        :param DBEngineConfig: Configuration information of database engine
Note: This field may return null, indicating that no valid values can be obtained.
        :type DBEngineConfig: str
        """
        self.Region = None
        self.Zone = None
        self.ProjectId = None
        self.VpcId = None
        self.SubnetId = None
        self.DBInstanceId = None
        self.DBInstanceName = None
        self.DBInstanceStatus = None
        self.DBInstanceMemory = None
        self.DBInstanceStorage = None
        self.DBInstanceCpu = None
        self.DBInstanceClass = None
        self.DBInstanceType = None
        self.DBInstanceVersion = None
        self.DBCharset = None
        self.DBVersion = None
        self.CreateTime = None
        self.UpdateTime = None
        self.ExpireTime = None
        self.IsolatedTime = None
        self.PayType = None
        self.AutoRenew = None
        self.DBInstanceNetInfo = None
        self.Type = None
        self.AppId = None
        self.Uid = None
        self.SupportIpv6 = None
        self.TagList = None
        self.MasterDBInstanceId = None
        self.ReadOnlyInstanceNum = None
        self.StatusInReadonlyGroup = None
        self.OfflineTime = None
        self.DBKernelVersion = None
        self.NetworkAccessList = None
        self.DBMajorVersion = None
        self.DBNodeSet = None
        self.IsSupportTDE = None
        self.DBEngine = None
        self.DBEngineConfig = None


    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.ProjectId = params.get("ProjectId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.DBInstanceId = params.get("DBInstanceId")
        self.DBInstanceName = params.get("DBInstanceName")
        self.DBInstanceStatus = params.get("DBInstanceStatus")
        self.DBInstanceMemory = params.get("DBInstanceMemory")
        self.DBInstanceStorage = params.get("DBInstanceStorage")
        self.DBInstanceCpu = params.get("DBInstanceCpu")
        self.DBInstanceClass = params.get("DBInstanceClass")
        self.DBInstanceType = params.get("DBInstanceType")
        self.DBInstanceVersion = params.get("DBInstanceVersion")
        self.DBCharset = params.get("DBCharset")
        self.DBVersion = params.get("DBVersion")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.ExpireTime = params.get("ExpireTime")
        self.IsolatedTime = params.get("IsolatedTime")
        self.PayType = params.get("PayType")
        self.AutoRenew = params.get("AutoRenew")
        if params.get("DBInstanceNetInfo") is not None:
            self.DBInstanceNetInfo = []
            for item in params.get("DBInstanceNetInfo"):
                obj = DBInstanceNetInfo()
                obj._deserialize(item)
                self.DBInstanceNetInfo.append(obj)
        self.Type = params.get("Type")
        self.AppId = params.get("AppId")
        self.Uid = params.get("Uid")
        self.SupportIpv6 = params.get("SupportIpv6")
        if params.get("TagList") is not None:
            self.TagList = []
            for item in params.get("TagList"):
                obj = Tag()
                obj._deserialize(item)
                self.TagList.append(obj)
        self.MasterDBInstanceId = params.get("MasterDBInstanceId")
        self.ReadOnlyInstanceNum = params.get("ReadOnlyInstanceNum")
        self.StatusInReadonlyGroup = params.get("StatusInReadonlyGroup")
        self.OfflineTime = params.get("OfflineTime")
        self.DBKernelVersion = params.get("DBKernelVersion")
        if params.get("NetworkAccessList") is not None:
            self.NetworkAccessList = []
            for item in params.get("NetworkAccessList"):
                obj = NetworkAccess()
                obj._deserialize(item)
                self.NetworkAccessList.append(obj)
        self.DBMajorVersion = params.get("DBMajorVersion")
        if params.get("DBNodeSet") is not None:
            self.DBNodeSet = []
            for item in params.get("DBNodeSet"):
                obj = DBNode()
                obj._deserialize(item)
                self.DBNodeSet.append(obj)
        self.IsSupportTDE = params.get("IsSupportTDE")
        self.DBEngine = params.get("DBEngine")
        self.DBEngineConfig = params.get("DBEngineConfig")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DBInstanceNetInfo(AbstractModel):
    """Instance network connection information

    """

    def __init__(self):
        r"""
        :param Address: DNS domain name
        :type Address: str
        :param Ip: Ip
        :type Ip: str
        :param Port: Connection port address
        :type Port: int
        :param NetType: Network type. 1: inner (private network address), 2: public (public network address)
        :type NetType: str
        :param Status: Network connection status. Valid values: `initing` (never enabled before), `opened` (enabled), `closed` (disabled), `opening` (enabling), `closing` (disabling)
        :type Status: str
        :param VpcId: VPC ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type VpcId: str
        :param SubnetId: Subnet ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type SubnetId: str
        :param ProtocolType: Database connection protocol type. Valid values: `postgresql`, `mssql` (MSSQL-compatible)
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProtocolType: str
        """
        self.Address = None
        self.Ip = None
        self.Port = None
        self.NetType = None
        self.Status = None
        self.VpcId = None
        self.SubnetId = None
        self.ProtocolType = None


    def _deserialize(self, params):
        self.Address = params.get("Address")
        self.Ip = params.get("Ip")
        self.Port = params.get("Port")
        self.NetType = params.get("NetType")
        self.Status = params.get("Status")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.ProtocolType = params.get("ProtocolType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DBNode(AbstractModel):
    """Instance node information including node type and AZ.

    """

    def __init__(self):
        r"""
        :param Role: Node type. Valid values:
`Primary`;
`Standby`.
        :type Role: str
        :param Zone: AZ where the node resides, such as ap-guangzhou-1.
        :type Zone: str
        """
        self.Role = None
        self.Zone = None


    def _deserialize(self, params):
        self.Role = params.get("Role")
        self.Zone = params.get("Zone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBaseBackupRequest(AbstractModel):
    """DeleteBaseBackup request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param BaseBackupId: Base backup ID
        :type BaseBackupId: str
        """
        self.DBInstanceId = None
        self.BaseBackupId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.BaseBackupId = params.get("BaseBackupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBaseBackupResponse(AbstractModel):
    """DeleteBaseBackup response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDBInstanceNetworkAccessRequest(AbstractModel):
    """DeleteDBInstanceNetworkAccess request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-6bwgamo3.
        :type DBInstanceId: str
        :param VpcId: Unified VPC ID. If you want to delete the classic network, set the parameter to `0`.
        :type VpcId: str
        :param SubnetId: Subnet ID. If you want to delete the classic network, set the parameter to `0`.
        :type SubnetId: str
        :param Vip: Target VIP.
        :type Vip: str
        """
        self.DBInstanceId = None
        self.VpcId = None
        self.SubnetId = None
        self.Vip = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Vip = params.get("Vip")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDBInstanceNetworkAccessResponse(AbstractModel):
    """DeleteDBInstanceNetworkAccess response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class DeleteLogBackupRequest(AbstractModel):
    """DeleteLogBackup request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param LogBackupId: Log backup ID
        :type LogBackupId: str
        """
        self.DBInstanceId = None
        self.LogBackupId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.LogBackupId = params.get("LogBackupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteLogBackupResponse(AbstractModel):
    """DeleteLogBackup response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteParameterTemplateRequest(AbstractModel):
    """DeleteParameterTemplate request structure.

    """

    def __init__(self):
        r"""
        :param TemplateId: Parameter template ID, which uniquely identifies the parameter template to be operated.
        :type TemplateId: str
        """
        self.TemplateId = None


    def _deserialize(self, params):
        self.TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteParameterTemplateResponse(AbstractModel):
    """DeleteParameterTemplate response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteReadOnlyGroupNetworkAccessRequest(AbstractModel):
    """DeleteReadOnlyGroupNetworkAccess request structure.

    """

    def __init__(self):
        r"""
        :param ReadOnlyGroupId: RO group ID in the format of pgro-4t9c6g7k.
        :type ReadOnlyGroupId: str
        :param VpcId: Unified VPC ID. If you want to delete the classic network, set the parameter to `0`.
        :type VpcId: str
        :param SubnetId: Subnet ID. If you want to delete the classic network, set the parameter to `0`.
        :type SubnetId: str
        :param Vip: Target VIP.
        :type Vip: str
        """
        self.ReadOnlyGroupId = None
        self.VpcId = None
        self.SubnetId = None
        self.Vip = None


    def _deserialize(self, params):
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Vip = params.get("Vip")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteReadOnlyGroupNetworkAccessResponse(AbstractModel):
    """DeleteReadOnlyGroupNetworkAccess response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class DeleteReadOnlyGroupRequest(AbstractModel):
    """DeleteReadOnlyGroup request structure.

    """

    def __init__(self):
        r"""
        :param ReadOnlyGroupId: ID of the RO group to be deleted
        :type ReadOnlyGroupId: str
        """
        self.ReadOnlyGroupId = None


    def _deserialize(self, params):
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteReadOnlyGroupResponse(AbstractModel):
    """DeleteReadOnlyGroup response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class DeleteServerlessDBInstanceRequest(AbstractModel):
    """DeleteServerlessDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceName: Instance name. Either instance name or instance ID (or both) must be passed in. If both are passed in, the instance ID will prevail.
        :type DBInstanceName: str
        :param DBInstanceId: Instance ID. Either instance name or instance ID (or both) must be passed in. If both are passed in, the instance ID will prevail.
        :type DBInstanceId: str
        """
        self.DBInstanceName = None
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceName = params.get("DBInstanceName")
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteServerlessDBInstanceResponse(AbstractModel):
    """DeleteServerlessDBInstance response structure.

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
        :param DBInstanceId: Instance ID in the format of postgres-6fego161
        :type DBInstanceId: str
        :param Limit: Number of entries returned per page. Default value: 10. Value range: 1–100.
        :type Limit: int
        :param Offset: Data offset, which starts from 0.
        :type Offset: int
        :param OrderBy: Whether to sort by creation time or username. Valid values: `createTime` (sort by creation time), `name` (sort by username)
        :type OrderBy: str
        :param OrderByType: Whether returns are sorted in ascending or descending order. Valid values: `desc` (descending), `asc` (ascending)
        :type OrderByType: str
        """
        self.DBInstanceId = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
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
        :param TotalCount: Number of date entries returned for this API call.
        :type TotalCount: int
        :param Details: Account list details.
        :type Details: list of AccountInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Details = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Details") is not None:
            self.Details = []
            for item in params.get("Details"):
                obj = AccountInfo()
                obj._deserialize(item)
                self.Details.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAvailableRecoveryTimeRequest(AbstractModel):
    """DescribeAvailableRecoveryTime request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAvailableRecoveryTimeResponse(AbstractModel):
    """DescribeAvailableRecoveryTime response structure.

    """

    def __init__(self):
        r"""
        :param RecoveryBeginTime: The earliest restoration time (UTC+8).
        :type RecoveryBeginTime: str
        :param RecoveryEndTime: The latest restoration time (UTC+8).
        :type RecoveryEndTime: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RecoveryBeginTime = None
        self.RecoveryEndTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.RecoveryBeginTime = params.get("RecoveryBeginTime")
        self.RecoveryEndTime = params.get("RecoveryEndTime")
        self.RequestId = params.get("RequestId")


class DescribeBackupDownloadRestrictionRequest(AbstractModel):
    """DescribeBackupDownloadRestriction request structure.

    """


class DescribeBackupDownloadRestrictionResponse(AbstractModel):
    """DescribeBackupDownloadRestriction response structure.

    """

    def __init__(self):
        r"""
        :param RestrictionType: Type of the network restrictions for downloading a backup file. Valid values: `NONE` (backups can be downloaded over both private and public networks), `INTRANET` (backups can only be downloaded over the private network), `CUSTOMIZE` (backups can be downloaded over specified VPCs or at specified IPs).
        :type RestrictionType: str
        :param VpcRestrictionEffect: Whether VPC is allowed. Valid values: `ALLOW` (allow), `DENY` (deny). 
Note:  This field may return null, indicating that no valid values can be obtained.
        :type VpcRestrictionEffect: str
        :param VpcIdSet: Whether it is allowed to download the VPC ID list of the backup files. 
Note:  This field may return null, indicating that no valid values can be obtained.
        :type VpcIdSet: list of str
        :param IpRestrictionEffect: Whether IP is allowed. Valid values: `ALLOW` (allow), `DENY` (deny). 
Note: Note: This field may return null, indicating that no valid values can be obtained.
        :type IpRestrictionEffect: str
        :param IpSet: Whether it is allowed to download the IP list of the backup files. 
Note:  This field may return null, indicating that no valid values can be obtained.
        :type IpSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RestrictionType = None
        self.VpcRestrictionEffect = None
        self.VpcIdSet = None
        self.IpRestrictionEffect = None
        self.IpSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.RestrictionType = params.get("RestrictionType")
        self.VpcRestrictionEffect = params.get("VpcRestrictionEffect")
        self.VpcIdSet = params.get("VpcIdSet")
        self.IpRestrictionEffect = params.get("IpRestrictionEffect")
        self.IpSet = params.get("IpSet")
        self.RequestId = params.get("RequestId")


class DescribeBackupDownloadURLRequest(AbstractModel):
    """DescribeBackupDownloadURL request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID.
        :type DBInstanceId: str
        :param BackupType: Backup type. Valid values: `LogBackup`, `BaseBackup`.
        :type BackupType: str
        :param BackupId: Unique backup ID.
        :type BackupId: str
        :param URLExpireTime: Validity period of a URL, which is 12 hours by default.
        :type URLExpireTime: int
        :param BackupDownloadRestriction: Backup download restriction
        :type BackupDownloadRestriction: :class:`tencentcloud.postgres.v20170312.models.BackupDownloadRestriction`
        """
        self.DBInstanceId = None
        self.BackupType = None
        self.BackupId = None
        self.URLExpireTime = None
        self.BackupDownloadRestriction = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.BackupType = params.get("BackupType")
        self.BackupId = params.get("BackupId")
        self.URLExpireTime = params.get("URLExpireTime")
        if params.get("BackupDownloadRestriction") is not None:
            self.BackupDownloadRestriction = BackupDownloadRestriction()
            self.BackupDownloadRestriction._deserialize(params.get("BackupDownloadRestriction"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupDownloadURLResponse(AbstractModel):
    """DescribeBackupDownloadURL response structure.

    """

    def __init__(self):
        r"""
        :param BackupDownloadURL: Backup download URL
        :type BackupDownloadURL: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BackupDownloadURL = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BackupDownloadURL = params.get("BackupDownloadURL")
        self.RequestId = params.get("RequestId")


class DescribeBackupOverviewRequest(AbstractModel):
    """DescribeBackupOverview request structure.

    """


class DescribeBackupOverviewResponse(AbstractModel):
    """DescribeBackupOverview response structure.

    """

    def __init__(self):
        r"""
        :param TotalFreeSize: Total free space size in bytes
        :type TotalFreeSize: int
        :param UsedFreeSize: Used free space size in bytes
        :type UsedFreeSize: int
        :param UsedBillingSize: Used paid space size in bytes
        :type UsedBillingSize: int
        :param LogBackupCount: Number of log backups
        :type LogBackupCount: int
        :param LogBackupSize: Log backup size in bytes
        :type LogBackupSize: int
        :param ManualBaseBackupCount: Number of manually created full backups
        :type ManualBaseBackupCount: int
        :param ManualBaseBackupSize: Size of manually created full backups in bytes
        :type ManualBaseBackupSize: int
        :param AutoBaseBackupCount: Number of automatically created full backups
        :type AutoBaseBackupCount: int
        :param AutoBaseBackupSize: Size of automatically created full backups in bytes
        :type AutoBaseBackupSize: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalFreeSize = None
        self.UsedFreeSize = None
        self.UsedBillingSize = None
        self.LogBackupCount = None
        self.LogBackupSize = None
        self.ManualBaseBackupCount = None
        self.ManualBaseBackupSize = None
        self.AutoBaseBackupCount = None
        self.AutoBaseBackupSize = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalFreeSize = params.get("TotalFreeSize")
        self.UsedFreeSize = params.get("UsedFreeSize")
        self.UsedBillingSize = params.get("UsedBillingSize")
        self.LogBackupCount = params.get("LogBackupCount")
        self.LogBackupSize = params.get("LogBackupSize")
        self.ManualBaseBackupCount = params.get("ManualBaseBackupCount")
        self.ManualBaseBackupSize = params.get("ManualBaseBackupSize")
        self.AutoBaseBackupCount = params.get("AutoBaseBackupCount")
        self.AutoBaseBackupSize = params.get("AutoBaseBackupSize")
        self.RequestId = params.get("RequestId")


class DescribeBackupPlansRequest(AbstractModel):
    """DescribeBackupPlans request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupPlansResponse(AbstractModel):
    """DescribeBackupPlans response structure.

    """

    def __init__(self):
        r"""
        :param Plans: The set of instance backup plans
        :type Plans: list of BackupPlan
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Plans = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Plans") is not None:
            self.Plans = []
            for item in params.get("Plans"):
                obj = BackupPlan()
                obj._deserialize(item)
                self.Plans.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBackupSummariesRequest(AbstractModel):
    """DescribeBackupSummaries request structure.

    """

    def __init__(self):
        r"""
        :param Limit: The maximum number of results returned per page. Value range: 1-100. Default: `10`
        :type Limit: int
        :param Offset: Data offset, which starts from 0.
        :type Offset: int
        :param Filters: Filter instances using one or more criteria. Valid filter names:
db-instance-id: Filter by instance ID (in string format).
db-instance-name: Filter by instance name (in string format).
db-instance-ip: Filter by instance VPC IP (in string format).
        :type Filters: list of Filter
        :param OrderBy: Sorting field. Valid values: `TotalBackupSize`, `LogBackupSize`, `ManualBaseBackupSize`, `AutoBaseBackupSize`.
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: `asc` (ascending), `desc` (descending).
        :type OrderByType: str
        """
        self.Limit = None
        self.Offset = None
        self.Filters = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupSummariesResponse(AbstractModel):
    """DescribeBackupSummaries response structure.

    """

    def __init__(self):
        r"""
        :param BackupSummarySet: Backup statistics list.
        :type BackupSummarySet: list of BackupSummary
        :param TotalCount: Number of all queried backups.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BackupSummarySet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("BackupSummarySet") is not None:
            self.BackupSummarySet = []
            for item in params.get("BackupSummarySet"):
                obj = BackupSummary()
                obj._deserialize(item)
                self.BackupSummarySet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeBaseBackupsRequest(AbstractModel):
    """DescribeBaseBackups request structure.

    """

    def __init__(self):
        r"""
        :param MinFinishTime: Minimum end time of a backup in the format of `2018-01-01 00:00:00`. It is 7 days ago by default.
        :type MinFinishTime: str
        :param MaxFinishTime: Maximum end time of a backup in the format of `2018-01-01 00:00:00`. It is the current time by default.
        :type MaxFinishTime: str
        :param Filters: Filter instances by using one or more filters. Valid values:  `db-instance-idFilter` (filter by instance ID in string),  `db-instance-name` (filter by instance name in string),  `db-instance-ip` (filter by instance VPC IP address in string),  `base-backup-id` (filter by backup set ID in string), 
        :type Filters: list of Filter
        :param Limit: The maximum number of results returned per page. Value range: 1-100. Default: `10`
        :type Limit: int
        :param Offset: Data offset, which starts from 0.
        :type Offset: int
        :param OrderBy: Sorting field. Valid values: `StartTime`, `FinishTime`, `Size`.
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: `asc` (ascending), `desc` (descending).
        :type OrderByType: str
        """
        self.MinFinishTime = None
        self.MaxFinishTime = None
        self.Filters = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        self.MinFinishTime = params.get("MinFinishTime")
        self.MaxFinishTime = params.get("MaxFinishTime")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBaseBackupsResponse(AbstractModel):
    """DescribeBaseBackups response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of queried full backups
        :type TotalCount: int
        :param BaseBackupSet: List of full backup details
        :type BaseBackupSet: list of BaseBackup
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.BaseBackupSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("BaseBackupSet") is not None:
            self.BaseBackupSet = []
            for item in params.get("BaseBackupSet"):
                obj = BaseBackup()
                obj._deserialize(item)
                self.BaseBackupSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClassesRequest(AbstractModel):
    """DescribeClasses request structure.

    """

    def __init__(self):
        r"""
        :param Zone: AZ ID, which can be obtained through the `DescribeZones` API.
        :type Zone: str
        :param DBEngine: Database engines. Valid values:
1. `postgresql` (TencentDB for PostgreSQL)
2. `mssql_compatible` (MSSQL compatible-TencentDB for PostgreSQL)
        :type DBEngine: str
        :param DBMajorVersion: Major version of a database, such as 12 or 13, which can be obtained through the `DescribeDBVersions` API.
        :type DBMajorVersion: str
        """
        self.Zone = None
        self.DBEngine = None
        self.DBMajorVersion = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.DBEngine = params.get("DBEngine")
        self.DBMajorVersion = params.get("DBMajorVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeClassesResponse(AbstractModel):
    """DescribeClasses response structure.

    """

    def __init__(self):
        r"""
        :param ClassInfoSet: List of database specifications
        :type ClassInfoSet: list of ClassInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ClassInfoSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ClassInfoSet") is not None:
            self.ClassInfoSet = []
            for item in params.get("ClassInfoSet"):
                obj = ClassInfo()
                obj._deserialize(item)
                self.ClassInfoSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCloneDBInstanceSpecRequest(AbstractModel):
    """DescribeCloneDBInstanceSpec request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID.
        :type DBInstanceId: str
        :param BackupSetId: Basic backup set ID. Either this parameter or `RecoveryTargetTime` must be passed in. If both are passed in, only this parameter takes effect.
        :type BackupSetId: str
        :param RecoveryTargetTime: Restoration time (UTC+8). Either this parameter or `BackupSetId` must be passed in.
        :type RecoveryTargetTime: str
        """
        self.DBInstanceId = None
        self.BackupSetId = None
        self.RecoveryTargetTime = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.BackupSetId = params.get("BackupSetId")
        self.RecoveryTargetTime = params.get("RecoveryTargetTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCloneDBInstanceSpecResponse(AbstractModel):
    """DescribeCloneDBInstanceSpec response structure.

    """

    def __init__(self):
        r"""
        :param MinSpecCode: Code of the minimum specification available for purchase.
        :type MinSpecCode: str
        :param MinStorage: The minimum disk capacity in GB available for purchase.
        :type MinStorage: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.MinSpecCode = None
        self.MinStorage = None
        self.RequestId = None


    def _deserialize(self, params):
        self.MinSpecCode = params.get("MinSpecCode")
        self.MinStorage = params.get("MinStorage")
        self.RequestId = params.get("RequestId")


class DescribeDBBackupsRequest(AbstractModel):
    """DescribeDBBackups request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-4wdeb0zv.
        :type DBInstanceId: str
        :param Type: Backup mode (1: full). Currently, only full backup is supported. The value is 1.
        :type Type: int
        :param StartTime: Query start time in the format of 2018-06-10 17:06:38, which cannot be more than 7 days ago
        :type StartTime: str
        :param EndTime: Query end time in the format of 2018-06-10 17:06:38
        :type EndTime: str
        :param Limit: Number of entries to be returned per page for backup list. Default value: 20. Minimum value: 1. Maximum value: 100. (If this parameter is left empty or 0, the default value will be used)
        :type Limit: int
        :param Offset: Page number for data return in paged query. Pagination starts from 0. Default value: 0.
        :type Offset: int
        """
        self.DBInstanceId = None
        self.Type = None
        self.StartTime = None
        self.EndTime = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.Type = params.get("Type")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBBackupsResponse(AbstractModel):
    """DescribeDBBackups response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of backup files in the returned backup list
        :type TotalCount: int
        :param BackupList: Backup list
        :type BackupList: list of DBBackup
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
                obj = DBBackup()
                obj._deserialize(item)
                self.BackupList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBErrlogsRequest(AbstractModel):
    """DescribeDBErrlogs request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-5bq3wfjd
        :type DBInstanceId: str
        :param StartTime: Query start time in the format of 2018-01-01 00:00:00, which cannot be more than 7 days ago
        :type StartTime: str
        :param EndTime: Query end time in the format of 2018-01-01 00:00:00
        :type EndTime: str
        :param DatabaseName: Database name
        :type DatabaseName: str
        :param SearchKeys: Search keyword
        :type SearchKeys: list of str
        :param Limit: Number of entries returned per page. Value range: 1-100
        :type Limit: int
        :param Offset: Page number for data return in paged query. Pagination starts from 0
        :type Offset: int
        """
        self.DBInstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.DatabaseName = None
        self.SearchKeys = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DatabaseName = params.get("DatabaseName")
        self.SearchKeys = params.get("SearchKeys")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBErrlogsResponse(AbstractModel):
    """DescribeDBErrlogs response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of date entries returned for this call
        :type TotalCount: int
        :param Details: Error log list
        :type Details: list of ErrLogDetail
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Details = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Details") is not None:
            self.Details = []
            for item in params.get("Details"):
                obj = ErrLogDetail()
                obj._deserialize(item)
                self.Details.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBInstanceAttributeRequest(AbstractModel):
    """DescribeDBInstanceAttribute request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBInstanceAttributeResponse(AbstractModel):
    """DescribeDBInstanceAttribute response structure.

    """

    def __init__(self):
        r"""
        :param DBInstance: Instance details.
        :type DBInstance: :class:`tencentcloud.postgres.v20170312.models.DBInstance`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DBInstance = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DBInstance") is not None:
            self.DBInstance = DBInstance()
            self.DBInstance._deserialize(params.get("DBInstance"))
        self.RequestId = params.get("RequestId")


class DescribeDBInstanceParametersRequest(AbstractModel):
    """DescribeDBInstanceParameters request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param ParamName: Name of the parameter to be queried. If `ParamName` is left empty or not passed in, the list of all parameters will be returned.
        :type ParamName: str
        """
        self.DBInstanceId = None
        self.ParamName = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.ParamName = params.get("ParamName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBInstanceParametersResponse(AbstractModel):
    """DescribeDBInstanceParameters response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of the parameters in the returned list
        :type TotalCount: int
        :param Detail: Details of the returned parameter list
        :type Detail: list of ParamInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Detail = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Detail") is not None:
            self.Detail = []
            for item in params.get("Detail"):
                obj = ParamInfo()
                obj._deserialize(item)
                self.Detail.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBInstanceSecurityGroupsRequest(AbstractModel):
    """DescribeDBInstanceSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID. Either this parameter or `ReadOnlyGroupId` must be passed in. If both parameters are passed in, `ReadOnlyGroupId` will be ignored.
        :type DBInstanceId: str
        :param ReadOnlyGroupId: RO group ID. Either this parameter or `DBInstanceId` must be passed in. To query the security groups associated with the RO groups, only pass in `ReadOnlyGroupId`.
        :type ReadOnlyGroupId: str
        """
        self.DBInstanceId = None
        self.ReadOnlyGroupId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBInstanceSecurityGroupsResponse(AbstractModel):
    """DescribeDBInstanceSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param SecurityGroupSet: Information of security groups in array
        :type SecurityGroupSet: list of SecurityGroup
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SecurityGroupSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SecurityGroupSet") is not None:
            self.SecurityGroupSet = []
            for item in params.get("SecurityGroupSet"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self.SecurityGroupSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBInstancesRequest(AbstractModel):
    """DescribeDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param Filters: Filter instances using one or more criteria. Valid filter names:
db-instance-id: filter by instance ID (in string format)
db-instance-name: filter by instance name (in string format)
db-project-id: filter by project ID (in integer format)
db-pay-mode: filter by billing mode (in string format)
db-tag-key: filter by tag key (in string format)
        :type Filters: list of Filter
        :param Limit: The maximum number of results returned per page. Value range: 1-100. Default: `10`
        :type Limit: int
        :param Offset: Data offset, which starts from 0.
        :type Offset: int
        :param OrderBy: Sorting metric, such as instance name or creation time. Valid values: DBInstanceId, CreateTime, Name, EndTime
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: `asc` (ascending), `desc` (descending)
        :type OrderByType: str
        """
        self.Filters = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBInstancesResponse(AbstractModel):
    """DescribeDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of instances found.
        :type TotalCount: int
        :param DBInstanceSet: Instance details set.
        :type DBInstanceSet: list of DBInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.DBInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DBInstanceSet") is not None:
            self.DBInstanceSet = []
            for item in params.get("DBInstanceSet"):
                obj = DBInstance()
                obj._deserialize(item)
                self.DBInstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBSlowlogsRequest(AbstractModel):
    """DescribeDBSlowlogs request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-lnp6j617
        :type DBInstanceId: str
        :param StartTime: Query start time in the format of 2018-06-10 17:06:38, which cannot be more than 7 days ago
        :type StartTime: str
        :param EndTime: Query end time in the format of 2018-06-10 17:06:38
        :type EndTime: str
        :param DatabaseName: Database name
        :type DatabaseName: str
        :param OrderBy: Metric for sorting. Valid values: `sum_calls` (total number of calls), `sum_cost_time` (total time consumed)
        :type OrderBy: str
        :param OrderByType: Sorting order. desc: descending, asc: ascending
        :type OrderByType: str
        :param Limit: Number of entries returned per page. Value range: 1-100. Default value: 20.
        :type Limit: int
        :param Offset: Page number for data return in paged query. Pagination starts from 0
        :type Offset: int
        """
        self.DBInstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.DatabaseName = None
        self.OrderBy = None
        self.OrderByType = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DatabaseName = params.get("DatabaseName")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBSlowlogsResponse(AbstractModel):
    """DescribeDBSlowlogs response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of date entries returned this time
        :type TotalCount: int
        :param Detail: Slow query log details
        :type Detail: :class:`tencentcloud.postgres.v20170312.models.SlowlogDetail`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Detail = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Detail") is not None:
            self.Detail = SlowlogDetail()
            self.Detail._deserialize(params.get("Detail"))
        self.RequestId = params.get("RequestId")


class DescribeDBVersionsRequest(AbstractModel):
    """DescribeDBVersions request structure.

    """


class DescribeDBVersionsResponse(AbstractModel):
    """DescribeDBVersions response structure.

    """

    def __init__(self):
        r"""
        :param VersionSet: List of database versions
        :type VersionSet: list of Version
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.VersionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("VersionSet") is not None:
            self.VersionSet = []
            for item in params.get("VersionSet"):
                obj = Version()
                obj._deserialize(item)
                self.VersionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBXlogsRequest(AbstractModel):
    """DescribeDBXlogs request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-4wdeb0zv.
        :type DBInstanceId: str
        :param StartTime: Query start time in the format of 2018-06-10 17:06:38, which cannot be more than 7 days ago
        :type StartTime: str
        :param EndTime: Query end time in the format of 2018-06-10 17:06:38
        :type EndTime: str
        :param Offset: Page number for data return in paged query. Pagination starts from 0
        :type Offset: int
        :param Limit: Number of entries returned per page in paged query. Value range: 1-100.
        :type Limit: int
        """
        self.DBInstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
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
        


class DescribeDBXlogsResponse(AbstractModel):
    """DescribeDBXlogs response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of date entries returned this time.
        :type TotalCount: int
        :param XlogList: Xlog list
        :type XlogList: list of Xlog
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.XlogList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("XlogList") is not None:
            self.XlogList = []
            for item in params.get("XlogList"):
                obj = Xlog()
                obj._deserialize(item)
                self.XlogList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatabasesRequest(AbstractModel):
    """DescribeDatabases request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatabasesResponse(AbstractModel):
    """DescribeDatabases response structure.

    """

    def __init__(self):
        r"""
        :param Items: Database information
        :type Items: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Items = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Items = params.get("Items")
        self.RequestId = params.get("RequestId")


class DescribeDefaultParametersRequest(AbstractModel):
    """DescribeDefaultParameters request structure.

    """

    def __init__(self):
        r"""
        :param DBMajorVersion: The major database version number, such as 11, 12, 13.
        :type DBMajorVersion: str
        :param DBEngine: Database engine, such as postgresql, mssql_compatible.
        :type DBEngine: str
        """
        self.DBMajorVersion = None
        self.DBEngine = None


    def _deserialize(self, params):
        self.DBMajorVersion = params.get("DBMajorVersion")
        self.DBEngine = params.get("DBEngine")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDefaultParametersResponse(AbstractModel):
    """DescribeDefaultParameters response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of parameters
        :type TotalCount: int
        :param ParamInfoSet: Parameter information
Note: This field may return null, indicating that no valid values can be obtained.
        :type ParamInfoSet: list of ParamInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ParamInfoSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ParamInfoSet") is not None:
            self.ParamInfoSet = []
            for item in params.get("ParamInfoSet"):
                obj = ParamInfo()
                obj._deserialize(item)
                self.ParamInfoSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeEncryptionKeysRequest(AbstractModel):
    """DescribeEncryptionKeys request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEncryptionKeysResponse(AbstractModel):
    """DescribeEncryptionKeys response structure.

    """

    def __init__(self):
        r"""
        :param EncryptionKeys: Instance key list
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type EncryptionKeys: list of EncryptionKey
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.EncryptionKeys = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("EncryptionKeys") is not None:
            self.EncryptionKeys = []
            for item in params.get("EncryptionKeys"):
                obj = EncryptionKey()
                obj._deserialize(item)
                self.EncryptionKeys.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeLogBackupsRequest(AbstractModel):
    """DescribeLogBackups request structure.

    """

    def __init__(self):
        r"""
        :param MinFinishTime: Minimum end time of a backup in the format of `2018-01-01 00:00:00`. It is 7 days ago by default.
        :type MinFinishTime: str
        :param MaxFinishTime: Maximum end time of a backup in the format of `2018-01-01 00:00:00`. It is the current time by default.
        :type MaxFinishTime: str
        :param Filters: Filter instances using one or more criteria. Valid filter names:
db-instance-id: Filter by instance ID (in string format).
db-instance-name: Filter by instance name (in string format).
db-instance-ip: Filter by instance VPC IP (in string format).
        :type Filters: list of Filter
        :param Limit: The maximum number of results returned per page. Value range: 1-100. Default: `10`.
        :type Limit: int
        :param Offset: Data offset, which starts from 0.
        :type Offset: int
        :param OrderBy: Sorting field. Valid values: `StartTime`, `FinishTime`, `Size`.
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: `asc` (ascending), `desc` (descending).
        :type OrderByType: str
        """
        self.MinFinishTime = None
        self.MaxFinishTime = None
        self.Filters = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        self.MinFinishTime = params.get("MinFinishTime")
        self.MaxFinishTime = params.get("MaxFinishTime")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLogBackupsResponse(AbstractModel):
    """DescribeLogBackups response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of queried log backups
        :type TotalCount: int
        :param LogBackupSet: List of log backup details
        :type LogBackupSet: list of LogBackup
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.LogBackupSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("LogBackupSet") is not None:
            self.LogBackupSet = []
            for item in params.get("LogBackupSet"):
                obj = LogBackup()
                obj._deserialize(item)
                self.LogBackupSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeOrdersRequest(AbstractModel):
    """DescribeOrders request structure.

    """

    def __init__(self):
        r"""
        :param DealNames: Order name set
        :type DealNames: list of str
        """
        self.DealNames = None


    def _deserialize(self, params):
        self.DealNames = params.get("DealNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeOrdersResponse(AbstractModel):
    """DescribeOrders response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of orders
        :type TotalCount: int
        :param Deals: Order array
        :type Deals: list of PgDeal
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Deals = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Deals") is not None:
            self.Deals = []
            for item in params.get("Deals"):
                obj = PgDeal()
                obj._deserialize(item)
                self.Deals.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeParameterTemplateAttributesRequest(AbstractModel):
    """DescribeParameterTemplateAttributes request structure.

    """

    def __init__(self):
        r"""
        :param TemplateId: Parameter template ID
        :type TemplateId: str
        """
        self.TemplateId = None


    def _deserialize(self, params):
        self.TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeParameterTemplateAttributesResponse(AbstractModel):
    """DescribeParameterTemplateAttributes response structure.

    """

    def __init__(self):
        r"""
        :param TemplateId: Parameter template ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type TemplateId: str
        :param TotalCount: Number of parameters contained in the parameter template
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalCount: int
        :param ParamInfoSet: Parameter information contained in the parameter template
Note: This field may return null, indicating that no valid values can be obtained.
        :type ParamInfoSet: list of ParamInfo
        :param TemplateName: Parameter template name
Note: This field may return null, indicating that no valid values can be obtained.
        :type TemplateName: str
        :param DBMajorVersion: Database version applicable to a parameter template
Note: This field may return null, indicating that no valid values can be obtained.
        :type DBMajorVersion: str
        :param DBEngine: Database engine applicable to a parameter template
Note: This field may return null, indicating that no valid values can be obtained.
        :type DBEngine: str
        :param TemplateDescription: Parameter template description
Note: This field may return null, indicating that no valid values can be obtained.
        :type TemplateDescription: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TemplateId = None
        self.TotalCount = None
        self.ParamInfoSet = None
        self.TemplateName = None
        self.DBMajorVersion = None
        self.DBEngine = None
        self.TemplateDescription = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TemplateId = params.get("TemplateId")
        self.TotalCount = params.get("TotalCount")
        if params.get("ParamInfoSet") is not None:
            self.ParamInfoSet = []
            for item in params.get("ParamInfoSet"):
                obj = ParamInfo()
                obj._deserialize(item)
                self.ParamInfoSet.append(obj)
        self.TemplateName = params.get("TemplateName")
        self.DBMajorVersion = params.get("DBMajorVersion")
        self.DBEngine = params.get("DBEngine")
        self.TemplateDescription = params.get("TemplateDescription")
        self.RequestId = params.get("RequestId")


class DescribeParameterTemplatesRequest(AbstractModel):
    """DescribeParameterTemplates request structure.

    """

    def __init__(self):
        r"""
        :param Filters: Filter conditions. Valid values: `TemplateName`, `TemplateId`, `DBMajorVersion`, `DBEngine`.
        :type Filters: list of Filter
        :param Limit: The maximum number of results returned per page. Value range: 0-100. Default: `20`.
        :type Limit: int
        :param Offset: Data offset
        :type Offset: int
        :param OrderBy: Sorting metric. Valid values: `CreateTime`, `TemplateName`, `DBMajorVersion`.
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: `asc` (ascending order),`desc` (descending order).
        :type OrderByType: str
        """
        self.Filters = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeParameterTemplatesResponse(AbstractModel):
    """DescribeParameterTemplates response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: The total number of eligible parameter templates
        :type TotalCount: int
        :param ParameterTemplateSet: Parameter template list
        :type ParameterTemplateSet: list of ParameterTemplate
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ParameterTemplateSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ParameterTemplateSet") is not None:
            self.ParameterTemplateSet = []
            for item in params.get("ParameterTemplateSet"):
                obj = ParameterTemplate()
                obj._deserialize(item)
                self.ParameterTemplateSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeParamsEventRequest(AbstractModel):
    """DescribeParamsEvent request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeParamsEventResponse(AbstractModel):
    """DescribeParamsEvent response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of modified parameters
        :type TotalCount: int
        :param EventItems: Details of parameter modification events
        :type EventItems: list of EventItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.EventItems = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("EventItems") is not None:
            self.EventItems = []
            for item in params.get("EventItems"):
                obj = EventItem()
                obj._deserialize(item)
                self.EventItems.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProductConfigRequest(AbstractModel):
    """DescribeProductConfig request structure.

    """

    def __init__(self):
        r"""
        :param Zone: AZ name
        :type Zone: str
        :param DBEngine: Database engines. Valid values:
1. `postgresql` (TencentDB for PostgreSQL)
2. `mssql_compatible` (MSSQL compatible-TencentDB for PostgreSQL)
Default value: `postgresql`
        :type DBEngine: str
        """
        self.Zone = None
        self.DBEngine = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.DBEngine = params.get("DBEngine")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeProductConfigResponse(AbstractModel):
    """DescribeProductConfig response structure.

    """

    def __init__(self):
        r"""
        :param SpecInfoList: Purchasable specification list.
        :type SpecInfoList: list of SpecInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SpecInfoList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SpecInfoList") is not None:
            self.SpecInfoList = []
            for item in params.get("SpecInfoList"):
                obj = SpecInfo()
                obj._deserialize(item)
                self.SpecInfoList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeReadOnlyGroupsRequest(AbstractModel):
    """DescribeReadOnlyGroups request structure.

    """

    def __init__(self):
        r"""
        :param Filters: Filter instances by using one or more filters. Valid values:  `db-master-instance-id` (filter by the primary instance ID in string), `read-only-group-id` (filter by the read-only group ID in string),
        :type Filters: list of Filter
        :param PageSize: The number of results per page. Default value: 10.
        :type PageSize: int
        :param PageNumber: Specify which page is displayed. Default value: 1 (the first page).
        :type PageNumber: int
        :param OrderBy: Sorting criterion. Valid values: `ROGroupId`, `CreateTime`, `Name`.
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: `desc`, `asc`.
        :type OrderByType: str
        """
        self.Filters = None
        self.PageSize = None
        self.PageNumber = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.PageSize = params.get("PageSize")
        self.PageNumber = params.get("PageNumber")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeReadOnlyGroupsResponse(AbstractModel):
    """DescribeReadOnlyGroups response structure.

    """

    def __init__(self):
        r"""
        :param ReadOnlyGroupList: RO group list
        :type ReadOnlyGroupList: list of ReadOnlyGroup
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ReadOnlyGroupList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ReadOnlyGroupList") is not None:
            self.ReadOnlyGroupList = []
            for item in params.get("ReadOnlyGroupList"):
                obj = ReadOnlyGroup()
                obj._deserialize(item)
                self.ReadOnlyGroupList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRegionsRequest(AbstractModel):
    """DescribeRegions request structure.

    """


class DescribeRegionsResponse(AbstractModel):
    """DescribeRegions response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of returned results.
        :type TotalCount: int
        :param RegionSet: Region information set.
        :type RegionSet: list of RegionInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.RegionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RegionSet") is not None:
            self.RegionSet = []
            for item in params.get("RegionSet"):
                obj = RegionInfo()
                obj._deserialize(item)
                self.RegionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeServerlessDBInstancesRequest(AbstractModel):
    """DescribeServerlessDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param Filter: Query conditions
        :type Filter: list of Filter
        :param Limit: The number of queries
        :type Limit: int
        :param Offset: The offset value
        :type Offset: int
        :param OrderBy: Sorting metric. Currently, only "CreateTime" (instance creation time) is supported.
        :type OrderBy: str
        :param OrderByType: Sorting order. Ascending and descending are supported.
        :type OrderByType: str
        """
        self.Filter = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None


    def _deserialize(self, params):
        if params.get("Filter") is not None:
            self.Filter = []
            for item in params.get("Filter"):
                obj = Filter()
                obj._deserialize(item)
                self.Filter.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeServerlessDBInstancesResponse(AbstractModel):
    """DescribeServerlessDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: The number of query results
        :type TotalCount: int
        :param DBInstanceSet: Query results
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBInstanceSet: list of ServerlessDBInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.DBInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DBInstanceSet") is not None:
            self.DBInstanceSet = []
            for item in params.get("DBInstanceSet"):
                obj = ServerlessDBInstance()
                obj._deserialize(item)
                self.DBInstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSlowQueryAnalysisRequest(AbstractModel):
    """DescribeSlowQueryAnalysis request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID.
        :type DBInstanceId: str
        :param StartTime: Start timestamp of the query range in the format of "YYYY-MM-DD HH:mm:ss". The log is retained for seven days by default, so the start timestamp must fall within the retention period.
        :type StartTime: str
        :param EndTime: End timestamp of the query range in the format of "YYYY-MM-DD HH:mm:ss".
        :type EndTime: str
        :param DatabaseName: Filter by database name. This parameter is optional.
        :type DatabaseName: str
        :param OrderBy: Sort by field. Valid values: `CallNum`, `CostTime`, `AvgCostTime`. Default value: `CallNum`.
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: `asc` (ascending), `desc` (descending). Default value: `desc`.
        :type OrderByType: str
        :param Limit: Number of entries per page. Value range: [1,100]. Default value: `50`.
        :type Limit: int
        :param Offset: Pagination offset. Value range: [0,INF). Default value: `0`.
        :type Offset: int
        """
        self.DBInstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.DatabaseName = None
        self.OrderBy = None
        self.OrderByType = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DatabaseName = params.get("DatabaseName")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSlowQueryAnalysisResponse(AbstractModel):
    """DescribeSlowQueryAnalysis response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: The total number of query results.
        :type TotalCount: int
        :param Detail: Detailed analysis.
        :type Detail: :class:`tencentcloud.postgres.v20170312.models.Detail`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Detail = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Detail") is not None:
            self.Detail = Detail()
            self.Detail._deserialize(params.get("Detail"))
        self.RequestId = params.get("RequestId")


class DescribeSlowQueryListRequest(AbstractModel):
    """DescribeSlowQueryList request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID.
        :type DBInstanceId: str
        :param StartTime: Start timestamp of the query range in the format of "YYYY-MM-DD HH:mm:ss". The log is retained for seven days by default, so the start timestamp must fall within the retention period.
        :type StartTime: str
        :param EndTime: End timestamp of the query range in the format of "YYYY-MM-DD HH:mm:ss".
        :type EndTime: str
        :param DatabaseName: Filter by database name. This parameter is optional.
        :type DatabaseName: str
        :param OrderByType: Sorting order. Valid values: `asc` (ascending), `desc` (descending). Default value: `desc`.
        :type OrderByType: str
        :param OrderBy: Sort by field. Valid values: `SessionStartTime` (default), `Duration`.
        :type OrderBy: str
        :param Limit: Number of entries per page. Value range: [1,100]. Default value: `20`.
        :type Limit: int
        :param Offset: Pagination offset. Value range: [0,INF). Default value: `0`.
        :type Offset: int
        """
        self.DBInstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.DatabaseName = None
        self.OrderByType = None
        self.OrderBy = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DatabaseName = params.get("DatabaseName")
        self.OrderByType = params.get("OrderByType")
        self.OrderBy = params.get("OrderBy")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSlowQueryListResponse(AbstractModel):
    """DescribeSlowQueryList response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: The total number of slow query statements during the specified period of time.
        :type TotalCount: int
        :param DurationAnalysis: Analysis of the execution time of slow query statements by classifying them to different time ranges. These slow query statements fall within the query range you specified in the request parameters.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DurationAnalysis: list of DurationAnalysis
        :param RawSlowQueryList: The list of slow query details during the specified period of time.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type RawSlowQueryList: list of RawSlowQuery
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.DurationAnalysis = None
        self.RawSlowQueryList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DurationAnalysis") is not None:
            self.DurationAnalysis = []
            for item in params.get("DurationAnalysis"):
                obj = DurationAnalysis()
                obj._deserialize(item)
                self.DurationAnalysis.append(obj)
        if params.get("RawSlowQueryList") is not None:
            self.RawSlowQueryList = []
            for item in params.get("RawSlowQueryList"):
                obj = RawSlowQuery()
                obj._deserialize(item)
                self.RawSlowQueryList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeZonesRequest(AbstractModel):
    """DescribeZones request structure.

    """


class DescribeZonesResponse(AbstractModel):
    """DescribeZones response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of returned results.
        :type TotalCount: int
        :param ZoneSet: AZ information set.
        :type ZoneSet: list of ZoneInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ZoneSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ZoneSet") is not None:
            self.ZoneSet = []
            for item in params.get("ZoneSet"):
                obj = ZoneInfo()
                obj._deserialize(item)
                self.ZoneSet.append(obj)
        self.RequestId = params.get("RequestId")


class DestroyDBInstanceRequest(AbstractModel):
    """DestroyDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: The ID of the instance to be eliminated
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DestroyDBInstanceResponse(AbstractModel):
    """DestroyDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Detail(AbstractModel):
    """Details returned by the `DescribeSlowQueryAnalysis` API

    """

    def __init__(self):
        r"""
        :param TotalTime: The total execution time (in ms) of all slow query statements during the specified period of time
        :type TotalTime: float
        :param TotalCallNum: The total number of all slow query statements during the specified period of time
        :type TotalCallNum: int
        :param AnalysisItems: The statistical analysis list of slow queries
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type AnalysisItems: list of AnalysisItems
        """
        self.TotalTime = None
        self.TotalCallNum = None
        self.AnalysisItems = None


    def _deserialize(self, params):
        self.TotalTime = params.get("TotalTime")
        self.TotalCallNum = params.get("TotalCallNum")
        if params.get("AnalysisItems") is not None:
            self.AnalysisItems = []
            for item in params.get("AnalysisItems"):
                obj = AnalysisItems()
                obj._deserialize(item)
                self.AnalysisItems.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisIsolateDBInstancesRequest(AbstractModel):
    """DisIsolateDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceIdSet: List of resource IDs. Note that currently you cannot remove multiple instances from isolation at the same time. Only one instance ID can be passed in here.
        :type DBInstanceIdSet: list of str
        :param Period: The valid period (in months) of the monthly-subscribed instance when removing it from isolation
        :type Period: int
        :param AutoVoucher: Whether to use vouchers. Valid values: `true` (yes), `false` (no). Default value: `false`.
        :type AutoVoucher: bool
        :param VoucherIds: Voucher ID list
        :type VoucherIds: list of str
        """
        self.DBInstanceIdSet = None
        self.Period = None
        self.AutoVoucher = None
        self.VoucherIds = None


    def _deserialize(self, params):
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        self.Period = params.get("Period")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisIsolateDBInstancesResponse(AbstractModel):
    """DisIsolateDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DurationAnalysis(AbstractModel):
    """Analyze the execution time of slow query statements by classifying them to different time ranges

    """

    def __init__(self):
        r"""
        :param TimeSegment: Time range
        :type TimeSegment: str
        :param Count: The number of slow query statements whose execution time falls within the time range
        :type Count: int
        """
        self.TimeSegment = None
        self.Count = None


    def _deserialize(self, params):
        self.TimeSegment = params.get("TimeSegment")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EncryptionKey(AbstractModel):
    """KMS key information

    """

    def __init__(self):
        r"""
        :param KeyId: Encrypted KeyId of KMS instance
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type KeyId: str
        :param KeyAlias: Encryption key alias of KMS instance 
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type KeyAlias: str
        :param DEKCipherTextBlob: Instance DEK ciphertext
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type DEKCipherTextBlob: str
        :param IsEnabled: Whether the key is enabled. Valid values: `1` (yes), `0` (no)
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type IsEnabled: int
        :param KeyRegion: Region where KMS key resides
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type KeyRegion: str
        :param CreateTime: DEK key creation time
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type CreateTime: str
        """
        self.KeyId = None
        self.KeyAlias = None
        self.DEKCipherTextBlob = None
        self.IsEnabled = None
        self.KeyRegion = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.KeyId = params.get("KeyId")
        self.KeyAlias = params.get("KeyAlias")
        self.DEKCipherTextBlob = params.get("DEKCipherTextBlob")
        self.IsEnabled = params.get("IsEnabled")
        self.KeyRegion = params.get("KeyRegion")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ErrLogDetail(AbstractModel):
    """Error log details

    """

    def __init__(self):
        r"""
        :param UserName: Username
        :type UserName: str
        :param Database: Database name
        :type Database: str
        :param ErrTime: Error occurrence time
        :type ErrTime: str
        :param ErrMsg: Error message
        :type ErrMsg: str
        """
        self.UserName = None
        self.Database = None
        self.ErrTime = None
        self.ErrMsg = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.Database = params.get("Database")
        self.ErrTime = params.get("ErrTime")
        self.ErrMsg = params.get("ErrMsg")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EventInfo(AbstractModel):
    """Parameter modification event information

    """

    def __init__(self):
        r"""
        :param ParamName: Parameter name
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ParamName: str
        :param OldValue: Original parameter value
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type OldValue: str
        :param NewValue: New parameter value in this modification event
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type NewValue: str
        :param ModifyTime: Start time of parameter modification
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ModifyTime: str
        :param EffectiveTime: Start time when the modified parameter takes effect
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type EffectiveTime: str
        :param State: Modification status
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type State: str
        :param Operator: Operator (generally, the value is the UIN of a sub-user)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Operator: str
        :param EventLog: Event log
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type EventLog: str
        """
        self.ParamName = None
        self.OldValue = None
        self.NewValue = None
        self.ModifyTime = None
        self.EffectiveTime = None
        self.State = None
        self.Operator = None
        self.EventLog = None


    def _deserialize(self, params):
        self.ParamName = params.get("ParamName")
        self.OldValue = params.get("OldValue")
        self.NewValue = params.get("NewValue")
        self.ModifyTime = params.get("ModifyTime")
        self.EffectiveTime = params.get("EffectiveTime")
        self.State = params.get("State")
        self.Operator = params.get("Operator")
        self.EventLog = params.get("EventLog")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EventItem(AbstractModel):
    """Modification details of one parameter

    """

    def __init__(self):
        r"""
        :param ParamName: Parameter name
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ParamName: str
        :param EventCount: The number of modification events
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type EventCount: int
        :param EventDetail: Modification event details
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type EventDetail: list of EventInfo
        """
        self.ParamName = None
        self.EventCount = None
        self.EventDetail = None


    def _deserialize(self, params):
        self.ParamName = params.get("ParamName")
        self.EventCount = params.get("EventCount")
        if params.get("EventDetail") is not None:
            self.EventDetail = []
            for item in params.get("EventDetail"):
                obj = EventInfo()
                obj._deserialize(item)
                self.EventDetail.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Filter(AbstractModel):
    """Key-value pair filter for conditional filtering queries, such as filter ID and name
    * If more than one filter exists, the logical relationship between these filters is `AND`.
    * If multiple values exist in one filter, the logical relationship between these values is `OR`.

    """

    def __init__(self):
        r"""
        :param Name: Filter name.
        :type Name: str
        :param Values: One or more filter values.
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
        


class InitDBInstancesRequest(AbstractModel):
    """InitDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceIdSet: Instance ID set.
        :type DBInstanceIdSet: list of str
        :param AdminName: Instance admin account username.
        :type AdminName: str
        :param AdminPassword: Password corresponding to instance root account username.
        :type AdminPassword: str
        :param Charset: Instance character set. Valid values: UTF8, LATIN1.
        :type Charset: str
        """
        self.DBInstanceIdSet = None
        self.AdminName = None
        self.AdminPassword = None
        self.Charset = None


    def _deserialize(self, params):
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        self.AdminName = params.get("AdminName")
        self.AdminPassword = params.get("AdminPassword")
        self.Charset = params.get("Charset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InitDBInstancesResponse(AbstractModel):
    """InitDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceIdSet: Instance ID set.
        :type DBInstanceIdSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DBInstanceIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        self.RequestId = params.get("RequestId")


class InquiryPriceCreateDBInstancesRequest(AbstractModel):
    """InquiryPriceCreateDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param Zone: AZ ID, which can be obtained through the `Zone` field in the returned value of the `DescribeZones` API.
        :type Zone: str
        :param SpecCode: Specification ID, which can be obtained through the `SpecCode` field in the returned value of the `DescribeProductConfig` API.
        :type SpecCode: str
        :param Storage: Storage capacity size in GB.
        :type Storage: int
        :param InstanceCount: Number of instances. Maximum value: 100. If you need to create more instances at a time, please contact customer service.
        :type InstanceCount: int
        :param Period: Length of purchase in months. Currently, only 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, and 36 are supported.
        :type Period: int
        :param Pid: [Disused] Billing ID, which can be obtained through the `Pid` field in the returned value of the `DescribeProductConfig` API.
        :type Pid: int
        :param InstanceChargeType: Instance billing type. Valid value: POSTPAID_BY_HOUR (pay-as-you-go)
        :type InstanceChargeType: str
        :param InstanceType: Instance type. Default value: `primary`. Valid values:
`primary` (dual-server high-availability, one-primary-one-standby)
`readonly` (read-only instance)
        :type InstanceType: str
        :param DBEngine: 
        :type DBEngine: str
        """
        self.Zone = None
        self.SpecCode = None
        self.Storage = None
        self.InstanceCount = None
        self.Period = None
        self.Pid = None
        self.InstanceChargeType = None
        self.InstanceType = None
        self.DBEngine = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.SpecCode = params.get("SpecCode")
        self.Storage = params.get("Storage")
        self.InstanceCount = params.get("InstanceCount")
        self.Period = params.get("Period")
        self.Pid = params.get("Pid")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.InstanceType = params.get("InstanceType")
        self.DBEngine = params.get("DBEngine")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceCreateDBInstancesResponse(AbstractModel):
    """InquiryPriceCreateDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param OriginalPrice: Published price in US Cent
        :type OriginalPrice: int
        :param Price: Discounted total amount in US Cent
        :type Price: int
        :param Currency: Currency, such as USD.
        :type Currency: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OriginalPrice = None
        self.Price = None
        self.Currency = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.Price = params.get("Price")
        self.Currency = params.get("Currency")
        self.RequestId = params.get("RequestId")


class InquiryPriceRenewDBInstanceRequest(AbstractModel):
    """InquiryPriceRenewDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param Period: Renewal duration in months. Maximum value: 48
        :type Period: int
        """
        self.DBInstanceId = None
        self.Period = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.Period = params.get("Period")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceRenewDBInstanceResponse(AbstractModel):
    """InquiryPriceRenewDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param OriginalPrice: Published price in cents. For example, 24650 indicates 246.5 USD.
        :type OriginalPrice: int
        :param Price: Discounted total amount. For example, 24650 indicates 246.5 USD.
        :type Price: int
        :param Currency: Currency, such as USD.
        :type Currency: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OriginalPrice = None
        self.Price = None
        self.Currency = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.Price = params.get("Price")
        self.Currency = params.get("Currency")
        self.RequestId = params.get("RequestId")


class InquiryPriceUpgradeDBInstanceRequest(AbstractModel):
    """InquiryPriceUpgradeDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param Storage: Instance disk size in GB
        :type Storage: int
        :param Memory: Instance memory size in GB
        :type Memory: int
        :param DBInstanceId: Instance ID in the format of postgres-hez4fh0v
        :type DBInstanceId: str
        :param InstanceChargeType: Instance billing type. Valid value: `POSTPAID_BY_HOUR` (pay-as-you-go hourly)
        :type InstanceChargeType: str
        """
        self.Storage = None
        self.Memory = None
        self.DBInstanceId = None
        self.InstanceChargeType = None


    def _deserialize(self, params):
        self.Storage = params.get("Storage")
        self.Memory = params.get("Memory")
        self.DBInstanceId = params.get("DBInstanceId")
        self.InstanceChargeType = params.get("InstanceChargeType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceUpgradeDBInstanceResponse(AbstractModel):
    """InquiryPriceUpgradeDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param OriginalPrice: Total cost before discount.
        :type OriginalPrice: int
        :param Price: Discounted total amount
        :type Price: int
        :param Currency: Currency, such as USD.
        :type Currency: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.OriginalPrice = None
        self.Price = None
        self.Currency = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.Price = params.get("Price")
        self.Currency = params.get("Currency")
        self.RequestId = params.get("RequestId")


class IsolateDBInstancesRequest(AbstractModel):
    """IsolateDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceIdSet: List of instance IDs. Note that currently you cannot isolate multiple instances at the same time. Only one instance ID can be passed in here.
        :type DBInstanceIdSet: list of str
        """
        self.DBInstanceIdSet = None


    def _deserialize(self, params):
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateDBInstancesResponse(AbstractModel):
    """IsolateDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class LogBackup(AbstractModel):
    """Log backup information of a database

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param Id: Unique ID of a backup file
        :type Id: str
        :param Name: Backup file name
        :type Name: str
        :param BackupMethod: Backup method, including physical and logical.
        :type BackupMethod: str
        :param BackupMode: Backup mode, including automatic and manual.
        :type BackupMode: str
        :param State: Backup task status
        :type State: str
        :param Size: Backup set size in bytes
        :type Size: int
        :param StartTime: Backup start time
        :type StartTime: str
        :param FinishTime: Backup end time
        :type FinishTime: str
        :param ExpireTime: Backup expiration time
        :type ExpireTime: str
        """
        self.DBInstanceId = None
        self.Id = None
        self.Name = None
        self.BackupMethod = None
        self.BackupMode = None
        self.State = None
        self.Size = None
        self.StartTime = None
        self.FinishTime = None
        self.ExpireTime = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.BackupMethod = params.get("BackupMethod")
        self.BackupMode = params.get("BackupMode")
        self.State = params.get("State")
        self.Size = params.get("Size")
        self.StartTime = params.get("StartTime")
        self.FinishTime = params.get("FinishTime")
        self.ExpireTime = params.get("ExpireTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAccountRemarkRequest(AbstractModel):
    """ModifyAccountRemark request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-4wdeb0zv
        :type DBInstanceId: str
        :param UserName: Instance username
        :type UserName: str
        :param Remark: New remarks corresponding to user `UserName`
        :type Remark: str
        """
        self.DBInstanceId = None
        self.UserName = None
        self.Remark = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.UserName = params.get("UserName")
        self.Remark = params.get("Remark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAccountRemarkResponse(AbstractModel):
    """ModifyAccountRemark response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBackupDownloadRestrictionRequest(AbstractModel):
    """ModifyBackupDownloadRestriction request structure.

    """

    def __init__(self):
        r"""
        :param RestrictionType: Type of the network restrictions for downloading a backup file. Valid values: `NONE` (backups can be downloaded over both private and public networks), `INTRANET` (backups can only be downloaded over the private network), `CUSTOMIZE` (backups can be downloaded over specified VPCs or at specified IPs).
        :type RestrictionType: str
        :param VpcRestrictionEffect: Whether VPC is allowed. Valid values: `ALLOW` (allow), `DENY` (deny).
        :type VpcRestrictionEffect: str
        :param VpcIdSet: Whether it is allowed to download the VPC ID list of the backup files.
        :type VpcIdSet: list of str
        :param IpRestrictionEffect: Whether IP is allowed. Valid values: `ALLOW` (allow), `DENY` (deny).
        :type IpRestrictionEffect: str
        :param IpSet: Whether it is allowed to download the IP list of the backup files.
        :type IpSet: list of str
        """
        self.RestrictionType = None
        self.VpcRestrictionEffect = None
        self.VpcIdSet = None
        self.IpRestrictionEffect = None
        self.IpSet = None


    def _deserialize(self, params):
        self.RestrictionType = params.get("RestrictionType")
        self.VpcRestrictionEffect = params.get("VpcRestrictionEffect")
        self.VpcIdSet = params.get("VpcIdSet")
        self.IpRestrictionEffect = params.get("IpRestrictionEffect")
        self.IpSet = params.get("IpSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBackupDownloadRestrictionResponse(AbstractModel):
    """ModifyBackupDownloadRestriction response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBackupPlanRequest(AbstractModel):
    """ModifyBackupPlan request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param MinBackupStartTime: The earliest time to start a backup
        :type MinBackupStartTime: str
        :param MaxBackupStartTime: The latest time to start a backup
        :type MaxBackupStartTime: str
        :param BaseBackupRetentionPeriod: Backup retention period in days. Value range: 3-7
        :type BaseBackupRetentionPeriod: int
        :param BackupPeriod: Backup cycle, which means on which days each week the instance will be backed up. The parameter value should be the lowercase names of the days of the week.
        :type BackupPeriod: list of str
        """
        self.DBInstanceId = None
        self.MinBackupStartTime = None
        self.MaxBackupStartTime = None
        self.BaseBackupRetentionPeriod = None
        self.BackupPeriod = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.MinBackupStartTime = params.get("MinBackupStartTime")
        self.MaxBackupStartTime = params.get("MaxBackupStartTime")
        self.BaseBackupRetentionPeriod = params.get("BaseBackupRetentionPeriod")
        self.BackupPeriod = params.get("BackupPeriod")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBackupPlanResponse(AbstractModel):
    """ModifyBackupPlan response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBaseBackupExpireTimeRequest(AbstractModel):
    """ModifyBaseBackupExpireTime request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param BaseBackupId: Base backup ID
        :type BaseBackupId: str
        :param NewExpireTime: New expiration time
        :type NewExpireTime: str
        """
        self.DBInstanceId = None
        self.BaseBackupId = None
        self.NewExpireTime = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.BaseBackupId = params.get("BaseBackupId")
        self.NewExpireTime = params.get("NewExpireTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBaseBackupExpireTimeResponse(AbstractModel):
    """ModifyBaseBackupExpireTime response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceChargeTypeRequest(AbstractModel):
    """ModifyDBInstanceChargeType request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of `postgres-6fego161`
        :type DBInstanceId: str
        :param InstanceChargeType: Instance billing mode.  Valid values:  `PREPAID` (monthly subscription), `POSTPAID_BY_HOUR` (pay-as-you-go). Default value:  `PREPAID`.
        :type InstanceChargeType: str
        :param Period: Validity period  in months. Valid values:  Valid period in months of the purchased instance. Valid values: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `24`, `36`. This parameter is set to `1` when the pay-as-you-go billing mode is used.
        :type Period: int
        :param AutoRenewFlag: Renewal flag. Valid values；  Valid values: `0` (manual renewal), `1` (auto-renewal).
        :type AutoRenewFlag: int
        :param AutoVoucher: Whether to automatically use vouchers. Valid values: `1` (yes), `0` (no). Default value: `0`.
        :type AutoVoucher: int
        """
        self.DBInstanceId = None
        self.InstanceChargeType = None
        self.Period = None
        self.AutoRenewFlag = None
        self.AutoVoucher = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.Period = params.get("Period")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.AutoVoucher = params.get("AutoVoucher")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceChargeTypeResponse(AbstractModel):
    """ModifyDBInstanceChargeType response structure.

    """

    def __init__(self):
        r"""
        :param DealName: Order name
        :type DealName: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceDeploymentRequest(AbstractModel):
    """ModifyDBInstanceDeployment request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID.
        :type DBInstanceId: str
        :param DBNodeSet: Instance node information.
        :type DBNodeSet: list of DBNode
        :param SwitchTag: Switch time. Valid values: `0` (switch now), `1` (switch at a specified time), `2` (switch during maintenance time). Default value: `0`.
        :type SwitchTag: int
        :param SwitchStartTime: Switch start time in the format of `HH:MM:SS`, such as 01:00:00. When `SwitchTag` is 0 or 2, this parameter becomes invalid.
        :type SwitchStartTime: str
        :param SwitchEndTime: Switch end time in the format of `HH:MM:SS`, such as 01:30:00. When `SwitchTag` is 0 or 2, this parameter becomes invalid.
        :type SwitchEndTime: str
        """
        self.DBInstanceId = None
        self.DBNodeSet = None
        self.SwitchTag = None
        self.SwitchStartTime = None
        self.SwitchEndTime = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        if params.get("DBNodeSet") is not None:
            self.DBNodeSet = []
            for item in params.get("DBNodeSet"):
                obj = DBNode()
                obj._deserialize(item)
                self.DBNodeSet.append(obj)
        self.SwitchTag = params.get("SwitchTag")
        self.SwitchStartTime = params.get("SwitchStartTime")
        self.SwitchEndTime = params.get("SwitchEndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceDeploymentResponse(AbstractModel):
    """ModifyDBInstanceDeployment response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceNameRequest(AbstractModel):
    """ModifyDBInstanceName request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Database instance ID in the format of postgres-6fego161
        :type DBInstanceId: str
        :param InstanceName: New name of database instance
        :type InstanceName: str
        """
        self.DBInstanceId = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.InstanceName = params.get("InstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceNameResponse(AbstractModel):
    """ModifyDBInstanceName response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceParametersRequest(AbstractModel):
    """ModifyDBInstanceParameters request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param ParamList: Parameters to be modified and their new values
        :type ParamList: list of ParamEntry
        """
        self.DBInstanceId = None
        self.ParamList = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        if params.get("ParamList") is not None:
            self.ParamList = []
            for item in params.get("ParamList"):
                obj = ParamEntry()
                obj._deserialize(item)
                self.ParamList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceParametersResponse(AbstractModel):
    """ModifyDBInstanceParameters response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceReadOnlyGroupRequest(AbstractModel):
    """ModifyDBInstanceReadOnlyGroup request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param ReadOnlyGroupId: ID of the RO group to which the read-only replica belongs
        :type ReadOnlyGroupId: str
        :param NewReadOnlyGroupId: ID of the new RO group into which the read-only replica will move
        :type NewReadOnlyGroupId: str
        """
        self.DBInstanceId = None
        self.ReadOnlyGroupId = None
        self.NewReadOnlyGroupId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        self.NewReadOnlyGroupId = params.get("NewReadOnlyGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceReadOnlyGroupResponse(AbstractModel):
    """ModifyDBInstanceReadOnlyGroup response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID
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
        :param SecurityGroupIdSet: The list of security groups to be associated with the instance or RO groups
        :type SecurityGroupIdSet: list of str
        :param DBInstanceId: Instance ID. Either this parameter or `ReadOnlyGroupId` must be passed in. If both parameters are passed in, `ReadOnlyGroupId` will be ignored.
        :type DBInstanceId: str
        :param ReadOnlyGroupId: RO group ID. Either this parameter or `DBInstanceId` must be passed in. To modify  the security groups associated with the RO groups, only pass in `ReadOnlyGroupId`.
        :type ReadOnlyGroupId: str
        """
        self.SecurityGroupIdSet = None
        self.DBInstanceId = None
        self.ReadOnlyGroupId = None


    def _deserialize(self, params):
        self.SecurityGroupIdSet = params.get("SecurityGroupIdSet")
        self.DBInstanceId = params.get("DBInstanceId")
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
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


class ModifyDBInstanceSpecRequest(AbstractModel):
    """ModifyDBInstanceSpec request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-6bwgamo3.
        :type DBInstanceId: str
        :param Memory: Instance memory size in GiB after modification.
        :type Memory: int
        :param Storage: Instance disk size in GiB after modification.
        :type Storage: int
        :param AutoVoucher: Whether to automatically use vouchers. Valid values: `1` (yes), `0` (no). Default value: `0`.
        :type AutoVoucher: int
        :param VoucherIds: Voucher ID list. Currently, you can specify only one voucher.
        :type VoucherIds: list of str
        :param ActivityId: Campaign ID.
        :type ActivityId: int
        :param SwitchTag: Switch time after instance configurations are modified. Valid values: `0` (switch now), `1` (switch at a specified time), `2` (switch during maintenance time). Default value: `0`.
        :type SwitchTag: int
        :param SwitchStartTime: Switch start time in the format of `HH:MM:SS`, such as 01:00:00. When `SwitchTag` is 0 or 2, this parameter becomes invalid.
        :type SwitchStartTime: str
        :param SwitchEndTime: Switch end time in the format of `HH:MM:SS`, such as 01:30:00. When `SwitchTag` is 0 or 2, this parameter becomes invalid.
        :type SwitchEndTime: str
        """
        self.DBInstanceId = None
        self.Memory = None
        self.Storage = None
        self.AutoVoucher = None
        self.VoucherIds = None
        self.ActivityId = None
        self.SwitchTag = None
        self.SwitchStartTime = None
        self.SwitchEndTime = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        self.ActivityId = params.get("ActivityId")
        self.SwitchTag = params.get("SwitchTag")
        self.SwitchStartTime = params.get("SwitchStartTime")
        self.SwitchEndTime = params.get("SwitchEndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceSpecResponse(AbstractModel):
    """ModifyDBInstanceSpec response structure.

    """

    def __init__(self):
        r"""
        :param DealName: Order ID.
        :type DealName: str
        :param BillId: Bill ID of frozen fees.
        :type BillId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealName = None
        self.BillId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.BillId = params.get("BillId")
        self.RequestId = params.get("RequestId")


class ModifyDBInstancesProjectRequest(AbstractModel):
    """ModifyDBInstancesProject request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceIdSet: List of instance IDs. Note that currently you cannot manipulate multiple instances at the same time. Only one instance ID can be passed in here.
        :type DBInstanceIdSet: list of str
        :param ProjectId: ID of the new project
        :type ProjectId: str
        """
        self.DBInstanceIdSet = None
        self.ProjectId = None


    def _deserialize(self, params):
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        self.ProjectId = params.get("ProjectId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstancesProjectResponse(AbstractModel):
    """ModifyDBInstancesProject response structure.

    """

    def __init__(self):
        r"""
        :param Count: Number of successfully transferred instances
        :type Count: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Count = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.RequestId = params.get("RequestId")


class ModifyParameterTemplateRequest(AbstractModel):
    """ModifyParameterTemplate request structure.

    """

    def __init__(self):
        r"""
        :param TemplateId: Parameter template ID, which uniquely identifies a parameter template and cannot be modified.
        :type TemplateId: str
        :param TemplateName: Parameter template name, which can contain 1-60 letters, digits, and symbols (-_./()[]()+=:@). If this field is empty, the original parameter template name will be used.
        :type TemplateName: str
        :param TemplateDescription: Parameter template description, which can contain 1-60 letters, digits, and symbols (-_./()[]()+=:@). If this parameter is not passed in, the original parameter template description will be used.
        :type TemplateDescription: str
        :param ModifyParamEntrySet: The set of parameters to be modified or added. A parameter cannot be put to `ModifyParamEntrySet` and `DeleteParamSet` at the same time, that is, it cannot be modified/added and deleted at the same time.
        :type ModifyParamEntrySet: list of ParamEntry
        :param DeleteParamSet: The set of parameters to be deleted in the template. A parameter cannot be put to `ModifyParamEntrySet` and `DeleteParamSet` at the same time, that is, it cannot be modified/added and deleted at the same time.
        :type DeleteParamSet: list of str
        """
        self.TemplateId = None
        self.TemplateName = None
        self.TemplateDescription = None
        self.ModifyParamEntrySet = None
        self.DeleteParamSet = None


    def _deserialize(self, params):
        self.TemplateId = params.get("TemplateId")
        self.TemplateName = params.get("TemplateName")
        self.TemplateDescription = params.get("TemplateDescription")
        if params.get("ModifyParamEntrySet") is not None:
            self.ModifyParamEntrySet = []
            for item in params.get("ModifyParamEntrySet"):
                obj = ParamEntry()
                obj._deserialize(item)
                self.ModifyParamEntrySet.append(obj)
        self.DeleteParamSet = params.get("DeleteParamSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyParameterTemplateResponse(AbstractModel):
    """ModifyParameterTemplate response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyReadOnlyGroupConfigRequest(AbstractModel):
    """ModifyReadOnlyGroupConfig request structure.

    """

    def __init__(self):
        r"""
        :param ReadOnlyGroupId: RO group ID
        :type ReadOnlyGroupId: str
        :param ReadOnlyGroupName: RO group name
        :type ReadOnlyGroupName: str
        :param ReplayLagEliminate: Whether to remove a read-only replica from an RO group if the delay between the read-only replica and the primary instance exceeds the threshold. Valid values: `0` (no), `1` (yes).
        :type ReplayLagEliminate: int
        :param ReplayLatencyEliminate: Whether to remove a read-only replica from an RO group if the sync log size difference between the read-only replica and the primary instance exceeds the threshold. Valid values: `0` (no), `1` (yes).
        :type ReplayLatencyEliminate: int
        :param MaxReplayLatency: Delayed log size threshold in MB
        :type MaxReplayLatency: int
        :param MaxReplayLag: Delay threshold in ms
        :type MaxReplayLag: int
        :param Rebalance: Whether to enable automatic load balancing. Valid values: `0` (disable), `1` (enable).
        :type Rebalance: int
        :param MinDelayEliminateReserve: The minimum number of read-only replicas that must be retained in an RO group
        :type MinDelayEliminateReserve: int
        """
        self.ReadOnlyGroupId = None
        self.ReadOnlyGroupName = None
        self.ReplayLagEliminate = None
        self.ReplayLatencyEliminate = None
        self.MaxReplayLatency = None
        self.MaxReplayLag = None
        self.Rebalance = None
        self.MinDelayEliminateReserve = None


    def _deserialize(self, params):
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        self.ReadOnlyGroupName = params.get("ReadOnlyGroupName")
        self.ReplayLagEliminate = params.get("ReplayLagEliminate")
        self.ReplayLatencyEliminate = params.get("ReplayLatencyEliminate")
        self.MaxReplayLatency = params.get("MaxReplayLatency")
        self.MaxReplayLag = params.get("MaxReplayLag")
        self.Rebalance = params.get("Rebalance")
        self.MinDelayEliminateReserve = params.get("MinDelayEliminateReserve")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyReadOnlyGroupConfigResponse(AbstractModel):
    """ModifyReadOnlyGroupConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySwitchTimePeriodRequest(AbstractModel):
    """ModifySwitchTimePeriod request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: The ID of the instance waiting for a switch
        :type DBInstanceId: str
        :param SwitchTag: Valid value: `0` (switch immediately)
        :type SwitchTag: int
        """
        self.DBInstanceId = None
        self.SwitchTag = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.SwitchTag = params.get("SwitchTag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySwitchTimePeriodResponse(AbstractModel):
    """ModifySwitchTimePeriod response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class NetworkAccess(AbstractModel):
    """Network information. (This parameter structure has been deprecated. Please use `DBInstanceNetInfo` to query network information.)

    """

    def __init__(self):
        r"""
        :param ResourceId: Network resource ID, instance ID, or RO group ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ResourceId: str
        :param ResourceType: Resource type. Valid values: `1` (instance), `2` (RO group)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ResourceType: int
        :param VpcId: VPC ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type VpcId: str
        :param Vip: IPv4 address
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Vip: str
        :param Vip6: IPv6 address
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Vip6: str
        :param Vport: Access port
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Vport: int
        :param SubnetId: Subnet ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type SubnetId: str
        :param VpcStatus: Network status. Valid values: `1` (applying), `2` (in use), `3` (deleting), `4` (deleted)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type VpcStatus: int
        """
        self.ResourceId = None
        self.ResourceType = None
        self.VpcId = None
        self.Vip = None
        self.Vip6 = None
        self.Vport = None
        self.SubnetId = None
        self.VpcStatus = None


    def _deserialize(self, params):
        self.ResourceId = params.get("ResourceId")
        self.ResourceType = params.get("ResourceType")
        self.VpcId = params.get("VpcId")
        self.Vip = params.get("Vip")
        self.Vip6 = params.get("Vip6")
        self.Vport = params.get("Vport")
        self.SubnetId = params.get("SubnetId")
        self.VpcStatus = params.get("VpcStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NormalQueryItem(AbstractModel):
    """Information of one SlowQuery

    """

    def __init__(self):
        r"""
        :param UserName: Username
        :type UserName: str
        :param Calls: Number of calls
        :type Calls: int
        :param CallsGrids: Granularity
        :type CallsGrids: list of int
        :param CostTime: Total time consumed
        :type CostTime: float
        :param Rows: Number of affected rows
        :type Rows: int
        :param MinCostTime: Minimum time consumed
        :type MinCostTime: float
        :param MaxCostTime: Maximum time consumed
        :type MaxCostTime: float
        :param FirstTime: Time of the earliest slow SQL statement
        :type FirstTime: str
        :param LastTime: Time of the latest slow SQL statement
        :type LastTime: str
        :param SharedReadBlks: Shared memory blocks for reads
        :type SharedReadBlks: int
        :param SharedWriteBlks: Shared memory blocks for writes
        :type SharedWriteBlks: int
        :param ReadCostTime: Total IO read time
        :type ReadCostTime: int
        :param WriteCostTime: Total IO write time
        :type WriteCostTime: int
        :param DatabaseName: Database name
        :type DatabaseName: str
        :param NormalQuery: Slow SQL statement after desensitization
        :type NormalQuery: str
        """
        self.UserName = None
        self.Calls = None
        self.CallsGrids = None
        self.CostTime = None
        self.Rows = None
        self.MinCostTime = None
        self.MaxCostTime = None
        self.FirstTime = None
        self.LastTime = None
        self.SharedReadBlks = None
        self.SharedWriteBlks = None
        self.ReadCostTime = None
        self.WriteCostTime = None
        self.DatabaseName = None
        self.NormalQuery = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.Calls = params.get("Calls")
        self.CallsGrids = params.get("CallsGrids")
        self.CostTime = params.get("CostTime")
        self.Rows = params.get("Rows")
        self.MinCostTime = params.get("MinCostTime")
        self.MaxCostTime = params.get("MaxCostTime")
        self.FirstTime = params.get("FirstTime")
        self.LastTime = params.get("LastTime")
        self.SharedReadBlks = params.get("SharedReadBlks")
        self.SharedWriteBlks = params.get("SharedWriteBlks")
        self.ReadCostTime = params.get("ReadCostTime")
        self.WriteCostTime = params.get("WriteCostTime")
        self.DatabaseName = params.get("DatabaseName")
        self.NormalQuery = params.get("NormalQuery")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OpenDBExtranetAccessRequest(AbstractModel):
    """OpenDBExtranetAccess request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-hez4fh0v
        :type DBInstanceId: str
        :param IsIpv6: Whether to enable public network access over IPv6 address. Valid values: 1 (yes), 0 (no)
        :type IsIpv6: int
        """
        self.DBInstanceId = None
        self.IsIpv6 = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.IsIpv6 = params.get("IsIpv6")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OpenDBExtranetAccessResponse(AbstractModel):
    """OpenDBExtranetAccess response structure.

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


class OpenServerlessDBExtranetAccessRequest(AbstractModel):
    """OpenServerlessDBExtranetAccess request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Unique ID of an instance
        :type DBInstanceId: str
        :param DBInstanceName: Instance name
        :type DBInstanceName: str
        """
        self.DBInstanceId = None
        self.DBInstanceName = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.DBInstanceName = params.get("DBInstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OpenServerlessDBExtranetAccessResponse(AbstractModel):
    """OpenServerlessDBExtranetAccess response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ParamEntry(AbstractModel):
    """Parameters to be modified in batches

    """

    def __init__(self):
        r"""
        :param Name: Parameter name
        :type Name: str
        :param ExpectedValue: The new value to which the parameter will be modified. When this parameter is used as an input parameter, its value must be a string, such as `0.1` (decimal), `1000` (integer), and `replica` (enum).
        :type ExpectedValue: str
        """
        self.Name = None
        self.ExpectedValue = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.ExpectedValue = params.get("ExpectedValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParamInfo(AbstractModel):
    """Parameter details

    """

    def __init__(self):
        r"""
        :param ID: Parameter ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ID: int
        :param Name: Parameter name
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Name: str
        :param ParamValueType: Value type of the parameter. Valid values: `integer`, `real` (floating-point), `bool`, `enum`, `mutil_enum` (this type of parameter can be set to multiple enumerated values).
For an `integer` or `real` parameter, the `Min` field represents the minimum value and the `Max` field the maximum value. 
For a `bool` parameter, the valid values include `true` and `false`; 
For an `enum` or `mutil_enum` parameter, the `EnumValue` field represents the valid values.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ParamValueType: str
        :param Unit: Unit of the parameter value. If the parameter has no unit, this field will return null.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Unit: str
        :param DefaultValue: Default value of the parameter, which is returned as a string
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DefaultValue: str
        :param CurrentValue: Current value of the parameter, which is returned as a string
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type CurrentValue: str
        :param Max: The maximum value of the `integer` or `real` parameter
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Max: float
        :param EnumValue: Value range of the enum parameter
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type EnumValue: list of str
        :param Min: The minimum value of the `integer` or `real` parameter
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Min: float
        :param ParamDescriptionCH: Parameter description in Chinese
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ParamDescriptionCH: str
        :param ParamDescriptionEN: Parameter description in English
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ParamDescriptionEN: str
        :param NeedReboot: Whether to restart the instance for the modified parameter to take effect. Valid values: `true` (yes), `false` (no)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type NeedReboot: bool
        :param ClassificationCN: Parameter category in Chinese
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ClassificationCN: str
        :param ClassificationEN: Parameter category in English
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ClassificationEN: str
        :param SpecRelated: Whether the parameter is related to specifications. Valid values: `true` (yes), `false` (no)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type SpecRelated: bool
        :param Advanced: Whether it is a key parameter. Valid values: `true` (yes, and modifying it may affect instance performance), `false` (no)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Advanced: bool
        :param LastModifyTime: The last modified time of the parameter
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type LastModifyTime: str
        :param StandbyRelated: Primary-standby constraint. Valid values: `0` (no constraint), `1` (The parameter value of the standby server must be greater than that of the primary server), `2` (The parameter value of the primary server must be greater than that of the standby server.)
Note: This field may return null, indicating that no valid values can be obtained.
        :type StandbyRelated: int
        :param VersionRelationSet: Associated parameter version information, which refers to the detailed parameter information of the kernel version.
Note: This field may return null, indicating that no valid values can be obtained.
        :type VersionRelationSet: list of ParamVersionRelation
        :param SpecRelationSet: Associated parameter specification information, which refers to the detailed parameter information of the specifications.
Note: This field may return null, indicating that no valid values can be obtained.
        :type SpecRelationSet: list of ParamSpecRelation
        """
        self.ID = None
        self.Name = None
        self.ParamValueType = None
        self.Unit = None
        self.DefaultValue = None
        self.CurrentValue = None
        self.Max = None
        self.EnumValue = None
        self.Min = None
        self.ParamDescriptionCH = None
        self.ParamDescriptionEN = None
        self.NeedReboot = None
        self.ClassificationCN = None
        self.ClassificationEN = None
        self.SpecRelated = None
        self.Advanced = None
        self.LastModifyTime = None
        self.StandbyRelated = None
        self.VersionRelationSet = None
        self.SpecRelationSet = None


    def _deserialize(self, params):
        self.ID = params.get("ID")
        self.Name = params.get("Name")
        self.ParamValueType = params.get("ParamValueType")
        self.Unit = params.get("Unit")
        self.DefaultValue = params.get("DefaultValue")
        self.CurrentValue = params.get("CurrentValue")
        self.Max = params.get("Max")
        self.EnumValue = params.get("EnumValue")
        self.Min = params.get("Min")
        self.ParamDescriptionCH = params.get("ParamDescriptionCH")
        self.ParamDescriptionEN = params.get("ParamDescriptionEN")
        self.NeedReboot = params.get("NeedReboot")
        self.ClassificationCN = params.get("ClassificationCN")
        self.ClassificationEN = params.get("ClassificationEN")
        self.SpecRelated = params.get("SpecRelated")
        self.Advanced = params.get("Advanced")
        self.LastModifyTime = params.get("LastModifyTime")
        self.StandbyRelated = params.get("StandbyRelated")
        if params.get("VersionRelationSet") is not None:
            self.VersionRelationSet = []
            for item in params.get("VersionRelationSet"):
                obj = ParamVersionRelation()
                obj._deserialize(item)
                self.VersionRelationSet.append(obj)
        if params.get("SpecRelationSet") is not None:
            self.SpecRelationSet = []
            for item in params.get("SpecRelationSet"):
                obj = ParamSpecRelation()
                obj._deserialize(item)
                self.SpecRelationSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParamSpecRelation(AbstractModel):
    """Parameter information of each specification

    """

    def __init__(self):
        r"""
        :param Name: Parameter name
Note: This field may return null, indicating that no valid values can be obtained.
        :type Name: str
        :param Memory: The specification that corresponds to the parameter information
Note: This field may return null, indicating that no valid values can be obtained.
        :type Memory: str
        :param Value: The default parameter value under this specification
Note: This field may return null, indicating that no valid values can be obtained.
        :type Value: str
        :param Unit: Unit of the parameter value. If the parameter has no unit, this field will return null.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Unit: str
        :param Max: The maximum value of the `integer` or `real` parameter
Note: This field may return null, indicating that no valid values can be obtained.
        :type Max: float
        :param Min: The minimum value of the `integer` or `real` parameter
Note: This field may return null, indicating that no valid values can be obtained.
        :type Min: float
        :param EnumValue: Value range of the enum parameter
Note: This field may return null, indicating that no valid values can be obtained.
        :type EnumValue: list of str
        """
        self.Name = None
        self.Memory = None
        self.Value = None
        self.Unit = None
        self.Max = None
        self.Min = None
        self.EnumValue = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Memory = params.get("Memory")
        self.Value = params.get("Value")
        self.Unit = params.get("Unit")
        self.Max = params.get("Max")
        self.Min = params.get("Min")
        self.EnumValue = params.get("EnumValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParamVersionRelation(AbstractModel):
    """Parameter information of each version

    """

    def __init__(self):
        r"""
        :param Name: Parameter name
Note: This field may return null, indicating that no valid values can be obtained.
        :type Name: str
        :param DBKernelVersion: The kernel version that corresponds to the parameter information
Note: This field may return null, indicating that no valid values can be obtained.
        :type DBKernelVersion: str
        :param Value: Default parameter value under the kernel version and specification of the instance
Note: This field may return null, indicating that no valid values can be obtained.
        :type Value: str
        :param Unit: Unit of the parameter value. If the parameter has no unit, this field will return null.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Unit: str
        :param Max: The maximum value of the `integer` or `real` parameter
Note: This field may return null, indicating that no valid values can be obtained.
        :type Max: float
        :param Min: The minimum value of the `integer` or `real` parameter
Note: This field may return null, indicating that no valid values can be obtained.
        :type Min: float
        :param EnumValue: Value range of the enum parameter
Note: This field may return null, indicating that no valid values can be obtained.
        :type EnumValue: list of str
        """
        self.Name = None
        self.DBKernelVersion = None
        self.Value = None
        self.Unit = None
        self.Max = None
        self.Min = None
        self.EnumValue = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.DBKernelVersion = params.get("DBKernelVersion")
        self.Value = params.get("Value")
        self.Unit = params.get("Unit")
        self.Max = params.get("Max")
        self.Min = params.get("Min")
        self.EnumValue = params.get("EnumValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParameterTemplate(AbstractModel):
    """Basic information of a parameter template

    """

    def __init__(self):
        r"""
        :param TemplateId: Parameter template ID
        :type TemplateId: str
        :param TemplateName: Parameter template name
        :type TemplateName: str
        :param DBMajorVersion: Database version applicable to a parameter template
        :type DBMajorVersion: str
        :param DBEngine: Database engine applicable to a parameter template
        :type DBEngine: str
        :param TemplateDescription: Parameter template description
        :type TemplateDescription: str
        """
        self.TemplateId = None
        self.TemplateName = None
        self.DBMajorVersion = None
        self.DBEngine = None
        self.TemplateDescription = None


    def _deserialize(self, params):
        self.TemplateId = params.get("TemplateId")
        self.TemplateName = params.get("TemplateName")
        self.DBMajorVersion = params.get("DBMajorVersion")
        self.DBEngine = params.get("DBEngine")
        self.TemplateDescription = params.get("TemplateDescription")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PgDeal(AbstractModel):
    """Order details

    """

    def __init__(self):
        r"""
        :param DealName: Order name
        :type DealName: str
        :param OwnerUin: User
        :type OwnerUin: str
        :param Count: Number of instances involved in order
        :type Count: int
        :param PayMode: Billing mode. 0: pay-as-you-go
        :type PayMode: int
        :param FlowId: Async task flow ID
        :type FlowId: int
        :param DBInstanceIdSet: Instance ID array
        :type DBInstanceIdSet: list of str
        """
        self.DealName = None
        self.OwnerUin = None
        self.Count = None
        self.PayMode = None
        self.FlowId = None
        self.DBInstanceIdSet = None


    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.OwnerUin = params.get("OwnerUin")
        self.Count = params.get("Count")
        self.PayMode = params.get("PayMode")
        self.FlowId = params.get("FlowId")
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PolicyRule(AbstractModel):
    """Rule information for security group

    """

    def __init__(self):
        r"""
        :param Action: Policy, Valid values: `ACCEPT`, `DROP`.
        :type Action: str
        :param CidrIp: Source or destination IP or IP range, such as 172.16.0.0/12.
        :type CidrIp: str
        :param PortRange: Port
        :type PortRange: str
        :param IpProtocol: Network protocol. UDP and TCP are supported.
        :type IpProtocol: str
        :param Description: The rule description
        :type Description: str
        """
        self.Action = None
        self.CidrIp = None
        self.PortRange = None
        self.IpProtocol = None
        self.Description = None


    def _deserialize(self, params):
        self.Action = params.get("Action")
        self.CidrIp = params.get("CidrIp")
        self.PortRange = params.get("PortRange")
        self.IpProtocol = params.get("IpProtocol")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RawSlowQuery(AbstractModel):
    """The list of slow query details returned by the `DescribeSlowQueryList` API

    """

    def __init__(self):
        r"""
        :param RawQuery: Slow query statement
        :type RawQuery: str
        :param DatabaseName: The database queried by the slow query statement
        :type DatabaseName: str
        :param Duration: The execution time of the slow query statement
        :type Duration: float
        :param ClientAddr: The client that executes the slow query statement
        :type ClientAddr: str
        :param UserName: The name of the user who executes the slow query statement
        :type UserName: str
        :param SessionStartTime: The time when the slow query statement starts to execute
        :type SessionStartTime: str
        """
        self.RawQuery = None
        self.DatabaseName = None
        self.Duration = None
        self.ClientAddr = None
        self.UserName = None
        self.SessionStartTime = None


    def _deserialize(self, params):
        self.RawQuery = params.get("RawQuery")
        self.DatabaseName = params.get("DatabaseName")
        self.Duration = params.get("Duration")
        self.ClientAddr = params.get("ClientAddr")
        self.UserName = params.get("UserName")
        self.SessionStartTime = params.get("SessionStartTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReadOnlyGroup(AbstractModel):
    """RO group information

    """

    def __init__(self):
        r"""
        :param ReadOnlyGroupId: RO group identifier
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ReadOnlyGroupId: str
        :param ReadOnlyGroupName: RO group name
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ReadOnlyGroupName: str
        :param ProjectId: Project ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ProjectId: int
        :param MasterDBInstanceId: Primary instance ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type MasterDBInstanceId: str
        :param MinDelayEliminateReserve: The minimum number of read-only replicas that must be retained in an RO group
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type MinDelayEliminateReserve: int
        :param MaxReplayLatency: Delayed log size threshold
        :type MaxReplayLatency: int
        :param ReplayLatencyEliminate: Whether to remove a read-only replica from an RO group if the sync log size difference between the read-only replica and the primary instance exceeds the threshold. Valid values: `0` (no), `1` (yes).
        :type ReplayLatencyEliminate: int
        :param MaxReplayLag: Delay threshold
        :type MaxReplayLag: float
        :param ReplayLagEliminate: Whether to remove a read-only replica from an RO group if the delay between the read-only replica and the primary instance exceeds the threshold. Valid values: `0` (no), `1` (yes).
        :type ReplayLagEliminate: int
        :param VpcId: VPC ID
        :type VpcId: str
        :param SubnetId: Subnet ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type SubnetId: str
        :param Region: Region ID
        :type Region: str
        :param Zone: Availability zone ID
        :type Zone: str
        :param Status: Status
        :type Status: str
        :param ReadOnlyDBInstanceList: Instance details
        :type ReadOnlyDBInstanceList: list of DBInstance
        :param Rebalance: Whether to enable automatic load balancing
        :type Rebalance: int
        :param DBInstanceNetInfo: Network information
        :type DBInstanceNetInfo: list of DBInstanceNetInfo
        :param NetworkAccessList: Network access list of the RO group (this field has been deprecated)
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type NetworkAccessList: list of NetworkAccess
        """
        self.ReadOnlyGroupId = None
        self.ReadOnlyGroupName = None
        self.ProjectId = None
        self.MasterDBInstanceId = None
        self.MinDelayEliminateReserve = None
        self.MaxReplayLatency = None
        self.ReplayLatencyEliminate = None
        self.MaxReplayLag = None
        self.ReplayLagEliminate = None
        self.VpcId = None
        self.SubnetId = None
        self.Region = None
        self.Zone = None
        self.Status = None
        self.ReadOnlyDBInstanceList = None
        self.Rebalance = None
        self.DBInstanceNetInfo = None
        self.NetworkAccessList = None


    def _deserialize(self, params):
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        self.ReadOnlyGroupName = params.get("ReadOnlyGroupName")
        self.ProjectId = params.get("ProjectId")
        self.MasterDBInstanceId = params.get("MasterDBInstanceId")
        self.MinDelayEliminateReserve = params.get("MinDelayEliminateReserve")
        self.MaxReplayLatency = params.get("MaxReplayLatency")
        self.ReplayLatencyEliminate = params.get("ReplayLatencyEliminate")
        self.MaxReplayLag = params.get("MaxReplayLag")
        self.ReplayLagEliminate = params.get("ReplayLagEliminate")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.Status = params.get("Status")
        if params.get("ReadOnlyDBInstanceList") is not None:
            self.ReadOnlyDBInstanceList = []
            for item in params.get("ReadOnlyDBInstanceList"):
                obj = DBInstance()
                obj._deserialize(item)
                self.ReadOnlyDBInstanceList.append(obj)
        self.Rebalance = params.get("Rebalance")
        if params.get("DBInstanceNetInfo") is not None:
            self.DBInstanceNetInfo = []
            for item in params.get("DBInstanceNetInfo"):
                obj = DBInstanceNetInfo()
                obj._deserialize(item)
                self.DBInstanceNetInfo.append(obj)
        if params.get("NetworkAccessList") is not None:
            self.NetworkAccessList = []
            for item in params.get("NetworkAccessList"):
                obj = NetworkAccess()
                obj._deserialize(item)
                self.NetworkAccessList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RebalanceReadOnlyGroupRequest(AbstractModel):
    """RebalanceReadOnlyGroup request structure.

    """

    def __init__(self):
        r"""
        :param ReadOnlyGroupId: RO group ID
        :type ReadOnlyGroupId: str
        """
        self.ReadOnlyGroupId = None


    def _deserialize(self, params):
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RebalanceReadOnlyGroupResponse(AbstractModel):
    """RebalanceReadOnlyGroup response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RegionInfo(AbstractModel):
    """Region information such as number and status

    """

    def __init__(self):
        r"""
        :param Region: Region abbreviation
        :type Region: str
        :param RegionName: Region name
        :type RegionName: str
        :param RegionId: Region number
        :type RegionId: int
        :param RegionState: Availability status. UNAVAILABLE: unavailable, AVAILABLE: available
        :type RegionState: str
        :param SupportInternational: Whether the resource can be purchased in this region. Valid values: `0` (no), `1` (yes).
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type SupportInternational: int
        """
        self.Region = None
        self.RegionName = None
        self.RegionId = None
        self.RegionState = None
        self.SupportInternational = None


    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionName = params.get("RegionName")
        self.RegionId = params.get("RegionId")
        self.RegionState = params.get("RegionState")
        self.SupportInternational = params.get("SupportInternational")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RemoveDBInstanceFromReadOnlyGroupRequest(AbstractModel):
    """RemoveDBInstanceFromReadOnlyGroup request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param ReadOnlyGroupId: RO group ID
        :type ReadOnlyGroupId: str
        """
        self.DBInstanceId = None
        self.ReadOnlyGroupId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.ReadOnlyGroupId = params.get("ReadOnlyGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RemoveDBInstanceFromReadOnlyGroupResponse(AbstractModel):
    """RemoveDBInstanceFromReadOnlyGroup response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class RenewInstanceRequest(AbstractModel):
    """RenewInstance request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of `postgres-6fego161`
        :type DBInstanceId: str
        :param Period: Renewal duration in months
        :type Period: int
        :param AutoVoucher: Whether to automatically use vouchers. 1: yes, 0: no. Default value: 0
        :type AutoVoucher: int
        :param VoucherIds: Voucher ID list (only one voucher can be specified currently)
        :type VoucherIds: list of str
        """
        self.DBInstanceId = None
        self.Period = None
        self.AutoVoucher = None
        self.VoucherIds = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.Period = params.get("Period")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewInstanceResponse(AbstractModel):
    """RenewInstance response structure.

    """

    def __init__(self):
        r"""
        :param DealName: Order name
        :type DealName: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.RequestId = params.get("RequestId")


class ResetAccountPasswordRequest(AbstractModel):
    """ResetAccountPassword request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-4wdeb0zv
        :type DBInstanceId: str
        :param UserName: Instance account name
        :type UserName: str
        :param Password: New password corresponding to `UserName` account
        :type Password: str
        """
        self.DBInstanceId = None
        self.UserName = None
        self.Password = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.UserName = params.get("UserName")
        self.Password = params.get("Password")
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


class RestartDBInstanceRequest(AbstractModel):
    """RestartDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID in the format of postgres-6r233v55
        :type DBInstanceId: str
        """
        self.DBInstanceId = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RestartDBInstanceResponse(AbstractModel):
    """RestartDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async flow ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class SecurityGroup(AbstractModel):
    """Security group information

    """

    def __init__(self):
        r"""
        :param ProjectId: Project ID
        :type ProjectId: int
        :param CreateTime: Creation time
        :type CreateTime: str
        :param Inbound: Inbound rule
        :type Inbound: list of PolicyRule
        :param Outbound: Outbound rule
        :type Outbound: list of PolicyRule
        :param SecurityGroupId: Security group ID
        :type SecurityGroupId: str
        :param SecurityGroupName: Security group name
        :type SecurityGroupName: str
        :param SecurityGroupDescription: Security group remarks
        :type SecurityGroupDescription: str
        """
        self.ProjectId = None
        self.CreateTime = None
        self.Inbound = None
        self.Outbound = None
        self.SecurityGroupId = None
        self.SecurityGroupName = None
        self.SecurityGroupDescription = None


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
        self.SecurityGroupDescription = params.get("SecurityGroupDescription")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServerlessDBAccount(AbstractModel):
    """PostgreSQL for Serverless instance account description

    """

    def __init__(self):
        r"""
        :param DBUser: Username
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBUser: str
        :param DBPassword: Password
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBPassword: str
        :param DBConnLimit: The maximum number of connections
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBConnLimit: int
        """
        self.DBUser = None
        self.DBPassword = None
        self.DBConnLimit = None


    def _deserialize(self, params):
        self.DBUser = params.get("DBUser")
        self.DBPassword = params.get("DBPassword")
        self.DBConnLimit = params.get("DBConnLimit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServerlessDBInstance(AbstractModel):
    """PostgreSQL for Serverless instance description

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID, which is the unique identifier
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBInstanceId: str
        :param DBInstanceName: Instance name
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBInstanceName: str
        :param DBInstanceStatus: Instance status
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBInstanceStatus: str
        :param Region: Region
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Region: str
        :param Zone: Availability zone
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Zone: str
        :param ProjectId: Project ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ProjectId: int
        :param VpcId: VPC ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type VpcId: str
        :param SubnetId: Subnet ID
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type SubnetId: str
        :param DBCharset: Character set
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBCharset: str
        :param DBVersion: Database version
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBVersion: str
        :param CreateTime: Creation time
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type CreateTime: str
        :param DBInstanceNetInfo: Instance network information
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBInstanceNetInfo: list of ServerlessDBInstanceNetInfo
        :param DBAccountSet: Instance account information
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBAccountSet: list of ServerlessDBAccount
        :param DBDatabaseList: Information of the databases in an instance
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBDatabaseList: list of str
        :param TagList: The array of tags bound to an instance
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type TagList: list of Tag
        :param DBKernelVersion: Database kernel version
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBKernelVersion: str
        :param DBMajorVersion: Database major version number
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type DBMajorVersion: str
        """
        self.DBInstanceId = None
        self.DBInstanceName = None
        self.DBInstanceStatus = None
        self.Region = None
        self.Zone = None
        self.ProjectId = None
        self.VpcId = None
        self.SubnetId = None
        self.DBCharset = None
        self.DBVersion = None
        self.CreateTime = None
        self.DBInstanceNetInfo = None
        self.DBAccountSet = None
        self.DBDatabaseList = None
        self.TagList = None
        self.DBKernelVersion = None
        self.DBMajorVersion = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.DBInstanceName = params.get("DBInstanceName")
        self.DBInstanceStatus = params.get("DBInstanceStatus")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.ProjectId = params.get("ProjectId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.DBCharset = params.get("DBCharset")
        self.DBVersion = params.get("DBVersion")
        self.CreateTime = params.get("CreateTime")
        if params.get("DBInstanceNetInfo") is not None:
            self.DBInstanceNetInfo = []
            for item in params.get("DBInstanceNetInfo"):
                obj = ServerlessDBInstanceNetInfo()
                obj._deserialize(item)
                self.DBInstanceNetInfo.append(obj)
        if params.get("DBAccountSet") is not None:
            self.DBAccountSet = []
            for item in params.get("DBAccountSet"):
                obj = ServerlessDBAccount()
                obj._deserialize(item)
                self.DBAccountSet.append(obj)
        self.DBDatabaseList = params.get("DBDatabaseList")
        if params.get("TagList") is not None:
            self.TagList = []
            for item in params.get("TagList"):
                obj = Tag()
                obj._deserialize(item)
                self.TagList.append(obj)
        self.DBKernelVersion = params.get("DBKernelVersion")
        self.DBMajorVersion = params.get("DBMajorVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServerlessDBInstanceNetInfo(AbstractModel):
    """PostgreSQL for Serverless instance network description

    """

    def __init__(self):
        r"""
        :param Address: Address
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Address: str
        :param Ip: IP address
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Ip: str
        :param Port: Port number
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Port: int
        :param Status: Status
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Status: str
        :param NetType: Network type
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type NetType: str
        """
        self.Address = None
        self.Ip = None
        self.Port = None
        self.Status = None
        self.NetType = None


    def _deserialize(self, params):
        self.Address = params.get("Address")
        self.Ip = params.get("Ip")
        self.Port = params.get("Port")
        self.Status = params.get("Status")
        self.NetType = params.get("NetType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetAutoRenewFlagRequest(AbstractModel):
    """SetAutoRenewFlag request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceIdSet: List of instance IDs. Note that currently you cannot manipulate multiple instances at the same time. Only one instance ID can be passed in here.
        :type DBInstanceIdSet: list of str
        :param AutoRenewFlag: Renewal flag. 0: normal renewal, 1: auto-renewal, 2: no renewal upon expiration
        :type AutoRenewFlag: int
        """
        self.DBInstanceIdSet = None
        self.AutoRenewFlag = None


    def _deserialize(self, params):
        self.DBInstanceIdSet = params.get("DBInstanceIdSet")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetAutoRenewFlagResponse(AbstractModel):
    """SetAutoRenewFlag response structure.

    """

    def __init__(self):
        r"""
        :param Count: Number of successfully set instances
        :type Count: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Count = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.RequestId = params.get("RequestId")


class SlowlogDetail(AbstractModel):
    """Slow query details

    """

    def __init__(self):
        r"""
        :param TotalTime: Total time consumed
        :type TotalTime: float
        :param TotalCalls: Total number of calls
        :type TotalCalls: int
        :param NormalQueries: List of slow SQL statements after desensitization
        :type NormalQueries: list of NormalQueryItem
        """
        self.TotalTime = None
        self.TotalCalls = None
        self.NormalQueries = None


    def _deserialize(self, params):
        self.TotalTime = params.get("TotalTime")
        self.TotalCalls = params.get("TotalCalls")
        if params.get("NormalQueries") is not None:
            self.NormalQueries = []
            for item in params.get("NormalQueries"):
                obj = NormalQueryItem()
                obj._deserialize(item)
                self.NormalQueries.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SpecInfo(AbstractModel):
    """Purchasable specification details in an AZ in a region.

    """

    def __init__(self):
        r"""
        :param Region: Region abbreviation, which corresponds to the `Region` field of `RegionSet`
        :type Region: str
        :param Zone: AZ abbreviate, which corresponds to the `Zone` field of `ZoneSet`
        :type Zone: str
        :param SpecItemInfoList: Specification details list
        :type SpecItemInfoList: list of SpecItemInfo
        :param SupportKMSRegions: Regions where KMS is supported
Note: This field may return `null`, indicating that no valid value was found.
        :type SupportKMSRegions: list of str
        """
        self.Region = None
        self.Zone = None
        self.SpecItemInfoList = None
        self.SupportKMSRegions = None


    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        if params.get("SpecItemInfoList") is not None:
            self.SpecItemInfoList = []
            for item in params.get("SpecItemInfoList"):
                obj = SpecItemInfo()
                obj._deserialize(item)
                self.SpecItemInfoList.append(obj)
        self.SupportKMSRegions = params.get("SupportKMSRegions")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SpecItemInfo(AbstractModel):
    """Specification description

    """

    def __init__(self):
        r"""
        :param SpecCode: Specification ID
        :type SpecCode: str
        :param Version: PostgerSQL version number
        :type Version: str
        :param VersionName: Full version name corresponding to kernel number
        :type VersionName: str
        :param Cpu: Number of CPU cores
        :type Cpu: int
        :param Memory: Memory size in MB
        :type Memory: int
        :param MaxStorage: Maximum storage capacity in GB supported by this specification
        :type MaxStorage: int
        :param MinStorage: Minimum storage capacity in GB supported by this specification
        :type MinStorage: int
        :param Qps: Estimated QPS for this specification
        :type Qps: int
        :param Pid: (Disused)
        :type Pid: int
        :param Type: Machine type
        :type Type: str
        :param MajorVersion: PostgreSQL major version number
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type MajorVersion: str
        :param KernelVersion: PostgreSQL kernel version number
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type KernelVersion: str
        :param IsSupportTDE: Whether TDE data encryption is supported. Valid values: 0 (no), 1 (yes)
Note: This field may return `null`, indicating that no valid value was found.
        :type IsSupportTDE: int
        """
        self.SpecCode = None
        self.Version = None
        self.VersionName = None
        self.Cpu = None
        self.Memory = None
        self.MaxStorage = None
        self.MinStorage = None
        self.Qps = None
        self.Pid = None
        self.Type = None
        self.MajorVersion = None
        self.KernelVersion = None
        self.IsSupportTDE = None


    def _deserialize(self, params):
        self.SpecCode = params.get("SpecCode")
        self.Version = params.get("Version")
        self.VersionName = params.get("VersionName")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.MaxStorage = params.get("MaxStorage")
        self.MinStorage = params.get("MinStorage")
        self.Qps = params.get("Qps")
        self.Pid = params.get("Pid")
        self.Type = params.get("Type")
        self.MajorVersion = params.get("MajorVersion")
        self.KernelVersion = params.get("KernelVersion")
        self.IsSupportTDE = params.get("IsSupportTDE")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Tag(AbstractModel):
    """The information of tags associated with instances, including `TagKey` and `TagValue`

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
        


class UpgradeDBInstanceKernelVersionRequest(AbstractModel):
    """UpgradeDBInstanceKernelVersion request structure.

    """

    def __init__(self):
        r"""
        :param DBInstanceId: Instance ID
        :type DBInstanceId: str
        :param TargetDBKernelVersion: Target kernel version, which can be obtained in the `AvailableUpgradeTarget` field returned by the `DescribeDBVersions` API.
        :type TargetDBKernelVersion: str
        :param SwitchTag: Switch time after the kernel version upgrade. Valid values:
`0` (default value): Switch now.
`1`: Switch at the specified time.
`2`: Switch in the maintenance time.
        :type SwitchTag: int
        :param SwitchStartTime: Switch start time in the format of `HH:MM:SS`, such as 01:00:00. When `SwitchTag` is `0` or `2`, this parameter is invalid.
        :type SwitchStartTime: str
        :param SwitchEndTime: Switch end time in the format of `HH:MM:SS`, such as 01:30:00. When `SwitchTag` is `0` or `2`, this parameter is invalid. The difference between `SwitchStartTime` and `SwitchEndTime` cannot be less than 30 minutes.
        :type SwitchEndTime: str
        :param DryRun: Whether to perform a precheck on the current operation of upgrading the instance kernel version. Valid values:
`true`: Performs a precheck without upgrading the kernel version. Check items include request parameters, kernel version compatibility, and instance parameters.
`false` (default value): Sends a normal request and upgrades the kernel version directly after the check is passed.
        :type DryRun: bool
        """
        self.DBInstanceId = None
        self.TargetDBKernelVersion = None
        self.SwitchTag = None
        self.SwitchStartTime = None
        self.SwitchEndTime = None
        self.DryRun = None


    def _deserialize(self, params):
        self.DBInstanceId = params.get("DBInstanceId")
        self.TargetDBKernelVersion = params.get("TargetDBKernelVersion")
        self.SwitchTag = params.get("SwitchTag")
        self.SwitchStartTime = params.get("SwitchStartTime")
        self.SwitchEndTime = params.get("SwitchEndTime")
        self.DryRun = params.get("DryRun")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpgradeDBInstanceKernelVersionResponse(AbstractModel):
    """UpgradeDBInstanceKernelVersion response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpgradeDBInstanceRequest(AbstractModel):
    """UpgradeDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param Memory: Instance memory size in GB after upgrade
        :type Memory: int
        :param Storage: Instance disk size in GB after upgrade
        :type Storage: int
        :param DBInstanceId: Instance ID in the format of postgres-lnp6j617
        :type DBInstanceId: str
        :param AutoVoucher: Whether to automatically use vouchers. 1: yes, 0: no. Default value: no
        :type AutoVoucher: int
        :param VoucherIds: Voucher ID list (only one voucher can be specified currently)
        :type VoucherIds: list of str
        :param ActivityId: Activity ID
        :type ActivityId: int
        :param SwitchTag: Switch time after instance configurations are modified. Valid values: `0` (switch immediately), `1` (switch at specified time). Default value: `0`
        :type SwitchTag: int
        :param SwitchStartTime: The earliest time to start a switch
        :type SwitchStartTime: str
        :param SwitchEndTime: The latest time to start a switch
        :type SwitchEndTime: str
        """
        self.Memory = None
        self.Storage = None
        self.DBInstanceId = None
        self.AutoVoucher = None
        self.VoucherIds = None
        self.ActivityId = None
        self.SwitchTag = None
        self.SwitchStartTime = None
        self.SwitchEndTime = None


    def _deserialize(self, params):
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.DBInstanceId = params.get("DBInstanceId")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        self.ActivityId = params.get("ActivityId")
        self.SwitchTag = params.get("SwitchTag")
        self.SwitchStartTime = params.get("SwitchStartTime")
        self.SwitchEndTime = params.get("SwitchEndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpgradeDBInstanceResponse(AbstractModel):
    """UpgradeDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param DealName: Transaction name.
        :type DealName: str
        :param BillId: Bill ID of frozen fees
        :type BillId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealName = None
        self.BillId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.BillId = params.get("BillId")
        self.RequestId = params.get("RequestId")


class Version(AbstractModel):
    """Database version information

    """

    def __init__(self):
        r"""
        :param DBEngine: Database engines. Valid values:
1. `postgresql` (TencentDB for PostgreSQL)
2. `mssql_compatible` (MSSQL compatible-TencentDB for PostgreSQL)
        :type DBEngine: str
        :param DBVersion: Database version, such as 12.4.
        :type DBVersion: str
        :param DBMajorVersion: Database major version, such as 12.
        :type DBMajorVersion: str
        :param DBKernelVersion: Database kernel version, such as v12.4_r1.3.
        :type DBKernelVersion: str
        :param SupportedFeatureNames: List of features supported by the database kernel, such as:
TDE: Supports data encryption.
        :type SupportedFeatureNames: list of str
        :param Status: Database version status. Valid values:
`AVAILABLE`.
`DEPRECATED`.
        :type Status: str
        :param AvailableUpgradeTarget: List of versions to which this database version (`DBKernelVersion`) can be upgraded.
        :type AvailableUpgradeTarget: list of str
        """
        self.DBEngine = None
        self.DBVersion = None
        self.DBMajorVersion = None
        self.DBKernelVersion = None
        self.SupportedFeatureNames = None
        self.Status = None
        self.AvailableUpgradeTarget = None


    def _deserialize(self, params):
        self.DBEngine = params.get("DBEngine")
        self.DBVersion = params.get("DBVersion")
        self.DBMajorVersion = params.get("DBMajorVersion")
        self.DBKernelVersion = params.get("DBKernelVersion")
        self.SupportedFeatureNames = params.get("SupportedFeatureNames")
        self.Status = params.get("Status")
        self.AvailableUpgradeTarget = params.get("AvailableUpgradeTarget")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Xlog(AbstractModel):
    """Database Xlog information

    """

    def __init__(self):
        r"""
        :param Id: Unique backup file ID
        :type Id: int
        :param StartTime: File generation start time
        :type StartTime: str
        :param EndTime: File generation end time
        :type EndTime: str
        :param InternalAddr: Download address on private network
        :type InternalAddr: str
        :param ExternalAddr: Download address on public network
        :type ExternalAddr: str
        :param Size: Backup file size
        :type Size: int
        """
        self.Id = None
        self.StartTime = None
        self.EndTime = None
        self.InternalAddr = None
        self.ExternalAddr = None
        self.Size = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.InternalAddr = params.get("InternalAddr")
        self.ExternalAddr = params.get("ExternalAddr")
        self.Size = params.get("Size")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ZoneInfo(AbstractModel):
    """AZ information such as number and status

    """

    def __init__(self):
        r"""
        :param Zone: AZ abbreviation
        :type Zone: str
        :param ZoneName: AZ name
        :type ZoneName: str
        :param ZoneId: AZ number
        :type ZoneId: int
        :param ZoneState: Availability status. Valid values:
`UNAVAILABLE`.
`AVAILABLE`.
`SELLOUT`.
`SUPPORTMODIFYONLY` (supports configuration adjustment).
        :type ZoneState: str
        :param ZoneSupportIpv6: Whether the AZ supports IPv6 address access
        :type ZoneSupportIpv6: int
        :param StandbyZoneSet: AZs that can be used as standby when this AZ is primary
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type StandbyZoneSet: list of str
        """
        self.Zone = None
        self.ZoneName = None
        self.ZoneId = None
        self.ZoneState = None
        self.ZoneSupportIpv6 = None
        self.StandbyZoneSet = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneName = params.get("ZoneName")
        self.ZoneId = params.get("ZoneId")
        self.ZoneState = params.get("ZoneState")
        self.ZoneSupportIpv6 = params.get("ZoneSupportIpv6")
        self.StandbyZoneSet = params.get("StandbyZoneSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        