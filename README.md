# Logic App: Outlook -> Storage Queue
Deploy the ARM template and wire Office 365 + Azure Queues connections. Replace <SUB>/<RG>/<LOC> placeholders then:
```
az deployment group create -g <RG> -f outlook_to_queue.logicapp.json   -p logicAppName=qcf-outlook-to-queue storageAccountName=<StorageAccountName> queueName=ingest-queue location=uaenorth
```
