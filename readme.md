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
BASE_DOMAIN=example.com
FLEXGET_SUBDOMAIN=flexget
JELLYFIN_SUBDOMAIN=jelly
METUBE_SUBDOMAIN=metube
RECIPES_SUBDOMAIN=recipes
PROXMOX_SUBDOMAIN=proxmox
IMMICH_SUBDOMAIN=immich
WARDROBE_SUBDOMAIN=wardrobe
N8N_SUBDOMAIN=n8n
AUDIOBOOKS_SUBDOMAIN=audiobooks
HA_SUBDOMAIN=ha
FLEXGET_PORT=5050
JELLYFIN_PORT=8096
METUBE_PORT=8081
RECIPES_PORT=3000
PROXMOX_PORT=8006
IMMICH_PORT=2283
WARDROBE_PORT=3000
N8N_PORT=5678
AUDIOBOOKS_PORT=4040
HA_PORT=8123

```

### Environment Variables

| Variable | Description |
| --- | --- |
| `ALUCARD_IP` | IP of the server "Alucard" |
| `TREVOR_IP` | IP of the server "Trevor" |
| `BASE_DOMAIN` | Root domain the reverse proxy serves (e.g. `example.com`); also used to locate the Let's Encrypt cert directory (`/etc/letsencrypt/${BASE_DOMAIN}/...`) |
| `FLEXGET_SUBDOMAIN` | Subdomain that routes to the Flexget web UI (proxied via Alucard) |
| `JELLYFIN_SUBDOMAIN` | Subdomain that routes to Jellyfin (proxied via Trevor) |
| `METUBE_SUBDOMAIN` | Subdomain that routes to MeTube (proxied via Trevor) |
| `RECIPES_SUBDOMAIN` | Subdomain that routes to the recipes app (proxied via Trevor) |
| `PROXMOX_SUBDOMAIN` | Subdomain that routes to the Proxmox web UI (proxied via Trevor) |
| `IMMICH_SUBDOMAIN` | Subdomain that routes to Immich (proxied via Trevor) |
| `WARDROBE_SUBDOMAIN` | Subdomain that routes to the wardrobe app (proxied via Trevor) |
| `N8N_SUBDOMAIN` | Subdomain that routes to n8n (proxied via Trevor) |
| `AUDIOBOOKS_SUBDOMAIN` | Subdomain that routes to the audiobooks app (proxied via Trevor) |
| `HA_SUBDOMAIN` | Subdomain that routes to Home Assistant (proxied via Trevor) |
| `FLEXGET_PORT` | Backend port for the Flexget web UI (proxied via Alucard) |
| `JELLYFIN_PORT` | Backend port for Jellyfin (proxied via Trevor) |
| `METUBE_PORT` | Backend port for MeTube (proxied via Trevor) |
| `RECIPES_PORT` | Backend port for the recipes app (proxied via Trevor) |
| `PROXMOX_PORT` | Backend port for the Proxmox web UI (proxied via Trevor) |
| `IMMICH_PORT` | Backend port for Immich (proxied via Trevor) |
| `WARDROBE_PORT` | Backend port for the wardrobe app (proxied via Trevor) |
| `N8N_PORT` | Backend port for n8n (proxied via Trevor) |
| `AUDIOBOOKS_PORT` | Backend port for the audiobooks app (proxied via Trevor) |
| `HA_PORT` | Backend port for Home Assistant (proxied via Trevor) |

Nginx picks these up via its [templating mechanism](https://hub.docker.com/_/nginx) (`envsubst` over `/etc/nginx/templates/*.template`), so the real domain, subdomains, and backend ports never need to appear in the committed config.

> **Note:** this hides the domain/topology from the *git repo* only. Once the stack is running, the domain and subdomains are still publicly visible to anyone — via DNS lookups, or via [certificate transparency logs](https://crt.sh/) for any Let's Encrypt certificate you issue. This change protects against accidental disclosure through the repo (e.g. if it's made public or shared), not against external reconnaissance of a live service.

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