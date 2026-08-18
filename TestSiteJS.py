import pytest
import json
import os
import shutil
import tempfile
import time
import threading
import subprocess
import sys
import signal
import socket
import ssl
import urllib.request
import urllib.error
from unittest.mock import Mock, patch, MagicMock
from contextlib import contextmanager

try:
    import requests
except ImportError:
    requests = None

try:
    import markdown
except ImportError:
    markdown = None

try:
    import jinja2
except ImportError:
    jinja2 = None

try:
    import cryptography
except ImportError:
    cryptography = None

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from sitejs import SiteJS, SiteJSConfig, SiteJSLogger, JSDB, PluginManager
    from sitejs import SiteJSServer, SiteJSBuilder, PollingWatcher, WatchdogWatcher
    from sitejs import AssetManager, Deployer, RateLimiter, SessionStore
    from sitejs import cli_new, cli_serve, cli_build, cli_deploy, cli_db
    from sitejs import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_SSL, DEFAULT_WATCH
    from sitejs import DEFAULT_RELOAD, DEFAULT_POLL_INTERVAL, DEFAULT_RELOAD_TYPE
    from sitejs import PAGES_DIR, PUBLIC_DIR, TEMPLATES_DIR, DATA_DIR, DB_PATH
    from sitejs import DIST_DIR, PLUGINS_DIR, LOGS_DIR, CONFIG_PATH
    from sitejs import CERT_DIR, DEFAULT_CERT, DEFAULT_KEY
    from sitejs import DEFAULT_TEMPLATE, DEFAULT_CSS, DEFAULT_RELOAD_JS, DEFAULT_404, DEFAULT_500
except ImportError:
    pytest.skip("sitejs module not available", allow_module_level=True)

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        old_cwd = os.getcwd()
        os.chdir(tmp)
        yield tmp
        os.chdir(old_cwd)

@pytest.fixture
def config(temp_dir):
    return SiteJSConfig({
        "host": "127.0.0.1",
        "port": 8443,
        "ssl": False,
        "watch": False,
        "reload": False,
        "poll_interval": 0.1,
        "reload_type": "poll",
        "pages_dir": os.path.join(temp_dir, "pages"),
        "public_dir": os.path.join(temp_dir, "public"),
        "templates_dir": os.path.join(temp_dir, "templates"),
        "data_dir": os.path.join(temp_dir, "data"),
        "db_path": os.path.join(temp_dir, "data", "db.json"),
        "dist_dir": os.path.join(temp_dir, "dist"),
        "plugins_dir": os.path.join(temp_dir, "plugins"),
        "logs_dir": os.path.join(temp_dir, "logs"),
        "cert_dir": os.path.join(temp_dir, "certs"),
        "log_level": "ERROR",
        "log_file": os.path.join(temp_dir, "logs", "sitejs.log"),
    })

@pytest.fixture
def db(config):
    return JSDB(config.get("db_path"))

@pytest.fixture
def logger(config):
    return SiteJSLogger(config.get("log_level"), config.get("log_file"))

@pytest.fixture
def builder(config, logger, db):
    return SiteJSBuilder(config, logger, db)

@pytest.fixture
def plugin_manager(config, logger):
    return PluginManager(config, logger)

@pytest.fixture
def asset_manager(config, logger):
    return AssetManager(config, logger)

@pytest.fixture
def deployer(config, logger):
    return Deployer(config, logger)

@pytest.fixture
def rate_limiter():
    return RateLimiter(limit=5, window=10)

@pytest.fixture
def session_store():
    return SessionStore("test_secret_32_bytes_long_xxxxxxxxxxxxxx", timeout=3600)

@pytest.fixture
def server_instance(config, logger, db, plugin_manager, asset_manager):
    watcher = PollingWatcher(
        [config.get("pages_dir"), config.get("public_dir"), config.get("templates_dir")],
        lambda: None,
        config.get("poll_interval"),
        logger
    )
    server = SiteJSServer(config, logger, db, watcher)
    return server

@pytest.fixture
def http_client():
    if requests is None:
        pytest.skip("requests not installed")
    session = requests.Session()
    session.verify = False
    session.timeout = 5
    return session

