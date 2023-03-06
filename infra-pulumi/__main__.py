import pulumi
from pulumi_aws import s3
from network import base_network
from computing import ec2
#CONFIGURAÇÃO DE NETWORK, ULTILIZA O CONSTRUTOR CRIADO EM NETWORK NO ARQUIVO base_network.
#APENAS CONFIGURAR AS VARIÁVEIS ABAIXO.

NAME = "ayo" #VPC NAME
BLOCK_IP_VPN = "10.1.0.0/16" # BLOCK VPC
BLOCK_IP_SUBNET_PUBLIC = "10.1.1.0/24" # BLOCK SUBNET PUBLIC
BLOCK_IP_SUBNET_PRIVATE = "10.1.2.0/24" # BLOCK SUBNET PRIVATE

base_network.network_constructor(NAME, BLOCK_IP_VPN, BLOCK_IP_SUBNET_PUBLIC, BLOCK_IP_SUBNET_PRIVATE)

user_data = """
#!/bin/bash
echo "Hello, World!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

#CONFIGURAÇÃO EC2, ULTILIZAR O CONSTRUTOR CRIADO EM COMPUTING NO ARQUIIVO ec2.
#APENAS CONFIGURAR AS VARIÁVEIS ABAIXO.
NAME =  "vpn"
AMIID = "ami-0557a15b87f6559cf"
INSTANCE_TYPE = "t2.medium"
PUBLIC_IP = True
VPC_ID = "vpc-0e41cb6f963ddd115"
SUBNET_ID = "subnet-0f93f1e4d6c6f65b5"
USER_DATA = user_data

ec2.ec2_instance_funcional(NAME,AMIID, INSTANCE_TYPE, PUBLIC_IP,VPC_ID, SUBNET_ID, USER_DATA)