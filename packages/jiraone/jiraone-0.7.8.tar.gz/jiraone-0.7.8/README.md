[![Codacy Badge](https://app.codacy.com/project/badge/Grade/86f1594e0ac3406aa9609c4cd7c70642)](https://www.codacy.com/gh/princenyeche/jiraone/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=princenyeche/jiraone&amp;utm_campaign=Badge_Grade)
[![Downloads](https://pepy.tech/badge/jiraone)](https://pepy.tech/project/jiraone)
[![PyPI version](https://badge.fury.io/py/jiraone.svg)](https://badge.fury.io/py/jiraone)
![PyPI - License](https://img.shields.io/pypi/l/jiraone)
![Build Doc](https://readthedocs.org/projects/jiraone/badge/?version=latest)
[![jiraone](https://snyk.io/advisor/python/jiraone/badge.svg)](https://snyk.io/advisor/python/jiraone)
[![Build Status](https://app.travis-ci.com/princenyeche/jiraone.svg?branch=main)](https://app.travis-ci.com/princenyeche/jiraone)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Jira one
A REST API Implementation to Jira Cloud APIs for creating reports and for performing other Jira queries.

## Configurations
Install using `pip`. You have to be on python >= 3.6.x in order to utilize this script.
* Download python and install on your device by visiting [python.org](https://python.org/downloads)
* Run the below command either using a virtual environment or from your python alias
```bash
pip install jiraone
```
OR
```bash
python3 -m pip install jiraone
```

## Classes, functions and methods
Jiraone comes with various classes, functions and methods. Aliases as well, are used to represent
links to classes and functions. The major ones to take note of are the ones shown on the directory link below.

For further knowledge on how to use the classes, methods or functions. Open the jiraone package and read the docstring on the
aforementioned methods or functions above to get further information.

If you're connecting to Jira server or datacenter, you will need to change the API endpoint to point to server instances. To do that, simply change
the attribute `LOGIN.api = False` this helps to use the endpoint `/rest/api/latest` which is compatible for Jira server or datacenter.

```python
from jiraone import LOGIN

data = "username", "password", "https://server.jiraserver.com"
LOGIN.api = False
LOGIN(*data)
```

The above login method applies only when you need to access a Jira server or datacenter type instances. The above has little or no effect on cloud instance and will work normally.

# Directory
* [Using the API](https://jiraone.readthedocs.io/en/latest/api.html)
  * [endpoint](https://jiraone.readthedocs.io/en/latest/api.html#endpoint)
  * [LOGIN](https://jiraone.readthedocs.io/en/latest/api.html#login)
  * [echo](https://jiraone.readthedocs.io/en/latest/api.html#id4)
  * [add_log](https://jiraone.readthedocs.io/en/latest/api.html#id5)
  * [file_writer](https://jiraone.readthedocs.io/en/latest/api.html#id6)
  * [file_reader](https://jiraone.readthedocs.io/en/latest/api.html#id7)
  * [path_builder](https://jiraone.readthedocs.io/en/latest/api.html#id8)
  * [For](https://jiraone.readthedocs.io/en/latest/api.html#id9)
  * [replacement_placeholder](https://jiraone.readthedocs.io/en/latest/api.html#id10)
  * [field](https://jiraone.readthedocs.io/en/latest/api.html#id11)
  * [comment](https://jiraone.readthedocs.io/en/latest/api.html#id12)
  * [manage](https://jiraone.readthedocs.io/en/latest/api.html#id13)
  * [Other Variables](https://jiraone.readthedocs.io/en/latest/api.html#id14)
* [Basic report usage](https://jiraone.readthedocs.io/en/latest/report.html)
  * [USER API](https://jiraone.readthedocs.io/en/latest/report.html#user-api)
  * [PROJECT API](https://jiraone.readthedocs.io/en/latest/report.html#project-api)
  * [Module API](https://jiraone.readthedocs.io/en/latest/report.html#module-api)
  * [Support](https://jiraone.readthedocs.io/en/latest/report.html#support)
