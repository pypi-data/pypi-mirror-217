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


class AddUserContactRequest(AbstractModel):
    """AddUserContact request structure.

    """

    def __init__(self):
        r"""
        :param Name: Recipient name, which can contain up to 20 letters, digits, spaces, and symbols `!@#$%^&*()_+-=()` and cannot begin with an underscore.
        :type Name: str
        :param ContactInfo: Email address, which can contain letters, digits, underscores, and the @ symbol, cannot begin with an underscore, and must be unique.
        :type ContactInfo: str
        :param Product: Service type, which is fixed to `mysql`.
        :type Product: str
        """
        self.Name = None
        self.ContactInfo = None
        self.Product = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.ContactInfo = params.get("ContactInfo")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddUserContactResponse(AbstractModel):
    """AddUserContact response structure.

    """

    def __init__(self):
        r"""
        :param Id: ID of the successfully added recipient.
        :type Id: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Id = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.RequestId = params.get("RequestId")


class ContactItem(AbstractModel):
    """Recipient description.

    """

    def __init__(self):
        r"""
        :param Id: Recipient ID.
        :type Id: int
        :param Name: Recipient name.
        :type Name: str
        :param Mail: Recipient email.
        :type Mail: str
        """
        self.Id = None
        self.Name = None
        self.Mail = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.Mail = params.get("Mail")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDBDiagReportTaskRequest(AbstractModel):
    """CreateDBDiagReportTask request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time, such as "2020-11-08T14:00:00+08:00".
        :type StartTime: str
        :param EndTime: End time, such as "2020-11-09T14:00:00+08:00".
        :type EndTime: str
        :param SendMailFlag: Whether to send an email. Valid values: `0` (yes), `1` (no).
        :type SendMailFlag: int
        :param ContactPerson: Array of the IDs of recipients to receive email.
        :type ContactPerson: list of int
        :param ContactGroup: Array of IDs of recipient groups to receive email.
        :type ContactGroup: list of int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.SendMailFlag = None
        self.ContactPerson = None
        self.ContactGroup = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.SendMailFlag = params.get("SendMailFlag")
        self.ContactPerson = params.get("ContactPerson")
        self.ContactGroup = params.get("ContactGroup")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDBDiagReportTaskResponse(AbstractModel):
    """CreateDBDiagReportTask response structure.

    """

    def __init__(self):
        r"""
        :param AsyncRequestId: Async task request ID, which can be used to query the execution result of an async task.
Note: This field may return null, indicating that no valid values can be obtained.
        :type AsyncRequestId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AsyncRequestId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.RequestId = params.get("RequestId")


class CreateDBDiagReportUrlRequest(AbstractModel):
    """CreateDBDiagReportUrl request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param AsyncRequestId: Health report task ID, which can be queried through `DescribeDBDiagReportTasks`.
        :type AsyncRequestId: int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.AsyncRequestId = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDBDiagReportUrlResponse(AbstractModel):
    """CreateDBDiagReportUrl response structure.

    """

    def __init__(self):
        r"""
        :param ReportUrl: Health report URL.
        :type ReportUrl: str
        :param ExpireTime: Expiration timestamp of the health report URL (in seconds).
        :type ExpireTime: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ReportUrl = None
        self.ExpireTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReportUrl = params.get("ReportUrl")
        self.ExpireTime = params.get("ExpireTime")
        self.RequestId = params.get("RequestId")


class CreateKillTaskRequest(AbstractModel):
    """CreateKillTask request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: ID of the instance associated with the session killing task.
        :type InstanceId: str
        :param Duration: Task duration in seconds. Pass in `-1` to stop the task manually.
        :type Duration: int
        :param Host: Client IP, which is a task filter.
        :type Host: str
        :param DB: Database name, which is a task filter. Multiple database names are separated by comma.
        :type DB: str
        :param Command: Related command, which is a task filter. Multiple commands are separated by comma.
        :type Command: str
        :param Info: Task filter. Filtering by single filter prefix is supported.
        :type Info: str
        :param User: User type, which is a task filter.
        :type User: str
        :param Time: Session duration in seconds, which is a task filter.
        :type Time: int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.Duration = None
        self.Host = None
        self.DB = None
        self.Command = None
        self.Info = None
        self.User = None
        self.Time = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Duration = params.get("Duration")
        self.Host = params.get("Host")
        self.DB = params.get("DB")
        self.Command = params.get("Command")
        self.Info = params.get("Info")
        self.User = params.get("User")
        self.Time = params.get("Time")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateKillTaskResponse(AbstractModel):
    """CreateKillTask response structure.

    """

    def __init__(self):
        r"""
        :param Status: Task status. `1` is returned if the session killing task is successfully created.
        :type Status: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class CreateMailProfileRequest(AbstractModel):
    """CreateMailProfile request structure.

    """

    def __init__(self):
        r"""
        :param ProfileInfo: Email configuration.
        :type ProfileInfo: :class:`tencentcloud.dbbrain.v20210527.models.ProfileInfo`
        :param ProfileLevel: Configuration level. Valid values: `User` (user-level), `Instance` (instance-level). For database inspection emails, it should be `User`. For scheduled task emails, it should be `Instance`.
        :type ProfileLevel: str
        :param ProfileName: Configuration name, which needs to be unique. For database inspection emails, this name can be customized as needed. For scheduled task emails, the name should be in the format of "scheduler_" + {instanceId}, such as "schduler_cdb-test".
        :type ProfileName: str
        :param ProfileType: Configuration type. Valid values: `dbScan_mail_configuration` (email configuration of the database inspection report), `scheduler_mail_configuration` (email configuration of the scheduled task report).
        :type ProfileType: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL).
        :type Product: str
        :param BindInstanceIds: Instance ID bound with the configuration, which is set when the configuration level is `Instance`. Only one instance can be bound at a time. When the configuration level is `User`, leave this parameter empty.
        :type BindInstanceIds: list of str
        """
        self.ProfileInfo = None
        self.ProfileLevel = None
        self.ProfileName = None
        self.ProfileType = None
        self.Product = None
        self.BindInstanceIds = None


    def _deserialize(self, params):
        if params.get("ProfileInfo") is not None:
            self.ProfileInfo = ProfileInfo()
            self.ProfileInfo._deserialize(params.get("ProfileInfo"))
        self.ProfileLevel = params.get("ProfileLevel")
        self.ProfileName = params.get("ProfileName")
        self.ProfileType = params.get("ProfileType")
        self.Product = params.get("Product")
        self.BindInstanceIds = params.get("BindInstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateMailProfileResponse(AbstractModel):
    """CreateMailProfile response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateProxySessionKillTaskRequest(AbstractModel):
    """CreateProxySessionKillTask request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Product: Service type. Valid value: `redis` (TencentDB for Redis).
        :type Product: str
        """
        self.InstanceId = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateProxySessionKillTaskResponse(AbstractModel):
    """CreateProxySessionKillTask response structure.

    """

    def __init__(self):
        r"""
        :param AsyncRequestId: Async task ID that is returned after the session killing task is created.
        :type AsyncRequestId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AsyncRequestId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.RequestId = params.get("RequestId")


class CreateSchedulerMailProfileRequest(AbstractModel):
    """CreateSchedulerMailProfile request structure.

    """

    def __init__(self):
        r"""
        :param WeekConfiguration: Value range: 1-7, representing Monday to Sunday respectively.
        :type WeekConfiguration: list of int
        :param ProfileInfo: Email configuration.
        :type ProfileInfo: :class:`tencentcloud.dbbrain.v20210527.models.ProfileInfo`
        :param ProfileName: Configuration name, which needs to be unique. For scheduled task emails, the name should be in the format of "scheduler_" + {instanceId}, such as "schduler_cdb-test".
        :type ProfileName: str
        :param BindInstanceId: ID of the instance for which to configure subscription.
        :type BindInstanceId: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.WeekConfiguration = None
        self.ProfileInfo = None
        self.ProfileName = None
        self.BindInstanceId = None
        self.Product = None


    def _deserialize(self, params):
        self.WeekConfiguration = params.get("WeekConfiguration")
        if params.get("ProfileInfo") is not None:
            self.ProfileInfo = ProfileInfo()
            self.ProfileInfo._deserialize(params.get("ProfileInfo"))
        self.ProfileName = params.get("ProfileName")
        self.BindInstanceId = params.get("BindInstanceId")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSchedulerMailProfileResponse(AbstractModel):
    """CreateSchedulerMailProfile response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateSecurityAuditLogExportTaskRequest(AbstractModel):
    """CreateSecurityAuditLogExportTask request structure.

    """

    def __init__(self):
        r"""
        :param SecAuditGroupId: Security audit group ID.
        :type SecAuditGroupId: str
        :param StartTime: Exported log start time, such as 2020-12-28 00:00:00.
        :type StartTime: str
        :param EndTime: Exported log end time, such as 2020-12-28 01:00:00.
        :type EndTime: str
        :param Product: Service type. Valid value: `mysql` (TencentDB for MySQL).
        :type Product: str
        :param DangerLevels: List of log risk levels. Valid values: `0` (no risk), `1` (low risk), `2` (medium risk), `3` (high risk).
        :type DangerLevels: list of int
        """
        self.SecAuditGroupId = None
        self.StartTime = None
        self.EndTime = None
        self.Product = None
        self.DangerLevels = None


    def _deserialize(self, params):
        self.SecAuditGroupId = params.get("SecAuditGroupId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Product = params.get("Product")
        self.DangerLevels = params.get("DangerLevels")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSecurityAuditLogExportTaskResponse(AbstractModel):
    """CreateSecurityAuditLogExportTask response structure.

    """

    def __init__(self):
        r"""
        :param AsyncRequestId: Log export task Id.
        :type AsyncRequestId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AsyncRequestId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.RequestId = params.get("RequestId")


