'''
# `aws_default_subnet`

Refer to the Terraform Registory for docs: [`aws_default_subnet`](https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DefaultSubnet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.defaultSubnet.DefaultSubnet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet aws_default_subnet}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        assign_ipv6_address_on_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
        enable_dns64: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_resource_name_dns_aaaa_record_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_resource_name_dns_a_record_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ipv6_cidr_block: typing.Optional[builtins.str] = None,
        ipv6_native: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_customer_owned_ip_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_public_ip_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_dns_hostname_type_on_launch: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DefaultSubnetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet aws_default_subnet} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#availability_zone DefaultSubnet#availability_zone}.
        :param assign_ipv6_address_on_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#assign_ipv6_address_on_creation DefaultSubnet#assign_ipv6_address_on_creation}.
        :param customer_owned_ipv4_pool: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#customer_owned_ipv4_pool DefaultSubnet#customer_owned_ipv4_pool}.
        :param enable_dns64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_dns64 DefaultSubnet#enable_dns64}.
        :param enable_resource_name_dns_aaaa_record_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_resource_name_dns_aaaa_record_on_launch DefaultSubnet#enable_resource_name_dns_aaaa_record_on_launch}.
        :param enable_resource_name_dns_a_record_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_resource_name_dns_a_record_on_launch DefaultSubnet#enable_resource_name_dns_a_record_on_launch}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#force_destroy DefaultSubnet#force_destroy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#id DefaultSubnet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ipv6_cidr_block: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#ipv6_cidr_block DefaultSubnet#ipv6_cidr_block}.
        :param ipv6_native: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#ipv6_native DefaultSubnet#ipv6_native}.
        :param map_customer_owned_ip_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#map_customer_owned_ip_on_launch DefaultSubnet#map_customer_owned_ip_on_launch}.
        :param map_public_ip_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#map_public_ip_on_launch DefaultSubnet#map_public_ip_on_launch}.
        :param private_dns_hostname_type_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#private_dns_hostname_type_on_launch DefaultSubnet#private_dns_hostname_type_on_launch}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#tags DefaultSubnet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#tags_all DefaultSubnet#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#timeouts DefaultSubnet#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20aa5449ccb08912d8c1f3230e88bd0d5edc994a2dee3b2c611422c009d04acf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DefaultSubnetConfig(
            availability_zone=availability_zone,
            assign_ipv6_address_on_creation=assign_ipv6_address_on_creation,
            customer_owned_ipv4_pool=customer_owned_ipv4_pool,
            enable_dns64=enable_dns64,
            enable_resource_name_dns_aaaa_record_on_launch=enable_resource_name_dns_aaaa_record_on_launch,
            enable_resource_name_dns_a_record_on_launch=enable_resource_name_dns_a_record_on_launch,
            force_destroy=force_destroy,
            id=id,
            ipv6_cidr_block=ipv6_cidr_block,
            ipv6_native=ipv6_native,
            map_customer_owned_ip_on_launch=map_customer_owned_ip_on_launch,
            map_public_ip_on_launch=map_public_ip_on_launch,
            private_dns_hostname_type_on_launch=private_dns_hostname_type_on_launch,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#create DefaultSubnet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#delete DefaultSubnet#delete}.
        '''
        value = DefaultSubnetTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAssignIpv6AddressOnCreation")
    def reset_assign_ipv6_address_on_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignIpv6AddressOnCreation", []))

    @jsii.member(jsii_name="resetCustomerOwnedIpv4Pool")
    def reset_customer_owned_ipv4_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerOwnedIpv4Pool", []))

    @jsii.member(jsii_name="resetEnableDns64")
    def reset_enable_dns64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDns64", []))

    @jsii.member(jsii_name="resetEnableResourceNameDnsAaaaRecordOnLaunch")
    def reset_enable_resource_name_dns_aaaa_record_on_launch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableResourceNameDnsAaaaRecordOnLaunch", []))

    @jsii.member(jsii_name="resetEnableResourceNameDnsARecordOnLaunch")
    def reset_enable_resource_name_dns_a_record_on_launch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableResourceNameDnsARecordOnLaunch", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpv6CidrBlock")
    def reset_ipv6_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6CidrBlock", []))

    @jsii.member(jsii_name="resetIpv6Native")
    def reset_ipv6_native(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Native", []))

    @jsii.member(jsii_name="resetMapCustomerOwnedIpOnLaunch")
    def reset_map_customer_owned_ip_on_launch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapCustomerOwnedIpOnLaunch", []))

    @jsii.member(jsii_name="resetMapPublicIpOnLaunch")
    def reset_map_public_ip_on_launch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapPublicIpOnLaunch", []))

    @jsii.member(jsii_name="resetPrivateDnsHostnameTypeOnLaunch")
    def reset_private_dns_hostname_type_on_launch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateDnsHostnameTypeOnLaunch", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneId")
    def availability_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneId"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="enableLniAtDeviceIndex")
    def enable_lni_at_device_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enableLniAtDeviceIndex"))

    @builtins.property
    @jsii.member(jsii_name="existingDefaultSubnet")
    def existing_default_subnet(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "existingDefaultSubnet"))

    @builtins.property
    @jsii.member(jsii_name="ipv6CidrBlockAssociationId")
    def ipv6_cidr_block_association_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6CidrBlockAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="outpostArn")
    def outpost_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outpostArn"))

    @builtins.property
    @jsii.member(jsii_name="ownerId")
    def owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DefaultSubnetTimeoutsOutputReference":
        return typing.cast("DefaultSubnetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @builtins.property
    @jsii.member(jsii_name="assignIpv6AddressOnCreationInput")
    def assign_ipv6_address_on_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assignIpv6AddressOnCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="customerOwnedIpv4PoolInput")
    def customer_owned_ipv4_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerOwnedIpv4PoolInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDns64Input")
    def enable_dns64_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDns64Input"))

    @builtins.property
    @jsii.member(jsii_name="enableResourceNameDnsAaaaRecordOnLaunchInput")
    def enable_resource_name_dns_aaaa_record_on_launch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableResourceNameDnsAaaaRecordOnLaunchInput"))

    @builtins.property
    @jsii.member(jsii_name="enableResourceNameDnsARecordOnLaunchInput")
    def enable_resource_name_dns_a_record_on_launch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableResourceNameDnsARecordOnLaunchInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6CidrBlockInput")
    def ipv6_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6NativeInput")
    def ipv6_native_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv6NativeInput"))

    @builtins.property
    @jsii.member(jsii_name="mapCustomerOwnedIpOnLaunchInput")
    def map_customer_owned_ip_on_launch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mapCustomerOwnedIpOnLaunchInput"))

    @builtins.property
    @jsii.member(jsii_name="mapPublicIpOnLaunchInput")
    def map_public_ip_on_launch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mapPublicIpOnLaunchInput"))

    @builtins.property
    @jsii.member(jsii_name="privateDnsHostnameTypeOnLaunchInput")
    def private_dns_hostname_type_on_launch_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateDnsHostnameTypeOnLaunchInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DefaultSubnetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DefaultSubnetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="assignIpv6AddressOnCreation")
    def assign_ipv6_address_on_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assignIpv6AddressOnCreation"))

    @assign_ipv6_address_on_creation.setter
    def assign_ipv6_address_on_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6c6edede15b6997abbaa5144daf6f15bc852f724cc00254defa76a0125418b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignIpv6AddressOnCreation", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c87160af03b807cf6c232d17a887b2e0312f316537c9d8742c549fa01a9ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="customerOwnedIpv4Pool")
    def customer_owned_ipv4_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerOwnedIpv4Pool"))

    @customer_owned_ipv4_pool.setter
    def customer_owned_ipv4_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f63ae87f3a3869b9d64cfc72bb929e854b9599b956bd46bdacd50105de6cd39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerOwnedIpv4Pool", value)

    @builtins.property
    @jsii.member(jsii_name="enableDns64")
    def enable_dns64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDns64"))

    @enable_dns64.setter
    def enable_dns64(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97b110f5e102da89bf6cc70e5d0b18ddc2dcf49ae9913c3c270bd646e0b3eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDns64", value)

    @builtins.property
    @jsii.member(jsii_name="enableResourceNameDnsAaaaRecordOnLaunch")
    def enable_resource_name_dns_aaaa_record_on_launch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableResourceNameDnsAaaaRecordOnLaunch"))

    @enable_resource_name_dns_aaaa_record_on_launch.setter
    def enable_resource_name_dns_aaaa_record_on_launch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9beb6cd8da55b7c84e3ca40981e8190b7fbf93b0830dec9ec5af570ae38290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourceNameDnsAaaaRecordOnLaunch", value)

    @builtins.property
    @jsii.member(jsii_name="enableResourceNameDnsARecordOnLaunch")
    def enable_resource_name_dns_a_record_on_launch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableResourceNameDnsARecordOnLaunch"))

    @enable_resource_name_dns_a_record_on_launch.setter
    def enable_resource_name_dns_a_record_on_launch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b715570b6be4392fa298c6f3dc8450226a55db21872af5e1af77d25d2df53091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourceNameDnsARecordOnLaunch", value)

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400ca82bba13bdde7e262aab79fdefbdf0ddc9d48cd866c76fc6d47f00feeba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebed193e4de4e498d7dc4b94cf2051d310ebd3085df9ebd496cd81742ced628a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6CidrBlock"))

    @ipv6_cidr_block.setter
    def ipv6_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c470e9baca8a5daa8026a11e6219d88abfebe6b5e2e65dbd866669bff69f39c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6CidrBlock", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6Native")
    def ipv6_native(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv6Native"))

    @ipv6_native.setter
    def ipv6_native(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66a7fff8a995b58cf9f4cb694f10754b9ac35e8ad68c7d101ff6b624d6bde99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Native", value)

    @builtins.property
    @jsii.member(jsii_name="mapCustomerOwnedIpOnLaunch")
    def map_customer_owned_ip_on_launch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mapCustomerOwnedIpOnLaunch"))

    @map_customer_owned_ip_on_launch.setter
    def map_customer_owned_ip_on_launch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e38901ed01e2614ad4aec5423d11fd1a7f8cdee24736a06439907dd0d06e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapCustomerOwnedIpOnLaunch", value)

    @builtins.property
    @jsii.member(jsii_name="mapPublicIpOnLaunch")
    def map_public_ip_on_launch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mapPublicIpOnLaunch"))

    @map_public_ip_on_launch.setter
    def map_public_ip_on_launch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41783be58bcf2f081e10cc961efd6819724427c47cbcb50192b79d0bb41a9643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapPublicIpOnLaunch", value)

    @builtins.property
    @jsii.member(jsii_name="privateDnsHostnameTypeOnLaunch")
    def private_dns_hostname_type_on_launch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateDnsHostnameTypeOnLaunch"))

    @private_dns_hostname_type_on_launch.setter
    def private_dns_hostname_type_on_launch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7a2b52529a69f07b7199d174b03c2c6459effac3680582c5e2874c4a12d9d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateDnsHostnameTypeOnLaunch", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998873d98a66dc30064c93b6f9ad3e13cc441f164ff27061753b3e617be0c6d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2913e46be7f8a5623276db31b3aab39501be26f1089ee5c963c8471fac7898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.defaultSubnet.DefaultSubnetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone": "availabilityZone",
        "assign_ipv6_address_on_creation": "assignIpv6AddressOnCreation",
        "customer_owned_ipv4_pool": "customerOwnedIpv4Pool",
        "enable_dns64": "enableDns64",
        "enable_resource_name_dns_aaaa_record_on_launch": "enableResourceNameDnsAaaaRecordOnLaunch",
        "enable_resource_name_dns_a_record_on_launch": "enableResourceNameDnsARecordOnLaunch",
        "force_destroy": "forceDestroy",
        "id": "id",
        "ipv6_cidr_block": "ipv6CidrBlock",
        "ipv6_native": "ipv6Native",
        "map_customer_owned_ip_on_launch": "mapCustomerOwnedIpOnLaunch",
        "map_public_ip_on_launch": "mapPublicIpOnLaunch",
        "private_dns_hostname_type_on_launch": "privateDnsHostnameTypeOnLaunch",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class DefaultSubnetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        availability_zone: builtins.str,
        assign_ipv6_address_on_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
        enable_dns64: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_resource_name_dns_aaaa_record_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_resource_name_dns_a_record_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ipv6_cidr_block: typing.Optional[builtins.str] = None,
        ipv6_native: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_customer_owned_ip_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_public_ip_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_dns_hostname_type_on_launch: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DefaultSubnetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#availability_zone DefaultSubnet#availability_zone}.
        :param assign_ipv6_address_on_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#assign_ipv6_address_on_creation DefaultSubnet#assign_ipv6_address_on_creation}.
        :param customer_owned_ipv4_pool: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#customer_owned_ipv4_pool DefaultSubnet#customer_owned_ipv4_pool}.
        :param enable_dns64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_dns64 DefaultSubnet#enable_dns64}.
        :param enable_resource_name_dns_aaaa_record_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_resource_name_dns_aaaa_record_on_launch DefaultSubnet#enable_resource_name_dns_aaaa_record_on_launch}.
        :param enable_resource_name_dns_a_record_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_resource_name_dns_a_record_on_launch DefaultSubnet#enable_resource_name_dns_a_record_on_launch}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#force_destroy DefaultSubnet#force_destroy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#id DefaultSubnet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ipv6_cidr_block: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#ipv6_cidr_block DefaultSubnet#ipv6_cidr_block}.
        :param ipv6_native: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#ipv6_native DefaultSubnet#ipv6_native}.
        :param map_customer_owned_ip_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#map_customer_owned_ip_on_launch DefaultSubnet#map_customer_owned_ip_on_launch}.
        :param map_public_ip_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#map_public_ip_on_launch DefaultSubnet#map_public_ip_on_launch}.
        :param private_dns_hostname_type_on_launch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#private_dns_hostname_type_on_launch DefaultSubnet#private_dns_hostname_type_on_launch}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#tags DefaultSubnet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#tags_all DefaultSubnet#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#timeouts DefaultSubnet#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DefaultSubnetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0637ef6e77abfac31b28dfaad595e7f21b1f4cb48112fa320585950c960b9e4f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument assign_ipv6_address_on_creation", value=assign_ipv6_address_on_creation, expected_type=type_hints["assign_ipv6_address_on_creation"])
            check_type(argname="argument customer_owned_ipv4_pool", value=customer_owned_ipv4_pool, expected_type=type_hints["customer_owned_ipv4_pool"])
            check_type(argname="argument enable_dns64", value=enable_dns64, expected_type=type_hints["enable_dns64"])
            check_type(argname="argument enable_resource_name_dns_aaaa_record_on_launch", value=enable_resource_name_dns_aaaa_record_on_launch, expected_type=type_hints["enable_resource_name_dns_aaaa_record_on_launch"])
            check_type(argname="argument enable_resource_name_dns_a_record_on_launch", value=enable_resource_name_dns_a_record_on_launch, expected_type=type_hints["enable_resource_name_dns_a_record_on_launch"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ipv6_cidr_block", value=ipv6_cidr_block, expected_type=type_hints["ipv6_cidr_block"])
            check_type(argname="argument ipv6_native", value=ipv6_native, expected_type=type_hints["ipv6_native"])
            check_type(argname="argument map_customer_owned_ip_on_launch", value=map_customer_owned_ip_on_launch, expected_type=type_hints["map_customer_owned_ip_on_launch"])
            check_type(argname="argument map_public_ip_on_launch", value=map_public_ip_on_launch, expected_type=type_hints["map_public_ip_on_launch"])
            check_type(argname="argument private_dns_hostname_type_on_launch", value=private_dns_hostname_type_on_launch, expected_type=type_hints["private_dns_hostname_type_on_launch"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if assign_ipv6_address_on_creation is not None:
            self._values["assign_ipv6_address_on_creation"] = assign_ipv6_address_on_creation
        if customer_owned_ipv4_pool is not None:
            self._values["customer_owned_ipv4_pool"] = customer_owned_ipv4_pool
        if enable_dns64 is not None:
            self._values["enable_dns64"] = enable_dns64
        if enable_resource_name_dns_aaaa_record_on_launch is not None:
            self._values["enable_resource_name_dns_aaaa_record_on_launch"] = enable_resource_name_dns_aaaa_record_on_launch
        if enable_resource_name_dns_a_record_on_launch is not None:
            self._values["enable_resource_name_dns_a_record_on_launch"] = enable_resource_name_dns_a_record_on_launch
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if id is not None:
            self._values["id"] = id
        if ipv6_cidr_block is not None:
            self._values["ipv6_cidr_block"] = ipv6_cidr_block
        if ipv6_native is not None:
            self._values["ipv6_native"] = ipv6_native
        if map_customer_owned_ip_on_launch is not None:
            self._values["map_customer_owned_ip_on_launch"] = map_customer_owned_ip_on_launch
        if map_public_ip_on_launch is not None:
            self._values["map_public_ip_on_launch"] = map_public_ip_on_launch
        if private_dns_hostname_type_on_launch is not None:
            self._values["private_dns_hostname_type_on_launch"] = private_dns_hostname_type_on_launch
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def availability_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#availability_zone DefaultSubnet#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assign_ipv6_address_on_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#assign_ipv6_address_on_creation DefaultSubnet#assign_ipv6_address_on_creation}.'''
        result = self._values.get("assign_ipv6_address_on_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def customer_owned_ipv4_pool(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#customer_owned_ipv4_pool DefaultSubnet#customer_owned_ipv4_pool}.'''
        result = self._values.get("customer_owned_ipv4_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_dns64(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_dns64 DefaultSubnet#enable_dns64}.'''
        result = self._values.get("enable_dns64")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_resource_name_dns_aaaa_record_on_launch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_resource_name_dns_aaaa_record_on_launch DefaultSubnet#enable_resource_name_dns_aaaa_record_on_launch}.'''
        result = self._values.get("enable_resource_name_dns_aaaa_record_on_launch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_resource_name_dns_a_record_on_launch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#enable_resource_name_dns_a_record_on_launch DefaultSubnet#enable_resource_name_dns_a_record_on_launch}.'''
        result = self._values.get("enable_resource_name_dns_a_record_on_launch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#force_destroy DefaultSubnet#force_destroy}.'''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#id DefaultSubnet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#ipv6_cidr_block DefaultSubnet#ipv6_cidr_block}.'''
        result = self._values.get("ipv6_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_native(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#ipv6_native DefaultSubnet#ipv6_native}.'''
        result = self._values.get("ipv6_native")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def map_customer_owned_ip_on_launch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#map_customer_owned_ip_on_launch DefaultSubnet#map_customer_owned_ip_on_launch}.'''
        result = self._values.get("map_customer_owned_ip_on_launch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def map_public_ip_on_launch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#map_public_ip_on_launch DefaultSubnet#map_public_ip_on_launch}.'''
        result = self._values.get("map_public_ip_on_launch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_dns_hostname_type_on_launch(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#private_dns_hostname_type_on_launch DefaultSubnet#private_dns_hostname_type_on_launch}.'''
        result = self._values.get("private_dns_hostname_type_on_launch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#tags DefaultSubnet#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#tags_all DefaultSubnet#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DefaultSubnetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#timeouts DefaultSubnet#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DefaultSubnetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultSubnetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.defaultSubnet.DefaultSubnetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class DefaultSubnetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#create DefaultSubnet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#delete DefaultSubnet#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db410b51ba852bb8b3c9396e7e5ad92b231a03bf5cc8f0029d587411f988668f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#create DefaultSubnet#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/resources/default_subnet#delete DefaultSubnet#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultSubnetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DefaultSubnetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.defaultSubnet.DefaultSubnetTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5852d44830924cac03bd93b5280369a92ca5768e8847772685df13bec7e29bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9e1e77192afb57276329081bc9c0cfbe83a8771f91b4086cb9595392dd5fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1ab13c11c9c8c58c4bfe40d4bfb96ced5009e2f170a62e03380f45999890a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DefaultSubnetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DefaultSubnetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DefaultSubnetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072b13ac9f6be3e41edc27a79ab3bca25f75170d45b7b1e5730a11447dae6096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DefaultSubnet",
    "DefaultSubnetConfig",
    "DefaultSubnetTimeouts",
    "DefaultSubnetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__20aa5449ccb08912d8c1f3230e88bd0d5edc994a2dee3b2c611422c009d04acf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: builtins.str,
    assign_ipv6_address_on_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
    enable_dns64: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_resource_name_dns_aaaa_record_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_resource_name_dns_a_record_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ipv6_cidr_block: typing.Optional[builtins.str] = None,
    ipv6_native: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_customer_owned_ip_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_public_ip_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_dns_hostname_type_on_launch: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DefaultSubnetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6c6edede15b6997abbaa5144daf6f15bc852f724cc00254defa76a0125418b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c87160af03b807cf6c232d17a887b2e0312f316537c9d8742c549fa01a9ceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f63ae87f3a3869b9d64cfc72bb929e854b9599b956bd46bdacd50105de6cd39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97b110f5e102da89bf6cc70e5d0b18ddc2dcf49ae9913c3c270bd646e0b3eb2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9beb6cd8da55b7c84e3ca40981e8190b7fbf93b0830dec9ec5af570ae38290(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b715570b6be4392fa298c6f3dc8450226a55db21872af5e1af77d25d2df53091(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400ca82bba13bdde7e262aab79fdefbdf0ddc9d48cd866c76fc6d47f00feeba6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebed193e4de4e498d7dc4b94cf2051d310ebd3085df9ebd496cd81742ced628a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c470e9baca8a5daa8026a11e6219d88abfebe6b5e2e65dbd866669bff69f39c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66a7fff8a995b58cf9f4cb694f10754b9ac35e8ad68c7d101ff6b624d6bde99(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e38901ed01e2614ad4aec5423d11fd1a7f8cdee24736a06439907dd0d06e13(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41783be58bcf2f081e10cc961efd6819724427c47cbcb50192b79d0bb41a9643(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7a2b52529a69f07b7199d174b03c2c6459effac3680582c5e2874c4a12d9d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998873d98a66dc30064c93b6f9ad3e13cc441f164ff27061753b3e617be0c6d9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2913e46be7f8a5623276db31b3aab39501be26f1089ee5c963c8471fac7898(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0637ef6e77abfac31b28dfaad595e7f21b1f4cb48112fa320585950c960b9e4f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: builtins.str,
    assign_ipv6_address_on_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
    enable_dns64: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_resource_name_dns_aaaa_record_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_resource_name_dns_a_record_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ipv6_cidr_block: typing.Optional[builtins.str] = None,
    ipv6_native: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_customer_owned_ip_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_public_ip_on_launch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_dns_hostname_type_on_launch: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DefaultSubnetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db410b51ba852bb8b3c9396e7e5ad92b231a03bf5cc8f0029d587411f988668f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5852d44830924cac03bd93b5280369a92ca5768e8847772685df13bec7e29bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9e1e77192afb57276329081bc9c0cfbe83a8771f91b4086cb9595392dd5fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1ab13c11c9c8c58c4bfe40d4bfb96ced5009e2f170a62e03380f45999890a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072b13ac9f6be3e41edc27a79ab3bca25f75170d45b7b1e5730a11447dae6096(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DefaultSubnetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
