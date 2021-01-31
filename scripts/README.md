# FreeFrom Map Forms - Google Apps Script

This script is intended to be deployed as a web app in the Google Apps Script console. It accepts form fields, writes them to a Google Sheet, and sends an email notification.

Message the #freefrom-map-dev Slack channel for the API URL!

## Request format

The app accepts requests of the form `POST {app url}`, with the data body for each form in the formats below. This should be updated if the Google Sheet format is changed.

Aside from `form`, all fields are optional.

### Give Feedback

```js
{
    "form": "feedback",  // required
    "useful": "",
    "useful_desc": "",
    "learned": "",
    "usage_plan": [""],
    "suggestions": ""
}
```

### Report Missing or Outdated Information

```js
{
    "form": "report_missing_info",  // required
    "information": "",
    "email": ""
}
```

### Partner with FreeFrom

```js
{
    "form": "partner_with_freefrom",  // required
    "name": "",
    "email": "",
    "pronouns": "",
    "organization": "",
    "title": "",
    "state": "",
    "goals": [""],
    "process_phase": [""]
}
```

### Build Collective Survivor Power

```js
{
    "form": "build_collective_survivor_power",  // required
    "name": "",
    "pronouns": "",
    "interests": [""],
    "contact_preference": "",
    "phone": "",
    "email": ""
}
```

### Share your Policy Ideas

```js
{
    "form": "policy_ideas",  // required
    "prioritize_policies": "",
    "missing_policies": "",
    "state": "",
    "name": "",
    "pronouns": "",
    "email": ""
}
```
