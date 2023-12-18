from perceval.backends.core.git import Git

from datetime import datetime
import csv


def extract_commits(repo_url, path):
    # Instantiate the GitHub backend
    repo = Git(uri=repo_url, gitpath="tmp/" + path)
    # Fetch all commits
    commits = list(repo.fetch())

    # Extract commit messages
    commit_data = [commit['data'] for commit in commits]
    return commit_data


def save_to_csv(project_id, commit_id, message, author, bug_title, bug_desc, bfx_hash, bfx_message, bfx_author,
                file_name):
    # Save commit messages to CSV file
    with open(file_name, mode='a', newline='') as csvfile:
        fieldnames = ['Project_id', 'BIC_Hash', 'BIC_Message', 'BIC_Author', 'BR_Title', 'BR_Description', 'BFX_Hash',
                      'BFX_Message', 'BFX_Author']
        writer = csv.writer(csvfile)

        # Write the header
        if csvfile.tell() == 0:
            writer.writerow(
                ['Project_id', 'BIC_Hash', 'BIC_Message', 'BIC_Author', 'BR_Title', 'BR_Description', 'BFX_Hash',
                 'BFX_Message', 'BFX_Author'])

        # Write commit messages
        try:
            writer.writerow(
                [project_id, commit_id, message, author, bug_title, bug_desc, bfx_hash, bfx_message, bfx_author])
        except:
            print([project_id, commit_id, message, author, bug_title, bug_desc, bfx_hash, bfx_message, bfx_author])


def get_commit_info(commit_hash, commits):
    for commit in commits:
        if commit["commit"] == commit_hash:
            text = commit["Author"]
            author = ""
            # Find the start and end positions of angle brackets
            start_index = text.find("<")
            end_index = text.find(">")

            # Extract the content between angle brackets
            if start_index != -1 and end_index != -1:
                author = text[start_index + 1:end_index]

            return commit["message"], author
    return None


# Initialize an empty list to store dictionaries
data_list = []
csv_file_path = "technical/projects_link.csv"
# Read the CSV file
with open(csv_file_path, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.DictReader(file)

    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Append the row (as a dictionary) to the list
        data_list.append(row)

commitsAllProjects = []
for data in data_list:
    repo_url = data["link"]
    output_csv = data["id"] + ".csv"
    commitsAllProjects.append(extract_commits(repo_url, data["id"]))
    print(repo_url)

# Read the CSV file
with open("technical/technical2.csv", 'r') as file:
    # Create a CSV reader
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Create a new dictionary for the modified data
        new_row = {}
        i = 0
        for project in data_list:
            if project["id"] == row['Project_id']:
                break
            i += 1
        commits = commitsAllProjects[i]
        # Copy Project_id, BIC_Hash, BR_Title, and BR_Description as they are
        new_row['Project_id'] = row['Project_id']
        new_row['BIC_Hash'] = row['BIC_Hash']
        new_row['BR_Title'] = row['BR_Title']
        new_row['BR_Description'] = row['BR_Description']

        # Create new keys for BIC_Message, BIC_Author, BFX_Hash, BFX_Message, BFX_Author
        repo_link = ''
        for data in data_list:
            if data['id'] == row['Project_id']:
                repo_link = data['link']
        bic_message, bic_author = get_commit_info(row['BIC_Hash'], commits)

        new_row['BIC_Message'] = bic_message  # You need to replace this with your logic to extract BIC_Message
        new_row['BIC_Author'] = bic_author  # You need to replace this with your logic to extract BIC_Author

        bfx_message, bfx_author = get_commit_info(row['BFX_Hash'], commits)
        new_row['BFX_Hash'] = row['BFX_Hash']
        new_row['BFX_Message'] = bfx_message  # You need to replace this with your logic to extract BFX_Message
        new_row['BFX_Author'] = bfx_author  # You need to replace this with your logic to extract BFX_Author

        # Append the modified row to the list
        save_to_csv(row['Project_id'], row['BIC_Hash'], bic_message, bic_author, row['BR_Title'],
                    row['BR_Description'], row['BFX_Hash'], bfx_message, bfx_author, "new_dataset.csv")
