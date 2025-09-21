# Node.js v 14
FROM node:14
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --only=production
COPY . .
CMD ["node", "app.js", "agent/"]