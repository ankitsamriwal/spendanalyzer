param location string = 'uaenorth'
param baseName string = 'qcf'

resource sa 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${baseName}sa'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

resource ai 'Microsoft.Insights/components@2020-02-02' = {
  name: '${baseName}-ai'
  location: location
  kind: 'web'
  properties: { Application_Type: 'web' }
}

// Add Function App, Key Vault, Postgres Flexible Server as needed.
