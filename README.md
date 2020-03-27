# TODO
* check init db that doesn't work
* develop default UI

# covid19-people-counter-system
covid19-people-counter-system comes to share queue length or simply count people outside markets/shop to citizens.

This system analize images from city cameras, count people inside them, and show a real-time user interface.

City cameras generally already exists or come from new installations by covid emergency.

GIF Example\
TODO

# Requirements
Hardware
* cameras with internet access (es. URL/IP)
* server with at least 2G of RAM

Software
* Docker

# Configs steps
* 1. set up cameras urls/ips
* 2. set up frequence
* 3. set up custom UI (optional)


# 1. set up cameras urls/ips
`config.json` contains all cameras that covid19-people-counter-system has to contact to get fresh frames.\
Urls can be also IPs.\
* url -> URL or IP of a camera (es. https://someserver.com/mycamera)
* code -> unique code of the camera, it must be lowercase alphanumeric (underscore acceptes) (es. carrefour_1)
* description -> short description of a camera (es. "Carrefour in front of the stadium")

(optional) At runtime the above variables are replaced in "url":
* [YYYY] -> year with century as a decimal number (es. 2020)
* [MM] -> Minute as a decimal number [00,59].
* [DD] -> Day of the month as a decimal number [01,31].
* [HH] -> Hour (24-hour clock) as a decimal number [00,23].
* [mm] -> Month as a decimal number [01,12].

So an url like:

```
[
    {
        "url": "https://someserver.com/YYYY/MM/DD/HH/mm",
        "code": "carrefour_1",
        "description": "Carrefour in front of the stadium"
    }
]
```

at runtime will be `https://someserver.com/2020/03/27/09/10`.\
The timezone is set by TZ env variable of "cron" in docker-compose.

# 2. set up frequence
How much you want the data to be fresh?\
FREQUENCE_MINUTES env variable set it.\
For example FREQUENCE_MINUTES=5 says to covid19-people-counter-system to get fresh images every 5 minutes from every images configured in config.json.

# 3. set up custom UI
TODO

