from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import InternetGateway, NATGateway, ALB
from diagrams.aws.management import SystemsManager, SystemsManagerParameterStore
from diagrams.aws.storage import S3
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker

graph_attr = {
    "fontsize": "16",
    "fontname": "Helvetica-Bold",
    "bgcolor": "white",
    "pad": "0.8",
    "splines": "spline",
    "nodesep": "1.0",
    "ranksep": "1.3"
}

node_attr = {
    "fontname": "Helvetica",
    "fontsize": "11"
}

cloud_cluster_attr = {
    "bgcolor": "#F4F8FB",
    "pencolor": "#232F3E",
    "penwidth": "2.0",
    "fontsize": "14",
    "fontname": "Helvetica-Bold",
    "style": "rounded",
    "margin": "28"
}

vpc_cluster_attr = {
    "bgcolor": "#FFFFFF",
    "pencolor": "#8C4FFF",
    "penwidth": "2.0",
    "fontsize": "13",
    "fontname": "Helvetica-Bold",
    "style": "rounded",
    "margin": "28"
}

public_cluster_attr = {
    "bgcolor": "#EBF7E3",
    "pencolor": "#3F8624",
    "penwidth": "2.0",
    "fontsize": "12",
    "fontname": "Helvetica-Bold",
    "style": "rounded",
    "margin": "26"
}

private_cluster_attr = {
    "bgcolor": "#E6F2F8",
    "pencolor": "#0073BB",
    "penwidth": "2.0",
    "fontsize": "12",
    "fontname": "Helvetica-Bold",
    "style": "rounded",
    "margin": "26"
}

cicd_cluster_attr = {
    "bgcolor": "#F4F6F8",
    "pencolor": "#2088FF",
    "penwidth": "1.8",
    "fontsize": "12",
    "fontname": "Helvetica-Bold",
    "style": "rounded",
    "margin": "26"
}

with Diagram(
    "AWS Secure VPC & Private EC2 Architecture",
    show=False,
    filename="docs/architecture",
    outformat="png",
    direction="LR",
    graph_attr=graph_attr,
    node_attr=node_attr
):
    users = Users("Internet Users")
    admin = Users("DevOps / Admin")

    with Cluster("CI/CD & Remote State (Bootstrap)", graph_attr=cicd_cluster_attr):
        gha = GithubActions("GitHub Actions")
        ssm_param = SystemsManagerParameterStore("SSM Parameter Store\n(/tfstate/bucket_name)")
        s3_state = S3("Amazon S3\n(Terraform State)")
        gha >> Edge(label="1. Read Bucket", fontname="Helvetica", fontsize="10") >> ssm_param
        gha >> Edge(label="2. Save State", fontname="Helvetica", fontsize="10") >> s3_state

    with Cluster("AWS Cloud - Region (us-east-1)", graph_attr=cloud_cluster_attr):
        ssm_session = SystemsManager("AWS SSM\nSession Manager")

        with Cluster("VPC (10.0.0.0/16)", graph_attr=vpc_cluster_attr):
            igw = InternetGateway("Internet Gateway")

            with Cluster("Public Subnets (10.0.1.0/24 & 10.0.2.0/24)", graph_attr=public_cluster_attr):
                alb = ALB("Application Load Balancer\n(HTTP :80 Open)")
                nat_gw = NATGateway("NAT Gateway + EIP\n(Outbound Only)")

            with Cluster("Private Subnet (10.0.3.0/24 - Single-AZ PoC)", graph_attr=private_cluster_attr):
                ec2_app = EC2("Private EC2 Instance\n(SG: Only from ALB)")
                docker_app = Docker("Docker :80\n(nginxdemos/hello)")
                ec2_app >> Edge(label="Runs", style="dotted", fontname="Helvetica", fontsize="10") >> docker_app

            # 1. Flujo Entrante (Usuario directo al ALB en puerto 80 -> EC2 privada)
            users >> Edge(label="HTTP :80", color="#232F3E", penwidth="2.0", fontname="Helvetica-Bold", fontsize="10") >> alb
            alb >> Edge(label="Forward :80\n(ALB SG Only)", color="#3F8624", penwidth="2.0", fontname="Helvetica-Bold", fontsize="10") >> ec2_app

            # 2. Flujo Saliente de la EC2 privada hacia Internet (EC2 -> NAT -> IGW)
            igw << Edge(label="Internet Egress", color="#ED7100", style="dashed", fontname="Helvetica", fontsize="10") << nat_gw
            nat_gw << Edge(label="Outbound Traffic\n(0.0.0.0/0)", color="#ED7100", style="dashed", fontname="Helvetica", fontsize="10") << ec2_app

            # 3. Flujo de Administración Segura (Zero SSH)
            admin >> Edge(label="IAM Auth", color="#C925D1", style="dashed", fontname="Helvetica", fontsize="10") >> ssm_session
            ssm_session >> Edge(label="Encrypted Tunnel\n(Zero SSH)", color="#C925D1", style="dashed", fontname="Helvetica", fontsize="10") >> ec2_app
