from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
from utils import read_release_note
import mimetypes
mimetypes.add_type('application/octet-stream', '.aab')

parser = argparse.ArgumentParser(description='Google Play Publishing Script')

parser.add_argument('-s', '--service-account-path', type=str, help='Service account path', required=True)
parser.add_argument('-t', '--track', type=str, help='Release track', required=True)
parser.add_argument('-p', '--package-name', type=str, help='Package name', required=True)
parser.add_argument('-b', '--bundle-path', type=str, help='Bundle path to upload', required=True)
parser.add_argument('-r', '--release-note-path', type=str, help='Release note path', required=True)
parser.add_argument('--release-status', choices=['draft', 'completed'], help='Set release status. Default is draft', default='draft')

args = parser.parse_args()

service_account_path=args.service_account_path
track=args.track
package_name=args.package_name
bundle_path=args.bundle_path
release_note_path=args.release_note_path
release_status=args.release_status


if None in [service_account_path, track, package_name, bundle_path, release_note_path]:
    parser.error("All arguments are required. Please provide values for all arguments.")

print('------------------SETUP INFORMATION-------------------')
print('All required argument populated successfully')

# Print the values of the arguments
print("Service Account Path: ", service_account_path)
print("Track: ", track)
print("Package Name: ", package_name)
print("Bundle Path: ", bundle_path)
print("Release Note Path: ", release_note_path)
print("Release Status: ", release_status)
print('------------------SETUP INFORMATION-------------------')

# Load the credentials from the JSON file
creds = Credentials.from_service_account_file(service_account_path, scopes=['https://www.googleapis.com/auth/androidpublisher'])

# Build the Android Publisher API service
android_publisher = build('androidpublisher', 'v3', credentials=creds)

# You can now use the `android_publisher` service object to make API requests
# For example, you can create an internal testing track for a production release

def create_edit(package_name):
    try:
        edit_info = android_publisher.edits().insert(
            packageName=package_name,
            body={}
        ).execute()
        edit_id = edit_info['id']
        return edit_id
    except HttpError as error:
        print(f'Failed to create new edit: {error}')
        raise

def upload_bundle(edit_id, package_name, bundle_file_path):
    try:
        upload_response = android_publisher.edits().bundles().upload(
            editId=edit_id,
            packageName=package_name,
            media_body=bundle_file_path
        ).execute()
        return upload_response
    except HttpError as error:
        print(f'Failed to upload APK or App Bundle: {error}')
        raise

def update_track_with_release_notes(edit_id, package_name, track, versionCode, release_notes, release_status):
    """Update the track with release notes."""
    try:
        release = {
            'versionCodes': [versionCode],
            'status': release_status,
            'releaseNotes': [{'language': 'en-US', 'text': release_notes}]
        }
        android_publisher.edits().tracks().update(
            editId=edit_id,
            packageName=package_name,
            track=track,
            body={'releases': [release]}
        ).execute()
    except HttpError as error:
        print(f'Failed to update track with release notes: {error}')
        raise

def commit_changes(edit_id, package_name):
    """Commit the changes made in the given edit."""
    try:
        android_publisher.edits().commit(
            editId=edit_id,
            packageName=package_name
        ).execute()
    except HttpError as error:
        print(f'Failed to commit changes: {error}')
        raise

def discard_edit(edit_id, package_name):
    try:
        android_publisher.edits().delete(
            editId=edit_id,
            packageName=package_name
        ).execute()
    except HttpError as error:
        print(f'An error occurred while discarding edit: {error}')
        raise

def performingReleaseProcess(edit_id, package_name, release_notes, bundle_path, track, release_status):
    try:
        print(f'Uploading {bundle_path} for edit {edit_id}')
        upload_response = upload_bundle(edit_id, package_name, bundle_path)
        print('Upload bundle successfully')

        version_code = upload_response['versionCode']
        print(f'Bundle version code {version_code}')

        print('Starting to update edit with release notes')
        update_track_with_release_notes(edit_id, package_name, track,  version_code, release_notes, release_status)
        print('Update track successfully')

        print('Starting to commit the changes')
        commit_changes(edit_id, package_name)
        print('Commit changes successfully')
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise
    except:
        discard_edit(edit_id, package_name)
        print(f'Successfully discard edit {edit_id}')
        raise

try:
    release_notes=read_release_note(release_note_path)
    print(f'Extract release note successfully. Release content:\n{release_notes}')

    edit_id = create_edit(package_name)
    print('Create release edit successfully')

    print('Starting to perform release process')
    performingReleaseProcess(
        edit_id=edit_id,
        bundle_path=bundle_path,
        package_name=package_name,
        release_notes=release_notes,
        track=track,
        release_status=release_status
    )
    print('Release process completed successfully')

except HttpError as error:
    print(f'An error occurred: {error}')
