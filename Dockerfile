# Build the dependencies
FROM node:12-alpine AS builder

ENV NODE_ENV production

ENV GH_TOKEN change_token

WORKDIR /opt

COPY package.json .

RUN yarn --production --silent

COPY . .

CMD ["sh", "-c", "scripts/kinto_ci.sh"]