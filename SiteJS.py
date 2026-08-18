#!/usr/bin/env python3
import argparse
import asyncio
import base64
import bisect
import bz2
import calendar
import collections
import contextlib
import copy
import csv
import ctypes
import datetime
import decimal
import difflib
import dis
import email
import email.utils
import enum
import errno
import fcntl
import filecmp
import fileinput
import fnmatch
import fractions
import ftplib
import functools
import gc
import getopt
import getpass
import gettext
import glob
import gzip
import hashlib
import heapq
import hmac
import html
import http
import http.client
import http.cookies
import http.cookiejar
import http.server
import imaplib
import importlib
import importlib.abc
import importlib.machinery
import importlib.util
import inspect
import io
import itertools
import json
import keyword
import linecache
import locale
import logging
import logging.config
import logging.handlers
import lzma
import mailbox
import mailcap
import marshal
import math
import mimetypes
import mmap
import modulefinder
import multiprocessing
import netrc
import nntplib
import numbers
import operator
import optparse
import os
import pathlib
import pdb
import pickle
import pickletools
import pipes
import pkgutil
import platform
import plistlib
import poplib
import posixpath
import pprint
import profile
import pstats
import pty
import pwd
import py_compile
import pyclbr
import pydoc
import queue
import quopri
import random
import re
import reprlib
import resource
import rlcompleter
import runpy
import sched
import secrets
import select
import selectors
import shelve
import shlex
import shutil
import signal
import smtplib
import sndhdr
import socket
import socketserver
import sqlite3
import ssl
import stat
import statistics
import string
import struct
import subprocess
import sys
import sysconfig
import tabnanny
import tarfile
import telnetlib
import tempfile
import textwrap
import threading
import time
import timeit
import tkinter
import token
import tokenize
import trace
import traceback
import tty
import turtle
import types
import typing
import unicodedata
import unittest
import urllib
import urllib.error
import urllib.parse
import urllib.request
import uuid
import uu
import warnings
import wave
import weakref
import webbrowser
import winreg
import winsound
import xml
import xml.dom
import xml.etree
import xml.parsers
import xml.sax
import xmlrpc
import xmlrpc.client
import xmlrpc.server
import zipapp
import zipfile
import zipimport
import zlib

try:
    import markdown
except ImportError:
    markdown = None
try:
    import jinja2
except ImportError:
    jinja2 = None
try:
    import watchdog
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    watchdog = None
    Observer = None
    FileSystemEventHandler = object
try:
    import websockets
except ImportError:
    websockets = None
try:
    import cryptography
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
except ImportError:
    cryptography = None
try:
    import PIL
    from PIL import Image
except ImportError:
    PIL = None
    Image = None
try:
    import cssmin
except ImportError:
    cssmin = None
try:
    import jsmin
except ImportError:
    jsmin = None
try:
    import boto3
except ImportError:
    boto3 = None
try:
    import paramiko
except ImportError:
    paramiko = None
try:
    import toml
except ImportError:
    toml = None

__version__ = "1.0.0"
__author__ = "Purrple-hub"
__license__ = "Boost Software License 1.0"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4433
DEFAULT_SSL = True
DEFAULT_WATCH = True
DEFAULT_RELOAD = True
DEFAULT_POLL_INTERVAL = 0.3
DEFAULT_RELOAD_TYPE = "poll"

PROJECT_ROOT = os.getcwd()
PAGES_DIR = os.path.join(PROJECT_ROOT, "pages")
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "db.json")
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")
PLUGINS_DIR = os.path.join(PROJECT_ROOT, "plugins")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
CONFIG_PATH = os.path.join(PROJECT_ROOT, "sitejs.toml")

CERT_DIR = os.path.expanduser("~/.sitejs/certs")
DEFAULT_CERT = os.path.join(CERT_DIR, "localhost.crt")
DEFAULT_KEY = os.path.join(CERT_DIR, "localhost.key")

DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title | default("SiteJS") }}</title>
    <link rel="stylesheet" href="/static/style.css">
    <script src="/static/reload.js" defer></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/blog">Blog</a>
            </nav>
        </header>
        <main>
            {{ content }}
        </main>
        <footer>
            <p>Generated by SiteJS.py</p>
        </footer>
    </div>