class TestJSDB:
    def test_set_get(self, db):
        db.set("key", {"value": 123})
        assert db.get("key") == {"value": 123}

    def test_delete(self, db):
        db.set("key", "value")
        assert db.delete("key") is True
        assert db.get("key") is None
        assert db.delete("nonexistent") is False

    def test_all_keys_values_items(self, db):
        db.set("a", 1)
        db.set("b", 2)
        assert set(db.keys()) == {"a", "b"}
        assert set(db.values()) == {1, 2}
        assert set(db.items()) == {("a", 1), ("b", 2)}

    def test_query_index(self, db):
        db.set("user1", {"role": "admin", "active": True})
        db.set("user2", {"role": "user", "active": True})
        db.set("user3", {"role": "admin", "active": False})
        results = db.query("role", "admin")
        assert len(results) == 2
        keys = [r[0] for r in results]
        assert "user1" in keys
        assert "user3" in keys
        results_active = db.query("active", True)
        assert len(results_active) == 2

    def test_update(self, db):
        db.set("obj", {"x": 1, "y": 2})
        assert db.update("obj", {"y": 99, "z": 100}) is True
        assert db.get("obj") == {"x": 1, "y": 99, "z": 100}
        assert db.update("missing", {}) is False

    def test_increment(self, db):
        db.set("counter", {"count": 10})
        assert db.increment("counter", "count", 5) is True
        assert db.get("counter")["count"] == 15
        assert db.increment("counter", "newfield", 3) is True
        assert db.get("counter")["newfield"] == 3
        assert db.increment("missing", "x") is False

    def test_push_pop(self, db):
        db.set("arr", {"items": []})
        assert db.push("arr", "items", "a") is True
        assert db.push("arr", "items", "b") is True
        assert db.get("arr")["items"] == ["a", "b"]
        assert db.pop("arr", "items") == "b"
        assert db.get("arr")["items"] == ["a"]
        assert db.pop("arr", "nonexistent") is None
        assert db.push("missing", "list", 1) is False

    def test_find(self, db):
        db.set("a", {"score": 10, "name": "alice"})
        db.set("b", {"score": 20, "name": "bob"})
        db.set("c", {"score": 10, "name": "charlie"})
        results = db.find(lambda k, v: v.get("score") == 10)
        assert len(results) == 2
        keys = [r[0] for r in results]
        assert "a" in keys and "c" in keys

    def test_aggregate_group_sum(self, db):
        db.set("a", {"score": 10, "team": "alpha"})
        db.set("b", {"score": 20, "team": "alpha"})
        db.set("c", {"score": 30, "team": "beta"})
        result = db.aggregate([
            {"group": {"by": ["team"], "sum": {"total": "score"}}}
        ])
        assert len(result) == 2
        for item in result:
            if item["_id"] == ("alpha",):
                assert item["total"] == 30
            elif item["_id"] == ("beta",):
                assert item["total"] == 30

    def test_aggregate_filter_sort_limit(self, db):
        db.set("a", {"value": 5})
        db.set("b", {"value": 3})
        db.set("c", {"value": 8})
        db.set("d", {"value": 1})
        result = db.aggregate([
            {"filter": {"value": {"$gt": 2}}},
            {"sort": "value"},
            {"limit": 2}
        ])
        assert result == [{"value": 3}, {"value": 5}]

class TestSiteJSConfig:
    def test_default_values(self):
        config = SiteJSConfig()
        assert config.get("host") == DEFAULT_HOST
        assert config.get("port") == DEFAULT_PORT
        assert config.get("ssl") == DEFAULT_SSL
        assert config.get("watch") == DEFAULT_WATCH
        assert config.get("reload") == DEFAULT_RELOAD

    def test_update_and_get(self):
        config = SiteJSConfig()
        config.set("custom", "value")
        assert config.get("custom") == "value"
        config.update({"a": 1, "b": 2})
        assert config.get("a") == 1
        assert config.get("b") == 2

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("SITEJS_PORT", "9999")
        monkeypatch.setenv("SITEJS_SSL", "false")
        config = SiteJSConfig()
        assert config.get("port") == 9999
        assert config.get("ssl") is False

    def test_toml_load(self, temp_dir, monkeypatch):
        if toml is None:
            pytest.skip("toml not installed")
        toml_path = os.path.join(temp_dir, "sitejs.toml")
        with open(toml_path, "w") as f:
            f.write('port = 8080\nhost = "0.0.0.0"')
        config = SiteJSConfig(config_file=toml_path)
        assert config.get("port") == 8080
        assert config.get("host") == "0.0.0.0"

    def test_to_dict(self):
        config = SiteJSConfig({"x": 1})
        d = config.to_dict()
        assert d["x"] == 1
        assert "host" in d