class DeleteDBDiagReportTasksRequest(AbstractModel):
    """DeleteDBDiagReportTasks request structure.

    """

    def __init__(self):
        r"""
        :param AsyncRequestIds: List of IDs of tasks to be deleted
        :type AsyncRequestIds: list of int
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.AsyncRequestIds = None
        self.InstanceId = None
        self.Product = None


    def _deserialize(self, params):
        self.AsyncRequestIds = params.get("AsyncRequestIds")
        self.InstanceId = params.get("InstanceId")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDBDiagReportTasksResponse(AbstractModel):
    """DeleteDBDiagReportTasks response structure.

    """

    def __init__(self):
        r"""
        :param Status: Task deletion status (`0`: Successful)
        :type Status: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DeleteSecurityAuditLogExportTasksRequest(AbstractModel):
    """DeleteSecurityAuditLogExportTasks request structure.

    """

    def __init__(self):
        r"""
        :param SecAuditGroupId: Security audit group ID.
        :type SecAuditGroupId: str
        :param AsyncRequestIds: List of log export task IDs. This API will ignore task IDs that do not exist or have been deleted.
        :type AsyncRequestIds: list of int non-negative
        :param Product: Service type. Valid value: `mysql` (TencentDB for MySQL).
        :type Product: str
        """
        self.SecAuditGroupId = None
        self.AsyncRequestIds = None
        self.Product = None


    def _deserialize(self, params):
        self.SecAuditGroupId = params.get("SecAuditGroupId")
        self.AsyncRequestIds = params.get("AsyncRequestIds")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSecurityAuditLogExportTasksResponse(AbstractModel):
    """DeleteSecurityAuditLogExportTasks response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAllUserContactRequest(AbstractModel):
    """DescribeAllUserContact request structure.

    """

    def __init__(self):
        r"""
        :param Product: Service type, which is fixed to `mysql`.
        :type Product: str
        :param Names: Array of recipient names. Fuzzy search is supported.
        :type Names: list of str
        """
        self.Product = None
        self.Names = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.Names = params.get("Names")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAllUserContactResponse(AbstractModel):
    """DescribeAllUserContact response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of recipients.
        :type TotalCount: int
        :param Contacts: Recipient information.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Contacts: list of ContactItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Contacts = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Contacts") is not None:
            self.Contacts = []
            for item in params.get("Contacts"):
                obj = ContactItem()
                obj._deserialize(item)
                self.Contacts.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAllUserGroupRequest(AbstractModel):
    """DescribeAllUserGroup request structure.

    """

    def __init__(self):
        r"""
        :param Product: Service type, which is fixed to `mysql`.
        :type Product: str
        :param Names: Array of recipient group names. Fuzzy search is supported.
        :type Names: list of str
        """
        self.Product = None
        self.Names = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.Names = params.get("Names")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAllUserGroupResponse(AbstractModel):
    """DescribeAllUserGroup response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of groups.
        :type TotalCount: int
        :param Groups: Group information.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Groups: list of GroupItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Groups = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Groups") is not None:
            self.Groups = []
            for item in params.get("Groups"):
                obj = GroupItem()
                obj._deserialize(item)
                self.Groups.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBDiagEventRequest(AbstractModel):
    """DescribeDBDiagEvent request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param EventId: Event ID, which can be obtained through the `DescribeDBDiagHistory` API.
        :type EventId: int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.EventId = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.EventId = params.get("EventId")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBDiagEventResponse(AbstractModel):
    """DescribeDBDiagEvent response structure.

    """

    def __init__(self):
        r"""
        :param DiagItem: Diagnosis item.
        :type DiagItem: str
        :param DiagType: Diagnosis type.
        :type DiagType: str
        :param EventId: Event ID.
        :type EventId: int
        :param Explanation: Diagnosis event details. If there is no additional explanation information, the output will be empty.
        :type Explanation: str
        :param Outline: Diagnosis summary.
        :type Outline: str
        :param Problem: Found problem.
        :type Problem: str
        :param Severity: Severity, which can be divided into 5 levels: `1` (Critical), `2` (Severe), `3` (Alarm), `4` (Reminder), `5` (healthy).
        :type Severity: int
        :param StartTime: Start time
        :type StartTime: str
        :param Suggestions: Suggestions. If there are no suggestions, the output will be empty.
        :type Suggestions: str
        :param Metric: Reserved field.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Metric: str
        :param EndTime: End time.
        :type EndTime: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DiagItem = None
        self.DiagType = None
        self.EventId = None
        self.Explanation = None
        self.Outline = None
        self.Problem = None
        self.Severity = None
        self.StartTime = None
        self.Suggestions = None
        self.Metric = None
        self.EndTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DiagItem = params.get("DiagItem")
        self.DiagType = params.get("DiagType")
        self.EventId = params.get("EventId")
        self.Explanation = params.get("Explanation")
        self.Outline = params.get("Outline")
        self.Problem = params.get("Problem")
        self.Severity = params.get("Severity")
        self.StartTime = params.get("StartTime")
        self.Suggestions = params.get("Suggestions")
        self.Metric = params.get("Metric")
        self.EndTime = params.get("EndTime")
        self.RequestId = params.get("RequestId")


class DescribeDBDiagEventsRequest(AbstractModel):
    """DescribeDBDiagEvents request structure.

    """

    def __init__(self):
        r"""
        :param StartTime: Start time in the format of “2021-05-27 00:00:00”. The earliest time that can be queried is 30 days before the current time.
        :type StartTime: str
        :param EndTime: End time in the format of "2021-05-27 01:00:00". The interval between the end time and the start time can be up to 7 days.
        :type EndTime: str
        :param Severities: Risk level list. Valid values in descending order of severity: `1` (critical), `2` (serious), `3` (alarm), `4` (warning), `5` (healthy).
        :type Severities: list of int
        :param InstanceIds: Instance ID list.
        :type InstanceIds: list of str
        :param Offset: Offset. Default value: 0.
        :type Offset: int
        :param Limit: Number of returned results. Default value: 20. Maximum value: 50.
        :type Limit: int
        """
        self.StartTime = None
        self.EndTime = None
        self.Severities = None
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Severities = params.get("Severities")
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBDiagEventsResponse(AbstractModel):
    """DescribeDBDiagEvents response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of diagnosis events.
        :type TotalCount: int
        :param Items: Diagnosis event list.
        :type Items: list of DiagHistoryEventItem
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
                obj = DiagHistoryEventItem()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBDiagHistoryRequest(AbstractModel):
    """DescribeDBDiagHistory request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time, such as "2019-09-10 12:13:14".
        :type StartTime: str
        :param EndTime: End time, such as "2019-09-11 12:13:14". The interval between the end time and the start time can be up to 2 days.
        :type EndTime: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBDiagHistoryResponse(AbstractModel):
    """DescribeDBDiagHistory response structure.

    """

    def __init__(self):
        r"""
        :param Events: Event description.
        :type Events: list of DiagHistoryEventItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Events = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Events") is not None:
            self.Events = []
            for item in params.get("Events"):
                obj = DiagHistoryEventItem()
                obj._deserialize(item)
                self.Events.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBDiagReportTasksRequest(AbstractModel):
    """DescribeDBDiagReportTasks request structure.

    """

    def __init__(self):
        r"""
        :param StartTime: Start time of the first task in the format of yyyy-MM-dd HH:mm:ss, such as 2019-09-10 12:13:14. It is used for queries by time range.
        :type StartTime: str
        :param EndTime: End time of the last task in the format of yyyy-MM-dd HH:mm:ss, such as 2019-09-10 12:13:14. It is used for queries by time range.
        :type EndTime: str
        :param InstanceIds: Array of instance IDs, which is used to filter the task list of the specified instance.
        :type InstanceIds: list of str
        :param Sources: Source that triggers the task. Valid values: `DAILY_INSPECTION` (instance inspection), `SCHEDULED` (scheduled task), and `MANUAL` (manual trigger).
        :type Sources: list of str
        :param HealthLevels: Health level. Valid values: `HEALTH` (healthy), `SUB_HEALTH` (suboptimal), `RISK` (risky), and `HIGH_RISK` (critical).
        :type HealthLevels: str
        :param TaskStatuses: Task status. Valid values: `created` (created), `chosen` (to be executed), `running` (being executed), `failed` (failed), and `finished` (completed).
        :type TaskStatuses: str
        :param Offset: Offset. Default value: `0`.
        :type Offset: int
        :param Limit: Number of returned results. Default value: `20`. Maximum value: `100`.
        :type Limit: int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.StartTime = None
        self.EndTime = None
        self.InstanceIds = None
        self.Sources = None
        self.HealthLevels = None
        self.TaskStatuses = None
        self.Offset = None
        self.Limit = None
        self.Product = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.InstanceIds = params.get("InstanceIds")
        self.Sources = params.get("Sources")
        self.HealthLevels = params.get("HealthLevels")
        self.TaskStatuses = params.get("TaskStatuses")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBDiagReportTasksResponse(AbstractModel):
    """DescribeDBDiagReportTasks response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of tasks.
        :type TotalCount: int
        :param Tasks: List of tasks.
        :type Tasks: list of HealthReportTask
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Tasks = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = HealthReportTask()
                obj._deserialize(item)
                self.Tasks.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBSpaceStatusRequest(AbstractModel):
    """DescribeDBSpaceStatus request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param RangeDays: Query period in days. The end date is the current date, and the query period is 7 days by default.
        :type RangeDays: int
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.RangeDays = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RangeDays = params.get("RangeDays")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBSpaceStatusResponse(AbstractModel):
    """DescribeDBSpaceStatus response structure.

    """

    def __init__(self):
        r"""
        :param Growth: Disk usage growth in MB.
        :type Growth: int
        :param Remain: Available disk space in MB.
        :type Remain: int
        :param Total: Total disk space in MB.
        :type Total: int
        :param AvailableDays: Estimated number of available days.
        :type AvailableDays: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Growth = None
        self.Remain = None
        self.Total = None
        self.AvailableDays = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Growth = params.get("Growth")
        self.Remain = params.get("Remain")
        self.Total = params.get("Total")
        self.AvailableDays = params.get("AvailableDays")
        self.RequestId = params.get("RequestId")


