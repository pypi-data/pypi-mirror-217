"""
    Dummy conftest.py for xepor.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html

    Imported from:
    https://github1s.com/mitmproxy/mitmproxy/blob/v7.0.4/test/conftest.py
"""

import os
import socket

from mitmproxy.options import Options
from mitmproxy.utils import data

import pytest

# pytest_plugins = ('test.full_coverage_plugin',)

skip_windows = pytest.mark.skipif(
    os.name == "nt",
    reason='Skipping due to Windows'
)

skip_not_windows = pytest.mark.skipif(
    os.name != "nt",
    reason='Skipping due to not Windows'
)

try:
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind(("::1", 0))
    s.close()
except OSError:
    no_ipv6 = True
else:
    no_ipv6 = False

skip_no_ipv6 = pytest.mark.skipif(
    no_ipv6,
    reason='Host has no IPv6 support'
)


@pytest.fixture()
def tdata():
    return data.Data(__name__)

@pytest.fixture()
def toptions():
    options = Options()
    # options duplicated here to simplify testing setup
    options.add_option(
        "connection_strategy",
        str,
        "lazy",
        "Determine when server connections should be established.",
        choices=("eager", "lazy"),
    )
    options.add_option(
        "keep_host_header",
        bool,
        False,
        """
        Reverse Proxy: Keep the original host header instead of rewriting it
        to the reverse proxy target.
        """,
    )
    return options
