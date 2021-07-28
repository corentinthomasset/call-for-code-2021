# EnvEst (IBM Call for Code 2021)

## The idea

*EnvEst* is an application that allows investors to arrange/re-arrange their investment portfolio according to companies' ESG (Enviromental, Social and Governance) performance. This is acheived by suggesting stocks that have higher ESG ratings and, in the mean time, perform similar to what the user already has in his/her investment portfolio.

Technically speaking, the application has three main components:

1. Data store: A repository where ESG ratings and indicators along with stock correlation data is stored. We use resources like *__ESG Enterprise__* and *__Yahoo Finance__* to extract these data and store it in the *__IBM Cloud__*. 

2. API: A RESTful API in front of the data store which exposes the data in the form of services consumable by the UI. 

3. UI: A web-based and Mobile application which leverages the API to implement/deliver the idea to the end users.
