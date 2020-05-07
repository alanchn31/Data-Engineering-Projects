import boto3
import configparser

def main():
    """
    Description:
        - Sets up a Redshift cluster on AWS
    
    Returns:
        None
    """
    KEY                    = config.get('AWS','KEY')
    SECRET                 = config.get('AWS','SECRET')
    DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
    DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")

    redshift = boto3.client('redshift',
                            region_name="us-west-2",
                            aws_access_key_id=KEY,
                            aws_secret_access_key=SECRET)

    iam = boto3.client('iam',
                       region_name='us-west-2',
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET)

    redshift.delete_cluster(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  
                            SkipFinalClusterSnapshot=True)
    
    # Remove role:
    iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, 
                           PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
    iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
    print("Cluster and IAM role has been deleted")

if __name__ == "__main__":
    main()