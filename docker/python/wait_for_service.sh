#! /usr/bin/env bash

# Let the DB start
echo "<==============================>"
echo "     Waiting for Postgres     "
echo "<==============================>"

while ! nc -z postgres 5432; do
  sleep 10
done

echo "<==============================>"
echo "     PostgreSQL started     "
echo "<==============================>"