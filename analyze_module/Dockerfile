FROM python:3.10-slim

RUN groupadd --gid 1000 code && \
          useradd --create-home --gid 1000 --uid 1000 code
RUN mkdir -p /home/code/psaa/analyze_module
WORKDIR /home/code/psaa/analyze_module
COPY ./requirements.txt /home/code/psaa/analyze_module/
RUN pip3 install -r requirements.txt
COPY ./ /home/code/psaa/analyze_module/
USER code
ENTRYPOINT ["./main.py"]
