# SiteJS.py – Small Web Construction Set

SiteJS.py is a **Python‑based “Small Web” construction set** inspired by the now‑deprecated Site.js (Node.js). It gives you a zero‑configuration development server, static site generator, live reload, automatic SSL, a built‑in JSON database (JSDB), and deployment tools – all in a single, self‑contained package.

## Why SiteJS.py?

- **Zero config** – run `sitejs serve` in any folder with a `pages/` directory and it works.
- **Live reload** – file changes trigger browser refresh without WebSocket overhead.
- **Markdown + Jinja2** – full templating power for dynamic pages.
- **Built‑in JSDB** – thread‑safe JSON database with queries, indexes, and aggregation.
- **One‑command deploy** – to rsync, FTP, S3, or SFTP.
- **Extensible** – plugin system with hook registration.
- **Asset pipeline** – minify CSS/JS and optimise images (PIL).
- **Production ready for development** – for high traffic, front with nginx or Caddy.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Purrple-hub/SiteJS.git
cd SiteJS

# Install the package
pip install .

# Create a new site skeleton
sitejs new mysite
cd mysite

# Start the development server
sitejs serve

# Build static output
sitejs build

# Deploy to your target (rsync, FTP, S3, SFTP)
sitejs deploy --target rsync --destination user@host:/path