class DescribeDiagDBInstancesRequest(AbstractModel):
    """DescribeDiagDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param IsSupported: Whether it is an instance supported by DBbrain. It is fixed to `true`.
        :type IsSupported: bool
        :param Product: Service type. Valid values: mysql (TencentDB for MySQL), cynosdb (TDSQL-C for MySQL). Default value: mysql.
        :type Product: str
        :param Offset: Pagination parameter indicating the offset.
        :type Offset: int
        :param Limit: Pagination parameter. Maximum value: 100.
        :type Limit: int
        :param InstanceNames: Query by instance name.
        :type InstanceNames: list of str
        :param InstanceIds: Query by instance ID.
        :type InstanceIds: list of str
        :param Regions: Query by region.
        :type Regions: list of str
        """
        self.IsSupported = None
        self.Product = None
        self.Offset = None
        self.Limit = None
        self.InstanceNames = None
        self.InstanceIds = None
        self.Regions = None


    def _deserialize(self, params):
        self.IsSupported = params.get("IsSupported")
        self.Product = params.get("Product")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InstanceNames = params.get("InstanceNames")
        self.InstanceIds = params.get("InstanceIds")
        self.Regions = params.get("Regions")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDiagDBInstancesResponse(AbstractModel):
    """DescribeDiagDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of instances.
        :type TotalCount: int
        :param DbScanStatus: Status of all instance inspection. 0: all instance inspection enabled, 1: all instance inspection disabled.
        :type DbScanStatus: int
        :param Items: Instance information.
        :type Items: list of InstanceInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.DbScanStatus = None
        self.Items = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        self.DbScanStatus = params.get("DbScanStatus")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = InstanceInfo()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeHealthScoreRequest(AbstractModel):
    """DescribeHealthScore request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID for which to get the health score.
        :type InstanceId: str
        :param Time: Time to get the health score in the format of `2019-09-10 12:13:14`.
        :type Time: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.Time = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Time = params.get("Time")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeHealthScoreResponse(AbstractModel):
    """DescribeHealthScore response structure.

    """

    def __init__(self):
        r"""
        :param Data: Health score and deduction for exceptions.
        :type Data: :class:`tencentcloud.dbbrain.v20210527.models.HealthScoreInfo`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = HealthScoreInfo()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeMailProfileRequest(AbstractModel):
    """DescribeMailProfile request structure.

    """

    def __init__(self):
        r"""
        :param ProfileType: Configuration type. Valid values: `dbScan_mail_configuration` (email configuration of the database inspection report), `scheduler_mail_configuration` (email configuration of the scheduled task report).
        :type ProfileType: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        :param Offset: Pagination offset.
        :type Offset: int
        :param Limit: Number of results per page in paginated queries. Maximum value: `50`.
        :type Limit: int
        :param ProfileName: Query by email configuration name. The name of the scheduled task email configuration should be in the format of "scheduler_"+{instanceId}.
        :type ProfileName: str
        """
        self.ProfileType = None
        self.Product = None
        self.Offset = None
        self.Limit = None
        self.ProfileName = None


    def _deserialize(self, params):
        self.ProfileType = params.get("ProfileType")
        self.Product = params.get("Product")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.ProfileName = params.get("ProfileName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMailProfileResponse(AbstractModel):
    """DescribeMailProfile response structure.

    """

    def __init__(self):
        r"""
        :param ProfileList: Email configuration details.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProfileList: list of UserProfile
        :param TotalCount: Total number of the configured emails.
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProfileList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ProfileList") is not None:
            self.ProfileList = []
            for item in params.get("ProfileList"):
                obj = UserProfile()
                obj._deserialize(item)
                self.ProfileList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeMySqlProcessListRequest(AbstractModel):
    """DescribeMySqlProcessList request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param ID: Thread ID, which is used to filter the thread list.
        :type ID: int
        :param User: Thread operation account name, which is used to filter the thread list.
        :type User: str
        :param Host: Thread operation host address, which is used to filter the thread list.
        :type Host: str
        :param DB: Thread operation database, which is used to filter the thread list.
        :type DB: str
        :param State: Thread operation status, which is used to filter the thread list.
        :type State: str
        :param Command: Thread execution type, which is used to filter the thread list.
        :type Command: str
        :param Time: Minimum operation duration of the thread in seconds, which is used to filter the list of threads whose operation duration is greater than this value.
        :type Time: int
        :param Info: Thread operation statement, which is used to filter the thread list.
        :type Info: str
        :param Limit: Number of returned results. Default value: 20.
        :type Limit: int
        :param Product: Service type. Valid values: mysql (TencentDB for MySQL), cynosdb (TDSQL-C for MySQL). Default value: mysql.
        :type Product: str
        """
        self.InstanceId = None
        self.ID = None
        self.User = None
        self.Host = None
        self.DB = None
        self.State = None
        self.Command = None
        self.Time = None
        self.Info = None
        self.Limit = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ID = params.get("ID")
        self.User = params.get("User")
        self.Host = params.get("Host")
        self.DB = params.get("DB")
        self.State = params.get("State")
        self.Command = params.get("Command")
        self.Time = params.get("Time")
        self.Info = params.get("Info")
        self.Limit = params.get("Limit")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMySqlProcessListResponse(AbstractModel):
    """DescribeMySqlProcessList response structure.

    """

    def __init__(self):
        r"""
        :param ProcessList: List of real-time threads.
        :type ProcessList: list of MySqlProcess
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProcessList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ProcessList") is not None:
            self.ProcessList = []
            for item in params.get("ProcessList"):
                obj = MySqlProcess()
                obj._deserialize(item)
                self.ProcessList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProxyProcessStatisticsRequest(AbstractModel):
    """DescribeProxyProcessStatistics request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param InstanceProxyId: The proxy ID you want to query under the instance
        :type InstanceProxyId: str
        :param Limit: Number of returned results.
        :type Limit: int
        :param Product: Service type. Valid value: `redis` (TencentDB for Redis).
        :type Product: str
        :param Offset: Offset. Default value: `0`.
        :type Offset: int
        :param SortBy: Sort by field. Valid values: `AllConn`, `ActiveConn`, `Ip`.
        :type SortBy: str
        :param OrderDirection: Sorting order. Valid values: `DESC`, `ASC`.
        :type OrderDirection: str
        """
        self.InstanceId = None
        self.InstanceProxyId = None
        self.Limit = None
        self.Product = None
        self.Offset = None
        self.SortBy = None
        self.OrderDirection = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceProxyId = params.get("InstanceProxyId")
        self.Limit = params.get("Limit")
        self.Product = params.get("Product")
        self.Offset = params.get("Offset")
        self.SortBy = params.get("SortBy")
        self.OrderDirection = params.get("OrderDirection")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeProxyProcessStatisticsResponse(AbstractModel):
    """DescribeProxyProcessStatistics response structure.

    """

    def __init__(self):
        r"""
        :param ProcessStatistics: Real-time session statistics.
        :type ProcessStatistics: :class:`tencentcloud.dbbrain.v20210527.models.ProcessStatistic`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.ProcessStatistics = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ProcessStatistics") is not None:
            self.ProcessStatistics = ProcessStatistic()
            self.ProcessStatistics._deserialize(params.get("ProcessStatistics"))
        self.RequestId = params.get("RequestId")


class DescribeProxySessionKillTasksRequest(AbstractModel):
    """DescribeProxySessionKillTasks request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param AsyncRequestIds: The async session killing task ID, which is obtained after the API `CreateProxySessionKillTask` is successfully called.
        :type AsyncRequestIds: list of int
        :param Product: Service type. Valid value: `redis` (TencentDB for Redis).
        :type Product: str
        """
        self.InstanceId = None
        self.AsyncRequestIds = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.AsyncRequestIds = params.get("AsyncRequestIds")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeProxySessionKillTasksResponse(AbstractModel):
    """DescribeProxySessionKillTasks response structure.

    """

    def __init__(self):
        r"""
        :param Tasks: Session killing task details.
        :type Tasks: list of TaskInfo
        :param TotalCount: Total number of tasks.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Tasks = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = TaskInfo()
                obj._deserialize(item)
                self.Tasks.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeRedisTopKeyPrefixListRequest(AbstractModel):
    """DescribeRedisTopKeyPrefixList request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Date: Date for query, such as `2021-05-27`. You can select a date as early as in the last 30 days for query.
        :type Date: str
        :param Product: Service type. Valid value: `redis` (TencentDB for Redis).
        :type Product: str
        :param Limit: The number of queried items. Default value: `20`. Max value: `100`.
        :type Limit: int
        """
        self.InstanceId = None
        self.Date = None
        self.Product = None
        self.Limit = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Date = params.get("Date")
        self.Product = params.get("Product")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeRedisTopKeyPrefixListResponse(AbstractModel):
    """DescribeRedisTopKeyPrefixList response structure.

    """

    def __init__(self):
        r"""
        :param Items: List of top key prefixes
        :type Items: list of RedisPreKeySpaceData
        :param Timestamp: Data collection timestamp in seconds
        :type Timestamp: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Items = None
        self.Timestamp = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = RedisPreKeySpaceData()
                obj._deserialize(item)
                self.Items.append(obj)
        self.Timestamp = params.get("Timestamp")
        self.RequestId = params.get("RequestId")


class DescribeSecurityAuditLogDownloadUrlsRequest(AbstractModel):
    """DescribeSecurityAuditLogDownloadUrls request structure.

    """

    def __init__(self):
        r"""
        :param SecAuditGroupId: Security audit group ID.
        :type SecAuditGroupId: str
        :param AsyncRequestId: Async task Id.
        :type AsyncRequestId: int
        :param Product: Service type. Valid value: `mysql` (TencentDB for MySQL).
        :type Product: str
        """
        self.SecAuditGroupId = None
        self.AsyncRequestId = None
        self.Product = None


    def _deserialize(self, params):
        self.SecAuditGroupId = params.get("SecAuditGroupId")
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSecurityAuditLogDownloadUrlsResponse(AbstractModel):
    """DescribeSecurityAuditLogDownloadUrls response structure.

    """

    def __init__(self):
        r"""
        :param Urls: List of COS URLs of the export results. If the result set is large, it may be divided into multiple URLs for download.
        :type Urls: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Urls = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Urls = params.get("Urls")
        self.RequestId = params.get("RequestId")


class DescribeSecurityAuditLogExportTasksRequest(AbstractModel):
    """DescribeSecurityAuditLogExportTasks request structure.

    """

    def __init__(self):
        r"""
        :param SecAuditGroupId: Security audit group ID.
        :type SecAuditGroupId: str
        :param Product: Service type. Valid value: `mysql` (TencentDB for MySQL).
        :type Product: str
        :param AsyncRequestIds: List of log export task IDs.
        :type AsyncRequestIds: list of int non-negative
        :param Offset: Offset. Default value: `0`.
        :type Offset: int
        :param Limit: Number of returned results. Default value: `20`. Maximum value: `100`.
        :type Limit: int
        """
        self.SecAuditGroupId = None
        self.Product = None
        self.AsyncRequestIds = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.SecAuditGroupId = params.get("SecAuditGroupId")
        self.Product = params.get("Product")
        self.AsyncRequestIds = params.get("AsyncRequestIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSecurityAuditLogExportTasksResponse(AbstractModel):
    """DescribeSecurityAuditLogExportTasks response structure.

    """

    def __init__(self):
        r"""
        :param Tasks: List of security audit log export tasks.
        :type Tasks: list of SecLogExportTaskInfo
        :param TotalCount: Total numbers of security audit log export tasks.
        :type TotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Tasks = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = SecLogExportTaskInfo()
                obj._deserialize(item)
                self.Tasks.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSlowLogTimeSeriesStatsRequest(AbstractModel):
    """DescribeSlowLogTimeSeriesStats request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time, such as "2019-09-10 12:13:14".
        :type StartTime: str
        :param EndTime: End time, such as "2019-09-10 12:13:14". The interval between the end time and the start time can be up to 7 days.
        :type EndTime: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSlowLogTimeSeriesStatsResponse(AbstractModel):
    """DescribeSlowLogTimeSeriesStats response structure.

    """

    def __init__(self):
        r"""
        :param Period: Time range in seconds in histogram.
        :type Period: int
        :param TimeSeries: Number of slow logs in the specified time range.
        :type TimeSeries: list of TimeSlice
        :param SeriesData: Instance CPU utilization monitoring data in the specified time range.
        :type SeriesData: :class:`tencentcloud.dbbrain.v20210527.models.MonitorMetricSeriesData`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Period = None
        self.TimeSeries = None
        self.SeriesData = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Period = params.get("Period")
        if params.get("TimeSeries") is not None:
            self.TimeSeries = []
            for item in params.get("TimeSeries"):
                obj = TimeSlice()
                obj._deserialize(item)
                self.TimeSeries.append(obj)
        if params.get("SeriesData") is not None:
            self.SeriesData = MonitorMetricSeriesData()
            self.SeriesData._deserialize(params.get("SeriesData"))
        self.RequestId = params.get("RequestId")


