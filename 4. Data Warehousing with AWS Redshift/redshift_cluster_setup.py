import boto3
import json
import configparser


def create_iam_role(DWH_IAM_ROLE_NAME):
    """
    Description:
        - Creates an IAM role that allows Redshift to call on 
          other AWS services
    
    Returns:
        - Role Arn
    """
    # Create the IAM role
    try:
        print('1.1 Creating a new IAM Role')
        dwh_role = iam.create_role(
        Path = '/',
        RoleName = DWH_IAM_ROLE_NAME,
        Description = 'Allows Redshift cluster to call AWS service on your behalf.',
        AssumeRolePolicyDocument = json.dumps(
            {'Statement': [{'Action': 'sts:AssumeRole',
                        'Effect': 'Allow', 
                        'Principal': {'Service': 'redshift.amazonaws.com'}}],
            'Version': '2012-10-17'})
        )
        # Attach Policy
        iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                               PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                               )['ResponseMetadata']['HTTPStatusCode']
        role_arn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']
        return role_arn
    except Exception as e:
        print(e)

    

def main():
    """
    Description:
        - Sets up a Redshift cluster on AWS
    
    Returns:
        None
    """
    # Load DWH parameters from a file
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))
    KEY                    = config.get('AWS','KEY')
    SECRET                 = config.get('AWS','SECRET')
    DWH_CLUSTER_TYPE       = config.get("DWH","DWH_CLUSTER_TYPE")
    DWH_NUM_NODES          = config.get("DWH","DWH_NUM_NODES")
    DWH_NODE_TYPE          = config.get("DWH","DWH_NODE_TYPE")
    DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
    DWH_DB                 = config.get("DWH","DWH_DB")
    DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
    DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
    DWH_PORT               = config.get("DWH","DWH_PORT")
    DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")

    # Create clients for EC2, S3, IAM, and Redshift
    ec2 = boto3.resource('ec2', 
                         region_name='us-west-2',
                         aws_access_key_id=KEY,
                         aws_secret_access_key=SECRET)

    iam = boto3.client('iam',
                       region_name='us-west-2',
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET)

    redshift = boto3.client('redshift',
                            region_name="us-west-2",
                            aws_access_key_id=KEY,
                            aws_secret_access_key=SECRET)
    
    role_arn = create_iam_role(DWH_IAM_ROLE_NAME)

    # Create the cluster
    try:
    response = redshift.create_cluster(        
        #HW
        ClusterType=DWH_CLUSTER_TYPE,
        NodeType=DWH_NODE_TYPE,
        NumberOfNodes=int(DWH_NUM_NODES),

        #Identifiers & Credentials
        DBName=DWH_DB,
        ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
        MasterUsername=DWH_DB_USER,
        MasterUserPassword=DWH_DB_PASSWORD,
        
        #Roles (for s3 access)
        IamRoles=[role_arn]  
    )

    # Open an incoming  TCP port to access the cluster endpoint
    vpc = ec2.Vpc(id=myClusterProps['VpcId'])
    default_sg = list(vpc.security_groups.all())[0]
    default_sg.authorize_ingress(
        GroupName=default_sg.group_name,
        CidrIp='0.0.0.0/0',
        IpProtocol='TCP',
        FromPort=int(DWH_PORT),
        ToPort=int(DWH_PORT)
    )
    except Exception as e:
        print(e)
    
    print("Cluster has been created, check details of cluster on AWS")


if __name__ == "__main__":
    main()