class TestSiteJSLogger:
    def test_logger_creation(self, temp_dir):
        log_file = os.path.join(temp_dir, "test.log")
        logger = SiteJSLogger("DEBUG", log_file)
        logger.info("test message")
        assert os.path.exists(log_file)
        with open(log_file, "r") as f:
            content = f.read()
            assert "test message" in content

    def test_log_levels(self, temp_dir):
        logger = SiteJSLogger("ERROR", None)
        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")
        assert logger.logger.level == logging.ERROR

class TestPollingWatcher:
    def test_watcher_detects_change(self, temp_dir, config, logger):
        callback_called = [False]
        def callback():
            callback_called[0] = True
        watch_dir = os.path.join(temp_dir, "watch")
        os.makedirs(watch_dir, exist_ok=True)
        watcher = PollingWatcher([watch_dir], callback, 0.05, logger)
        watcher.start()
        time.sleep(0.1)
        with open(os.path.join(watch_dir, "test.txt"), "w") as f:
            f.write("change")
        time.sleep(0.2)
        watcher.stop()
        assert callback_called[0]

    def test_watcher_stop(self, temp_dir, logger):
        watcher = PollingWatcher([temp_dir], lambda: None, 0.1, logger)
        watcher.start()
        time.sleep(0.05)
        watcher.stop()
        assert not watcher.running

class TestSiteJSBuilder:
    def test_render_markdown_simple(self, config, logger, db, temp_dir):
        pages = config.get("pages_dir")
        os.makedirs(pages, exist_ok=True)
        md_path = os.path.join(pages, "test.md")
        with open(md_path, "w") as f:
            f.write("# Title\n\nParagraph.")
        builder = SiteJSBuilder(config, logger, db)
        html = builder.render_page(md_path)
        assert "<h1>Title</h1>" in html
        assert "<p>Paragraph.</p>" in html
        assert "SiteJS" in html

    def test_render_with_context(self, config, logger, db, temp_dir):
        pages = config.get("pages_dir")
        os.makedirs(pages, exist_ok=True)
        md_path = os.path.join(pages, "ctx.md")
        with open(md_path, "w") as f:
            f.write("Hello {{ extra }}")
        builder = SiteJSBuilder(config, logger, db)
        html = builder.render_page(md_path, {"extra": "World"})
        assert "Hello World" in html

    def test_build_all_creates_sitemap_rss(self, config, logger, db, temp_dir):
        pages = config.get("pages_dir")
        os.makedirs(pages, exist_ok=True)
        with open(os.path.join(pages, "index.md"), "w") as f:
            f.write("# Home")
        with open(os.path.join(pages, "about.md"), "w") as f:
            f.write("# About")
        builder = SiteJSBuilder(config, logger, db)
        output = os.path.join(temp_dir, "build_output")
        builder.build_all(output)
        assert os.path.exists(os.path.join(output, "index.html"))
        assert os.path.exists(os.path.join(output, "about.html"))
        assert os.path.exists(os.path.join(output, "sitemap.xml"))
        assert os.path.exists(os.path.join(output, "feed.xml"))
        with open(os.path.join(output, "sitemap.xml"), "r") as f:
            content = f.read()
            assert "about.html" in content
            assert "index.html" in content

    def test_build_with_assets(self, config, logger, db, temp_dir):
        public = config.get("public_dir")
        os.makedirs(public, exist_ok=True)
        with open(os.path.join(public, "style.css"), "w") as f:
            f.write("body { color: red; }")
        pages = config.get("pages_dir")
        os.makedirs(pages, exist_ok=True)
        with open(os.path.join(pages, "index.md"), "w") as f:
            f.write("# Home")
        builder = SiteJSBuilder(config, logger, db)
        output = os.path.join(temp_dir, "build_assets")
        builder.build_all(output)
        assert os.path.exists(os.path.join(output, "style.css"))