class DescribeSlowLogTopSqlsRequest(AbstractModel):
    """DescribeSlowLogTopSqls request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time, such as "2019-09-10 12:13:14".
        :type StartTime: str
        :param EndTime: End time in the format of "2019-09-11 10:13:14". The interval between the end time and the start time can be up to 7 days.
        :type EndTime: str
        :param SortBy: Sorting key. Valid values: `QueryTime`, `ExecTimes`, `RowsSent`, `LockTime`, `RowsExamined`. Default value: `QueryTime`.
        :type SortBy: str
        :param OrderBy: Sorting order. Valid values: `ASC` (ascending), `DESC` (descending). Default value: `DESC`.
        :type OrderBy: str
        :param Limit: Number of returned results. Default value: `20`. Maximum value: `100`.
        :type Limit: int
        :param Offset: Offset. Default value: `0`.
        :type Offset: int
        :param SchemaList: Database name array.
        :type SchemaList: list of SchemaItem
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.SortBy = None
        self.OrderBy = None
        self.Limit = None
        self.Offset = None
        self.SchemaList = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.SortBy = params.get("SortBy")
        self.OrderBy = params.get("OrderBy")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("SchemaList") is not None:
            self.SchemaList = []
            for item in params.get("SchemaList"):
                obj = SchemaItem()
                obj._deserialize(item)
                self.SchemaList.append(obj)
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSlowLogTopSqlsResponse(AbstractModel):
    """DescribeSlowLogTopSqls response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible entries.
        :type TotalCount: int
        :param Rows: List of top slow SQL statements
        :type Rows: list of SlowLogTopSqlItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Rows = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Rows") is not None:
            self.Rows = []
            for item in params.get("Rows"):
                obj = SlowLogTopSqlItem()
                obj._deserialize(item)
                self.Rows.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSlowLogUserHostStatsRequest(AbstractModel):
    """DescribeSlowLogUserHostStats request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param StartTime: Start time of the time range in the format of yyyy-MM-dd HH:mm:ss, such as 2019-09-10 12:13:14.
        :type StartTime: str
        :param EndTime: End time of the time range in the format of yyyy-MM-dd HH:mm:ss, such as 2019-09-10 12:13:14.
        :type EndTime: str
        :param Product: Service type. Valid values: mysql (TencentDB for MySQL), cynosdb (TDSQL-C for MySQL). Default value: mysql.
        :type Product: str
        :param Md5: MD5 value of SOL template
        :type Md5: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Product = None
        self.Md5 = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Product = params.get("Product")
        self.Md5 = params.get("Md5")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSlowLogUserHostStatsResponse(AbstractModel):
    """DescribeSlowLogUserHostStats response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of source addresses.
        :type TotalCount: int
        :param Items: Detailed list of the proportion of slow logs from each source address.
        :type Items: list of SlowLogHost
        :param UserNameItems: Detailed list of the percentages of slow logs from different source usernames
        :type UserNameItems: list of SlowLogUser
        :param UserTotalCount: The number of source users
        :type UserTotalCount: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Items = None
        self.UserNameItems = None
        self.UserTotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = SlowLogHost()
                obj._deserialize(item)
                self.Items.append(obj)
        if params.get("UserNameItems") is not None:
            self.UserNameItems = []
            for item in params.get("UserNameItems"):
                obj = SlowLogUser()
                obj._deserialize(item)
                self.UserNameItems.append(obj)
        self.UserTotalCount = params.get("UserTotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSlowLogsRequest(AbstractModel):
    """DescribeSlowLogs request structure.

    """

    def __init__(self):
        r"""
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Md5: MD5 value of a SQL template
        :type Md5: str
        :param StartTime: Start time in the format of "2019-09-10 12:13:14".
        :type StartTime: str
        :param EndTime: End time in the format of "2019-09-11 10:13:14". The interval between the end time and the start time can be up to 7 days.
        :type EndTime: str
        :param Offset: The offset. Default value: `0`.
        :type Offset: int
        :param Limit: The number of queried items. Default value: `20`. Max value: `100`.
        :type Limit: int
        :param DB: Database list
        :type DB: list of str
        :param Key: Keyword
        :type Key: list of str
        :param User: User
        :type User: list of str
        :param Ip: IP
        :type Ip: list of str
        :param Time: Duration range. The left and right borders of the range are the zeroth and first element of the array, respectively.
        :type Time: list of int
        """
        self.Product = None
        self.InstanceId = None
        self.Md5 = None
        self.StartTime = None
        self.EndTime = None
        self.Offset = None
        self.Limit = None
        self.DB = None
        self.Key = None
        self.User = None
        self.Ip = None
        self.Time = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.InstanceId = params.get("InstanceId")
        self.Md5 = params.get("Md5")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.DB = params.get("DB")
        self.Key = params.get("Key")
        self.User = params.get("User")
        self.Ip = params.get("Ip")
        self.Time = params.get("Time")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSlowLogsResponse(AbstractModel):
    """DescribeSlowLogs response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible entries.
        :type TotalCount: int
        :param Rows: Slow log details
        :type Rows: list of SlowLogInfoItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Rows = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Rows") is not None:
            self.Rows = []
            for item in params.get("Rows"):
                obj = SlowLogInfoItem()
                obj._deserialize(item)
                self.Rows.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTopSpaceSchemaTimeSeriesRequest(AbstractModel):
    """DescribeTopSpaceSchemaTimeSeries request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Limit: Number of returned top databases. Maximum value: `100`. Default value: `20`.
        :type Limit: int
        :param SortBy: Field used to sort top databases. Valid values: `DataLength`, `IndexLength`, `TotalLength`, `DataFree`, `FragRatio`, `TableRows`, `PhysicalFileSize` (supported only by TencentDB for MySQL instances). For TencentDB for MySQL instances, the default value is `PhysicalFileSize`. For other database instances, the default value is `TotalLength`.
        :type SortBy: str
        :param StartDate: Start date, such as "2021-01-01". It can be as early as 29 days before the current date and is 6 days before the end date by default.
        :type StartDate: str
        :param EndDate: End date, such as "2021-01-01". It can be as early as 29 days before the current date and is the current date by default.
        :type EndDate: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.Limit = None
        self.SortBy = None
        self.StartDate = None
        self.EndDate = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.StartDate = params.get("StartDate")
        self.EndDate = params.get("EndDate")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTopSpaceSchemaTimeSeriesResponse(AbstractModel):
    """DescribeTopSpaceSchemaTimeSeries response structure.

    """

    def __init__(self):
        r"""
        :param TopSpaceSchemaTimeSeries: Time series list of the returned space statistics of top databases.
        :type TopSpaceSchemaTimeSeries: list of SchemaSpaceTimeSeries
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TopSpaceSchemaTimeSeries = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TopSpaceSchemaTimeSeries") is not None:
            self.TopSpaceSchemaTimeSeries = []
            for item in params.get("TopSpaceSchemaTimeSeries"):
                obj = SchemaSpaceTimeSeries()
                obj._deserialize(item)
                self.TopSpaceSchemaTimeSeries.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTopSpaceSchemasRequest(AbstractModel):
    """DescribeTopSpaceSchemas request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Limit: Number of returned top databases. Maximum value: 100. Default value: 20.
        :type Limit: int
        :param SortBy: Field used to sort top databases. Valid values: DataLength, IndexLength, TotalLength, DataFree, FragRatio, TableRows, PhysicalFileSize (supported only by TencentDB for MySQL instances). For TencentDB for MySQL instances, the default value is `PhysicalFileSize`. For other database instances, the default value is `TotalLength`.
        :type SortBy: str
        :param Product: Service type. Valid values: mysql (TencentDB for MySQL), cynosdb (TDSQL-C for MySQL). Default value: mysql.
        :type Product: str
        """
        self.InstanceId = None
        self.Limit = None
        self.SortBy = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTopSpaceSchemasResponse(AbstractModel):
    """DescribeTopSpaceSchemas response structure.

    """

    def __init__(self):
        r"""
        :param TopSpaceSchemas: List of the returned space statistics of top databases.
        :type TopSpaceSchemas: list of SchemaSpaceData
        :param Timestamp: Timestamp (in seconds) of database space data collection points
        :type Timestamp: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TopSpaceSchemas = None
        self.Timestamp = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TopSpaceSchemas") is not None:
            self.TopSpaceSchemas = []
            for item in params.get("TopSpaceSchemas"):
                obj = SchemaSpaceData()
                obj._deserialize(item)
                self.TopSpaceSchemas.append(obj)
        self.Timestamp = params.get("Timestamp")
        self.RequestId = params.get("RequestId")


class DescribeTopSpaceTableTimeSeriesRequest(AbstractModel):
    """DescribeTopSpaceTableTimeSeries request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Limit: Number of returned top tables. Maximum value: `100`. Default value: `20`.
        :type Limit: int
        :param SortBy: Field used to sort top tables. Valid values: `DataLength`, `IndexLength`, `TotalLength`, `DataFree`, `FragRatio`, `TableRows`, `PhysicalFileSize`. Default value: `PhysicalFileSize`.
        :type SortBy: str
        :param StartDate: Start date, such as "2021-01-01". It can be as early as 29 days before the current date and is 6 days before the end date by default.
        :type StartDate: str
        :param EndDate: End date, such as "2021-01-01". It can be as early as 29 days before the current date and is the current date by default.
        :type EndDate: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.Limit = None
        self.SortBy = None
        self.StartDate = None
        self.EndDate = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.StartDate = params.get("StartDate")
        self.EndDate = params.get("EndDate")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTopSpaceTableTimeSeriesResponse(AbstractModel):
    """DescribeTopSpaceTableTimeSeries response structure.

    """

    def __init__(self):
        r"""
        :param TopSpaceTableTimeSeries: Time series list of the returned space statistics of top tables.
        :type TopSpaceTableTimeSeries: list of TableSpaceTimeSeries
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TopSpaceTableTimeSeries = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TopSpaceTableTimeSeries") is not None:
            self.TopSpaceTableTimeSeries = []
            for item in params.get("TopSpaceTableTimeSeries"):
                obj = TableSpaceTimeSeries()
                obj._deserialize(item)
                self.TopSpaceTableTimeSeries.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTopSpaceTablesRequest(AbstractModel):
    """DescribeTopSpaceTables request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Limit: Number of returned top tables. Maximum value: `100`. Default value: `20`.
        :type Limit: int
        :param SortBy: Field used to sort top tables. Valid values: `DataLength`, `IndexLength`, `TotalLength`, `DataFree`, `FragRatio`, `TableRows`, `PhysicalFileSize` (only supported for TencentDB for MySQL instances). For TencentDB for MySQL instances, the default value is `PhysicalFileSize`. For other database instances, the default value is `TotalLength`.
        :type SortBy: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.Limit = None
        self.SortBy = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTopSpaceTablesResponse(AbstractModel):
    """DescribeTopSpaceTables response structure.

    """

    def __init__(self):
        r"""
        :param TopSpaceTables: List of the returned space statistics of top tables.
        :type TopSpaceTables: list of TableSpaceData
        :param Timestamp: Timestamp (in seconds) of tablespace data collection points
        :type Timestamp: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TopSpaceTables = None
        self.Timestamp = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TopSpaceTables") is not None:
            self.TopSpaceTables = []
            for item in params.get("TopSpaceTables"):
                obj = TableSpaceData()
                obj._deserialize(item)
                self.TopSpaceTables.append(obj)
        self.Timestamp = params.get("Timestamp")
        self.RequestId = params.get("RequestId")


class DescribeUserSqlAdviceRequest(AbstractModel):
    """DescribeUserSqlAdvice request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param SqlText: SQL statement.
        :type SqlText: str
        :param Schema: Database name.
        :type Schema: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL), `dbbrain-mysql` (self-built MySQL). Default value: `mysql`.
        :type Product: str
        """
        self.InstanceId = None
        self.SqlText = None
        self.Schema = None
        self.Product = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SqlText = params.get("SqlText")
        self.Schema = params.get("Schema")
        self.Product = params.get("Product")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUserSqlAdviceResponse(AbstractModel):
    """DescribeUserSqlAdvice response structure.

    """

    def __init__(self):
        r"""
        :param Advices: SQL statement optimization suggestions, which can be parsed into JSON arrays. If there is no need for optimization, the output will be empty.
        :type Advices: str
        :param Comments: Notes of SQL statement optimization suggestions, which can be parsed into String arrays. If there is no need for optimization, the output will be empty.
        :type Comments: str
        :param SqlText: SQL statement.
        :type SqlText: str
        :param Schema: Database name.
        :type Schema: str
        :param Tables: DDL information of related tables, which can be parsed into JSON arrays.
        :type Tables: str
        :param SqlPlan: SQL execution plan, which can be parsed into JSON arrays. If there is no need for optimization, the output will be empty.
        :type SqlPlan: str
        :param Cost: Cost saving details after SQL statement optimization, which can be parsed into JSON arrays. If there is no need for optimization, the output will be empty.
        :type Cost: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Advices = None
        self.Comments = None
        self.SqlText = None
        self.Schema = None
        self.Tables = None
        self.SqlPlan = None
        self.Cost = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Advices = params.get("Advices")
        self.Comments = params.get("Comments")
        self.SqlText = params.get("SqlText")
        self.Schema = params.get("Schema")
        self.Tables = params.get("Tables")
        self.SqlPlan = params.get("SqlPlan")
        self.Cost = params.get("Cost")
        self.RequestId = params.get("RequestId")


class DiagHistoryEventItem(AbstractModel):
    """Instance diagnosis event

    """

    def __init__(self):
        r"""
        :param DiagType: Diagnosis type.
        :type DiagType: str
        :param EndTime: End time.
        :type EndTime: str
        :param StartTime: Start time.
        :type StartTime: str
        :param EventId: Unique event ID.
        :type EventId: int
        :param Severity: Severity, which can be divided into 5 levels: 1: fatal, 2: severe, 3: warning, 4: notice, 5: healthy.
        :type Severity: int
        :param Outline: Diagnosis summary.
        :type Outline: str
        :param DiagItem: Diagnosis item description.
        :type DiagItem: str
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Metric: Reserved field.
Note: this field may return null, indicating that no valid values can be obtained.
        :type Metric: str
        :param Region: Region.
        :type Region: str
        """
        self.DiagType = None
        self.EndTime = None
        self.StartTime = None
        self.EventId = None
        self.Severity = None
        self.Outline = None
        self.DiagItem = None
        self.InstanceId = None
        self.Metric = None
        self.Region = None


    def _deserialize(self, params):
        self.DiagType = params.get("DiagType")
        self.EndTime = params.get("EndTime")
        self.StartTime = params.get("StartTime")
        self.EventId = params.get("EventId")
        self.Severity = params.get("Severity")
        self.Outline = params.get("Outline")
        self.DiagItem = params.get("DiagItem")
        self.InstanceId = params.get("InstanceId")
        self.Metric = params.get("Metric")
        self.Region = params.get("Region")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EventInfo(AbstractModel):
    """Exception information.

    """

    def __init__(self):
        r"""
        :param EventId: Event ID.
        :type EventId: int
        :param DiagType: Diagnosis type.
        :type DiagType: str
        :param StartTime: Start time.
        :type StartTime: str
        :param EndTime: End time.
        :type EndTime: str
        :param Outline: Summary.
        :type Outline: str
        :param Severity: Severity, which can be divided into 5 levels: `1` (Critical), `2` (Severe), `3` (Alarm), `4` (Reminder), `5` (Healthy).
        :type Severity: int
        :param ScoreLost: Deduction.
        :type ScoreLost: int
        :param Metric: Reserved field.
        :type Metric: str
        :param Count: Number of alarms.
        :type Count: int
        """
        self.EventId = None
        self.DiagType = None
        self.StartTime = None
        self.EndTime = None
        self.Outline = None
        self.Severity = None
        self.ScoreLost = None
        self.Metric = None
        self.Count = None


    def _deserialize(self, params):
        self.EventId = params.get("EventId")
        self.DiagType = params.get("DiagType")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Outline = params.get("Outline")
        self.Severity = params.get("Severity")
        self.ScoreLost = params.get("ScoreLost")
        self.Metric = params.get("Metric")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GroupItem(AbstractModel):
    """Describes the group information.

    """

    def __init__(self):
        r"""
        :param Id: Group ID.
        :type Id: int
        :param Name: Group name.
        :type Name: str
        :param MemberCount: Number of group members.
        :type MemberCount: int
        """
        self.Id = None
        self.Name = None
        self.MemberCount = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.MemberCount = params.get("MemberCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HealthReportTask(AbstractModel):
    """Details of the health report task.

    """

    def __init__(self):
        r"""
        :param AsyncRequestId: Async task request ID.
        :type AsyncRequestId: int
        :param Source: Source that triggers the task. Valid values: `DAILY_INSPECTION` (instance inspection), `SCHEDULED` (scheduled task), and `MANUAL` (manual trigger).
        :type Source: str
        :param Progress: Task progress in %.
        :type Progress: int
        :param CreateTime: Task creation time.
        :type CreateTime: str
        :param StartTime: Task start time.
        :type StartTime: str
        :param EndTime: Task end time.
        :type EndTime: str
        :param InstanceInfo: Basic information of the instance to which the task belongs.
        :type InstanceInfo: :class:`tencentcloud.dbbrain.v20210527.models.InstanceBasicInfo`
        :param HealthStatus: Health information in health report.
        :type HealthStatus: :class:`tencentcloud.dbbrain.v20210527.models.HealthStatus`
        """
        self.AsyncRequestId = None
        self.Source = None
        self.Progress = None
        self.CreateTime = None
        self.StartTime = None
        self.EndTime = None
        self.InstanceInfo = None
        self.HealthStatus = None


    def _deserialize(self, params):
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.Source = params.get("Source")
        self.Progress = params.get("Progress")
        self.CreateTime = params.get("CreateTime")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        if params.get("InstanceInfo") is not None:
            self.InstanceInfo = InstanceBasicInfo()
            self.InstanceInfo._deserialize(params.get("InstanceInfo"))
        if params.get("HealthStatus") is not None:
            self.HealthStatus = HealthStatus()
            self.HealthStatus._deserialize(params.get("HealthStatus"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HealthScoreInfo(AbstractModel):
    """Details of the obtained health score.

    """

    def __init__(self):
        r"""
        :param IssueTypes: Exception details.
        :type IssueTypes: list of IssueTypeInfo
        :param EventsTotalCount: Total number of exceptions.
        :type EventsTotalCount: int
        :param HealthScore: Health score.
        :type HealthScore: int
        :param HealthLevel: Health level, such as `HEALTH`, `SUB_HEALTH`, `RISK`, and `HIGH_RISK`.
        :type HealthLevel: str
        """
        self.IssueTypes = None
        self.EventsTotalCount = None
        self.HealthScore = None
        self.HealthLevel = None


    def _deserialize(self, params):
        if params.get("IssueTypes") is not None:
            self.IssueTypes = []
            for item in params.get("IssueTypes"):
                obj = IssueTypeInfo()
                obj._deserialize(item)
                self.IssueTypes.append(obj)
        self.EventsTotalCount = params.get("EventsTotalCount")
        self.HealthScore = params.get("HealthScore")
        self.HealthLevel = params.get("HealthLevel")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HealthStatus(AbstractModel):
    """Instance health status.

    """

    def __init__(self):
        r"""
        :param HealthScore: Health score out of 100 points.
        :type HealthScore: int
        :param HealthLevel: Health level. Valid values: `HEALTH` (healthy), `SUB_HEALTH` (sub-healthy), `RISK` (dangerous), and `HIGH_RISK` (high-risk).
        :type HealthLevel: str
        :param ScoreLost: Total deducted scores.
        :type ScoreLost: int
        :param ScoreDetails: Deduction details.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ScoreDetails: list of ScoreDetail
        """
        self.HealthScore = None
        self.HealthLevel = None
        self.ScoreLost = None
        self.ScoreDetails = None


    def _deserialize(self, params):
        self.HealthScore = params.get("HealthScore")
        self.HealthLevel = params.get("HealthLevel")
        self.ScoreLost = params.get("ScoreLost")
        if params.get("ScoreDetails") is not None:
            self.ScoreDetails = []
            for item in params.get("ScoreDetails"):
                obj = ScoreDetail()
                obj._deserialize(item)
                self.ScoreDetails.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceBasicInfo(AbstractModel):
    """Basic instance information.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param InstanceName: Instance name.
        :type InstanceName: str
        :param Vip: Private IP of the instance.
        :type Vip: str
        :param Vport: Private port of the instance.
        :type Vport: int
        :param Product: Instance service.
        :type Product: str
        :param EngineVersion: Instance engine version.
        :type EngineVersion: str
        """
        self.InstanceId = None
        self.InstanceName = None
        self.Vip = None
        self.Vport = None
        self.Product = None
        self.EngineVersion = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.Product = params.get("Product")
        self.EngineVersion = params.get("EngineVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceConfs(AbstractModel):
    """Instance configuration.

    """

    def __init__(self):
        r"""
        :param DailyInspection: Whether to enable database inspection. Valid values: Yes, No.
        :type DailyInspection: str
        :param OverviewDisplay: Whether to enable instance overview. Valid values: Yes, No.
        :type OverviewDisplay: str
        :param KeyDelimiters: Custom big key analysis separator for Redis only
Note: This field may return null, indicating that no valid values can be obtained.
        :type KeyDelimiters: list of str
        """
        self.DailyInspection = None
        self.OverviewDisplay = None
        self.KeyDelimiters = None


    def _deserialize(self, params):
        self.DailyInspection = params.get("DailyInspection")
        self.OverviewDisplay = params.get("OverviewDisplay")
        self.KeyDelimiters = params.get("KeyDelimiters")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceInfo(AbstractModel):
    """Queries the list of instances and returns their information.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param InstanceName: Instance name.
        :type InstanceName: str
        :param Region: Instance region.
        :type Region: str
        :param HealthScore: Health score.
        :type HealthScore: int
        :param Product: Service.
        :type Product: str
        :param EventCount: Number of exceptions.
        :type EventCount: int
        :param InstanceType: Instance type. Valid values: 1 (MASTER), 2 (DR), 3 (RO), 4 (SDR)
        :type InstanceType: int
        :param Cpu: Number of cores.
        :type Cpu: int
        :param Memory: Memory in MB.
        :type Memory: int
        :param Volume: Disk storage in GB.
        :type Volume: int
        :param EngineVersion: Database version.
        :type EngineVersion: str
        :param Vip: Private network address.
        :type Vip: str
        :param Vport: Private network port.
        :type Vport: int
        :param Source: Access source.
        :type Source: str
        :param GroupId: Group ID.
        :type GroupId: str
        :param GroupName: Group name.
        :type GroupName: str
        :param Status: Instance status. Valid values: 0 (delivering), 1 (running), 4 (terminating), 5 (isolated)
        :type Status: int
        :param UniqSubnetId: Unified subnet ID.
        :type UniqSubnetId: str
        :param DeployMode: TencentDB instance type.
        :type DeployMode: str
        :param InitFlag: TencentDB instance initialization flag. Valid values: 0 (not initialized), 1 (initialized).
        :type InitFlag: int
        :param TaskStatus: Task status.
        :type TaskStatus: int
        :param UniqVpcId: Unified VPC ID.
        :type UniqVpcId: str
        :param InstanceConf: Instance inspection/overview status.
        :type InstanceConf: :class:`tencentcloud.dbbrain.v20210527.models.InstanceConfs`
        :param DeadlineTime: Resource expiration time.
        :type DeadlineTime: str
        :param IsSupported: Whether it is an instance supported by DBbrain.
        :type IsSupported: bool
        :param SecAuditStatus: Status of instance security audit log. Valid values: ON (enabled), OFF (disabled).
        :type SecAuditStatus: str
        :param AuditPolicyStatus: Status of instance audit log. Valid values: ALL_AUDIT (full audit is enabled), RULE_AUDIT (rule audit is enabled), UNBOUND (audit is disabled).
        :type AuditPolicyStatus: str
        :param AuditRunningStatus: Running status of instance audit log. Valid values: normal (running), paused (suspension due to overdue payment).
        :type AuditRunningStatus: str
        :param InternalVip: Private VIP 
Note: This field may return null, indicating that no valid values can be obtained.
        :type InternalVip: str
        :param InternalVport: Private network port 
Note: This field may return null, indicating that no valid values can be obtained.
        :type InternalVport: int
        :param CreateTime: Creation time
        :type CreateTime: str
        :param ClusterId: Cluster ID. This field is only required for cluster database products like TDSQL-C. 
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClusterId: str
        :param ClusterName: Cluster name. This field is only required for cluster database products like TDSQL-C. 
Note: This field may return null, indicating that no valid values can be obtained.
        :type ClusterName: str
        """
        self.InstanceId = None
        self.InstanceName = None
        self.Region = None
        self.HealthScore = None
        self.Product = None
        self.EventCount = None
        self.InstanceType = None
        self.Cpu = None
        self.Memory = None
        self.Volume = None
        self.EngineVersion = None
        self.Vip = None
        self.Vport = None
        self.Source = None
        self.GroupId = None
        self.GroupName = None
        self.Status = None
        self.UniqSubnetId = None
        self.DeployMode = None
        self.InitFlag = None
        self.TaskStatus = None
        self.UniqVpcId = None
        self.InstanceConf = None
        self.DeadlineTime = None
        self.IsSupported = None
        self.SecAuditStatus = None
        self.AuditPolicyStatus = None
        self.AuditRunningStatus = None
        self.InternalVip = None
        self.InternalVport = None
        self.CreateTime = None
        self.ClusterId = None
        self.ClusterName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.Region = params.get("Region")
        self.HealthScore = params.get("HealthScore")
        self.Product = params.get("Product")
        self.EventCount = params.get("EventCount")
        self.InstanceType = params.get("InstanceType")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Volume = params.get("Volume")
        self.EngineVersion = params.get("EngineVersion")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.Source = params.get("Source")
        self.GroupId = params.get("GroupId")
        self.GroupName = params.get("GroupName")
        self.Status = params.get("Status")
        self.UniqSubnetId = params.get("UniqSubnetId")
        self.DeployMode = params.get("DeployMode")
        self.InitFlag = params.get("InitFlag")
        self.TaskStatus = params.get("TaskStatus")
        self.UniqVpcId = params.get("UniqVpcId")
        if params.get("InstanceConf") is not None:
            self.InstanceConf = InstanceConfs()
            self.InstanceConf._deserialize(params.get("InstanceConf"))
        self.DeadlineTime = params.get("DeadlineTime")
        self.IsSupported = params.get("IsSupported")
        self.SecAuditStatus = params.get("SecAuditStatus")
        self.AuditPolicyStatus = params.get("AuditPolicyStatus")
        self.AuditRunningStatus = params.get("AuditRunningStatus")
        self.InternalVip = params.get("InternalVip")
        self.InternalVport = params.get("InternalVport")
        self.CreateTime = params.get("CreateTime")
        self.ClusterId = params.get("ClusterId")
        self.ClusterName = params.get("ClusterName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IssueTypeInfo(AbstractModel):
    """Metric information.

    """

    def __init__(self):
        r"""
        :param IssueType: Metric categories. Valid values: `AVAILABILITY`, `MAINTAINABILITY`, `PERFORMANCE`, and `RELIABILITY`.
        :type IssueType: str
        :param Events: Exception.
        :type Events: list of EventInfo
        :param TotalCount: Total number of exceptions.
        :type TotalCount: int
        """
        self.IssueType = None
        self.Events = None
        self.TotalCount = None


    def _deserialize(self, params):
        self.IssueType = params.get("IssueType")
        if params.get("Events") is not None:
            self.Events = []
            for item in params.get("Events"):
                obj = EventInfo()
                obj._deserialize(item)
                self.Events.append(obj)
        self.TotalCount = params.get("TotalCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KillMySqlThreadsRequest(AbstractModel):
    """KillMySqlThreads request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID.
        :type InstanceId: str
        :param Stage: The stage of a session killing task. Valid values: `Prepare` (preparation stage), `Commit` (commit stage).
        :type Stage: str
        :param Threads: List of IDs of the MySQL sessions to be killed. This parameter is used in the `Prepare` stage.
        :type Threads: list of int
        :param SqlExecId: Execution ID. This parameter is used in the `Commit` stage.
        :type SqlExecId: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL). Default value: `mysql`.
        :type Product: str
        :param RecordHistory: Whether to record the thread killing history. The default value is `true`, indicating “yes”. You can set it to `false` (“no”) to speed up the killing process.
        :type RecordHistory: bool
        """
        self.InstanceId = None
        self.Stage = None
        self.Threads = None
        self.SqlExecId = None
        self.Product = None
        self.RecordHistory = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Stage = params.get("Stage")
        self.Threads = params.get("Threads")
        self.SqlExecId = params.get("SqlExecId")
        self.Product = params.get("Product")
        self.RecordHistory = params.get("RecordHistory")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KillMySqlThreadsResponse(AbstractModel):
    """KillMySqlThreads response structure.

    """

    def __init__(self):
        r"""
        :param Threads: List of IDs of the MySQL sessions that have been killed.
        :type Threads: list of int
        :param SqlExecId: Execution ID, which is output in the `Prepare` stage and used to specify the ID of the session to be killed in the `Commit` stage.
