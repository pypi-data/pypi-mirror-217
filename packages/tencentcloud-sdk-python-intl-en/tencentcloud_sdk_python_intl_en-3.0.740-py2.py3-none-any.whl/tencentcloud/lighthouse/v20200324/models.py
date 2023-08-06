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


class ApplyInstanceSnapshotRequest(AbstractModel):
    """ApplyInstanceSnapshot request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param SnapshotId: Snapshot ID.
        :type SnapshotId: str
        """
        self.InstanceId = None
        self.SnapshotId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SnapshotId = params.get("SnapshotId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ApplyInstanceSnapshotResponse(AbstractModel):
    """ApplyInstanceSnapshot response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AssociateInstancesKeyPairsRequest(AbstractModel):
    """AssociateInstancesKeyPairs request structure.

    """

    def __init__(self):
        r"""
        :param KeyIds: Key pair ID list. Each request can contain up to 100 key pairs.
        :type KeyIds: list of str
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
        :type InstanceIds: list of str
        """
        self.KeyIds = None
        self.InstanceIds = None


    def _deserialize(self, params):
        self.KeyIds = params.get("KeyIds")
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociateInstancesKeyPairsResponse(AbstractModel):
    """AssociateInstancesKeyPairs response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachCcnRequest(AbstractModel):
    """AttachCcn request structure.

    """

    def __init__(self):
        r"""
        :param CcnId: CCN instance ID.
        :type CcnId: str
        """
        self.CcnId = None


    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AttachCcnResponse(AbstractModel):
    """AttachCcn response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachDetail(AbstractModel):
    """Attachment information

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param AttachedDiskCount: Number of elastic cloud disks attached to the instance
        :type AttachedDiskCount: int
        :param MaxAttachCount: Upper limit of attached elastic cloud disks
        :type MaxAttachCount: int
        """
        self.InstanceId = None
        self.AttachedDiskCount = None
        self.MaxAttachCount = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.AttachedDiskCount = params.get("AttachedDiskCount")
        self.MaxAttachCount = params.get("MaxAttachCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AttachDisksRequest(AbstractModel):
    """AttachDisks request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param RenewFlag: Whether Auto-Renewal is enabled 
        :type RenewFlag: str
        """
        self.DiskIds = None
        self.InstanceId = None
        self.RenewFlag = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.InstanceId = params.get("InstanceId")
        self.RenewFlag = params.get("RenewFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AttachDisksResponse(AbstractModel):
    """AttachDisks response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Blueprint(AbstractModel):
    """Image information.

    """

    def __init__(self):
        r"""
        :param BlueprintId: Image ID, which is the unique identifier of `Blueprint`.
        :type BlueprintId: str
        :param DisplayTitle: Image title to be displayed.
        :type DisplayTitle: str
        :param DisplayVersion: Image version to be displayed.
        :type DisplayVersion: str
        :param Description: Image description information.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type Description: str
        :param OsName: OS name.
        :type OsName: str
        :param Platform: OS type.
        :type Platform: str
        :param PlatformType: OS type, such as LINUX_UNIX and WINDOWS.
        :type PlatformType: str
        :param BlueprintType: Image type, such as APP_OS, PURE_OS, and PRIVATE.
        :type BlueprintType: str
        :param ImageUrl: Image picture URL.
        :type ImageUrl: str
        :param RequiredSystemDiskSize: System disk size required by image in GB.
        :type RequiredSystemDiskSize: int
        :param BlueprintState: Image status.
        :type BlueprintState: str
        :param CreatedTime: Creation time according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: this field may return null, indicating that no valid values can be obtained.
        :type CreatedTime: str
        :param BlueprintName: Image name.
        :type BlueprintName: str
        :param SupportAutomationTools: Whether the image supports automation tools.
        :type SupportAutomationTools: bool
        :param RequiredMemorySize: Memory size required by image in GB.
        :type RequiredMemorySize: int
        :param ImageId: ID of the Lighthouse image shared from a CVM image
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ImageId: str
        :param CommunityUrl: URL of official website of the open-source project
        :type CommunityUrl: str
        :param GuideUrl: Guide documentation URL
        :type GuideUrl: str
        :param SceneIdSet: Array of IDs of scenes associated with an image
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type SceneIdSet: list of str
        :param DockerVersion: Docker version.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type DockerVersion: str
        """
        self.BlueprintId = None
        self.DisplayTitle = None
        self.DisplayVersion = None
        self.Description = None
        self.OsName = None
        self.Platform = None
        self.PlatformType = None
        self.BlueprintType = None
        self.ImageUrl = None
        self.RequiredSystemDiskSize = None
        self.BlueprintState = None
        self.CreatedTime = None
        self.BlueprintName = None
        self.SupportAutomationTools = None
        self.RequiredMemorySize = None
        self.ImageId = None
        self.CommunityUrl = None
        self.GuideUrl = None
        self.SceneIdSet = None
        self.DockerVersion = None


    def _deserialize(self, params):
        self.BlueprintId = params.get("BlueprintId")
        self.DisplayTitle = params.get("DisplayTitle")
        self.DisplayVersion = params.get("DisplayVersion")
        self.Description = params.get("Description")
        self.OsName = params.get("OsName")
        self.Platform = params.get("Platform")
        self.PlatformType = params.get("PlatformType")
        self.BlueprintType = params.get("BlueprintType")
        self.ImageUrl = params.get("ImageUrl")
        self.RequiredSystemDiskSize = params.get("RequiredSystemDiskSize")
        self.BlueprintState = params.get("BlueprintState")
        self.CreatedTime = params.get("CreatedTime")
        self.BlueprintName = params.get("BlueprintName")
        self.SupportAutomationTools = params.get("SupportAutomationTools")
        self.RequiredMemorySize = params.get("RequiredMemorySize")
        self.ImageId = params.get("ImageId")
        self.CommunityUrl = params.get("CommunityUrl")
        self.GuideUrl = params.get("GuideUrl")
        self.SceneIdSet = params.get("SceneIdSet")
        self.DockerVersion = params.get("DockerVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BlueprintInstance(AbstractModel):
    """Image instance information.

    """

    def __init__(self):
        r"""
        :param Blueprint: Image information.
        :type Blueprint: :class:`tencentcloud.lighthouse.v20200324.models.Blueprint`
        :param SoftwareSet: Software list.
        :type SoftwareSet: list of Software
        :param InstanceId: Instance ID.
        :type InstanceId: str
        """
        self.Blueprint = None
        self.SoftwareSet = None
        self.InstanceId = None


    def _deserialize(self, params):
        if params.get("Blueprint") is not None:
            self.Blueprint = Blueprint()
            self.Blueprint._deserialize(params.get("Blueprint"))
        if params.get("SoftwareSet") is not None:
            self.SoftwareSet = []
            for item in params.get("SoftwareSet"):
                obj = Software()
                obj._deserialize(item)
                self.SoftwareSet.append(obj)
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BlueprintPrice(AbstractModel):
    """BlueprintPrice	Custom image price parameter.

    """

    def __init__(self):
        r"""
        :param OriginalBlueprintPrice: Original image unit price in USD.
        :type OriginalBlueprintPrice: float
        :param OriginalPrice: Original image total price in USD.
        :type OriginalPrice: float
        :param Discount: Discount.
        :type Discount: int
        :param DiscountPrice: Discounted image total price in USD.
        :type DiscountPrice: float
        """
        self.OriginalBlueprintPrice = None
        self.OriginalPrice = None
        self.Discount = None
        self.DiscountPrice = None


    def _deserialize(self, params):
        self.OriginalBlueprintPrice = params.get("OriginalBlueprintPrice")
        self.OriginalPrice = params.get("OriginalPrice")
        self.Discount = params.get("Discount")
        self.DiscountPrice = params.get("DiscountPrice")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Bundle(AbstractModel):
    """Package information.

    """

    def __init__(self):
        r"""
        :param BundleId: Package ID.
        :type BundleId: str
        :param Memory: Memory size in GB.
        :type Memory: int
        :param SystemDiskType: System disk type.
Valid values: 
<li> LOCAL_BASIC: local disk</li><li> LOCAL_SSD: local SSD disk</li><li> CLOUD_BASIC: HDD cloud disk</li><li> CLOUD_SSD: SSD cloud disk</li><li> CLOUD_PREMIUM: Premium Cloud Storage</li>
        :type SystemDiskType: str
        :param SystemDiskSize: System disk size.
        :type SystemDiskSize: int
        :param MonthlyTraffic: Monthly network traffic in Gb.
        :type MonthlyTraffic: int
        :param SupportLinuxUnixPlatform: Whether Linux/Unix is supported.
        :type SupportLinuxUnixPlatform: bool
        :param SupportWindowsPlatform: Whether Windows is supported.
        :type SupportWindowsPlatform: bool
        :param Price: Current package unit price information.
        :type Price: :class:`tencentcloud.lighthouse.v20200324.models.Price`
        :param CPU: Number of CPU cores.
        :type CPU: int
        :param InternetMaxBandwidthOut: Peak bandwidth in Mbps.
        :type InternetMaxBandwidthOut: int
        :param InternetChargeType: Network billing mode.
        :type InternetChargeType: str
        :param BundleSalesState: Package sale status. Valid values: AVAILABLE, SOLD_OUT
        :type BundleSalesState: str
        :param BundleType: Bundle type. 
Valid values: 
<li>STARTER_BUNDLE: Starter bundle</li>
<li>GENERAL_BUNDLE: General bundle</li>
<li>ENTERPRISE_BUNDLE: Enterprise bundle</li>
<li>STORAGE_BUNDLE: Storage-optimized bundle</li>
<li>EXCLUSIVE_BUNDLE: Dedicated bundle</li>
<li>HK_EXCLUSIVE_BUNDLE: Hong Kong-dedicated bundle </li>
<li>CAREFREE_BUNDLE: Lighthouse Care bundle</li>
<li>BEFAST_BUNDLE: BeFast bundle </li>
        :type BundleType: str
        :param BundleTypeDescription: Bundle type description 
Note: This parameter may return null, indicating that no valid values can be obtained.
        :type BundleTypeDescription: str
        :param BundleDisplayLabel: Package tag.
Valid values:
"ACTIVITY": promotional package
"NORMAL": regular package
"CAREFREE": carefree package
        :type BundleDisplayLabel: str
        """
        self.BundleId = None
        self.Memory = None
        self.SystemDiskType = None
        self.SystemDiskSize = None
        self.MonthlyTraffic = None
        self.SupportLinuxUnixPlatform = None
        self.SupportWindowsPlatform = None
        self.Price = None
        self.CPU = None
        self.InternetMaxBandwidthOut = None
        self.InternetChargeType = None
        self.BundleSalesState = None
        self.BundleType = None
        self.BundleTypeDescription = None
        self.BundleDisplayLabel = None


    def _deserialize(self, params):
        self.BundleId = params.get("BundleId")
        self.Memory = params.get("Memory")
        self.SystemDiskType = params.get("SystemDiskType")
        self.SystemDiskSize = params.get("SystemDiskSize")
        self.MonthlyTraffic = params.get("MonthlyTraffic")
        self.SupportLinuxUnixPlatform = params.get("SupportLinuxUnixPlatform")
        self.SupportWindowsPlatform = params.get("SupportWindowsPlatform")
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.CPU = params.get("CPU")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.InternetChargeType = params.get("InternetChargeType")
        self.BundleSalesState = params.get("BundleSalesState")
        self.BundleType = params.get("BundleType")
        self.BundleTypeDescription = params.get("BundleTypeDescription")
        self.BundleDisplayLabel = params.get("BundleDisplayLabel")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CcnAttachedInstance(AbstractModel):
    """List of instances associated with the CCN instance.

    """

    def __init__(self):
        r"""
        :param CcnId: CCN instance ID.
        :type CcnId: str
        :param CidrBlock: CIDR block of associated instance.
        :type CidrBlock: list of str
        :param State: Associated instance status:

•  PENDING: applying
•  ACTIVE: connected
•  EXPIRED: expired
•  REJECTED: rejected
•  DELETED: deleted
•  FAILED: failed (it will be asynchronously unassociated after 2 hours)
•  ATTACHING: associating
•  DETACHING: unassociating
•  DETACHFAILED: failed to unassociate (it will be asynchronously unassociated after 2 hours)
        :type State: str
        :param AttachedTime: Association time.
Note: this field may return null, indicating that no valid values can be obtained.
        :type AttachedTime: str
        :param Description: Remarks
        :type Description: str
        """
        self.CcnId = None
        self.CidrBlock = None
        self.State = None
        self.AttachedTime = None
        self.Description = None


    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.CidrBlock = params.get("CidrBlock")
        self.State = params.get("State")
        self.AttachedTime = params.get("AttachedTime")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ContainerEnv(AbstractModel):
    """Container environment variable

    """

    def __init__(self):
        r"""
        :param Key: Environment variable key
        :type Key: str
        :param Value: Environment variable value
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
        


class CreateBlueprintRequest(AbstractModel):
    """CreateBlueprint request structure.

    """

    def __init__(self):
        r"""
        :param BlueprintName: Image name, which can contain up to 60 characters.
        :type BlueprintName: str
        :param Description: Image description, which can contain up to 60 characters.
        :type Description: str
        :param InstanceId: ID of the instance for which to make an image.
        :type InstanceId: str
        :param ForcePowerOff: Whether to forcibly shut down the instance before creating the image 
Valid values: 
`True`: Shut down and instance first 
`False`: Create the image when the instance is running 
Default: `True` 
Note that if you create an image when the instance is running, there might be data loss.
        :type ForcePowerOff: bool
        """
        self.BlueprintName = None
        self.Description = None
        self.InstanceId = None
        self.ForcePowerOff = None


    def _deserialize(self, params):
        self.BlueprintName = params.get("BlueprintName")
        self.Description = params.get("Description")
        self.InstanceId = params.get("InstanceId")
        self.ForcePowerOff = params.get("ForcePowerOff")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBlueprintResponse(AbstractModel):
    """CreateBlueprint response structure.

    """

    def __init__(self):
        r"""
        :param BlueprintId: Custom image ID.
        :type BlueprintId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BlueprintId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BlueprintId = params.get("BlueprintId")
        self.RequestId = params.get("RequestId")


class CreateFirewallRulesRequest(AbstractModel):
    """CreateFirewallRules request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param FirewallRules: Firewall rule list.
        :type FirewallRules: list of FirewallRule
        :param FirewallVersion: Current firewall version number. Every time you update the firewall rule version, it will be automatically increased by 1 to prevent the rule from expiring. If it is left empty, conflicts will not be considered.
        :type FirewallVersion: int
        """
        self.InstanceId = None
        self.FirewallRules = None
        self.FirewallVersion = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("FirewallRules") is not None:
            self.FirewallRules = []
            for item in params.get("FirewallRules"):
                obj = FirewallRule()
                obj._deserialize(item)
                self.FirewallRules.append(obj)
        self.FirewallVersion = params.get("FirewallVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateFirewallRulesResponse(AbstractModel):
    """CreateFirewallRules response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateInstanceSnapshotRequest(AbstractModel):
    """CreateInstanceSnapshot request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: ID of the instance for which to create a snapshot.
        :type InstanceId: str
        :param SnapshotName: Snapshot name, which can contain up to 60 characters.
        :type SnapshotName: str
        """
        self.InstanceId = None
        self.SnapshotName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SnapshotName = params.get("SnapshotName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateInstanceSnapshotResponse(AbstractModel):
    """CreateInstanceSnapshot response structure.

    """

    def __init__(self):
        r"""
        :param SnapshotId: Snapshot ID.
        :type SnapshotId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SnapshotId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.RequestId = params.get("RequestId")


class CreateInstancesRequest(AbstractModel):
    """CreateInstances request structure.

    """

    def __init__(self):
        r"""
        :param BundleId: Bundle ID. You can get it via the [DescribeBundles](https://intl.cloud.tencent.com/document/api/1207/47575?from_cn_redirect=1) API.
        :type BundleId: str
        :param BlueprintId: Image ID. You can get it via the [DescribeBlueprints](https://intl.cloud.tencent.com/document/api/1207/47689?from_cn_redirect=1) API.
        :type BlueprintId: str
        :param InstanceChargePrepaid: Monthly subscription information for the instance, including the purchase period, setting of auto-renewal, etc.
        :type InstanceChargePrepaid: :class:`tencentcloud.lighthouse.v20200324.models.InstanceChargePrepaid`
        :param InstanceName: Instance display name.
        :type InstanceName: str
        :param InstanceCount: Number of the instances to purchase. For monthly subscribed instances, the value can be 1 to 30. The default value is `1`. Note that this number can not exceed the remaining quota under the current account.
        :type InstanceCount: int
        :param Zones: List of availability zones. A random AZ is selected by default.
        :type Zones: list of str
        :param DryRun: Whether the request is a dry run only.
`true`: dry run only. The request will not create instance(s). A dry run can check whether all the required parameters are specified, whether the request format is right, whether the request exceeds service limits, and whether the specified CVMs are available.
If the dry run fails, the corresponding error code will be returned.
If the dry run succeeds, the RequestId will be returned.
`false` (default value): send a normal request and create instance(s) if all the requirements are met.
        :type DryRun: bool
        :param ClientToken: A unique string supplied by the client to ensure that the request is idempotent. Its maximum length is 64 ASCII characters. If this parameter is not specified, the idem-potency of the request cannot be guaranteed.
        :type ClientToken: str
        :param LoginConfiguration: Login password of the instance. It’s only available for Windows instances. If it’s not specified, it means that the user choose to set the login password after the instance creation.
        :type LoginConfiguration: :class:`tencentcloud.lighthouse.v20200324.models.LoginConfiguration`
        :param Containers: Configuration of the containers to create
        :type Containers: list of DockerContainerConfiguration
        :param AutoVoucher: Whether to use the vouchers automatically. It defaults to No.
        :type AutoVoucher: bool
        """
        self.BundleId = None
        self.BlueprintId = None
        self.InstanceChargePrepaid = None
        self.InstanceName = None
        self.InstanceCount = None
        self.Zones = None
        self.DryRun = None
        self.ClientToken = None
        self.LoginConfiguration = None
        self.Containers = None
        self.AutoVoucher = None


    def _deserialize(self, params):
        self.BundleId = params.get("BundleId")
        self.BlueprintId = params.get("BlueprintId")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.InstanceName = params.get("InstanceName")
        self.InstanceCount = params.get("InstanceCount")
        self.Zones = params.get("Zones")
        self.DryRun = params.get("DryRun")
        self.ClientToken = params.get("ClientToken")
        if params.get("LoginConfiguration") is not None:
            self.LoginConfiguration = LoginConfiguration()
            self.LoginConfiguration._deserialize(params.get("LoginConfiguration"))
        if params.get("Containers") is not None:
            self.Containers = []
            for item in params.get("Containers"):
                obj = DockerContainerConfiguration()
                obj._deserialize(item)
                self.Containers.append(obj)
        self.AutoVoucher = params.get("AutoVoucher")
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
        :param InstanceIdSet: List of IDs created by using this API. The returning of IDs does not mean that the instances are created successfully.

You can call `DescribeInstances` API, and find the instance ID in the `InstancesSet` returned to check its status. If the `status` is `running`, the instance is created successfully.
        :type InstanceIdSet: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceIdSet = params.get("InstanceIdSet")
        self.RequestId = params.get("RequestId")


class CreateKeyPairRequest(AbstractModel):
    """CreateKeyPair request structure.

    """

    def __init__(self):
        r"""
        :param KeyName: Key pair name, which can contain up to 25 digits, letters, and underscores.
        :type KeyName: str
        """
        self.KeyName = None


    def _deserialize(self, params):
        self.KeyName = params.get("KeyName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateKeyPairResponse(AbstractModel):
    """CreateKeyPair response structure.

    """

    def __init__(self):
        r"""
        :param KeyPair: Key pair information.
        :type KeyPair: :class:`tencentcloud.lighthouse.v20200324.models.KeyPair`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.KeyPair = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("KeyPair") is not None:
            self.KeyPair = KeyPair()
            self.KeyPair._deserialize(params.get("KeyPair"))
        self.RequestId = params.get("RequestId")


class DataDiskPrice(AbstractModel):
    """Data disk price

    """

    def __init__(self):
        r"""
        :param DiskId: Cloud disk ID.
        :type DiskId: str
        :param OriginalDiskPrice: Cloud disk unit price.
        :type OriginalDiskPrice: float
        :param OriginalPrice: Total price of cloud disk
        :type OriginalPrice: float
        :param Discount: Discount.
        :type Discount: float
        :param DiscountPrice: Discounted total price.
        :type DiscountPrice: float
        :param InstanceId: ID of the instance to which the data disk is mounted.
Note: This field may return `null`, indicating that no valid value was found.
        :type InstanceId: str
        """
        self.DiskId = None
        self.OriginalDiskPrice = None
        self.OriginalPrice = None
        self.Discount = None
        self.DiscountPrice = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.OriginalDiskPrice = params.get("OriginalDiskPrice")
        self.OriginalPrice = params.get("OriginalPrice")
        self.Discount = params.get("Discount")
        self.DiscountPrice = params.get("DiscountPrice")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBlueprintsRequest(AbstractModel):
    """DeleteBlueprints request structure.

    """

    def __init__(self):
        r"""
        :param BlueprintIds: Image ID list, which can be obtained from the `BlueprintId` returned by the [DescribeBlueprints](https://intl.cloud.tencent.com/document/product/1207/47689?from_cn_redirect=1) API.
        :type BlueprintIds: list of str
        """
        self.BlueprintIds = None


    def _deserialize(self, params):
        self.BlueprintIds = params.get("BlueprintIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBlueprintsResponse(AbstractModel):
    """DeleteBlueprints response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteFirewallRulesRequest(AbstractModel):
    """DeleteFirewallRules request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param FirewallRules: Firewall rule list.
        :type FirewallRules: list of FirewallRule
        :param FirewallVersion: Current firewall version number. Every time you update the firewall rule version, it will be automatically increased by 1 to prevent the rule from expiring. If it is left empty, conflicts will not be considered.
        :type FirewallVersion: int
        """
        self.InstanceId = None
        self.FirewallRules = None
        self.FirewallVersion = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("FirewallRules") is not None:
            self.FirewallRules = []
            for item in params.get("FirewallRules"):
                obj = FirewallRule()
                obj._deserialize(item)
                self.FirewallRules.append(obj)
        self.FirewallVersion = params.get("FirewallVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteFirewallRulesResponse(AbstractModel):
    """DeleteFirewallRules response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteKeyPairsRequest(AbstractModel):
    """DeleteKeyPairs request structure.

    """

    def __init__(self):
        r"""
        :param KeyIds: Key pair ID list. Each request can contain up to 10 key pairs.
        :type KeyIds: list of str
        """
        self.KeyIds = None


    def _deserialize(self, params):
        self.KeyIds = params.get("KeyIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteKeyPairsResponse(AbstractModel):
    """DeleteKeyPairs response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSnapshotsRequest(AbstractModel):
    """DeleteSnapshots request structure.

    """

    def __init__(self):
        r"""
        :param SnapshotIds: List of IDs of snapshots to be deleted, which can be queried through `DescribeSnapshots`.
        :type SnapshotIds: list of str
        """
        self.SnapshotIds = None


    def _deserialize(self, params):
        self.SnapshotIds = params.get("SnapshotIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSnapshotsResponse(AbstractModel):
    """DeleteSnapshots response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeniedAction(AbstractModel):
    """Restricted operation.

    """

    def __init__(self):
        r"""
        :param Action: Restricted operation name.
        :type Action: str
        :param Code: Restricted operation message code.
        :type Code: str
        :param Message: Restricted operation message.
        :type Message: str
        """
        self.Action = None
        self.Code = None
        self.Message = None


    def _deserialize(self, params):
        self.Action = params.get("Action")
        self.Code = params.get("Code")
        self.Message = params.get("Message")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAllScenesRequest(AbstractModel):
    """DescribeAllScenes request structure.

    """

    def __init__(self):
        r"""
        :param SceneIds: List of scene IDs
        :type SceneIds: list of str
        :param Offset: Offset. Default value: 0
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100
        :type Limit: int
        """
        self.SceneIds = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.SceneIds = params.get("SceneIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAllScenesResponse(AbstractModel):
    """DescribeAllScenes response structure.

    """

    def __init__(self):
        r"""
        :param SceneInfoSet: List of scenes
        :type SceneInfoSet: list of SceneInfo
        :param TotalCount: Total count of scenes
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SceneInfoSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SceneInfoSet") is not None:
            self.SceneInfoSet = []
            for item in params.get("SceneInfoSet"):
                obj = SceneInfo()
                obj._deserialize(item)
                self.SceneInfoSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeBlueprintInstancesRequest(AbstractModel):
    """DescribeBlueprintInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list, which currently can contain only one instance.
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
        


class DescribeBlueprintInstancesResponse(AbstractModel):
    """DescribeBlueprintInstances response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible image instances.
        :type TotalCount: int
        :param BlueprintInstanceSet: Image instance list information.
        :type BlueprintInstanceSet: list of BlueprintInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.BlueprintInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("BlueprintInstanceSet") is not None:
            self.BlueprintInstanceSet = []
            for item in params.get("BlueprintInstanceSet"):
                obj = BlueprintInstance()
                obj._deserialize(item)
                self.BlueprintInstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBlueprintsRequest(AbstractModel):
    """DescribeBlueprints request structure.

    """

    def __init__(self):
        r"""
        :param BlueprintIds: Image ID list.
        :type BlueprintIds: list of str
        :param Offset: Offset. Default value: 0. For more information on `Offset`, please see the relevant section in [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100. For more information on `Limit`, please see the relevant section in the API [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Limit: int
        :param Filters: Filter list.
<li>blueprint-id</li>Filter by the **image ID**.
Type: String
Required: no
<li>blueprint-type</li>Filter by the **image type**.
Valid values: `APP_OS` (application image), `PURE_OS` (system image), `DOCKER` (Docker container image), `PRIVATE` (custom image), `SHARED` (shared image)
Type: String
Required: no
<li>platform-type</li>Filter by the **image operating system**.
Valid values: `LINUX_UNIX` (Linux or Unix), `WINDOWS` (Windows)
Type: String
Required: no
<li>blueprint-name</li>Filter by the **image name**.
Type: String
Required: no
<li>blueprint-state</li>Filter by the **image status**.
Type: String
Required: no
<li>scene-id</li>Filter by the **scene ID**.
Type: String
Required: no

Each request can contain up to 10 `Filters`, each of which can contain up to 100 `Filter.Values`. `BlueprintIds` and `Filters` cannot be specified at the same time.
        :type Filters: list of Filter
        """
        self.BlueprintIds = None
        self.Offset = None
        self.Limit = None
        self.Filters = None


    def _deserialize(self, params):
        self.BlueprintIds = params.get("BlueprintIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBlueprintsResponse(AbstractModel):
    """DescribeBlueprints response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible images.
        :type TotalCount: int
        :param BlueprintSet: Image details list.
        :type BlueprintSet: list of Blueprint
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.BlueprintSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("BlueprintSet") is not None:
            self.BlueprintSet = []
            for item in params.get("BlueprintSet"):
                obj = Blueprint()
                obj._deserialize(item)
                self.BlueprintSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBundleDiscountRequest(AbstractModel):
    """DescribeBundleDiscount request structure.

    """

    def __init__(self):
        r"""
        :param BundleId: Package ID.
        :type BundleId: str
        """
        self.BundleId = None


    def _deserialize(self, params):
        self.BundleId = params.get("BundleId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBundleDiscountResponse(AbstractModel):
    """DescribeBundleDiscount response structure.

    """

    def __init__(self):
        r"""
        :param Currency: Currency: CNY, USD.
        :type Currency: str
        :param DiscountDetail: Discount tier details. The information of each tier includes the duration, discounted quantity, total price, discounted price, and discount details (user discount, official website discount, or final discount).
        :type DiscountDetail: list of DiscountDetail
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Currency = None
        self.DiscountDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Currency = params.get("Currency")
        if params.get("DiscountDetail") is not None:
            self.DiscountDetail = []
            for item in params.get("DiscountDetail"):
                obj = DiscountDetail()
                obj._deserialize(item)
                self.DiscountDetail.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBundlesRequest(AbstractModel):
    """DescribeBundles request structure.

    """

    def __init__(self):
        r"""
        :param BundleIds: Package ID list.
        :type BundleIds: list of str
        :param Offset: Offset. Default value: 0. For more information on `Offset`, please see the relevant section in [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100. For more information on `Limit`, please see the relevant section in the API [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Limit: int
        :param Filters: Filter list
<li>bundle-id</li>Filter by the **bundle ID**.
Type: String
Required: No
<li>support-platform-type</li>Filter by the **OS type**.
Valid values: `LINUX_UNIX` (Linux or Unix), `WINDOWS` (Windows)
Type: String
Required: No
<li>bundle-type</li>Filter by the **bundle type**.
Valid values: `GENERAL_BUNDLE` (General bundle), `STORAGE_BUNDLE` (Storage bundle), `ENTERPRISE_BUNDLE` (Enterprise bundle), `EXCLUSIVE_BUNDLE` (Dedicated bundle), `BEFAST_BUNDLE` (BeFast bundle)
Type: String
Required: No
<li>bundle-state</li>Filter by the **bundle status**.
Valid values: `ONLINE`, `OFFLINE`
Type: String
Required: No
Each request can contain up to 10 `Filters`, and up to 5 `Filter.Values` for each filter. You cannot specify both `BundleIds` and `Filters` at the same time.
        :type Filters: list of Filter
        :param Zones: AZ list, which contains all AZs by default.
        :type Zones: list of str
        """
        self.BundleIds = None
        self.Offset = None
        self.Limit = None
        self.Filters = None
        self.Zones = None


    def _deserialize(self, params):
        self.BundleIds = params.get("BundleIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Zones = params.get("Zones")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBundlesResponse(AbstractModel):
    """DescribeBundles response structure.

    """

    def __init__(self):
        r"""
        :param BundleSet: List of package details.
        :type BundleSet: list of Bundle
        :param TotalCount: Total number of eligible packages, which is used for pagination.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BundleSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("BundleSet") is not None:
            self.BundleSet = []
            for item in params.get("BundleSet"):
                obj = Bundle()
                obj._deserialize(item)
                self.BundleSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeCcnAttachedInstancesRequest(AbstractModel):
    """DescribeCcnAttachedInstances request structure.

    """


class DescribeCcnAttachedInstancesResponse(AbstractModel):
    """DescribeCcnAttachedInstances response structure.

    """

    def __init__(self):
        r"""
        :param CcnAttachedInstanceSet: List of instances associated with the CCN instance.
Note: this field may return null, indicating that no valid values can be obtained.
        :type CcnAttachedInstanceSet: list of CcnAttachedInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.CcnAttachedInstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CcnAttachedInstanceSet") is not None:
            self.CcnAttachedInstanceSet = []
            for item in params.get("CcnAttachedInstanceSet"):
                obj = CcnAttachedInstance()
                obj._deserialize(item)
                self.CcnAttachedInstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDiskConfigsRequest(AbstractModel):
    """DescribeDiskConfigs request structure.

    """

    def __init__(self):
        r"""
        :param Filters: Filter list.
<li>zone</li>Filter by availability zone.
Type: String
Required: no
        :type Filters: list of Filter
        """
        self.Filters = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDiskConfigsResponse(AbstractModel):
    """DescribeDiskConfigs response structure.

    """

    def __init__(self):
        r"""
        :param DiskConfigSet: List of cloud disk configurations.
        :type DiskConfigSet: list of DiskConfig
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DiskConfigSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskConfigSet") is not None:
            self.DiskConfigSet = []
            for item in params.get("DiskConfigSet"):
                obj = DiskConfig()
                obj._deserialize(item)
                self.DiskConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDiskDiscountRequest(AbstractModel):
    """DescribeDiskDiscount request structure.

    """

    def __init__(self):
        r"""
        :param DiskType: Cloud disk type. Valid values: "CLOUD_PREMIUM".
        :type DiskType: str
        :param DiskSize: Cloud disk size.
        :type DiskSize: int
        :param DiskBackupQuota: Specify the quota of disk backups. No quota if it’s left empty. Only one quota is allowed.
        :type DiskBackupQuota: int
        """
        self.DiskType = None
        self.DiskSize = None
        self.DiskBackupQuota = None


    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.DiskSize = params.get("DiskSize")
        self.DiskBackupQuota = params.get("DiskBackupQuota")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDiskDiscountResponse(AbstractModel):
    """DescribeDiskDiscount response structure.

    """

    def __init__(self):
        r"""
        :param Currency: Currency: CNY, USD.
        :type Currency: str
        :param DiscountDetail: Discount tier details. The information of each tier includes the duration, discounted quantity, total price, discounted price, and discount details (user discount, official website discount, or final discount).
        :type DiscountDetail: list of DiscountDetail
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Currency = None
        self.DiscountDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Currency = params.get("Currency")
        if params.get("DiscountDetail") is not None:
            self.DiscountDetail = []
            for item in params.get("DiscountDetail"):
                obj = DiscountDetail()
                obj._deserialize(item)
                self.DiscountDetail.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDisksDeniedActionsRequest(AbstractModel):
    """DescribeDisksDeniedActions request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        """
        self.DiskIds = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDisksDeniedActionsResponse(AbstractModel):
    """DescribeDisksDeniedActions response structure.

    """

    def __init__(self):
        r"""
        :param DiskDeniedActionSet: List of operation limits of cloud disks.
        :type DiskDeniedActionSet: list of DiskDeniedActions
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DiskDeniedActionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskDeniedActionSet") is not None:
            self.DiskDeniedActionSet = []
            for item in params.get("DiskDeniedActionSet"):
                obj = DiskDeniedActions()
                obj._deserialize(item)
                self.DiskDeniedActionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDisksRequest(AbstractModel):
    """DescribeDisks request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        :param Filters: Filter list
disk-id
Filter by **cloud disk ID**.
Type: String
Required: No
instance-id
Filter by **instance ID**.
Type: String
Required: No
disk-name
Filter by **cloud disk name**.
Type: String
Required: No
zone
Filter by **availability zone**.
Type: String
Required: No
disk-usage
Filter by **cloud disk type**.
Type: String
Required: No
Values: `SYSTEM_DISK` and `DATA_DISK`
disk-state
Filter by **cloud disk status**.
Type: String
Required: No
Values: See `DiskState` in [Disk](https://intl.cloud.tencent.com/document/api/1207/47576?from_cn_redirect=1#Disk)
Each request can contain up to 10 `Filters` and 100 `Filter.Values`. `DiskIds` and `Filters` cannot be specified at the same time.
        :type Filters: list of Filter
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100.
        :type Limit: int
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param OrderField: The field by which the cloud disks are sorted. Valid values: "CREATED_TIME" (creation time), "EXPIRED_TIME" (expiration time), "DISK_SIZE" (size of cloud disks). Default value: "CREATED_TIME".
        :type OrderField: str
        :param Order: Sorting order of the output cloud disks. Valid values: "ASC" (ascending order), "DESC" (descending order). Default value: "DESC".
        :type Order: str
        """
        self.DiskIds = None
        self.Filters = None
        self.Limit = None
        self.Offset = None
        self.OrderField = None
        self.Order = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderField = params.get("OrderField")
        self.Order = params.get("Order")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDisksResponse(AbstractModel):
    """DescribeDisks response structure.

    """

    def __init__(self):
        r"""
        :param DiskSet: List of cloud disk information.
        :type DiskSet: list of Disk
        :param TotalCount: Number of eligible cloud disks.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DiskSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskSet") is not None:
            self.DiskSet = []
            for item in params.get("DiskSet"):
                obj = Disk()
                obj._deserialize(item)
                self.DiskSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDisksReturnableRequest(AbstractModel):
    """DescribeDisksReturnable request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100.
        :type Limit: int
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        """
        self.DiskIds = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDisksReturnableResponse(AbstractModel):
    """DescribeDisksReturnable response structure.

    """

    def __init__(self):
        r"""
        :param DiskReturnableSet: List of returnable cloud disks.
        :type DiskReturnableSet: list of DiskReturnable
        :param TotalCount: Number of eligible cloud disks.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DiskReturnableSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskReturnableSet") is not None:
            self.DiskReturnableSet = []
            for item in params.get("DiskReturnableSet"):
                obj = DiskReturnable()
                obj._deserialize(item)
                self.DiskReturnableSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeFirewallRulesRequest(AbstractModel):
    """DescribeFirewallRules request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100.
        :type Limit: int
        """
        self.InstanceId = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeFirewallRulesResponse(AbstractModel):
    """DescribeFirewallRules response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible firewall rules.
        :type TotalCount: int
        :param FirewallRuleSet: Firewall rule details list.
        :type FirewallRuleSet: list of FirewallRuleInfo
        :param FirewallVersion: Firewall version number.
        :type FirewallVersion: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.FirewallRuleSet = None
        self.FirewallVersion = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("FirewallRuleSet") is not None:
            self.FirewallRuleSet = []
            for item in params.get("FirewallRuleSet"):
                obj = FirewallRuleInfo()
                obj._deserialize(item)
                self.FirewallRuleSet.append(obj)
        self.FirewallVersion = params.get("FirewallVersion")
        self.RequestId = params.get("RequestId")


class DescribeFirewallRulesTemplateRequest(AbstractModel):
    """DescribeFirewallRulesTemplate request structure.

    """


class DescribeFirewallRulesTemplateResponse(AbstractModel):
    """DescribeFirewallRulesTemplate response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible firewall rules.
        :type TotalCount: int
        :param FirewallRuleSet: Firewall rule details list.
        :type FirewallRuleSet: list of FirewallRuleInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.FirewallRuleSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("FirewallRuleSet") is not None:
            self.FirewallRuleSet = []
            for item in params.get("FirewallRuleSet"):
                obj = FirewallRuleInfo()
                obj._deserialize(item)
                self.FirewallRuleSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeGeneralResourceQuotasRequest(AbstractModel):
    """DescribeGeneralResourceQuotas request structure.

    """

    def __init__(self):
        r"""
        :param ResourceNames: Resource name list. Values:
- `GENERAL_BUNDLE_INSTANCE`: General bundle
- `STORAGE_BUNDLE_INSTANCE`:  Storage bundle 
- `ENTERPRISE_BUNDLE_INSTANCE`: Enterprise bundle 
- `EXCLUSIVE_BUNDLE_INSTANCE`： Dedicated bundle
- `BEFAST_BUNDLE_INSTANCE`: BeFast bundle
- `USER_KEY_PAIR`: Key pair
- `SNAPSHOT`: Snapshot
- `BLUEPRINT`: Custom image
- `FREE_BLUEPRINT`: Free custom image
- `DATA_DISK`: Data disk
- `FIREWALL_RULE`: Firewall rules
        :type ResourceNames: list of str
        """
        self.ResourceNames = None


    def _deserialize(self, params):
        self.ResourceNames = params.get("ResourceNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeGeneralResourceQuotasResponse(AbstractModel):
    """DescribeGeneralResourceQuotas response structure.

    """

    def __init__(self):
        r"""
        :param GeneralResourceQuotaSet: List of general resource quota details.
        :type GeneralResourceQuotaSet: list of GeneralResourceQuota
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.GeneralResourceQuotaSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("GeneralResourceQuotaSet") is not None:
            self.GeneralResourceQuotaSet = []
            for item in params.get("GeneralResourceQuotaSet"):
                obj = GeneralResourceQuota()
                obj._deserialize(item)
                self.GeneralResourceQuotaSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceLoginKeyPairAttributeRequest(AbstractModel):
    """DescribeInstanceLoginKeyPairAttribute request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
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
        


class DescribeInstanceLoginKeyPairAttributeResponse(AbstractModel):
    """DescribeInstanceLoginKeyPairAttribute response structure.

    """

    def __init__(self):
        r"""
        :param PermitLogin: Whether to allow login with the default key pair. Valid values: YES, NO.
        :type PermitLogin: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.PermitLogin = None
        self.RequestId = None


    def _deserialize(self, params):
        self.PermitLogin = params.get("PermitLogin")
        self.RequestId = params.get("RequestId")


class DescribeInstanceVncUrlRequest(AbstractModel):
    """DescribeInstanceVncUrl request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which can be obtained from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
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
        


class DescribeInstanceVncUrlResponse(AbstractModel):
    """DescribeInstanceVncUrl response structure.

    """

    def __init__(self):
        r"""
        :param InstanceVncUrl: Instance VNC URL.
        :type InstanceVncUrl: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceVncUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceVncUrl = params.get("InstanceVncUrl")
        self.RequestId = params.get("RequestId")


class DescribeInstancesDeniedActionsRequest(AbstractModel):
    """DescribeInstancesDeniedActions request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
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
        


class DescribeInstancesDeniedActionsResponse(AbstractModel):
    """DescribeInstancesDeniedActions response structure.

    """

    def __init__(self):
        r"""
        :param InstanceDeniedActionSet: List of instance operation limit details.
        :type InstanceDeniedActionSet: list of InstanceDeniedActions
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceDeniedActionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("InstanceDeniedActionSet") is not None:
            self.InstanceDeniedActionSet = []
            for item in params.get("InstanceDeniedActionSet"):
                obj = InstanceDeniedActions()
                obj._deserialize(item)
                self.InstanceDeniedActionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesDiskNumRequest(AbstractModel):
    """DescribeInstancesDiskNum request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: List of instance IDs.
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
        


class DescribeInstancesDiskNumResponse(AbstractModel):
    """DescribeInstancesDiskNum response structure.

    """

    def __init__(self):
        r"""
        :param AttachDetailSet: Information of all attached disks
        :type AttachDetailSet: list of AttachDetail
        :param TotalCount: Number of attached cloud disks
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AttachDetailSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AttachDetailSet") is not None:
            self.AttachDetailSet = []
            for item in params.get("AttachDetailSet"):
                obj = AttachDetail()
                obj._deserialize(item)
                self.AttachDetailSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeInstancesRequest(AbstractModel):
    """DescribeInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time.
        :type InstanceIds: list of str
        :param Filters: Filter list. 
<li>instance-name</li>Filter by the **instance name**. 
Type: String 
Required: No 
<li>private-ip-address</li>Filter by the **private IP of instance primary ENI**. 
Type: String 
Required: No 
<li>public-ip-address</li>Filter by the **public IP of instance primary ENI**. 
Type: String 
Required: No 
<li>zone</li>Filter by the availability zone. 
Type: String 
Required: No 
<li>instance-state</li>Filter by the **instance status**. 
Type: String 
Required: No 
<li>tag-key</li>Filter by the **tag key**. 
Type: String 
Required: No 
<li>tag-value</li>Filter by the **tag value**. 
Type: String 
Required: No 
<li> tag:tag-key</li>Filter by tag key-value pair. The `tag-key` should be replaced with a specific tag key. 
Type: String 
Required: No 
Each request can contain up to 10 `Filters` and 100 `Filter.Values`. You cannot specify both `InstanceIds` and `Filters` at the same time.
        :type Filters: list of Filter
        :param Offset: Offset. Default value: 0. For more information on `Offset`, please see the relevant section in [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100. For more information on `Limit`, please see the relevant section in the API [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Limit: int
        """
        self.InstanceIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
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
        :param TotalCount: Number of eligible instances.
        :type TotalCount: int
        :param InstanceSet: List of instance details
        :type InstanceSet: list of Instance
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
                obj = Instance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesReturnableRequest(AbstractModel):
    """DescribeInstancesReturnable request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
        :type InstanceIds: list of str
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100.
        :type Limit: int
        """
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstancesReturnableResponse(AbstractModel):
    """DescribeInstancesReturnable response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible instances.
        :type TotalCount: int
        :param InstanceReturnableSet: List of returnable instance details.
        :type InstanceReturnableSet: list of InstanceReturnable
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceReturnableSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceReturnableSet") is not None:
            self.InstanceReturnableSet = []
            for item in params.get("InstanceReturnableSet"):
                obj = InstanceReturnable()
                obj._deserialize(item)
                self.InstanceReturnableSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesTrafficPackagesRequest(AbstractModel):
    """DescribeInstancesTrafficPackages request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
        :type InstanceIds: list of str
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100.
        :type Limit: int
        """
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstancesTrafficPackagesResponse(AbstractModel):
    """DescribeInstancesTrafficPackages response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible instance traffic package details.
        :type TotalCount: int
        :param InstanceTrafficPackageSet: List of instance traffic package details.
        :type InstanceTrafficPackageSet: list of InstanceTrafficPackage
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceTrafficPackageSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceTrafficPackageSet") is not None:
            self.InstanceTrafficPackageSet = []
            for item in params.get("InstanceTrafficPackageSet"):
                obj = InstanceTrafficPackage()
                obj._deserialize(item)
                self.InstanceTrafficPackageSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeKeyPairsRequest(AbstractModel):
    """DescribeKeyPairs request structure.

    """

    def __init__(self):
        r"""
        :param KeyIds: Key pair ID list.
        :type KeyIds: list of str
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100.
        :type Limit: int
        :param Filters: Filter list.
<li>key-id</li>Filter by **key pair ID**.
Type: String
Required: no
<li>key-name</li>Filter by the **key pair name**. Fuzzy match is supported.
Type: String
Required: no
Each request can contain up to 10 `Filters` and up to 5 `Filter.Values` for each filter. `KeyIds` and `Filters` cannot be specified at the same time.
        :type Filters: list of Filter
        """
        self.KeyIds = None
        self.Offset = None
        self.Limit = None
        self.Filters = None


    def _deserialize(self, params):
        self.KeyIds = params.get("KeyIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeKeyPairsResponse(AbstractModel):
    """DescribeKeyPairs response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible key pairs.
        :type TotalCount: int
        :param KeyPairSet: List of key pair details.
        :type KeyPairSet: list of KeyPair
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.KeyPairSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("KeyPairSet") is not None:
            self.KeyPairSet = []
            for item in params.get("KeyPairSet"):
                obj = KeyPair()
                obj._deserialize(item)
                self.KeyPairSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeModifyInstanceBundlesRequest(AbstractModel):
    """DescribeModifyInstanceBundles request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Filters: Filter list
<li>bundle-id</li>Filter by the **bundle ID**.
Type: String
Required: No
<li>support-platform-type</li>Filter by the **OS type**.
Valid values: `LINUX_UNIX` (Linux or Unix), `WINDOWS` (Windows)
Type: String
Required: No
<li>bundle-type</li>Filter by the **bundle type**.
Valid values: `GENERAL_BUNDLE` (General bundle), `STORAGE_BUNDLE` (Storage bundle), `ENTERPRISE_BUNDLE` (Enterprise bundle), `EXCLUSIVE_BUNDLE` (Dedicated bundle), `BEFAST_BUNDLE` (BeFast bundle)
Type: String
Required: No
<li>bundle-state</li>Filter by the **bundle status**.
Valid values: `ONLINE`, `OFFLINE`
Type: String
Required: No
Each request can contain up to 10 `Filters`, and each filter can have up to 5 `Filter.Values`.
        :type Filters: list of Filter
        :param Offset: Offset. Default value: 0. For more information on `Offset`, please see the relevant section in [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100. For more information on `Limit`, please see the relevant section in the API [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Limit: int
        """
        self.InstanceId = None
        self.Filters = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModifyInstanceBundlesResponse(AbstractModel):
    """DescribeModifyInstanceBundles response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of matched instances.
        :type TotalCount: int
        :param ModifyBundleSet: New package details
        :type ModifyBundleSet: list of ModifyBundle
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ModifyBundleSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ModifyBundleSet") is not None:
            self.ModifyBundleSet = []
            for item in params.get("ModifyBundleSet"):
                obj = ModifyBundle()
                obj._deserialize(item)
                self.ModifyBundleSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRegionsRequest(AbstractModel):
    """DescribeRegions request structure.

    """


class DescribeRegionsResponse(AbstractModel):
    """DescribeRegions response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of regions.
        :type TotalCount: int
        :param RegionSet: Region information list.
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


class DescribeResetInstanceBlueprintsRequest(AbstractModel):
    """DescribeResetInstanceBlueprints request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Offset: Offset. Default value: 0. For more information on `Offset`, please see the relevant section in [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100. For more information on `Limit`, please see the relevant section in the API [Overview](https://intl.cloud.tencent.com/document/product/1207/47578?from_cn_redirect=1).
        :type Limit: int
        :param Filters: Filter list
<li>blueprint-id</li>Filter by **image ID**.
Type: String
Required: no
<li>blueprint-type</li>Filter by **image type**.
Valid values: `APP_OS`: application image; `PURE_OS`: system image; `PRIVATE`: custom image
Type: String
Required: no
<li>platform-type</li>Filter by **image platform type**.
Valid values: `LINUX_UNIX`: Linux or Unix; `WINDOWS`: Windows
Type: String
Required: no
<li>blueprint-name</li>Filter by **image name**.
Type: String
Required: no
<li>blueprint-state</li>Filter by **image status**.
Type: String
Required: no

Each request can contain up to 10 `Filters` and 5 `Filter.Values`. `BlueprintIds` and `Filters` cannot be specified at the same time.
        :type Filters: list of Filter
        """
        self.InstanceId = None
        self.Offset = None
        self.Limit = None
        self.Filters = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeResetInstanceBlueprintsResponse(AbstractModel):
    """DescribeResetInstanceBlueprints response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible images.
        :type TotalCount: int
        :param ResetInstanceBlueprintSet: Image reset information list
        :type ResetInstanceBlueprintSet: list of ResetInstanceBlueprint
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ResetInstanceBlueprintSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ResetInstanceBlueprintSet") is not None:
            self.ResetInstanceBlueprintSet = []
            for item in params.get("ResetInstanceBlueprintSet"):
                obj = ResetInstanceBlueprint()
                obj._deserialize(item)
                self.ResetInstanceBlueprintSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeScenesRequest(AbstractModel):
    """DescribeScenes request structure.

    """

    def __init__(self):
        r"""
        :param SceneIds: List of scene IDs
        :type SceneIds: list of str
        :param Offset: Offset. Default value: 0
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100
        :type Limit: int
        """
        self.SceneIds = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.SceneIds = params.get("SceneIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeScenesResponse(AbstractModel):
    """DescribeScenes response structure.

    """

    def __init__(self):
        r"""
        :param SceneSet: List of scenes
        :type SceneSet: list of Scene
        :param TotalCount: Total number of scenes
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SceneSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SceneSet") is not None:
            self.SceneSet = []
            for item in params.get("SceneSet"):
                obj = Scene()
                obj._deserialize(item)
                self.SceneSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSnapshotsDeniedActionsRequest(AbstractModel):
    """DescribeSnapshotsDeniedActions request structure.

    """

    def __init__(self):
        r"""
        :param SnapshotIds: Snapshot ID list, which can be queried through `DescribeSnapshots`.
        :type SnapshotIds: list of str
        """
        self.SnapshotIds = None


    def _deserialize(self, params):
        self.SnapshotIds = params.get("SnapshotIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSnapshotsDeniedActionsResponse(AbstractModel):
    """DescribeSnapshotsDeniedActions response structure.

    """

    def __init__(self):
        r"""
        :param SnapshotDeniedActionSet: List of snapshot operation limit details.
        :type SnapshotDeniedActionSet: list of SnapshotDeniedActions
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SnapshotDeniedActionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SnapshotDeniedActionSet") is not None:
            self.SnapshotDeniedActionSet = []
            for item in params.get("SnapshotDeniedActionSet"):
                obj = SnapshotDeniedActions()
                obj._deserialize(item)
                self.SnapshotDeniedActionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSnapshotsRequest(AbstractModel):
    """DescribeSnapshots request structure.

    """

    def __init__(self):
        r"""
        :param SnapshotIds: List of IDs of snapshots to be queried.
You cannot specify `SnapshotIds` and `Filters` at the same time.
        :type SnapshotIds: list of str
        :param Filters: Filter list.
<li>snapshot-id</li>Filter by **snapshot ID**.
Type: String
Required: no
<li>disk-id</li>Filter by **disk ID**.
Type: String
Required: no
<li>snapshot-name</li>Filter by **snapshot name**.
Type: String
Required: no
<li>instance-id</li>Filter by **instance ID**.
Type: String
Required: no
Each request can contain up to 10 `Filters` and 5 `Filter.Values`. You cannot specify both `SnapshotIds` and `Filters` at the same time.
        :type Filters: list of Filter
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 100.
        :type Limit: int
        """
        self.SnapshotIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.SnapshotIds = params.get("SnapshotIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSnapshotsResponse(AbstractModel):
    """DescribeSnapshots response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of snapshots.
        :type TotalCount: int
        :param SnapshotSet: List of snapshot details.
        :type SnapshotSet: list of Snapshot
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.SnapshotSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("SnapshotSet") is not None:
            self.SnapshotSet = []
            for item in params.get("SnapshotSet"):
                obj = Snapshot()
                obj._deserialize(item)
                self.SnapshotSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeZonesRequest(AbstractModel):
    """DescribeZones request structure.

    """

    def __init__(self):
        r"""
        :param OrderField: Sorting field. Valid values:
<li>`ZONE`: Sort by the availability zone.
<li>`INSTANCE_DISPLAY_LABEL`: Sort by visibility labels (`HIDDEN`, `NORMAL` and `SELECTED`). Default: ['HIDDEN', 'NORMAL', 'SELECTED'].
The default value is `ZONE`.
        :type OrderField: str
        :param Order: Specifies how availability zones are listed. Valid values:
<li>ASC: Ascending sort. 
<li>DESC: Descending sort.
The default value is `ASC`.
        :type Order: str
        """
        self.OrderField = None
        self.Order = None


    def _deserialize(self, params):
        self.OrderField = params.get("OrderField")
        self.Order = params.get("Order")
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
        :param TotalCount: Number of AZs
        :type TotalCount: int
        :param ZoneInfoSet: List of AZ details
        :type ZoneInfoSet: list of ZoneInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.ZoneInfoSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ZoneInfoSet") is not None:
            self.ZoneInfoSet = []
            for item in params.get("ZoneInfoSet"):
                obj = ZoneInfo()
                obj._deserialize(item)
                self.ZoneInfoSet.append(obj)
        self.RequestId = params.get("RequestId")


class DetachCcnRequest(AbstractModel):
    """DetachCcn request structure.

    """

    def __init__(self):
        r"""
        :param CcnId: CCN instance ID.
        :type CcnId: str
        """
        self.CcnId = None


    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DetachCcnResponse(AbstractModel):
    """DetachCcn response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DetachDisksRequest(AbstractModel):
    """DetachDisks request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        """
        self.DiskIds = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DetachDisksResponse(AbstractModel):
    """DetachDisks response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DetailPrice(AbstractModel):
    """Billable items

    """

    def __init__(self):
        r"""
        :param PriceName: Values: 
<li>"DiskSpace": Cloud disk space</li>
<li>"DiskBackupQuota": Cloud disk backups</li>
        :type PriceName: str
        :param OriginUnitPrice: Official unit price of the billable item
        :type OriginUnitPrice: float
        :param OriginalPrice: Official total price of the billable item
        :type OriginalPrice: float
        :param Discount: Discount of the billable item
        :type Discount: float
        :param DiscountPrice: Discounted total price of the billable item
        :type DiscountPrice: float
        """
        self.PriceName = None
        self.OriginUnitPrice = None
        self.OriginalPrice = None
        self.Discount = None
        self.DiscountPrice = None


    def _deserialize(self, params):
        self.PriceName = params.get("PriceName")
        self.OriginUnitPrice = params.get("OriginUnitPrice")
        self.OriginalPrice = params.get("OriginalPrice")
        self.Discount = params.get("Discount")
        self.DiscountPrice = params.get("DiscountPrice")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisassociateInstancesKeyPairsRequest(AbstractModel):
    """DisassociateInstancesKeyPairs request structure.

    """

    def __init__(self):
        r"""
        :param KeyIds: Key pair ID list. Each request can contain up to 100 key pairs.
        :type KeyIds: list of str
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
        :type InstanceIds: list of str
        """
        self.KeyIds = None
        self.InstanceIds = None


    def _deserialize(self, params):
        self.KeyIds = params.get("KeyIds")
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisassociateInstancesKeyPairsResponse(AbstractModel):
    """DisassociateInstancesKeyPairs response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DiscountDetail(AbstractModel):
    """Package discount details (only returned for price query APIs called in the console).

    """

    def __init__(self):
        r"""
        :param TimeSpan: Billing duration.
        :type TimeSpan: int
        :param TimeUnit: Billing unit.
        :type TimeUnit: str
        :param TotalCost: Total price.
        :type TotalCost: float
        :param RealTotalCost: Discounted total price.
        :type RealTotalCost: float
        :param Discount: Discount.
        :type Discount: int
        :param PolicyDetail: Discount details.
        :type PolicyDetail: :class:`tencentcloud.lighthouse.v20200324.models.PolicyDetail`
        """
        self.TimeSpan = None
        self.TimeUnit = None
        self.TotalCost = None
        self.RealTotalCost = None
        self.Discount = None
        self.PolicyDetail = None


    def _deserialize(self, params):
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        self.TotalCost = params.get("TotalCost")
        self.RealTotalCost = params.get("RealTotalCost")
        self.Discount = params.get("Discount")
        if params.get("PolicyDetail") is not None:
            self.PolicyDetail = PolicyDetail()
            self.PolicyDetail._deserialize(params.get("PolicyDetail"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Disk(AbstractModel):
    """Disk information

    """

    def __init__(self):
        r"""
        :param DiskId: Disk ID
        :type DiskId: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Zone: Availability zone
        :type Zone: str
        :param DiskName: Disk name
        :type DiskName: str
        :param DiskUsage: Disk type
        :type DiskUsage: str
        :param DiskType: Disk media type
        :type DiskType: str
        :param DiskChargeType: Disk payment type
        :type DiskChargeType: str
        :param DiskSize: Disk size
        :type DiskSize: int
        :param RenewFlag: Renewal flag
        :type RenewFlag: str
        :param DiskState: Disk status. Values: 
<li>`PENDING`: Creating</li>
<li>`UNATTACHED`: Not attached</li>
<li>`ATTACHING`: Attaching</li>
<li>`ATTACHED`: Attached</li>
<li>`DETACHING`: Detaching</li>
<li>`SHUTDOWN`: Isolated</li>
<li>`CREATED_FAILED`: Failed to create</li>
<li>`TERMINATING`: Terminating</li>
<li>`DELETING`: Deleting</li>
<li>`FREEZING`: Freezing</li>
        :type DiskState: str
        :param Attached: Whether the disk is attached to an instance
        :type Attached: bool
        :param DeleteWithInstance: Whether to release the disk along with the instance
        :type DeleteWithInstance: bool
        :param LatestOperation: Last operation
        :type LatestOperation: str
        :param LatestOperationState: Last operation status
        :type LatestOperationState: str
        :param LatestOperationRequestId: Last request ID
        :type LatestOperationRequestId: str
        :param CreatedTime: Creation time according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type CreatedTime: str
        :param ExpiredTime: Expiration time according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ExpiredTime: str
        :param IsolatedTime: Isolation time according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: This field may return null, indicating that no valid values can be obtained.
        :type IsolatedTime: str
        :param DiskBackupCount: Total disk backups
        :type DiskBackupCount: int
        :param DiskBackupQuota: Disk backup quota
        :type DiskBackupQuota: int
        """
        self.DiskId = None
        self.InstanceId = None
        self.Zone = None
        self.DiskName = None
        self.DiskUsage = None
        self.DiskType = None
        self.DiskChargeType = None
        self.DiskSize = None
        self.RenewFlag = None
        self.DiskState = None
        self.Attached = None
        self.DeleteWithInstance = None
        self.LatestOperation = None
        self.LatestOperationState = None
        self.LatestOperationRequestId = None
        self.CreatedTime = None
        self.ExpiredTime = None
        self.IsolatedTime = None
        self.DiskBackupCount = None
        self.DiskBackupQuota = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.InstanceId = params.get("InstanceId")
        self.Zone = params.get("Zone")
        self.DiskName = params.get("DiskName")
        self.DiskUsage = params.get("DiskUsage")
        self.DiskType = params.get("DiskType")
        self.DiskChargeType = params.get("DiskChargeType")
        self.DiskSize = params.get("DiskSize")
        self.RenewFlag = params.get("RenewFlag")
        self.DiskState = params.get("DiskState")
        self.Attached = params.get("Attached")
        self.DeleteWithInstance = params.get("DeleteWithInstance")
        self.LatestOperation = params.get("LatestOperation")
        self.LatestOperationState = params.get("LatestOperationState")
        self.LatestOperationRequestId = params.get("LatestOperationRequestId")
        self.CreatedTime = params.get("CreatedTime")
        self.ExpiredTime = params.get("ExpiredTime")
        self.IsolatedTime = params.get("IsolatedTime")
        self.DiskBackupCount = params.get("DiskBackupCount")
        self.DiskBackupQuota = params.get("DiskBackupQuota")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DiskChargePrepaid(AbstractModel):
    """Parameter settings for the monthly subscribed cloud disk

    """

    def __init__(self):
        r"""
        :param Period: Purchase duration.
        :type Period: int
        :param RenewFlag: Whether Auto-Renewal is enabled 
        :type RenewFlag: str
        :param TimeUnit: Purchase duration unit. Default value: "m" (month)
        :type TimeUnit: str
        """
        self.Period = None
        self.RenewFlag = None
        self.TimeUnit = None


    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")
        self.TimeUnit = params.get("TimeUnit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DiskConfig(AbstractModel):
    """Cloud disk configuration

    """

    def __init__(self):
        r"""
        :param Zone: Availability zone.
        :type Zone: str
        :param DiskType: Cloud disk type.
        :type DiskType: str
        :param DiskSalesState: Cloud disk sale status.
        :type DiskSalesState: str
        :param MaxDiskSize: Maximum cloud disk size.
        :type MaxDiskSize: int
        :param MinDiskSize: Minimum cloud disk size.
        :type MinDiskSize: int
        :param DiskStepSize: Cloud disk increment.
        :type DiskStepSize: int
        """
        self.Zone = None
        self.DiskType = None
        self.DiskSalesState = None
        self.MaxDiskSize = None
        self.MinDiskSize = None
        self.DiskStepSize = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.DiskType = params.get("DiskType")
        self.DiskSalesState = params.get("DiskSalesState")
        self.MaxDiskSize = params.get("MaxDiskSize")
        self.MinDiskSize = params.get("MinDiskSize")
        self.DiskStepSize = params.get("DiskStepSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DiskDeniedActions(AbstractModel):
    """List of operation limits of disks.

    """

    def __init__(self):
        r"""
        :param DiskId: Cloud disk ID.
        :type DiskId: str
        :param DeniedActions: List of operation limits.
        :type DeniedActions: list of DeniedAction
        """
        self.DiskId = None
        self.DeniedActions = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        if params.get("DeniedActions") is not None:
            self.DeniedActions = []
            for item in params.get("DeniedActions"):
                obj = DeniedAction()
                obj._deserialize(item)
                self.DeniedActions.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DiskPrice(AbstractModel):
    """Cloud disk price

    """

    def __init__(self):
        r"""
        :param OriginalDiskPrice: Cloud disk unit price.
        :type OriginalDiskPrice: float
        :param OriginalPrice: Total cloud disk price.
        :type OriginalPrice: float
        :param Discount: Discount.
        :type Discount: float
        :param DiscountPrice: Discounted total price.
        :type DiscountPrice: float
        :param DetailPrices: Detailed billing items
        :type DetailPrices: list of DetailPrice
        """
        self.OriginalDiskPrice = None
        self.OriginalPrice = None
        self.Discount = None
        self.DiscountPrice = None
        self.DetailPrices = None


    def _deserialize(self, params):
        self.OriginalDiskPrice = params.get("OriginalDiskPrice")
        self.OriginalPrice = params.get("OriginalPrice")
        self.Discount = params.get("Discount")
        self.DiscountPrice = params.get("DiscountPrice")
        if params.get("DetailPrices") is not None:
            self.DetailPrices = []
            for item in params.get("DetailPrices"):
                obj = DetailPrice()
                obj._deserialize(item)
                self.DetailPrices.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DiskReturnable(AbstractModel):
    """Details of the returnable cloud disk

    """

    def __init__(self):
        r"""
        :param DiskId: Cloud disk ID.
        :type DiskId: str
        :param IsReturnable: Whether the cloud disk can be returned.
        :type IsReturnable: bool
        :param ReturnFailCode: Error code of cloud disk return failure.
        :type ReturnFailCode: int
        :param ReturnFailMessage: Error message of cloud disk return failure.
        :type ReturnFailMessage: str
        """
        self.DiskId = None
        self.IsReturnable = None
        self.ReturnFailCode = None
        self.ReturnFailMessage = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.IsReturnable = params.get("IsReturnable")
        self.ReturnFailCode = params.get("ReturnFailCode")
        self.ReturnFailMessage = params.get("ReturnFailMessage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DockerContainerConfiguration(AbstractModel):
    """Configuration used to create Docker containers

    """

    def __init__(self):
        r"""
        :param ContainerImage: Container image address
        :type ContainerImage: str
        :param ContainerName: Container name
        :type ContainerName: str
        :param Envs: List of environment variables
        :type Envs: list of ContainerEnv
        :param PublishPorts: List of mappings of container ports and host ports
        :type PublishPorts: list of DockerContainerPublishPort
        :param Volumes: List of container mount volumes
        :type Volumes: list of DockerContainerVolume
        :param Command: The command to run
        :type Command: str
        """
        self.ContainerImage = None
        self.ContainerName = None
        self.Envs = None
        self.PublishPorts = None
        self.Volumes = None
        self.Command = None


    def _deserialize(self, params):
        self.ContainerImage = params.get("ContainerImage")
        self.ContainerName = params.get("ContainerName")
        if params.get("Envs") is not None:
            self.Envs = []
            for item in params.get("Envs"):
                obj = ContainerEnv()
                obj._deserialize(item)
                self.Envs.append(obj)
        if params.get("PublishPorts") is not None:
            self.PublishPorts = []
            for item in params.get("PublishPorts"):
                obj = DockerContainerPublishPort()
                obj._deserialize(item)
                self.PublishPorts.append(obj)
        if params.get("Volumes") is not None:
            self.Volumes = []
            for item in params.get("Volumes"):
                obj = DockerContainerVolume()
                obj._deserialize(item)
                self.Volumes.append(obj)
        self.Command = params.get("Command")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DockerContainerPublishPort(AbstractModel):
    """Port mapping of the Docker container

    """

    def __init__(self):
        r"""
        :param HostPort: Host port
        :type HostPort: int
        :param ContainerPort: Container port
        :type ContainerPort: int
        :param Ip: External IP. It defaults to 0.0.0.0.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Ip: str
        :param Protocol: The protocol defaults to `tcp`. Valid values: `tcp`, `udp` and `sctp`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Protocol: str
        """
        self.HostPort = None
        self.ContainerPort = None
        self.Ip = None
        self.Protocol = None


    def _deserialize(self, params):
        self.HostPort = params.get("HostPort")
        self.ContainerPort = params.get("ContainerPort")
        self.Ip = params.get("Ip")
        self.Protocol = params.get("Protocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DockerContainerVolume(AbstractModel):
    """Docker container mount volume

    """

    def __init__(self):
        r"""
        :param ContainerPath: Container path
        :type ContainerPath: str
        :param HostPath: Host path
        :type HostPath: str
        """
        self.ContainerPath = None
        self.HostPath = None


    def _deserialize(self, params):
        self.ContainerPath = params.get("ContainerPath")
        self.HostPath = params.get("HostPath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Filter(AbstractModel):
    """>Key-Value pair filter for conditional filtering queries, such as filtering name
    > * If there are multiple `Filter` parameters, the relationship among them is the logical `AND`.
    > * If there are multiple `Values` for the same `Filter`, the relationship among the `Values` is the logical `OR`.
    >
    > Taking the `Filter` in the `DescribeInstances` API as an example, you can use the following filters to query the instance whose name (`instance-name`) is `test` ***and*** private IP (`private-ip-address`) is 10.10.10.10:
    ```
    Filters.0.Name=instance-name
    &Filters.0.Values.0=test
    &Filters.1.Name=private-ip-address
    &Filters.1.Values.0=10.10.10.10
    ```

    """

    def __init__(self):
        r"""
        :param Name: Field to be filtered.
        :type Name: str
        :param Values: Filter value of field.
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
        


class FirewallRule(AbstractModel):
    """Firewall rule information.

    """

    def __init__(self):
        r"""
        :param Protocol: Protocol. Valid values: TCP, UDP, ICMP, ALL.
        :type Protocol: str
        :param Port: Port. Valid values: ALL, one single port, multiple ports separated by commas, or port range indicated by a minus sign
        :type Port: str
        :param CidrBlock: IP range or IP (mutually exclusive). Default value: 0.0.0.0/0, which indicates all sources.
        :type CidrBlock: str
        :param Action: Valid values: ACCEPT, DROP. Default value: ACCEPT.
        :type Action: str
        :param FirewallRuleDescription: Firewall rule description.
        :type FirewallRuleDescription: str
        """
        self.Protocol = None
        self.Port = None
        self.CidrBlock = None
        self.Action = None
        self.FirewallRuleDescription = None


    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        self.CidrBlock = params.get("CidrBlock")
        self.Action = params.get("Action")
        self.FirewallRuleDescription = params.get("FirewallRuleDescription")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FirewallRuleInfo(AbstractModel):
    """Firewall rule details.

    """

    def __init__(self):
        r"""
        :param AppType: Application type. Valid values: custom, HTTP (80), HTTPS (443), Linux login (22), Windows login (3389), MySQL (3306), SQL Server (1433), all TCP ports, all UDP ports, Ping-ICMP, ALL.
        :type AppType: str
        :param Protocol: Protocol. Valid values: TCP, UDP, ICMP, ALL.
        :type Protocol: str
        :param Port: Port. Valid values: ALL, one single port, multiple ports separated by commas, or port range indicated by a minus sign
        :type Port: str
        :param CidrBlock: IP range or IP (mutually exclusive). Default value: 0.0.0.0/0, which indicates all sources.
        :type CidrBlock: str
        :param Action: Valid values: ACCEPT, DROP. Default value: ACCEPT.
        :type Action: str
        :param FirewallRuleDescription: Firewall rule description.
        :type FirewallRuleDescription: str
        """
        self.AppType = None
        self.Protocol = None
        self.Port = None
        self.CidrBlock = None
        self.Action = None
        self.FirewallRuleDescription = None


    def _deserialize(self, params):
        self.AppType = params.get("AppType")
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        self.CidrBlock = params.get("CidrBlock")
        self.Action = params.get("Action")
        self.FirewallRuleDescription = params.get("FirewallRuleDescription")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GeneralResourceQuota(AbstractModel):
    """General resource quota information.


    """

    def __init__(self):
        r"""
        :param ResourceName: Resource name.
        :type ResourceName: str
        :param ResourceQuotaAvailable: Number of available resources.
        :type ResourceQuotaAvailable: int
        :param ResourceQuotaTotal: Total number of resources.
        :type ResourceQuotaTotal: int
        """
        self.ResourceName = None
        self.ResourceQuotaAvailable = None
        self.ResourceQuotaTotal = None


    def _deserialize(self, params):
        self.ResourceName = params.get("ResourceName")
        self.ResourceQuotaAvailable = params.get("ResourceQuotaAvailable")
        self.ResourceQuotaTotal = params.get("ResourceQuotaTotal")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImportKeyPairRequest(AbstractModel):
    """ImportKeyPair request structure.

    """

    def __init__(self):
        r"""
        :param KeyName: Key pair name, which can contain up to 25 digits, letters, and underscores.
        :type KeyName: str
        :param PublicKey: Public key content of the key pair, which is in the OpenSSH RSA format.
        :type PublicKey: str
        """
        self.KeyName = None
        self.PublicKey = None


    def _deserialize(self, params):
        self.KeyName = params.get("KeyName")
        self.PublicKey = params.get("PublicKey")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImportKeyPairResponse(AbstractModel):
    """ImportKeyPair response structure.

    """

    def __init__(self):
        r"""
        :param KeyId: Key pair ID.
        :type KeyId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.KeyId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.KeyId = params.get("KeyId")
        self.RequestId = params.get("RequestId")


class InquirePriceCreateBlueprintRequest(AbstractModel):
    """InquirePriceCreateBlueprint request structure.

    """

    def __init__(self):
        r"""
        :param BlueprintCount: Number of custom images. Default value: 1.
        :type BlueprintCount: int
        """
        self.BlueprintCount = None


    def _deserialize(self, params):
        self.BlueprintCount = params.get("BlueprintCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceCreateBlueprintResponse(AbstractModel):
    """InquirePriceCreateBlueprint response structure.

    """

    def __init__(self):
        r"""
        :param BlueprintPrice: Custom image price.
        :type BlueprintPrice: :class:`tencentcloud.lighthouse.v20200324.models.BlueprintPrice`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BlueprintPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("BlueprintPrice") is not None:
            self.BlueprintPrice = BlueprintPrice()
            self.BlueprintPrice._deserialize(params.get("BlueprintPrice"))
        self.RequestId = params.get("RequestId")


class InquirePriceCreateDisksRequest(AbstractModel):
    """InquirePriceCreateDisks request structure.

    """

    def __init__(self):
        r"""
        :param DiskSize: Cloud disk size in GB.
        :type DiskSize: int
        :param DiskType: Cloud disk media type. Valid values: "CLOUD_PREMIUM" (premium cloud storage), "CLOUD_SSD" (SSD cloud disk).
        :type DiskType: str
        :param DiskChargePrepaid: Parameter settings for purchasing the monthly subscribed cloud disk.
        :type DiskChargePrepaid: :class:`tencentcloud.lighthouse.v20200324.models.DiskChargePrepaid`
        :param DiskCount: Number of cloud disks. Default value: 1.
        :type DiskCount: int
        :param DiskBackupQuota: Specify the quota of disk backups. No quota if it’s left empty. Only one quota is allowed.
        :type DiskBackupQuota: int
        """
        self.DiskSize = None
        self.DiskType = None
        self.DiskChargePrepaid = None
        self.DiskCount = None
        self.DiskBackupQuota = None


    def _deserialize(self, params):
        self.DiskSize = params.get("DiskSize")
        self.DiskType = params.get("DiskType")
        if params.get("DiskChargePrepaid") is not None:
            self.DiskChargePrepaid = DiskChargePrepaid()
            self.DiskChargePrepaid._deserialize(params.get("DiskChargePrepaid"))
        self.DiskCount = params.get("DiskCount")
        self.DiskBackupQuota = params.get("DiskBackupQuota")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceCreateDisksResponse(AbstractModel):
    """InquirePriceCreateDisks response structure.

    """

    def __init__(self):
        r"""
        :param DiskPrice: Cloud disk price.
        :type DiskPrice: :class:`tencentcloud.lighthouse.v20200324.models.DiskPrice`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DiskPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = DiskPrice()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class InquirePriceCreateInstancesRequest(AbstractModel):
    """InquirePriceCreateInstances request structure.

    """

    def __init__(self):
        r"""
        :param BundleId: Instance package ID.
        :type BundleId: str
        :param InstanceChargePrepaid: Parameter setting for prepaid mode. This parameter can specify the purchase period, whether to enable auto-renewal, and other attributes of the monthly subscribed instances.
        :type InstanceChargePrepaid: :class:`tencentcloud.lighthouse.v20200324.models.InstanceChargePrepaid`
        :param InstanceCount: Number of instances to be created. Default value: 1.
        :type InstanceCount: int
        :param BlueprintId: Application image ID, which is required if a paid application image is used and can be obtained from the `BlueprintId` returned by the [DescribeBlueprints](https://intl.cloud.tencent.com/document/product/1207/47689?from_cn_redirect=1) API.
        :type BlueprintId: str
        """
        self.BundleId = None
        self.InstanceChargePrepaid = None
        self.InstanceCount = None
        self.BlueprintId = None


    def _deserialize(self, params):
        self.BundleId = params.get("BundleId")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.InstanceCount = params.get("InstanceCount")
        self.BlueprintId = params.get("BlueprintId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceCreateInstancesResponse(AbstractModel):
    """InquirePriceCreateInstances response structure.

    """

    def __init__(self):
        r"""
        :param Price: Price query information.
        :type Price: :class:`tencentcloud.lighthouse.v20200324.models.Price`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquirePriceRenewDisksRequest(AbstractModel):
    """InquirePriceRenewDisks request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        :param RenewDiskChargePrepaid: Parameter settings for renewing the monthly subscribed cloud disk.
        :type RenewDiskChargePrepaid: :class:`tencentcloud.lighthouse.v20200324.models.RenewDiskChargePrepaid`
        """
        self.DiskIds = None
        self.RenewDiskChargePrepaid = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        if params.get("RenewDiskChargePrepaid") is not None:
            self.RenewDiskChargePrepaid = RenewDiskChargePrepaid()
            self.RenewDiskChargePrepaid._deserialize(params.get("RenewDiskChargePrepaid"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceRenewDisksResponse(AbstractModel):
    """InquirePriceRenewDisks response structure.

    """

    def __init__(self):
        r"""
        :param DiskPrice: Cloud disk price.
        :type DiskPrice: :class:`tencentcloud.lighthouse.v20200324.models.DiskPrice`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DiskPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = DiskPrice()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class InquirePriceRenewInstancesRequest(AbstractModel):
    """InquirePriceRenewInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: IDs of the instances to be renewed. Each request can contain up to 50 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
        :type InstanceIds: list of str
        :param InstanceChargePrepaid: Parameter setting for prepaid mode. This parameter can specify the renewal period, whether to enable auto-renewal, and other attributes of the monthly subscribed instances.
        :type InstanceChargePrepaid: :class:`tencentcloud.lighthouse.v20200324.models.InstanceChargePrepaid`
        :param RenewDataDisk: Whether to renew the data disk. Default: `false`.
        :type RenewDataDisk: bool
        :param AlignInstanceExpiredTime: Whether to align the data disk expiration with the instance expiration time. Default: `false`.
        :type AlignInstanceExpiredTime: bool
        """
        self.InstanceIds = None
        self.InstanceChargePrepaid = None
        self.RenewDataDisk = None
        self.AlignInstanceExpiredTime = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.RenewDataDisk = params.get("RenewDataDisk")
        self.AlignInstanceExpiredTime = params.get("AlignInstanceExpiredTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceRenewInstancesResponse(AbstractModel):
    """InquirePriceRenewInstances response structure.

    """

    def __init__(self):
        r"""
        :param Price: Price information. It defaults to the price information of the first instance in the list.
        :type Price: :class:`tencentcloud.lighthouse.v20200324.models.Price`
        :param DataDiskPriceSet: List of data disk price information.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DataDiskPriceSet: list of DataDiskPrice
        :param InstancePriceDetailSet: Price list of the instances to be renewed.
Note: This field may return `null`, indicating that no valid value was found.
        :type InstancePriceDetailSet: list of InstancePriceDetail
        :param TotalPrice: Total price
        :type TotalPrice: :class:`tencentcloud.lighthouse.v20200324.models.TotalPrice`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Price = None
        self.DataDiskPriceSet = None
        self.InstancePriceDetailSet = None
        self.TotalPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        if params.get("DataDiskPriceSet") is not None:
            self.DataDiskPriceSet = []
            for item in params.get("DataDiskPriceSet"):
                obj = DataDiskPrice()
                obj._deserialize(item)
                self.DataDiskPriceSet.append(obj)
        if params.get("InstancePriceDetailSet") is not None:
            self.InstancePriceDetailSet = []
            for item in params.get("InstancePriceDetailSet"):
                obj = InstancePriceDetail()
                obj._deserialize(item)
                self.InstancePriceDetailSet.append(obj)
        if params.get("TotalPrice") is not None:
            self.TotalPrice = TotalPrice()
            self.TotalPrice._deserialize(params.get("TotalPrice"))
        self.RequestId = params.get("RequestId")


class Instance(AbstractModel):
    """Instance information.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param BundleId: Package ID.
        :type BundleId: str
        :param BlueprintId: Image ID.
        :type BlueprintId: str
        :param CPU: Number of instance CPU cores.
        :type CPU: int
        :param Memory: Instance memory capacity in GB.
        :type Memory: int
        :param InstanceName: Instance name.
        :type InstanceName: str
        :param InstanceChargeType: Instance billing mode. Valid values: 
PREPAID: prepaid (i.e., monthly subscription).
        :type InstanceChargeType: str
        :param SystemDisk: Instance system disk information.
        :type SystemDisk: :class:`tencentcloud.lighthouse.v20200324.models.SystemDisk`
        :param PrivateAddresses: Private IP of instance primary ENI. 
Note: this field may return null, indicating that no valid values can be obtained.
        :type PrivateAddresses: list of str
        :param PublicAddresses: Public IP of instance primary ENI. 
Note: this field may return null, indicating that no valid values can be obtained.
        :type PublicAddresses: list of str
        :param InternetAccessible: Instance bandwidth information.
        :type InternetAccessible: :class:`tencentcloud.lighthouse.v20200324.models.InternetAccessible`
        :param RenewFlag: Auto-Renewal flag. Valid values: 
NOTIFY_AND_MANUAL_RENEW: notify upon expiration but do not renew automatically  
NOTIFY_AND_AUTO_RENEW: notify upon expiration and renew automatically.
        :type RenewFlag: str
        :param LoginSettings: Instance login settings.
        :type LoginSettings: :class:`tencentcloud.lighthouse.v20200324.models.LoginSettings`
        :param InstanceState: Instance status. Valid values: 
<li>PENDING: Creating</li><li>LAUNCH_FAILED: Failed to create</li><li>RUNNING: Running</li><li>STOPPED: Shut down</li><li>STARTING: Starting up</li><li>STOPPING: Shutting down</li><li>REBOOTING: Restarting</li><li>SHUTDOWN: Shutdown and to be terminated</li><li>TERMINATING: Terminating</li><li>DELETING: Deleting</li><li>FREEZING: Frozen</li><li>ENTER_RESCUE_MODE: Entering the rescue mode</li><li>RESCUE_MODE: Rescue mode</li><li>EXIT_RESCUE_MODE: Exiting from the rescue mode</li>
        :type InstanceState: str
        :param Uuid: Globally unique ID of instance.
        :type Uuid: str
        :param LatestOperation: Last instance operation, such as `StopInstances` and `ResetInstance`. Note: this field may return null, indicating that no valid values can be obtained.
        :type LatestOperation: str
        :param LatestOperationState: Last instance operation status. Valid values: 
SUCCESS: operation succeeded 
OPERATING: the operation is being executed 
FAILED: operation failed 
Note: this field may return null, indicating that no valid values can be obtained.
        :type LatestOperationState: str
        :param LatestOperationRequestId: Unique request ID for the last operation of the instance. 
Note: this field may return null, indicating that no valid values can be obtained.
        :type LatestOperationRequestId: str
        :param IsolatedTime: Isolation time according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: this field may return null, indicating that no valid values can be obtained.
        :type IsolatedTime: str
        :param CreatedTime: Creation time according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: this field may return null, indicating that no valid values can be obtained.
        :type CreatedTime: str
        :param ExpiredTime: Expiration time according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: this field may return null, indicating that no valid values can be obtained.
        :type ExpiredTime: str
        :param PlatformType: OS type, such as LINUX_UNIX and WINDOWS.
        :type PlatformType: str
        :param Platform: OS type.
        :type Platform: str
        :param OsName: OS name.
        :type OsName: str
        :param Zone: AZ.
        :type Zone: str
        :param Tags: The list of tags associated with the instance
        :type Tags: list of Tag
        :param InstanceRestrictState: Obtain instance status
<li>NORMAL: The instance is normal</li><li>NETWORK_RESTRICT: The instance is blocked from the network.</li>
        :type InstanceRestrictState: str
        """
        self.InstanceId = None
        self.BundleId = None
        self.BlueprintId = None
        self.CPU = None
        self.Memory = None
        self.InstanceName = None
        self.InstanceChargeType = None
        self.SystemDisk = None
        self.PrivateAddresses = None
        self.PublicAddresses = None
        self.InternetAccessible = None
        self.RenewFlag = None
        self.LoginSettings = None
        self.InstanceState = None
        self.Uuid = None
        self.LatestOperation = None
        self.LatestOperationState = None
        self.LatestOperationRequestId = None
        self.IsolatedTime = None
        self.CreatedTime = None
        self.ExpiredTime = None
        self.PlatformType = None
        self.Platform = None
        self.OsName = None
        self.Zone = None
        self.Tags = None
        self.InstanceRestrictState = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.BundleId = params.get("BundleId")
        self.BlueprintId = params.get("BlueprintId")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")
        self.InstanceName = params.get("InstanceName")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = SystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        self.PrivateAddresses = params.get("PrivateAddresses")
        self.PublicAddresses = params.get("PublicAddresses")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.RenewFlag = params.get("RenewFlag")
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        self.InstanceState = params.get("InstanceState")
        self.Uuid = params.get("Uuid")
        self.LatestOperation = params.get("LatestOperation")
        self.LatestOperationState = params.get("LatestOperationState")
        self.LatestOperationRequestId = params.get("LatestOperationRequestId")
        self.IsolatedTime = params.get("IsolatedTime")
        self.CreatedTime = params.get("CreatedTime")
        self.ExpiredTime = params.get("ExpiredTime")
        self.PlatformType = params.get("PlatformType")
        self.Platform = params.get("Platform")
        self.OsName = params.get("OsName")
        self.Zone = params.get("Zone")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.InstanceRestrictState = params.get("InstanceRestrictState")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceChargePrepaid(AbstractModel):
    """Instance billing mode

    """

    def __init__(self):
        r"""
        :param Period: Subscription period in months. Valid values: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36, 48, 60.
        :type Period: int
        :param RenewFlag: Auto-Renewal flag. Valid values: <br><li>NOTIFY_AND_AUTO_RENEW: notify upon expiration and renew automatically <br><li>NOTIFY_AND_MANUAL_RENEW: notify upon expiration but do not renew automatically. You need to manually renew <br><li>DISABLE_NOTIFY_AND_AUTO_RENEW: neither notify upon expiration nor renew automatically<br><br>Default value: NOTIFY_AND_MANUAL_RENEW. If this parameter is specified as `NOTIFY_AND_AUTO_RENEW`, the instance will be automatically renewed monthly if the account balance is sufficient.
        :type RenewFlag: str
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
        


class InstanceDeniedActions(AbstractModel):
    """List of instance operation limits.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
Note: this field may return null, indicating that no valid values can be obtained.
        :type InstanceId: str
        :param DeniedActions: List of operation limits.
        :type DeniedActions: list of DeniedAction
        """
        self.InstanceId = None
        self.DeniedActions = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DeniedActions") is not None:
            self.DeniedActions = []
            for item in params.get("DeniedActions"):
                obj = DeniedAction()
                obj._deserialize(item)
                self.DeniedActions.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstancePrice(AbstractModel):
    """Price information of Lighthouse instances

    """

    def __init__(self):
        r"""
        :param OriginalBundlePrice: Original package unit price.
        :type OriginalBundlePrice: float
        :param OriginalPrice: Original price.
        :type OriginalPrice: float
        :param Discount: Discount.
        :type Discount: int
        :param DiscountPrice: Discounted price.
        :type DiscountPrice: float
        :param Currency: Currency unit. Valid values: `CNY` and `USD`.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type Currency: str
        """
        self.OriginalBundlePrice = None
        self.OriginalPrice = None
        self.Discount = None
        self.DiscountPrice = None
        self.Currency = None


    def _deserialize(self, params):
        self.OriginalBundlePrice = params.get("OriginalBundlePrice")
        self.OriginalPrice = params.get("OriginalPrice")
        self.Discount = params.get("Discount")
        self.DiscountPrice = params.get("DiscountPrice")
        self.Currency = params.get("Currency")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstancePriceDetail(AbstractModel):
    """Instance price details

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
Note: This field may return `null`, indicating that no valid value was found.
        :type InstanceId: str
        :param InstancePrice: Price query information.
Note: This field may return `null`, indicating that no valid value was found.
        :type InstancePrice: :class:`tencentcloud.lighthouse.v20200324.models.InstancePrice`
        :param DiscountDetail: Tiered-pricing details. The information of each tier includes the billable period, discount percentage, total price, discounted price, and discount details (`UserDiscount`, `CommonDiscount` and `FinalDiscount`).
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type DiscountDetail: list of DiscountDetail
        """
        self.InstanceId = None
        self.InstancePrice = None
        self.DiscountDetail = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("InstancePrice") is not None:
            self.InstancePrice = InstancePrice()
            self.InstancePrice._deserialize(params.get("InstancePrice"))
        if params.get("DiscountDetail") is not None:
            self.DiscountDetail = []
            for item in params.get("DiscountDetail"):
                obj = DiscountDetail()
                obj._deserialize(item)
                self.DiscountDetail.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceReturnable(AbstractModel):
    """Whether the instance can be returned.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param IsReturnable: Whether the instance can be returned.
        :type IsReturnable: bool
        :param ReturnFailCode: Error code of instance return failure.
        :type ReturnFailCode: int
        :param ReturnFailMessage: Error message of instance return failure.
        :type ReturnFailMessage: str
        """
        self.InstanceId = None
        self.IsReturnable = None
        self.ReturnFailCode = None
        self.ReturnFailMessage = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.IsReturnable = params.get("IsReturnable")
        self.ReturnFailCode = params.get("ReturnFailCode")
        self.ReturnFailMessage = params.get("ReturnFailMessage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceTrafficPackage(AbstractModel):
    """Instance traffic package details

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param TrafficPackageSet: List of traffic package details.
        :type TrafficPackageSet: list of TrafficPackage
        """
        self.InstanceId = None
        self.TrafficPackageSet = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("TrafficPackageSet") is not None:
            self.TrafficPackageSet = []
            for item in params.get("TrafficPackageSet"):
                obj = TrafficPackage()
                obj._deserialize(item)
                self.TrafficPackageSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InternetAccessible(AbstractModel):
    """This describes the internet accessibility of the instance created by a launch configuration and declares the internet usage billing method of the instance and the maximum bandwidth

    """

    def __init__(self):
        r"""
        :param InternetChargeType: Network billing mode. Valid values:
<li>Bill by traffic package: TRAFFIC_POSTPAID_BY_HOUR</li>
<li>Bill by bandwidth: BANDWIDTH_POSTPAID_BY_HOUR</li>
        :type InternetChargeType: str
        :param InternetMaxBandwidthOut: Public network outbound bandwidth cap in Mbps.
        :type InternetMaxBandwidthOut: int
        :param PublicIpAssigned: Whether to assign a public IP.
        :type PublicIpAssigned: bool
        """
        self.InternetChargeType = None
        self.InternetMaxBandwidthOut = None
        self.PublicIpAssigned = None


    def _deserialize(self, params):
        self.InternetChargeType = params.get("InternetChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.PublicIpAssigned = params.get("PublicIpAssigned")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateInstancesRequest(AbstractModel):
    """IsolateInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: IDs of target instances. You can get the IDs from the `InstanceId` parameter returned by the `DescribeInstances` API. Up to 20 instances can be specified at the same time.
        :type InstanceIds: list of str
        :param IsolateDataDisk: Whether to return data disks mounted on the instance together with the instance. Valid values: 
`TRUE`: Return the mounted data disks at the same time 
`FALSE`: Do not return the mounted data disks at the same time 
Default value: `TRUE`.
        :type IsolateDataDisk: bool
        """
        self.InstanceIds = None
        self.IsolateDataDisk = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.IsolateDataDisk = params.get("IsolateDataDisk")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateInstancesResponse(AbstractModel):
    """IsolateInstances response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class KeyPair(AbstractModel):
    """Key pair information.

    """

    def __init__(self):
        r"""
        :param KeyId: Key pair ID, which is the unique identifier of a key pair.
        :type KeyId: str
        :param KeyName: Key pair name.
        :type KeyName: str
        :param PublicKey: Public key (in plain text) of key pair.
        :type PublicKey: str
        :param AssociatedInstanceIds: List of IDs of instances associated with the key pair.
Note: this field may return null, indicating that no valid values can be obtained.
        :type AssociatedInstanceIds: list of str
        :param CreatedTime: Creation time in the format of YYYY-MM-DDThh:mm:ssZ according to ISO 8601 standard. UTC time is used
Note: this field may return null, indicating that no valid values can be obtained.
        :type CreatedTime: str
        :param PrivateKey: Private key of key pair.
Note: this field may return null, indicating that no valid values can be obtained.
        :type PrivateKey: str
        """
        self.KeyId = None
        self.KeyName = None
        self.PublicKey = None
        self.AssociatedInstanceIds = None
        self.CreatedTime = None
        self.PrivateKey = None


    def _deserialize(self, params):
        self.KeyId = params.get("KeyId")
        self.KeyName = params.get("KeyName")
        self.PublicKey = params.get("PublicKey")
        self.AssociatedInstanceIds = params.get("AssociatedInstanceIds")
        self.CreatedTime = params.get("CreatedTime")
        self.PrivateKey = params.get("PrivateKey")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LoginConfiguration(AbstractModel):
    """Login password information

    """

    def __init__(self):
        r"""
        :param AutoGeneratePassword: <li>`YES`: Random password. In this case, `Password` cannot be specified. </li>
<li>`No`: Custom. `Password` must be specified. </li>
        :type AutoGeneratePassword: str
        :param Password: Instace login password.
For Windows instances, the password must contain 12 to 30 characters of the following types. It cannot start with “/” and cannot include the username.
<li>[a-z]</li>
<li>[A-Z]</li>
<li>[0-9]</li>
<li>[()`~!@#$%^&*-+=_|{}[]:;' <>,.?/]</li>
        :type Password: str
        """
        self.AutoGeneratePassword = None
        self.Password = None


    def _deserialize(self, params):
        self.AutoGeneratePassword = params.get("AutoGeneratePassword")
        self.Password = params.get("Password")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LoginSettings(AbstractModel):
    """Describes login settings of an instance.

    """

    def __init__(self):
        r"""
        :param KeyIds: Key ID list. After a key is associated, you can use it to access the instance. Note: this field may return [], indicating that no valid values can be obtained.
        :type KeyIds: list of str
        """
        self.KeyIds = None


    def _deserialize(self, params):
        self.KeyIds = params.get("KeyIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBlueprintAttributeRequest(AbstractModel):
    """ModifyBlueprintAttribute request structure.

    """

    def __init__(self):
        r"""
        :param BlueprintId: Image ID, which can be obtained from the `BlueprintId` returned by the [DescribeBlueprints](https://intl.cloud.tencent.com/document/product/1207/47689?from_cn_redirect=1) API.
        :type BlueprintId: str
        :param BlueprintName: New image name, which can contain up to 60 characters.
        :type BlueprintName: str
        :param Description: New image description, which can contain up to 60 characters.
        :type Description: str
        """
        self.BlueprintId = None
        self.BlueprintName = None
        self.Description = None


    def _deserialize(self, params):
        self.BlueprintId = params.get("BlueprintId")
        self.BlueprintName = params.get("BlueprintName")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBlueprintAttributeResponse(AbstractModel):
    """ModifyBlueprintAttribute response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBundle(AbstractModel):
    """Changeable packages for the instance.

    """

    def __init__(self):
        r"""
        :param ModifyPrice: Price difference that you need to pay for the new instance package after change.
        :type ModifyPrice: :class:`tencentcloud.lighthouse.v20200324.models.Price`
        :param ModifyBundleState: Package change status. Valid values:
<li>SOLD_OUT: packages are sold out</li>
<li>AVAILABLE: packages can be changed</li>
<li>UNAVAILABLE: packages cannot be changed currently</li>
        :type ModifyBundleState: str
        :param Bundle: Package information.
        :type Bundle: :class:`tencentcloud.lighthouse.v20200324.models.Bundle`
        :param NotSupportModifyMessage: The reason of package changing failure. It’s empty if the package change status is `AVAILABLE`.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type NotSupportModifyMessage: str
        """
        self.ModifyPrice = None
        self.ModifyBundleState = None
        self.Bundle = None
        self.NotSupportModifyMessage = None


    def _deserialize(self, params):
        if params.get("ModifyPrice") is not None:
            self.ModifyPrice = Price()
            self.ModifyPrice._deserialize(params.get("ModifyPrice"))
        self.ModifyBundleState = params.get("ModifyBundleState")
        if params.get("Bundle") is not None:
            self.Bundle = Bundle()
            self.Bundle._deserialize(params.get("Bundle"))
        self.NotSupportModifyMessage = params.get("NotSupportModifyMessage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDisksAttributeRequest(AbstractModel):
    """ModifyDisksAttribute request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        :param DiskName: Cloud disk name.
        :type DiskName: str
        """
        self.DiskIds = None
        self.DiskName = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.DiskName = params.get("DiskName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDisksAttributeResponse(AbstractModel):
    """ModifyDisksAttribute response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDisksRenewFlagRequest(AbstractModel):
    """ModifyDisksRenewFlag request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        :param RenewFlag: Whether Auto-Renewal is enabled 
        :type RenewFlag: str
        """
        self.DiskIds = None
        self.RenewFlag = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.RenewFlag = params.get("RenewFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDisksRenewFlagResponse(AbstractModel):
    """ModifyDisksRenewFlag response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyFirewallRuleDescriptionRequest(AbstractModel):
    """ModifyFirewallRuleDescription request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param FirewallRule: Firewall rule.
        :type FirewallRule: :class:`tencentcloud.lighthouse.v20200324.models.FirewallRule`
        :param FirewallVersion: Current firewall version number. Every time you update the firewall rule version, it will be automatically increased by 1 to prevent the rule from expiring. If it is left empty, conflicts will not be considered.
        :type FirewallVersion: int
        """
        self.InstanceId = None
        self.FirewallRule = None
        self.FirewallVersion = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("FirewallRule") is not None:
            self.FirewallRule = FirewallRule()
            self.FirewallRule._deserialize(params.get("FirewallRule"))
        self.FirewallVersion = params.get("FirewallVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyFirewallRuleDescriptionResponse(AbstractModel):
    """ModifyFirewallRuleDescription response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyFirewallRulesRequest(AbstractModel):
    """ModifyFirewallRules request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param FirewallRules: Firewall rule list.
        :type FirewallRules: list of FirewallRule
        :param FirewallVersion: Current firewall version number. Every time you update the firewall rule version, it will be automatically increased by 1 to prevent the rule from expiring. If it is left empty, conflicts will not be considered.
        :type FirewallVersion: int
        """
        self.InstanceId = None
        self.FirewallRules = None
        self.FirewallVersion = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("FirewallRules") is not None:
            self.FirewallRules = []
            for item in params.get("FirewallRules"):
                obj = FirewallRule()
                obj._deserialize(item)
                self.FirewallRules.append(obj)
        self.FirewallVersion = params.get("FirewallVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyFirewallRulesResponse(AbstractModel):
    """ModifyFirewallRules response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesAttributeRequest(AbstractModel):
    """ModifyInstancesAttribute request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
        :type InstanceIds: list of str
        :param InstanceName: Instance name, which is customizable and can contain up to 60 characters.
        :type InstanceName: str
        """
        self.InstanceIds = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceName = params.get("InstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyInstancesAttributeResponse(AbstractModel):
    """ModifyInstancesAttribute response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesBundleRequest(AbstractModel):
    """ModifyInstancesBundle request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: IDs of target instances. You can get the IDs from the `InstanceId` parameter returned by the `DescribeInstances` API. Up to 15 instances can be specified at the same time.
        :type InstanceIds: list of str
        :param BundleId: ID of bundles to change. You can get the IDs from the `BundleId` returned by the [DescribeBundles](https://intl.cloud.tencent.com/document/api/1207/47575?from_cn_redirect=1).
        :type BundleId: str
        :param AutoVoucher: Whether to use existing vouchers under the current account automatically. Valid values: 
`true`: Deduct from existing vouchers automatically 
`false`: Do not deduct from existing vouchers automatically 
Default value: `false`.
        :type AutoVoucher: bool
        """
        self.InstanceIds = None
        self.BundleId = None
        self.AutoVoucher = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.BundleId = params.get("BundleId")
        self.AutoVoucher = params.get("AutoVoucher")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyInstancesBundleResponse(AbstractModel):
    """ModifyInstancesBundle response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesLoginKeyPairAttributeRequest(AbstractModel):
    """ModifyInstancesLoginKeyPairAttribute request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time.
        :type InstanceIds: list of str
        :param PermitLogin: Whether to allow login with the default key pair. Valid values: YES: yes; NO: no.
        :type PermitLogin: str
        """
        self.InstanceIds = None
        self.PermitLogin = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.PermitLogin = params.get("PermitLogin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyInstancesLoginKeyPairAttributeResponse(AbstractModel):
    """ModifyInstancesLoginKeyPairAttribute response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesRenewFlagRequest(AbstractModel):
    """ModifyInstancesRenewFlag request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
        :type InstanceIds: list of str
        :param RenewFlag: Auto-Renewal flag. Valid values: <br><li>NOTIFY_AND_AUTO_RENEW: notify upon expiration and renew automatically <br><li>NOTIFY_AND_MANUAL_RENEW: notify upon expiration but do not renew automatically <br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW: neither notify upon expiration nor renew automatically <br><br>If this parameter is specified as `NOTIFY_AND_AUTO_RENEW`, the instance will be automatically renewed monthly if the account balance is sufficient.
        :type RenewFlag: str
        """
        self.InstanceIds = None
        self.RenewFlag = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.RenewFlag = params.get("RenewFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyInstancesRenewFlagResponse(AbstractModel):
    """ModifyInstancesRenewFlag response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySnapshotAttributeRequest(AbstractModel):
    """ModifySnapshotAttribute request structure.

    """

    def __init__(self):
        r"""
        :param SnapshotId: Snapshot ID, which can be queried through `DescribeSnapshots`.
        :type SnapshotId: str
        :param SnapshotName: New snapshot name, which can contain up to 60 characters.
        :type SnapshotName: str
        """
        self.SnapshotId = None
        self.SnapshotName = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.SnapshotName = params.get("SnapshotName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySnapshotAttributeResponse(AbstractModel):
    """ModifySnapshotAttribute response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class PolicyDetail(AbstractModel):
    """Discount details.

    """

    def __init__(self):
        r"""
        :param UserDiscount: User discount.
        :type UserDiscount: int
        :param CommonDiscount: Public discount.
        :type CommonDiscount: int
        :param FinalDiscount: Final discount.
        :type FinalDiscount: int
        :param ActivityDiscount: Activity discount. The value `null` indicates no discount.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type ActivityDiscount: float
        :param DiscountType: Discount type.
Valid values: `user` (user discount), `common` (discount displayed on the official website), `activity` (activity discount), `null` (no discount).
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type DiscountType: str
        """
        self.UserDiscount = None
        self.CommonDiscount = None
        self.FinalDiscount = None
        self.ActivityDiscount = None
        self.DiscountType = None


    def _deserialize(self, params):
        self.UserDiscount = params.get("UserDiscount")
        self.CommonDiscount = params.get("CommonDiscount")
        self.FinalDiscount = params.get("FinalDiscount")
        self.ActivityDiscount = params.get("ActivityDiscount")
        self.DiscountType = params.get("DiscountType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Price(AbstractModel):
    """Price information

    """

    def __init__(self):
        r"""
        :param InstancePrice: Instance price.
        :type InstancePrice: :class:`tencentcloud.lighthouse.v20200324.models.InstancePrice`
        """
        self.InstancePrice = None


    def _deserialize(self, params):
        if params.get("InstancePrice") is not None:
            self.InstancePrice = InstancePrice()
            self.InstancePrice._deserialize(params.get("InstancePrice"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RebootInstancesRequest(AbstractModel):
    """RebootInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
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
        


class RebootInstancesResponse(AbstractModel):
    """RebootInstances response structure.

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
    """Region information.

    """

    def __init__(self):
        r"""
        :param Region: Region name, such as `ap-guangzhou`.
        :type Region: str
        :param RegionName: Region description, such as South China (Guangzhou).
        :type RegionName: str
        :param RegionState: Region availability status. Its value can only be `AVAILABLE`.
        :type RegionState: str
        :param IsChinaMainland: Whether the region is in the Chinese mainland
        :type IsChinaMainland: bool
        """
        self.Region = None
        self.RegionName = None
        self.RegionState = None
        self.IsChinaMainland = None


    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionName = params.get("RegionName")
        self.RegionState = params.get("RegionState")
        self.IsChinaMainland = params.get("IsChinaMainland")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewDiskChargePrepaid(AbstractModel):
    """Parameter settings for renewing the monthly subscribed cloud disk

    """

    def __init__(self):
        r"""
        :param Period: Purchase duration.
        :type Period: int
        :param RenewFlag: Whether Auto-Renewal is enabled 
        :type RenewFlag: str
        :param TimeUnit: Duration unit. Default value: "m" (month).
        :type TimeUnit: str
        :param CurInstanceDeadline: Expiration time of the current instance.
        :type CurInstanceDeadline: str
        """
        self.Period = None
        self.RenewFlag = None
        self.TimeUnit = None
        self.CurInstanceDeadline = None


    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")
        self.TimeUnit = params.get("TimeUnit")
        self.CurInstanceDeadline = params.get("CurInstanceDeadline")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetAttachCcnRequest(AbstractModel):
    """ResetAttachCcn request structure.

    """

    def __init__(self):
        r"""
        :param CcnId: CCN instance ID.
        :type CcnId: str
        """
        self.CcnId = None


    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetAttachCcnResponse(AbstractModel):
    """ResetAttachCcn response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetInstanceBlueprint(AbstractModel):
    """Image reset information

    """

    def __init__(self):
        r"""
        :param BlueprintInfo: Image details
        :type BlueprintInfo: :class:`tencentcloud.lighthouse.v20200324.models.Blueprint`
        :param IsResettable: Whether the image can be reset as the target image
        :type IsResettable: bool
        :param NonResettableMessage: Non-Resettable flag. If the image is resettable, it will be ""
        :type NonResettableMessage: str
        """
        self.BlueprintInfo = None
        self.IsResettable = None
        self.NonResettableMessage = None


    def _deserialize(self, params):
        if params.get("BlueprintInfo") is not None:
            self.BlueprintInfo = Blueprint()
            self.BlueprintInfo._deserialize(params.get("BlueprintInfo"))
        self.IsResettable = params.get("IsResettable")
        self.NonResettableMessage = params.get("NonResettableMessage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetInstanceRequest(AbstractModel):
    """ResetInstance request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which can be obtained from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
        :type InstanceId: str
        :param BlueprintId: Image ID, which can be obtained from the `BlueprintId` returned by the [DescribeBlueprints](https://intl.cloud.tencent.com/document/product/1207/47689?from_cn_redirect=1) API.
        :type BlueprintId: str
        """
        self.InstanceId = None
        self.BlueprintId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.BlueprintId = params.get("BlueprintId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetInstanceResponse(AbstractModel):
    """ResetInstance response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetInstancesPasswordRequest(AbstractModel):
    """ResetInstancesPassword request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time.
        :type InstanceIds: list of str
        :param Password: Login password of the instance(s). The password requirements vary among different operating systems:
The password of a `LINUX_UNIX` instance must contain 8–30 characters (above 12 characters preferably) in at least three of the following types and cannot begin with "/": <br><li>Lowercase letters: [a–z]<br><li>Uppercase letters: [A–Z]<br><li>Digits: 0–9<br><li>Special symbols: ()\`~!@#$%^&\*-+=\_|{}[]:;'<>,.?/</li>
The password of a `WINDOWS` instance must contain 12–30 characters in at least three of the following types and cannot begin with "/" or include the username: <br><li>Lowercase letters: [a–z]<br><li>Uppercase letters: [A–Z]<br><li>Digits: 0–9<br><li>Special symbols: ()\`~!@#$%^&\*-+=\_|{}[]:;' <>,.?/<br><li>If both `LINUX_UNIX` and `WINDOWS` instances exist, the requirements for password complexity of `WINDOWS` instances shall prevail.
        :type Password: str
        :param UserName: OS username of the instance for which you want to reset the password, which can contain up to 64 characters.
        :type UserName: str
        """
        self.InstanceIds = None
        self.Password = None
        self.UserName = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Password = params.get("Password")
        self.UserName = params.get("UserName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetInstancesPasswordResponse(AbstractModel):
    """ResetInstancesPassword response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Scene(AbstractModel):
    """Scene information

    """

    def __init__(self):
        r"""
        :param SceneId: Scene ID
        :type SceneId: str
        :param DisplayName: Display name of the scene
        :type DisplayName: str
        :param Description: Scene description
        :type Description: str
        """
        self.SceneId = None
        self.DisplayName = None
        self.Description = None


    def _deserialize(self, params):
        self.SceneId = params.get("SceneId")
        self.DisplayName = params.get("DisplayName")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SceneInfo(AbstractModel):
    """Scene information

    """

    def __init__(self):
        r"""
        :param SceneId: Scene ID
        :type SceneId: str
        :param DisplayName: Display name of the scene
        :type DisplayName: str
        :param Description: Scene description
        :type Description: str
        """
        self.SceneId = None
        self.DisplayName = None
        self.Description = None


    def _deserialize(self, params):
        self.SceneId = params.get("SceneId")
        self.DisplayName = params.get("DisplayName")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Snapshot(AbstractModel):
    """Snapshot information.

    """

    def __init__(self):
        r"""
        :param SnapshotId: Snapshot ID.
        :type SnapshotId: str
        :param DiskUsage: Type of the disk for which the snapshot is created. Valid values: <li>SYSTEM_DISK: system disk</li>
        :type DiskUsage: str
        :param DiskId: ID of the disk for which the snapshot is created.
        :type DiskId: str
        :param DiskSize: Size of the disk in GB for which the snapshot is created.
        :type DiskSize: int
        :param SnapshotName: Snapshot name, which is a custom snapshot alias.
        :type SnapshotName: str
        :param SnapshotState: Snapshot status. Valid values:
<li>NORMAL: normal </li>
<li>CREATING: creating</li>
<li>ROLLBACKING: rolling back</li>
        :type SnapshotState: str
        :param Percent: Snapshot creation or rollback progress in percentage. After success, the value of this field will become 100.
        :type Percent: int
        :param LatestOperation: Last snapshot operation. It is recorded only during snapshot creation and rollback.
Example values: CreateInstanceSnapshot, RollbackInstanceSnapshot.
Note: this field may return null, indicating that no valid values can be obtained.
        :type LatestOperation: str
        :param LatestOperationState: Last snapshot operation status. It is recorded only during snapshot creation and rollback.
Valid values:
<li>SUCCESS: operation succeeded</li>
<li>OPERATING: the operation is being executed</li>
<li>FAILED: operation failed</li>
Note: this field may return null, indicating that no valid values can be obtained.
        :type LatestOperationState: str
        :param LatestOperationRequestId: Unique request ID for the last snapshot operation. It is recorded only during snapshot creation and rollback.
Note: this field may return null, indicating that no valid values can be obtained.
        :type LatestOperationRequestId: str
        :param CreatedTime: Snapshot creation time.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type CreatedTime: str
        """
        self.SnapshotId = None
        self.DiskUsage = None
        self.DiskId = None
        self.DiskSize = None
        self.SnapshotName = None
        self.SnapshotState = None
        self.Percent = None
        self.LatestOperation = None
        self.LatestOperationState = None
        self.LatestOperationRequestId = None
        self.CreatedTime = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.DiskUsage = params.get("DiskUsage")
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")
        self.SnapshotName = params.get("SnapshotName")
        self.SnapshotState = params.get("SnapshotState")
        self.Percent = params.get("Percent")
        self.LatestOperation = params.get("LatestOperation")
        self.LatestOperationState = params.get("LatestOperationState")
        self.LatestOperationRequestId = params.get("LatestOperationRequestId")
        self.CreatedTime = params.get("CreatedTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SnapshotDeniedActions(AbstractModel):
    """List of snapshot operation limits.

    """

    def __init__(self):
        r"""
        :param SnapshotId: Snapshot ID.
        :type SnapshotId: str
        :param DeniedActions: List of operation limits.
        :type DeniedActions: list of DeniedAction
        """
        self.SnapshotId = None
        self.DeniedActions = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        if params.get("DeniedActions") is not None:
            self.DeniedActions = []
            for item in params.get("DeniedActions"):
                obj = DeniedAction()
                obj._deserialize(item)
                self.DeniedActions.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Software(AbstractModel):
    """Image software information.

    """

    def __init__(self):
        r"""
        :param Name: Software name.
        :type Name: str
        :param Version: Software version.
        :type Version: str
        :param ImageUrl: Software picture URL.
        :type ImageUrl: str
        :param InstallDir: Software installation directory.
        :type InstallDir: str
        :param DetailSet: List of software details.
        :type DetailSet: list of SoftwareDetail
        """
        self.Name = None
        self.Version = None
        self.ImageUrl = None
        self.InstallDir = None
        self.DetailSet = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Version = params.get("Version")
        self.ImageUrl = params.get("ImageUrl")
        self.InstallDir = params.get("InstallDir")
        if params.get("DetailSet") is not None:
            self.DetailSet = []
            for item in params.get("DetailSet"):
                obj = SoftwareDetail()
                obj._deserialize(item)
                self.DetailSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SoftwareDetail(AbstractModel):
    """Image software details.

    """

    def __init__(self):
        r"""
        :param Key: Unique detail key
        :type Key: str
        :param Title: Detail title.
        :type Title: str
        :param Value: Detail value.
        :type Value: str
        """
        self.Key = None
        self.Title = None
        self.Value = None


    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Title = params.get("Title")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartInstancesRequest(AbstractModel):
    """StartInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
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
        


class StartInstancesResponse(AbstractModel):
    """StartInstances response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StopInstancesRequest(AbstractModel):
    """StopInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list. Each request can contain up to 100 instances at a time. You can get an instance ID from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
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
        


class StopInstancesResponse(AbstractModel):
    """StopInstances response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SystemDisk(AbstractModel):
    """Information on the block device where the operating system is installed, namely the system disk.

    """

    def __init__(self):
        r"""
        :param DiskType: System disk type.
Valid values: 
<li> LOCAL_BASIC: local disk</li><li> LOCAL_SSD: local SSD disk</li><li> CLOUD_BASIC: HDD cloud disk</li><li> CLOUD_SSD: SSD cloud disk</li><li> CLOUD_PREMIUM: Premium Cloud Storage</li>
        :type DiskType: str
        :param DiskSize: System disk size in GB.
        :type DiskSize: int
        :param DiskId: System disk ID.
Note: this field may return null, indicating that no valid values can be obtained.
        :type DiskId: str
        """
        self.DiskType = None
        self.DiskSize = None
        self.DiskId = None


    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.DiskSize = params.get("DiskSize")
        self.DiskId = params.get("DiskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Tag(AbstractModel):
    """Information on tags

    """

    def __init__(self):
        r"""
        :param Key: Tag key
        :type Key: str
        :param Value: Tag value
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
        


class TerminateDisksRequest(AbstractModel):
    """TerminateDisks request structure.

    """

    def __init__(self):
        r"""
        :param DiskIds: List of cloud disk IDs.
        :type DiskIds: list of str
        """
        self.DiskIds = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateDisksResponse(AbstractModel):
    """TerminateDisks response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class TerminateInstancesRequest(AbstractModel):
    """TerminateInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list, which can be obtained from the `InstanceId` returned by the [DescribeInstances](https://intl.cloud.tencent.com/document/api/1207/47573?from_cn_redirect=1) API.
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
        


class TerminateInstancesResponse(AbstractModel):
    """TerminateInstances response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class TotalPrice(AbstractModel):
    """Total price information

    """

    def __init__(self):
        r"""
        :param OriginalPrice: Total original price
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type OriginalPrice: float
        :param DiscountPrice: Total discounted price
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type DiscountPrice: float
        """
        self.OriginalPrice = None
        self.DiscountPrice = None


    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.DiscountPrice = params.get("DiscountPrice")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrafficPackage(AbstractModel):
    """Traffic package details.

    """

    def __init__(self):
        r"""
        :param TrafficPackageId: Traffic package ID.
        :type TrafficPackageId: str
        :param TrafficUsed: Used traffic in bytes during traffic package validity period.
        :type TrafficUsed: int
        :param TrafficPackageTotal: Total traffic in bytes during traffic package validity period.
        :type TrafficPackageTotal: int
        :param TrafficPackageRemaining: Remaining traffic in bytes during traffic package validity period.
        :type TrafficPackageRemaining: int
        :param TrafficOverflow: Traffic exceeding package amount in bytes during traffic package validity period.
        :type TrafficOverflow: int
        :param StartTime: Start time of traffic package validity period according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: this field may return null, indicating that no valid values can be obtained.
        :type StartTime: str
        :param EndTime: End time of traffic package validity period according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: this field may return null, indicating that no valid values can be obtained.
        :type EndTime: str
        :param Deadline: Traffic package expiration time according to ISO 8601 standard. UTC time is used. 
Format: YYYY-MM-DDThh:mm:ssZ.
Note: this field may return null, indicating that no valid values can be obtained.
        :type Deadline: str
        :param Status: Traffic package status:
<li>NETWORK_NORMAL: normal</li>
<li>OVERDUE_NETWORK_DISABLED: the network is disconnected due to overdue payments</li>
        :type Status: str
        """
        self.TrafficPackageId = None
        self.TrafficUsed = None
        self.TrafficPackageTotal = None
        self.TrafficPackageRemaining = None
        self.TrafficOverflow = None
        self.StartTime = None
        self.EndTime = None
        self.Deadline = None
        self.Status = None


    def _deserialize(self, params):
        self.TrafficPackageId = params.get("TrafficPackageId")
        self.TrafficUsed = params.get("TrafficUsed")
        self.TrafficPackageTotal = params.get("TrafficPackageTotal")
        self.TrafficPackageRemaining = params.get("TrafficPackageRemaining")
        self.TrafficOverflow = params.get("TrafficOverflow")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Deadline = params.get("Deadline")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ZoneInfo(AbstractModel):
    """AZ details

    """

    def __init__(self):
        r"""
        :param Zone: AZ
        :type Zone: str
        :param ZoneName: Chinese name of AZ
        :type ZoneName: str
        :param InstanceDisplayLabel: AZ tags on instance purchase page
        :type InstanceDisplayLabel: str
        """
        self.Zone = None
        self.ZoneName = None
        self.InstanceDisplayLabel = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneName = params.get("ZoneName")
        self.InstanceDisplayLabel = params.get("InstanceDisplayLabel")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        