FROM python:3.6


RUN apt update \
 && apt install -y apt-transport-https \
 && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
 && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
 && curl -sL https://deb.nodesource.com/setup_8.x | bash - \
 && apt install -y yarn


RUN mkdir pgadmin \
 && mkdir pgadmin_venv \
 && python -m venv /pgadmin_venv

ADD build.sh /bin/build_pgadmin.sh

RUN chmod u+x /bin/build_pgadmin.sh
