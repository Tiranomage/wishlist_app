FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* tsconfig.json /app/
RUN npm ci || npm i
COPY src /app/src
COPY styles.css /app/
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html/dist
COPY index.html /usr/share/nginx/html/index.html
COPY styles.css /usr/share/nginx/html/styles.css
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
