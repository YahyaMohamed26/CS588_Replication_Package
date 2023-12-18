from perceval.backends.core.git import Git

from datetime import datetime
import csv

# Initialize an empty list to store dictionaries
data_list = []
csv_file_path="technical/projects_link.csv"
# Read the CSV file
with open(csv_file_path, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.DictReader(file)

    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Append the row (as a dictionary) to the list
        data_list.append(row)

# Print the resulting list of dictionaries
print(data_list)

def extract_commit_messages(repo_url, path, output_csv):
    # Instantiate the GitHub backend
    repo = Git(uri=repo_url, gitpath="tmp/"+path)
    # Fetch all commits
    commits = list(repo.fetch())

    # Extract commit messages
    commit_data = [commit['data'] for commit in commits]


    # Save commit messages to CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Commit Hash', 'User Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write commit messages
        for data in commit_data:
            try:
                text = data["Author"]
                author = ""
                # Find the start and end positions of angle brackets
                start_index = text.find("<")
                end_index = text.find(">")

                # Extract the content between angle brackets
                if start_index != -1 and end_index != -1:
                    author = text[start_index + 1:end_index]
                writer.writerow({'Commit Hash': data['commit'], 'User Email': author})
            except:
                print({'Commit Hash': data['commit'], 'Commit Message': data['message']})
        print("hi")



for data in data_list:
    repo_url = data["link"]
    output_csv = data["id"]+ ".csv"
    extract_commit_messages(repo_url,data["id"] ,output_csv)
    print(f"Commit messages saved to {output_csv}.")

