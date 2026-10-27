FROM node:22-alpine AS build

WORKDIR /app

COPY frontend/frontend/package*.json ./
RUN npm ci

COPY frontend/frontend/ ./
RUN npm run build

FROM node:22-alpine AS runtime

WORKDIR /app
ENV NODE_ENV=production
ENV PORT=4000

COPY --from=build /app/dist ./dist

EXPOSE 4000

CMD ["node", "dist/frontend/server/server.mjs"]