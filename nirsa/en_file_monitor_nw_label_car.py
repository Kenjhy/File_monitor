import os
import hashlib
from datetime import datetime
import time
from pathlib import Path

class FileMonitor:
    def __init__(self, output_file="en_file_monitor_nw_label_car.txt", min_update_interval=2):
        """
        Initializes the file monitor.
        
        Args:
            output_file (str):Name of the file where the code will be combined
            min_update_interval (int): Minimun time (in second) between updates
        """
        self.file_hashes = {}
        self.output_file = output_file
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
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\audit\AuditAwareImpl.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\client\WebClientApiZpl.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\CorsConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\CorsLoggingFilter.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\CurrentUser.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\JacksonConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\SwaggerConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\UserConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\UserInterceptor.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\constants\RequestConstants.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\controller\RequestLabelsController.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\controller\RequestPrintController.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\response\ErrorResponseDto.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\ImagesDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\LabelsDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\PrintsDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\response\ResponseDto.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\UserDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\BaseEntity.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Images.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Labels.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Prints.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Templates.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\AuthorizationTokenException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\GlobalExceptionHandler.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\IntegrationZplException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\PrintException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\ResourceNotFoundException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\mapper\LabelsMapper.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\ImagesRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\LabelsRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\PrintsRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\TemplatesRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\Impl\PrintService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\Impl\RequestLabelsServiceImpl.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\Impl\UtilityService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\IPrintService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\IRequestLabelsService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\IUtilityService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\AccountsApplication.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Typetransactions.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\States.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Transactions.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Cars.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\CarStates.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Boxes.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\BoxesDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\response\TransactionCarBoxResponseDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\mapper\TransactionMapper.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\TypeTransactionsRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\StatesRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\TransactionsRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\CarsRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\CarStatesRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\BoxesRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\MaxBoxesExceededException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\InvalidTransactionStateException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\NirsaIntegrationException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\CarNotFoundException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\BoxNotFoundException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\InvalidTransactionStateException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\GlobalExceptionHandler.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\ITransactionCarService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\Impl\TransactionCarServiceImpl.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\RestTemplateConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\controller\TransactionCarController.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\request\TransactionCarBoxRequestDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\ClosedCars.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\ClosedCarsRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\AuthorizationException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\request\NirsaStatusRequestDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\NirsaConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\request\NirsaSaveCloseCarRequestDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\request\MaterialBoxesFinaliseRequestDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\response\MaterialBoxesQuantityResponseDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\wrapper\MaterialBoxesCloseResponseWrapper.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\wrapper\MaterialBoxesInfoResponseWrapper.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\MaterialBoxesCarCloseDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\utilities\TransactionUtils.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\Impl\NirsaIntegrationService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\response\NirsaResponse.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\NonUniqueResultException.java",
    
    # ... (rest of the file paths remain the same, shared code CurrentUser, ErrorResponseDto, ResponseDto)
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