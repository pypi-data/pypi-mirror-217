'''
# `data_aws_ec2_instance_type`

Refer to the Terraform Registory for docs: [`data_aws_ec2_instance_type`](https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type).
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


class DataAwsEc2InstanceType(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceType",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type aws_ec2_instance_type}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAwsEc2InstanceTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type aws_ec2_instance_type} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#instance_type DataAwsEc2InstanceType#instance_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#id DataAwsEc2InstanceType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#timeouts DataAwsEc2InstanceType#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efc21c0297267382146cb750b3d5dd78d9997f274cb2153a720a1d3cd855f22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAwsEc2InstanceTypeConfig(
            instance_type=instance_type,
            id=id,
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
    def put_timeouts(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#read DataAwsEc2InstanceType#read}.
        '''
        value = DataAwsEc2InstanceTypeTimeouts(read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="autoRecoverySupported")
    def auto_recovery_supported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autoRecoverySupported"))

    @builtins.property
    @jsii.member(jsii_name="bareMetal")
    def bare_metal(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "bareMetal"))

    @builtins.property
    @jsii.member(jsii_name="burstablePerformanceSupported")
    def burstable_performance_supported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "burstablePerformanceSupported"))

    @builtins.property
    @jsii.member(jsii_name="currentGeneration")
    def current_generation(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "currentGeneration"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedHostsSupported")
    def dedicated_hosts_supported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "dedicatedHostsSupported"))

    @builtins.property
    @jsii.member(jsii_name="defaultCores")
    def default_cores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultCores"))

    @builtins.property
    @jsii.member(jsii_name="defaultThreadsPerCore")
    def default_threads_per_core(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultThreadsPerCore"))

    @builtins.property
    @jsii.member(jsii_name="defaultVcpus")
    def default_vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultVcpus"))

    @builtins.property
    @jsii.member(jsii_name="ebsEncryptionSupport")
    def ebs_encryption_support(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebsEncryptionSupport"))

    @builtins.property
    @jsii.member(jsii_name="ebsNvmeSupport")
    def ebs_nvme_support(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebsNvmeSupport"))

    @builtins.property
    @jsii.member(jsii_name="ebsOptimizedSupport")
    def ebs_optimized_support(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebsOptimizedSupport"))

    @builtins.property
    @jsii.member(jsii_name="ebsPerformanceBaselineBandwidth")
    def ebs_performance_baseline_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsPerformanceBaselineBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="ebsPerformanceBaselineIops")
    def ebs_performance_baseline_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsPerformanceBaselineIops"))

    @builtins.property
    @jsii.member(jsii_name="ebsPerformanceBaselineThroughput")
    def ebs_performance_baseline_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsPerformanceBaselineThroughput"))

    @builtins.property
    @jsii.member(jsii_name="ebsPerformanceMaximumBandwidth")
    def ebs_performance_maximum_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsPerformanceMaximumBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="ebsPerformanceMaximumIops")
    def ebs_performance_maximum_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsPerformanceMaximumIops"))

    @builtins.property
    @jsii.member(jsii_name="ebsPerformanceMaximumThroughput")
    def ebs_performance_maximum_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsPerformanceMaximumThroughput"))

    @builtins.property
    @jsii.member(jsii_name="efaSupported")
    def efa_supported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "efaSupported"))

    @builtins.property
    @jsii.member(jsii_name="enaSupport")
    def ena_support(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enaSupport"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInTransitSupported")
    def encryption_in_transit_supported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "encryptionInTransitSupported"))

    @builtins.property
    @jsii.member(jsii_name="fpgas")
    def fpgas(self) -> "DataAwsEc2InstanceTypeFpgasList":
        return typing.cast("DataAwsEc2InstanceTypeFpgasList", jsii.get(self, "fpgas"))

    @builtins.property
    @jsii.member(jsii_name="freeTierEligible")
    def free_tier_eligible(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "freeTierEligible"))

    @builtins.property
    @jsii.member(jsii_name="gpus")
    def gpus(self) -> "DataAwsEc2InstanceTypeGpusList":
        return typing.cast("DataAwsEc2InstanceTypeGpusList", jsii.get(self, "gpus"))

    @builtins.property
    @jsii.member(jsii_name="hibernationSupported")
    def hibernation_supported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hibernationSupported"))

    @builtins.property
    @jsii.member(jsii_name="hypervisor")
    def hypervisor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hypervisor"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAccelerators")
    def inference_accelerators(
        self,
    ) -> "DataAwsEc2InstanceTypeInferenceAcceleratorsList":
        return typing.cast("DataAwsEc2InstanceTypeInferenceAcceleratorsList", jsii.get(self, "inferenceAccelerators"))

    @builtins.property
    @jsii.member(jsii_name="instanceDisks")
    def instance_disks(self) -> "DataAwsEc2InstanceTypeInstanceDisksList":
        return typing.cast("DataAwsEc2InstanceTypeInstanceDisksList", jsii.get(self, "instanceDisks"))

    @builtins.property
    @jsii.member(jsii_name="instanceStorageSupported")
    def instance_storage_supported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "instanceStorageSupported"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Supported")
    def ipv6_supported(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "ipv6Supported"))

    @builtins.property
    @jsii.member(jsii_name="maximumIpv4AddressesPerInterface")
    def maximum_ipv4_addresses_per_interface(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumIpv4AddressesPerInterface"))

    @builtins.property
    @jsii.member(jsii_name="maximumIpv6AddressesPerInterface")
    def maximum_ipv6_addresses_per_interface(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumIpv6AddressesPerInterface"))

    @builtins.property
    @jsii.member(jsii_name="maximumNetworkInterfaces")
    def maximum_network_interfaces(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumNetworkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySize"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformance")
    def network_performance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPerformance"))

    @builtins.property
    @jsii.member(jsii_name="supportedArchitectures")
    def supported_architectures(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedArchitectures"))

    @builtins.property
    @jsii.member(jsii_name="supportedPlacementStrategies")
    def supported_placement_strategies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedPlacementStrategies"))

    @builtins.property
    @jsii.member(jsii_name="supportedRootDeviceTypes")
    def supported_root_device_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedRootDeviceTypes"))

    @builtins.property
    @jsii.member(jsii_name="supportedUsagesClasses")
    def supported_usages_classes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedUsagesClasses"))

    @builtins.property
    @jsii.member(jsii_name="supportedVirtualizationTypes")
    def supported_virtualization_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedVirtualizationTypes"))

    @builtins.property
    @jsii.member(jsii_name="sustainedClockSpeed")
    def sustained_clock_speed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sustainedClockSpeed"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataAwsEc2InstanceTypeTimeoutsOutputReference":
        return typing.cast("DataAwsEc2InstanceTypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="totalFpgaMemory")
    def total_fpga_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalFpgaMemory"))

    @builtins.property
    @jsii.member(jsii_name="totalGpuMemory")
    def total_gpu_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalGpuMemory"))

    @builtins.property
    @jsii.member(jsii_name="totalInstanceStorage")
    def total_instance_storage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalInstanceStorage"))

    @builtins.property
    @jsii.member(jsii_name="validCores")
    def valid_cores(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "validCores"))

    @builtins.property
    @jsii.member(jsii_name="validThreadsPerCore")
    def valid_threads_per_core(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "validThreadsPerCore"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataAwsEc2InstanceTypeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataAwsEc2InstanceTypeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d5a8fdc0d69a238b4e132109e51622e17de450d2ff09b203055ca21ea186d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859f4c9b49729e25eb4529929f2266820ba8fe76cb6487082ce3c5b0ddae1299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_type": "instanceType",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DataAwsEc2InstanceTypeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAwsEc2InstanceTypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#instance_type DataAwsEc2InstanceType#instance_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#id DataAwsEc2InstanceType#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#timeouts DataAwsEc2InstanceType#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataAwsEc2InstanceTypeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982c0072b558e485271638b25292444547da17368b337b66fe98ba3afa0b1f79)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
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
        if id is not None:
            self._values["id"] = id
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
    def instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#instance_type DataAwsEc2InstanceType#instance_type}.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#id DataAwsEc2InstanceType#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataAwsEc2InstanceTypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#timeouts DataAwsEc2InstanceType#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataAwsEc2InstanceTypeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsEc2InstanceTypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeFpgas",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAwsEc2InstanceTypeFpgas:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsEc2InstanceTypeFpgas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsEc2InstanceTypeFpgasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeFpgasList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8bdf149d73c015ae862bc17bb11c41a727b1ac698c1af13add97e842cc3374)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataAwsEc2InstanceTypeFpgasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57cc4325ca184f7eaeb7bb6a9dc60f76628e4d4a7aa8a05e2ed200ab6956002)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsEc2InstanceTypeFpgasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c06a7463dd4cdef11b88078d21fd4b5dfa846b89f6342f0b6e773f574875db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3feedee9dd1673e09b1a33b8a08deb5cef2e224ef213f1ea9cf9c2fbab42aff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7625d91243992a3307d99c21dd03f9ac4bdc5cb0d4928d4cb5e93ac382c1bd7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAwsEc2InstanceTypeFpgasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeFpgasOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ac70175701b0ff31347bc819a02dc0b1c211510b5c36ff6bbfbf0be484399e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="manufacturer")
    def manufacturer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manufacturer"))

    @builtins.property
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySize"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataAwsEc2InstanceTypeFpgas]:
        return typing.cast(typing.Optional[DataAwsEc2InstanceTypeFpgas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsEc2InstanceTypeFpgas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a224751b03caabfe66f2b07e18ee96301e8bd1d4afb5b090941bb80b4bf1a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeGpus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAwsEc2InstanceTypeGpus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsEc2InstanceTypeGpus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsEc2InstanceTypeGpusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeGpusList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36af18f5d5fa2e09b53b51be1faffdb43de0633baba2034aa9cd9447da54ff6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataAwsEc2InstanceTypeGpusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f738c01dfc16f3ebbe944c96964d61ba5c3755e5cee3da56ce6fae271c9d71)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsEc2InstanceTypeGpusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232f09d4ccf91e958b4e94194a8a94d3a82ad4b506413fba7431f77db482d1f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f7e3405d1b3fb072781b2014f649d46f6a9ab2e4fda59c5282a02adddf171f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426b8f787a05855277a37d185289db8e7bcf8b9aa42dee48a8fe612117f51678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAwsEc2InstanceTypeGpusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeGpusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68631f39abf7bae1146da86748485ff539e436f1dcd2f1ca6478ebe7359e2533)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="manufacturer")
    def manufacturer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manufacturer"))

    @builtins.property
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySize"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataAwsEc2InstanceTypeGpus]:
        return typing.cast(typing.Optional[DataAwsEc2InstanceTypeGpus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsEc2InstanceTypeGpus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63025fd903738ae957aaa44d94c272875690591520bf69d1629c790b7f29ff71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeInferenceAccelerators",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAwsEc2InstanceTypeInferenceAccelerators:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsEc2InstanceTypeInferenceAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsEc2InstanceTypeInferenceAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeInferenceAcceleratorsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd68deff9fcfb7271ce7bdbf506743db1365b4e7a4ea09b7ddac5fdf6d4bd49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsEc2InstanceTypeInferenceAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae2de7d82422a6f651ad4ef472866089ce10a995d58a768b8798526d3a63f83)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsEc2InstanceTypeInferenceAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1236e27ce7b7c4526fa23a63b69623de2bb0edfa75f56b641dee0ebd02b3d670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5da524dbbb1c7a3158d30d15ded2a05e6effbe5015a34bb6df8cdc94492b18b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cbb3f287f42f71e0085190a0a16cb250ebffbb3c2e25e8b17a3350d4ed6bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAwsEc2InstanceTypeInferenceAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeInferenceAcceleratorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d026d26cf0a85d2186089f7001bcdcf98007a5ba0818d224ae3a9b80f72c9dbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="manufacturer")
    def manufacturer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manufacturer"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAwsEc2InstanceTypeInferenceAccelerators]:
        return typing.cast(typing.Optional[DataAwsEc2InstanceTypeInferenceAccelerators], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsEc2InstanceTypeInferenceAccelerators],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91aafe4885bb0d57d91bce39849a5696bfadc182a035dacacb5ffa9d5833b094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeInstanceDisks",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAwsEc2InstanceTypeInstanceDisks:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsEc2InstanceTypeInstanceDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsEc2InstanceTypeInstanceDisksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeInstanceDisksList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21da3d8d35fc969b36e0f977dd49d7fa45b86c33d18feb8cefe200a66e85f98e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsEc2InstanceTypeInstanceDisksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed949dcbeee0ba4acd9ef778c060653da11492a19e6b14d012f0862e49861b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsEc2InstanceTypeInstanceDisksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3095d7e915442111b766b83e5cee2725807581f3bacbd3b24b87754f5cd229ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a83a2f04d31195bddcf1c989c8e34f3b9a321010aaadcbbb64ecbf136dcebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329f795c917d084a41640918840a29d154fda67c854d0c65b2e0d04f7d1f4073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAwsEc2InstanceTypeInstanceDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeInstanceDisksOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b139a87f68a9af003c3971add066ae0467c5130264e9c997500f8c558970c21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataAwsEc2InstanceTypeInstanceDisks]:
        return typing.cast(typing.Optional[DataAwsEc2InstanceTypeInstanceDisks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsEc2InstanceTypeInstanceDisks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afd436900348608de344d1a092434aa87a2484f339d5877eaa70ebc03ee407d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"read": "read"},
)
class DataAwsEc2InstanceTypeTimeouts:
    def __init__(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#read DataAwsEc2InstanceType#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9cad653cb260cbfa995796aee55005c1f30faf87c98144a58c738c46a6b02a)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.6.2/docs/data-sources/ec2_instance_type#read DataAwsEc2InstanceType#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsEc2InstanceTypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsEc2InstanceTypeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsEc2InstanceType.DataAwsEc2InstanceTypeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8914744d2aee8c9819ba489db08f8d9c051b7a3f3eba888d974d4ae4da73105)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96da75a7d0b13ee073e770b12b0bb97f7f0aafbaab2259098210e33e0840cec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAwsEc2InstanceTypeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAwsEc2InstanceTypeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAwsEc2InstanceTypeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3ef444f4dbcadd025d217bb4ba01f90deb4ea3260dbd3b96319f8695293a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataAwsEc2InstanceType",
    "DataAwsEc2InstanceTypeConfig",
    "DataAwsEc2InstanceTypeFpgas",
    "DataAwsEc2InstanceTypeFpgasList",
    "DataAwsEc2InstanceTypeFpgasOutputReference",
    "DataAwsEc2InstanceTypeGpus",
    "DataAwsEc2InstanceTypeGpusList",
    "DataAwsEc2InstanceTypeGpusOutputReference",
    "DataAwsEc2InstanceTypeInferenceAccelerators",
    "DataAwsEc2InstanceTypeInferenceAcceleratorsList",
    "DataAwsEc2InstanceTypeInferenceAcceleratorsOutputReference",
    "DataAwsEc2InstanceTypeInstanceDisks",
    "DataAwsEc2InstanceTypeInstanceDisksList",
    "DataAwsEc2InstanceTypeInstanceDisksOutputReference",
    "DataAwsEc2InstanceTypeTimeouts",
    "DataAwsEc2InstanceTypeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8efc21c0297267382146cb750b3d5dd78d9997f274cb2153a720a1d3cd855f22(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAwsEc2InstanceTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__64d5a8fdc0d69a238b4e132109e51622e17de450d2ff09b203055ca21ea186d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859f4c9b49729e25eb4529929f2266820ba8fe76cb6487082ce3c5b0ddae1299(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982c0072b558e485271638b25292444547da17368b337b66fe98ba3afa0b1f79(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAwsEc2InstanceTypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8bdf149d73c015ae862bc17bb11c41a727b1ac698c1af13add97e842cc3374(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57cc4325ca184f7eaeb7bb6a9dc60f76628e4d4a7aa8a05e2ed200ab6956002(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c06a7463dd4cdef11b88078d21fd4b5dfa846b89f6342f0b6e773f574875db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3feedee9dd1673e09b1a33b8a08deb5cef2e224ef213f1ea9cf9c2fbab42aff8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7625d91243992a3307d99c21dd03f9ac4bdc5cb0d4928d4cb5e93ac382c1bd7c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ac70175701b0ff31347bc819a02dc0b1c211510b5c36ff6bbfbf0be484399e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a224751b03caabfe66f2b07e18ee96301e8bd1d4afb5b090941bb80b4bf1a1(
    value: typing.Optional[DataAwsEc2InstanceTypeFpgas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36af18f5d5fa2e09b53b51be1faffdb43de0633baba2034aa9cd9447da54ff6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f738c01dfc16f3ebbe944c96964d61ba5c3755e5cee3da56ce6fae271c9d71(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232f09d4ccf91e958b4e94194a8a94d3a82ad4b506413fba7431f77db482d1f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f7e3405d1b3fb072781b2014f649d46f6a9ab2e4fda59c5282a02adddf171f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426b8f787a05855277a37d185289db8e7bcf8b9aa42dee48a8fe612117f51678(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68631f39abf7bae1146da86748485ff539e436f1dcd2f1ca6478ebe7359e2533(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63025fd903738ae957aaa44d94c272875690591520bf69d1629c790b7f29ff71(
    value: typing.Optional[DataAwsEc2InstanceTypeGpus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd68deff9fcfb7271ce7bdbf506743db1365b4e7a4ea09b7ddac5fdf6d4bd49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae2de7d82422a6f651ad4ef472866089ce10a995d58a768b8798526d3a63f83(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1236e27ce7b7c4526fa23a63b69623de2bb0edfa75f56b641dee0ebd02b3d670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5da524dbbb1c7a3158d30d15ded2a05e6effbe5015a34bb6df8cdc94492b18b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cbb3f287f42f71e0085190a0a16cb250ebffbb3c2e25e8b17a3350d4ed6bb0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d026d26cf0a85d2186089f7001bcdcf98007a5ba0818d224ae3a9b80f72c9dbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91aafe4885bb0d57d91bce39849a5696bfadc182a035dacacb5ffa9d5833b094(
    value: typing.Optional[DataAwsEc2InstanceTypeInferenceAccelerators],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21da3d8d35fc969b36e0f977dd49d7fa45b86c33d18feb8cefe200a66e85f98e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed949dcbeee0ba4acd9ef778c060653da11492a19e6b14d012f0862e49861b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3095d7e915442111b766b83e5cee2725807581f3bacbd3b24b87754f5cd229ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a83a2f04d31195bddcf1c989c8e34f3b9a321010aaadcbbb64ecbf136dcebf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329f795c917d084a41640918840a29d154fda67c854d0c65b2e0d04f7d1f4073(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b139a87f68a9af003c3971add066ae0467c5130264e9c997500f8c558970c21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afd436900348608de344d1a092434aa87a2484f339d5877eaa70ebc03ee407d(
    value: typing.Optional[DataAwsEc2InstanceTypeInstanceDisks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9cad653cb260cbfa995796aee55005c1f30faf87c98144a58c738c46a6b02a(
    *,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8914744d2aee8c9819ba489db08f8d9c051b7a3f3eba888d974d4ae4da73105(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96da75a7d0b13ee073e770b12b0bb97f7f0aafbaab2259098210e33e0840cec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3ef444f4dbcadd025d217bb4ba01f90deb4ea3260dbd3b96319f8695293a29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAwsEc2InstanceTypeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
