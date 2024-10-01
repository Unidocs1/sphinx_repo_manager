# Docker Images for XBE Docs

## Contents

[TOC]

## Environment Configuration

The following environment variables can be set in runtime enviromnet, or in the [`docker/.env`](.env) file:

| Variable            | Description                                             | Default         |
|---------------------|---------------------------------------------------------|-----------------|
| `FROM_IMAGE`        | Set the base image.                                      | `ubuntu:22.04`  |
| `COMPOSE_PROJECT_NAME` | Set to a specific name.                                | `xbe-docs`      |
| `NAME`              | Set to a specific image name prefix.                     | `xbe/docs`      |
| `TAG`               | Set to a specific image tag.                             | `latest`        |
| `WORK_DIR`          | Set the builder root project directory.                  | `/app`          |
| `BASE_DIR`          | Set the host root project directory for the `base` image.| `.`             |
| `BASE_DIR_SPHINX`   | Set the host root project directory for the `sphinx` image.| `.`             |

## Dockerfiles

### [`docker/Dockerfile.base`](Dockerfile.base)

- Base image with several development tools and Python `3.10` installed.
- `extensions` folder added to the working directory: `/app/docs`

### [`docker/Dockerfile.sphinx`](Dockerfile.sphinx)

- Sphinx builder image based on the `base` image.
- `docs` folder added to the working directory: `/app/docs`
- `make install` command executed to install the requirements

## Docker Scripts

### Build Base Images with  [`docker/docker-compose.base.yaml`](docker-compose.base.yaml)

- Generates the following images
  - `xbe/docs/base` | The base image with ubuntu and python 3.10, extensions folder added.
  - `xbe/docs/sphinx` | Based on `base` image. The `docs` folder is added to `/app/docs` and requirements installed.
  - `xbe/docs/doxygen` | Based on `base` image. The `tools/template-doxygen` folder is added to `/app` and doxygen is installed.
  - `xbe/docs/doxygen-sphinx` | Based on `doxygen` image. The `docs` folder is added to `/app/docs` and requirements installed.

```bash
docker compose -f docker/docker-compose.base.yaml build
```

### Build Main HTML [`docker/docker-compose.main.yaml`](docker-compose.main.yaml)

- Compose run to generate html files from the `docs` folder:

```bash
docker compose -f docker/docker-compose.main.yaml run --rm -main
```