</body>
</html>"""

DEFAULT_CSS = """* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif; background:#f8f9fa; color:#212529; line-height:1.6; padding:2rem 1rem; }
.container { max-width:960px; margin:0 auto; background:#fff; padding:2rem; border-radius:12px; box-shadow:0 4px 24px rgba(0,0,0,0.06); }
header { border-bottom:1px solid #e9ecef; padding-bottom:1rem; margin-bottom:2rem; }
header h1 { font-weight:600; font-size:2.2rem; letter-spacing:-0.02em; }
nav { margin-top:0.5rem; }
nav a { color:#0d6efd; text-decoration:none; margin-right:1.5rem; font-weight:500; }
nav a:hover { text-decoration:underline; }
main { min-height:60vh; }
h1, h2, h3, h4 { margin:1.5rem 0 0.75rem; font-weight:600; line-height:1.2; }
p { margin-bottom:1rem; }
a { color:#0d6efd; }
code { background:#f1f3f5; padding:0.2rem 0.4rem; border-radius:4px; font-size:0.9em; }
pre { background:#f1f3f5; padding:1rem; border-radius:8px; overflow-x:auto; }
ul, ol { padding-left:1.5rem; margin-bottom:1rem; }
blockquote { border-left:4px solid #0d6efd; padding-left:1rem; color:#6c757d; margin:1rem 0; }
table { width:100%; border-collapse:collapse; margin:1rem 0; }
th, td { border:1px solid #dee2e6; padding:0.5rem 0.75rem; text-align:left; }
th { background:#e9ecef; }
footer { border-top:1px solid #e9ecef; padding-top:1rem; margin-top:2rem; color:#6c757d; font-size:0.9rem; }
img { max-width:100%; height:auto; border-radius:6px; }
@media (max-width:600px) { body { padding:1rem; } .container { padding:1rem; } }
"""

DEFAULT_RELOAD_JS = """(function() {
    var version = 0;
    function check() {
        fetch('/__version')
            .then(function(r) { return r.text(); })
            .then(function(v) {
                var newVer = parseInt(v, 10);
                if (newVer > version) {
                    version = newVer;
                    location.reload();
                }
            })
            .catch(function() {});
    }
    setInterval(check, 500);
})();"""

DEFAULT_404 = "<h1>404</h1><p>Page not found.</p>"
DEFAULT_500 = "<h1>500</h1><p>Internal server error.</p>"

DEFAULT_CONFIG = {
    "host": DEFAULT_HOST,
    "port": DEFAULT_PORT,
    "ssl": DEFAULT_SSL,
    "watch": DEFAULT_WATCH,
    "reload": DEFAULT_RELOAD,
    "poll_interval": DEFAULT_POLL_INTERVAL,
    "reload_type": DEFAULT_RELOAD_TYPE,
    "pages_dir": PAGES_DIR,
    "public_dir": PUBLIC_DIR,
    "templates_dir": TEMPLATES_DIR,
    "data_dir": DATA_DIR,
    "db_path": DB_PATH,
    "dist_dir": DIST_DIR,
    "plugins_dir": PLUGINS_DIR,
    "logs_dir": LOGS_DIR,
    "cert_dir": CERT_DIR,
    "default_template": DEFAULT_TEMPLATE,
    "default_css": DEFAULT_CSS,
    "default_reload_js": DEFAULT_RELOAD_JS,
    "default_404": DEFAULT_404,
    "default_500": DEFAULT_500,
    "markdown_extensions": ["fenced_code", "tables", "nl2br", "codehilite"],
    "template_engine": "jinja2",
    "minify_css": False,
    "minify_js": False,
    "optimize_images": False,
    "image_quality": 85,
    "sitemap": True,
    "rss": True,
    "search_index": False,
    "deploy_method": "rsync",
    "deploy_target": "",
    "deploy_exclude": [".git", "__pycache__", "*.pyc", ".DS_Store"],
    "middleware": [],
    "plugins": [],
    "log_level": "INFO",
    "log_file": os.path.join(LOGS_DIR, "sitejs.log"),
    "session_secret": secrets.token_hex(32),
    "session_timeout": 86400,
    "rate_limit": 100,
    "rate_limit_window": 60,
    "cors_allow_origin": "*",
    "cors_allow_methods": "GET, POST, PUT, DELETE, OPTIONS",
    "cors_allow_headers": "*",
    "csrf_protection": True,
    "max_upload_size": 10485760,
    "cache_control": "no-cache, no-store, must-revalidate",
    "etag": True,
    "gzip_static": True,
    "serve_robots": True,
    "serve_favicon": True,
}

class SiteJSLogger:
    def __init__(self, level="INFO", log_file=None):
        self.level = level
        self.log_file = log_file
        self._setup()
    def _setup(self):
        self.logger = logging.getLogger("SiteJS")
        self.logger.setLevel(getattr(logging, self.level.upper(), logging.INFO))
        self.logger.handlers.clear()
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(self.logger.level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        if self.log_file:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            fh = logging.handlers.RotatingFileHandler(self.log_file, maxBytes=10485760, backupCount=5, encoding="utf-8")
            fh.setLevel(self.logger.level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def critical(self, msg): self.logger.critical(msg)
    def exception(self, msg): self.logger.exception(msg)

class SiteJSConfig:
    def __init__(self, config_dict=None, config_file=None):
        self._data = DEFAULT_CONFIG.copy()
        if config_file and os.path.exists(config_file):
            self._load_file(config_file)
        if config_dict:
            self._data.update(config_dict)
        self._apply_env()
    def _load_file(self, path):
        if toml is None:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = toml.load(f)
            self._data.update(data)
        except Exception:
            pass
    def _apply_env(self):
        for key in self._data:
            env_key = f"SITEJS_{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                if isinstance(self._data[key], bool):
                    self._data[key] = val.lower() in ("true", "1", "yes")
                elif isinstance(self._data[key], int):
                    self._data[key] = int(val)
                elif isinstance(self._data[key], float):
                    self._data[key] = float(val)
                elif isinstance(self._data[key], list):
                    self._data[key] = [x.strip() for x in val.split(",") if x.strip()]
                else:
                    self._data[key] = val
    def __getitem__(self, key): return self._data.get(key)
    def __setitem__(self, key, value): self._data[key] = value
    def __contains__(self, key): return key in self._data
    def get(self, key, default=None): return self._data.get(key, default)
    def set(self, key, value): self._data[key] = value
    def update(self, other): self._data.update(other)
    def to_dict(self): return self._data.copy()
    def save(self, path):
        if toml is None:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                toml.dump(self._data, f)
        except Exception:
            pass

class PluginManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.plugins = {}
        self.hooks = {}
    def load_plugin(self, name, module_path):
        try:
            spec = importlib.util.spec_from_file_location(name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "setup"):
                module.setup(self.config, self.logger)
            self.plugins[name] = module
            self.logger.info(f"Loaded plugin: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load plugin {name}: {e}")
            return False
    def register_hook(self, hook_name, callback):
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)
    def run_hook(self, hook_name, *args, **kwargs):
        results = []
        for cb in self.hooks.get(hook_name, []):
            try:
                res = cb(*args, **kwargs)
                results.append(res)
            except Exception as e:
                self.logger.error(f"Hook {hook_name} callback failed: {e}")
        for name, module in self.plugins.items():
            if hasattr(module, hook_name):
                try:
                    res = getattr(module, hook_name)(*args, **kwargs)
                    results.append(res)
                except Exception as e:
                    self.logger.error(f"Plugin {name} hook {hook_name} failed: {e}")
        return results
    def load_all(self, plugins_dir):
        if not os.path.exists(plugins_dir):
            return
        for file in os.listdir(plugins_dir):
            if file.endswith(".py"):
                name = file[:-3]
                path = os.path.join(plugins_dir, file)
                self.load_plugin(name, path)

class JSDB:
    def __init__(self, path=DB_PATH, logger=None):
        self.path = path
        self.logger = logger or SiteJSLogger()
        self.data = {}
        self.indexes = {}
        self.lock = threading.RLock()
        self._load()
    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                self._build_indexes()
            except (json.JSONDecodeError, IOError):
                self.data = {}
                self.indexes = {}
    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    def _build_indexes(self):
        self.indexes = {}
        for key, value in self.data.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    if k not in self.indexes:
                        self.indexes[k] = {}
                    if v not in self.indexes[k]:
                        self.indexes[k][v] = []
                    self.indexes[k][v].append(key)
    def get(self, key, default=None):
        with self.lock:
            return self.data.get(key, default)
    def set(self, key, value):
        with self.lock:
            self.data[key] = value
            self._save()
            self._build_indexes()
    def delete(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]
                self._save()
                self._build_indexes()
                return True
            return False
    def all(self):
        with self.lock:
            return dict(self.data)
    def keys(self):
        with self.lock:
            return list(self.data.keys())
    def values(self):
        with self.lock:
            return list(self.data.values())
    def items(self):
        with self.lock:
            return list(self.data.items())
    def query(self, field, value):
        with self.lock:
            if field in self.indexes and value in self.indexes[field]:
                results = []
                for key in self.indexes[field][value]:
                    results.append((key, self.data.get(key)))
                return results
            return []
    def update(self, key, update_dict):
        with self.lock:
            if key in self.data and isinstance(self.data[key], dict):
                self.data[key].update(update_dict)
                self._save()
                self._build_indexes()
                return True
            return False
    def increment(self, key, field, amount=1):
        with self.lock:
            if key in self.data and isinstance(self.data[key], dict):
                if field in self.data[key]:
                    self.data[key][field] += amount
                else:
                    self.data[key][field] = amount
                self._save()
                self._build_indexes()
                return True
            return False
    def push(self, key, array_field, item):
        with self.lock:
            if key in self.data and isinstance(self.data[key], dict):
                if array_field not in self.data[key]:
                    self.data[key][array_field] = []
                self.data[key][array_field].append(item)
                self._save()
                self._build_indexes()
                return True
            return False
    def pop(self, key, array_field, index=-1):
        with self.lock:
            if key in self.data and isinstance(self.data[key], dict):
                if array_field in self.data[key] and isinstance(self.data[key][array_field], list):
                    if self.data[key][array_field]:
                        val = self.data[key][array_field].pop(index)
                        self._save()
                        self._build_indexes()
                        return val
            return None
    def find(self, filter_func):
        with self.lock:
            results = []
            for key, value in self.data.items():
                if filter_func(key, value):
                    results.append((key, value))
            return results
    def aggregate(self, pipeline):
        with self.lock:
            data = list(self.data.values())
            for stage in pipeline:
                if "group" in stage:
                    groups = {}
                    gb = stage["group"]
                    by = gb.get("by", [])
                    for item in data:
                        key = tuple(item.get(k) for k in by)
                        if key not in groups:
                            groups[key] = []
                        groups[key].append(item)
                    result = []
                    for key, group in groups.items():
                        row = {"_id": key}
                        for agg, field in gb.get("sum", {}).items():
                            row[agg] = sum(item.get(field, 0) for item in group)
                        for agg, field in gb.get("avg", {}).items():
                            vals = [item.get(field, 0) for item in group]
                            row[agg] = sum(vals) / len(vals) if vals else 0
                        for agg, field in gb.get("max", {}).items():
                            row[agg] = max((item.get(field) for item in group), default=0)
                        for agg, field in gb.get("min", {}).items():
                            row[agg] = min((item.get(field) for item in group), default=0)
                        result.append(row)
                    data = result
                if "filter" in stage:
                    filters = stage["filter"]
                    def passes(item):
                        for k, v in filters.items():
                            if isinstance(v, dict):
                                if "$gt" in v:
                                    if not (item.get(k, float("-inf")) > v["$gt"]):
                                        return False
                                elif "$lt" in v:
                                    if not (item.get(k, float("inf")) < v["$lt"]):
                                        return False
                                elif "$eq" in v:
                                    if not (item.get(k) == v["$eq"]):
                                        return False
                            else:
                                if item.get(k) != v:
                                    return False
                        return True
                    data = [item for item in data if passes(item)]
                if "sort" in stage:
                    sort_key = stage["sort"]
                    reverse = stage.get("reverse", False)
                    data.sort(key=lambda x: x.get(sort_key, 0), reverse=reverse)
                if "limit" in stage:
                    data = data[:stage["limit"]]
                if "skip" in stage:
                    data = data[stage["skip"]:]
            return data

class RateLimiter:
    def __init__(self, limit=100, window=60):
        self.limit = limit
        self.window = window
        self.records = {}
        self.lock = threading.Lock()
    def is_allowed(self, key):
        now = time.time()
        with self.lock:
            if key not in self.records:
                self.records[key] = []
            self.records[key] = [t for t in self.records[key] if now - t < self.window]
            if len(self.records[key]) >= self.limit:
                return False
            self.records[key].append(now)
            return True
    def reset(self, key):
        with self.lock:
            if key in self.records:
                del self.records[key]

class SessionStore:
    def __init__(self, secret, timeout=86400):
        self.secret = secret
        self.timeout = timeout
        self.sessions = {}
        self.lock = threading.Lock()
    def create(self, data=None):
        sid = secrets.token_hex(32)
        with self.lock:
            self.sessions[sid] = {
                "data": data or {},
                "created": time.time(),
                "last_access": time.time()
            }
        return sid
    def get(self, sid):
        with self.lock:
            if sid not in self.sessions:
                return None
            sess = self.sessions[sid]
            if time.time() - sess["last_access"] > self.timeout:
                del self.sessions[sid]
                return None
            sess["last_access"] = time.time()
            return sess["data"]
    def destroy(self, sid):
        with self.lock:
            if sid in self.sessions:
                del self.sessions[sid]
                return True
            return False
    def touch(self, sid):
        with self.lock:
            if sid in self.sessions:
                self.sessions[sid]["last_access"] = time.time()
                return True
            return False

class PollingWatcher:
    def __init__(self, paths, callback, interval=DEFAULT_POLL_INTERVAL, logger=None):
        self.paths = [os.path.abspath(p) for p in paths]
        self.callback = callback
        self.interval = interval
        self.logger = logger or SiteJSLogger()
        self.mtimes = {}
        self.running = False
        self.thread = None
    def start(self):
        if self.running:
            return
        self.running = True
        self._scan_mtimes()
        self.thread = threading.Thread(target=self._poll, daemon=True)
        self.thread.start()
        self.logger.info("Polling watcher started")
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None
        self.logger.info("Polling watcher stopped")
    def _scan_mtimes(self):
        for path in self.paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for name in files:
                        full = os.path.join(root, name)
                        try:
                            self.mtimes[full] = os.path.getmtime(full)
                        except OSError:
                            pass
    def _poll(self):
        while self.running:
            changed = False
            for path in self.paths:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for name in files:
                            full = os.path.join(root, name)
                            try:
                                mtime = os.path.getmtime(full)
                                if full not in self.mtimes or self.mtimes[full] != mtime:
                                    self.mtimes[full] = mtime
                                    changed = True
                            except OSError:
                                pass
            if changed:
                self.callback()
            time.sleep(self.interval)

class WatchdogWatcher:
    def __init__(self, paths, callback, logger):
        self.paths = paths
        self.callback = callback
        self.logger = logger
        self.observer = None
        self.event_handler = None
    def start(self):
        if Observer is None:
            self.logger.error("Watchdog not installed")
            return
        class Handler(FileSystemEventHandler):
            def __init__(self, cb):
                self.cb = cb
            def on_modified(self, event):
                if not event.is_directory:
                    self.cb()
        self.event_handler = Handler(self.callback)
        self.observer = Observer()
        for path in self.paths:
            if os.path.exists(path):
                self.observer.schedule(self.event_handler, path, recursive=True)
        self.observer.start()
        self.logger.info("Watchdog watcher started")
    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.logger.info("Watchdog watcher stopped")

class SiteJSBuilder:
    def __init__(self, config, logger, db):
        self.config = config
        self.logger = logger
        self.db = db
        self.template_env = None
        self._init_template_engine()
    def _init_template_engine(self):
        engine = self.config.get("template_engine", "jinja2")
        if engine == "jinja2" and jinja2 is not None:
            loader = jinja2.FileSystemLoader(self.config.get("templates_dir", TEMPLATES_DIR))
            self.template_env = jinja2.Environment(loader=loader, autoescape=True)
        else:
            self.template_env = None
    def render_page(self, md_path, context=None):
        if context is None:
            context = {}
        if markdown is None:
            self.logger.error("Markdown library not installed")
            return "<p>Error: markdown not available</p>"
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
        except IOError as e:
            self.logger.error(f"Failed to read {md_path}: {e}")
            return f"<p>Error reading file: {e}</p>"
        extensions = self.config.get("markdown_extensions", ["fenced_code", "tables"])
        html = markdown.markdown(content, extensions=extensions)
        title = os.path.basename(md_path).replace(".md", "").replace("_", " ").title()
        ctx = {"title": title, "content": html, "path": md_path, "config": self.config.to_dict()}
        ctx.update(context)
        if self.template_env:
            try:
                template = self.template_env.get_template("page.html")
                output = template.render(**ctx)
            except jinja2.TemplateNotFound:
                template = jinja2.Template(self.config.get("default_template", DEFAULT_TEMPLATE))
                output = template.render(**ctx)
        else:
            template = jinja2.Template(self.config.get("default_template", DEFAULT_TEMPLATE))
            output = template.render(**ctx)
        return output
    def build_all(self, output_dir=DIST_DIR):
        pages_dir = self.config.get("pages_dir", PAGES_DIR)
        public_dir = self.config.get("public_dir", PUBLIC_DIR)
        templates_dir = self.config.get("templates_dir", TEMPLATES_DIR)
        output_dir = os.path.abspath(output_dir)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        if os.path.exists(public_dir):
            for item in os.listdir(public_dir):
                src = os.path.join(public_dir, item)
                dst = os.path.join(output_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*self.config.get("deploy_exclude", [])))
                else:
                    shutil.copy2(src, dst)
        if os.path.exists(templates_dir):
            for f in os.listdir(templates_dir):
                if f.endswith(".html") or f.endswith(".htm"):
                    shutil.copy2(os.path.join(templates_dir, f), os.path.join(output_dir, f))
        if os.path.exists(pages_dir):
            for root, dirs, files in os.walk(pages_dir):
                for file in files:
                    if file.endswith(".md"):
                        rel_dir = os.path.relpath(root, pages_dir)
                        out_dir = os.path.join(output_dir, rel_dir)
                        os.makedirs(out_dir, exist_ok=True)
                        md_path = os.path.join(root, file)
                        html = self.render_page(md_path)
                        out_file = os.path.join(out_dir, file.replace(".md", ".html"))
                        with open(out_file, "w", encoding="utf-8") as f:
                            f.write(html)
        if self.config.get("sitemap", True):
            self._generate_sitemap(output_dir)
        if self.config.get("rss", True):
            self._generate_rss(output_dir)
        if self.config.get("search_index", False):
            self._generate_search_index(output_dir)
        self.logger.info(f"Build complete: {output_dir}")
    def _generate_sitemap(self, output_dir):
        sitemap = []
        pages_dir = self.config.get("pages_dir", PAGES_DIR)
        for root, dirs, files in os.walk(pages_dir):
            for file in files:
                if file.endswith(".md"):
                    rel = os.path.relpath(os.path.join(root, file), pages_dir)
                    url = "/" + rel.replace(".md", ".html").replace(os.sep, "/")
                    sitemap.append(url)
        sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in sitemap:
            sitemap_xml += f"  <url><loc>https://localhost{url}</loc></url>\n"
        sitemap_xml += "</urlset>"
        with open(os.path.join(output_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sitemap_xml)
    def _generate_rss(self, output_dir):
        items = []
        pages_dir = self.config.get("pages_dir", PAGES_DIR)
        for root, dirs, files in os.walk(pages_dir):
            for file in files:
                if file.endswith(".md"):
                    rel = os.path.relpath(os.path.join(root, file), pages_dir)
                    url = "/" + rel.replace(".md", ".html").replace(os.sep, "/")
                    title = file.replace(".md", "").replace("_", " ").title()
                    items.append({"title": title, "link": url})
        rss = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n<title>SiteJS RSS</title>\n<link>https://localhost/</link>\n<description>Recent updates</description>\n'
        for item in items:
            rss += f"  <item><title>{item['title']}</title><link>https://localhost{item['link']}</link></item>\n"
        rss += "</channel>\n</rss>"
        with open(os.path.join(output_dir, "feed.xml"), "w", encoding="utf-8") as f:
            f.write(rss)
    def _generate_search_index(self, output_dir):
        index = []
        pages_dir = self.config.get("pages_dir", PAGES_DIR)
        for root, dirs, files in os.walk(pages_dir):
            for file in files:
                if file.endswith(".md"):
                    rel = os.path.relpath(os.path.join(root, file), pages_dir)
                    url = "/" + rel.replace(".md", ".html").replace(os.sep, "/")
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            text = f.read()
                        index.append({"url": url, "title": file.replace(".md", ""), "content": text[:500]})
                    except IOError:
                        pass
        with open(os.path.join(output_dir, "search.json"), "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)

class AssetManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    def minify_css(self, content):
        if cssmin:
            try:
                return cssmin.cssmin(content)
            except Exception:
                return content
        return content
    def minify_js(self, content):
        if jsmin:
            try:
                return jsmin.jsmin(content)
            except Exception:
                return content
        return content
    def optimize_image(self, input_path, output_path=None, quality=85):
        if Image is None:
            return False
        try:
            img = Image.open(input_path)
            if output_path is None:
                output_path = input_path
            if img.format in ("JPEG", "JPG"):
                img.save(output_path, "JPEG", quality=quality, optimize=True)
            elif img.format == "PNG":
                img.save(output_path, "PNG", optimize=True)
            else:
                img.save(output_path, quality=quality)
            return True
        except Exception as e:
            self.logger.error(f"Image optimization failed for {input_path}: {e}")
            return False
    def process_assets(self, input_dir, output_dir):
        public_dir = self.config.get("public_dir", PUBLIC_DIR)
        if not os.path.exists(public_dir):
            return
        for root, dirs, files in os.walk(public_dir):
            rel_dir = os.path.relpath(root, public_dir)
            out_dir = os.path.join(output_dir, rel_dir)
            os.makedirs(out_dir, exist_ok=True)
            for file in files:
                src = os.path.join(root, file)
                dst = os.path.join(out_dir, file)
                ext = os.path.splitext(file)[1].lower()
                if ext in (".css", ".css.map"):
                    if self.config.get("minify_css", False):
                        with open(src, "r", encoding="utf-8") as f:
                            data = f.read()
                        data = self.minify_css(data)
                        with open(dst, "w", encoding="utf-8") as f:
                            f.write(data)
                    else:
                        shutil.copy2(src, dst)
                elif ext in (".js", ".js.map"):
                    if self.config.get("minify_js", False):
                        with open(src, "r", encoding="utf-8") as f:
                            data = f.read()
                        data = self.minify_js(data)
                        with open(dst, "w", encoding="utf-8") as f:
                            f.write(data)
                    else:
                        shutil.copy2(src, dst)
                elif ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
                    if self.config.get("optimize_images", False):
                        self.optimize_image(src, dst, self.config.get("image_quality", 85))
                    else:
                        shutil.copy2(src, dst)
                else:
                    shutil.copy2(src, dst)

class Deployer:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    def deploy(self, source_dir=DIST_DIR):
        method = self.config.get("deploy_method", "rsync")
        target = self.config.get("deploy_target", "")
        if not target:
            self.logger.error("No deploy target set")
            return False
        exclude = self.config.get("deploy_exclude", [])
        if method == "rsync":
            cmd = ["rsync", "-avz", "--delete"]
            for e in exclude:
                cmd.append(f"--exclude={e}")
            cmd.append(source_dir + "/")
            cmd.append(target)
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                self.logger.info(f"Deployed via rsync to {target}")
                return True
            except subprocess.CalledProcessError as e:
                self.logger.error(f"rsync failed: {e.stderr.decode()}")
                return False
        elif method == "ftp" and ftplib:
            parts = urllib.parse.urlparse(target)
            if parts.scheme != "ftp":
                self.logger.error("Invalid FTP URL")
                return False
            try:
                ftp = ftplib.FTP(parts.hostname)
                ftp.login(parts.username or "anonymous", parts.password or "")
                ftp.cwd(parts.path or "/")
                for root, dirs, files in os.walk(source_dir):
                    rel = os.path.relpath(root, source_dir)
                    if rel == ".":
                        rel = ""
                    for d in dirs:
                        try:
                            ftp.mkd(os.path.join(rel, d))
                        except ftplib.error_perm:
                            pass
                    for f in files:
                        local = os.path.join(root, f)
                        remote = os.path.join(rel, f)
                        with open(local, "rb") as lf:
                            ftp.storbinary(f"STOR {remote}", lf)
                ftp.quit()
                self.logger.info(f"Deployed via FTP to {target}")
                return True
            except Exception as e:
                self.logger.error(f"FTP deploy failed: {e}")
                return False
        elif method == "s3" and boto3:
            parts = urllib.parse.urlparse(target)
            bucket = parts.hostname
            prefix = parts.path.lstrip("/")
            if not bucket:
                self.logger.error("S3 bucket not specified")
                return False
            try:
                s3 = boto3.client("s3")
                for root, dirs, files in os.walk(source_dir):
                    for f in files:
                        local = os.path.join(root, f)
                        key = os.path.join(prefix, os.path.relpath(local, source_dir))
                        s3.upload_file(local, bucket, key)
                self.logger.info(f"Deployed to S3 bucket {bucket}")
                return True
            except Exception as e:
                self.logger.error(f"S3 deploy failed: {e}")
                return False
        elif method == "sftp" and paramiko:
            parts = urllib.parse.urlparse(target)
            host = parts.hostname
            port = parts.port or 22
            user = parts.username or "root"
            pwd = parts.password or ""
            path = parts.path or "/"
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=port, username=user, password=pwd)
                sftp = ssh.open_sftp()
                for root, dirs, files in os.walk(source_dir):
                    rel = os.path.relpath(root, source_dir)
                    remote_dir = os.path.join(path, rel).replace("\\", "/")
                    try:
                        sftp.stat(remote_dir)
                    except FileNotFoundError:
                        sftp.mkdir(remote_dir)
                    for f in files:
                        local = os.path.join(root, f)
                        remote = os.path.join(remote_dir, f).replace("\\", "/")
                        sftp.put(local, remote)
                sftp.close()
                ssh.close()
                self.logger.info(f"Deployed via SFTP to {target}")
                return True
            except Exception as e:
                self.logger.error(f"SFTP deploy failed: {e}")
                return False
        else:
            self.logger.error(f"Unsupported deploy method: {method}")
            return False

class SiteJSServer:
    def __init__(self, config, logger, db, watcher=None):
        self.config = config
        self.logger = logger
        self.db = db
        self.watcher = watcher
        self.httpd = None
        self.version = 0
        self.builder = SiteJSBuilder(config, logger, db)
        self.plugin_manager = PluginManager(config, logger)
        self.plugin_manager.register_hook("before_request", lambda *a, **kw: None)
        self.plugin_manager.register_hook("after_request", lambda *a, **kw: None)
        self.rate_limiter = RateLimiter(
            config.get("rate_limit", 100),
            config.get("rate_limit_window", 60)
        )
        self.session_store = SessionStore(
            config.get("session_secret", secrets.token_hex(32)),
            config.get("session_timeout", 86400)
        )
        self._init_server()
    def _init_server(self):
        host = self.config.get("host", DEFAULT_HOST)
        port = self.config.get("port", DEFAULT_PORT)
        self.host = host
        self.port = port
        self.use_ssl = self.config.get("ssl", DEFAULT_SSL)
        self.server_address = (host, port)
        self.handler_class = self._make_handler()
    def _make_handler(self):
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.server_ref = self.server
                super().__init__(*args, **kwargs)
            def do_GET(self):
                self._handle_request("GET")
            def do_POST(self):
                self._handle_request("POST")
            def do_PUT(self):
                self._handle_request("PUT")
            def do_DELETE(self):
                self._handle_request("DELETE")
            def do_OPTIONS(self):
                self._handle_request("OPTIONS")
            def _handle_request(self, method):
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path
                query = urllib.parse.parse_qs(parsed.query)
                client_ip = self.client_address[0]
                if not self.server_ref.rate_limiter.is_allowed(client_ip):
                    self.send_error(429, "Too Many Requests")
                    return
                self.server_ref.plugin_manager.run_hook("before_request", self, method, path, query)
                if path == "/__version":
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write(str(self.server_ref.version).encode())
                    self.server_ref.plugin_manager.run_hook("after_request", self)
                    return
                if path == "/__reload.js":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/javascript")
                    self.end_headers()
                    js = self.server_ref.config.get("default_reload_js", DEFAULT_RELOAD_JS)
                    self.wfile.write(js.encode())
                    self.server_ref.plugin_manager.run_hook("after_request", self)
                    return
                if path.startswith("/static/"):
                    static_dir = self.server_ref.config.get("public_dir", PUBLIC_DIR)
                    file_path = os.path.join(static_dir, path[8:])
                    if os.path.exists(file_path) and not os.path.isdir(file_path):
                        self.serve_file(file_path)
                        self.server_ref.plugin_manager.run_hook("after_request", self)
                        return
                    else:
                        self.send_error(404, self.server_ref.config.get("default_404", DEFAULT_404))
                        self.server_ref.plugin_manager.run_hook("after_request", self)
                        return
                if method == "GET":
                    pages_dir = self.server_ref.config.get("pages_dir", PAGES_DIR)
                    file_path = os.path.join(pages_dir, path.lstrip("/"))
                    if os.path.exists(file_path) and not os.path.isdir(file_path) and file_path.endswith(".md"):
                        ctx = {"query": query}
                        html = self.server_ref.builder.render_page(file_path, ctx)
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html")
                        self.end_headers()
                        self.wfile.write(html.encode("utf-8"))
                        self.server_ref.plugin_manager.run_hook("after_request", self)
                        return
                    static_file = os.path.join(self.server_ref.config.get("public_dir", PUBLIC_DIR), path.lstrip("/"))
                    if os.path.exists(static_file) and not os.path.isdir(static_file):
                        self.serve_file(static_file)
                        self.server_ref.plugin_manager.run_hook("after_request", self)
                        return
                self.send_error(404, self.server_ref.config.get("default_404", DEFAULT_404))
                self.server_ref.plugin_manager.run_hook("after_request", self)
            def serve_file(self, path):
                try:
                    content_type, _ = mimetypes.guess_type(path)
                    if content_type is None:
                        content_type = "application/octet-stream"
                    with open(path, "rb") as f:
                        self.send_response(200)
                        self.send_header("Content-Type", content_type)
                        self.end_headers()
                        self.wfile.write(f.read())
                except Exception as e:
                    self.send_error(500, self.server_ref.config.get("default_500", DEFAULT_500))
            def log_message(self, format, *args):
                self.server_ref.logger.info(f"{self.address_string()} - {format % args}")
            def handle_one_request(self):
                try:
                    super().handle_one_request()
                except Exception as e:
                    self.send_error(500, str(e))
        return Handler
    def start(self):
        self.httpd = http.server.HTTPServer(self.server_address, self.handler_class)
        self.httpd.version = self.version
        self.httpd.config = self.config
        self.httpd.logger = self.logger
        self.httpd.db = self.db
        self.httpd.builder = self.builder
        self.httpd.plugin_manager = self.plugin_manager
        self.httpd.rate_limiter = self.rate_limiter
        if self.use_ssl:
            self._setup_ssl()
        if self.watcher:
            self.watcher.start()
        self.logger.info(f"Server started at {'https' if self.use_ssl else 'http'}://{self.host}:{self.port}")
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            self.stop()
    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        if self.watcher:
            self.watcher.stop()
        self.logger.info("Server stopped")
    def _setup_ssl(self):
        if cryptography is None:
            self.logger.warning("cryptography not installed, falling back to HTTP")
            self.use_ssl = False
            return
        os.makedirs(CERT_DIR, exist_ok=True)
        cert_path = DEFAULT_CERT
        key_path = DEFAULT_KEY
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            self._generate_cert(cert_path, key_path)
        try:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(cert_path, key_path)
            self.httpd.socket = context.wrap_socket(self.httpd.socket, server_side=True)
        except Exception as e:
            self.logger.error(f"SSL setup failed: {e}, falling back to HTTP")
            self.use_ssl = False
    def _generate_cert(self, cert_path, key_path):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)
        cert = cert.public_key(key.public_key())
        cert = cert.serial_number(x509.random_serial_number())
        cert = cert.not_valid_before(datetime.datetime.utcnow())
        cert = cert.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        cert = cert.add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost"), x509.DNSName("*.localhost")]), critical=False)
        cert = cert.sign(key, hashes.SHA256())
        with open(key_path, "wb") as f:
            f.write(key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()))
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        self.logger.info(f"Generated self-signed certificate: {cert_path}")
    def reload(self):
        self.version += 1
        self.logger.info(f"Reload triggered (version {self.version})")
        if self.httpd:
            self.httpd.version = self.version

class SiteJS:
    def __init__(self, config_dict=None, config_file=None):
        self.config = SiteJSConfig(config_dict, config_file)
        self.logger = SiteJSLogger(self.config.get("log_level", "INFO"), self.config.get("log_file"))
        self.db = JSDB(self.config.get("db_path", DB_PATH), self.logger)
        self.asset_manager = AssetManager(self.config, self.logger)
        self.deployer = Deployer(self.config, self.logger)
        self.watcher = None
        self.server = None
        self._init_watcher()
    def _init_watcher(self):
        if self.config.get("watch", True):
            paths = [self.config.get("pages_dir", PAGES_DIR),
                     self.config.get("public_dir", PUBLIC_DIR),
                     self.config.get("templates_dir", TEMPLATES_DIR)]
            reload_type = self.config.get("reload_type", "poll")
            if reload_type == "watchdog" and Observer is not None:
                self.watcher = WatchdogWatcher(paths, self._on_change, self.logger)
            else:
                self.watcher = PollingWatcher(paths, self._on_change,
                                              self.config.get("poll_interval", DEFAULT_POLL_INTERVAL),
                                              self.logger)
        else:
            self.watcher = None
    def _on_change(self):
        if self.server:
            self.server.reload()
    def serve(self):
        self.server = SiteJSServer(self.config, self.logger, self.db, self.watcher)
        self.server.start()
    def build(self, output_dir=None):
        if output_dir is None:
            output_dir = self.config.get("dist_dir", DIST_DIR)
        builder = SiteJSBuilder(self.config, self.logger, self.db)
        builder.build_all(output_dir)
        self.asset_manager.process_assets(self.config.get("public_dir", PUBLIC_DIR), output_dir)
    def deploy(self):
        return self.deployer.deploy(self.config.get("dist_dir", DIST_DIR))
    def db_command(self, subcommand, *args):
        if subcommand == "get":
            if not args:
                self.logger.error("Missing key")
                return
            val = self.db.get(args[0])
            print(json.dumps(val, indent=2) if val is not None else "null")
        elif subcommand == "set":
            if len(args) < 2:
                self.logger.error("Usage: db set key value_json")
                return
            try:
                value = json.loads(args[1])
                self.db.set(args[0], value)
                self.logger.info(f"Set {args[0]}")
            except json.JSONDecodeError:
                self.logger.error("Invalid JSON")
        elif subcommand == "delete":
            if not args:
                self.logger.error("Missing key")
                return
            if self.db.delete(args[0]):
                self.logger.info(f"Deleted {args[0]}")
            else:
                self.logger.warning(f"Key {args[0]} not found")
        elif subcommand == "all":
            data = self.db.all()
            print(json.dumps(data, indent=2))
        elif subcommand == "query":
            if len(args) < 2:
                self.logger.error("Usage: db query field value")
                return
            results = self.db.query(args[0], args[1])
            print(json.dumps(results, indent=2))
        elif subcommand == "aggregate":
            if not args:
                self.logger.error("Usage: db aggregate json_pipeline")
                return
            try:
                pipeline = json.loads(args[0])
                results = self.db.aggregate(pipeline)
                print(json.dumps(results, indent=2))
            except json.JSONDecodeError:
                self.logger.error("Invalid JSON pipeline")
        else:
            self.logger.error(f"Unknown db subcommand: {subcommand}")
    def cleanup(self):
        if self.watcher:
            self.watcher.stop()
        if self.server:
            self.server.stop()
        self.logger.info("Cleanup completed")

def cli_new(name):
    if os.path.exists(name):
        print(f"Error: {name} already exists")
        sys.exit(1)
    os.makedirs(name)
    os.chdir(name)
    os.makedirs("pages", exist_ok=True)
    os.makedirs("public", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    with open(os.path.join("pages", "index.md"), "w", encoding="utf-8") as f:
        f.write(f"# Welcome to {name}\n\nThis site was created with SiteJS.py.\n\n## Features\n\n- Zero config\n- Live reload\n- Markdown rendering\n- JSON database\n- Build to static HTML\n")
    with open(os.path.join("templates", "page.html"), "w", encoding="utf-8") as f:
        f.write(DEFAULT_TEMPLATE)
    with open(os.path.join("public", "style.css"), "w", encoding="utf-8") as f:
        f.write(DEFAULT_CSS)
    with open(os.path.join("public", "reload.js"), "w", encoding="utf-8") as f:
        f.write(DEFAULT_RELOAD_JS)
    with open(os.path.join("data", "db.json"), "w", encoding="utf-8") as f:
        json.dump({}, f, indent=2)
    with open(os.path.join("logs", "sitejs.log"), "w") as f:
        f.write("")
    print(f"Created new site: {name}")
    print(f"  cd {name}")
    print("  sitejs serve")

def cli_serve(host, port, no_ssl, no_watch):
    config = {
        "host": host or DEFAULT_HOST,
        "port": port or DEFAULT_PORT,
        "ssl": not no_ssl,
        "watch": not no_watch,
        "reload_type": "poll"
    }
    app = SiteJS(config)
    try:
        app.serve()
    except KeyboardInterrupt:
        app.cleanup()
        print("\nServer stopped")

def cli_build(output_dir):
    app = SiteJS()
    app.build(output_dir)

def cli_deploy():
    app = SiteJS()
    if app.deploy():
        print("Deployment successful")
    else:
        print("Deployment failed")
        sys.exit(1)

def cli_db(subcommand, key, value):
    app = SiteJS()
    app.db_command(subcommand, key, value)

def main():
    parser = argparse.ArgumentParser(prog="sitejs", description="SiteJS.py – the Python Small Web builder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a new site")
    new_parser.add_argument("name", help="Project name")

    serve_parser = subparsers.add_parser("serve", help="Start development server")
    serve_parser.add_argument("--host", default=DEFAULT_HOST, help="Host to bind")
    serve_parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port")
    serve_parser.add_argument("--no-ssl", action="store_true", help="Disable SSL")
    serve_parser.add_argument("--no-watch", action="store_true", help="Disable file watching")

    build_parser = subparsers.add_parser("build", help="Build static site")
    build_parser.add_argument("--output", "-o", default=DIST_DIR, help="Output directory")

    deploy_parser = subparsers.add_parser("deploy", help="Deploy to target")

    db_parser = subparsers.add_parser("db", help="Database operations")
    db_parser.add_argument("action", choices=["get", "set", "delete", "all", "query", "aggregate"], help="Action")
    db_parser.add_argument("key", nargs="?", help="Key")
    db_parser.add_argument("value", nargs="?", help="Value (JSON for set/aggregate)")

    args = parser.parse_args()

    if args.command == "new":
        cli_new(args.name)
    elif args.command == "serve":
        cli_serve(args.host, args.port, args.no_ssl, args.no_watch)
    elif args.command == "build":
        cli_build(args.output)
    elif args.command == "deploy":
        cli_deploy()
    elif args.command == "db":
        cli_db(args.action, args.key, args.value)

if __name__ == "__main__":
    main()