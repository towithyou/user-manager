FROM haiquanduan/nginx-py36
RUN rm -rf /dist
COPY user-manager /user-manager
COPY dist /dist
RUN cd /user-manager && pip3 install -r requirements.txt -i  https://mirrors.aliyun.com/pypi/simple/
WORKDIR /user-manager
CMD ["/bin/bash", "start.sh"]
