# Manual de usuario — Wireless HeatMapper

SPA estatica del manual de usuario, basada en las funcionalidades implementadas
en la web, app movil y backend del repositorio.

## Ejecucion local

```bash
python3 -m http.server 4174 --directory manual-usuario
```

Abrir `http://localhost:4174`.

## Contenedor para Azure

```bash
docker build -t wireless-heatmapper-manual:latest manual-usuario
docker run --rm -p 8081:80 wireless-heatmapper-manual:latest
```

Para desplegarlo en un dominio distinto, publicar este contenedor como Azure Web
App independiente o conectarlo a un host separado en el reverse proxy.
