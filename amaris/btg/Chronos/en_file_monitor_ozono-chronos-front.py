import os
import hashlib
from datetime import datetime
import time
from pathlib import Path

class FileMonitor:
    def __init__(self, output_file="en_file_monitor_ozono-chronos-front.txt", min_update_interval=2):
        """
        Initializes the file monitor.
        
        Args:
            output_file (str):Name of the file where the code will be combined
            min_update_interval (int): Minimun time (in second) between updates
        """
        
         # Get the script's directory and create the output path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_file = os.path.join(script_dir, output_file)
        self.file_hashes = {}
        self.last_update_time = 0
        self.min_update_interval = min_update_interval
        self.existing_files = set()  # Track existing files
        
    def calculate_file_hash(self, filepath):
        """Calculates MD5 hashof the file content."""
        try:
            with open(filepath, 'rb') as file:
                content = file.read()
                hasher = hashlib.md5()
                hasher.update(content)
                return hasher.hexdigest()
        except Exception as e:
            print(f"Error reading file {filepath}: {str(e)}")
            return None
    
    def has_file_changed(self, filepath):
        """Checks if a file has changed by comparing its content."""
         # Check if file exists
        file_exists = os.path.exists(filepath)
        if not os.path.exists(filepath):
            return False
        
        current_hash = self.calculate_file_hash(filepath)
        if current_hash is None:
            return False
        
        if filepath not in self.file_hashes:
            self.file_hashes[filepath] = current_hash
            return True
        
        if self.file_hashes[filepath] != current_hash:
            self.file_hashes[filepath] = current_hash
            return True
        
        return False
    
    def update_combined_file(self, files):
        """
        Updates the combined file if enough time has passed since the last update.
        """
        current_time = time.time()
        time_since_last_update = current_time - self.last_update_time
        
        # If not enough time has passed since last update, do nothing
        if time_since_last_update < self.min_update_interval:
            print(f"Waiting {self.min_update_interval - time_since_last_update:.1f} seconds before next update...")
            return
            
        self.last_update_time = current_time
        print(f"\nUpdating combined file... ({datetime.now().strftime('%H:%M:%S')})")

        # Only include files that currently exist
        existing_files = [f for f in files if os.path.exists(f)]
        unique_files = list(dict.fromkeys(existing_files))
        
        with open(self.output_file, 'w', encoding='utf-8') as output:
            output.write(f"// Last update transaction car: {datetime.now()}\n")
            output.write(f"// Total files: {len(unique_files)}\n\n")
            
            for filepath in unique_files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        output.write(f"\n// File: {filepath}\n")
                        output.write("/" + "=" * 79 + "\n\n")
                        output.write(content)
                        output.write("\n\n")
                except Exception as e:
                    print(f"Error reading file {filepath}: {str(e)}")
    
    def monitor_files(self, files, check_interval=10):
        """
        Monitors files for changes.
        
        Args:
            files (list): List of files to monitor
            check_interval (int): Time in seconds between each file check
        """
        # Remove duplicates from file list
        unique_files = list(dict.fromkeys(files))
        print(f"Starting monitoring of {len(unique_files)} unique files...")
        print(f"Configuration:")
        print(f"- Chack interval: {check_interval} seconds")
        print(f"- Minimum time between updates: {self.min_update_interval} seconds")
        print(f"- Output file: {self.output_file}")
        print("-" * 50)
        
         # Initial file check
        for filepath in unique_files:
            if os.path.exists(filepath):
                self.existing_files.add(filepath)
                self.calculate_file_hash(filepath)
        
        # First read of all files
        for filepath in unique_files:
            self.calculate_file_hash(filepath)
        
        while True:
            changes_detected = False
            changed_files = []
            
            for filepath in unique_files:
                if self.has_file_changed(filepath):
                    print(f"Change detected in: {os.path.basename(filepath)}")
                    changes_detected = True
                    if os.path.exists(filepath):
                        changed_files.append(filepath)
            
            if changes_detected:
                self.update_combined_file(unique_files)
                print(f"Combined file updated: {self.output_file}")
                print(f"Current file count: {len(self.existing_files)}")
                print("-" * 50)
            
            time.sleep(check_interval)
            
# Complete list of files to monitor
files_to_monitor = [
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\__mocks__\mocks.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Menu\Content\ItemLink.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Menu\Content\ItemsCard.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Menu\Content\SubNavbar.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Menu\Navbar.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Reports\DynamicReportForm.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Reports\HistoryTable.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Reports\InitialView.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\CustomAutocomplete.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\CustomChipItem.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\CustomDateField.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\CustomNumericField.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\CustomSelect.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\CustomTextField.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\CustomToolbar.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\DataTable.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\components\Utils\Notification.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\config\constants.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\config\env.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\components\Menu\useNavbar.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\components\Reports\validators\useFatcaValidator.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\components\Reports\validators\validatorController.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\components\Reports\buildPayload.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\components\Reports\useDynamicParameters.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\components\Reports\useHistoryTable.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\components\Reports\useInitialView.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\components\Utils\useUtils.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\hooks\useHistory.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\interfaces\Menu\navbar.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\interfaces\Reports\reports.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\interfaces\Utils\validations.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\pages\Reports\DynamicReports.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\redux\reports\historyReportsDucks.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\redux\reports\reportsDuck.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\redux\hooks.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\redux\store.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\redux\types.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\styles\index.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\types\components\Reports\reports.d.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\types\components\Utils\utils.d.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\types\redux\redux.d.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\types\index.d.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\utils\app.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\utils\identifiers.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\utils\styles.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\utils\validations.ts",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\App.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\src\index.tsx",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\.env",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\azure-pipeline.yml",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\package.json",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\README.md",
    r"C:\Proyectos_software\Work\btg\Serverless\CHRONOS\ozono-chronos-front\tsconfig.json"
]

if __name__ == "__main__":
    # Customizable configuration
    REVISION_INTERVAL = 30  # Seconds between each file check
    MIN_UPDATE_INTERVAL = 10  # minimum seconds between combined file updates
    
    monitor = FileMonitor(min_update_interval=MIN_UPDATE_INTERVAL)
    try:
        monitor.monitor_files(files_to_monitor, check_interval=REVISION_INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring finished.")