Note: This field may return null, indicating that no valid values can be obtained.
        :type SqlExecId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Threads = None
        self.SqlExecId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Threads = params.get("Threads")
        self.SqlExecId = params.get("SqlExecId")
        self.RequestId = params.get("RequestId")


class MailConfiguration(AbstractModel):
    """Email sending configuration

    """

    def __init__(self):
        r"""
        :param SendMail: Whether to enable email sending. Valid values: `0` (no), `1` (yes).
        :type SendMail: int
        :param Region: Region configuration, such as "ap-guangzhou" and "ap-shanghai". For the inspection email sending template, configure the region where you need to send the inspection email. For the subscription email sending template, configure the region where the current subscribed instance resides.
        :type Region: list of str
        :param HealthStatus: Sends a report with the specified health level, such as `HEALTH`, `SUB_HEALTH`, `RISK`, and `HIGH_RISK`.
        :type HealthStatus: list of str
        :param ContactPerson: Recipient ID. Either `ContactPerson` or `ContactGroup` should be passed in.
        :type ContactPerson: list of int
        :param ContactGroup: Recipient group ID. Either `ContactPerson` or `ContactGroup` should be passed in.
        :type ContactGroup: list of int
        """
        self.SendMail = None
        self.Region = None
        self.HealthStatus = None
        self.ContactPerson = None
        self.ContactGroup = None


    def _deserialize(self, params):
        self.SendMail = params.get("SendMail")
        self.Region = params.get("Region")
        self.HealthStatus = params.get("HealthStatus")
        self.ContactPerson = params.get("ContactPerson")
        self.ContactGroup = params.get("ContactGroup")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDiagDBInstanceConfRequest(AbstractModel):
    """ModifyDiagDBInstanceConf request structure.

    """

    def __init__(self):
        r"""
        :param InstanceConfs: Instance configuration, including inspection and overview switch.
        :type InstanceConfs: :class:`tencentcloud.dbbrain.v20210527.models.InstanceConfs`
        :param Regions: Target regions of the request. If the value is `All`, it is applied to all regions.
        :type Regions: str
        :param Product: Service type. Valid values: `mysql` (TencentDB for MySQL), `cynosdb` (TDSQL-C for MySQL).
        :type Product: str
        :param InstanceIds: ID of the instance to modify.
        :type InstanceIds: list of str
        """
        self.InstanceConfs = None
        self.Regions = None
        self.Product = None
        self.InstanceIds = None


    def _deserialize(self, params):
        if params.get("InstanceConfs") is not None:
            self.InstanceConfs = InstanceConfs()
            self.InstanceConfs._deserialize(params.get("InstanceConfs"))
        self.Regions = params.get("Regions")
        self.Product = params.get("Product")
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDiagDBInstanceConfResponse(AbstractModel):
    """ModifyDiagDBInstanceConf response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class MonitorFloatMetric(AbstractModel):
    """Monitoring data in float type

    """

    def __init__(self):
        r"""
        :param Metric: Metric name.
        :type Metric: str
        :param Unit: Metric unit.
        :type Unit: str
        :param Values: Metric value.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Values: list of float
        """
        self.Metric = None
        self.Unit = None
        self.Values = None


    def _deserialize(self, params):
        self.Metric = params.get("Metric")
        self.Unit = params.get("Unit")
        self.Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MonitorFloatMetricSeriesData(AbstractModel):
    """Monitoring metric value in float type in a unit of time interval

    """

    def __init__(self):
        r"""
        :param Series: Monitoring metric.
        :type Series: list of MonitorFloatMetric
        :param Timestamp: Timestamp corresponding to monitoring metric.
        :type Timestamp: list of int
        """
        self.Series = None
        self.Timestamp = None


    def _deserialize(self, params):
        if params.get("Series") is not None:
            self.Series = []
            for item in params.get("Series"):
                obj = MonitorFloatMetric()
                obj._deserialize(item)
                self.Series.append(obj)
        self.Timestamp = params.get("Timestamp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MonitorMetric(AbstractModel):
    """Monitoring data

    """

    def __init__(self):
        r"""
        :param Metric: Metric name.
        :type Metric: str
        :param Unit: Metric unit.
        :type Unit: str
        :param Values: Metric value.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Values: list of float
        """
        self.Metric = None
        self.Unit = None
        self.Values = None


    def _deserialize(self, params):
        self.Metric = params.get("Metric")
        self.Unit = params.get("Unit")
        self.Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MonitorMetricSeriesData(AbstractModel):
    """Monitoring metric value in a unit of time interval

    """

    def __init__(self):
        r"""
        :param Series: Monitoring metric.
        :type Series: list of MonitorMetric
        :param Timestamp: Timestamp corresponding to monitoring metric.
        :type Timestamp: list of int
        """
        self.Series = None
        self.Timestamp = None


    def _deserialize(self, params):
        if params.get("Series") is not None:
            self.Series = []
            for item in params.get("Series"):
                obj = MonitorMetric()
                obj._deserialize(item)
                self.Series.append(obj)
        self.Timestamp = params.get("Timestamp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MySqlProcess(AbstractModel):
    """Relational database thread

    """

    def __init__(self):
        r"""
        :param ID: Thread ID.
        :type ID: str
        :param User: Thread operation account name.
        :type User: str
        :param Host: Thread operation host address.
        :type Host: str
        :param DB: Thread operation database.
        :type DB: str
        :param State: Thread operation status.
        :type State: str
        :param Command: Thread execution type.
        :type Command: str
        :param Time: Thread operation duration in seconds.
        :type Time: str
        :param Info: Thread operation statement.
        :type Info: str
        """
        self.ID = None
        self.User = None
        self.Host = None
        self.DB = None
        self.State = None
        self.Command = None
        self.Time = None
        self.Info = None


    def _deserialize(self, params):
        self.ID = params.get("ID")
        self.User = params.get("User")
        self.Host = params.get("Host")
        self.DB = params.get("DB")
        self.State = params.get("State")
        self.Command = params.get("Command")
        self.Time = params.get("Time")
        self.Info = params.get("Info")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProcessStatistic(AbstractModel):
    """Real-time session statistics.

    """

    def __init__(self):
        r"""
        :param Items: Array of session details
        :type Items: list of SessionItem
        :param AllConnSum: The total number of connections
        :type AllConnSum: int
        :param ActiveConnSum: The total number of active connections
        :type ActiveConnSum: int
        """
        self.Items = None
        self.AllConnSum = None
        self.ActiveConnSum = None


    def _deserialize(self, params):
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = SessionItem()
                obj._deserialize(item)
                self.Items.append(obj)
        self.AllConnSum = params.get("AllConnSum")
        self.ActiveConnSum = params.get("ActiveConnSum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProfileInfo(AbstractModel):
    """Information configured by the user.

    """

    def __init__(self):
        r"""
        :param Language: Email language, such as `en`.
        :type Language: str
        :param MailConfiguration: Email template content.
        :type MailConfiguration: :class:`tencentcloud.dbbrain.v20210527.models.MailConfiguration`
        """
        self.Language = None
        self.MailConfiguration = None


    def _deserialize(self, params):
        self.Language = params.get("Language")
        if params.get("MailConfiguration") is not None:
            self.MailConfiguration = MailConfiguration()
            self.MailConfiguration._deserialize(params.get("MailConfiguration"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RedisPreKeySpaceData(AbstractModel):
    """Space information of Redis key prefixes

    """

    def __init__(self):
        r"""
        :param AveElementSize: Average element length
        :type AveElementSize: int
        :param Length: Total memory usage in bytes
        :type Length: int
        :param KeyPreIndex: Key prefix
        :type KeyPreIndex: str
        :param ItemCount: The number of elements
        :type ItemCount: int
        :param Count: The number of keys
        :type Count: int
        :param MaxElementSize: The max element length
        :type MaxElementSize: int
        """
        self.AveElementSize = None
        self.Length = None
        self.KeyPreIndex = None
        self.ItemCount = None
        self.Count = None
        self.MaxElementSize = None


    def _deserialize(self, params):
        self.AveElementSize = params.get("AveElementSize")
        self.Length = params.get("Length")
        self.KeyPreIndex = params.get("KeyPreIndex")
        self.ItemCount = params.get("ItemCount")
        self.Count = params.get("Count")
        self.MaxElementSize = params.get("MaxElementSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SchemaItem(AbstractModel):
    """`SchemaItem` array

    """

    def __init__(self):
        r"""
        :param Schema: Database name
        :type Schema: str
        """
        self.Schema = None


    def _deserialize(self, params):
        self.Schema = params.get("Schema")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SchemaSpaceData(AbstractModel):
    """Database space statistics.

    """

    def __init__(self):
        r"""
        :param TableSchema: Database name.
        :type TableSchema: str
        :param DataLength: Data space in MB.
        :type DataLength: float
        :param IndexLength: Index space in MB.
        :type IndexLength: float
        :param DataFree: Fragmented space in MB.
        :type DataFree: float
        :param TotalLength: Total space usage in MB.
        :type TotalLength: float
        :param FragRatio: Fragmentation rate in %.
        :type FragRatio: float
        :param TableRows: Number of rows.
        :type TableRows: int
        :param PhysicalFileSize: Total size in MB of physical files exclusive to all tables in the database.
