from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import InternetGateway, NATGateway, ALB
from diagrams.aws.management import SystemsManager, SystemsManagerParameterStore
from diagrams.aws.storage import S3
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker

graph_attr = {
    "fontsize": "15",
    "bgcolor": "white",
    "pad": "0.6",
    "splines": "spline",
    "nodesep": "0.9",
    "ranksep": "1.2"
}

public_cluster_attr = {
    "bgcolor": "#EBF7E3",
    "pencolor": "#3F8624",
    "penwidth": "2.0",
    "fontsize": "13",
    "style": "rounded"
}

private_cluster_attr = {
    "bgcolor": "#E6F2F8",
    "pencolor": "#0073BB",
    "penwidth": "2.0",
    "fontsize": "13",
    "style": "rounded"
}

vpc_cluster_attr = {
    "bgcolor": "#F8F9FA",
    "pencolor": "#8C4FFF",
    "penwidth": "2.0",
    "fontsize": "14",
    "style": "rounded"
}

cicd_cluster_attr = {
    "bgcolor": "#F4F6F8",
    "pencolor": "#2088FF",
    "penwidth": "1.5",
    "fontsize": "13",
    "style": "rounded"
}

with Diagram(
    "AWS Multi-AZ Secure Infrastructure",
    show=False,
    filename="docs/architecture",
    outformat="png",
    direction="LR",
    graph_attr=graph_attr
):
    users = Users("Internet Users")
    admin = Users("DevOps / Admin")

    with Cluster("CI/CD & Remote State (Bootstrap)", graph_attr=cicd_cluster_attr):
        gha = GithubActions("GitHub Actions")
        ssm_param = SystemsManagerParameterStore("SSM Parameter Store\n(/tfstate/bucket_name)")
        s3_state = S3("Amazon S3\n(Terraform State)")
        gha >> Edge(label="1. Get Bucket", fontsize="11") >> ssm_param
        gha >> Edge(label="2. Save State", fontsize="11") >> s3_state

    with Cluster("AWS Cloud - Region (us-east-1)"):
        ssm_session = SystemsManager("AWS SSM\nSession Manager")

        with Cluster("VPC (10.0.0.0/16)", graph_attr=vpc_cluster_attr):
            igw = InternetGateway("Internet Gateway")

            with Cluster("Public Subnets Multi-AZ\n(10.0.1.0/24 - AZ-a | 10.0.2.0/24 - AZ-b)", graph_attr=public_cluster_attr):
                alb = ALB("Application Load Balancer\n(SG: HTTP :80 Open)")
                nat_gw = NATGateway("NAT Gateway + EIP\n(Public Subnet AZ-a)")

            with Cluster("Private Subnet (AZ-a)\n(10.0.3.0/24 - Isolated / No Public IP)", graph_attr=private_cluster_attr):
                ec2_app = EC2("EC2 Instance\n(SG: Only from ALB)")
                docker_app = Docker("Docker :80\n(nginxdemos/hello)")
                ec2_app >> Edge(label="Runs", style="dotted", fontsize="11") >> docker_app

            # 1. Flujo Entrante (Izquierda -> Derecha: Internet -> IGW -> ALB -> EC2)
            users >> Edge(label="HTTP :80", color="#232F3E", penwidth="2.0", fontsize="11") >> igw
            igw >> Edge(label="Public Route", color="#232F3E", penwidth="2.0", fontsize="11") >> alb
            alb >> Edge(label="Forward :80\n(ALB SG Only)", color="#3F8624", penwidth="2.0", fontsize="11") >> ec2_app

            # 2. Flujo Saliente (EC2 -> NAT -> IGW usando constraint=false para mantener orden visual Izq->Der)
            igw << Edge(label="Internet Egress", color="#ED7100", style="dashed", fontsize="11") << nat_gw
            nat_gw << Edge(label="Outbound Traffic\n(0.0.0.0/0)", color="#ED7100", style="dashed", fontsize="11") << ec2_app

            # 3. Flujo de Administración Segura (Zero SSH)
            admin >> Edge(label="IAM Auth", color="#C925D1", style="dashed", fontsize="11") >> ssm_session
            ssm_session >> Edge(label="Encrypted Tunnel\n(Zero SSH)", color="#C925D1", style="dashed", fontsize="11") >> ec2_app
