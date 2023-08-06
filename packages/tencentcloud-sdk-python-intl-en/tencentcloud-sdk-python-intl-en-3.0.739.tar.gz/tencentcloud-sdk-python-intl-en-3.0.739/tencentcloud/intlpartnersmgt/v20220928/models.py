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


class ActionSummaryOverviewItem(AbstractModel):
    """Transaction type details in the customer bill data totaled by payment mode

    """

    def __init__(self):
        r"""
        :param ActionType: Transaction type code
Note: This field may return null, indicating that no valid values can be obtained.
        :type ActionType: str
        :param ActionTypeName: Transaction type name
Note: This field may return null, indicating that no valid values can be obtained.
        :type ActionTypeName: str
        :param OriginalCost: The actual total consumption amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: str
        :param VoucherPayAmount: The deducted voucher amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type VoucherPayAmount: str
        :param TotalCost: Total consumption amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalCost: str
        """
        self.ActionType = None
        self.ActionTypeName = None
        self.OriginalCost = None
        self.VoucherPayAmount = None
        self.TotalCost = None


    def _deserialize(self, params):
        self.ActionType = params.get("ActionType")
        self.ActionTypeName = params.get("ActionTypeName")
        self.OriginalCost = params.get("OriginalCost")
        self.VoucherPayAmount = params.get("VoucherPayAmount")
        self.TotalCost = params.get("TotalCost")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AllocateCustomerCreditRequest(AbstractModel):
    """AllocateCustomerCredit request structure.

    """

    def __init__(self):
        r"""
        :param AddedCredit: Specific value of the credit allocated to the customer
        :type AddedCredit: float
        :param ClientUin: Customer UIN
        :type ClientUin: int
        """
        self.AddedCredit = None
        self.ClientUin = None


    def _deserialize(self, params):
        self.AddedCredit = params.get("AddedCredit")
        self.ClientUin = params.get("ClientUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AllocateCustomerCreditResponse(AbstractModel):
    """AllocateCustomerCredit response structure.

    """

    def __init__(self):
        r"""
        :param TotalCredit: The updated total credit
        :type TotalCredit: float
        :param RemainingCredit: The updated available credit
        :type RemainingCredit: float
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCredit = None
        self.RemainingCredit = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCredit = params.get("TotalCredit")
        self.RemainingCredit = params.get("RemainingCredit")
        self.RequestId = params.get("RequestId")


class BillDetailData(AbstractModel):
    """Customer bill details

    """

    def __init__(self):
        r"""
        :param PayerAccountId: Reseller account
Note: This field may return null, indicating that no valid values can be obtained.
        :type PayerAccountId: int
        :param OwnerAccountId: Customer account
Note: This field may return null, indicating that no valid values can be obtained.
        :type OwnerAccountId: int
        :param OperatorAccountId: Operator account
Note: This field may return null, indicating that no valid values can be obtained.
        :type OperatorAccountId: int
        :param ProductName: Product name
Note: This field may return null, indicating that no valid values can be obtained.
        :type ProductName: str
        :param BillingMode: Billing mode
`Monthly subscription` (Monthly subscription)
`Pay-As-You-Go resources` (Pay-as-you-go)
`Standard RI` (Reserved instance)
Note: This field may return null, indicating that no valid values can be obtained.
        :type BillingMode: str
        :param ProjectName: Project name

Note: This field may return null, indicating that no valid values can be obtained.
        :type ProjectName: str
        :param Region: Resource region
Note: This field may return null, indicating that no valid values can be obtained.
        :type Region: str
        :param AvailabilityZone: Resource AZ
Note: This field may return null, indicating that no valid values can be obtained.
        :type AvailabilityZone: str
        :param InstanceId: Instance ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceId: str
        :param InstanceName: Instance name
Note: This field may return null, indicating that no valid values can be obtained.
        :type InstanceName: str
        :param SubProductName: Subproduct name

Note: This field may return null, indicating that no valid values can be obtained.
        :type SubProductName: str
        :param TransactionType: Settlement type
Note: This field may return null, indicating that no valid values can be obtained.
        :type TransactionType: str
        :param TransactionId: Transaction ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type TransactionId: str
        :param TransactionTime: Settlement time

Note: This field may return null, indicating that no valid values can be obtained.
        :type TransactionTime: str
        :param UsageStartTime: Start time of resource use
Note: This field may return null, indicating that no valid values can be obtained.
        :type UsageStartTime: str
        :param UsageEndTime: End time of resource use
Note: This field may return null, indicating that no valid values can be obtained.
        :type UsageEndTime: str
        :param ComponentType: Component
Note: This field may return null, indicating that no valid values can be obtained.
        :type ComponentType: str
        :param ComponentName: Component name
Note: This field may return null, indicating that no valid values can be obtained.
        :type ComponentName: str
        :param ComponentListPrice: Component list price
Note: This field may return null, indicating that no valid values can be obtained.
        :type ComponentListPrice: str
        :param ComponentPriceMeasurementUnit: Price unit
Note: This field may return null, indicating that no valid values can be obtained.
        :type ComponentPriceMeasurementUnit: str
        :param ComponentUsage: Component usage
Note: This field may return null, indicating that no valid values can be obtained.
        :type ComponentUsage: str
        :param ComponentUsageUnit: Component usage unit
Note: This field may return null, indicating that no valid values can be obtained.
        :type ComponentUsageUnit: str
        :param UsageDuration: Resource usage duration
Note: This field may return null, indicating that no valid values can be obtained.
        :type UsageDuration: str
        :param DurationUnit: Duration unit
Note: This field may return null, indicating that no valid values can be obtained.
        :type DurationUnit: str
        :param OriginalCost: Original cost
Original cost = component list price * component usage * usage duration
Note: This field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: str
        :param DiscountRate: Discount, which defaults to `1`, indicating there is no discount.
Note: This field may return null, indicating that no valid values can be obtained.
        :type DiscountRate: str
        :param Currency: Currency
Note: This field may return null, indicating that no valid values can be obtained.
        :type Currency: str
        :param TotalAmountAfterDiscount: Discounted total
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalAmountAfterDiscount: str
        :param VoucherDeduction: Voucher deduction
Note: This field may return null, indicating that no valid values can be obtained.
        :type VoucherDeduction: str
        :param TotalCost: Total cost = discounted total - voucher deduction
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalCost: str
        """
        self.PayerAccountId = None
        self.OwnerAccountId = None
        self.OperatorAccountId = None
        self.ProductName = None
        self.BillingMode = None
        self.ProjectName = None
        self.Region = None
        self.AvailabilityZone = None
        self.InstanceId = None
        self.InstanceName = None
        self.SubProductName = None
        self.TransactionType = None
        self.TransactionId = None
        self.TransactionTime = None
        self.UsageStartTime = None
        self.UsageEndTime = None
        self.ComponentType = None
        self.ComponentName = None
        self.ComponentListPrice = None
        self.ComponentPriceMeasurementUnit = None
        self.ComponentUsage = None
        self.ComponentUsageUnit = None
        self.UsageDuration = None
        self.DurationUnit = None
        self.OriginalCost = None
        self.DiscountRate = None
        self.Currency = None
        self.TotalAmountAfterDiscount = None
        self.VoucherDeduction = None
        self.TotalCost = None


    def _deserialize(self, params):
        self.PayerAccountId = params.get("PayerAccountId")
        self.OwnerAccountId = params.get("OwnerAccountId")
        self.OperatorAccountId = params.get("OperatorAccountId")
        self.ProductName = params.get("ProductName")
        self.BillingMode = params.get("BillingMode")
        self.ProjectName = params.get("ProjectName")
        self.Region = params.get("Region")
        self.AvailabilityZone = params.get("AvailabilityZone")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.SubProductName = params.get("SubProductName")
        self.TransactionType = params.get("TransactionType")
        self.TransactionId = params.get("TransactionId")
        self.TransactionTime = params.get("TransactionTime")
        self.UsageStartTime = params.get("UsageStartTime")
        self.UsageEndTime = params.get("UsageEndTime")
        self.ComponentType = params.get("ComponentType")
        self.ComponentName = params.get("ComponentName")
        self.ComponentListPrice = params.get("ComponentListPrice")
        self.ComponentPriceMeasurementUnit = params.get("ComponentPriceMeasurementUnit")
        self.ComponentUsage = params.get("ComponentUsage")
        self.ComponentUsageUnit = params.get("ComponentUsageUnit")
        self.UsageDuration = params.get("UsageDuration")
        self.DurationUnit = params.get("DurationUnit")
        self.OriginalCost = params.get("OriginalCost")
        self.DiscountRate = params.get("DiscountRate")
        self.Currency = params.get("Currency")
        self.TotalAmountAfterDiscount = params.get("TotalAmountAfterDiscount")
        self.VoucherDeduction = params.get("VoucherDeduction")
        self.TotalCost = params.get("TotalCost")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BusinessSummaryOverviewItem(AbstractModel):
    """Product details in the customer bill data totaled by product

    """

    def __init__(self):
        r"""
        :param BusinessCode: Product code
Note: This field may return null, indicating that no valid values can be obtained.
        :type BusinessCode: str
        :param BusinessCodeName: Product name
Note: This field may return null, indicating that no valid values can be obtained.
        :type BusinessCodeName: str
        :param OriginalCost: List price accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: str
        :param VoucherPayAmount: The deducted voucher amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type VoucherPayAmount: str
        :param TotalCost: Consumption amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalCost: str
        """
        self.BusinessCode = None
        self.BusinessCodeName = None
        self.OriginalCost = None
        self.VoucherPayAmount = None
        self.TotalCost = None


    def _deserialize(self, params):
        self.BusinessCode = params.get("BusinessCode")
        self.BusinessCodeName = params.get("BusinessCodeName")
        self.OriginalCost = params.get("OriginalCost")
        self.VoucherPayAmount = params.get("VoucherPayAmount")
        self.TotalCost = params.get("TotalCost")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CountryCodeItem(AbstractModel):
    """Element type of the `GetCountryCodes` API

    """

    def __init__(self):
        r"""
        :param EnName: Country/region name in English
        :type EnName: str
        :param Name: Country/region name in Chinese
        :type Name: str
        :param IOS2: 
        :type IOS2: str
        :param IOS3: 
        :type IOS3: str
        :param Code: International dialing code
        :type Code: str
        """
        self.EnName = None
        self.Name = None
        self.IOS2 = None
        self.IOS3 = None
        self.Code = None


    def _deserialize(self, params):
        self.EnName = params.get("EnName")
        self.Name = params.get("Name")
        self.IOS2 = params.get("IOS2")
        self.IOS3 = params.get("IOS3")
        self.Code = params.get("Code")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAccountRequest(AbstractModel):
    """CreateAccount request structure.

    """

    def __init__(self):
        r"""
        :param AccountType: Account type of a new customer. Valid values: `personal`, `company`.
        :type AccountType: str
        :param Mail: Registered email address, which should be valid and correct.
For example, account@qq.com.
        :type Mail: str
        :param Password: Account password
Length limit: 8-20 characters
A password must contain numbers, letters, and symbols (!@#$%^&*()). Space is not allowed.
        :type Password: str
        :param ConfirmPassword: The confirmed password, which must be the same as that entered in the `Password` field.
        :type ConfirmPassword: str
        :param PhoneNum: Customer mobile number, which should be valid and correct.
A global mobile number within 1-32 digits is allowed, such as 18888888888.
        :type PhoneNum: str
        :param CountryCode: Customer's country/region code, which can be obtained via the `GetCountryCodes` API, such as "852".
        :type CountryCode: str
        :param Area: Customer's ISO2 standard country/region code, which can be obtained via the `GetCountryCodes` API. It should correspond to the `CountryCode` field, such as `HK`.
        :type Area: str
        :param Extended: Extension field, which is left empty by default.
        :type Extended: str
        """
        self.AccountType = None
        self.Mail = None
        self.Password = None
        self.ConfirmPassword = None
        self.PhoneNum = None
        self.CountryCode = None
        self.Area = None
        self.Extended = None


    def _deserialize(self, params):
        self.AccountType = params.get("AccountType")
        self.Mail = params.get("Mail")
        self.Password = params.get("Password")
        self.ConfirmPassword = params.get("ConfirmPassword")
        self.PhoneNum = params.get("PhoneNum")
        self.CountryCode = params.get("CountryCode")
        self.Area = params.get("Area")
        self.Extended = params.get("Extended")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAccountResponse(AbstractModel):
    """CreateAccount response structure.

    """

    def __init__(self):
        r"""
        :param Uin: Account UIN
        :type Uin: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Uin = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Uin = params.get("Uin")
        self.RequestId = params.get("RequestId")


class DescribeBillSummaryByPayModeRequest(AbstractModel):
    """DescribeBillSummaryByPayMode request structure.

    """

    def __init__(self):
        r"""
        :param BillMonth: Bill month in the format of "yyyy-MM"
        :type BillMonth: str
        :param CustomerUin: Customer UIN
        :type CustomerUin: int
        """
        self.BillMonth = None
        self.CustomerUin = None


    def _deserialize(self, params):
        self.BillMonth = params.get("BillMonth")
        self.CustomerUin = params.get("CustomerUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillSummaryByPayModeResponse(AbstractModel):
    """DescribeBillSummaryByPayMode response structure.

    """

    def __init__(self):
        r"""
        :param SummaryOverview: Payment mode details in the customer bill data totaled by payment mode
Note: This field may return null, indicating that no valid values can be obtained.
        :type SummaryOverview: list of PayModeSummaryOverviewItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SummaryOverview = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SummaryOverview") is not None:
            self.SummaryOverview = []
            for item in params.get("SummaryOverview"):
                obj = PayModeSummaryOverviewItem()
                obj._deserialize(item)
                self.SummaryOverview.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBillSummaryByProductRequest(AbstractModel):
    """DescribeBillSummaryByProduct request structure.

    """

    def __init__(self):
        r"""
        :param BillMonth: Bill month in the format of "yyyy-MM"
        :type BillMonth: str
        :param CustomerUin: Customer UIN
        :type CustomerUin: int
        """
        self.BillMonth = None
        self.CustomerUin = None


    def _deserialize(self, params):
        self.BillMonth = params.get("BillMonth")
        self.CustomerUin = params.get("CustomerUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillSummaryByProductResponse(AbstractModel):
    """DescribeBillSummaryByProduct response structure.

    """

    def __init__(self):
        r"""
        :param SummaryOverview: Bill details from the product dimension
Note: This field may return null, indicating that no valid values can be obtained.
        :type SummaryOverview: list of BusinessSummaryOverviewItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SummaryOverview = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SummaryOverview") is not None:
            self.SummaryOverview = []
            for item in params.get("SummaryOverview"):
                obj = BusinessSummaryOverviewItem()
                obj._deserialize(item)
                self.SummaryOverview.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBillSummaryByRegionRequest(AbstractModel):
    """DescribeBillSummaryByRegion request structure.

    """

    def __init__(self):
        r"""
        :param BillMonth: Bill month in the format of "yyyy-MM"
        :type BillMonth: str
        :param CustomerUin: Customer UIN
        :type CustomerUin: int
        """
        self.BillMonth = None
        self.CustomerUin = None


    def _deserialize(self, params):
        self.BillMonth = params.get("BillMonth")
        self.CustomerUin = params.get("CustomerUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillSummaryByRegionResponse(AbstractModel):
    """DescribeBillSummaryByRegion response structure.

    """

    def __init__(self):
        r"""
        :param SummaryOverview: Region details in the customer bill data totaled by region
Note: This field may return null, indicating that no valid values can be obtained.
        :type SummaryOverview: list of RegionSummaryOverviewItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SummaryOverview = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SummaryOverview") is not None:
            self.SummaryOverview = []
            for item in params.get("SummaryOverview"):
                obj = RegionSummaryOverviewItem()
                obj._deserialize(item)
                self.SummaryOverview.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCustomerBillDetailRequest(AbstractModel):
    """DescribeCustomerBillDetail request structure.

    """

    def __init__(self):
        r"""
        :param CustomerUin: Customer UIN
        :type CustomerUin: int
        :param Month: The queried month in “YYYY-MM” format, such as 2023-01.
        :type Month: str
        :param PageSize: A pagination parameter that specifies the number of entries per page
        :type PageSize: int
        :param Page: A pagination parameter that specifies the current page number
        :type Page: int
        :param PayMode: Billing mode. Valid values:
`prePay` (Monthly subscription)
`postPay` (Pay-as-you-go)
        :type PayMode: str
        :param ActionType: Transaction type. Valid values:
`prepay_purchase` (Purchase)
`prepay_renew` (Renewal)
`prepay_modify` (Upgrade/Downgrade)
`prepay_return` ( Monthly subscription refund)
`postpay_deduct` (Pay-as-you-go)
`postpay_deduct_h` (Hourly settlement)
`postpay_deduct_d` (Daily settlement)
`postpay_deduct_m` (Monthly settlement)
`offline_deduct` (Offline project deduction)
`online_deduct` (Offline product deduction)
`recon_deduct` (Adjustment - deduction)
`recon_increase` (Adjustment - compensation)
`ripay_purchase` (One-off RI Fee)
`postpay_deduct_s` (Spot)
`ri_hour_pay` (Hourly RI fee)
`prePurchase` (New monthly subscription)
`preRenew` (Monthly subscription renewal)
`preUpgrade` (Upgrade/Downgrade)
`preDowngrade` (Upgrade/Downgrade)
`svp_hour_pay` (Hourly Savings Plan fee)
`recon_guarantee` (Minimum spend deduction)
`pre_purchase` (New monthly subscription)
`pre_renew` (Monthly subscription renewal)
`pre_upgrade` (Upgrade/Downgrade)
`pre_downgrade` (Upgrade/Downgrade)
        :type ActionType: str
        :param IsConfirmed: Payment status
`0`: N/A
`1`: Paid
`2`: Unpaid
        :type IsConfirmed: str
        """
        self.CustomerUin = None
        self.Month = None
        self.PageSize = None
        self.Page = None
        self.PayMode = None
        self.ActionType = None
        self.IsConfirmed = None


    def _deserialize(self, params):
        self.CustomerUin = params.get("CustomerUin")
        self.Month = params.get("Month")
        self.PageSize = params.get("PageSize")
        self.Page = params.get("Page")
        self.PayMode = params.get("PayMode")
        self.ActionType = params.get("ActionType")
        self.IsConfirmed = params.get("IsConfirmed")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCustomerBillDetailResponse(AbstractModel):
    """DescribeCustomerBillDetail response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of data entries
        :type Total: int
        :param DetailSet: Data details
Note: This field may return null, indicating that no valid values can be obtained.
        :type DetailSet: list of BillDetailData
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.DetailSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("DetailSet") is not None:
            self.DetailSet = []
            for item in params.get("DetailSet"):
                obj = BillDetailData()
                obj._deserialize(item)
                self.DetailSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCustomerBillSummaryRequest(AbstractModel):
    """DescribeCustomerBillSummary request structure.

    """

    def __init__(self):
        r"""
        :param CustomerUin: Customer UIN
        :type CustomerUin: int
        :param Month: The queried month in “YYYY-MM” format, such as 2023-01.
        :type Month: str
        :param PayMode: Billing mode. Valid values:
`prePay` (Monthly subscription)
`postPay` (Pay-as-you-go)
        :type PayMode: str
        :param ActionType: Transaction type. Valid values:
`prepay_purchase` (Purchase)
`prepay_renew` (Renewal)
`prepay_modify` (Upgrade/Downgrade)
`prepay_return` (Monthly subscription refund)
`postpay_deduct` (Pay-as-you-go)
`postpay_deduct_h` (Hourly settlement)
`postpay_deduct_d` (Daily settlement)
`postpay_deduct_m` (Monthly settlement)
`offline_deduct` (Offline project deduction)
`online_deduct` (Offline product deduction)
`recon_deduct` (Adjustment - deduction)
`recon_increase` (Adjustment - compensation)
`ripay_purchase` (One-off RI Fee)
`postpay_deduct_s` (Spot)
`ri_hour_pay` (Hourly RI fee)
`prePurchase` (New monthly subscription)
`preRenew` (Monthly subscription renewal)
`preUpgrade` (Upgrade/Downgrade)
`preDowngrade` (Upgrade/Downgrade)
`svp_hour_pay` (Hourly Savings Plan fee)
`recon_guarantee` (Minimum spend deduction)
`pre_purchase` (New monthly subscription)
`pre_renew` (Monthly subscription renewal)
`pre_upgrade` (Upgrade/Downgrade)
`pre_downgrade` (Upgrade/Downgrade)
        :type ActionType: str
        :param IsConfirmed: Payment status
`0`: N/A
`1`: Paid
`2`: Unpaid
        :type IsConfirmed: str
        """
        self.CustomerUin = None
        self.Month = None
        self.PayMode = None
        self.ActionType = None
        self.IsConfirmed = None


    def _deserialize(self, params):
        self.CustomerUin = params.get("CustomerUin")
        self.Month = params.get("Month")
        self.PayMode = params.get("PayMode")
        self.ActionType = params.get("ActionType")
        self.IsConfirmed = params.get("IsConfirmed")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCustomerBillSummaryResponse(AbstractModel):
    """DescribeCustomerBillSummary response structure.

    """

    def __init__(self):
        r"""
        :param TotalCost: Total amount
        :type TotalCost: float
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCost = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCost = params.get("TotalCost")
        self.RequestId = params.get("RequestId")


class GetCountryCodesRequest(AbstractModel):
    """GetCountryCodes request structure.

    """


class GetCountryCodesResponse(AbstractModel):
    """GetCountryCodes response structure.

    """

    def __init__(self):
        r"""
        :param Data: List of country/region codes
        :type Data: list of CountryCodeItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = CountryCodeItem()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class PayModeSummaryOverviewItem(AbstractModel):
    """Payment mode details in the customer bill data totaled by payment mode

    """

    def __init__(self):
        r"""
        :param PayMode: Billing mode
Note: This field may return null, indicating that no valid values can be obtained.
        :type PayMode: str
        :param PayModeName: Billing mode name
Note: This field may return null, indicating that no valid values can be obtained.
        :type PayModeName: str
        :param OriginalCost: The actual total consumption amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: str
        :param Detail: Bill details in each payment mode
Note: This field may return null, indicating that no valid values can be obtained.
        :type Detail: list of ActionSummaryOverviewItem
        :param VoucherPayAmount: The deducted voucher amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type VoucherPayAmount: str
        :param TotalCost: Total consumption amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalCost: str
        """
        self.PayMode = None
        self.PayModeName = None
        self.OriginalCost = None
        self.Detail = None
        self.VoucherPayAmount = None
        self.TotalCost = None


    def _deserialize(self, params):
        self.PayMode = params.get("PayMode")
        self.PayModeName = params.get("PayModeName")
        self.OriginalCost = params.get("OriginalCost")
        if params.get("Detail") is not None:
            self.Detail = []
            for item in params.get("Detail"):
                obj = ActionSummaryOverviewItem()
                obj._deserialize(item)
                self.Detail.append(obj)
        self.VoucherPayAmount = params.get("VoucherPayAmount")
        self.TotalCost = params.get("TotalCost")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryCreditAllocationHistoryData(AbstractModel):
    """Returned information for querying the customer credit allocation records

    """

    def __init__(self):
        r"""
        :param AllocatedTime: Allocation time
        :type AllocatedTime: str
        :param Operator: Operator
        :type Operator: str
        :param Credit: Allocated credit value
        :type Credit: float
        :param AllocatedCredit: The allocated total credit
        :type AllocatedCredit: float
        """
        self.AllocatedTime = None
        self.Operator = None
        self.Credit = None
        self.AllocatedCredit = None


    def _deserialize(self, params):
        self.AllocatedTime = params.get("AllocatedTime")
        self.Operator = params.get("Operator")
        self.Credit = params.get("Credit")
        self.AllocatedCredit = params.get("AllocatedCredit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryCreditAllocationHistoryRequest(AbstractModel):
    """QueryCreditAllocationHistory request structure.

    """

    def __init__(self):
        r"""
        :param ClientUin: Customer UIN
        :type ClientUin: int
        :param Page: Page number
        :type Page: int
        :param PageSize: Number of data entries per page
        :type PageSize: int
        """
        self.ClientUin = None
        self.Page = None
        self.PageSize = None


    def _deserialize(self, params):
        self.ClientUin = params.get("ClientUin")
        self.Page = params.get("Page")
        self.PageSize = params.get("PageSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryCreditAllocationHistoryResponse(AbstractModel):
    """QueryCreditAllocationHistory response structure.

    """

    def __init__(self):
        r"""
        :param Total: Total number of records
Note: This field may return null, indicating that no valid values can be obtained.
        :type Total: int
        :param History: List of record details
Note: This field may return null, indicating that no valid values can be obtained.
        :type History: list of QueryCreditAllocationHistoryData
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Total = None
        self.History = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("History") is not None:
            self.History = []
            for item in params.get("History"):
                obj = QueryCreditAllocationHistoryData()
                obj._deserialize(item)
                self.History.append(obj)
        self.RequestId = params.get("RequestId")


class QueryCreditByUinListRequest(AbstractModel):
    """QueryCreditByUinList request structure.

    """

    def __init__(self):
        r"""
        :param UinList: User list
        :type UinList: list of int non-negative
        """
        self.UinList = None


    def _deserialize(self, params):
        self.UinList = params.get("UinList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryCreditByUinListResponse(AbstractModel):
    """QueryCreditByUinList response structure.

    """

    def __init__(self):
        r"""
        :param Data: User information list
        :type Data: list of QueryDirectCustomersCreditData
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = QueryDirectCustomersCreditData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class QueryCustomersCreditData(AbstractModel):
    """Complex type of output parameters for querying customer's credit

    """

    def __init__(self):
        r"""
        :param Name: Name
        :type Name: str
        :param Type: Type
        :type Type: str
        :param Mobile: Mobile number
        :type Mobile: str
        :param Email: Email
        :type Email: str
        :param Arrears: Overdue payment flag
        :type Arrears: str
        :param AssociationTime: Binding time
        :type AssociationTime: str
        :param RecentExpiry: Expiration time
        :type RecentExpiry: str
        :param ClientUin: Customer UIN
        :type ClientUin: int
        :param Credit: Credit allocated to a customer
        :type Credit: float
        :param RemainingCredit: The remaining credit of a customer
        :type RemainingCredit: float
        :param IdentifyType: `0`: Identity not verified; `1`: Individual identity verified; `2`: Enterprise identity verified.
        :type IdentifyType: int
        :param Remark: Customer remarks
        :type Remark: str
        :param Force: Forced status
        :type Force: int
        """
        self.Name = None
        self.Type = None
        self.Mobile = None
        self.Email = None
        self.Arrears = None
        self.AssociationTime = None
        self.RecentExpiry = None
        self.ClientUin = None
        self.Credit = None
        self.RemainingCredit = None
        self.IdentifyType = None
        self.Remark = None
        self.Force = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.Mobile = params.get("Mobile")
        self.Email = params.get("Email")
        self.Arrears = params.get("Arrears")
        self.AssociationTime = params.get("AssociationTime")
        self.RecentExpiry = params.get("RecentExpiry")
        self.ClientUin = params.get("ClientUin")
        self.Credit = params.get("Credit")
        self.RemainingCredit = params.get("RemainingCredit")
        self.IdentifyType = params.get("IdentifyType")
        self.Remark = params.get("Remark")
        self.Force = params.get("Force")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryCustomersCreditRequest(AbstractModel):
    """QueryCustomersCredit request structure.

    """

    def __init__(self):
        r"""
        :param FilterType: Search condition type. You can only search by customer ID, name, remarks, or email.
        :type FilterType: str
        :param Filter: Search condition
        :type Filter: str
        :param Page: A pagination parameter that specifies the current page number, with a value starting from 1.
        :type Page: int
        :param PageSize: A pagination parameter that specifies the number of entries per page.
        :type PageSize: int
        :param Order: A sort parameter that specifies the sort order. Valid values: `desc` (descending order), or `asc` (ascending order) based on `AssociationTime`. The value will be `desc` if left empty.
        :type Order: str
        """
        self.FilterType = None
        self.Filter = None
        self.Page = None
        self.PageSize = None
        self.Order = None


    def _deserialize(self, params):
        self.FilterType = params.get("FilterType")
        self.Filter = params.get("Filter")
        self.Page = params.get("Page")
        self.PageSize = params.get("PageSize")
        self.Order = params.get("Order")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryCustomersCreditResponse(AbstractModel):
    """QueryCustomersCredit response structure.

    """

    def __init__(self):
        r"""
        :param Data: The list of queried customers
Note: This field may return null, indicating that no valid values can be obtained.
        :type Data: list of QueryCustomersCreditData
        :param Total: Number of customers
        :type Total: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = QueryCustomersCreditData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class QueryDirectCustomersCreditData(AbstractModel):
    """The credit information of direct customers

    """

    def __init__(self):
        r"""
        :param Uin: User UIN
        :type Uin: int
        :param TotalCredit: Total credit
        :type TotalCredit: float
        :param RemainingCredit: Remaining credit
        :type RemainingCredit: float
        """
        self.Uin = None
        self.TotalCredit = None
        self.RemainingCredit = None


    def _deserialize(self, params):
        self.Uin = params.get("Uin")
        self.TotalCredit = params.get("TotalCredit")
        self.RemainingCredit = params.get("RemainingCredit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryDirectCustomersCreditRequest(AbstractModel):
    """QueryDirectCustomersCredit request structure.

    """


class QueryDirectCustomersCreditResponse(AbstractModel):
    """QueryDirectCustomersCredit response structure.

    """

    def __init__(self):
        r"""
        :param Data: Direct customer information list
        :type Data: list of QueryDirectCustomersCreditData
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = QueryDirectCustomersCreditData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class QueryPartnerCreditRequest(AbstractModel):
    """QueryPartnerCredit request structure.

    """


class QueryPartnerCreditResponse(AbstractModel):
    """QueryPartnerCredit response structure.

    """

    def __init__(self):
        r"""
        :param AllocatedCredit: Allocated credit
        :type AllocatedCredit: float
        :param TotalCredit: Total credit
        :type TotalCredit: float
        :param RemainingCredit: Remaining credit
        :type RemainingCredit: float
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AllocatedCredit = None
        self.TotalCredit = None
        self.RemainingCredit = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AllocatedCredit = params.get("AllocatedCredit")
        self.TotalCredit = params.get("TotalCredit")
        self.RemainingCredit = params.get("RemainingCredit")
        self.RequestId = params.get("RequestId")


class QueryVoucherAmountByUinItem(AbstractModel):
    """Customer voucher quota

    """

    def __init__(self):
        r"""
        :param ClientUin: Customer UIN
        :type ClientUin: int
        :param TotalAmount: Voucher quota
        :type TotalAmount: float
        :param RemainAmount: Voucher amount
        :type RemainAmount: float
        """
        self.ClientUin = None
        self.TotalAmount = None
        self.RemainAmount = None


    def _deserialize(self, params):
        self.ClientUin = params.get("ClientUin")
        self.TotalAmount = params.get("TotalAmount")
        self.RemainAmount = params.get("RemainAmount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryVoucherAmountByUinRequest(AbstractModel):
    """QueryVoucherAmountByUin request structure.

    """

    def __init__(self):
        r"""
        :param ClientUins: Customer UIN list
        :type ClientUins: list of int non-negative
        """
        self.ClientUins = None


    def _deserialize(self, params):
        self.ClientUins = params.get("ClientUins")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryVoucherAmountByUinResponse(AbstractModel):
    """QueryVoucherAmountByUin response structure.

    """

    def __init__(self):
        r"""
        :param Data: Customer voucher quota information
        :type Data: list of QueryVoucherAmountByUinItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = QueryVoucherAmountByUinItem()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class QueryVoucherListByUinItem(AbstractModel):
    """Voucher information of a single customer

    """

    def __init__(self):
        r"""
        :param ClientUin: Customer UIN
        :type ClientUin: int
        :param TotalCount: The total number of vouchers
        :type TotalCount: int
        :param Data: Voucher details
        :type Data: list of QueryVoucherListByUinVoucherItem
        """
        self.ClientUin = None
        self.TotalCount = None
        self.Data = None


    def _deserialize(self, params):
        self.ClientUin = params.get("ClientUin")
        self.TotalCount = params.get("TotalCount")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = QueryVoucherListByUinVoucherItem()
                obj._deserialize(item)
                self.Data.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryVoucherListByUinRequest(AbstractModel):
    """QueryVoucherListByUin request structure.

    """

    def __init__(self):
        r"""
        :param ClientUins: Customer UIN list
        :type ClientUins: list of int non-negative
        :param Status: Voucher status. If this parameter is not passed in, all status will be queried by default. Valid values: `Unused`, `Used`, `Expired`.
        :type Status: str
        """
        self.ClientUins = None
        self.Status = None


    def _deserialize(self, params):
        self.ClientUins = params.get("ClientUins")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryVoucherListByUinResponse(AbstractModel):
    """QueryVoucherListByUin response structure.

    """

    def __init__(self):
        r"""
        :param Data: Customer voucher information
        :type Data: list of QueryVoucherListByUinItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = QueryVoucherListByUinItem()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class QueryVoucherListByUinVoucherItem(AbstractModel):
    """Customer voucher information

    """

    def __init__(self):
        r"""
        :param VoucherId: Voucher ID
        :type VoucherId: str
        :param VoucherStatus: Voucher status
        :type VoucherStatus: str
        :param TotalAmount: Voucher value
        :type TotalAmount: float
        :param RemainAmount: Balance
        :type RemainAmount: float
        """
        self.VoucherId = None
        self.VoucherStatus = None
        self.TotalAmount = None
        self.RemainAmount = None


    def _deserialize(self, params):
        self.VoucherId = params.get("VoucherId")
        self.VoucherStatus = params.get("VoucherStatus")
        self.TotalAmount = params.get("TotalAmount")
        self.RemainAmount = params.get("RemainAmount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryVoucherPoolRequest(AbstractModel):
    """QueryVoucherPool request structure.

    """


class QueryVoucherPoolResponse(AbstractModel):
    """QueryVoucherPool response structure.

    """

    def __init__(self):
        r"""
        :param AgentName: Reseller name
        :type AgentName: str
        :param AccountType: Reseller role type (1: Reseller; 2: Distributor; 3: Second-level reseller)
        :type AccountType: int
        :param TotalQuota: Total quota
        :type TotalQuota: float
        :param RemainingQuota: Remaining quota
        :type RemainingQuota: float
        :param IssuedNum: The number of issued vouchers
        :type IssuedNum: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.AgentName = None
        self.AccountType = None
        self.TotalQuota = None
        self.RemainingQuota = None
        self.IssuedNum = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AgentName = params.get("AgentName")
        self.AccountType = params.get("AccountType")
        self.TotalQuota = params.get("TotalQuota")
        self.RemainingQuota = params.get("RemainingQuota")
        self.IssuedNum = params.get("IssuedNum")
        self.RequestId = params.get("RequestId")


class RegionSummaryOverviewItem(AbstractModel):
    """Region details in the customer bill data totaled by region

    """

    def __init__(self):
        r"""
        :param RegionId: Region ID
Note: This field may return null, indicating that no valid values can be obtained.
        :type RegionId: str
        :param RegionName: Region name
Note: This field may return null, indicating that no valid values can be obtained.
        :type RegionName: str
        :param OriginalCost: The actual total consumption amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type OriginalCost: str
        :param VoucherPayAmount: The deducted voucher amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type VoucherPayAmount: str
        :param TotalCost: Total consumption amount accurate down to eight decimal places
Note: This field may return null, indicating that no valid values can be obtained.
        :type TotalCost: str
        """
        self.RegionId = None
        self.RegionName = None
        self.OriginalCost = None
        self.VoucherPayAmount = None
        self.TotalCost = None


    def _deserialize(self, params):
        self.RegionId = params.get("RegionId")
        self.RegionName = params.get("RegionName")
        self.OriginalCost = params.get("OriginalCost")
        self.VoucherPayAmount = params.get("VoucherPayAmount")
        self.TotalCost = params.get("TotalCost")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        