Note: this field may return null, indicating that no valid values can be obtained.
        :type PhysicalFileSize: float
        """
        self.TableSchema = None
        self.DataLength = None
        self.IndexLength = None
        self.DataFree = None
        self.TotalLength = None
        self.FragRatio = None
        self.TableRows = None
        self.PhysicalFileSize = None


    def _deserialize(self, params):
        self.TableSchema = params.get("TableSchema")
        self.DataLength = params.get("DataLength")
        self.IndexLength = params.get("IndexLength")
        self.DataFree = params.get("DataFree")
        self.TotalLength = params.get("TotalLength")
        self.FragRatio = params.get("FragRatio")
        self.TableRows = params.get("TableRows")
        self.PhysicalFileSize = params.get("PhysicalFileSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SchemaSpaceTimeSeries(AbstractModel):
    """Time series of database space data

    """

    def __init__(self):
        r"""
        :param TableSchema: Database name
        :type TableSchema: str
        :param SeriesData: Space metric value in a unit of time interval
        :type SeriesData: :class:`tencentcloud.dbbrain.v20210527.models.MonitorMetricSeriesData`
        """
        self.TableSchema = None
        self.SeriesData = None


    def _deserialize(self, params):
        self.TableSchema = params.get("TableSchema")
        if params.get("SeriesData") is not None:
            self.SeriesData = MonitorMetricSeriesData()
            self.SeriesData._deserialize(params.get("SeriesData"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScoreDetail(AbstractModel):
    """Deduction details.

    """

    def __init__(self):
        r"""
        :param IssueType: Deduction item type. Valid values: `Availability`, `Maintainability`, `Performance`, `Reliability`.
        :type IssueType: str
        :param ScoreLost: Total deducted scores.
        :type ScoreLost: int
        :param ScoreLostMax: Upper limit of the deducted scores.
        :type ScoreLostMax: int
        :param Items: List of deduction items.
