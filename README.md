```
import subprocess

def run_commands():
    commands = [
        "rm -rf ds",
        "git clone https://github.com/Sabbirn/ds.git",
        "cd ds && ls",  # Change directory command combined with a list command
        "python ds/ds.py"  # Specify the exact path for running the script
    ]

    for command in commands:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    print("Running...")
    run_commands()
    print("Completed!")
    
```
