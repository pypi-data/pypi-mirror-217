import datetime
import io
import mimetypes
import os
import shutil
import time
import hashlib

from apiclient import discovery
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive']

GOOGLE_MIME_TYPES = {
    'application/vnd.google-apps.document':
        ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',
         '.docx'],
    'application/vnd.google-apps.spreadsheet':
        ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
         '.xlsx'],
    'application/vnd.google-apps.presentation':
        ['application/vnd.openxmlformats-officedocument.presentationml.presentation',
         '.pptx']
}


def folder_upload(service, local_folder: str):
    parents_id = {}

    for root, _, files in os.walk(local_folder, topdown=True):
        last_dir = root.split('/')[-1]
        pre_last_dir = root.split('/')[-2]
        if pre_last_dir not in parents_id.keys():
            pre_last_dir = []
        else:
            pre_last_dir = parents_id[pre_last_dir]

        folder_metadata = {'name': last_dir,
                           'parents': [pre_last_dir],
                           'mimeType': 'application/vnd.google-apps.folder'}
        create_folder = service.files().create(body=folder_metadata,
                                               fields='id').execute()
        folder_id = create_folder.get('id', [])

        for name in files:
            file_metadata = {'name': name, 'parents': [folder_id]}
            media = MediaFileUpload(
                os.path.join(root, name),
                mimetype=mimetypes.MimeTypes().guess_type(name)[0])
            service.files().create(body=file_metadata,
                                   media_body=media,
                                   fields='id').execute()

        parents_id[last_dir] = folder_id

    return parents_id


def check_upload(service, local_folder: str, remote_folder: str):
    results = service.files().list(
        pageSize=100,
        q="'root' in parents and trashed != True and \
        mimeType='application/vnd.google-apps.folder'").execute()

    items = results.get('files', [])

    # Check if folder exists, and then create it or get this folder's id.
    if remote_folder in [item['name'] for item in items]:
        folder_id = [item['id'] for item in items
                     if item['name'] == remote_folder][0]
    else:
        parents_id = folder_upload(service, local_folder)
        folder_id = parents_id[remote_folder]

    return folder_id, local_folder


def get_credentials(creds_file: str, token_file: str):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_tree(folder_name, tree_list, root, parents_id, service):
    """Gets folder tree relative paths.

    Recursively gets through subfolders, remembers their names ad ID's.

    Args:
        folder_name: Name of folder, initially
        name of parent folder string.
        folder_id: ID of folder, initially ID of parent folder.
        tree_list: List of relative folder paths, initially
        empy list.
        root: Current relative folder path, initially empty string.
        parents_id: Dictionary with pairs of {key:value} like
        {folder's name: folder's Drive ID}, initially empty dict.
        service: Google Drive service instance.

    Returns:
        List of folder tree relative folder paths.

    """
    folder_id = parents_id[folder_name]

    results = service.files().list(
        pageSize=100,
        q=("%r in parents and \
        mimeType = 'application/vnd.google-apps.folder'and \
        trashed != True" % folder_id)).execute()

    items = results.get('files', [])
    root += folder_name + os.path.sep

    for item in items:
        parents_id[item['name']] = item['id']
        tree_list.append(root + item['name'])
        folder_id = [i['id'] for i in items
                     if i['name'] == item['name']][0]
        folder_name = item['name']
        get_tree(folder_name, tree_list,
                 root, parents_id, service)


