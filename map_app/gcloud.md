# Navigate and use gcloud

Our map identifiers / keys
api_key = "***REMOVED***"
our_map_id = "1a3de3b04bbcad29"


```sh
# List projects
$ gcloud projects list
# Select a project
$ gcloud config set project PROJECT_ID
# List enabled apis, services
$ gcloud services list
# List api keys for the current project
$ gcloud alpha services api-keys list
# Create api keys for the current project
$ gcloud alpha services api-keys create --project PROJECT_NAME --display-name DISPLAY_NAME


```