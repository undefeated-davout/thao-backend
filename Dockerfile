FROM python:3.10.7-slim-bullseye

RUN apt update && apt install --no-install-recommends -y \
    bash \
    git \
    tesseract-ocr \
    libtesseract-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN echo "alias ll='ls -lahF'" >> ~/.bashrc

WORKDIR /opt/app
COPY requirements.txt /opt/app
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /opt/app/src

CMD ["/bin/bash"]
