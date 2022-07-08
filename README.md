# SWEE - Find SWE Internships
![Style Check](https://github.com/fp456/SEO-proj1/actions/workflows/style.yaml/badge.svg)

Find software engineering internships easily with swee and have fun while doing so. Enter a location and swipe left or right to review internships.

## Prerequisites

* Sign up for an [Adzuna developer account](https://developer.adzuna.com) in order to get an Application ID and key. 
* Have Python 3 installed.

## Setup instructions
### Environment Variables
In order to run our program you will need to set up some environment variables. You can find your Application ID and Application key in the "API Access Details" section of the developer dashboard.

You will need to export your Application ID and Application key in your terminal as environment variables. Replace <your_application_id> and <your_application_key> with your own credentials.
```
export ADZUNA_ID_KEY='<your_application_id>'
export ADZUNA_KEY='<your_application_key>'
```

### Additional Libraries

You will need to install the requests package. You can install it as follows:

```
pip install requests
```

## How to Use

In the main menu, select if you want to search jobs, view the saved jobs, or quit. 

To search jobs, write the country and location of the internships desired. The program is going to return a list of all the internships that match those requirements, sorted by relevance. Then, using the ```n``` key, move to the next job. To save a job, use the ```s``` key and to go back to the main menu, press the ```m``` key.

To view the saved jobs, press the ```n``` key to see the next job or ```p``` to show the previous one. You can also delete a saved job.