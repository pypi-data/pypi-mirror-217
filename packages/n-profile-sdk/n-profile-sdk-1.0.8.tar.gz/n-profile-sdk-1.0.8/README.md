
# Getting Started with CTD - Documentation

## Install the Package

The package is compatible with Python versions `3 >=3.7, <= 3.11`.
Install the package from PyPi using the following pip command:

```python
pip install n-profile-sdk==1.0.8
```

You can also view the package at:
https://pypi.python.org/pypi/n-profile-sdk/1.0.8

## Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `pytest` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
pytest
```

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `host` | `string` | *Default*: `'HostValue'` |
| `environment` | Environment | The API environment. <br> **Default: `Environment.PRODUCTION`** |
| `http_client_instance` | `HttpClient` | The Http Client passed from the sdk user for making requests |
| `override_http_client_configuration` | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| `http_call_back` | `HttpCallBack` | The callback value that is invoked before and after an HTTP call is made to an endpoint |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| `retry_statuses` | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| `retry_methods` | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |
| `authorization` | `string` |  |

The API client can be initialized as follows:

```python
from ctddocumentation.ctddocumentation_client import CtddocumentationClient
from ctddocumentation.configuration import Environment

client = CtddocumentationClient(
    authorization='Authorization'
)
```

## Authorization

This API uses `Custom Header Signature`.

## List of APIs

* [Tasks Queries](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/tasks-queries.md)
* [Custom Attributes Categories](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/custom-attributes-categories.md)
* [Login](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/login.md)
* [Assets](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/assets.md)
* [Alerts](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/alerts.md)
* [Tasks](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/tasks.md)
* [Queries](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/queries.md)
* [Insights](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/insights.md)
* [Sites](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/sites.md)
* [Activities](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/activities.md)
* [License](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/license.md)
* [Users](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/users.md)
* [Groups](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/groups.md)
* [Sensors](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/sensors.md)
* [Events](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/controllers/events.md)

## Classes Documentation

* [Utility Classes](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/utility-classes.md)
* [HttpResponse](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/http-response.md)
* [HttpRequest](https://www.github.com/Syed-Subtain/n-profile-python-sdk/tree/1.0.8/doc/http-request.md)

