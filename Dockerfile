FROM ubuntu:latest

RUN apt-get update && apt-get -y install  python3.11 python3.11-distutils python3-pip
RUN pip install pyTelegramBotAPI
RUN pip install requests
RUN pip install bs4
RUN pip install asyncio
RUN pip install aiohttp