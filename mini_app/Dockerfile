FROM node:19.5.0-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --no-optional --verbose

COPY . .

RUN npm run build

CMD ["npm", "start"]