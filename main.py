import os
import subprocess
import sys
import psutil  # This will throw an error if not installed, prompting installation below.
import platform
import time
from datetime import datetime
import shutil

def install_packages():
    required_packages = ['psutil']

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Installing now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")

# Check and install required packages
install_packages()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_startup_programs():
    print("Startup Programs:")
    if platform.system() == "Windows":
        startup_folder = os.getenv('APPDATA') + r'\Microsoft\Windows\Start Menu\Programs\Startup'
        print(f"Startup folder: {startup_folder}\n")
        for root, dirs, files in os.walk(startup_folder):
            for file in files:
                print(file)
    else:
        print("This feature is only available on Windows.")
    input("\nPress Enter to return to the main menu...")

def remove_bloatware():
    if platform.system() == "Windows":
        bloatware_list = [
            "3D Builder",
            "Candy Crush Saga",
            "Microsoft Solitaire Collection"
        ]
        print("Removing bloatware:")
        for app in bloatware_list:
            try:
                print(f"Attempting to remove {app}...")
                subprocess.run(["powershell", "-Command", f"Get-AppxPackage *{app}* | Remove-AppxPackage"], check=True)
                print(f"{app} removed successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to remove {app}. It might not be installed.")
    else:
        print("This feature is only available on Windows.")
    input("\nPress Enter to return to the main menu...")

def monitor_system_resources():
    print("Monitoring System Resources:")
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')
            clear_console()
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"CPU Usage: {cpu_usage}%")
            print(f"Memory Usage: {memory_info.percent}%")
            print(f"Disk Usage: {disk_info.percent}%")
            print("\nPress Ctrl+C to return to the main menu.")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def cleanup_temp_files():
    if platform.system() == "Windows":
        temp_folder = os.getenv('TEMP')
        print(f"Cleaning up temporary files in {temp_folder}...")
        try:
            shutil.rmtree(temp_folder)
            os.mkdir(temp_folder)
            print("Temporary files cleaned up successfully.")
        except Exception as e:
            print(f"Failed to clean temporary files: {e}")
    else:
        print("This feature is only available on Windows.")
    input("\nPress Enter to return to the main menu...")

def clean_ram():
    print("Cleaning up RAM...")
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            # Close processes that use more than 10% of memory and are not system-critical
            if proc.info['memory_percent'] > 10 and proc.info['name'].lower() not in ["system", "explorer.exe"]:
                print(f"Terminating process {proc.info['name']} (PID: {proc.info['pid']}) using {proc.info['memory_percent']:.2f}% of RAM")
                psutil.Process(proc.info['pid']).terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    print("RAM cleanup completed.")
    input("\nPress Enter to return to the main menu...")

def main_menu():
    while True:
        clear_console()
        print("PC Optimization Tool")
        print("====================")
        print("1. List Startup Programs")
        print("2. Remove Bloatware")
        print("3. Monitor System Resources")
        print("4. Cleanup Temporary Files")
        print("5. Clean RAM")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")

        if choice == '1':
            list_startup_programs()
        elif choice == '2':
            remove_bloatware()
        elif choice == '3':
            monitor_system_resources()
        elif choice == '4':
            cleanup_temp_files()
        elif choice == '5':
            clean_ram()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(2)

if __name__ == "__main__":
    main_menu()
