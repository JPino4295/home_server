# Home Server Setup

A Docker-based media automation and web service deployment split into two isolated Compose environments.

---

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/) installed
* [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+) installed

---

## Architecture Overview

The system is split into two logical stacks:

1. **`contents`**: Handles media acquisition and streaming.
* **Jellyfin**: Media server for streaming movies and TV shows.
* **Flexget**: Automation tool to download and manage content.


2. **`webservices`**: Handles web traffic routing and external exposure.
* **Nginx**: Reverse proxy to manage domain routing and SSL.



---

## Configuration

Before starting the containers, create a `.env` file inside the `contents/` directory:

```bash
# contents/.env

RAW_CONTENT_URL=/path/to/host/raw_content
MOVIES_CONTENT_URL=/path/to/host/movies
SERIES_CONTENT_URL=/path/to/host/series
FLEXGET_PASSWORD=your_secure_password_here

```

### Environment Variables

| Variable | Description |
| --- | --- |
| `RAW_CONTENT_URL` | Host path for raw/incoming media |
| `MOVIES_CONTENT_URL` | Host path for processed movies |
| `SERIES_CONTENT_URL` | Host path for processed TV series |
| `FLEXGET_PASSWORD` | Password used to authenticate with the Flexget web UI |

and a `.env` file inside the `webservices/` directory:

```bash
# webservices/.env

ALUCARD_IP=1.2.3.4
TREVOR_IP=4.3.2.1

```

### Environment Variables

| Variable | Description |
| --- | --- |
| `ALUCARD_IP` | IP of the server "Alucard" |
| `TREVOR_IP` | IP of the server "Trevor" |

---

## Getting Started

### 1. Start Contents Stack

Navigate to the `contents` directory and launch the media pipeline:

```bash
cd contents
docker compose up -d

```

### 2. Start Web Services Stack

Navigate to the `webservices` directory and launch Nginx:

```bash
cd webservices
docker compose up -d

```