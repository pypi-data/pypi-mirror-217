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


class Alias(AbstractModel):
    """Version alias of function

    """

    def __init__(self):
        r"""
        :param FunctionVersion: Master version pointed to by the alias
        :type FunctionVersion: str
        :param Name: Alias name
        :type Name: str
        :param RoutingConfig: Routing information of alias
Note: this field may return null, indicating that no valid values can be obtained.
        :type RoutingConfig: :class:`tencentcloud.scf.v20180416.models.RoutingConfig`
        :param Description: Description
Note: this field may return null, indicating that no valid values can be obtained.
        :type Description: str
        :param AddTime: Creation time
Note: this field may return null, indicating that no valid values can be obtained.
        :type AddTime: str
        :param ModTime: Update time
Note: this field may return null, indicating that no valid values can be obtained.
        :type ModTime: str
        """
        self.FunctionVersion = None
        self.Name = None
        self.RoutingConfig = None
        self.Description = None
        self.AddTime = None
        self.ModTime = None


    def _deserialize(self, params):
        self.FunctionVersion = params.get("FunctionVersion")
        self.Name = params.get("Name")
        if params.get("RoutingConfig") is not None:
            self.RoutingConfig = RoutingConfig()
            self.RoutingConfig._deserialize(params.get("RoutingConfig"))
        self.Description = params.get("Description")
        self.AddTime = params.get("AddTime")
        self.ModTime = params.get("ModTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AsyncEvent(AbstractModel):
    """Async event

    """

    def __init__(self):
        r"""
        :param InvokeRequestId: Invocation request ID
        :type InvokeRequestId: str
        :param InvokeType: Invocation type
        :type InvokeType: str
        :param Qualifier: Function version
        :type Qualifier: str
        :param Status: Event status. Values: `RUNNING`; `FINISHED` (invoked successfully); `ABORTED` (invocation ended); `FAILED` (invocation failed)
        :type Status: str
        :param StartTime: Invocation start time in the format of "%Y-%m-%d %H:%M:%S.%f"
        :type StartTime: str
        :param EndTime: Invocation end time in the format of "%Y-%m-%d %H:%M:%S.%f"
        :type EndTime: str
        """
        self.InvokeRequestId = None
        self.InvokeType = None
        self.Qualifier = None
        self.Status = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.InvokeRequestId = params.get("InvokeRequestId")
        self.InvokeType = params.get("InvokeType")
        self.Qualifier = params.get("Qualifier")
        self.Status = params.get("Status")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AsyncEventStatus(AbstractModel):
    """Async event status

    """

    def __init__(self):
        r"""
        :param Status: Async event status. Values: `RUNNING` (running); `FINISHED` (invoked successfully); `ABORTED` (invocation ended); `FAILED` (invocation failed).
        :type Status: str
        :param StatusCode: Request status code
        :type StatusCode: int
        :param InvokeRequestId: Async execution request ID
        :type InvokeRequestId: str
        """
        self.Status = None
        self.StatusCode = None
        self.InvokeRequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.StatusCode = params.get("StatusCode")
        self.InvokeRequestId = params.get("InvokeRequestId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AsyncTriggerConfig(AbstractModel):
    """Async retry configuration details of function

    """

    def __init__(self):
        r"""
        :param RetryConfig: Async retry configuration of function upon user error
        :type RetryConfig: list of RetryConfig
        :param MsgTTL: Message retention period
        :type MsgTTL: int
        """
        self.RetryConfig = None
        self.MsgTTL = None


    def _deserialize(self, params):
        if params.get("RetryConfig") is not None:
            self.RetryConfig = []
            for item in params.get("RetryConfig"):
                obj = RetryConfig()
                obj._deserialize(item)
                self.RetryConfig.append(obj)
        self.MsgTTL = params.get("MsgTTL")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Code(AbstractModel):
    """Function code

    """

    def __init__(self):
        r"""
        :param CosBucketName: Object bucket name (enter the custom part of the bucket name without `-appid`)
        :type CosBucketName: str
        :param CosObjectName: File path of code package stored in COS, which should start with “/”
        :type CosObjectName: str
        :param ZipFile: This parameter contains a .zip file (up to 50 MB) of the function code file and its dependencies. When this API is used, the content of the .zip file needs to be Base64-encoded
        :type ZipFile: str
        :param CosBucketRegion: COS region. For Beijing regions, you need to import `ap-beijing`. For Beijing Region 1, you need to input `ap-beijing-1`. For other regions, no import is required.
        :type CosBucketRegion: str
        :param DemoId: `DemoId` is required if Demo is used for the creation.
        :type DemoId: str
        :param TempCosObjectName: `TempCosObjectName` is required if TempCos is used for the creation.
        :type TempCosObjectName: str
        :param GitUrl: (Disused) Git address
        :type GitUrl: str
        :param GitUserName: (Disused) Git username
        :type GitUserName: str
        :param GitPassword: (Disused) Git password
        :type GitPassword: str
        :param GitPasswordSecret: (Disused) Git password after encryption. It’s usually not required.
        :type GitPasswordSecret: str
        :param GitBranch: (Disused) Git branch
        :type GitBranch: str
        :param GitDirectory: (Disused) Directory to the codes in the Git repository. 
        :type GitDirectory: str
        :param GitCommitId: (Disused) 
        :type GitCommitId: str
        :param GitUserNameSecret: (Disused) Git username after encryption. It’s usually not required.
        :type GitUserNameSecret: str
        :param ImageConfig: TCR image configurations
        :type ImageConfig: :class:`tencentcloud.scf.v20180416.models.ImageConfig`
        """
        self.CosBucketName = None
        self.CosObjectName = None
        self.ZipFile = None
        self.CosBucketRegion = None
        self.DemoId = None
        self.TempCosObjectName = None
        self.GitUrl = None
        self.GitUserName = None
        self.GitPassword = None
        self.GitPasswordSecret = None
        self.GitBranch = None
        self.GitDirectory = None
        self.GitCommitId = None
        self.GitUserNameSecret = None
        self.ImageConfig = None


    def _deserialize(self, params):
        self.CosBucketName = params.get("CosBucketName")
        self.CosObjectName = params.get("CosObjectName")
        self.ZipFile = params.get("ZipFile")
        self.CosBucketRegion = params.get("CosBucketRegion")
        self.DemoId = params.get("DemoId")
        self.TempCosObjectName = params.get("TempCosObjectName")
        self.GitUrl = params.get("GitUrl")
        self.GitUserName = params.get("GitUserName")
        self.GitPassword = params.get("GitPassword")
        self.GitPasswordSecret = params.get("GitPasswordSecret")
        self.GitBranch = params.get("GitBranch")
        self.GitDirectory = params.get("GitDirectory")
        self.GitCommitId = params.get("GitCommitId")
        self.GitUserNameSecret = params.get("GitUserNameSecret")
        if params.get("ImageConfig") is not None:
            self.ImageConfig = ImageConfig()
            self.ImageConfig._deserialize(params.get("ImageConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CopyFunctionRequest(AbstractModel):
    """CopyFunction request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Name of the function to be replicated
        :type FunctionName: str
        :param NewFunctionName: Name of the new function
        :type NewFunctionName: str
        :param Namespace: Namespace of the function to be replicated. The default value is `default`.
        :type Namespace: str
        :param TargetNamespace: Namespace of the replicated function. The default value is default.
        :type TargetNamespace: str
        :param Description: Description of the new function
        :type Description: str
        :param TargetRegion: Region of the target of the function replication. If the value is not set, the current region is used by default.
        :type TargetRegion: str
        :param Override: It specifies whether to replace the function with the same name in the target namespace. The default option is `FALSE`.
(Note: The `TRUE` option results in deletion of the function in the target namespace. Please operate with caution.)
TRUE: Replaces the function.
FALSE: Does not replace the function.
        :type Override: bool
        :param CopyConfiguration: It specifies whether to replicate the function attributes, including environment variables, memory, timeout, function description, labels, and VPC. The default value is `TRUE`.
TRUE: Replicates the function configuration.
FALSE: Does not replicate the function configuration.
        :type CopyConfiguration: bool
        """
        self.FunctionName = None
        self.NewFunctionName = None
        self.Namespace = None
        self.TargetNamespace = None
        self.Description = None
        self.TargetRegion = None
        self.Override = None
        self.CopyConfiguration = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.NewFunctionName = params.get("NewFunctionName")
        self.Namespace = params.get("Namespace")
        self.TargetNamespace = params.get("TargetNamespace")
        self.Description = params.get("Description")
        self.TargetRegion = params.get("TargetRegion")
        self.Override = params.get("Override")
        self.CopyConfiguration = params.get("CopyConfiguration")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CopyFunctionResponse(AbstractModel):
    """CopyFunction response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateAliasRequest(AbstractModel):
    """CreateAlias request structure.

    """

    def __init__(self):
        r"""
        :param Name: Alias name, which must be unique in the function, can contain 1 to 64 letters, digits, `_`, and `-`, and must begin with a letter
        :type Name: str
        :param FunctionName: Function name
        :type FunctionName: str
        :param FunctionVersion: Master version pointed to by the alias
        :type FunctionVersion: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param RoutingConfig: Request routing configuration of alias
        :type RoutingConfig: :class:`tencentcloud.scf.v20180416.models.RoutingConfig`
        :param Description: Alias description
        :type Description: str
        """
        self.Name = None
        self.FunctionName = None
        self.FunctionVersion = None
        self.Namespace = None
        self.RoutingConfig = None
        self.Description = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.FunctionName = params.get("FunctionName")
        self.FunctionVersion = params.get("FunctionVersion")
        self.Namespace = params.get("Namespace")
        if params.get("RoutingConfig") is not None:
            self.RoutingConfig = RoutingConfig()
            self.RoutingConfig._deserialize(params.get("RoutingConfig"))
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAliasResponse(AbstractModel):
    """CreateAlias response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateNamespaceRequest(AbstractModel):
    """CreateNamespace request structure.

    """

    def __init__(self):
        r"""
        :param Namespace: Namespace name
        :type Namespace: str
        :param Description: Namespace description
        :type Description: str
        """
        self.Namespace = None
        self.Description = None


    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateNamespaceResponse(AbstractModel):
    """CreateNamespace response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateTriggerRequest(AbstractModel):
    """CreateTrigger request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Name of the function bound to the new trigger
        :type FunctionName: str
        :param TriggerName: Name of a new trigger. For a timer trigger, the name can contain up to 100 letters, digits, dashes, and underscores; for a COS trigger, it should be an access domain name of the corresponding COS bucket applicable to the XML API (e.g., 5401-5ff414-12345.cos.ap-shanghai.myqcloud.com); for other triggers, please see the descriptions of parameters bound to the specific trigger.
        :type TriggerName: str
        :param Type: Type of trigger. Values: `cos`, `cmq`, `timer`, `ckafka` and `apigw`. To create a CLS trigger, please refer to [Creating Shipping Task (SCF)](https://intl.cloud.tencent.com/document/product/614/61096?from_cn_redirect=1).
        :type Type: str
        :param TriggerDesc: For parameters of triggers, see [Trigger Description](https://intl.cloud.tencent.com/document/product/583/39901?from_cn_redirect=1)
        :type TriggerDesc: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param Qualifier: Function version. It defaults to `$LATEST`. It’s recommended to use `[$DEFAULT](https://intl.cloud.tencent.com/document/product/583/36149?from_cn_redirect=1#.E9.BB.98.E8.AE.A4.E5.88.AB.E5.90.8D)` for canary release.
        :type Qualifier: str
        :param Enable: Initial enabling status of the trigger. `OPEN` indicates enabled, and `CLOSE` indicates disabled.
        :type Enable: str
        :param CustomArgument: Custom argument, supporting only the timer trigger.
        :type CustomArgument: str
        """
        self.FunctionName = None
        self.TriggerName = None
        self.Type = None
        self.TriggerDesc = None
        self.Namespace = None
        self.Qualifier = None
        self.Enable = None
        self.CustomArgument = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.TriggerName = params.get("TriggerName")
        self.Type = params.get("Type")
        self.TriggerDesc = params.get("TriggerDesc")
        self.Namespace = params.get("Namespace")
        self.Qualifier = params.get("Qualifier")
        self.Enable = params.get("Enable")
        self.CustomArgument = params.get("CustomArgument")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTriggerResponse(AbstractModel):
    """CreateTrigger response structure.

    """

    def __init__(self):
        r"""
        :param TriggerInfo: Trigger information
        :type TriggerInfo: :class:`tencentcloud.scf.v20180416.models.Trigger`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TriggerInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TriggerInfo") is not None:
            self.TriggerInfo = Trigger()
            self.TriggerInfo._deserialize(params.get("TriggerInfo"))
        self.RequestId = params.get("RequestId")


class DeleteAliasRequest(AbstractModel):
    """DeleteAlias request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Name: Alias name
        :type Name: str
        :param Namespace: Function namespace
        :type Namespace: str
        """
        self.FunctionName = None
        self.Name = None
        self.Namespace = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Name = params.get("Name")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAliasResponse(AbstractModel):
    """DeleteAlias response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteFunctionRequest(AbstractModel):
    """DeleteFunction request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Name of the function to be deleted
        :type FunctionName: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param Qualifier: ID of the version to delete. All versions are deleted if it’s left empty.
        :type Qualifier: str
        """
        self.FunctionName = None
        self.Namespace = None
        self.Qualifier = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        self.Qualifier = params.get("Qualifier")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteFunctionResponse(AbstractModel):
    """DeleteFunction response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLayerVersionRequest(AbstractModel):
    """DeleteLayerVersion request structure.

    """

    def __init__(self):
        r"""
        :param LayerName: Layer name
        :type LayerName: str
        :param LayerVersion: Version number
        :type LayerVersion: int
        """
        self.LayerName = None
        self.LayerVersion = None


    def _deserialize(self, params):
        self.LayerName = params.get("LayerName")
        self.LayerVersion = params.get("LayerVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteLayerVersionResponse(AbstractModel):
    """DeleteLayerVersion response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNamespaceRequest(AbstractModel):
    """DeleteNamespace request structure.

    """

    def __init__(self):
        r"""
        :param Namespace: Namespace name
        :type Namespace: str
        """
        self.Namespace = None


    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteNamespaceResponse(AbstractModel):
    """DeleteNamespace response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteProvisionedConcurrencyConfigRequest(AbstractModel):
    """DeleteProvisionedConcurrencyConfig request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Name of the function for which to delete the provisioned concurrency
        :type FunctionName: str
        :param Qualifier: Function version number
        :type Qualifier: str
        :param Namespace: Function namespace. Default value: `default`
        :type Namespace: str
        """
        self.FunctionName = None
        self.Qualifier = None
        self.Namespace = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Qualifier = params.get("Qualifier")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteProvisionedConcurrencyConfigResponse(AbstractModel):
    """DeleteProvisionedConcurrencyConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteReservedConcurrencyConfigRequest(AbstractModel):
    """DeleteReservedConcurrencyConfig request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Specifies the function of which you want to delete the reserved quota
        :type FunctionName: str
        :param Namespace: Function namespace. Default value: `default`
        :type Namespace: str
        """
        self.FunctionName = None
        self.Namespace = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteReservedConcurrencyConfigResponse(AbstractModel):
    """DeleteReservedConcurrencyConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTriggerRequest(AbstractModel):
    """DeleteTrigger request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param TriggerName: Name of the trigger to be deleted
        :type TriggerName: str
        :param Type: Type of the trigger to be deleted. Currently, COS, CMQ, timer, and ckafka triggers are supported.
        :type Type: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param TriggerDesc: This field is required if a COS trigger is to be deleted. It stores the data {"event":"cos:ObjectCreated:*"} in the JSON format. The data content of this field is in the same format as that of SetTrigger. This field is optional if a scheduled trigger or CMQ trigger is to be deleted.
        :type TriggerDesc: str
        :param Qualifier: Function version. It defaults to `$LATEST`. It’s recommended to use `[$DEFAULT](https://intl.cloud.tencent.com/document/product/583/36149?from_cn_redirect=1#.E9.BB.98.E8.AE.A4.E5.88.AB.E5.90.8D)` for canary release.
        :type Qualifier: str
        """
        self.FunctionName = None
        self.TriggerName = None
        self.Type = None
        self.Namespace = None
        self.TriggerDesc = None
        self.Qualifier = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.TriggerName = params.get("TriggerName")
        self.Type = params.get("Type")
        self.Namespace = params.get("Namespace")
        self.TriggerDesc = params.get("TriggerDesc")
        self.Qualifier = params.get("Qualifier")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTriggerResponse(AbstractModel):
    """DeleteTrigger response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Filter(AbstractModel):
    """Key-value pair filters for conditional filtering queries, such as filtering ID, name, and status.
    If more than one filter exists, the logical relationship between these filters is `AND`.
    If multiple values exist in one filter, the logical relationship between these values under the same filter is `OR`.

    """

    def __init__(self):
        r"""
        :param Name: Fields to be filtered. Up to 10 conditions allowed.
Values of `Name`: `VpcId`, `SubnetId`, `ClsTopicId`, `ClsLogsetId`, `Role`, `CfsId`, `CfsMountInsId`, `Eip`. Values limit: 1.
Name options: Status, Runtime, FunctionType, PublicNetStatus, AsyncRunEnable, TraceEnable. Values limit: 20.
When `Name` is `Runtime`, `CustomImage` refers to the image type function 
        :type Name: str
        :param Values: Filter values of the field
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
        


class Function(AbstractModel):
    """Function list

    """

    def __init__(self):
        r"""
        :param ModTime: Modification time
        :type ModTime: str
        :param AddTime: Creation time
        :type AddTime: str
        :param Runtime: Running
        :type Runtime: str
        :param FunctionName: Function name
        :type FunctionName: str
        :param FunctionId: Function ID
        :type FunctionId: str
        :param Namespace: Namespace
        :type Namespace: str
        :param Status: Function status. For valid values and status change process, please see [here](https://intl.cloud.tencent.com/document/product/583/47175?from_cn_redirect=1)
        :type Status: str
        :param StatusDesc: Function status details
        :type StatusDesc: str
        :param Description: Function description
        :type Description: str
        :param Tags: Function tag
        :type Tags: list of Tag
        :param Type: Function type. The value is `HTTP` or `Event`.
        :type Type: str
        :param StatusReasons: Cause of function failure
        :type StatusReasons: list of StatusReason
        :param TotalProvisionedConcurrencyMem: Sum of provisioned concurrence memory for all function versions
Note: this field may return null, indicating that no valid values can be obtained.
        :type TotalProvisionedConcurrencyMem: int
        :param ReservedConcurrencyMem: Reserved memory for function concurrence
Note: this field may return null, indicating that no valid values can be obtained.
        :type ReservedConcurrencyMem: int
        :param AsyncRunEnable: Asynchronization attribute of the function. Values: `TRUE` and `FALSE`.
        :type AsyncRunEnable: str
        :param TraceEnable: Whether to enable call tracing for ansynchronized functions. Values: `TRUE` and `FALSE`.
        :type TraceEnable: str
        """
        self.ModTime = None
        self.AddTime = None
        self.Runtime = None
        self.FunctionName = None
        self.FunctionId = None
        self.Namespace = None
        self.Status = None
        self.StatusDesc = None
        self.Description = None
        self.Tags = None
        self.Type = None
        self.StatusReasons = None
        self.TotalProvisionedConcurrencyMem = None
        self.ReservedConcurrencyMem = None
        self.AsyncRunEnable = None
        self.TraceEnable = None


    def _deserialize(self, params):
        self.ModTime = params.get("ModTime")
        self.AddTime = params.get("AddTime")
        self.Runtime = params.get("Runtime")
        self.FunctionName = params.get("FunctionName")
        self.FunctionId = params.get("FunctionId")
        self.Namespace = params.get("Namespace")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.Description = params.get("Description")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.Type = params.get("Type")
        if params.get("StatusReasons") is not None:
            self.StatusReasons = []
            for item in params.get("StatusReasons"):
                obj = StatusReason()
                obj._deserialize(item)
                self.StatusReasons.append(obj)
        self.TotalProvisionedConcurrencyMem = params.get("TotalProvisionedConcurrencyMem")
        self.ReservedConcurrencyMem = params.get("ReservedConcurrencyMem")
        self.AsyncRunEnable = params.get("AsyncRunEnable")
        self.TraceEnable = params.get("TraceEnable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FunctionLog(AbstractModel):
    """Log information

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param RetMsg: Return value after the function is executed
        :type RetMsg: str
        :param RequestId: RequestId corresponding to the executed function
        :type RequestId: str
        :param StartTime: Start time of the function execution
        :type StartTime: str
        :param RetCode: Function execution result. `0` indicates successful execution and other values indicate failure.
        :type RetCode: int
        :param InvokeFinished: It specifies whether the function invocation is finished. `1` indicates execution completion and other values indicate that exceptions occurred during the invocation.
        :type InvokeFinished: int
        :param Duration: Duration of the function execution. The unit is millisecond (ms).
        :type Duration: float
        :param BillDuration: Function billing duration. The unit is millisecond (ms). The value is rounded up to a multiple of 100 ms.
        :type BillDuration: int
        :param MemUsage: Actual memory size used during the function execution. The unit is byte.
        :type MemUsage: int
        :param Log: Function execution logs
        :type Log: str
        :param Level: Log level
        :type Level: str
        :param Source: Log source
        :type Source: str
        :param RetryNum: Number of retries
        :type RetryNum: int
        """
        self.FunctionName = None
        self.RetMsg = None
        self.RequestId = None
        self.StartTime = None
        self.RetCode = None
        self.InvokeFinished = None
        self.Duration = None
        self.BillDuration = None
        self.MemUsage = None
        self.Log = None
        self.Level = None
        self.Source = None
        self.RetryNum = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.RetMsg = params.get("RetMsg")
        self.RequestId = params.get("RequestId")
        self.StartTime = params.get("StartTime")
        self.RetCode = params.get("RetCode")
        self.InvokeFinished = params.get("InvokeFinished")
        self.Duration = params.get("Duration")
        self.BillDuration = params.get("BillDuration")
        self.MemUsage = params.get("MemUsage")
        self.Log = params.get("Log")
        self.Level = params.get("Level")
        self.Source = params.get("Source")
        self.RetryNum = params.get("RetryNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FunctionVersion(AbstractModel):
    """Function version information

    """

    def __init__(self):
        r"""
        :param Version: Function version name
        :type Version: str
        :param Description: Version description
Note: This field may return null, indicating that no valid values is found.
        :type Description: str
        :param AddTime: The creation time
Note: This field may return null, indicating that no valid value was found.
        :type AddTime: str
        :param ModTime: Update time
Note: This field may return null, indicating that no valid value was found.
        :type ModTime: str
        :param Status: Version status
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Status: str
        """
        self.Version = None
        self.Description = None
        self.AddTime = None
        self.ModTime = None
        self.Status = None


    def _deserialize(self, params):
        self.Version = params.get("Version")
        self.Description = params.get("Description")
        self.AddTime = params.get("AddTime")
        self.ModTime = params.get("ModTime")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetAccountRequest(AbstractModel):
    """GetAccount request structure.

    """


class GetAccountResponse(AbstractModel):
    """GetAccount response structure.

    """

    def __init__(self):
        r"""
        :param AccountUsage: Namespace usage information
        :type AccountUsage: :class:`tencentcloud.scf.v20180416.models.UsageInfo`
        :param AccountLimit: Namespace limit information
        :type AccountLimit: :class:`tencentcloud.scf.v20180416.models.LimitsInfo`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AccountUsage = None
        self.AccountLimit = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AccountUsage") is not None:
            self.AccountUsage = UsageInfo()
            self.AccountUsage._deserialize(params.get("AccountUsage"))
        if params.get("AccountLimit") is not None:
            self.AccountLimit = LimitsInfo()
            self.AccountLimit._deserialize(params.get("AccountLimit"))
        self.RequestId = params.get("RequestId")


class GetAliasRequest(AbstractModel):
    """GetAlias request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Name: Alias name
        :type Name: str
        :param Namespace: Function namespace
        :type Namespace: str
        """
        self.FunctionName = None
        self.Name = None
        self.Namespace = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Name = params.get("Name")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetAliasResponse(AbstractModel):
    """GetAlias response structure.

    """

    def __init__(self):
        r"""
        :param FunctionVersion: Master version pointed to by the alias
        :type FunctionVersion: str
        :param Name: Alias name
        :type Name: str
        :param RoutingConfig: Routing information of alias
        :type RoutingConfig: :class:`tencentcloud.scf.v20180416.models.RoutingConfig`
        :param Description: Alias description
Note: this field may return null, indicating that no valid values can be obtained.
        :type Description: str
        :param AddTime: Creation time
Note: this field may return null, indicating that no valid values can be obtained.
        :type AddTime: str
        :param ModTime: Update time
Note: this field may return null, indicating that no valid values can be obtained.
        :type ModTime: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FunctionVersion = None
        self.Name = None
        self.RoutingConfig = None
        self.Description = None
        self.AddTime = None
        self.ModTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FunctionVersion = params.get("FunctionVersion")
        self.Name = params.get("Name")
        if params.get("RoutingConfig") is not None:
            self.RoutingConfig = RoutingConfig()
            self.RoutingConfig._deserialize(params.get("RoutingConfig"))
        self.Description = params.get("Description")
        self.AddTime = params.get("AddTime")
        self.ModTime = params.get("ModTime")
        self.RequestId = params.get("RequestId")


class GetAsyncEventStatusRequest(AbstractModel):
    """GetAsyncEventStatus request structure.

    """

    def __init__(self):
        r"""
        :param InvokeRequestId: ID of the async execution request
        :type InvokeRequestId: str
        """
        self.InvokeRequestId = None


    def _deserialize(self, params):
        self.InvokeRequestId = params.get("InvokeRequestId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetAsyncEventStatusResponse(AbstractModel):
    """GetAsyncEventStatus response structure.

    """

    def __init__(self):
        r"""
        :param Result: Async event status
        :type Result: :class:`tencentcloud.scf.v20180416.models.AsyncEventStatus`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Result") is not None:
            self.Result = AsyncEventStatus()
            self.Result._deserialize(params.get("Result"))
        self.RequestId = params.get("RequestId")


class GetFunctionAddressRequest(AbstractModel):
    """GetFunctionAddress request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Qualifier: Function version
        :type Qualifier: str
        :param Namespace: Function namespace
        :type Namespace: str
        """
        self.FunctionName = None
        self.Qualifier = None
        self.Namespace = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Qualifier = params.get("Qualifier")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetFunctionAddressResponse(AbstractModel):
    """GetFunctionAddress response structure.

    """

    def __init__(self):
        r"""
        :param Url: Cos address of the function
        :type Url: str
        :param CodeSha256: SHA256 code of the function
        :type CodeSha256: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Url = None
        self.CodeSha256 = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Url = params.get("Url")
        self.CodeSha256 = params.get("CodeSha256")
        self.RequestId = params.get("RequestId")


class GetFunctionEventInvokeConfigRequest(AbstractModel):
    """GetFunctionEventInvokeConfig request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Namespace: Function namespace. Default value: default
        :type Namespace: str
        :param Qualifier: Function version. Default value: $LATEST
        :type Qualifier: str
        """
        self.FunctionName = None
        self.Namespace = None
        self.Qualifier = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        self.Qualifier = params.get("Qualifier")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetFunctionEventInvokeConfigResponse(AbstractModel):
    """GetFunctionEventInvokeConfig response structure.

    """

    def __init__(self):
        r"""
        :param AsyncTriggerConfig: Async retry configuration information
        :type AsyncTriggerConfig: :class:`tencentcloud.scf.v20180416.models.AsyncTriggerConfig`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AsyncTriggerConfig = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AsyncTriggerConfig") is not None:
            self.AsyncTriggerConfig = AsyncTriggerConfig()
            self.AsyncTriggerConfig._deserialize(params.get("AsyncTriggerConfig"))
        self.RequestId = params.get("RequestId")


class GetFunctionLogsRequest(AbstractModel):
    """GetFunctionLogs request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name.
- To ensure the compatibility of the [`GetFunctionLogs`](https://intl.cloud.tencent.com/document/product/583/18583?from_cn_redirect=1) API, the input parameter `FunctionName` is optional, but we recommend you enter it; otherwise, log acquisition may fail.
- After the function is connected to CLS, we recommend you use the [related CLS API](https://intl.cloud.tencent.com/document/product/614/16875?from_cn_redirect=1) to get the best log retrieval experience.
        :type FunctionName: str
        :param Offset: Data offset. The addition of `Offset` and `Limit` cannot exceed 10,000.
        :type Offset: int
        :param Limit: Length of the return data. The addition of `Offset` and `Limit` cannot exceed 10,000.
        :type Limit: int
        :param Order: It specifies whether to sort the logs in an ascending or descending order. The value is `desc` or `asc`.
        :type Order: str
        :param OrderBy: It specifies the sorting order of the logs based on a specified field, such as `function_name`, `duration`, `mem_usage`, and `start_time`.
        :type OrderBy: str
        :param Filter: Log filter used to identify whether to return logs of successful or failed requests. `filter.RetCode=not0` indicates that only the logs of failed requests will be returned. `filter.RetCode=is0` indicates that only the logs of successful requests will be returned. If this parameter is left blank, all logs will be returned. 
        :type Filter: :class:`tencentcloud.scf.v20180416.models.LogFilter`
        :param Namespace: Function namespace
        :type Namespace: str
        :param Qualifier: Function version
        :type Qualifier: str
        :param FunctionRequestId: RequestId corresponding to the executed function
        :type FunctionRequestId: str
        :param StartTime: Query date, for example, 2017-05-16 20:00:00. The date must be within one day of the end time.
        :type StartTime: str
        :param EndTime: Query date, for example, 2017-05-16 20:59:59. The date must be within one day of the start time.
        :type EndTime: str
        :param SearchContext: This field is disused.
        :type SearchContext: :class:`tencentcloud.scf.v20180416.models.LogSearchContext`
        """
        self.FunctionName = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderBy = None
        self.Filter = None
        self.Namespace = None
        self.Qualifier = None
        self.FunctionRequestId = None
        self.StartTime = None
        self.EndTime = None
        self.SearchContext = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderBy = params.get("OrderBy")
        if params.get("Filter") is not None:
            self.Filter = LogFilter()
            self.Filter._deserialize(params.get("Filter"))
        self.Namespace = params.get("Namespace")
        self.Qualifier = params.get("Qualifier")
        self.FunctionRequestId = params.get("FunctionRequestId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        if params.get("SearchContext") is not None:
            self.SearchContext = LogSearchContext()
            self.SearchContext._deserialize(params.get("SearchContext"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetFunctionLogsResponse(AbstractModel):
    """GetFunctionLogs response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of function logs
        :type TotalCount: int
        :param Data: Function log information
        :type Data: list of FunctionLog
        :param SearchContext: This field is disused.
        :type SearchContext: :class:`tencentcloud.scf.v20180416.models.LogSearchContext`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Data = None
        self.SearchContext = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = FunctionLog()
                obj._deserialize(item)
                self.Data.append(obj)
        if params.get("SearchContext") is not None:
            self.SearchContext = LogSearchContext()
            self.SearchContext._deserialize(params.get("SearchContext"))
        self.RequestId = params.get("RequestId")


class GetLayerVersionRequest(AbstractModel):
    """GetLayerVersion request structure.

    """

    def __init__(self):
        r"""
        :param LayerName: Layer name
        :type LayerName: str
        :param LayerVersion: Version number
        :type LayerVersion: int
        """
        self.LayerName = None
        self.LayerVersion = None


    def _deserialize(self, params):
        self.LayerName = params.get("LayerName")
        self.LayerVersion = params.get("LayerVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetLayerVersionResponse(AbstractModel):
    """GetLayerVersion response structure.

    """

    def __init__(self):
        r"""
        :param CompatibleRuntimes: Compatible runtimes
        :type CompatibleRuntimes: list of str
        :param CodeSha256: SHA256 encoding of version file on the layer
        :type CodeSha256: str
        :param Location: Download address of version file on the layer
        :type Location: str
        :param AddTime: Version creation time
        :type AddTime: str
        :param Description: Version description
        :type Description: str
        :param LicenseInfo: License information
        :type LicenseInfo: str
        :param LayerVersion: Version number
        :type LayerVersion: int
        :param LayerName: Layer name
        :type LayerName: str
        :param Status: Current status of specific layer version. For the status values, [see here](https://intl.cloud.tencent.com/document/product/583/47175?from_cn_redirect=1#.E5.B1.82.EF.BC.88layer.EF.BC.89.E7.8A.B6.E6.80.81)
        :type Status: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.CompatibleRuntimes = None
        self.CodeSha256 = None
        self.Location = None
        self.AddTime = None
        self.Description = None
        self.LicenseInfo = None
        self.LayerVersion = None
        self.LayerName = None
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.CompatibleRuntimes = params.get("CompatibleRuntimes")
        self.CodeSha256 = params.get("CodeSha256")
        self.Location = params.get("Location")
        self.AddTime = params.get("AddTime")
        self.Description = params.get("Description")
        self.LicenseInfo = params.get("LicenseInfo")
        self.LayerVersion = params.get("LayerVersion")
        self.LayerName = params.get("LayerName")
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class GetProvisionedConcurrencyConfigRequest(AbstractModel):
    """GetProvisionedConcurrencyConfig request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Name of the function for which to get the provisioned concurrency details.
        :type FunctionName: str
        :param Namespace: Function namespace. Default value: default.
        :type Namespace: str
        :param Qualifier: Function version number. If this parameter is left empty, the provisioned concurrency information of all function versions will be returned.
        :type Qualifier: str
        """
        self.FunctionName = None
        self.Namespace = None
        self.Qualifier = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        self.Qualifier = params.get("Qualifier")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetProvisionedConcurrencyConfigResponse(AbstractModel):
    """GetProvisionedConcurrencyConfig response structure.

    """

    def __init__(self):
        r"""
        :param UnallocatedConcurrencyNum: Unallocated provisioned concurrency amount of function.
        :type UnallocatedConcurrencyNum: int
        :param Allocated: Allocated provisioned concurrency amount of function.
        :type Allocated: list of VersionProvisionedConcurrencyInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.UnallocatedConcurrencyNum = None
        self.Allocated = None
        self.RequestId = None


    def _deserialize(self, params):
        self.UnallocatedConcurrencyNum = params.get("UnallocatedConcurrencyNum")
        if params.get("Allocated") is not None:
            self.Allocated = []
            for item in params.get("Allocated"):
                obj = VersionProvisionedConcurrencyInfo()
                obj._deserialize(item)
                self.Allocated.append(obj)
        self.RequestId = params.get("RequestId")


class GetRequestStatusRequest(AbstractModel):
    """GetRequestStatus request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param FunctionRequestId: ID of the request to be queried
        :type FunctionRequestId: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param StartTime: Start time of the query, for example `2017-05-16 20:00:00`. If it’s left empty, it defaults to 15 minutes before the current time.
        :type StartTime: str
        :param EndTime: End time of the query. such as `2017-05-16 20:59:59`. If `StartTime` is not specified, `EndTime` defaults to the current time. If `StartTime` is specified, `EndTime` is required, and it need to be later than the `StartTime`.
        :type EndTime: str
        """
        self.FunctionName = None
        self.FunctionRequestId = None
        self.Namespace = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.FunctionRequestId = params.get("FunctionRequestId")
        self.Namespace = params.get("Namespace")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetRequestStatusResponse(AbstractModel):
    """GetRequestStatus response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total running functions
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type TotalCount: int
        :param Data: Details of the function running status
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Data: list of RequestStatus
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = RequestStatus()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class GetReservedConcurrencyConfigRequest(AbstractModel):
    """GetReservedConcurrencyConfig request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Specifies the function of which you want to obtain the reserved quota
        :type FunctionName: str
        :param Namespace: Function namespace. Default value: default.
        :type Namespace: str
        """
        self.FunctionName = None
        self.Namespace = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetReservedConcurrencyConfigResponse(AbstractModel):
    """GetReservedConcurrencyConfig response structure.

    """

    def __init__(self):
        r"""
        :param ReservedMem: The reserved quota of the function
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ReservedMem: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ReservedMem = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReservedMem = params.get("ReservedMem")
        self.RequestId = params.get("RequestId")


class ImageConfig(AbstractModel):
    """TCR image information

    """

    def __init__(self):
        r"""
        :param ImageType: Image repository type, which can be `personal` or `enterprise`
        :type ImageType: str
        :param ImageUri: {domain}/{namespace}/{imageName}:{tag}@{digest}
        :type ImageUri: str
        :param RegistryId: The temp token that a TCR Enterprise instance uses to obtain an image. It’s required when `ImageType` is `enterprise`.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type RegistryId: str
        :param EntryPoint: Disused
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type EntryPoint: str
        :param Command: The command to start up the container, such as `python`. If it’s not specified, Entrypoint in Dockerfile is used.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type Command: str
        :param Args: The parameters to start up the container. Separate parameters with spaces, such as `u app.py`. If it’s not specified, `CMD in Dockerfile is used.
Note: This field may return `null`, indicating that no valid value can be found.
        :type Args: str
        :param ContainerImageAccelerate: Whether to enable image acceleration. It defaults to `False`.
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type ContainerImageAccelerate: bool
        :param ImagePort: Image function port settings
`-1`: No port-specific image functions
`0`: Default port (Port 9000)
Others: Special ports
Note: This field may return null, indicating that no valid values can be obtained.
        :type ImagePort: int
        """
        self.ImageType = None
        self.ImageUri = None
        self.RegistryId = None
        self.EntryPoint = None
        self.Command = None
        self.Args = None
        self.ContainerImageAccelerate = None
        self.ImagePort = None


    def _deserialize(self, params):
        self.ImageType = params.get("ImageType")
        self.ImageUri = params.get("ImageUri")
        self.RegistryId = params.get("RegistryId")
        self.EntryPoint = params.get("EntryPoint")
        self.Command = params.get("Command")
        self.Args = params.get("Args")
        self.ContainerImageAccelerate = params.get("ContainerImageAccelerate")
        self.ImagePort = params.get("ImagePort")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InvokeFunctionRequest(AbstractModel):
    """InvokeFunction request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Qualifier: Version or alias of the function. It defaults to `$DEFAULT`.
        :type Qualifier: str
        :param Event: Function running parameter, which is in the JSON format. Maximum parameter size is 6 MB. This field corresponds to [event input parameter](https://intl.cloud.tencent.com/document/product/583/9210?from_cn_redirect=1#.E5.87.BD.E6.95.B0.E5.85.A5.E5.8F.82.3Ca-id.3D.22input.22.3E.3C.2Fa.3E).
        :type Event: str
        :param LogType: Valid value: `None` (default) or `Tail`. If the value is `Tail`, `log` in the response will contain the corresponding function execution log (up to 4KB).
        :type LogType: str
        :param Namespace: Namespace. `default` is used if it’s left empty.
        :type Namespace: str
        :param RoutingKey: Traffic routing config in json format, e.g., {"k":"v"}. Please note that both "k" and "v" must be strings. Up to 1024 bytes allowed.
        :type RoutingKey: str
        """
        self.FunctionName = None
        self.Qualifier = None
        self.Event = None
        self.LogType = None
        self.Namespace = None
        self.RoutingKey = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Qualifier = params.get("Qualifier")
        self.Event = params.get("Event")
        self.LogType = params.get("LogType")
        self.Namespace = params.get("Namespace")
        self.RoutingKey = params.get("RoutingKey")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InvokeFunctionResponse(AbstractModel):
    """InvokeFunction response structure.

    """

    def __init__(self):
        r"""
        :param Result: Function execution result
        :type Result: :class:`tencentcloud.scf.v20180416.models.Result`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Result") is not None:
            self.Result = Result()
            self.Result._deserialize(params.get("Result"))
        self.RequestId = params.get("RequestId")


class InvokeRequest(AbstractModel):
    """Invoke request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param InvocationType: Fill in `RequestResponse` for synchronized invocations (default and recommended) and `Event` for asychronized invocations. Note that for synchronized invocations, the max timeout period is 300s. Choose asychronized invocations if the required timeout period is longer than 300 seconds. You can also use [InvokeFunction](https://intl.cloud.tencent.com/document/product/583/58400?from_cn_redirect=1) for synchronized invocations. 
        :type InvocationType: str
        :param Qualifier: The version or alias of the triggered function. It defaults to $LATEST
        :type Qualifier: str
        :param ClientContext: Function running parameter, which is in the JSON format. The maximum parameter size is 6 MB for synchronized invocations and 128KB for asynchronized invocations. This field corresponds to [event input parameter](https://intl.cloud.tencent.com/document/product/583/9210?from_cn_redirect=1#.E5.87.BD.E6.95.B0.E5.85.A5.E5.8F.82.3Ca-id.3D.22input.22.3E.3C.2Fa.3E).
        :type ClientContext: str
        :param LogType: Null for async invocations
        :type LogType: str
        :param Namespace: Namespace
        :type Namespace: str
        :param RoutingKey: Traffic routing config in json format, e.g., {"k":"v"}. Please note that both "k" and "v" must be strings. Up to 1024 bytes allowed.
        :type RoutingKey: str
        """
        self.FunctionName = None
        self.InvocationType = None
        self.Qualifier = None
        self.ClientContext = None
        self.LogType = None
        self.Namespace = None
        self.RoutingKey = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.InvocationType = params.get("InvocationType")
        self.Qualifier = params.get("Qualifier")
        self.ClientContext = params.get("ClientContext")
        self.LogType = params.get("LogType")
        self.Namespace = params.get("Namespace")
        self.RoutingKey = params.get("RoutingKey")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InvokeResponse(AbstractModel):
    """Invoke response structure.

    """

    def __init__(self):
        r"""
        :param Result: Function execution result
        :type Result: :class:`tencentcloud.scf.v20180416.models.Result`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Result") is not None:
            self.Result = Result()
            self.Result._deserialize(params.get("Result"))
        self.RequestId = params.get("RequestId")


class LayerVersionInfo(AbstractModel):
    """Layer version information

    """

    def __init__(self):
        r"""
        :param CompatibleRuntimes: Runtime applicable to a version
Note: This field may return null, indicating that no valid values can be obtained.
        :type CompatibleRuntimes: list of str
        :param AddTime: Creation time
        :type AddTime: str
        :param Description: Version description
Note: This field may return null, indicating that no valid values can be obtained.
        :type Description: str
        :param LicenseInfo: License information
Note: This field may return null, indicating that no valid values can be obtained.
        :type LicenseInfo: str
        :param LayerVersion: Version number
        :type LayerVersion: int
        :param LayerName: Layer name
        :type LayerName: str
        :param Status: Current status of specific layer version. For valid values, please see [here](https://intl.cloud.tencent.com/document/product/583/47175?from_cn_redirect=1#.E5.B1.82.EF.BC.88layer.EF.BC.89.E7.8A.B6.E6.80.81)
        :type Status: str
        :param Stamp: Stamp
Note: This field may return null, indicating that no valid values can be obtained.
        :type Stamp: str
        """
        self.CompatibleRuntimes = None
        self.AddTime = None
        self.Description = None
        self.LicenseInfo = None
        self.LayerVersion = None
        self.LayerName = None
        self.Status = None
        self.Stamp = None


    def _deserialize(self, params):
        self.CompatibleRuntimes = params.get("CompatibleRuntimes")
        self.AddTime = params.get("AddTime")
        self.Description = params.get("Description")
        self.LicenseInfo = params.get("LicenseInfo")
        self.LayerVersion = params.get("LayerVersion")
        self.LayerName = params.get("LayerName")
        self.Status = params.get("Status")
        self.Stamp = params.get("Stamp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LimitsInfo(AbstractModel):
    """Limit information

    """

    def __init__(self):
        r"""
        :param NamespacesCount: Limit of namespace quantity
        :type NamespacesCount: int
        :param Namespace: Namespace limit information
        :type Namespace: list of NamespaceLimit
        """
        self.NamespacesCount = None
        self.Namespace = None


    def _deserialize(self, params):
        self.NamespacesCount = params.get("NamespacesCount")
        if params.get("Namespace") is not None:
            self.Namespace = []
            for item in params.get("Namespace"):
                obj = NamespaceLimit()
                obj._deserialize(item)
                self.Namespace.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListAliasesRequest(AbstractModel):
    """ListAliases request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param FunctionVersion: If this parameter is provided, only aliases associated with this function version will be returned.
        :type FunctionVersion: str
        :param Offset: Data offset. Default value: 0
        :type Offset: str
        :param Limit: Number of results to be returned. Default value: 20
        :type Limit: str
        """
        self.FunctionName = None
        self.Namespace = None
        self.FunctionVersion = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        self.FunctionVersion = params.get("FunctionVersion")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListAliasesResponse(AbstractModel):
    """ListAliases response structure.

    """

    def __init__(self):
        r"""
        :param Aliases: Alias list
        :type Aliases: list of Alias
        :param TotalCount: Total number of aliases
Note: this field may return null, indicating that no valid values can be obtained.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Aliases = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Aliases") is not None:
            self.Aliases = []
            for item in params.get("Aliases"):
                obj = Alias()
                obj._deserialize(item)
                self.Aliases.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class ListAsyncEventsRequest(AbstractModel):
    """ListAsyncEvents request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Namespace: Namespace
        :type Namespace: str
        :param Qualifier: Filter (function version)
        :type Qualifier: str
        :param InvokeType: Filter (invocation type list)
        :type InvokeType: list of str
        :param Status: Filter (event status list)
        :type Status: list of str
        :param StartTimeInterval: Filter (left-closed-right-open range of execution start time)
        :type StartTimeInterval: :class:`tencentcloud.scf.v20180416.models.TimeInterval`
        :param EndTimeInterval: Filter (left-closed-right-open range of execution end time)
        :type EndTimeInterval: :class:`tencentcloud.scf.v20180416.models.TimeInterval`
        :param Order: Valid values: ASC, DESC. Default value: DESC
        :type Order: str
        :param Orderby: Valid values: StartTime, EndTime. Default value: StartTime
        :type Orderby: str
        :param Offset: Data offset. Default value: 0
        :type Offset: int
        :param Limit: Number of results to be returned. Default value: 20. Maximum value: 100
        :type Limit: int
        :param InvokeRequestId: Filter (event invocation request ID)
        :type InvokeRequestId: str
        """
        self.FunctionName = None
        self.Namespace = None
        self.Qualifier = None
        self.InvokeType = None
        self.Status = None
        self.StartTimeInterval = None
        self.EndTimeInterval = None
        self.Order = None
        self.Orderby = None
        self.Offset = None
        self.Limit = None
        self.InvokeRequestId = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        self.Qualifier = params.get("Qualifier")
        self.InvokeType = params.get("InvokeType")
        self.Status = params.get("Status")
        if params.get("StartTimeInterval") is not None:
            self.StartTimeInterval = TimeInterval()
            self.StartTimeInterval._deserialize(params.get("StartTimeInterval"))
        if params.get("EndTimeInterval") is not None:
            self.EndTimeInterval = TimeInterval()
            self.EndTimeInterval._deserialize(params.get("EndTimeInterval"))
        self.Order = params.get("Order")
        self.Orderby = params.get("Orderby")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InvokeRequestId = params.get("InvokeRequestId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListAsyncEventsResponse(AbstractModel):
    """ListAsyncEvents response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of events that meet the filter
        :type TotalCount: int
        :param EventList: Async event list
        :type EventList: list of AsyncEvent
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.EventList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("EventList") is not None:
            self.EventList = []
            for item in params.get("EventList"):
                obj = AsyncEvent()
                obj._deserialize(item)
                self.EventList.append(obj)
        self.RequestId = params.get("RequestId")


class ListFunctionsRequest(AbstractModel):
    """ListFunctions request structure.

    """

    def __init__(self):
        r"""
        :param Order: It specifies whether to return the results in ascending or descending order. The value is `ASC` or `DESC`.
        :type Order: str
        :param Orderby: It specifies the sorting order of the results according to a specified field, such as `AddTime`, `ModTime`, and `FunctionName`.
        :type Orderby: str
        :param Offset: Data offset. The default value is `0`.
        :type Offset: int
        :param Limit: Return data length. The default value is `20`.
        :type Limit: int
        :param SearchKey: It specifies whether to support fuzzy matching for the function name.
        :type SearchKey: str
        :param Namespace: Namespace
        :type Namespace: str
        :param Description: Function description. Fuzzy search is supported.
        :type Description: str
        :param Filters: Filters
- tag:tag-key - String - Required: No - Filtering criteria based on tag-key - value pairs. Replace `tag-key` with a specific tag-key.

The maximum number of `Filters` for each request is 10, and that of `Filter.Values` is 5.
        :type Filters: list of Filter
        """
        self.Order = None
        self.Orderby = None
        self.Offset = None
        self.Limit = None
        self.SearchKey = None
        self.Namespace = None
        self.Description = None
        self.Filters = None


    def _deserialize(self, params):
        self.Order = params.get("Order")
        self.Orderby = params.get("Orderby")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SearchKey = params.get("SearchKey")
        self.Namespace = params.get("Namespace")
        self.Description = params.get("Description")
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
        


class ListFunctionsResponse(AbstractModel):
    """ListFunctions response structure.

    """

    def __init__(self):
        r"""
        :param Functions: Function list
        :type Functions: list of Function
        :param TotalCount: Total number
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Functions = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Functions") is not None:
            self.Functions = []
            for item in params.get("Functions"):
                obj = Function()
                obj._deserialize(item)
                self.Functions.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class ListLayerVersionsRequest(AbstractModel):
    """ListLayerVersions request structure.

    """

    def __init__(self):
        r"""
        :param LayerName: Layer name
        :type LayerName: str
        :param CompatibleRuntime: Compatible runtimes
        :type CompatibleRuntime: list of str
        """
        self.LayerName = None
        self.CompatibleRuntime = None


    def _deserialize(self, params):
        self.LayerName = params.get("LayerName")
        self.CompatibleRuntime = params.get("CompatibleRuntime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListLayerVersionsResponse(AbstractModel):
    """ListLayerVersions response structure.

    """

    def __init__(self):
        r"""
        :param LayerVersions: Layer version list
        :type LayerVersions: list of LayerVersionInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.LayerVersions = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LayerVersions") is not None:
            self.LayerVersions = []
            for item in params.get("LayerVersions"):
                obj = LayerVersionInfo()
                obj._deserialize(item)
                self.LayerVersions.append(obj)
        self.RequestId = params.get("RequestId")


class ListLayersRequest(AbstractModel):
    """ListLayers request structure.

    """

    def __init__(self):
        r"""
        :param CompatibleRuntime: Compatible runtimes
        :type CompatibleRuntime: str
        :param Offset: Offset
        :type Offset: int
        :param Limit: Limit
        :type Limit: int
        :param SearchKey: Query key, which fuzzily matches the name
        :type SearchKey: str
        """
        self.CompatibleRuntime = None
        self.Offset = None
        self.Limit = None
        self.SearchKey = None


    def _deserialize(self, params):
        self.CompatibleRuntime = params.get("CompatibleRuntime")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SearchKey = params.get("SearchKey")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListLayersResponse(AbstractModel):
    """ListLayers response structure.

    """

    def __init__(self):
        r"""
        :param Layers: Layer list
        :type Layers: list of LayerVersionInfo
        :param TotalCount: Total number of layers
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Layers = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Layers") is not None:
            self.Layers = []
            for item in params.get("Layers"):
                obj = LayerVersionInfo()
                obj._deserialize(item)
                self.Layers.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class ListNamespacesRequest(AbstractModel):
    """ListNamespaces request structure.

    """

    def __init__(self):
        r"""
        :param Limit: Return data length. The default value is `20`.
        :type Limit: int
        :param Offset: Data offset. The default value is `0`.
        :type Offset: int
        :param Orderby: It specifies the sorting order of the results according to a specified field, such as `Name` and `Updatetime`.
        :type Orderby: str
        :param Order: It specifies whether to return the results in ascending or descending order. The value is `ASC` or `DESC`.
        :type Order: str
        :param SearchKey: Specifies the range and keyword for search. The value of `Key` can be `Namespace` or `Description`. Multiple AND conditions can be specified.
        :type SearchKey: list of SearchKey
        """
        self.Limit = None
        self.Offset = None
        self.Orderby = None
        self.Order = None
        self.SearchKey = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Orderby = params.get("Orderby")
        self.Order = params.get("Order")
        if params.get("SearchKey") is not None:
            self.SearchKey = []
            for item in params.get("SearchKey"):
                obj = SearchKey()
                obj._deserialize(item)
                self.SearchKey.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListNamespacesResponse(AbstractModel):
    """ListNamespaces response structure.

    """

    def __init__(self):
        r"""
        :param Namespaces: Namespace details
        :type Namespaces: list of Namespace
        :param TotalCount: Number of return namespaces
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Namespaces = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Namespaces") is not None:
            self.Namespaces = []
            for item in params.get("Namespaces"):
                obj = Namespace()
                obj._deserialize(item)
                self.Namespaces.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class ListTriggersRequest(AbstractModel):
    """ListTriggers request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Namespace: Namespace. Default value: default
        :type Namespace: str
        :param Offset: Data offset. Default value: 0
        :type Offset: int
        :param Limit: Number of results to be returned. Default value: 20
        :type Limit: int
        :param OrderBy: Indicates by which field to sort the returned results. Valid values: add_time, mod_time. Default value: mod_time
        :type OrderBy: str
        :param Order: Indicates whether the returned results are sorted in ascending or descending order. Valid values: ASC, DESC. Default value: DESC
        :type Order: str
        :param Filters: * Qualifier:
Function version, alias
        :type Filters: list of Filter
        """
        self.FunctionName = None
        self.Namespace = None
        self.Offset = None
        self.Limit = None
        self.OrderBy = None
        self.Order = None
        self.Filters = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderBy = params.get("OrderBy")
        self.Order = params.get("Order")
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
        


class ListTriggersResponse(AbstractModel):
    """ListTriggers response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of triggers
        :type TotalCount: int
        :param Triggers: Trigger list
        :type Triggers: list of TriggerInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Triggers = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Triggers") is not None:
            self.Triggers = []
            for item in params.get("Triggers"):
                obj = TriggerInfo()
                obj._deserialize(item)
                self.Triggers.append(obj)
        self.RequestId = params.get("RequestId")


class ListVersionByFunctionRequest(AbstractModel):
    """ListVersionByFunction request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function Name
        :type FunctionName: str
        :param Namespace: The namespace where the function locates
        :type Namespace: str
        :param Offset: Data offset. The default value is `0`.
        :type Offset: int
        :param Limit: Return data length. The default value is `20`.
        :type Limit: int
        :param Order: It specifies whether to return the results in ascending or descending order. The value is `ASC` or `DESC`.
        :type Order: str
        :param OrderBy: It specifies the sorting order of the results according to a specified field, such as `AddTime`, `ModTime`.
        :type OrderBy: str
        """
        self.FunctionName = None
        self.Namespace = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderBy = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderBy = params.get("OrderBy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListVersionByFunctionResponse(AbstractModel):
    """ListVersionByFunction response structure.

    """

    def __init__(self):
        r"""
        :param FunctionVersion: Function version
        :type FunctionVersion: list of str
        :param Versions: Function version list
Note: This field may return null, indicating that no valid values is found.
        :type Versions: list of FunctionVersion
        :param TotalCount: Total number of function versions
Note: This field may return null, indicating that no valid value was found.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FunctionVersion = None
        self.Versions = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FunctionVersion = params.get("FunctionVersion")
        if params.get("Versions") is not None:
            self.Versions = []
            for item in params.get("Versions"):
                obj = FunctionVersion()
                obj._deserialize(item)
                self.Versions.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class LogFilter(AbstractModel):
    """Log filtering criteria, which is for distinguishing between logs of successful and failed execution

    """

    def __init__(self):
        r"""
        :param RetCode: Values of `filter.RetCode` include:
not0, indicating that only logs of failed execution will be returned.
is0, indicating that only logs of successful execution will be returned.
TimeLimitExceeded, indicating that logs of function invocations which timed out will be returned.
ResourceLimitExceeded, indicating that logs of function invocations during which resources exceeded the upper limit will be returned.
UserCodeException, indicating that logs of function invocations during which a user code error occurred will be returned.
Blank, indicating that all logs will be returned.
        :type RetCode: str
        """
        self.RetCode = None


    def _deserialize(self, params):
        self.RetCode = params.get("RetCode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LogSearchContext(AbstractModel):
    """Log search context

    """

    def __init__(self):
        r"""
        :param Offset: Offset.
        :type Offset: str
        :param Limit: Log record number
        :type Limit: int
        :param Keyword: Log keyword
        :type Keyword: str
        :param Type: Log type. The value is `Application` (default) or `Platform`.
        :type Type: str
        """
        self.Offset = None
        self.Limit = None
        self.Keyword = None
        self.Type = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Keyword = params.get("Keyword")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Namespace(AbstractModel):
    """Namespace

    """

    def __init__(self):
        r"""
        :param ModTime: Creation time of the namespace
        :type ModTime: str
        :param AddTime: Modification time of the namespace
        :type AddTime: str
        :param Description: Namespace description
        :type Description: str
        :param Name: Namespace name
        :type Name: str
        :param Type: The default value is default. TCB indicates that the namespace is developed and created through the mini-program cloud.
        :type Type: str
        """
        self.ModTime = None
        self.AddTime = None
        self.Description = None
        self.Name = None
        self.Type = None


    def _deserialize(self, params):
        self.ModTime = params.get("ModTime")
        self.AddTime = params.get("AddTime")
        self.Description = params.get("Description")
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NamespaceLimit(AbstractModel):
    """Namespace limit

    """

    def __init__(self):
        r"""
        :param FunctionsCount: Total number of functions
        :type FunctionsCount: int
        :param Trigger: Trigger information
        :type Trigger: :class:`tencentcloud.scf.v20180416.models.TriggerCount`
        :param Namespace: Namespace name
        :type Namespace: str
        :param ConcurrentExecutions: Concurrency
        :type ConcurrentExecutions: int
        :param TimeoutLimit: Timeout limit
        :type TimeoutLimit: int
        :param TestModelLimit: Test event limit
Note: this field may return null, indicating that no valid values can be obtained.
        :type TestModelLimit: int
        :param InitTimeoutLimit: Initialization timeout limit
        :type InitTimeoutLimit: int
        :param RetryNumLimit: Limit of async retry attempt quantity
        :type RetryNumLimit: int
        :param MinMsgTTL: Lower limit of message retention time for async retry
        :type MinMsgTTL: int
        :param MaxMsgTTL: Upper limit of message retention time for async retry
        :type MaxMsgTTL: int
        """
        self.FunctionsCount = None
        self.Trigger = None
        self.Namespace = None
        self.ConcurrentExecutions = None
        self.TimeoutLimit = None
        self.TestModelLimit = None
        self.InitTimeoutLimit = None
        self.RetryNumLimit = None
        self.MinMsgTTL = None
        self.MaxMsgTTL = None


    def _deserialize(self, params):
        self.FunctionsCount = params.get("FunctionsCount")
        if params.get("Trigger") is not None:
            self.Trigger = TriggerCount()
            self.Trigger._deserialize(params.get("Trigger"))
        self.Namespace = params.get("Namespace")
        self.ConcurrentExecutions = params.get("ConcurrentExecutions")
        self.TimeoutLimit = params.get("TimeoutLimit")
        self.TestModelLimit = params.get("TestModelLimit")
        self.InitTimeoutLimit = params.get("InitTimeoutLimit")
        self.RetryNumLimit = params.get("RetryNumLimit")
        self.MinMsgTTL = params.get("MinMsgTTL")
        self.MaxMsgTTL = params.get("MaxMsgTTL")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NamespaceUsage(AbstractModel):
    """Namespace usage information

    """

    def __init__(self):
        r"""
        :param Functions: Function array
        :type Functions: list of str
        :param Namespace: Namespace name
        :type Namespace: str
        :param FunctionsCount: Number of functions in namespace
        :type FunctionsCount: int
        :param TotalConcurrencyMem: Total memory quota of the namespace
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type TotalConcurrencyMem: int
        :param TotalAllocatedConcurrencyMem: Concurrency usage of the namespace
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type TotalAllocatedConcurrencyMem: int
        :param TotalAllocatedProvisionedMem: Provisioned concurrency usage of the namespace
Note: This field may return `null`, indicating that no valid value can be obtained.
        :type TotalAllocatedProvisionedMem: int
        """
        self.Functions = None
        self.Namespace = None
        self.FunctionsCount = None
        self.TotalConcurrencyMem = None
        self.TotalAllocatedConcurrencyMem = None
        self.TotalAllocatedProvisionedMem = None


    def _deserialize(self, params):
        self.Functions = params.get("Functions")
        self.Namespace = params.get("Namespace")
        self.FunctionsCount = params.get("FunctionsCount")
        self.TotalConcurrencyMem = params.get("TotalConcurrencyMem")
        self.TotalAllocatedConcurrencyMem = params.get("TotalAllocatedConcurrencyMem")
        self.TotalAllocatedProvisionedMem = params.get("TotalAllocatedProvisionedMem")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PublishLayerVersionRequest(AbstractModel):
    """PublishLayerVersion request structure.

    """

    def __init__(self):
        r"""
        :param LayerName: Layer name, which can contain 1-64 English letters, digits, hyphens, and underscores, must begin with a letter, and cannot end with a hyphen or underscore
        :type LayerName: str
        :param CompatibleRuntimes: Runtimes compatible with layer. Multiple choices are allowed. The valid values of this parameter correspond to the valid values of the `Runtime` of the function.
        :type CompatibleRuntimes: list of str
        :param Content: Layer file source or content
        :type Content: :class:`tencentcloud.scf.v20180416.models.Code`
        :param Description: Layer version description
        :type Description: str
        :param LicenseInfo: Software license of layer
        :type LicenseInfo: str
        """
        self.LayerName = None
        self.CompatibleRuntimes = None
        self.Content = None
        self.Description = None
        self.LicenseInfo = None


    def _deserialize(self, params):
        self.LayerName = params.get("LayerName")
        self.CompatibleRuntimes = params.get("CompatibleRuntimes")
        if params.get("Content") is not None:
            self.Content = Code()
            self.Content._deserialize(params.get("Content"))
        self.Description = params.get("Description")
        self.LicenseInfo = params.get("LicenseInfo")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PublishLayerVersionResponse(AbstractModel):
    """PublishLayerVersion response structure.

    """

    def __init__(self):
        r"""
        :param LayerVersion: Version number of the layer created in this request
        :type LayerVersion: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.LayerVersion = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LayerVersion = params.get("LayerVersion")
        self.RequestId = params.get("RequestId")


class PublishVersionRequest(AbstractModel):
    """PublishVersion request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Name of the released function
        :type FunctionName: str
        :param Description: Function description
        :type Description: str
        :param Namespace: Function namespace
        :type Namespace: str
        """
        self.FunctionName = None
        self.Description = None
        self.Namespace = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Description = params.get("Description")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PublishVersionResponse(AbstractModel):
    """PublishVersion response structure.

    """

    def __init__(self):
        r"""
        :param FunctionVersion: Function version
        :type FunctionVersion: str
        :param CodeSize: Code size
        :type CodeSize: int
        :param MemorySize: Maximum available memory
        :type MemorySize: int
        :param Description: Function description
        :type Description: str
        :param Handler: Function entry
        :type Handler: str
        :param Timeout: Function timeout
        :type Timeout: int
        :param Runtime: Function running environment
        :type Runtime: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FunctionVersion = None
        self.CodeSize = None
        self.MemorySize = None
        self.Description = None
        self.Handler = None
        self.Timeout = None
        self.Runtime = None
        self.Namespace = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FunctionVersion = params.get("FunctionVersion")
        self.CodeSize = params.get("CodeSize")
        self.MemorySize = params.get("MemorySize")
        self.Description = params.get("Description")
        self.Handler = params.get("Handler")
        self.Timeout = params.get("Timeout")
        self.Runtime = params.get("Runtime")
        self.Namespace = params.get("Namespace")
        self.RequestId = params.get("RequestId")


class PutProvisionedConcurrencyConfigRequest(AbstractModel):
    """PutProvisionedConcurrencyConfig request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Name of the function for which to set the provisioned concurrency
        :type FunctionName: str
        :param Qualifier: Function version number. Note: the `$LATEST` version does not support provisioned concurrency
        :type Qualifier: str
        :param VersionProvisionedConcurrencyNum: Provisioned concurrency amount. Note: there is an upper limit for the sum of provisioned concurrency amounts of all versions, which currently is the function's maximum concurrency quota minus 100
        :type VersionProvisionedConcurrencyNum: int
        :param Namespace: Function namespace. Default value: `default`
        :type Namespace: str
        :param TriggerActions: Scheduled provisioned concurrency scaling action
        :type TriggerActions: list of TriggerAction
        :param ProvisionedType: Specifies the provisioned concurrency type.
`Default`: Static provisioned concurrency. 
`ConcurrencyUtilizationTracking`: Scales the concurrency automatically according to the concurrency utilization.
If `ConcurrencyUtilizationTracking` is passed in, 

`TrackingTarget`, `MinCapacity` and `MaxCapacity` are required, and `VersionProvisionedConcurrencyNum` must be `0`. 
        :type ProvisionedType: str
        :param TrackingTarget: The target concurrency utilization. Range: (0,1) (two decimal places)
        :type TrackingTarget: float
        :param MinCapacity: The minimum number of instances. It can not be smaller than `1`.
        :type MinCapacity: int
        :param MaxCapacity: The maximum number of instances
        :type MaxCapacity: int
        """
        self.FunctionName = None
        self.Qualifier = None
        self.VersionProvisionedConcurrencyNum = None
        self.Namespace = None
        self.TriggerActions = None
        self.ProvisionedType = None
        self.TrackingTarget = None
        self.MinCapacity = None
        self.MaxCapacity = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Qualifier = params.get("Qualifier")
        self.VersionProvisionedConcurrencyNum = params.get("VersionProvisionedConcurrencyNum")
        self.Namespace = params.get("Namespace")
        if params.get("TriggerActions") is not None:
            self.TriggerActions = []
            for item in params.get("TriggerActions"):
                obj = TriggerAction()
                obj._deserialize(item)
                self.TriggerActions.append(obj)
        self.ProvisionedType = params.get("ProvisionedType")
        self.TrackingTarget = params.get("TrackingTarget")
        self.MinCapacity = params.get("MinCapacity")
        self.MaxCapacity = params.get("MaxCapacity")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PutProvisionedConcurrencyConfigResponse(AbstractModel):
    """PutProvisionedConcurrencyConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class PutReservedConcurrencyConfigRequest(AbstractModel):
    """PutReservedConcurrencyConfig request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Specifies the function of which you want to configure the reserved quota
        :type FunctionName: str
        :param ReservedConcurrencyMem: Reserved memory quota of the function. Note: the upper limit for the total reserved quota of the function is the user's total concurrency memory minus 12800
        :type ReservedConcurrencyMem: int
        :param Namespace: Function namespace. Default value: `default`
        :type Namespace: str
        """
        self.FunctionName = None
        self.ReservedConcurrencyMem = None
        self.Namespace = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.ReservedConcurrencyMem = params.get("ReservedConcurrencyMem")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PutReservedConcurrencyConfigResponse(AbstractModel):
    """PutReservedConcurrencyConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class PutTotalConcurrencyConfigRequest(AbstractModel):
    """PutTotalConcurrencyConfig request structure.

    """

    def __init__(self):
        r"""
        :param TotalConcurrencyMem: Account concurrency memory quota. Note: the lower limit for the account concurrency memory quota is the user's total concurrency memory used + 12800
        :type TotalConcurrencyMem: int
        :param Namespace: Namespace. Default value: `default`
        :type Namespace: str
        """
        self.TotalConcurrencyMem = None
        self.Namespace = None


    def _deserialize(self, params):
        self.TotalConcurrencyMem = params.get("TotalConcurrencyMem")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PutTotalConcurrencyConfigResponse(AbstractModel):
    """PutTotalConcurrencyConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RequestStatus(AbstractModel):
    """Running status of the function

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param RetMsg: Return value after the function is executed
        :type RetMsg: str
        :param RequestId: Request ID
        :type RequestId: str
        :param StartTime: Request start time
        :type StartTime: str
        :param RetCode: Result of the request. `0`: succeeded, `1`: running, `-1`: exception
        :type RetCode: int
        :param Duration: Time consumed for the request in ms
        :type Duration: float
        :param MemUsage: Time consumed by the request in MB
        :type MemUsage: float
        :param RetryNum: Retry Attempts
        :type RetryNum: int
        """
        self.FunctionName = None
        self.RetMsg = None
        self.RequestId = None
        self.StartTime = None
        self.RetCode = None
        self.Duration = None
        self.MemUsage = None
        self.RetryNum = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.RetMsg = params.get("RetMsg")
        self.RequestId = params.get("RequestId")
        self.StartTime = params.get("StartTime")
        self.RetCode = params.get("RetCode")
        self.Duration = params.get("Duration")
        self.MemUsage = params.get("MemUsage")
        self.RetryNum = params.get("RetryNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Result(AbstractModel):
    """Response of the executed function

    """

    def __init__(self):
        r"""
        :param Log: It indicates the log output during the function execution. Null is returned for asynchronous invocations.
        :type Log: str
        :param RetMsg: It indicates the response from the executed function. Null is returned for asynchronous invocations.
        :type RetMsg: str
        :param ErrMsg: It indicates the error message of the executed function. Null is returned for asynchronous invocations.
        :type ErrMsg: str
        :param MemUsage: It indicates the memory size (in bytes) when the function is running. Null is returned for asynchronous invocations.
        :type MemUsage: int
        :param Duration: It indicates the duration (in milliseconds) required for running the function. Null is returned for asynchronous invocations.
        :type Duration: float
        :param BillDuration: It indicates the billing duration (in milliseconds) for the function. Null is returned for asynchronous invocations.
        :type BillDuration: int
        :param FunctionRequestId: ID of the executed function
        :type FunctionRequestId: str
        :param InvokeResult: The [status code](https://intl.cloud.tencent.com/document/product/583/42611?from_cn_redirect=1) of the request. It’s not available for `Invoke` API. 
        :type InvokeResult: int
        """
        self.Log = None
        self.RetMsg = None
        self.ErrMsg = None
        self.MemUsage = None
        self.Duration = None
        self.BillDuration = None
        self.FunctionRequestId = None
        self.InvokeResult = None


    def _deserialize(self, params):
        self.Log = params.get("Log")
        self.RetMsg = params.get("RetMsg")
        self.ErrMsg = params.get("ErrMsg")
        self.MemUsage = params.get("MemUsage")
        self.Duration = params.get("Duration")
        self.BillDuration = params.get("BillDuration")
        self.FunctionRequestId = params.get("FunctionRequestId")
        self.InvokeResult = params.get("InvokeResult")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RetryConfig(AbstractModel):
    """Async retry configuration

    """

    def __init__(self):
        r"""
        :param RetryNum: Number of retry attempts
        :type RetryNum: int
        """
        self.RetryNum = None


    def _deserialize(self, params):
        self.RetryNum = params.get("RetryNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RoutingConfig(AbstractModel):
    """Version routing configuration of alias

    """

    def __init__(self):
        r"""
        :param AdditionalVersionWeights: Additional version with random weight-based routing
        :type AdditionalVersionWeights: list of VersionWeight
        :param AddtionVersionMatchs: Additional version with rule-based routing
        :type AddtionVersionMatchs: list of VersionMatch
        """
        self.AdditionalVersionWeights = None
        self.AddtionVersionMatchs = None


    def _deserialize(self, params):
        if params.get("AdditionalVersionWeights") is not None:
            self.AdditionalVersionWeights = []
            for item in params.get("AdditionalVersionWeights"):
                obj = VersionWeight()
                obj._deserialize(item)
                self.AdditionalVersionWeights.append(obj)
        if params.get("AddtionVersionMatchs") is not None:
            self.AddtionVersionMatchs = []
            for item in params.get("AddtionVersionMatchs"):
                obj = VersionMatch()
                obj._deserialize(item)
                self.AddtionVersionMatchs.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SearchKey(AbstractModel):
    """Key-value condition for keyword search

    """

    def __init__(self):
        r"""
        :param Key: Search range
        :type Key: str
        :param Value: Keyword for search
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
        


class StatusReason(AbstractModel):
    """State reason description

    """

    def __init__(self):
        r"""
        :param ErrorCode: Error code
        :type ErrorCode: str
        :param ErrorMessage: Error message
        :type ErrorMessage: str
        """
        self.ErrorCode = None
        self.ErrorMessage = None


    def _deserialize(self, params):
        self.ErrorCode = params.get("ErrorCode")
        self.ErrorMessage = params.get("ErrorMessage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Tag(AbstractModel):
    """Function tag

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
        


class TerminateAsyncEventRequest(AbstractModel):
    """TerminateAsyncEvent request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param InvokeRequestId: Terminated invocation request ID
        :type InvokeRequestId: str
        :param Namespace: Namespace
        :type Namespace: str
        :param GraceShutdown: Whether to enable grace shutdown. If it’s `true`, a `SIGTERM` signal is sent to the specified request. See [Sending termination signal](https://intl.cloud.tencent.com/document/product/583/63969?from_cn_redirect=1#.E5.8F.91.E9.80.81.E7.BB.88.E6.AD.A2.E4.BF.A1.E5.8F.B7]. It’s set to `false` by default.
        :type GraceShutdown: bool
        """
        self.FunctionName = None
        self.InvokeRequestId = None
        self.Namespace = None
        self.GraceShutdown = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.InvokeRequestId = params.get("InvokeRequestId")
        self.Namespace = params.get("Namespace")
        self.GraceShutdown = params.get("GraceShutdown")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateAsyncEventResponse(AbstractModel):
    """TerminateAsyncEvent response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class TimeInterval(AbstractModel):
    """Left-closed-right-open time range between the start time and end time in the format of "%Y-%m-%d %H:%M:%S"

    """

    def __init__(self):
        r"""
        :param Start: Start time (inclusive) in the format of "%Y-%m-%d %H:%M:%S"
        :type Start: str
        :param End: End time (exclusive) in the format of "%Y-%m-%d %H:%M:%S"
        :type End: str
        """
        self.Start = None
        self.End = None


    def _deserialize(self, params):
        self.Start = params.get("Start")
        self.End = params.get("End")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Trigger(AbstractModel):
    """Trigger type

    """

    def __init__(self):
        r"""
        :param ModTime: Latest modification time of the trigger
        :type ModTime: str
        :param Type: Trigger type
        :type Type: str
        :param TriggerDesc: Detailed trigger configuration
        :type TriggerDesc: str
        :param TriggerName: Trigger name
        :type TriggerName: str
        :param AddTime: Creation time of the trigger
        :type AddTime: str
        :param Enable: Enabling switch
        :type Enable: int
        :param CustomArgument: Custom parameter
        :type CustomArgument: str
        :param AvailableStatus: Trigger status
        :type AvailableStatus: str
        :param ResourceId: Minimum resource ID of trigger
        :type ResourceId: str
        :param BindStatus: Trigger-Function binding status
        :type BindStatus: str
        :param TriggerAttribute: Trigger type. Two-way means that the trigger can be manipulated in both consoles, while one-way means that the trigger can be created only in the SCF Console
        :type TriggerAttribute: str
        :param Qualifier: The alias or version bound with the trigger
        :type Qualifier: str
        """
        self.ModTime = None
        self.Type = None
        self.TriggerDesc = None
        self.TriggerName = None
        self.AddTime = None
        self.Enable = None
        self.CustomArgument = None
        self.AvailableStatus = None
        self.ResourceId = None
        self.BindStatus = None
        self.TriggerAttribute = None
        self.Qualifier = None


    def _deserialize(self, params):
        self.ModTime = params.get("ModTime")
        self.Type = params.get("Type")
        self.TriggerDesc = params.get("TriggerDesc")
        self.TriggerName = params.get("TriggerName")
        self.AddTime = params.get("AddTime")
        self.Enable = params.get("Enable")
        self.CustomArgument = params.get("CustomArgument")
        self.AvailableStatus = params.get("AvailableStatus")
        self.ResourceId = params.get("ResourceId")
        self.BindStatus = params.get("BindStatus")
        self.TriggerAttribute = params.get("TriggerAttribute")
        self.Qualifier = params.get("Qualifier")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TriggerAction(AbstractModel):
    """Details of a scheduled provisioned concurrency scaling action

    """

    def __init__(self):
        r"""
        :param TriggerName: Scheduled action name
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type TriggerName: str
        :param TriggerProvisionedConcurrencyNum: Target provisioned concurrency of the scheduled scaling action 
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type TriggerProvisionedConcurrencyNum: int
        :param TriggerCronConfig: Trigger time of the scheduled action in Cron expression. Seven fields are required and should be separated with a space.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type TriggerCronConfig: str
        :param ProvisionedType: The provision type. Value: `Default`
Note: This field may return `null`, indicating that no valid value can be found.
        :type ProvisionedType: str
        """
        self.TriggerName = None
        self.TriggerProvisionedConcurrencyNum = None
        self.TriggerCronConfig = None
        self.ProvisionedType = None


    def _deserialize(self, params):
        self.TriggerName = params.get("TriggerName")
        self.TriggerProvisionedConcurrencyNum = params.get("TriggerProvisionedConcurrencyNum")
        self.TriggerCronConfig = params.get("TriggerCronConfig")
        self.ProvisionedType = params.get("ProvisionedType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TriggerCount(AbstractModel):
    """`TriggerCount` describes the numbers of triggers in different types

    """

    def __init__(self):
        r"""
        :param Cos: Number of COS triggers
        :type Cos: int
        :param Timer: Number of timer triggers
        :type Timer: int
        :param Cmq: Number of CMQ triggers
        :type Cmq: int
        :param Total: Total number of triggers
        :type Total: int
        :param Ckafka: Number of CKafka triggers
        :type Ckafka: int
        :param Apigw: Number of API Gateway triggers
        :type Apigw: int
        :param Cls: Number of CLS triggers
        :type Cls: int
        :param Clb: Number of CLB triggers
        :type Clb: int
        :param Mps: Number of MPS triggers
        :type Mps: int
        :param Cm: Number of CM triggers
        :type Cm: int
        :param Vod: Number of VOD triggers
        :type Vod: int
        :param Eb: Number of EventBridge triggers
Note: This field may return `null`, indicating that no valid values can be obtained.
        :type Eb: int
        """
        self.Cos = None
        self.Timer = None
        self.Cmq = None
        self.Total = None
        self.Ckafka = None
        self.Apigw = None
        self.Cls = None
        self.Clb = None
        self.Mps = None
        self.Cm = None
        self.Vod = None
        self.Eb = None


    def _deserialize(self, params):
        self.Cos = params.get("Cos")
        self.Timer = params.get("Timer")
        self.Cmq = params.get("Cmq")
        self.Total = params.get("Total")
        self.Ckafka = params.get("Ckafka")
        self.Apigw = params.get("Apigw")
        self.Cls = params.get("Cls")
        self.Clb = params.get("Clb")
        self.Mps = params.get("Mps")
        self.Cm = params.get("Cm")
        self.Vod = params.get("Vod")
        self.Eb = params.get("Eb")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TriggerInfo(AbstractModel):
    """Trigger information

    """

    def __init__(self):
        r"""
        :param Enable: Whether to enable
        :type Enable: int
        :param Qualifier: Function version or alias
        :type Qualifier: str
        :param TriggerName: Trigger name
        :type TriggerName: str
        :param Type: Trigger type
        :type Type: str
        :param TriggerDesc: Detailed configuration of trigger
        :type TriggerDesc: str
        :param AvailableStatus: Whether the trigger is available
        :type AvailableStatus: str
        :param CustomArgument: Custom parameter
Note: this field may return null, indicating that no valid values can be obtained.
        :type CustomArgument: str
        :param AddTime: Trigger creation time
        :type AddTime: str
        :param ModTime: Trigger last modified time
        :type ModTime: str
        :param ResourceId: Minimum resource ID of trigger
        :type ResourceId: str
        :param BindStatus: Trigger-Function binding status
        :type BindStatus: str
        :param TriggerAttribute: Trigger type. Two-way means that the trigger can be manipulated in both consoles, while one-way means that the trigger can be created only in the SCF Console
        :type TriggerAttribute: str
        """
        self.Enable = None
        self.Qualifier = None
        self.TriggerName = None
        self.Type = None
        self.TriggerDesc = None
        self.AvailableStatus = None
        self.CustomArgument = None
        self.AddTime = None
        self.ModTime = None
        self.ResourceId = None
        self.BindStatus = None
        self.TriggerAttribute = None


    def _deserialize(self, params):
        self.Enable = params.get("Enable")
        self.Qualifier = params.get("Qualifier")
        self.TriggerName = params.get("TriggerName")
        self.Type = params.get("Type")
        self.TriggerDesc = params.get("TriggerDesc")
        self.AvailableStatus = params.get("AvailableStatus")
        self.CustomArgument = params.get("CustomArgument")
        self.AddTime = params.get("AddTime")
        self.ModTime = params.get("ModTime")
        self.ResourceId = params.get("ResourceId")
        self.BindStatus = params.get("BindStatus")
        self.TriggerAttribute = params.get("TriggerAttribute")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateAliasRequest(AbstractModel):
    """UpdateAlias request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Function name
        :type FunctionName: str
        :param Name: Alias name
        :type Name: str
        :param FunctionVersion: Master version pointed to by the alias
        :type FunctionVersion: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param RoutingConfig: Routing information of alias, which is required if you need to specify an additional version for the alias.
        :type RoutingConfig: :class:`tencentcloud.scf.v20180416.models.RoutingConfig`
        :param Description: Alias description
        :type Description: str
        """
        self.FunctionName = None
        self.Name = None
        self.FunctionVersion = None
        self.Namespace = None
        self.RoutingConfig = None
        self.Description = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Name = params.get("Name")
        self.FunctionVersion = params.get("FunctionVersion")
        self.Namespace = params.get("Namespace")
        if params.get("RoutingConfig") is not None:
            self.RoutingConfig = RoutingConfig()
            self.RoutingConfig._deserialize(params.get("RoutingConfig"))
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateAliasResponse(AbstractModel):
    """UpdateAlias response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateFunctionCodeRequest(AbstractModel):
    """UpdateFunctionCode request structure.

    """

    def __init__(self):
        r"""
        :param FunctionName: Name of the function to be modified
        :type FunctionName: str
        :param Handler: Function handler name, which is in the `file name.function name` form. Use a period (.) to separate a file name and function name. The file name and function name must start and end with letters and contain 2-60 characters, including letters, digits, underscores (_), and hyphens (-).
        :type Handler: str
        :param CosBucketName: COS bucket name
        :type CosBucketName: str
        :param CosObjectName: COS object path
        :type CosObjectName: str
        :param ZipFile: It contains a function code file and its dependencies in the ZIP format. When you use this API, the ZIP file needs to be encoded with Base64. Up to 20 MB is supported.
        :type ZipFile: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param CosBucketRegion: COS region. Note: Beijing includes ap-beijing and ap-beijing-1.
        :type CosBucketRegion: str
        :param InstallDependency: Whether to install dependencies automatically
        :type InstallDependency: str
        :param EnvId: Function environment
        :type EnvId: str
        :param Publish: It specifies whether to synchronously release a new version during the update. The default value is `FALSE`, indicating not to release a new version.
        :type Publish: str
        :param Code: Function code
        :type Code: :class:`tencentcloud.scf.v20180416.models.Code`
        :param CodeSource: Code source. Valid values: ZipFile, Cos, Inline
        :type CodeSource: str
        """
        self.FunctionName = None
        self.Handler = None
        self.CosBucketName = None
        self.CosObjectName = None
        self.ZipFile = None
        self.Namespace = None
        self.CosBucketRegion = None
        self.InstallDependency = None
        self.EnvId = None
        self.Publish = None
        self.Code = None
        self.CodeSource = None


    def _deserialize(self, params):
        self.FunctionName = params.get("FunctionName")
        self.Handler = params.get("Handler")
        self.CosBucketName = params.get("CosBucketName")
        self.CosObjectName = params.get("CosObjectName")
        self.ZipFile = params.get("ZipFile")
        self.Namespace = params.get("Namespace")
        self.CosBucketRegion = params.get("CosBucketRegion")
        self.InstallDependency = params.get("InstallDependency")
        self.EnvId = params.get("EnvId")
        self.Publish = params.get("Publish")
        if params.get("Code") is not None:
            self.Code = Code()
            self.Code._deserialize(params.get("Code"))
        self.CodeSource = params.get("CodeSource")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateFunctionCodeResponse(AbstractModel):
    """UpdateFunctionCode response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateFunctionEventInvokeConfigRequest(AbstractModel):
    """UpdateFunctionEventInvokeConfig request structure.

    """

    def __init__(self):
        r"""
        :param AsyncTriggerConfig: Async retry configuration information
        :type AsyncTriggerConfig: :class:`tencentcloud.scf.v20180416.models.AsyncTriggerConfig`
        :param FunctionName: Function name
        :type FunctionName: str
        :param Namespace: Function namespace. Default value: default
        :type Namespace: str
        """
        self.AsyncTriggerConfig = None
        self.FunctionName = None
        self.Namespace = None


    def _deserialize(self, params):
        if params.get("AsyncTriggerConfig") is not None:
            self.AsyncTriggerConfig = AsyncTriggerConfig()
            self.AsyncTriggerConfig._deserialize(params.get("AsyncTriggerConfig"))
        self.FunctionName = params.get("FunctionName")
        self.Namespace = params.get("Namespace")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateFunctionEventInvokeConfigResponse(AbstractModel):
    """UpdateFunctionEventInvokeConfig response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateNamespaceRequest(AbstractModel):
    """UpdateNamespace request structure.

    """

    def __init__(self):
        r"""
        :param Namespace: Namespace name
        :type Namespace: str
        :param Description: Namespace description
        :type Description: str
        """
        self.Namespace = None
        self.Description = None


    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateNamespaceResponse(AbstractModel):
    """UpdateNamespace response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateTriggerStatusRequest(AbstractModel):
    """UpdateTriggerStatus request structure.

    """

    def __init__(self):
        r"""
        :param Enable: Initial status of the trigger. Values: `OPEN` (enabled); `CLOSE` disabled)
        :type Enable: str
        :param FunctionName: Function name.
        :type FunctionName: str
        :param TriggerName: Trigger name
        :type TriggerName: str
        :param Type: Trigger Type
        :type Type: str
        :param Qualifier: Function version. It defaults to `$LATEST`. It’s recommended to use `[$DEFAULT](https://intl.cloud.tencent.com/document/product/583/36149?from_cn_redirect=1#.E9.BB.98.E8.AE.A4.E5.88.AB.E5.90.8D)` for canary release.
        :type Qualifier: str
        :param Namespace: Function namespace
        :type Namespace: str
        :param TriggerDesc: To update a COS trigger, this field is required. It stores the data {"event":"cos:ObjectCreated:*"} in the JSON format. The data content of this field is in the same format as that of SetTrigger. This field is optional if a scheduled trigger or CMQ trigger is to be deleted.
        :type TriggerDesc: str
        """
        self.Enable = None
        self.FunctionName = None
        self.TriggerName = None
        self.Type = None
        self.Qualifier = None
        self.Namespace = None
        self.TriggerDesc = None


    def _deserialize(self, params):
        self.Enable = params.get("Enable")
        self.FunctionName = params.get("FunctionName")
        self.TriggerName = params.get("TriggerName")
        self.Type = params.get("Type")
        self.Qualifier = params.get("Qualifier")
        self.Namespace = params.get("Namespace")
        self.TriggerDesc = params.get("TriggerDesc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateTriggerStatusResponse(AbstractModel):
    """UpdateTriggerStatus response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UsageInfo(AbstractModel):
    """Usage information

    """

    def __init__(self):
        r"""
        :param NamespacesCount: Number of namespaces
        :type NamespacesCount: int
        :param Namespace: Namespace details
        :type Namespace: list of NamespaceUsage
        :param TotalConcurrencyMem: Upper limit of user concurrency memory in the current region
        :type TotalConcurrencyMem: int
        :param TotalAllocatedConcurrencyMem: Quota of configured user concurrency memory in the current region
        :type TotalAllocatedConcurrencyMem: int
        :param UserConcurrencyMemLimit: Quota of account concurrency actually configured by user
        :type UserConcurrencyMemLimit: int
        """
        self.NamespacesCount = None
        self.Namespace = None
        self.TotalConcurrencyMem = None
        self.TotalAllocatedConcurrencyMem = None
        self.UserConcurrencyMemLimit = None


    def _deserialize(self, params):
        self.NamespacesCount = params.get("NamespacesCount")
        if params.get("Namespace") is not None:
            self.Namespace = []
            for item in params.get("Namespace"):
                obj = NamespaceUsage()
                obj._deserialize(item)
                self.Namespace.append(obj)
        self.TotalConcurrencyMem = params.get("TotalConcurrencyMem")
        self.TotalAllocatedConcurrencyMem = params.get("TotalAllocatedConcurrencyMem")
        self.UserConcurrencyMemLimit = params.get("UserConcurrencyMemLimit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VersionMatch(AbstractModel):
    """Function version with match rule

    """

    def __init__(self):
        r"""
        :param Version: Function version name
        :type Version: str
        :param Key: Matching rule key. When the API is called, pass in the `key` to route the request to the specified version based on the matching rule
Header method:
Enter "invoke.headers.User" for `key` and pass in `RoutingKey:{"User":"value"}` when invoking a function through `invoke` for invocation based on rule matching
        :type Key: str
        :param Method: Match method. Valid values:
range: range match
exact: exact string match
        :type Method: str
        :param Expression: Rule requirements for range match:
It should be described in an open or closed range, i.e., `(a,b)` or `[a,b]`, where both a and b are integers
Rule requirements for exact match:
Exact string match
        :type Expression: str
        """
        self.Version = None
        self.Key = None
        self.Method = None
        self.Expression = None


    def _deserialize(self, params):
        self.Version = params.get("Version")
        self.Key = params.get("Key")
        self.Method = params.get("Method")
        self.Expression = params.get("Expression")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VersionProvisionedConcurrencyInfo(AbstractModel):
    """Provisioned concurrency information of function version, including the set provisioned concurrency amount, available provisioned concurrency amount, and provisioned concurrency setting task status.

    """

    def __init__(self):
        r"""
        :param AllocatedProvisionedConcurrencyNum: Set provisioned concurrency amount.
        :type AllocatedProvisionedConcurrencyNum: int
        :param AvailableProvisionedConcurrencyNum: Currently available provisioned concurrency amount.
        :type AvailableProvisionedConcurrencyNum: int
        :param Status: Provisioned concurrency setting task status. `Done`: completed; `InProgress`: in progress; `Failed`: partially or completely failed.
        :type Status: str
        :param StatusReason: Status description of provisioned concurrency setting task.
        :type StatusReason: str
        :param Qualifier: Function version number
        :type Qualifier: str
        :param TriggerActions: List of scheduled provisioned concurrency scaling actions
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type TriggerActions: list of TriggerAction
        """
        self.AllocatedProvisionedConcurrencyNum = None
        self.AvailableProvisionedConcurrencyNum = None
        self.Status = None
        self.StatusReason = None
        self.Qualifier = None
        self.TriggerActions = None


    def _deserialize(self, params):
        self.AllocatedProvisionedConcurrencyNum = params.get("AllocatedProvisionedConcurrencyNum")
        self.AvailableProvisionedConcurrencyNum = params.get("AvailableProvisionedConcurrencyNum")
        self.Status = params.get("Status")
        self.StatusReason = params.get("StatusReason")
        self.Qualifier = params.get("Qualifier")
        if params.get("TriggerActions") is not None:
            self.TriggerActions = []
            for item in params.get("TriggerActions"):
                obj = TriggerAction()
                obj._deserialize(item)
                self.TriggerActions.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VersionWeight(AbstractModel):
    """Function version with weight

    """

    def __init__(self):
        r"""
        :param Version: Function version name
        :type Version: str
        :param Weight: Version weight
        :type Weight: float
        """
        self.Version = None
        self.Weight = None


    def _deserialize(self, params):
        self.Version = params.get("Version")
        self.Weight = params.get("Weight")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        