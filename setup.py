import os
import subprocess

install_command = ["pip", "install", "-r", "requirements.txt"]
run_server_command = ["uvicorn", "main:app", "--reload"]

if __name__ == "__main__":
    subprocess.run(install_command)
    files = os.listdir(os.getcwd())
    env_file_name = '.env'
    if env_file_name not in files:
        pg_user = input("Enter postgre user: ")
        pg_pass = input("Enter postgre password: ")
        pg_port = int(input("Enter postgre port: "))
        pg_db = input("Enter postgre db name: ")
        with open(env_file_name, "w") as file:
            file.write(f'POSTGRE_USER="{pg_user}"\n')
            file.write(f'POSTGRE_PASSWORD="{pg_pass}"\n')
            file.write(f'POSTGRE_PORT={pg_port}\n')
            file.write(f'POSTGRE_DB="{pg_db}"\n')
         
    subprocess.run(run_server_command)

