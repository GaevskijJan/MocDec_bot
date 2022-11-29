FROM python:3.10.8
ARG API_TOKEN_ARG
ENV API_TOKEN=$API_TOKEN_ARG
RUN mkdir /mocDeclarant
WORKDIR /mocDeclarant
ENV PYTHONPATH="/mocDeclarant"
COPY ["setup.py", "requirements.txt", "/mocDeclarant/"]
RUN  python -m venv venv  \
     && pip install --upgrade pip \
     && venv/bin/pip3 install wheel \
     && venv/bin/python3 setup.py
COPY src /mocDeclarant/src
CMD ["python", "src/telegram.py"]
