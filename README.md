# Disaster Evacuation Mapping

A cloud-native, real-time disaster management and evacuation mapping platform that visualizes active hazard zones and computes optimal evacuation routes to the nearest safe zone. Conceived in the spirit of **防災 (bōsai)** — the Japanese philosophy of disaster prevention and preparedness — this project explores how geospatial tooling can support faster, more informed emergency response in disaster-prone regions such as Japan and India.

**Live demo:** https://eshan3160.github.io/disaster-mapping/frontend/index.html

## Overview

The application ingests disaster reports (type, location, severity) and renders them on an interactive map, color-coded by hazard category. Upon request, it identifies the nearest designated safe zone and generates a navigable evacuation route in real time — condensing what would otherwise be a manual, error-prone process into a single, immediate visualization.

## Features

- **Color-coded hazard markers** distinguishing disaster types (flood, fire, earthquake) at a glance
- **Location data grounded in real hazard research** — disaster zones and evacuation sites correspond to documented, real-world risk areas in Tokyo (e.g. Edogawa's flood-prone lowlands, Sumida's dense wooden-housing fire risk, Koto's reclaimed-land liquefaction risk)

- **Full CRUD functionality** — disasters can be reported, amended, or resolved directly through the interface
- **Live data synchronization** between the client and the backend
- **Automated evacuation routing** — calculates the nearest safe zone and renders the corresponding road route
- **End-to-end cloud deployment** — no local setup required to view or interact with the live application

## Architecture & Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, PostgreSQL (hosted on Neon) |
| Frontend | HTML, CSS, JavaScript, [Leaflet.js](https://leafletjs.com/) |
| Routing | [Leaflet Routing Machine](https://www.liedman.net/leaflet-routing-machine/) |
| Hosting | Backend on [Render](https://render.com/); frontend on GitHub Pages |

## System Design

1. **Data layer** — A FastAPI backend persists disaster records in a PostgreSQL database (hosted on Neon for permanent,long-ter, availability) and exposes a RESTful interface for create, read, update, and delete operations.
2. **Presentation layer** — The frontend retrieves this data asynchronously and renders it on a Leaflet.js map, with markers styled according to disaster classification.
3. **Routing logic** — A dedicated `/nearest-safe-zone` endpoint evaluates proximity to predefined safe zones and returns the optimal candidate.
4. **Visualization** — Leaflet Routing Machine renders the resulting evacuation path as a navigable route overlaid on the map.

## Running Locally

```bash
# Backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
# Open frontend/index.html directly in a browser
```
## Motivation
This project was undertaken as a deliberate step toward disaster-response engineering, with particular interest in Japan's advanced 防災 (bōsai) infrastructure and its emphasis on preparedness, rapid response, and public safety technology. It reflects an intent to contribute meaningfully to disaster mitigation efforts through applied software engineering.
