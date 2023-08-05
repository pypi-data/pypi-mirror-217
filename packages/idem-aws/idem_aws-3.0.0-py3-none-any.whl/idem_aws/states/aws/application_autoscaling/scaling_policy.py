"""State module for managing Amazon Application Autoscaling scaling policies."""
import copy
import re
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

TREQ = {
    "present": {
        "require": [
            "aws.application_autoscaling.scaling_target.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    policy_name: str,
    service_namespace: str,
    scaling_resource_id: str,
    scalable_dimension: str,
    policy_type: str,
    resource_id: str = None,
    step_scaling_policy_configuration: make_dataclass(
        "StepScalingPolicyConfiguration",
        [
            ("AdjustmentType", str, field(default=None)),
            (
                "StepAdjustments",
                List[
                    make_dataclass(
                        "StepAdjustment",
                        [
                            ("MetricIntervalLowerBound", float, field(default=None)),
                            ("MetricIntervalUpperBound", float, field(default=None)),
                            ("ScalingAdjustment", int, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("MinAdjustmentMagnitude", int, field(default=None)),
            ("Cooldown", int, field(default=None)),
            ("MetricAggregationType", str, field(default=None)),
        ],
    ) = None,
    target_tracking_scaling_policy_configuration: make_dataclass(
        "TargetTrackingScalingPolicyConfiguration",
        [
            ("TargetValue", float),
            (
                "PredefinedMetricSpecification",
                make_dataclass(
                    "PredefinedMetricSpecification",
                    [
                        ("PredefinedMetricType", str),
                        ("ResourceLabel", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "CustomizedMetricSpecification",
                make_dataclass(
                    "CustomizedMetricSpecification",
                    [
                        ("MetricName", str),
                        ("Namespace", str),
                        ("Statistic", str),
                        (
                            "Dimensions",
                            List[
                                make_dataclass(
                                    "MetricDimension", [("Name", str), ("Value", str)]
                                )
                            ],
                            field(default=None),
                        ),
                        ("Unit", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("ScaleOutCooldown", int, field(default=None)),
            ("ScaleInCooldown", int, field(default=None)),
            ("DisableScaleIn", bool, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates or updates a scaling policy for an Application Auto Scaling scalable target.

    Each scalable target is identified by a service namespace, resource ID, and scalable dimension.
    A scaling policy applies to the scalable target identified by those three attributes.
    You cannot create a scaling policy until you have registered the resource as a scalable target.

    Multiple scaling policies can be in force at the same time for the same scalable
    target. You can have one or more target tracking scaling policies, one or more step scaling policies, or both.
    However, there is a chance that multiple policies could conflict, instructing the scalable target to scale out
    or in at the same time. Application Auto Scaling gives precedence to the policy that provides the largest
    capacity for both scale out and scale in. For example, if one policy increases capacity by 3, another policy
    increases capacity by 200 percent, and the current capacity is 10, Application Auto Scaling uses the policy with
    the highest calculated capacity (200% of 10 = 20) and scales out to 30.

    We recommend caution, however, when using target tracking scaling policies with step scaling policies because
    conflicts between these policies can cause undesirable behavior.
    For example, if the step scaling policy initiates a scale-in activity before the
    target tracking policy is ready to scale in, the scale-in activity will not be blocked. After the scale-in
    activity completes, the target tracking policy could instruct the scalable target to scale out again.

    For more information, see Target tracking scaling policies and Step scaling policies in
    the Application Auto Scaling User Guide.

    .. Note::
        If a scalable target is deregistered, the scalable target is no longer available to execute scaling
        policies. Any scaling policies that were specified for the scalable target are deleted.

    Args:
        name(str):
            An Idem name of the resource.

        policy_name(str):
            The name of the scaling policy.

        service_namespace(str):
            The namespace of the Amazon Web Services service that provides the resource.
            For a resource provided by your own application or service, use custom-resource instead.

        scaling_resource_id(str): The identifier of the resource associated with the scaling policy.
            This string consists of the resource type and unique identifier.

            * ECS service - The resource type is service and the unique identifier is the cluster name and service name.
              Example: service/default/sample-webapp.
            * Spot Fleet - The resource type is spot-fleet-request and the unique identifier is the Spot Fleet request
              ID. Example: spot-fleet-request/sfr-73fbd2ce-aa30-494c-8788-1cee4EXAMPLE.
            * EMR cluster - The resource type is instancegroup and the unique identifier is the cluster ID and instance
              group ID. Example: instancegroup/j-2EEZNYKUA1NTV/ig-1791Y4E1L8YI0.
            * AppStream 2.0 fleet - The resource type is fleet and the unique identifier is the fleet name.
              Example: fleet/sample-fleet.
            * DynamoDB table - The resource type is table and the unique identifier is the table name.
              Example: table/my-table.
            * DynamoDB global secondary index - The resource type is index and the unique identifier is the index name.
              Example: table/my-table/index/my-table-index.
            * Aurora DB cluster - The resource type is cluster and the unique identifier is the cluster name.
              Example:cluster:my-db-cluster.
            * SageMaker endpoint variant - The resource type is variant and the unique identifier is the resource ID.
              Example: endpoint/my-end-point/variant/KMeansClustering.
            * Custom resources are not supported with a resource type. This parameter must specify the OutputValue
              from the CloudFormation template stack used to access the resources. The unique
              identifier is defined by the service provider. More information is available in our GitHub repository.
            * Amazon Comprehend document classification endpoint - The resource type and unique identifier are specified
              using the endpoint ARN.
              Example: arn:aws:comprehend:us-west-2:123456789012:document-classifier-endpoint/EXAMPLE.
            * Amazon Comprehend entity recognizer endpoint - The resource type and unique identifier are specified using
              the endpoint ARN. Example: arn:aws:comprehend:us-west-2:123456789012:entity-recognizer-endpoint/EXAMPLE.
            * Lambda provisioned concurrency - The resource type is function and the unique identifier is the function
              name with a function version or alias name suffix that is not $LATEST.
              Example: function:my-function:prod or function:my-function:1.
            * Amazon Keyspaces table - The resource type is table and the unique identifier is the table name.
              Example: keyspace/mykeyspace/table/mytable.
            * Amazon MSK cluster - The resource type and unique identifier are specified using the cluster ARN. Example:
              arn:aws:kafka:us-east-1:123456789012:cluster/demo-cluster-1/6357e0b2-0e6a-4b86-a0b4-70df934c2e31-5.
            * Amazon ElastiCache replication group - The resource type is replication-group and the unique identifier
              is the replication group name. Example: replication-group/mycluster.
            * Neptune cluster - The resource type is cluster and the unique identifier is the cluster name.
              Example: cluster:mycluster.

        scalable_dimension(str):
            The scalable dimension. This string consists of the service namespace, resource type, and scaling property.

            * ecs:service:DesiredCount - The desired task count of an ECS service.
            * elasticmapreduce:instancegroup:InstanceCount - The instance count of an EMR Instance Group.
            * ec2:spot-fleet-request:TargetCapacity - The target capacity of a Spot Fleet.
            * appstream:fleet:DesiredCapacity - The desired capacity of an AppStream 2.0 fleet.
            * dynamodb:table:ReadCapacityUnits - The provisioned read capacity for a DynamoDB table.
            * dynamodb:table:WriteCapacityUnits - The provisioned write capacity for a DynamoDB table.
            * dynamodb:index:ReadCapacityUnits - The provisioned read capacity for a DynamoDB global secondary index.
            * dynamodb:index:WriteCapacityUnits - The provisioned write capacity for a DynamoDB global secondary index.
            * rds:cluster:ReadReplicaCount - The count of Aurora Replicas in an Aurora DB cluster.
              Available for Aurora MySQL-compatible edition and Aurora PostgreSQL- compatible edition.
            * sagemaker:variant:DesiredInstanceCount -
              The number of EC2 instances for an SageMaker model endpoint variant.
            * custom-resource:ResourceType:Property -
              The scalable dimension for a custom resource provided by your own application or service.
            * comprehend:document-classifier-endpoint:DesiredInferenceUnits -
              The number of inference units for an Amazon Comprehend document classification endpoint.
            * comprehend:entity-recognizer-endpoint:DesiredInferenceUnits -
              The number of inference units for an Amazon Comprehend entity recognizer endpoint.
            * lambda:function:ProvisionedConcurrency - The provisioned concurrency for a Lambda function.
            * cassandra:table:ReadCapacityUnits - The provisioned read capacity for an Amazon Keyspaces table.
            * cassandra:table:WriteCapacityUnits - The provisioned write capacity for an Amazon Keyspaces table.
            * kafka:broker-storage:VolumeSize -
              The provisioned volume size (in GiB) for brokers in an Amazon MSK cluster.
            * elasticache:replication-group:NodeGroups -
              The number of node groups for an Amazon ElastiCache replication group.
            * elasticache:replication-group:Replicas -
              The number of replicas per node group for an Amazon ElastiCache replication group.
            * neptune:cluster:ReadReplicaCount -
              The count of read replicas in an Amazon Neptune DB cluster.

        policy_type(str):
            The policy type. This parameter is required if you are creating a scaling policy.

            The following policy types are supported:

            * TargetTrackingScaling — Not supported for Amazon EMR
            * StepScaling — Not supported for DynamoDB, Amazon Comprehend, Lambda, Amazon Keyspaces, Amazon MSK,
              Amazon ElastiCache, or Neptune.

            For more information, see Target tracking scaling policies and Step scaling policies in
            the Application Auto Scaling User Guide. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        step_scaling_policy_configuration(dict[str, Any], Optional):
            A step scaling policy.
            This parameter is required if you are creating a policy and the policy type is StepScaling.
            Defaults to None.

            * AdjustmentType (str, Optional):
                Specifies how the ScalingAdjustment value in a StepAdjustment is interpreted (for example, an
                absolute number or a percentage). The valid values are ChangeInCapacity, ExactCapacity, and
                PercentChangeInCapacity.
                AdjustmentType is required if you are adding a new step scaling policy configuration.
            * StepAdjustments (list[dict[str, Any]], Optional):
                A set of adjustments that enable you to scale based on the size of the alarm breach. At least
                one step adjustment is required if you are adding a new step scaling policy configuration.

                * MetricIntervalLowerBound (float, Optional):
                    The lower bound for the difference between the alarm threshold and the CloudWatch metric. If the
                    metric value is above the breach threshold, the lower bound is inclusive (the metric must be
                    greater than or equal to the threshold plus the lower bound). Otherwise, it is exclusive (the
                    metric must be greater than the threshold plus the lower bound). A null value indicates negative
                    infinity.
                * MetricIntervalUpperBound (float, Optional):
                    The upper bound for the difference between the alarm threshold and the CloudWatch metric. If the
                    metric value is above the breach threshold, the upper bound is exclusive (the metric must be
                    less than the threshold plus the upper bound). Otherwise, it is inclusive (the metric must be
                    less than or equal to the threshold plus the upper bound). A null value indicates positive
                    infinity. The upper bound must be greater than the lower bound.
                * ScalingAdjustment (int):
                    The amount by which to scale, based on the specified adjustment type. A positive value adds to
                    the current capacity while a negative number removes from the current capacity. For exact capacity,
                    you must specify a positive value.

            * MinAdjustmentMagnitude (int, Optional):
                The minimum value to scale by when the adjustment type is PercentChangeInCapacity. For example,
                suppose that you create a step scaling policy to scale out an Amazon ECS service by 25 percent
                and you specify a MinAdjustmentMagnitude of 2. If the service has 4 tasks and the scaling policy
                is performed, 25 percent of 4 is 1. However, because you specified a MinAdjustmentMagnitude of
                2, Application Auto Scaling scales out the service by 2 tasks.

            * Cooldown (int, Optional):
                The amount of time, in seconds, to wait for a previous scaling activity to take effect.  With
                scale-out policies, the intention is to continuously (but not excessively) scale out. After
                Application Auto Scaling successfully scales out using a step scaling policy, it starts to
                calculate the cooldown time. The scaling policy won't increase the desired capacity again unless
                either a larger scale out is triggered or the cooldown period ends. While the cooldown period is
                in effect, capacity added by the initiating scale-out activity is calculated as part of the
                desired capacity for the next scale-out activity. For example, when an alarm triggers a step
                scaling policy to increase the capacity by 2, the scaling activity completes successfully, and a
                cooldown period starts. If the alarm triggers again during the cooldown period but at a more
                aggressive step adjustment of 3, the previous increase of 2 is considered part of the current
                capacity. Therefore, only 1 is added to the capacity. With scale-in policies, the intention is
                to scale in conservatively to protect your application’s availability, so scale-in activities
                are blocked until the cooldown period has expired. However, if another alarm triggers a scale-
                out activity during the cooldown period after a scale-in activity, Application Auto Scaling
                scales out the target immediately. In this case, the cooldown period for the scale-in activity
                stops and doesn't complete.

                Application Auto Scaling provides a default value of 600 for Amazon ElastiCache replication groups and a default value of 300 for the following scalable targets:
                 * AppStream 2.0 fleets
                 * Aurora DB clusters
                 * ECS services
                 * EMR clusters
                 * Neptune clusters
                 * SageMaker endpoint variants
                 * Spot Fleets
                 * Custom resources

                For all other scalable targets, the default value is 0:
                 * Amazon Comprehend document classification and entity recognizer endpoints
                 * DynamoDB tables and global secondary indexes
                 * Amazon Keyspaces tables
                 * Lambda provisioned concurrency
                 * Amazon MSK broker storage

            * MetricAggregationType (str, Optional):
                The aggregation type for the CloudWatch metrics. Valid values are Minimum, Maximum, and Average.
                If the aggregation type is null, the value is treated as Average.

        target_tracking_scaling_policy_configuration(dict[str, Any], Optional):
            A target tracking scaling policy. Includes support for predefined or customized metrics.
            This parameter is required if you are creating a policy and the policy type is TargetTrackingScaling.
            Defaults to None.

            * TargetValue (float):
                The target value for the metric. Although this property accepts numbers of type Double, it won't
                accept values that are either too small or too large. Values must be in the range of -2^360 to
                2^360. The value must be a valid number based on the choice of metric. For example, if the
                metric is CPU utilization, then the target value is a percent value that represents how much of
                the CPU can be used before scaling out.
            * PredefinedMetricSpecification (dict[str, Any], Optional):
                A predefined metric. You can specify either a predefined metric or a customized metric.

                * PredefinedMetricType (str):
                    The metric type. The ALBRequestCountPerTarget metric type applies only to Spot Fleet requests and
                    ECS services.
                * ResourceLabel (str, Optional):
                    Identifies the resource associated with the metric type. You can't specify a resource label
                    unless the metric type is ALBRequestCountPerTarget and there is a target group attached to the
                    Spot Fleet request or ECS service.

                    You create the resource label by appending the final portion
                    of the load balancer ARN and the final portion of the target group ARN into a single value,
                    separated by a forward slash (/).

                    The format of the resource label is:
                    app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff.

                    Where:

                    * app/<load-balancer-name>/<load-balancer-id> is the final portion of the load balancer ARN
                    * targetgroup/<target-group-name>/<target-group-id> is the final portion of the target group ARN.

                    To find the ARN for an Application Load Balancer, use the DescribeLoadBalancers API operation.
                    To find the ARN for the target group, use the DescribeTargetGroups API operation.

            * CustomizedMetricSpecification (dict[str, Any], Optional):
                A customized metric. You can specify either a predefined metric or a customized metric.

                * MetricName (str): The name of the metric.
                * Namespace (str): The namespace of the metric.
                * Dimensions (List[Dict[str, Any]], Optional): The dimensions of the metric.

                  Conditional: If you published your metric with dimensions, you must specify the same dimensions in
                  your scaling policy.

                  * Name (str): The name of the dimension.
                  * Value (str): The value of the dimension.

                * Statistic (str): The statistic of the metric.
                * Unit (str, Optional): The unit of the metric.

            * ScaleOutCooldown (int, Optional):
                The amount of time, in seconds, to wait for a previous scale-out activity to take effect.

                With the scale-out cooldown period, the intention is to continuously (but not excessively) scale out.
                After Application Auto Scaling successfully scales out using a target tracking scaling policy,
                it starts to calculate the cooldown time. The scaling policy won't increase the desired capacity
                again unless either a larger scale out is triggered or the cooldown period ends. While the
                cooldown period is in effect, the capacity added by the initiating scale-out activity is
                calculated as part of the desired capacity for the next scale-out activity.

                Application Auto Scaling provides a default value of 600 for Amazon ElastiCache replication groups and a default value of 300 for the following scalable targets:
                 * AppStream 2.0 fleets
                 * Aurora DB clusters
                 * ECS services
                 * EMR clusters
                 * Neptune clusters
                 * SageMaker endpoint variants
                 * Spot Fleets
                 * Custom resources

                For all other scalable targets, the default value is 0:
                 * Amazon Comprehend document classification and entity recognizer endpoints
                 * DynamoDB tables and global secondary indexes
                 * Amazon Keyspaces tables
                 * Lambda provisioned concurrency
                 * Amazon MSK broker storage

            * ScaleInCooldown (int, Optional):
                The amount of time, in seconds, after a scale-in activity completes before another scale-in
                activity can start.

                With the scale-in cooldown period, the intention is to scale in conservatively to protect your
                application’s availability, so scale-in activities are blocked
                until the cooldown period has expired. However, if another alarm triggers a scale-out activity
                during the scale-in cooldown period, Application Auto Scaling scales out the target immediately.
                In this case, the scale-in cooldown period stops and doesn't complete.

                Application Auto Scaling provides a default value of 600 for Amazon ElastiCache replication groups  and a default value of 300 for the following scalable targets:
                 * AppStream 2.0 fleets
                 * Aurora DB clusters
                 * ECS services
                 * EMR clusters
                 * Neptune clusters
                 * SageMaker endpoint variants
                 * Spot Fleets
                 * Custom resources

                For all other scalable targets, the default value is 0:
                 * Amazon Comprehend document classification and entity recognizer endpoints
                 * DynamoDB tables and global secondary indexes
                 * Amazon Keyspaces tables
                 * Lambda provisioned concurrency
                 * Amazon MSK broker storage

            * DisableScaleIn (bool, Optional):
                Indicates whether scale in by the target tracking scaling policy is disabled. If the value is
                true, scale in is disabled and the target tracking scaling policy won't remove capacity from the
                scalable target. Otherwise, scale in is enabled and the target tracking scaling policy can
                remove capacity from the scalable target. The default value is false.

    Request Syntax:
        .. code-block:: sls

            [scaling_policy_name]:
              aws.application_autoscaling.scaling_policy.present:
                - name: 'string'
                - policy_name: 'string'
                - service_namespace: 'string'
                - scalable_dimension: 'string'
                - scaling_resource_id: 'string'
                - policy_type: 'string'
                - step_scaling_policy_configuration:
                    AdjustmentType: 'string'
                    StepAdjustments:
                        - MetricIntervalLowerBound: 'int'
                          MetricIntervalUpperBound: 'int'
                          ScalingAdjustment: 'int'
                        - MetricIntervalLowerBound: 'int'
                          MetricIntervalUpperBound: 'int'
                          ScalingAdjustment: 'int'
                        - MetricIntervalLowerBound: 'int'
                          ScalingAdjustment: 'int'
                    MinAdjustmentMagnitude: 'int'
                    Cooldown: 'int'
                    MetricAggregationType: 'string'


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            rds_scaling_policy_name:
              aws.application_autoscaling.scaling_policy.present:
                - name: rds_scaling_policy
                - policy_name: rds_scaling_policy
                - service_namespace: rds
                - scalable_dimension: rds:cluster:ReadReplicaCount
                - scaling_resource_id: idem-test-rds-aurora-table
                - policy_type: StepScaling
                - step_scaling_policy_configuration:
                    AdjustmentType: PercentChangeInCapacity
                    StepAdjustments:
                        - MetricIntervalLowerBound: 0
                          MetricIntervalUpperBound: 15
                          ScalingAdjustment: 1
                        - MetricIntervalLowerBound: 15
                          MetricIntervalUpperBound: 25
                          ScalingAdjustment: 2
                        - MetricIntervalLowerBound: 25
                          ScalingAdjustment: 3
                    MinAdjustmentMagnitude: 1
                    Cooldown: 20
                    MetricAggregationType: Average
    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    plan_state = None
    if resource_id:
        if not re.search(
            f"^({service_namespace})/({scaling_resource_id})/({scalable_dimension})/({policy_name})$",
            resource_id,
        ):
            result["comment"] = (
                f"Incorrect aws.application_autoscaling.scaling_policy resource_id: {resource_id}. Expected id {service_namespace}/{scaling_resource_id}/{scalable_dimension}/{policy_name}",
            )
            result["result"] = False
            return result
        before = await hub.exec.aws.application_autoscaling.scaling_policy.get(
            ctx=ctx,
            name=name,
            service_namespace=service_namespace,
            scaling_resource_id=scaling_resource_id,
            policy_names=[policy_name],
            scalable_dimension=scalable_dimension,
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        update_ret = await hub.tool.aws.application_autoscaling.scaling_policy.update_scaling_policy(
            ctx=ctx,
            name=name,
            before=result["old_state"],
            policy_name=policy_name,
            service_namespace=service_namespace,
            scaling_resource_id=scaling_resource_id,
            scalable_dimension=scalable_dimension,
            policy_type=policy_type,
            step_scaling_policy_configuration=step_scaling_policy_configuration,
            target_tracking_scaling_policy_configuration=target_tracking_scaling_policy_configuration,
        )
        result["comment"] = update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            for modified_param in update_ret["ret"]:
                plan_state[modified_param] = update_ret["ret"][modified_param]
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.application_autoscaling.scaling_policy", name=name
            )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "policy_name": policy_name,
                    "service_namespace": service_namespace,
                    "scaling_resource_id": scaling_resource_id,
                    "scalable_dimension": scalable_dimension,
                    "policy_type": policy_type,
                    "step_scaling_policy_configuration": step_scaling_policy_configuration,
                    "target_tracking_scaling_policy_configuration": target_tracking_scaling_policy_configuration,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.application_autoscaling.scaling_policy", name=name
            )
            return result
        ret = await hub.exec.boto3.client["application-autoscaling"].put_scaling_policy(
            ctx,
            PolicyName=policy_name,
            ServiceNamespace=service_namespace,
            ResourceId=scaling_resource_id,
            ScalableDimension=scalable_dimension,
            PolicyType=policy_type,
            StepScalingPolicyConfiguration=step_scaling_policy_configuration,
            TargetTrackingScalingPolicyConfiguration=target_tracking_scaling_policy_configuration,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.application_autoscaling.scaling_policy", name=name
        )
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.aws.application_autoscaling.scaling_policy.get(
                ctx=ctx,
                name=name,
                service_namespace=service_namespace,
                scaling_resource_id=scaling_resource_id,
                policy_names=[policy_name],
                scalable_dimension=scalable_dimension,
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] += after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] = result["comment"] + (str(e),)
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    scaling_resource_id: str = None,
    policy_name: str = None,
    service_namespace: str = None,
    scalable_dimension: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the specified scaling policy for an Application Auto Scaling scalable target.

    Deleting a step scaling policy deletes the underlying alarm action, but does not delete the CloudWatch alarm
    associated with the scaling policy, even if it no longer has an associated action. For more information, see
    Delete a step scaling policy and Delete a target tracking scaling policy in the Application Auto Scaling User Guide.

    Args:
        name(str):
            An Idem name of the resource.

        policy_name(str, Optional):
            The name of the scaling policy.

        service_namespace(str, Optional):
            The namespace of the Amazon Web Services service that provides the resource.
            For a resource provided by your own application or service, use custom-resource instead.

        scaling_resource_id(str, Optional):
            The identifier of the resource associated with the scalable target.
            This string consists of the resource type and unique identifier.

            * ECS service - The resource type is service and the unique identifier is the cluster name and service name.
              Example: service/default/sample-webapp.
            * Spot Fleet -
              The resource type is spot-fleet-request and the unique identifier is the Spot Fleet request ID.
              Example: spot-fleet-request/sfr-73fbd2ce-aa30-494c-8788-1cee4EXAMPLE.
            * EMR cluster - The resource type is instancegroup and the unique identifier is the cluster ID and instance
              group ID. Example: instancegroup/j-2EEZNYKUA1NTV/ig-1791Y4E1L8YI0.
            * AppStream 2.0 fleet - The resource type is fleet and the unique identifier is the fleet name.
              Example: fleet/sample-fleet.
            * DynamoDB table - The resource type is table and the unique identifier is the table name.
              Example: table/my-table.
            * DynamoDB global secondary index - The resource type is index and the
              unique identifier is the index name. Example: table/my-table/index/my-table-index.
            * Aurora DB cluster - The resource type is cluster and the unique identifier is the cluster name.
              Example: cluster:my-db-cluster.
            * SageMaker endpoint variant - The resource type is variant and the
              unique identifier is the resource ID. Example: endpoint/my-end-point/variant/KMeansClustering.
            * Custom resources are not supported with a resource type. This parameter must specify the
              OutputValue from the CloudFormation template stack used to access the resources. The unique
              identifier is defined by the service provider. More information is available in our GitHub
              repository.
            * Amazon Comprehend document classification endpoint -
              The resource type and unique identifier are specified using the endpoint ARN.
              Example: arn:aws:comprehend:us-west-2:123456789012:document-classifier-endpoint/EXAMPLE.
            * Amazon Comprehend entity recognizer endpoint -
              The resource type and unique identifier are specified using the endpoint ARN.
              Example: arn:aws:comprehend:us-west-2:123456789012:entity-recognizer-endpoint/EXAMPLE.
            * Lambda provisioned concurrency - The resource type is function and the unique identifier is the
              function name with a function version or alias name suffix that is not $LATEST. Example:
              function:my-function:prod or function:my-function:1.
            * Amazon Keyspaces table -
              The resource type is table and the unique identifier is the table name. Example:
              keyspace/mykeyspace/table/mytable.
            * Amazon MSK cluster -
              The resource type and unique identifier are specified using the cluster ARN.
              Example: arn:aws:kafka:us-east-1:123456789012:cluster/demo-cluster-1/6357e0b2-0e6a-4b86-a0b4-70df934c2e31-5.
            * Amazon ElastiCache replication group - The resource type is replication-group and the unique identifier
              is the replication group name. Example: replication-group/mycluster.
            * Neptune cluster -
              The resource type is cluster and the unique identifier is the cluster name. Example: cluster:mycluster.

        scalable_dimension(str, Optional):
            The scalable dimension. This string consists of the service namespace, resource type, and scaling property.

            * ecs:service:DesiredCount - The desired task count of an ECS service.
            * elasticmapreduce:instancegroup:InstanceCount - The instance count of an EMR Instance Group.
            * ec2:spot-fleet-request:TargetCapacity - The target capacity of a Spot Fleet.
            * appstream:fleet:DesiredCapacity - The desired capacity of an AppStream 2.0 fleet.
            * dynamodb:table:ReadCapacityUnits - The provisioned read capacity for a DynamoDB table.
            * dynamodb:table:WriteCapacityUnits - The provisioned write capacity for a DynamoDB table.
            * dynamodb:index:ReadCapacityUnits - The provisioned read capacity for a DynamoDB global secondary index.
            * dynamodb:index:WriteCapacityUnits - The provisioned write capacity for a DynamoDB global secondary index.
            * rds:cluster:ReadReplicaCount - The count of Aurora Replicas in an Aurora DB cluster.
              Available for Aurora MySQL-compatible edition and Aurora PostgreSQL- compatible edition.
            * sagemaker:variant:DesiredInstanceCount -
              The number of EC2 instances for an SageMaker model endpoint variant.
            * custom-resource:ResourceType:Property -
              The scalable dimension for a custom resource provided by your own application or service.
            * comprehend:document-classifier-endpoint:DesiredInferenceUnits -
              The number of inference units for an Amazon Comprehend document classification endpoint.
            * comprehend:entity-recognizer- endpoint:DesiredInferenceUnits -
              The number of inference units for an Amazon Comprehend entity recognizer endpoint.
            * lambda:function:ProvisionedConcurrency - The provisioned concurrency for a Lambda function.
            * cassandra:table:ReadCapacityUnits - The provisioned read capacity for an Amazon Keyspaces table.
            * cassandra:table:WriteCapacityUnits - The provisioned write capacity for an Amazon Keyspaces table.
            * kafka:broker-storage:VolumeSize -
              The provisioned volume size(in GiB) for brokers in an Amazon MSK cluster.
            * elasticache:replication-group:NodeGroups -
              The number of node groups for an Amazon ElastiCache replication group.
            * elasticache:replication-group:Replicas -
              The number of replicas per node group for an Amazon ElastiCache replication group.
            * neptune:cluster:ReadReplicaCount - The count of read replicas in an Amazon Neptune DB cluster.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Request Syntax:
        .. code-block:: sls

            [scaling_policy_name]:
              aws.application_autoscaling.scaling_policy.absent:
                - name: 'string'
                - policy_name: 'string'
                - service_namespace: 'string'
                - scalable_dimension: 'string'
                - scaling_resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            rds_scaling_policy_name:
              aws.application_autoscaling.scaling_policy.absent:
                - name: rds_scaling_policy
                - policy_name: rds_scaling_policy
                - service_namespace: rds
                - scalable_dimension: rds:cluster:ReadReplicaCount
                - scaling_resource_id: idem-test-rds-aurora-table
    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.application_autoscaling.scaling_policy", name=name
        )
        return result

    if (
        not service_namespace
        or not scaling_resource_id
        or not scalable_dimension
        or not policy_name
    ):
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.application_autoscaling.scaling_policy",
            name=name,
            args=[
                "service_namespace",
                "scaling_resource_id",
                "scalable_dimension",
                "policy_name",
            ],
        )
        result["result"] = False
        return result

    if not re.search(
        f"^({service_namespace})/({scaling_resource_id})/({scalable_dimension})/({policy_name})$",
        resource_id,
    ):
        result["comment"] = (
            f"Incorrect aws.application_autoscaling.scaling_policy resource_id: {resource_id}. Expected id {service_namespace}/{scaling_resource_id}/{scalable_dimension}/{policy_name}",
        )
        result["result"] = False
        return result
    before = await hub.exec.aws.application_autoscaling.scaling_policy.get(
        ctx=ctx,
        name=name,
        service_namespace=service_namespace,
        scaling_resource_id=scaling_resource_id,
        policy_names=[policy_name],
        scalable_dimension=scalable_dimension,
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.application_autoscaling.scaling_policy", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.application_autoscaling.scaling_policy", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client[
            "application-autoscaling"
        ].delete_scaling_policy(
            ctx,
            PolicyName=policy_name,
            ServiceNamespace=service_namespace,
            ResourceId=scaling_resource_id,
            ScalableDimension=scalable_dimension,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = result[
            "comment"
        ] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.application_autoscaling.scaling_policy", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Describes the Application Auto Scaling scaling policies for the specified service namespace. You can filter the
    results using ResourceId, ScalableDimension, and PolicyNames. For more information, see Target tracking scaling
    policies and Step scaling policies in the Application Auto Scaling User Guide.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.application_autoscaling.scaling_policy
    """
    result = {}
    # service_name_spaces supported by AWS. loop through all the service name spaces and list policies of each service.
    service_name_spaces = [
        "ecs",
        "elasticmapreduce",
        "ec2",
        "appstream",
        "dynamodb",
        "rds",
        "sagemaker",
        "custom-resource",
        "comprehend",
        "lambda",
        "cassandra",
        "kafka",
        "elasticache",
        "neptune",
    ]
    for service_name_space in service_name_spaces:
        ret = await hub.exec.boto3.client[
            "application-autoscaling"
        ].describe_scaling_policies(ctx, ServiceNamespace=service_name_space)
        if not ret["result"]:
            hub.log.debug(
                f"Could not describe scaling_policies for service name space {service_name_space}. {ret['comment']}"
            )
            continue
        for scaling_policy in ret["ret"]["ScalingPolicies"]:
            resource_id = f"{scaling_policy.get('ServiceNamespace')}/{scaling_policy.get('ResourceId')}/{scaling_policy.get('ScalableDimension')}/{scaling_policy.get('PolicyName')}"
            resource_translated = hub.tool.aws.application_autoscaling.conversion_utils.convert_raw_scaling_policy_to_present(
                ctx, raw_resource=scaling_policy, idem_resource_name=resource_id
            )
            result[resource_id] = {
                "aws.application_autoscaling.scaling_policy.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_translated.items()
                ]
            }
    return result
