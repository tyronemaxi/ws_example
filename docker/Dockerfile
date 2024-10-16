FROM tyronextian/debian-python

# 把根目录的requirements.txt拷贝到这来再做镜像
COPY requirements.txt /tmp

ARG code_dir="/code"
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:$code_dir"

WORKDIR $code_dir

RUN pip install  --no-cache-dir -r  /tmp/requirements.txt -i http://10.142.12.18:38080/storages/ai/ai-dep-pypi-group --trusted-host 10.142.12.18 &&  \
    pip install --no-cache-dir http://10.142.12.18:38080/storages/ai/ai-dep-raw/spacy-models/zh_core_web_md-3.7.0/zh_core_web_md-3.7.0.tar.gz  \
    -i http://10.142.12.18:38080/storages/folib-common/python-proxy-pypi/ --trusted-host 10.142.12.18 --timeout=600 && \
    rm -rf /tmp/requirements.txt && apt clean && rm -rf /var/lib/apt/lists/*

#RUN pip install --no-cache-dir -r  /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
#    pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/zh_core_web_md-3.7.0/zh_core_web_md-3.7.0.tar.gz && \
#    rm -rf /tmp/requirements.txt && apt clean && rm -rf /var/lib/apt/lists/*


COPY . $code_dir

CMD ["gunicorn", "-c", "gunicorn.conf.py", "server:create_app()"]