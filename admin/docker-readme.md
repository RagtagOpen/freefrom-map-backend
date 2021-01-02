This is a modified template based on [this tutorial](https://kb.objectrocket.com/postgresql/create-a-postgresql-docker-container-975). I am assuming you have `docker` and `docker-compose` installed.

NOTE: All these commands may require `sudo` depending on your docker user settings

To get the `docker` `postgres` image:

```bash

docker pull postgres
```

To start the database image:

```bash

docker-compose up
```

The image should be ready to accept connections. To log into the database:

```bash

psql -U freefrom_map_user  -h localhost -d freefrom_map_dev
```

