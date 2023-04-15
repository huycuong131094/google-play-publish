from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse

parser = argparse.ArgumentParser(description='Google Play Publishing Script')

parser.add_argument('-s', '--service-account-path', type=str, help='Service account path', required=True)
parser.add_argument('-t', '--track', type=str, help='Release track', required=True)
parser.add_argument('-p', '--package-name', type=str, help='Package name', required=True)
parser.add_argument('-b', '--bundle-path', type=str, help='Bundle path to upload', required=True)
parser.add_argument('-r', '--release-note-path', type=str, help='Release note path', required=True)

args = parser.parse_args()

service_account_path=args.service_account_path
track=args.track
package_name=args.package_name
bundle_path=args.bundle_path
release_note_path=args.release_note_path


if None in [service_account_path, track, package_name, bundle_path, release_note_path]:
    parser.error("All arguments are required. Please provide values for all arguments.")

# Print the values of the arguments
print("Service Account Path: ", service_account_path)
print("Track: ", track)
print("Package Name: ", package_name)
print("Bundle Path: ", bundle_path)
print("Release Note Path: ", release_note_path)

# Load the credentials from the JSON file
creds = Credentials.from_service_account_file(service_account_path, scopes=['https://www.googleapis.com/auth/androidpublisher'])

# Build the Android Publisher API service
android_publisher = build('androidpublisher', 'v3', credentials=creds)

# You can now use the `android_publisher` service object to make API requests
# For example, you can create an internal testing track for a production release
try:
    edit_info = android_publisher.edits().insert(
        packageName=package_name,
        body={}
    ).execute()
    edit_id = edit_info['id']

    track_info = android_publisher.edits().tracks().get(
        editId=edit_id,
        packageName=package_name,
        track=track
    ).execute()
    releases = track_info.get('releases', [])
    print(releases)
except HttpError as error:
    print(f'An error occurred: {error}')

# Print the response
