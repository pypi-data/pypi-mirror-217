# Self Discover

Self Discover serves autodiscover (Outlook) and autoconfig (Thunderbird) XML files for mail auto-configuration.

# Install

## Generic

Run the following command to create a source distribution:

    python3 setup.py sdist

## PyPI

Run the following command to install the package from PyPI:

    pip3 install self-discover

# Configure

Pass the following environment variables:

* `IMAP_SERVER_HOSTNAME`
* `POP3_SERVER_HOSTNAME`
* `SMTP_SERVER_HOSTNAME`

# Usage

Run the app using an ASGI server such as Uvicorn.

# Tests

Run tests with pytest:

    pytest tests/

