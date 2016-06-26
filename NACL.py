import boto3

vpc = raw_input("Enter a VPC ID: ")

EC2client = boto3.client('ec2')
EC2resource = boto3.resource('ec2')

network_acl_id = EC2client.create_network_acl(VpcId=vpc)['NetworkAcl']['NetworkAclId']
#print network_acl_id

EC2client.create_network_acl_entry(
    NetworkAclId=network_acl_id,
    RuleNumber=200,
    Protocol='6',
    RuleAction='deny',
    Egress=False,
    CidrBlock='0.0.0.0/0',
    PortRange={
        'From': 23,
        'To': 23
    }
)

EC2client.create_network_acl_entry(
    NetworkAclId=network_acl_id,
    RuleNumber=300,
    Protocol='-1',
    RuleAction='deny',
    Egress=False,
    CidrBlock='0.0.0.0/0'
)

network_acls = EC2client.describe_network_acls(
    Filters=[
        {
            'Name':'vpc-id',
            'Values': [vpc]
        }
    ]
)
network_acls.pop('ResponseMetadata')
#print network_acls
#print len(network_acls['NetworkAcls'])

#network_acl_id = map(lambda x: x['Associations'][0]['NetworkAclId'], network_acls['NetworkAcls'])
network_acls_filter = filter(lambda x: x['Associations']!=[], network_acls['NetworkAcls'])
print network_acls_filter
network_acl_association_id = map(lambda x: x['NetworkAclAssociationId'], network_acls_filter[0]['Associations'])
#print network_acl_association_id

i=0
while i < len(network_acl_association_id):
    EC2client.replace_network_acl_association(
        AssociationId=network_acl_association_id[i],
        NetworkAclId=network_acl_id
    )
    i=i+1

