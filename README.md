# Libguides Harvester

This python script can be used to quickly harvest metadata and full HTML of all LibGuides within a single organization. It uses the LibGuides API to retreive the full list of guides, then iterates over each "page" within a guide, grabbing the full html output of that page and storing it locally.  

The script builds a shallow directory structure in  `./data`, with the top level being subdirectories for each "guide" using the guide ID (as provided by the LibGuides API), as the name. Each guide directory contains:
1. `guide.json` which contains the [full metadata for the guide from the LibGuides API](#example-guidejson). 
2. `html` files for each "page" within a guide, using the page ID as the name.

The file structure looks like:
```
data/
├── 1000430
│   ├── guide.json
│   ├── page-7243525.html
│   ├── page-7243526.html
│   ├── page-7243527.html
│   └── page-7243528.html
├── 1000431
 ...
```

## Getting Started

### Requirements

You'll need:
* A recent python3 (Developed with 3.8.3)
* pipenv
* Access to your LibGuides instance API - only available to logged in users with the right credentials 
  * https://YOURDOMAIN.libapps.com/libguides/api.php?action=1&resource=1&version=1.1


### Setup
```

git checkout https://github.com/tulibraries/libguider.git

cd libguider

pipenv install --dev
```

### Usage

Simplest' usage
```
python libguider.py --site_id SITE_NUMBER --api_key YOURVERYLONGAPIKEY
Operation took 28.326523780822754 seconds
```

By default, this only harvests published guides, however, you can harvest guides with other statuses
by passing the `--guide_status` param along with a comma delimted list of status codes, as deifned in the
LibGuides API documentation.  

### Full list of usage
```
python libguider.py -h

usage: libguider.py [-h] --site_id SITE_ID --api_key API_KEY
                    [--guide_status GUIDE_STATUS]

optional arguments:
  -h, --help            show this help message and exit
  --site_id SITE_ID     Libguides Site ID
  --api_key API_KEY     Libguides API key
  --guide_status GUIDE_STATUS
                        Libguides statuses to include. ex. 1 or 1,2
```

## Why harvest it like this?
This felt like the least opinionated way to harvest this data for reuse in other pocesses. By storing the metadata with the
HTML files in a tree structure, other scripts could be written to iterate over the directories and push to a database, or ingest into solr, fairly easily. 

Also, I always prefer to start my data exploration with command line tools like grep, uniq, jq, etc., so it just worked for me,


## TODOs
* Overwrite existing HTML for pages' when they have been updated
* Clear out Guides that have been removed?



## Example guide.json
```json
{
  "id": "312",
  "type_id": "4",
  "site_id": "17",
  "owner_id": "213",
  "group_id": "139",
  "name": "Statistics,Data-Health",
  "description": "Resources to help with public health assignments and research",
  "redirect_url": "",
  "status": "1",
  "published": "2014-05-09 19:52:51",
  "created": "2014-02-25 16:42:30",
  "updated": "2020-08-24 20:03:07",
  "slug_id": "1049303",
  "friendly_url": "https://guides.temple.edu/healthstatistics",
  "nav_type": "1",
  "count_hit": "349",
  "url": "https://guides.temple.edu/c.php?g=312",
  "status_label": "Published",
  "type_label": "Topic Guide",
  "owner": {
    "id": "213",
    "first_name": "Lauri",
    "last_name": "Fennell",
    "email": "lfennell@temple.edu",
    "title": null,
    "nickname": "",
    "signature": "Lauri Fennell\nPublic Health and Social Sciences Librarian\nCharles Library\n215-204-8758\nlfennell@temple.edu",
    "created_by": "56",
    "created": "2014-02-19 16:08:20",
    "updated": "2020-06-11 13:04:40"
  },
  "group": {
    "id": 139,
    "type_id": 1,
    "name": "Health Science Libraries",
    "description": "Information and tools for the Schools of Medicine, Pharmacy, Podiatry, Dentistry,  the College of Public Health",
    "created": "2014-03-26 16:09:26",
    "updated": "2016-05-26 12:54:51",
    "slug_id": 833147,
    "slug": "hsl"
  },
  "subjects": [
    {
      "id": "19748",
      "name": "Public Health",
      "slug_id": "0"
    }
  ],
  "pages": [
    {
      "id": "1155",
      "type_id": "1",
      "name": "Introduction-Resources",
      "description": "",
      "redirect_url": "",
      "parent_id": "0",
      "source_id": "0",
      "created": "2014-02-25 16:42:30",
      "updated": "2019-10-15 12:58:13",
      "num_cols": "2",
      "column_layout": "{\"1\":{\"span\":\"6\"},\"2\":{\"span\":\"6\"}}",
      "enable_display": "1",
      "enable_newwin": "0",
      "position": "1",
      "url": "https://guides.temple.edu/c.php?g=312&p=1155",
      "slug_id": "37001",
      "friendly_url": "https://guides.temple.edu/healthstats",
      "er_course_id": "0"
    },
    {
      "id": "12411",
      "type_id": "1",
      "name": "Special Topics",
      "description": "Disease specific and other specific topics",
      "redirect_url": "",
      "parent_id": "0",
      "source_id": "0",
      "created": "2014-04-23 13:47:05",
      "updated": "2015-03-25 00:37:07",
      "num_cols": "3",
      "column_layout": "{\"1\":{\"span\":3},\"2\":{\"span\":6},\"3\":{\"span\":3}}",
      "enable_display": "1",
      "enable_newwin": "0",
      "position": "4",
      "url": "https://guides.temple.edu/c.php?g=312&p=12411",
      "slug_id": "0",
      "friendly_url": null,
      "er_course_id": "0"
    }
  ]
}
```