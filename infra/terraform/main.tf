resource "azurerm_resource_group" "this" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
  tags     = var.tags
}

resource "azurerm_storage_account" "lake" {
  name                     = substr(replace("st${var.project_name}${var.environment}", "-", ""), 0, 24)
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true
  min_tls_version          = "TLS1_2"

  blob_properties {
    versioning_enabled = true
  }

  tags = var.tags
}

resource "azurerm_storage_data_lake_gen2_filesystem" "landing" {
  name               = "landing"
  storage_account_id = azurerm_storage_account.lake.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "checkpoints" {
  name               = "checkpoints"
  storage_account_id = azurerm_storage_account.lake.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "archive" {
  name               = "archive"
  storage_account_id = azurerm_storage_account.lake.id
}

resource "azurerm_log_analytics_workspace" "this" {
  name                = "log-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = var.tags
}

resource "azurerm_databricks_workspace" "this" {
  name                        = "dbw-${var.project_name}-${var.environment}"
  resource_group_name         = azurerm_resource_group.this.name
  location                    = azurerm_resource_group.this.location
  sku                         = "premium"
  managed_resource_group_name = "rg-${var.project_name}-${var.environment}-dbx-managed"
  tags                        = var.tags
}

resource "azurerm_data_factory" "this" {
  name                = "adf-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

resource "azurerm_eventhub_namespace" "this" {
  name                = "evhns-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  sku                 = "Standard"
  capacity            = 1
  tags                = var.tags
}

resource "azurerm_eventhub" "screening" {
  name              = "screening-events"
  namespace_id      = azurerm_eventhub_namespace.this.id
  partition_count   = 4
  message_retention = 1
}

resource "azurerm_eventhub_authorization_rule" "databricks" {
  name                = "databricks-consumer"
  namespace_name      = azurerm_eventhub_namespace.this.name
  eventhub_name       = azurerm_eventhub.screening.name
  resource_group_name = azurerm_resource_group.this.name
  listen              = true
  send                = false
  manage              = false
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "this" {
  name                       = substr("kv-${var.project_name}-${var.environment}", 0, 24)
  location                   = azurerm_resource_group.this.location
  resource_group_name        = azurerm_resource_group.this.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  rbac_authorization_enabled = true
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  tags                       = var.tags
}

resource "azurerm_monitor_diagnostic_setting" "storage" {
  name                       = "diag-storage"
  target_resource_id         = azurerm_storage_account.lake.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.this.id

  enabled_metric {
    category = "Transaction"
  }
}
