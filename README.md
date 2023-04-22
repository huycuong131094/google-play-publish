# Google Play Publishing Script

This is a Python script that allows you to publish an application on Google Play. The script automates the process of uploading an app bundle to a release track, adding release notes, and changing the release status to completed.

## Requirements
- Python 3.x
- `google-api-python-client` module

You also need to set up a Google Cloud project with the following APIs enabled: 
- Google Play Android Developer API
- Google Cloud Storage

## Usage

To use this script, you need to run it from the command line with the following arguments:

```bash
python3 publish.py \
  --service-account-path /path/to/service/account.json \
  --track alpha \
  --package-name com.example.app \
  --bundle-path /path/to/bundle.aab \
  --release-note-path /path/to/release/note.txt \
  --release-status completed
```

The script takes the following arguments:

- `--service-account-path`: The path to the service account JSON file. This file contains the credentials required to authenticate the API request.
- `--track`: The release track to publish the app to. Valid values are `internal`, `alpha`, `beta`, or `production`.
- `--package-name`: The package name of the app.
- `--bundle-path`: The path to the app bundle (`.aab`) file.
- `--release-note-path`: The path to the release notes file.
- `--release-status`: The release status of the app. Valid values are `draft` or `completed`. The default value is `draft`.

By default, the script sets the release status to `draft`. If you want to set the release status to `completed` without being prompted for confirmation, you can use the `-y` or `--yes` option:

```bash
python3 publish.py \
  --service-account-path /path/to/service/account.json \
  --track alpha \
  --package-name com.example.app \
  --bundle-path /path/to/bundle.aab \
  --release-note-path /path/to/release/note.txt \
  --release-status completed \
  -y
```

### Example

Here's an example command to publish an app bundle on the `alpha` release track:

```bash
python3 publish.py \
  --service-account-path /path/to/service/account.json \
  --track alpha \
  --package-name com.example.app \
  --bundle-path /path/to/bundle.aab \
  --release-note-path /path/to/release/note.txt \
  --release-status completed
```

## Script Details

This script automates the following steps:

1. Authenticate the API request using the service account credentials.
2. Create a new edit for the app.
3. Upload the app bundle to the release track.
4. Set the release notes for the new release.
5. Set the release status to completed.
6. Commit the changes to the edit.

If any of the steps fail, the script will print an error message and exit.

## License

This script is released under the [MIT License](https://github.com/Open-Source-Agency/google-play-publishing-script/blob/main/LICENSE). Feel free to modify and use this script in your own projects.