Note: This field may return null, indicating that no valid values can be obtained.
        :type Items: list of ScoreItem
        """
        self.IssueType = None
        self.ScoreLost = None
        self.ScoreLostMax = None
        self.Items = None


    def _deserialize(self, params):
        self.IssueType = params.get("IssueType")
        self.ScoreLost = params.get("ScoreLost")
        self.ScoreLostMax = params.get("ScoreLostMax")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = ScoreItem()
                obj._deserialize(item)
                self.Items.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScoreItem(AbstractModel):
    """Diagnosis deduction item.

    """

    def __init__(self):
        r"""
        :param DiagItem: Exception diagnosis item name.
        :type DiagItem: str
        :param IssueType: Diagnosis item type. Valid values: `Availability`, `Maintainability`, `Performance`, `Reliability`.
        :type IssueType: str
        :param TopSeverity: Health level. Valid values: `Healthy`, `Reminder`, `Alarm`, `Severe`, `Critical`.
        :type TopSeverity: str
        :param Count: Number of occurrences of this exception diagnosis item.
        :type Count: int
        :param ScoreLost: Deducted scores.
        :type ScoreLost: int
        """
        self.DiagItem = None
        self.IssueType = None
        self.TopSeverity = None
        self.Count = None
        self.ScoreLost = None


    def _deserialize(self, params):
        self.DiagItem = params.get("DiagItem")
        self.IssueType = params.get("IssueType")
        self.TopSeverity = params.get("TopSeverity")
        self.Count = params.get("Count")
        self.ScoreLost = params.get("ScoreLost")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SecLogExportTaskInfo(AbstractModel):
    """Security audit log export task information.

    """

    def __init__(self):
        r"""
        :param AsyncRequestId: Async task Id.
        :type AsyncRequestId: int
        :param StartTime: Task start time.
Note: This field may return null, indicating that no valid values can be obtained.
        :type StartTime: str
        :param EndTime: Task end time.
Note: This field may return null, indicating that no valid values can be obtained.
        :type EndTime: str
        :param CreateTime: Task creation time.
        :type CreateTime: str
        :param Status: Task status.
        :type Status: str
        :param Progress: Task progress.
        :type Progress: int
        :param LogStartTime: Exported log start time.
Note: This field may return null, indicating that no valid values can be obtained.
        :type LogStartTime: str
        :param LogEndTime: Exported log end time.
Note: This field may return null, indicating that no valid values can be obtained.
        :type LogEndTime: str
        :param TotalSize: Total size of log files in KB.
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalSize: int
        :param DangerLevels: List of risk levels. Valid values: `0` (no risk), `1` (low risk), `2` (medium risk), `3` (high risk).
Note: This field may return null, indicating that no valid values can be obtained.
        :type DangerLevels: list of int non-negative
        """
        self.AsyncRequestId = None
        self.StartTime = None
        self.EndTime = None
        self.CreateTime = None
        self.Status = None
        self.Progress = None
        self.LogStartTime = None
        self.LogEndTime = None
        self.TotalSize = None
        self.DangerLevels = None


    def _deserialize(self, params):
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.CreateTime = params.get("CreateTime")
        self.Status = params.get("Status")
        self.Progress = params.get("Progress")
        self.LogStartTime = params.get("LogStartTime")
        self.LogEndTime = params.get("LogEndTime")
        self.TotalSize = params.get("TotalSize")
        self.DangerLevels = params.get("DangerLevels")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SessionItem(AbstractModel):
    """Access source details of the real-time session

    """

    def __init__(self):
        r"""
        :param Ip: Access source
        :type Ip: str
        :param ActiveConn: The number of active connections from the current access source
        :type ActiveConn: str
        :param AllConn: The total number of connections from the current access source
        :type AllConn: int
        """
        self.Ip = None
        self.ActiveConn = None
        self.AllConn = None


    def _deserialize(self, params):
        self.Ip = params.get("Ip")
        self.ActiveConn = params.get("ActiveConn")
        self.AllConn = params.get("AllConn")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SlowLogHost(AbstractModel):
    """Details of slow log source addresses.

    """

    def __init__(self):
        r"""
        :param UserHost: Source addresses.
        :type UserHost: str
        :param Ratio: Proportion (in %) of slow logs from this source address to the total number of slow logs.
        :type Ratio: float
        :param Count: Number of slow logs from this source address.
        :type Count: int
        """
        self.UserHost = None
        self.Ratio = None
        self.Count = None


    def _deserialize(self, params):
        self.UserHost = params.get("UserHost")
        self.Ratio = params.get("Ratio")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SlowLogInfoItem(AbstractModel):
    """Slow log details

    """

    def __init__(self):
        r"""
        :param Timestamp: Slow log start time
        :type Timestamp: str
        :param SqlText: SQL statement
        :type SqlText: str
        :param Database: Database
        :type Database: str
        :param UserName: User source
Note: This field may return null, indicating that no valid values can be obtained.
        :type UserName: str
        :param UserHost: IP source
Note: This field may return null, indicating that no valid values can be obtained.
        :type UserHost: str
        :param QueryTime: Execution time in seconds
        :type QueryTime: int
        :param LockTime: Lock time in seconds
Note: This field may return null, indicating that no valid values can be obtained.
        :type LockTime: int
        :param RowsExamined: Number of scanned rows
Note: This field may return null, indicating that no valid values can be obtained.
        :type RowsExamined: int
        :param RowsSent: Number of returned rows
