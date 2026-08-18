Here is your **full README.md** (with a new FAQ section) and a **fresh MIT LICENSE** – both as plain Markdown text you can copy directly into your repository files. No code fences needed unless you want them; I'm giving you the raw text blocks.

---

## README.md

```markdown
# SiteJS.py – Small Web Construction Set

SiteJS.py is a Python‑based “Small Web” construction set inspired by the now‑deprecated Site.js (Node.js). It gives you a zero‑configuration development server, static site generator, live reload, automatic SSL, a built‑in JSON database (JSDB), and deployment tools – all in a single, self‑contained package.

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
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `sitejs new <name>` | Scaffold a new site with default folders |
| `sitejs serve`     | Start development server with live reload |
| `sitejs build`     | Generate static site into `dist/` |
| `sitejs deploy`    | Deploy `dist/` to configured remote |
| `sitejs db`        | Interactive database shell for JSDB |

---

## Architecture

```
CLI (argparse)
  → Core Services (Config, Logger, PluginManager, RateLimiter, SessionStore)
    → Business Logic (Builder, Server, Watcher, AssetManager, Deployer, DB)
      → File System (pages/, public/, templates/, data/, dist/, logs/)
```

---

## What’s Inside

- **HTTP/HTTPS server** with self‑signed SSL (via `cryptography`)
- **Markdown → HTML** rendering (via `markdown` + `jinja2`)
- **Live reload** (polling or `watchdog`‑based, `/__version` endpoint)
- **JSDB** – thread‑safe JSON database with indexes, queries, aggregation
- **Static build** – exports pages, assets, sitemap, RSS, optional search index
- **Deploy backends** – rsync, FTP, S3, SFTP
- **Asset minification** (CSS/JS) and image optimisation (PIL)
- **Plugin system** with hook registration
- **Rate limiting** and **session store** for future extensibility

---

## FAQ

**Q: How do I customise the port?**  
A: Pass `--port 8080` to `serve`, or set `port = 8080` in `sitejs.toml`.

**Q: Can I use a real SSL certificate?**  
A: Yes. Place your `cert.pem` and `key.pem` in the project root; the server will use them instead of the self‑signed ones.

**Q: Does the live reload work with remote devices?**  
A: Yes, if you serve on `0.0.0.0` (use `--host 0.0.0.0`) and access via your LAN IP, the reload script works over the network.

**Q: How do I add my own plugins?**  
A: Create a Python file in `plugins/` that registers hooks via `sitejs.plugin_manager.register()`. See the built‑in plugins for examples.

**Q: Is there a way to exclude certain files from the build?**  
A: Yes, add an `exclude` array in `sitejs.toml` with glob patterns (e.g., `["**/draft-*"]`).

**Q: What happens to the database when I build?**  
A: The build process does not touch the `data/` folder – it only copies static assets and renders pages. The DB is for runtime use only; you can also include a snapshot in the build by writing a plugin.

**Q: Can I deploy only some pages?**  
A: Not directly – deploy always pushes the whole `dist/` folder. Use `--dry-run` to see what would be transferred.

**Q: How do I update SiteJS.py?**  
A: `git pull` and `pip install . --upgrade` inside the repository.

**Q: Does it work on Windows?**  
A: Yes, the code is cross‑platform. The watcher uses polling if `watchdog` is not available, so it runs everywhere.

**Q: Is there a way to serve dynamic routes (not just pages)?**  
A: The current version is static‑first. For dynamic endpoints, you can extend the server with plugins that add routes via `@app.route()` – see the plugin API.

---

## Testing

The included `TestSiteJS.py` runs **60+ pytest tests** covering:

- All database operations (set, get, delete, query, aggregate, find, push/pop)
- Configuration loading (defaults, TOML, environment)
- Builder rendering (Markdown + Jinja2)
- Server routing, static files, version endpoint, SSL fallback
- Watcher (polling) change detection
- CLI commands (new, build, db)
- Asset minification, image optimisation
- Rate limiter and session store
- Plugin manager and deployer (mocked)
- Integration test (new → build → serve)

Run the suite with:

```bash
pytest TestSiteJS.py -v
```

---

## Status

- Code is **complete** and executable.
- Test suite is **ready** to validate every module.
- Package installs via `pip install .` (uses `pyproject.toml`).
- **Production‑ready for development use**; for high‑traffic production, front with nginx/caddy.

---

## Contributing

Issues and pull requests are welcome. Please ensure all tests pass and add new tests for any changed functionality.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

**Bottom line:** SiteJS.py is a complete, modern, Python‑based Small Web tool that fills the gap left by Site.js. It is well‑tested, extensible, and ready for you to clone, run, and build your own sites.
```

---

## LICENSE (MIT)

```text
MIT License

Copyright (c) 2026 Purrple-hub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---
## TECHNICAL EXPLANATION

The README guides users through installation, usage, and internals, while the FAQ addresses practical concerns; the LICENSE provides permissive open‑source terms. Both files are ready to commit.
