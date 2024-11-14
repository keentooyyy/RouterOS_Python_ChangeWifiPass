import paramiko
import requests
import os


def get_password_from_url(url):
    print(f"Fetching password from URL: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text.strip()


def save_password_to_file(password, filename="password.txt", directory="dist"):
    print(f"Saving password to file: {directory}/{filename}")
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as file:
        file.write(password)
    print(f"Password saved to {file_path}")


def execute_script_command(host, username, password, command):
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Establish SSH connection
        ssh.connect(hostname=host, username=username, password=password)
        print("Connection established.")

        # Execute the command
        print(f"Executing command: {command}")
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            print("Command output:")
            print(output)
        if error:
            print("Command error:")
            print(error)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        ssh.close()
        print("Connection closed.")


def main():
    host = '192.168.88.1'
    username = 'admin'
    password = 'pass'

    # Retrieve the new password from the URL
    password_url = "url"
    new_password = get_password_from_url(password_url)
    print(f"New password retrieved: {new_password}")

    # Save the new password to a file
    save_password_to_file(new_password)

    # Define the RouterOS command to update the security profile
    command = f"""
    /interface wireless security-profiles set [find name="guest pass 1"] wpa2-pre-shared-key="{new_password}"
    """

    # Execute the command
    execute_script_command(host, username, password, command)


if __name__ == '__main__':
    main()