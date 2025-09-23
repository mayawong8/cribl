# Node.js v 14 as the base image
FROM node:14
# Set working directory inside the container
WORKDIR /app
# Copy dependencies manifests
COPY package.json package-lock.json ./
# Install dependencies from above files
RUN npm install --only=production
# Copy assignment code into the container
COPY . .
# Run assignment with Node.js, passing app,js  and /agent as arguments
CMD ["node", "app.js", "agent/"]