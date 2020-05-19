# labmojo

In /archive, there is the original data file, `all-duplicate.json` & test script.

## Data
The data to query is in `all.json`

# Scholarly
I was having issues with too many requests and hitting Timeouts. What I did:

* Pull in Scholarly into the app
* This is using a proxy

# Query Scholar

`python3 script.py`

Is the file to run for:
* Looping over `all.json`
* Query each researcher against `scholarly`
* Save the results in `/results`
