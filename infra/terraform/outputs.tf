output "resource_group_name" { value=azurerm_resource_group.this.name }
output "storage_account_name" { value=azurerm_storage_account.lake.name }
output "databricks_workspace_url" { value="https://${azurerm_databricks_workspace.this.workspace_url}" }
output "eventhub_namespace" { value=azurerm_eventhub_namespace.this.name }
output "eventhub_name" { value=azurerm_eventhub.screening.name }
output "key_vault_name" { value=azurerm_key_vault.this.name }
output "data_factory_name" { value=azurerm_data_factory.this.name }
