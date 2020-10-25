#!/usr/bin/python

"""Script to generate ssh config file for AWS EC2 instances in a region."""

import boto3
import os

# The generated config file
path_to_config = '/root/.ssh/aws_ec2.config'

# The path to the SSH key we use to connect to those instances
path_to_ssh_key = os.environ['SSH_KEY_PATH']

# The username to use for ssh
instance_username = os.environ['INSTANCE_USERNAME']

def main():
 
    try:
        """
        Describe ec2 instances and generate the format of the ssh config file.
        """
        aws_client = boto3.client('ec2')
        paginator = aws_client.get_paginator('describe_instances')
        response_iterator = paginator.paginate(
            DryRun=False,
            PaginationConfig={
                'MaxItems': 100,
                'PageSize': 10
            }
        )

       
        ssh_config_file = open(path_to_config, 'w')

        ssh_config_file.write("##########################\n")
        ssh_config_file.write("##### AWS SSH CONFIG #####\n")
        ssh_config_file.write("##########################\n\n")

        """
        We iterate the results and read the tags for each instance.
        If the instance has no Tags we use the PublicDnsName as host
        Using those we create an ssh config entry for each instance.
        and append it to the config file.
        host <Tag Name or PublicDnsName>
            Hostname <ec2-public-ip>
            IdentityFile <path_to_ssh_key>
            User <instance_username>
        """
        for page in response_iterator:
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    
                    try:
                        host_line = ""
                        host = ""
                        env = ""
                        if 'PublicIpAddress' in instance:
                            public_ip = instance['PublicIpAddress']
                            for tag in instance['Tags']:
                                if tag['Key'] == "Name":
                                    name = tag['Value']
                                else:
                                    name=instance['PublicDnsName']

                            host_line += "##########################\n"
                            host_line += "host {}\n".format(name)
                            host_line += "    Hostname {}\n".format(public_ip)
                            host_line += "    IdentityFile {}\n".format(
                                path_to_ssh_key)
                            host_line += "    user {}\n".format(
                                instance_username)
                            host_line += "##########################\n"
                            host_line += "\n"
                            ssh_config_file.write(host_line)
                    except Exception as e:
                        raise e

        print("File updated: " + path_to_config)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()