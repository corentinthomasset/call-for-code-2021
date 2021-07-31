# greenup - Utilities

### Extract and save company info and market data

``ticker_info.py`` is a utility script that uses Yahoo finance to retreive and store details and market data for a given company ticker. Here is the command line options and arguments:

```asciidoc
$ python ticker_info.py --help
Usage: ticker_info.py [OPTIONS] COMPANYLIST

  Store company details (info and market data) to IBM Cloudant

  COMPANYLIST is a file containing company names.

Options:
  --cloudant-account TEXT  IBM Cloudant account  [required]
  --cloudant-api-key TEXT  IBM Cloudant API key  [required]
  -d, --debug              Show debug messages
  --help                   Show this message and exit.
```

The script expects a plain text file containing the companies' symbols; e.g. the symbol for *Apple* is *AAPL*. It will then use the __Yahoo Finance__ library to retrieve company details and its market data and will store the results in ``ticker-details-ibm-cfc`` database which is hosted on an IBM Cloudant service on *__IBM Cloud__*. It also checks whether the details have been already inserted to the data store for a given ticker.  

### Extract and save ESG ratings and indicators

``esg.py`` does two things:

* Consults __ESG Enterprise__ REST API to retrieve ESG ratings and indicators for a given company

* Stores the returned responses in the form of JSON documents in an IBM Cloudant service created on ___IBM Cloud___

Here is the the command line options and arguments:

```asciidoc
$ python esg.py --help
Usage: esg.py [OPTIONS] COMPANYLIST

  Extract ESG ratings for given companies using ESG Enterprise API

  COMPANYLIST is a file containing company names.

Options:
  --esg-api-key TEXT       ESG Enterprise API key  [required]
  --esg-api-host TEXT      ESG Enterprise API host  [default:
                           tf689y3hbj.execute-api.us-
                           east-1.amazonaws.com/prod/authorization]
  --cloudant-account TEXT  IBM Cloudant account  [required]
  --cloudant-api-key TEXT  IBM Cloudant API key  [required]
  -c, --check              Check settings
  -d, --debug              Show debug messages
  --help                   Show this message and exit.
```

The script expects a plain text file containing the companies' symbols; e.g. the symbol for _Apple_ is _AAPL_. The list of companies present in the _Russel 3000_ index can be found [here](http://www.kibot.com/Historical_Data/Russell_3000_Historical_Intraday_Data.aspx). I've also added the raw text file to the repository as a reference. It will then parses the file, takes each company's symbol and consults __ESG Enterprise__ REST API in order to receive _ESG Ratings_ and _ESG Indicators_ for the given company.

It will then store the JSON responses in two separate Cloudant databases on __IBM Cloud__:

1. `esg-indicators-ibm-cfc` which stores the indicators for all companies

2. `esg-ratings-ibm-cfc` which stores the ratings for all companies

We can then utilize Cloudant HTTP API to retrieve JSON documents from the above databases and expose them through a RESTful API.

**Note**

Please note that the script first checks whether the given ticker details exist in the data store and if not added before, it will continue the processing according to the above procedure.

---

**Warning**

If you want to examine the script, make sure that you specify the _-c_ or _--check_. Using this mode, the script uses a freely available dataset (GitHub events API) and stores the returned JSON responses into a test database on IBM Cloudant given that the connection details for IBM Cloudant are valid; otherwise, the results will be stored as files on local filesystem. Also note that GitHub limits the rate at which its API can be contacted in which case the script would not be able to store the results at all.

---

### Prerequisites

1. List of companies' symbols

2. A free account with __ISG Enterprise__ to use the ESG REST API

3. A free __IBM Cloud__ account to create the Cloudant service

### Limitations

My accounts with __ISG Enterprise__ and __IBM Cloud__ are free which pose the following limitations:

* Each day, we can only retrieve ESG ratings and indicators for 50 companies; i.e. 50 calls to the ratings endpoint and 50 calls to the indicators endpoint.

* The Cloudant service on __IBM Cloud__ allows 20 reads, 10 writes and 5 global queries per second and provides 1 GB of storage.