def download_file_from_gdrive(file_path, drive_file, service):
    """Downloads file from Google Drive.

    If file is Google Doc's type, then it will be downloaded
    with the corresponding non-Google mimetype.

    Args:
        path: Directory string, where file will be saved.
        file: File information object (dictionary), including it's name, ID
        and mimeType.
        service: Google Drive service instance.
    """
    file_id = drive_file['id']
    file_name = drive_file['name']
    if drive_file['mimeType'] in GOOGLE_MIME_TYPES.keys():
        if file_name.endswith(GOOGLE_MIME_TYPES[drive_file['mimeType']][1]):
            file_name = drive_file['name']
        else:
            file_name = '{}{}'.format(
                drive_file['name'],
                GOOGLE_MIME_TYPES[drive_file['mimeType']][1])
            service.files().update(fileId=file_id,
                                   body={'name': file_name}).execute()

        request = service.files().export(
            fileId=file_id,
            mimeType=(GOOGLE_MIME_TYPES[drive_file['mimeType']])[0]).execute()
        with io.FileIO(os.path.join(file_path, file_name), 'wb') as file_write:
            file_write.write(request)

    else:
        request = service.files().get_media(fileId=file_id)
        file_io = io.FileIO(os.path.join(file_path, drive_file['name']), 'wb')
        downloader = MediaIoBaseDownload(file_io, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()


def by_lines(input_str):
    """Helps Sort items by the number of slashes in it.

    Returns:
        Number of slashes in string.
    """
    return input_str.count(os.path.sep)


def download(creds_file: str, local_folder: str, remote_folder: str):
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials(creds_file, 'token.json')
    service = discovery.build('drive', 'v3', credentials=credentials)
    service._http.timeout = 10000  # Set the timeout value (in seconds)

    # Get id of Google Drive folder and it's path (from other script)
    # folder_id, full_path = initial_upload.check_upload(service)
    folder_id, full_path = check_upload(service, local_folder, remote_folder)
    folder_name = full_path.split(os.path.sep)[-1]
    tree_list, root, parents_id = [], '', {}

    # About_drive = service.about().get(
    # fields='importFormats, exportFormats').execute()
    # print(About_drive)
    parents_id[folder_name] = folder_id
    get_tree(folder_name, tree_list, root, parents_id, service)
    os_tree_list = []
    root_len = len(full_path.split(os.path.sep)[0:-2])

    # Get list of folders three paths on computer
    for root, dirs, files in os.walk(full_path, topdown=True):
        for name in dirs:
            var_path = (os.path.sep).join(
                root.split(os.path.sep)[root_len + 1:])
            os_tree_list.append(os.path.join(var_path, name))

    # old folders on computer
    download_folders = list(set(tree_list).difference(set(os_tree_list)))
    # new folders on computer, which you dont have(i suppose heh)
    remove_folders = list(set(os_tree_list).difference(set(tree_list)))
    # foldes that match
    exact_folders = list(set(os_tree_list).intersection(set(tree_list)))

    exact_folders.append(folder_name)

    var = (os.path.sep).join(full_path.split(os.path.sep)[0:-1]) + os.path.sep

    # Download folders from Drive
    download_folders = sorted(download_folders, key=by_lines)

    for folder_dir in download_folders:
        variable = var + folder_dir
        last_dir = folder_dir.split(os.path.sep)[-1]

        folder_id = parents_id[last_dir]
        results = service.files().list(
            pageSize=20, q=('%r in parents and trashed = false' % folder_id)).execute()

        items = results.get('files', [])
        os.makedirs(variable)
        files = [f for f in items
                 if f['mimeType'] != 'application/vnd.google-apps.folder']

        for drive_file in files:
            # file_id = f['id']
            download_file_from_gdrive(variable, drive_file, service)

    # Check and refresh files in existing folders
    for folder_dir in exact_folders:
        # var = '/'.join(full_path.split('/')[0:-1]) + '/'
        variable = var + folder_dir
        last_dir = folder_dir.split(os.path.sep)[-1]
        os_files = [f for f in os.listdir(variable)
                    if os.path.isfile(os.path.join(variable, f))]
        folder_id = parents_id[last_dir]

        results = service.files().list(
            pageSize=1000,
            q=('%r in parents and \
            mimeType!="application/vnd.google-apps.folder" and trashed = false' % folder_id),
            fields="files(id, name, mimeType, \
                modifiedTime, md5Checksum)").execute()

        items = results.get('files', [])

        refresh_files = [f for f in items if f['name'] in os_files]
        upload_files = [f for f in items if f['name'] not in os_files]
        remove_files = [f for f in os_files
                        if f not in [j['name'] for j in items]]

        for drive_file in refresh_files:
            file_dir = os.path.join(variable, drive_file['name'])
            file_time = os.path.getmtime(file_dir)
            # mtime = drive_file['modifiedTime']
            mtime = datetime.datetime.strptime(drive_file['modifiedTime'][:-2],
                                               "%Y-%m-%dT%H:%M:%S.%f")
            drive_time = time.mktime(mtime.timetuple())

            file_dir = os.path.join(variable, drive_file['name'])
            os_file_md5 = hashlib.md5(open(file_dir, 'rb').read()).hexdigest()
            if 'md5Checksum' in drive_file.keys():
                # print(1, file['md5Checksum'])
                drive_md5 = drive_file['md5Checksum']
                # print(2, os_file_md5)
            else:
                drive_md5 = None

            if (file_time < drive_time) or (drive_md5 != os_file_md5):
                os.remove(os.path.join(variable, drive_file['name']))
                download_file_from_gdrive(variable, drive_file, service)

        for os_file in remove_files:
            os.remove(os.path.join(variable, os_file))

        for drive_file in upload_files:
            download_file_from_gdrive(variable, drive_file, service)

    # Delete old and unwanted folders from computer
    # remove_folders = sorted(remove_folders, key=by_lines, reverse=True)

    # for folder_dir in remove_folders:
    #     # var = '/'.join(full_path.split('/')[0:-1]) + '/'
    #     variable = var + folder_dir
    #     last_dir = folder_dir.split(os.path.sep)[-1]
    #     shutil.rmtree(variable)
