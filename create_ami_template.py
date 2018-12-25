import boto3

template_id = "i-0451fb4d63df2a99a"
ami_name = "danielfm123 clowd datascience"

session = boto3.Session(profile_name = "danielfm123")
ec2 = session.resource("ec2")

template = ec2.Instance(id=template_id)
template.tags
ami = ec2.images.filter(Filters = [{'Name': 'tag:template_id',
                                    'Values':[template_id]}])
ami = list(ami)[0]
snapshots = ami.block_device_mappings
snapshots_id = [x["Ebs"]["SnapshotId"] for x in snapshots]
ami.deregister()
for s in snapshots_id:
    snapshot = ec2.Snapshot(s)
    snapshot.delete()

ami = template.create_image(Name = 'danielfm123 clowd datascience',)
ami.create_tags(Tags = [{'Key':'template_id', 'Value': template_id}])
ami.modify_attribute(LaunchPermission ={'Add' : [{'Group':'all'}]})

url = 'https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#LaunchInstanceWizard:ami=' + ami.id