Note: This field may return null, indicating that no valid values can be obtained.
        :type RowsSent: int
        """
        self.Timestamp = None
        self.SqlText = None
        self.Database = None
        self.UserName = None
        self.UserHost = None
        self.QueryTime = None
        self.LockTime = None
        self.RowsExamined = None
        self.RowsSent = None


    def _deserialize(self, params):
        self.Timestamp = params.get("Timestamp")
        self.SqlText = params.get("SqlText")
        self.Database = params.get("Database")
        self.UserName = params.get("UserName")
        self.UserHost = params.get("UserHost")
        self.QueryTime = params.get("QueryTime")
        self.LockTime = params.get("LockTime")
        self.RowsExamined = params.get("RowsExamined")
        self.RowsSent = params.get("RowsSent")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SlowLogTopSqlItem(AbstractModel):
    """Top slow SQL statements

    """

    def __init__(self):
        r"""
        :param LockTime: Total SQL lock wait time in seconds.
        :type LockTime: float
        :param LockTimeMax: Maximum lock wait time in seconds
        :type LockTimeMax: float
        :param LockTimeMin: Minimum lock wait time in seconds
        :type LockTimeMin: float
        :param RowsExamined: Total number of scanned rows
        :type RowsExamined: int
        :param RowsExaminedMax: Maximum number of scanned rows
        :type RowsExaminedMax: int
        :param RowsExaminedMin: Minimum number of scanned rows
        :type RowsExaminedMin: int
        :param QueryTime: Total duration in seconds
        :type QueryTime: float
        :param QueryTimeMax: Maximum execution time in seconds
        :type QueryTimeMax: float
        :param QueryTimeMin: Minimum execution time in seconds
        :type QueryTimeMin: float
        :param RowsSent: Total number of returned rows
        :type RowsSent: int
        :param RowsSentMax: Maximum number of returned rows
        :type RowsSentMax: int
        :param RowsSentMin: Minimum number of returned rows
        :type RowsSentMin: int
        :param ExecTimes: Number of executions
        :type ExecTimes: int
        :param SqlTemplate: SQL template
        :type SqlTemplate: str
        :param SqlText: SQL statements with parameter (random)
        :type SqlText: str
        :param Schema: Database name
        :type Schema: str
        :param QueryTimeRatio: Ratio of the total duration in %
        :type QueryTimeRatio: float
        :param LockTimeRatio: Ratio of the total SQL lock wait time in %
        :type LockTimeRatio: float
        :param RowsExaminedRatio: Ratio of total number of scanned rows in %
        :type RowsExaminedRatio: float
        :param RowsSentRatio: Ratio of total number of returned rows in %
        :type RowsSentRatio: float
        :param QueryTimeAvg: Average execution time in seconds
        :type QueryTimeAvg: float
        :param RowsSentAvg: Average number of returned rows
        :type RowsSentAvg: float
        :param LockTimeAvg: Average lock wait time in seconds
        :type LockTimeAvg: float
        :param RowsExaminedAvg: Average number of scanned rows
        :type RowsExaminedAvg: float
        :param Md5: MD5 value of the SQL template
        :type Md5: str
        """
        self.LockTime = None
        self.LockTimeMax = None
        self.LockTimeMin = None
        self.RowsExamined = None
        self.RowsExaminedMax = None
        self.RowsExaminedMin = None
        self.QueryTime = None
        self.QueryTimeMax = None
        self.QueryTimeMin = None
        self.RowsSent = None
        self.RowsSentMax = None
        self.RowsSentMin = None
        self.ExecTimes = None
        self.SqlTemplate = None
        self.SqlText = None
        self.Schema = None
        self.QueryTimeRatio = None
        self.LockTimeRatio = None
        self.RowsExaminedRatio = None
        self.RowsSentRatio = None
        self.QueryTimeAvg = None
        self.RowsSentAvg = None
        self.LockTimeAvg = None
        self.RowsExaminedAvg = None
        self.Md5 = None


    def _deserialize(self, params):
        self.LockTime = params.get("LockTime")
        self.LockTimeMax = params.get("LockTimeMax")
        self.LockTimeMin = params.get("LockTimeMin")
        self.RowsExamined = params.get("RowsExamined")
        self.RowsExaminedMax = params.get("RowsExaminedMax")
        self.RowsExaminedMin = params.get("RowsExaminedMin")
        self.QueryTime = params.get("QueryTime")
        self.QueryTimeMax = params.get("QueryTimeMax")
        self.QueryTimeMin = params.get("QueryTimeMin")
        self.RowsSent = params.get("RowsSent")
        self.RowsSentMax = params.get("RowsSentMax")
        self.RowsSentMin = params.get("RowsSentMin")
        self.ExecTimes = params.get("ExecTimes")
        self.SqlTemplate = params.get("SqlTemplate")
        self.SqlText = params.get("SqlText")
        self.Schema = params.get("Schema")
        self.QueryTimeRatio = params.get("QueryTimeRatio")
        self.LockTimeRatio = params.get("LockTimeRatio")
        self.RowsExaminedRatio = params.get("RowsExaminedRatio")
        self.RowsSentRatio = params.get("RowsSentRatio")
        self.QueryTimeAvg = params.get("QueryTimeAvg")
        self.RowsSentAvg = params.get("RowsSentAvg")
        self.LockTimeAvg = params.get("LockTimeAvg")
        self.RowsExaminedAvg = params.get("RowsExaminedAvg")
        self.Md5 = params.get("Md5")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SlowLogUser(AbstractModel):
    """Details of the source users of slow logs

    """

    def __init__(self):
        r"""
        :param UserName: Source username
        :type UserName: str
        :param Ratio: Percentage of the number of slow logs from this source username to the total number of slow logs
        :type Ratio: float
        :param Count: Number of slow logs from this source username
        :type Count: int
        """
        self.UserName = None
        self.Ratio = None
        self.Count = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.Ratio = params.get("Ratio")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TableSpaceData(AbstractModel):
    """Database tablespace statistics.

    """

    def __init__(self):
        r"""
        :param TableName: Table name.
        :type TableName: str
        :param TableSchema: Database name.
        :type TableSchema: str
        :param Engine: Database table storage engine.
        :type Engine: str
        :param DataLength: Data space in MB.
        :type DataLength: float
        :param IndexLength: Index space in MB.
        :type IndexLength: float
        :param DataFree: Fragmented space in MB.
        :type DataFree: float
        :param TotalLength: Total space usage in MB.
        :type TotalLength: float
        :param FragRatio: Fragmentation rate in %.
        :type FragRatio: float
        :param TableRows: Number of rows.
        :type TableRows: int
        :param PhysicalFileSize: Size in MB of the physical file exclusive to a table.
        :type PhysicalFileSize: float
        """
        self.TableName = None
        self.TableSchema = None
        self.Engine = None
        self.DataLength = None
        self.IndexLength = None
        self.DataFree = None
        self.TotalLength = None
        self.FragRatio = None
        self.TableRows = None
        self.PhysicalFileSize = None


    def _deserialize(self, params):
        self.TableName = params.get("TableName")
        self.TableSchema = params.get("TableSchema")
        self.Engine = params.get("Engine")
        self.DataLength = params.get("DataLength")
        self.IndexLength = params.get("IndexLength")
        self.DataFree = params.get("DataFree")
        self.TotalLength = params.get("TotalLength")
        self.FragRatio = params.get("FragRatio")
        self.TableRows = params.get("TableRows")
        self.PhysicalFileSize = params.get("PhysicalFileSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TableSpaceTimeSeries(AbstractModel):
    """Time series of database tablespace data

    """

    def __init__(self):
        r"""
        :param TableName: Table name.
        :type TableName: str
        :param TableSchema: Database name.
        :type TableSchema: str
        :param Engine: Database table storage engine.
        :type Engine: str
        :param SeriesData: Space metric value in a unit of time interval
        :type SeriesData: :class:`tencentcloud.dbbrain.v20210527.models.MonitorFloatMetricSeriesData`
        """
        self.TableName = None
        self.TableSchema = None
        self.Engine = None
        self.SeriesData = None


    def _deserialize(self, params):
        self.TableName = params.get("TableName")
        self.TableSchema = params.get("TableSchema")
        self.Engine = params.get("Engine")
        if params.get("SeriesData") is not None:
            self.SeriesData = MonitorFloatMetricSeriesData()
            self.SeriesData._deserialize(params.get("SeriesData"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TaskInfo(AbstractModel):
    """Information about Redis session killing task status

    """

    def __init__(self):
        r"""
        :param AsyncRequestId: Async task ID.
        :type AsyncRequestId: int
        :param InstProxyList: List of all proxies of the current instance.
        :type InstProxyList: list of str
        :param InstProxyCount: Total number of proxies of the current instance.
        :type InstProxyCount: int
        :param CreateTime: Task creation time.
        :type CreateTime: str
        :param StartTime: Task start time.
        :type StartTime: str
        :param TaskStatus: Task status. Valid values: `created` (create), `chosen` (to be executed), `running` (being executed), `failed` (failed), and `finished` (completed).
        :type TaskStatus: str
        :param FinishedProxyList: IDs of the proxies that have completed the session killing tasks.
        :type FinishedProxyList: list of str
        :param FailedProxyList: IDs of the proxies that failed to execute the session killing tasks.
        :type FailedProxyList: list of str
        :param EndTime: Task end time.
        :type EndTime: str
        :param Progress: Task progress.
        :type Progress: int
        :param InstanceId: Instance ID.
        :type InstanceId: str
        """
        self.AsyncRequestId = None
        self.InstProxyList = None
        self.InstProxyCount = None
        self.CreateTime = None
        self.StartTime = None
        self.TaskStatus = None
        self.FinishedProxyList = None
        self.FailedProxyList = None
        self.EndTime = None
        self.Progress = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.AsyncRequestId = params.get("AsyncRequestId")
        self.InstProxyList = params.get("InstProxyList")
        self.InstProxyCount = params.get("InstProxyCount")
        self.CreateTime = params.get("CreateTime")
        self.StartTime = params.get("StartTime")
        self.TaskStatus = params.get("TaskStatus")
        self.FinishedProxyList = params.get("FinishedProxyList")
        self.FailedProxyList = params.get("FailedProxyList")
        self.EndTime = params.get("EndTime")
        self.Progress = params.get("Progress")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TimeSlice(AbstractModel):
    """Slow log statistics in the specified time range

    """

    def __init__(self):
        r"""
        :param Count: Total number
        :type Count: int
        :param Timestamp: Statistics start time
        :type Timestamp: int
        """
        self.Count = None
        self.Timestamp = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.Timestamp = params.get("Timestamp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserProfile(AbstractModel):
    """Information configured by user, including email configuration.

    """

    def __init__(self):
        r"""
        :param ProfileId: Configured ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProfileId: str
        :param ProfileType: Configuration type. Valid values: `dbScan_mail_configuration` (email configuration of the database inspection report), `scheduler_mail_configuration` (email configuration of the scheduled task report).
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProfileType: str
        :param ProfileLevel: Configuration level. Valid values: `User` (user-level), `Instance` (instance-level). For database inspection emails, it should be `User`. For scheduled task emails, it should be `Instance`.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProfileLevel: str
        :param ProfileName: Configuration name.
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProfileName: str
        :param ProfileInfo: Configuration details.
        :type ProfileInfo: :class:`tencentcloud.dbbrain.v20210527.models.ProfileInfo`
        """
        self.ProfileId = None
        self.ProfileType = None
        self.ProfileLevel = None
        self.ProfileName = None
        self.ProfileInfo = None


    def _deserialize(self, params):
        self.ProfileId = params.get("ProfileId")
        self.ProfileType = params.get("ProfileType")
        self.ProfileLevel = params.get("ProfileLevel")
        self.ProfileName = params.get("ProfileName")
        if params.get("ProfileInfo") is not None:
            self.ProfileInfo = ProfileInfo()
            self.ProfileInfo._deserialize(params.get("ProfileInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        