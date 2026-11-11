# Para generar la imagen oficial con iconos oficiales de AWS:
# 1. Instalar graphviz: brew install graphviz
# 2. Instalar diagrams: pip install diagrams
# 3. Ejecutar: python3 docs/architecture_diagram.py

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPC, PublicSubnet, PrivateSubnet, InternetGateway, NATGateway, ALB
from diagrams.aws.management import SystemsManager, SystemsManagerParameterStore
from diagrams.aws.storage import S3
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import Users

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram("AWS Multi-AZ Secure Infrastructure", show=False, filename="docs/architecture", outformat="png", graph_attr=graph_attr):
    users = Users("Internet Users")
    admin = Users("DevOps / Admin")

    gha = GithubActions("GitHub Actions CI/CD")
    ssm_param = SystemsManagerParameterStore("SSM Parameter Store\n(State Bucket Name)")
    s3_state = S3("S3 Remote State")

    # Flujo de CI/CD
    gha >> Edge(label="1. Get Bucket") >> ssm_param
    gha >> Edge(label="2. Remote State") >> s3_state

    with Cluster("AWS Cloud - Region (us-east-1)"):
        with Cluster("VPC (10.0.0.0/16)"):
            igw = InternetGateway("Internet Gateway")
            alb = ALB("Application Load Balancer\n(Multi-AZ)")

            with Cluster("Availability Zone A (us-east-1a)"):
                pub_subnet_a = PublicSubnet("Public Subnet A\n10.0.1.0/24")
                nat_gw = NATGateway("NAT Gateway + EIP")
                priv_subnet_a = PrivateSubnet("Private Subnet A\n10.0.3.0/24")
                ec2_app = EC2("EC2 Instance\n(Docker :80)")

            with Cluster("Availability Zone B (us-east-1b)"):
                pub_subnet_b = PublicSubnet("Public Subnet B\n10.0.2.0/24")

            # Conexiones de red
            users >> Edge(label="HTTP :80") >> alb
            alb >> Edge(label="Forward :80") >> ec2_app

            ec2_app >> Edge(label="Outbound") >> nat_gw
            nat_gw >> igw
            igw >> Edge(label="Internet") >> users

            # Conexión SSM
            admin >> Edge(label="SSM Session\n(Zero SSH)", style="dashed", color="purple") >> ec2_app
