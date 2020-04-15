### 1. Get Linux
FROM rappdw/docker-java-python:openjdk1.8.0_171-python3.6.6

RUN apt-get update && apt-get install -y git openssl apt-transport-https ca-certificates

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN apt-get update && apt-get -y install yarn

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -y nodejs

ENV NODE_ENV production

ENV GH_TOKEN change_token

WORKDIR /app

COPY . /app

RUN yarn --production --silent

CMD ["sh", "-c", "scripts/kinto_ci.sh"]