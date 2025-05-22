# Project Documentation

## Postbuild Validation

This project is designed to validate Azure resources post-deployment. It includes scripts to retrieve details about Azure virtual machines and their configurations, network interfaces, and backup status.

### Project Structure

- `src/main.py`: Contains the main logic of the application, interacting with Azure services.
- `test.py`: A script that retrieves details about Azure virtual machines, including configurations, network interfaces, and backup status.
- `azure-pipelines.yml`: Azure Pipeline configuration file that handles authentication and subscription setup.
- `README.md`: Documentation for the project.

### Setup Instructions

1. **Prerequisites**:
   - Ensure you have the Azure CLI installed.
   - You need a service principal with the necessary permissions to access Azure resources.

2. **Authentication**:
   - The Azure Pipeline will authenticate using a service principal. Ensure the following environment variables are set:
     - `CAF_SP_CLIENTID`: The client ID of the service principal.
     - `CAF_SP_SECRET`: The secret of the service principal.
     - `LAUNCHPAD_TENANTID`: The tenant ID of your Azure subscription.
     - `Target_SUBSCRIPTION_ID`: The ID of the Azure subscription you want to set.

3. **Usage**:
   - To run the validation script, execute `python test.py` after setting up the necessary environment variables.

### Azure Pipeline Configuration

The `azure-pipelines.yml` file includes steps for:
- Authenticating with Azure using the service principal.
- Setting the Azure subscription to ensure the scripts run in the correct context.