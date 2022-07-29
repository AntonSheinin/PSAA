FROM python:3.10-slim

RUN groupadd --gid 1000 code && \
          useradd --create-home --gid 1000 --uid 1000 code
RUN mkdir -p /home/code
WORKDIR /home/code/psaa
COPY ./requirements.txt /home/code/psaa/
RUN pip3 install -r requirements.txt
COPY ./ /home/code/psaa/
USER code
ENTRYPOINT ["./main.py"]
