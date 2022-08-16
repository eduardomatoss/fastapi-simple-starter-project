#!/bin/bash
#
# Simple script to run the database migrations.
#
# This script uses some env vars:
#
# env.VERSION: Image tag that will be used to run the migrations
# env.DATABASE_URL: The url of the database server
# env.DATABASE_NAME: The name of the database
# env.DATABASE_PORT: The port to connect to the database
# env.DATABASE_USER : The user, of course
# env.DATABASE_PASSWORD: The password, of course
#
# Usage:
# export the env vars before
# sh ./.deploy/migrations.sh

if [[ "$VERSION" && "$DATABASE_URL" && "$DATABASE_NAME" && "$DATABASE_PORT" && "$DATABASE_USER" && "$DATABASE_PASSWORD" ]]; then
  docker run --rm --network=host \
      --env DATABASE_URL=$DATABASE_URL \
      --env DATABASE_NAME=$DATABASE_NAME \
      --env DATABASE_PORT=$DATABASE_PORT \
      --env DATABASE_USER=$DATABASE_USER \
      --env DATABASE_PASSWORD=$DATABASE_PASSWORD \
      "eduardomatoss/fastapi-simple-starter-project:${VERSION}" "alembic" "upgrade" "head"
else
  echo "Missing values! You must define these env vars: VERSION, DATABASE_URL, DATABASE_NAME, DATABASE_PORT, DATABASE_USER and DATABASE_PASSWORD!"
  exit 1
fi
