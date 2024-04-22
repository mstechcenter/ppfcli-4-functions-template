# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.8-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.8

WORKDIR /tmp

RUN wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y dotnet-sdk-8.0 && \
    rm packages-microsoft-prod.deb
# RUN dotnet --version

RUN /usr/bin/dotnet tool install --global Microsoft.PowerApps.CLI.Tool && \
    cp $HOME/.dotnet/tools/pac /usr/bin && \
    cp -R $HOME/.dotnet/tools/.store /usr/bin && \
    rm $HOME/.dotnet/tools/pac && \
    rm -r $HOME/.dotnet/tools/.store
# RUN pac

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot