# AWS EC2 GET SSH CONFIG

## Description

A simple dockerized python script that queries the AWS EC2 API with boto and generates a [SSH config file](https://linuxize.com/post/using-the-ssh-config-file/) to use. There are already similar scripts but I couldnt find a dockerized one that allows execution with one-line command. In order to generate names that you can easily use to ssh in the `host` option of the config file, this script reads the `TAGS` of each instance and tries to find a tag `NAME` on the instance and use its value. If this tag doesnt exist the public dns name is used to populate the `host` option.

## Usage

Before using this script make sure:

- you have an ssh key file that will be used to connect to EC2 instances in `/Users/$USER/.ssh/`
- you have installed `awscli`
- run `awscli configure` to configure connection details to aws. If you have multi-factor auth enabled you ll need first to run
  `aws sts get-session-token --serial-number arn:aws:iam::0123456789:mfa/<username here> --token-code <token here>`
- use the details from the ouput of the above command and export as env variables:

```bash
export AWS_ACCESS_KEY_ID=#############
export AWS_SECRET_ACCESS_KEY=###############
```

(if multi-factor auth enabled also):

```bash
export AWS_SESSION_TOKEN=###############
```

And you are ready to generate the ssh config file! Example command shown below. The docker run command should specify:

- the path where your `.ssh` directory is, mount it as volume: `-v ~/.ssh/:/root/.ssh/`
- set the env vars `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`(if needed), `SSH_KEY_PATH`

```bash
docker run -v ~/.ssh/:/root/.ssh/ -e "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" -e "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" -e "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN" -e "SSH_KEY_PATH=~/.ssh/ssh_example_name.pem" moustakis/aws-ec2-get-ssh-config:1.0
```

- by default is set `AWS_DEFAULT_REGION=us-east-2` and `INSTANCE_USERNAME=ubuntu` you can also override these using the `-e` option:

```bash
docker run -v ~/.ssh/:/root/.ssh/ -e "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" -e "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" -e "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN" -e "SSH_KEY_PATH=~/.ssh/ssh_example_name.pem" -e "AWS_DEFAULT_REGION=us-east-1" moustakis/aws-ec2-get-ssh-config:1.0
```

On successful  execution you should see a message:
`File updated: /root/.ssh/aws_ec2.config`
The `/root` location refers to the path inside the container. Locally you should have have generated the file under `/Users/$USER/.ssh/`. Go to this directory and rename the file to `config` and you are good to go!

Now you can use it to ssh to AWS EC2 instances by using the name after every `host` value. For example for an entry:

```bash
##########################
host dummy_name
    Hostname #.#.#.#
    IdentityFile ~/.ssh/ssh_example_name.pem
    user ubuntu
##########################
```

You can just use `ssh dummy_name` to connect to the instance, Happy SSHing!
