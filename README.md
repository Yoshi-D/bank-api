This is an API used to fetch bank details from the database, which is a huge csv file here. The csv contains columns like ifsc code, bank id, addresses, etc. 
I have used pandas .head() function to get the rows when /banks is called as I am only returning the first few rows as it is not feasible to return all the rows. I have given a limit parameter to display {limit} number of rows. Default value is 100.

Then I have used FastAPI to specify which routes are for what function. For getting specific bank_id banks, /banks/bank_id=...  endpoint is used. Similarly for ifsc codes, /banks/ifsc=..  endpoint is used. Errors are handled gracefully and 404 status code is returned if nothing is found and 400 is returned if an incorrect limit is sent through. I have kept a range of 1-8250 for the limit parameter.

Render url: https://yashs-bank-api.onrender.com
(add /docs at the end of the url to try all of the endpoints)

I have provided the banks csv file for reference.

Time taken: About 4-5 hours.

In the future, I could add API key authentication. Open to any contributions.
