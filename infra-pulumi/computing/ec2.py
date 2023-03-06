import pulumi
import pulumi_aws as aws


def ec2_instance_funcional(name, amiId, instanceType, public_ip, vpc_id, subnet_id, userData):
    size = instanceType

    group = aws.ec2.SecurityGroup('web-secgrp',
        description='Enable HTTP access',
        vpc_id = f'{vpc_id}',
        ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol = 'tcp',
            from_port = 80,
            to_port = 80,
            cidr_blocks = ['0.0.0.0/0']
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol = 'tcp',
            from_port = 22,
            to_port = 22,
            cidr_blocks = ['0.0.0.0/0']
        ),
        aws.ec2.SecurityGroupEgressArgs(
                from_port=0,
                to_port=0,
                protocol="-1",
                cidr_blocks=["0.0.0.0/0"],
                ipv6_cidr_blocks=["::/0"],
            )],
        )
    server = aws.ec2.Instance(f'{name}',
        instance_type = size,
        associate_public_ip_address = public_ip,
        vpc_security_group_ids = [group.id],
        user_data = userData,
        subnet_id = subnet_id,
        ami = amiId)

    pulumi.export('public_ip', server.public_ip)
    pulumi.export('public_dns', server.public_dns)