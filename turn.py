import git
import datetime
import os

REPO_PATH = os.path.dirname(os.path.abspath(__file__))

def main():
    print("Bit awakening...")
    repo = git.Repo(REPO_PATH)

    # Pull latest
    origin = repo.remotes.origin
    origin.pull()
    print("Pulled latest changes.")

    # Write/update a file with timestamp
    filename = os.path.join(REPO_PATH, "bit_log.txt")
    with open(filename, "a") as f:
        f.write(f"Bit heartbeat at {datetime.datetime.now()}\n")

    # Stage, commit, and push
    repo.index.add([filename])
    repo.index.commit(f"Bit update: {datetime.datetime.now()}")
    origin.push()
    print("Committed and pushed changes.")

if __name__ == "__main__":
    main()
