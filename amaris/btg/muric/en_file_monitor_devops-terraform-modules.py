import os
import hashlib
from datetime import datetime
import time
from pathlib import Path

class FileMonitor:
    def __init__(self, output_file="en_file_monitor_devops-terraform-modules.txt", min_update_interval=2):
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
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\.azuredevops\modules-pipeline.yaml",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\acm\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\acm\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\acm\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\acm\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\alb\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\alb\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\alb\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\alb\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\alb_rules\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\alb_rules\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\alb_rules\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\alb_rules\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigtw_public_cognito\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigtw_public_cognito\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigtw_public_cognito\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigtw_public_cognito\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigw_nlb_integration\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigw_nlb_integration\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigw_nlb_integration\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigw_nlb_integration\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigw_vpc_link\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigw_vpc_link\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigw_vpc_link\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\apigw_vpc_link\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\cloudfront\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\cloudfront\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\cloudfront\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\cloudfront\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\code_build\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\code_build\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\code_build\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\code_build\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\codestar\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\codestar\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\codestar\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\codestar\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ddb\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ddb\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ddb\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ddb\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\docker_build_push\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\docker_build_push\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\docker_build_push\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\docker_build_push\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\dynamodb\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\dynamodb\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\dynamodb\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\dynamodb\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecr\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecr\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecr\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecr\versions.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_cluster\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_cluster\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_cluster\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_cluster\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_nlb\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_nlb\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_nlb\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_nlb\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_service\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_service\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_service\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_service\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_service_alb\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_service_alb\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_service_alb\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_service_alb\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_task_role\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_task_role\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_task_role\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ecs_task_role\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\efs\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\efs\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\efs\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\efs\version.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\eks\data.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\eks\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\eks\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\eks\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\eks\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\elasticache\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\elasticache\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\elasticache\provider.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\elasticache\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\lambda\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\lambda\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\lambda\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\lambda\versions.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\network\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\network\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\network\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\network\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\nlb\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\nlb\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\nlb\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\nlb\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\nlb-alb\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\nlb-alb\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\nlb-alb\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\nlb-alb\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\private_hosted_zone\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\private_hosted_zone\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\private_hosted_zone\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\private_hosted_zone\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\rds\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\rds\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\rds\provider.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\rds\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\rds_serverless_cluster\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\rds_serverless_cluster\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\rds_serverless_cluster\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\rds_serverless_cluster\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\route53\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\route53\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\route53\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\route53\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\s3\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\s3\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\s3\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\s3\versions.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\secrets_manager\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\secrets_manager\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\secrets_manager\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\secrets_manager\versions.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\service_discovery_namespace\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\service_discovery_namespace\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\service_discovery_namespace\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\service_discovery_namespace\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sns\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sns\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sns\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sns\versions.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sns_subscriptions\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sns_subscriptions\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sns_subscriptions\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sns_subscriptions\versions.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sqs\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sqs\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sqs\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sqs\versions.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sqs_policy\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sqs_policy\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sqs_policy\variables.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\sqs_policy\versions.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ssm_parameter\main.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ssm_parameter\outputs.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ssm_parameter\providers.tf",
    r"C:\Proyectos_software\Work\btg\Terraform\MURIC\devops-terraform-modules\ssm_parameter\variables.tf"

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