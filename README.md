# chip.de scraper

this script scrapes all recent articles from [chip.de](www.chip.de) and saves them to a folder. it will sort them by their date.  
the articles will be saved as raw `.html` files.

### folder structure

```
- 2019
-- 01
--- 01
--- 02
--- 03
--- ...
-- 02
--- 01
--- 02
--- 03
--- ...
-- 03
--- 01
--- 02
--- 03
--- ...
...

```

### example docker-compose

```docker-compose
version: '3'
services:
  chip:
    image: felixbreuer/chip.de-scrape
    restart: unless-stopped
    volumes:
      - ./data:/usr/app/chip.de
```

## links

- [dockerhub](https://hub.docker.com/repository/docker/felixbreuer/chip.de-scrape)
