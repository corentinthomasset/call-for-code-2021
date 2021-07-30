# GreenUp

## Contents

- [GreenUp](#greenup)
  
  - [Contents](#contents)
  
  - [The problem](#the-problem)
  
  - [How can technology help?](#how-can-technology-help)
  
  - [The idea](#the-idea)
  
  - [Demo video](#demo-video)
  
  - [Architecture](#architecture)
  
  - [Details](#details)
  
  - [Roadmap](#roadmap)
  
  - [Getting started](#getting-started)
  
  - [Live demo](#live-demo)
  
  - [Built with](#built-with)
  
  - [Contributing](#contributing)
  
  - [Versioning](#versioning)
  
  - [Authors](#authors)
  
  - [License](#liecense)
  
  - [Acknowledgments](#acknowledgments)

## The problem

## How can technology help?

## The idea

*GreenUp* is an application that allows investors to arrange/re-arrange their investment portfolio according to companies' ESG (Enviromental, Social and Governance) performance. This is acheived by suggesting stocks that have higher ESG ratings and, in the mean time, perform similar to what the user already has in his/her investment portfolio.

## Demo video

## Architecture

Check the below diagram:

![GreenUp Architecture](./docs/greenup_arch.png "GreenUp Architecture")

## Details

Technically speaking, the application has three main components:

1. Data store: A repository where ESG ratings and indicators along with stock correlation data is stored. We use resources like ***ESG Enterprise*** and ***Yahoo Finance*** to extract these data and store it in the ***IBM Cloud***.

2. API: A RESTful API in front of the data store which exposes the data in the form of services consumable by the UI.

3. UI: A web-based and Mobile application which leverages the API to implement/deliver the idea to the end users.

## Roadmap

## Getting started

## Live demo

| Endpoint | Address                                         |
| -------- | ----------------------------------------------- |
| API      | http://52.117.182.214:31587/swagger/api-docs/#/ |
| UI       | http://corentinthomasset.me/call-for-code/#/    |

## Built with

- [IBM Cloudant](https://cloud.ibm.com/catalog?search=cloudant#search_results) - Storage for JSON documents

- [Python Flask](https://flask.palletsprojects.com/en/2.0.x/) - REST API

- [Vue.js](https://vuejs.org/) - User interface

- [Kubernetes on IBM Cloud](https://cloud.ibm.com/catalog?search=kubernetes%20service#search_results) - Service infrastructure

## Contributing

* Fork the repository.

* Commit your changes to your fork.

* Submit a pull request.

* Handle any feedback before the request is merged.

## Versioning

## Authors

## License

This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ESG Enterprise](https://www.esgenterprise.com/) for providing access to their ESG API
