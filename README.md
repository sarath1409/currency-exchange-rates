# Exchange Rate

A service that gives the **latest and historical exchange rate** for the currency
[Go to deployed code](https://exchange-rates-flask-app.herokuapp.com/)

## Tech and libs used

Python, Flask, HTML, CSS, sqlite3, jinja


## API used

[Open Exchange Rates](https://openexchangerates.org/)

## Solution-focus

Backend - Logging, Exception handling, Modular code, Scalability
Frontend - Form validation, custom syling

## Solution approach

 - **User Input**: date between 1 Jan 1999 and Today, number of days (x) to get historical exchange rates (1-7 days).
 -  **Output**: Exchange rates of multiple currencies for latest x number of dates.
 -  API provides only 1000 free requests per month. So everytime a new request is made by user backend data is verified and inserted if not present.
 -  This overcomes the request limit issue of api and also improves performance.
 -  The results are populated as a HTML table.

## Trade offs

- To create a SPA with React. 
- Add trendlines in webpage instead of tabular data.

### Contact
[LinkedIn](https://www.linkedin.com/in/sarath-chandra5/)
[Mail](p.g.sarathchandra@gmail.com)