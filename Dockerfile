FROM tiangolo/uvicorn-gunicorn:python3.9-slim
LABEL maintainer="poojasingari"
ENV WORKERS_PER_CORE=4
ENV MAX_WORKERS=4
ENV LOG_LEVEL="warning"
ENV TIMEOUT="200"
RUN mkdir /objdetect
COPY requirements.txt /objdetect
COPY . /objdetect
WORKDIR /objdetect
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn","server:app","--host","0.0.0.0","--port","8000"]
