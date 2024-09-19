# Zeus-Google Calendar Sync

This Python project provides a utility to synchronize timetable data from **Zeus** (a timetable manager) with **Google Calendar**. It helps ensure your calendar stays up-to-date with any changes made in Zeus, including adding, modifying, and deleting events.

## Features

- **Automated Syncing**: Automatically syncs events from Zeus to Google Calendar.
- **Add New Classes**: Add new events from Zeus to Google Calendar.
- **Delete Events**: Remove all events related to the Zeus timetable from Google Calendar.
- **Event Fetching**: Retrieve and display events from Google Calendar.
- **Update Events**: Synchronize changes from Zeus to Google Calendar to ensure that the two platforms are always aligned.

## Prerequisites

1. **Google Calendar API Setup**:
   - You will need to set up a project in the [Google Cloud Console](https://console.cloud.google.com/) and enable the Google Calendar API.
   - Download the `credentials.json` file for OAuth 2.0 and place it in the root directory of your project.

2. **Zeus Timetable Manager**:
   - Get your office access token on [microsoft graph explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) from your school account.
   - Put it in a file named `office_token.txt` at the root of the project. This token will allow the app to access to your timetable.

3. **Install python libraries**:
   - Install the Google API Python client:
     ```bash
     pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
     ```
   - Install the requests library:
     ```bash
     pip install requests
     ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kilso80/zeusToCalendar.git
   ```

2. Ensure the `credentials.json` file is in the root folder for Google Calendar API authentication.

## Usage

### Main Script: `main.py`

The primary script to run the syncing process between Zeus and Google Calendar is `main.py`. It integrates the functionality from various modules such as adding, updating, and deleting events.

Run the script as follows:

```bash
python main.py
```

### Module Overview

- **`actualize.py`**: This script provides a function handling the synchronization of events between Zeus and Google Calendar. It ensures that changes in Zeus are reflected in your Google Calendar, such as updating modified events.
  
- **`addNewClass.py`**: Use this script to create an agenda for a new class group.

- **`deleteEverything.py`**: This script provides a function deleting all events related to Zeus from Google Calendar.

- **`eventGetter.py`**: Retrieves and lists events from Zeus for a specific class group.

### How to add a New Class

To add new classes from Zeus to Google Calendar:

```bash
python addNewClass.py
```


## Configuration

- **Google Calendar Credentials**: Place the OAuth credentials file (`credentials.json`) in the root directory.
  
- **Zeus API/Configuration**: Ensure you have access to Zeus timetable data and that the necessary API credentials are configured in your project.

## Troubleshooting

- **Authentication Issues**: If you encounter issues with Google Calendar authentication, delete the `token.json` file and re-run the program to authenticate again.
