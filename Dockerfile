FROM python:3.7-alpine as base

ENV INSTANCE_USERNAME=ubuntu
ENV AWS_DEFAULT_REGION=us-east-2

FROM base as builder

RUN mkdir /install
WORKDIR /install

# copy the dependencies file to the working directory
COPY requirements.txt /requirements.txt

# install dependencies
RUN pip install --prefix=/install -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local

# set the working directory in the container
WORKDIR /root
RUN mkdir .ssh

COPY aws_ssh_get_info.py ./

ENTRYPOINT [ "python" ] 
CMD ["./aws_ssh_get_info.py" ]