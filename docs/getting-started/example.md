# Start an example

```bash
# To build the docker images
make build
# To initialize airflow and create `./etc/settings.env` and `./etc/settings.airflow.env`
make init-example
# To close the services started during initialization
make down

# To start the services
make up
```