class TestSiteJSServer:
    def test_version_endpoint(self, server_instance, http_client):
        server_thread = threading.Thread(target=server_instance.start, daemon=True)
        server_thread.start()
        time.sleep(0.5)
        try:
            resp = http_client.get("http://127.0.0.1:8443/__version")
            assert resp.status_code == 200
            assert resp.text == "0"
        finally:
            server_instance.stop()
            server_thread.join(timeout=1)

    def test_static_file_serving(self, server_instance, http_client, temp_dir):
        public = server_instance.config.get("public_dir")
        os.makedirs(public, exist_ok=True)
        with open(os.path.join(public, "test.txt"), "w") as f:
            f.write("static content")
        server_thread = threading.Thread(target=server_instance.start, daemon=True)
        server_thread.start()
        time.sleep(0.5)
        try:
            resp = http_client.get("http://127.0.0.1:8443/test.txt")
            assert resp.status_code == 200
            assert resp.text == "static content"
        finally:
            server_instance.stop()
            server_thread.join(timeout=1)

    def test_markdown_route(self, server_instance, http_client, temp_dir):
        pages = server_instance.config.get("pages_dir")
        os.makedirs(pages, exist_ok=True)
        with open(os.path.join(pages, "hello.md"), "w") as f:
            f.write("# Hello\n\nWorld.")
        server_thread = threading.Thread(target=server_instance.start, daemon=True)
        server_thread.start()
        time.sleep(0.5)
        try:
            resp = http_client.get("http://127.0.0.1:8443/hello.md")
            assert resp.status_code == 200
            assert "<h1>Hello</h1>" in resp.text
            assert "World." in resp.text
        finally:
            server_instance.stop()
            server_thread.join(timeout=1)

    def test_404_not_found(self, server_instance, http_client):
        server_thread = threading.Thread(target=server_instance.start, daemon=True)
        server_thread.start()
        time.sleep(0.5)
        try:
            resp = http_client.get("http://127.0.0.1:8443/nonexistent")
            assert resp.status_code == 404
        finally:
            server_instance.stop()
            server_thread.join(timeout=1)

    def test_reload_increments_version(self, server_instance):
        version0 = server_instance.version
        server_instance.reload()
        assert server_instance.version == version0 + 1
        server_instance.reload()
        assert server_instance.version == version0 + 2

    def test_ssl_context_creation(self, config, logger, db):
        if cryptography is None:
            pytest.skip("cryptography not installed")
        config.set("ssl", True)
        config.set("cert_dir", os.path.join(tempfile.mkdtemp(), "certs"))
        server = SiteJSServer(config, logger, db, None)
        server._setup_ssl()
        assert server.use_ssl is True

class TestAssetManager:
    def test_minify_css(self, asset_manager):
        css = "body { color: red; }"
        if cssmin:
            result = asset_manager.minify_css(css)
            assert "body{color:red}" in result
        else:
            assert asset_manager.minify_css(css) == css

    def test_minify_js(self, asset_manager):
        js = "var x = 1; var y = 2;"
        if jsmin:
            result = asset_manager.minify_js(js)
            assert "var x=1;var y=2;" in result
        else:
            assert asset_manager.minify_js(js) == js

    def test_optimize_image(self, asset_manager, temp_dir):
        if Image is None:
            pytest.skip("PIL not installed")
        img_path = os.path.join(temp_dir, "test.jpg")
        img = Image.new("RGB", (10, 10), color="red")
        img.save(img_path, "JPEG")
        result = asset_manager.optimize_image(img_path, quality=50)
        assert result is True
        assert os.path.getsize(img_path) > 0

    def test_process_assets(self, asset_manager, temp_dir):
        public = os.path.join(temp_dir, "public")
        os.makedirs(public, exist_ok=True)
        with open(os.path.join(public, "test.css"), "w") as f:
            f.write("body { color: blue; }")
        output = os.path.join(temp_dir, "dist")
        asset_manager.config.set("minify_css", True)
        asset_manager.process_assets(public, output)
        assert os.path.exists(os.path.join(output, "test.css"))

class TestRateLimiter:
    def test_is_allowed_within_limit(self, rate_limiter):
        key = "user1"
        for _ in range(5):
            assert rate_limiter.is_allowed(key) is True
        assert rate_limiter.is_allowed(key) is False

    def test_reset(self, rate_limiter):
        key = "user1"
        for _ in range(5):
            rate_limiter.is_allowed(key)
        rate_limiter.reset(key)
        assert rate_limiter.is_allowed(key) is True

class TestSessionStore:
    def test_create_and_get(self, session_store):
        sid = session_store.create({"user": "alice"})
        sess = session_store.get(sid)
        assert sess is not None
        assert sess["data"]["user"] == "alice"
        assert "created" in sess
        assert "last_access" in sess

    def test_get_nonexistent(self, session_store):
        assert session_store.get("invalid") is None

    def test_timeout_expiry(self, session_store):
        session_store.timeout = 1
        sid = session_store.create()
        time.sleep(1.5)
        assert session_store.get(sid) is None

