import sys
import subprocess
import os

def print_usage():
    print("Usage: python3 cron.py '<cron_time>' <script_path>")
    print("Example: python3 cron.py '0 * * * *' /path/to/new_script.py")

def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    cron_time = sys.argv[1]
    script_path = sys.argv[2]

    # Validate script path
    if not os.path.isfile(script_path):
        print(f"Error: Script file '{script_path}' does not exist.")
        sys.exit(1)

    # Absolute path to script
    abs_script_path = os.path.abspath(script_path)

    cron_job = f"{cron_time} /root/venv/bin/python {abs_script_path} 2>> /root/bit/cron_errors.log\n"

    # Read existing crontab
    try:
        existing_cron = subprocess.check_output(['crontab', '-l'], text=True)
    except subprocess.CalledProcessError:
        existing_cron = ''

    # Avoid duplicate entry
    if cron_job in existing_cron:
        print("Cron job already exists.")
    else:
        new_cron = existing_cron + cron_job
        proc = subprocess.Popen(['crontab'], stdin=subprocess.PIPE, text=True)
        proc.communicate(new_cron)
        print(f"Cron job added:\n{cron_job.strip()}")

if __name__ == "__main__":
    main()
