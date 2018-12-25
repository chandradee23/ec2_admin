# Description

This is an application intended to be used with public AMI: [ami-0bc875f9c35daaa25](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#LaunchInstanceWizard:ami=ami-0bc875f9c35daaa25), but most features will work with any EC2 AMI.

The application will allow:
* Setup AWS Api Keys and SSH PEM
* Create users and set password
* Connect S3 Buckets
* Install required Applications via [chocolately](https://chocolatey.org/)
* Login via SSH
* Launch Rstudio Server website
* Launch JupyterHUB with JupyterLab
* Launch x2go Remote Resktop
* Launch WinSCP for file transfer
* Resize EC2 but not changing architecture
* Turn on, of and reset EC2

The AMI is based on [Arch](https://www.uplinklabs.net/projects/arch-linux-on-ec2/) and it includes:
* s3fs for direct interactionwith s3 Bucket
* XFCE4
* x2go for remote desktop
* libreoffice
* rsturio-server
* JupyterHub with Jupyterlab configured with R, Julia and Python
* Misc tools like yay, screen, wget, htop, etc...
* configured to be passwordless

The following video will show the application and configuration:
ToDo

## AMI Description

The ami is intended to provide a cheap and elastic Data Science Cloud laboratory.

## Compatibility

Most features will work the best on Windows and KDE

## Instructions

After creating you EC2 from the [ami-0bc875f9c35daaa25](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#LaunchInstanceWizard:ami=ami-0bc875f9c35daaa25), follow the buttons of the Setup Tab from top to bottom.