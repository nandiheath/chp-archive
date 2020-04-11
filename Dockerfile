# Build the dependencies
FROM node:12-alpine AS builder

ENV NODE_ENV production
ENV GH_TOKEN change_token

RUN apk update && apk add --no-cache git openssl ca-certificates

# https://github.com/docker-library/python/issues/381
RUN apk add --no-cache python3-dev libstdc++ python3 py3-pip openjdk11 && \
    apk add --no-cache g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install numpy && \
    pip3 install pandas    

# symlink for pip works (for the py script)
RUN ln -s /usr/bin/pip3 /usr/bin/pip

WORKDIR /opt

COPY package.json .

RUN yarn --production --silent

COPY . .

CMD ["sh", "-c", "scripts/kinto_ci.sh"]