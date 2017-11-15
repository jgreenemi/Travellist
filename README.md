## Travellist 

### Prereqs

- Python 3.+
- Boto 3.+

See `requirements.txt` for the full list.

### Setup

```bash
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt 
```

### Roadmap

[x] Store mock data in Dynamo.
[ ] Retrieve data from Dynamo.
[ ] Create a RESTful API that can display data from Dynamo.
[ ] Retrieve data programmatically from an external source.
[ ] Standardize the data as its pulled in from external sources. (Will likely need a different source for each country, so different response handling will be necessary.) 
[ ] Create a means of taking filter parameter input from the API and return matching records.
[ ] Create a web-browser frontend to use the API.
[ ] Create a user profile system whereby a user's filter history can be stored.
[ ] Introduce MXnet to pull data based on a user's profile.
[ ] Create a logistic regression algorithm to determine what a user is likely to be interested in based on past filters.
[ ] Incorporate a user's preferences into future searches. 
[ ] Introduce a means of resetting parameters.

#### Roadmap Bonus Items

[ ] Create an Alexa Skill that uses this API, translating user requests to filter options.