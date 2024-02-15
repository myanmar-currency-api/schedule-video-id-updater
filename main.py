import os
import json
from googleapiclient.discovery import build
from github import Github

def push_youtube_meta_to_github():
# Define GitHub repository details
    repo_owner = 'myanmar-currency-api'
    repo_name = 'youtube-scraper'
    file_path = 'video_meta.json'
    file_content = ''

    # GitHub personal access token with 'repo' scope
    access_token = os.getenv("GH_ACCESS_TOKEN")

    # Create a GitHub instance using access token
    g = Github(access_token)


    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            print("File content:")
            print(file_content)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    # Get the repository
    repo = g.get_user(repo_owner).get_repo(repo_name)

    # Create or update file
    try:
        contents = repo.get_contents(file_path)
        print(contents.sha)
        repo.update_file(file_path, "Update file", file_content, contents.sha)
        print(f"File '{file_path}' updated successfully.")
    except Exception as e:
        repo.create_file(file_path, "Create file", file_content)
        print(f"File '{file_path}' created successfully.")
        pass

def fetch_youtube_video_id():
    api_key = os.getenv("YOU_TUBE_API_KEY")

    # Replace 'CHANNEL_ID' with the ID of the specific channel
    channel_id = 'UCuaRmKJLYaVMDHrnjhWUcHw'

    # Replace 'VIDEO_NAME' with the name of the video you want to search for
    video_name = 'dvb tvnews currency rate'

    youtube = build('youtube', 'v3', developerKey=api_key)

    # Call the search.list method to search for videos
    search_response = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        q=video_name,
        order='date',  # Filter by recently uploaded
        type='video'
    ).execute()

    search_result = search_response.get('items',[])[0]
    video_meta = {
        "video_title":search_result["snippet"]["title"],
        "video_id":search_result["id"]["videoId"]}
    
    print(video_meta)

    with open('video_meta.json', 'w') as json_file:
        json.dump(video_meta, json_file, indent=4)


def main():
    fetch_youtube_video_id()
    push_youtube_meta_to_github()

main()
