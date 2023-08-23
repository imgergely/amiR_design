import streamlit as st
import dropbox  
import os

def dropbox_list_files(path):
    dbx = dropbox_connect()
    try:
        files = dbx.files_list_folder(path).entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                files_list.append(file.path_display)

        return files_list

    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


def dropbox_connect():
    try:
        dbx = dropbox.Dropbox(st.secrets["access_token"])
    except Exception as e:
        st.write('Error connecting to Database: ' + str(e))
    return dbx


def dropbox_download_files():
    local_folder_path = "db"
    flag_file_path = os.path.join(local_folder_path, "downloaded.flag")

    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)

    if not os.path.exists(flag_file_path):
        try:
            dbx = dropbox_connect()
            file_paths = dropbox_list_files("/db")

            for dropbox_file_path in file_paths:
                local_file_path = os.path.join(local_folder_path, os.path.basename(dropbox_file_path))

                with open(local_file_path, 'wb') as f:
                    metadata, result = dbx.files_download(path=dropbox_file_path)
                    f.write(result.content)

            # Create the flag file
            open(flag_file_path, "w").close()

        except Exception as e:
            print('Error downloading files from Dropbox: ' + str(e))





