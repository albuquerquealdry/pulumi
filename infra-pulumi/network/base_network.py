import pulumi
import pulumi_aws as aws

def network_constructor(vpc_name, block_vpc_ip, block_subnet_public, block_subnet_private):

    vpc = aws.ec2.Vpc(f"{vpc_name}",
        cidr_block = f"{block_vpc_ip}",
        instance_tenancy="default",
        tags={
            f"Name": f"{vpc_name}",
        })

    subnet_public = aws.ec2.Subnet(f"subnet_public-{vpc_name}",
        vpc_id=vpc.id,
        cidr_block = f"{block_subnet_public}",
        tags={
            "Name": f"subnet_public-{vpc_name}",
        })

    subnet_private = aws.ec2.Subnet(f"subnet_private-{vpc_name}",
        vpc_id=vpc.id,
        cidr_block = f"{block_subnet_private}",
        tags={
            "Name": f"subnet_private-{vpc_name}",
        })

    igw = aws.ec2.InternetGateway(f"igwt-{vpc_name}",
        vpc_id=vpc.id,
        tags={
            "Name": f"igwt-{vpc_name}",
        })

    rt_public = aws.ec2.RouteTable(f"rt_public_{vpc_name}",
        vpc_id=vpc.id,
        routes=[
            aws.ec2.RouteTableRouteArgs(
                cidr_block="0.0.0.0/0",
                gateway_id=igw.id,
            )
        ],
        tags={
            "Name": f"rt_public_{vpc_name}",
        })

    public_rt_association = aws.ec2.RouteTableAssociation(
            f"rt_associatio_{vpc_name}",
            route_table_id=rt_public.id,
            subnet_id=subnet_public.id
    )

    elastic_ip = aws.ec2.Eip(f"elastic_ip{vpc_name}",
        vpc=True)

    natgateway = aws.ec2.NatGateway(f"natgateway_{vpc_name}",
        allocation_id=elastic_ip.allocation_id,
        subnet_id=subnet_public.id,
        tags={
            "Name": f"natgateway_{vpc_name}",
        },
        opts=pulumi.ResourceOptions(depends_on=[igw]))

    rt_private = aws.ec2.RouteTable(f"rt_private_{vpc_name}",
        vpc_id=vpc.id,
        routes=[
            aws.ec2.RouteTableRouteArgs(
                cidr_block="0.0.0.0/0",
                gateway_id=natgateway.id,
            )
        ],
        tags={
            "Name": f"rt_private_{vpc_name}",
        })

    private_rt_association = aws.ec2.RouteTableAssociation(
            f"private_rt_association_{vpc_name}",
            route_table_id=rt_private.id,
            subnet_id=subnet_private.id
    )