class TestPluginManager:
    def test_load_plugin(self, plugin_manager, temp_dir):
        plugin_path = os.path.join(temp_dir, "dummy_plugin.py")
        with open(plugin_path, "w") as f:
            f.write("def setup(config, logger):\n    logger.info('plugin loaded')")
        result = plugin_manager.load_plugin("dummy", plugin_path)
        assert result is True
        assert "dummy" in plugin_manager.plugins

    def test_register_and_run_hook(self, plugin_manager):
        called = [False]
        def callback(x):
            called[0] = True
            return x * 2
        plugin_manager.register_hook("test_hook", callback)
        results = plugin_manager.run_hook("test_hook", 5)
        assert results == [10]
        assert called[0] is True

class TestDeployer:
    def test_deploy_rsync(self, deployer, temp_dir):
        deployer.config.set("deploy_method", "rsync")
        deployer.config.set("deploy_target", "/dev/null")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(returncode=0)
            result = deployer.deploy(temp_dir)
            assert result is True
            mock_run.assert_called_once()

    def test_deploy_ftp_missing_target(self, deployer):
        deployer.config.set("deploy_method", "ftp")
        deployer.config.set("deploy_target", "")
        result = deployer.deploy()
        assert result is False

    def test_deploy_s3_missing_boto3(self, deployer):
        if boto3 is None:
            deployer.config.set("deploy_method", "s3")
            deployer.config.set("deploy_target", "s3://bucket/prefix")
            result = deployer.deploy()
            assert result is False

class TestCLI:
    def test_cli_new(self, temp_dir):
        cli_new("mynewsite")
        assert os.path.exists("mynewsite/pages/index.md")
        assert os.path.exists("mynewsite/public/style.css")
        assert os.path.exists("mynewsite/templates/page.html")
        assert os.path.exists("mynewsite/data/db.json")

    def test_cli_build(self, temp_dir, config):
        pages = config.get("pages_dir")
        os.makedirs(pages, exist_ok=True)
        with open(os.path.join(pages, "index.md"), "w") as f:
            f.write("# Build Test")
        dist = os.path.join(temp_dir, "mybuild")
        cli_build(dist)
        assert os.path.exists(os.path.join(dist, "index.html"))
        assert "<h1>Build Test</h1>" in open(os.path.join(dist, "index.html")).read()

    def test_cli_db_get_set_delete(self, temp_dir, config, monkeypatch):
        monkeypatch.setenv("SITEJS_DB_PATH", config.get("db_path"))
        cli_db("set", "testkey", '{"value": 42}')
        cli_db("get", "testkey", None)
        # Capture stdout? Not easily without mocking, but we can test file existence
        db = JSDB(config.get("db_path"))
        assert db.get("testkey") == {"value": 42}
        cli_db("delete", "testkey", None)
        assert db.get("testkey") is None
        cli_db("all", None, None)

    def test_cli_serve_starts_server(self, temp_dir, config, monkeypatch):
        monkeypatch.setenv("SITEJS_PORT", "8444")
        monkeypatch.setenv("SITEJS_SSL", "false")
        monkeypatch.setenv("SITEJS_WATCH", "false")
        pages = config.get("pages_dir")
        os.makedirs(pages, exist_ok=True)
        with open(os.path.join(pages, "index.md"), "w") as f:
            f.write("# Serve Test")
        import threading
        def run_serve():
            cli_serve("127.0.0.1", 8444, True, True)
        thread = threading.Thread(target=run_serve, daemon=True)
        thread.start()
        time.sleep(1)
        try:
            if requests:
                resp = requests.get("http://127.0.0.1:8444/__version", timeout=2)
                assert resp.status_code == 200
        finally:
            # Need to stop server gracefully - we can send SIGINT to thread? Simpler: kill the process.
            # For test, we just rely on daemon thread ending.
            pass

class TestIntegration:
    def test_full_workflow_new_build_serve(self, temp_dir):
        import subprocess
        import requests
        # Create new site
        cli_new("fullsite")
        os.chdir("fullsite")
        # Build
        cli_build("dist")
        assert os.path.exists("dist/index.html")
        # Serve (in separate thread)
        from sitejs.cli import cli_serve
        import threading
        def serve():
            cli_serve("127.0.0.1", 8445, True, True)
        thread = threading.Thread(target=serve, daemon=True)
        thread.start()
        time.sleep(1.5)
        try:
            resp = requests.get("http://127.0.0.1:8445/__version", timeout=2)
            assert resp.status_code == 200
            resp2 = requests.get("http://127.0.0.1:8445/index.md", timeout=2)
            assert "Welcome to fullsite" in resp2.text
        finally:
            # No clean stop - daemon thread dies with process
            pass
        os.chdir("..")

def test_import_all():
    from sitejs import SiteJS, SiteJSConfig, SiteJSLogger, JSDB
    assert SiteJS is not None