FROM openstax/python3-poetry
# 设置开发者信息
MAINTAINER xgz <prestieaetgmts@gmail.com>
COPY . /ip
WORKDIR /ip
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "ip.py"]