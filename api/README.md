<p align="center">
    <a href="https://cloud.ibm.com">
        <img src="https://cloud.ibm.com/media/docs/developer-appservice/resources/ibm-cloud.svg" height="100" alt="IBM Cloud">
    </a>
</p>

<p align="center">
    <a href="https://cloud.ibm.com">
    <img src="https://img.shields.io/badge/IBM%20Cloud-powered-blue.svg" alt="IBM Cloud">
    </a>
    <img src="https://img.shields.io/badge/platform-python-lightgrey.svg?style=flat" alt="platform">
    <img src="https://img.shields.io/badge/license-Apache2-blue.svg?style=flat" alt="Apache 2">
</p>

# ESG REST API

This is a Flask-based RESTful API that exposes the following data items:

* ESG Ratings for a given company

* ESG Indicators for a given company

* Details and market data for a given company

## Endpoints

### /health

#### GET

##### Description:

Get health status of the Flask application

##### Responses

| Code | Description           | Schema                            |
| ---- | --------------------- | --------------------------------- |
| 200  | Health check response | [healthResponse](#healthResponse) |

### /metrics

#### GET

##### Description:

Get Prometheus metrics

##### Responses

| Code | Description        |
| ---- | ------------------ |
| 200  | Prometheus metrics |

### /ratings/{symbol}

#### GET

##### Description:

Get ESG ratings for a given company

##### Parameters

| Name   | Located in | Description            | Required | Schema |
| ------ | ---------- | ---------------------- | -------- | ------ |
| symbol | path       | Company's stock symbol | Yes      | string |

##### Responses

| Code | Description | Schema                    |
| ---- | ----------- | ------------------------- |
| 200  | ESG ratings | [ESGRatings](#ESGRatings) |

### /indicators/{symbol}

#### GET

##### Description:

Get ESG indicators for a given company

##### Parameters

| Name   | Located in | Description            | Required | Schema |
| ------ | ---------- | ---------------------- | -------- | ------ |
| symbol | path       | Company's stock symbol | Yes      | string |

##### Responses

| Code | Description    | Schema                          |
| ---- | -------------- | ------------------------------- |
| 200  | ESG indicators | [ESGIndicators](#ESGIndicators) |

### /catchall/{symbol}

#### GET

##### Description:

Get all details for a given company. These details include:

* Info

* Market data

* ESG ratings

* ESG indicators

* Market data correlation to DJIA index

##### Parameters

| Name   | Located in | Description                                                         | Required | Schema |
| ------ | ---------- | ------------------------------------------------------------------- | -------- | ------ |
| symbol | path       | Company's stock symbol                                              | Yes      | string |
| period | query      | Fetch market data for the given company during the specified period | No       | string |

##### Responses

| Code | Description     | Schema                |
| ---- | --------------- | --------------------- |
| 200  | Company details | [catchAll](#catchAll) |

### Models

#### healthResponse

| Name   | Type   | Description | Required |
| ------ | ------ | ----------- | -------- |
| status | string |             | No       |

#### ESGRatings

| Name                 | Type    | Description | Required |
| -------------------- | ------- | ----------- | -------- |
| _id                  | string  |             | No       |
| _rev                 | string  |             | No       |
| company_name         | string  |             | No       |
| disclaimer           | string  |             | No       |
| environment_grade    | string  |             | No       |
| environment_level    | string  |             | No       |
| environment_score    | integer |             | No       |
| esg_id               | integer |             | No       |
| exchange_symbol      | string  |             | No       |
| governance_grade     | string  |             | No       |
| governance_level     | string  |             | No       |
| governance_score     | integer |             | No       |
| last_processing_date | string  |             | No       |
| social_grade         | string  |             | No       |
| social_level         | string  |             | No       |
| social_score         | integer |             | No       |
| stock_symbol         | string  |             | No       |
| total                | integer |             | No       |
| total_grade          | string  |             | No       |
| total_level          | string  |             | No       |

#### ESGIndicators

| Name            | Type       | Description | Required |
| --------------- | ---------- | ----------- | -------- |
| _id             | string     |             | No       |
| _rev            | string     |             | No       |
| company_name    | string     |             | No       |
| disclaimer      | string     |             | No       |
| esg_id          | integer    |             | No       |
| exchange_symbol | string     |             | No       |
| goals           | [ object ] |             | No       |
| stock_symbol    | string     |             | No       |

#### catchAll

| Name        | Type   | Description | Required |
| ----------- | ------ | ----------- | -------- |
| target      | string |             |          |
| inidicators | object |             | No       |
| ratings     | object |             | No       |

#### Deployment

The API is deployed on IBM Cloud using a K8 cluster and an automated CI/CD pipeline.

#### Development

* Install [Python](https://www.python.org/downloads/)

Running Flask applications has been simplified with a `manage.py` file to avoid dealing with configuring environment variables to run your app. From your project root, you can download the project dependencies with (NOTE: If you don't have pipenv installed, execute: `pip install pipenv`):

```bash
pipenv install
```

Then, activate this app's virtualenv:

```bash
pipenv shell
```

To run your application locally, run this inside the virtualenv:

```bash
python manage.py start
```

`manage.py` offers a variety of different run commands to match the proper situation:

* `start`: starts a server in a production setting using `gunicorn`.
* `run`: starts a native Flask development server. This includes backend reloading upon file saves and the Werkzeug stack-trace debugger for diagnosing runtime failures in-browser.
* `livereload`: starts a development server via the `livereload` package. This includes backend reloading as well as dynamic frontend browser reloading. The Werkzeug stack-trace debugger will be disabled, so this is only recommended when working on frontend development.
* `debug`: starts a native Flask development server, but with the native reloader/tracer disabled. This leaves the debug port exposed to be attached to an IDE (such as PyCharm's `Attach to Local Process`).

There are also a few utility commands:

* `build`: compiles `.py` files within the project directory into `.pyc` files
* `test`: runs all unit tests inside of the project's `test` directory

Your application is running at: `http://localhost:3000/` in your browser.

- Your [Swagger UI](http://swagger.io/swagger-ui/) is running on: `/explorer`
- Your Swagger definition is running on: `/swagger/api`
- Health endpoint: `/health`

There are two different options for debugging the Flask project:

1. Run `python manage.py runserver` to start a native Flask development server. This comes with the Werkzeug stack-trace debugger, which will present runtime failure stack-traces in-browser with the ability to inspect objects at any point in the trace. For more information, see [Werkzeug documentation](http://werkzeug.pocoo.org/).
2. Run `python manage.py debug` to run a Flask development server with debug exposed, but the native debugger/reloader turned off. This grants access for an IDE to attach itself to the process (i.e. in PyCharm, use `Run` -> `Attach to Local Process`).

You can also verify the state of your locally running application using the Selenium UI test script included in the `scripts` directory.

> **Note for Windows users:** `gunicorn` is not supported on Windows. You may start the server with `python manage.py run` on your local machine or build and start the Dockerfile.

#### IBM Cloud Developer Tools

Install [IBM Cloud Developer Tools](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started) on your machine by running the following command:

```
curl -sL https://ibm.biz/idt-installer | bash
```

Create an application on IBM Cloud by running:

```bash
ibmcloud dev create
```

This will create and download a starter application with the necessary files needed for local development and deployment.

Your application will be compiled with Docker containers. To compile and run your app, run:

```bash
ibmcloud dev build
ibmcloud dev run
```

This will launch your application locally. When you are ready to deploy to IBM Cloud on Cloud Foundry or Kubernetes, run one of the commands:

```bash
ibmcloud dev deploy -t buildpack // to Cloud Foundry
ibmcloud dev deploy -t container // to K8s cluster
```

You can build and debug your app locally with:

```bash
ibmcloud dev build --debug
ibmcloud dev debug
```
