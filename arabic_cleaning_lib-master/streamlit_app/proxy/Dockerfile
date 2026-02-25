From traefik:v2.9
WORKDIR /etc/traefik/

COPY static.yaml ./static.yaml
COPY configs ./configs

RUN mkdir -p /etc/traefik/acme
