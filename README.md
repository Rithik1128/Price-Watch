# Price-Watch
A full-stack price tracking tool that lets users monitor product prices across e-commerce platforms and receive alert when prices drop. Built with React, Express, MongoDB, and a Python-based web scraper, all orchestrated using Docker containers for seamless deployment and scalability.
hu

## Configuring MongoDB

By default the scraper writes to a local MongoDB at `mongodb://localhost:27017`.

To use MongoDB Atlas, set the `MONGO_URI` environment variable to your Atlas
connection string before running the scraper. For PowerShell:

```powershell
$env:MONGO_URI = "mongodb+srv://<user>:<password>@<cluster>.mongodb.net"
python scraper\reliance-scraper.py
```

Optionally, you can put your URI into a `.env` file and load it with `python-dotenv`.