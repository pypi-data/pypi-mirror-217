operations = {
  "commitMeta": {
    "author": "authorName <authorName@example.com>",
    "authorTime": "2021-04-07T14:42:25.534748Z",
    "message": "Example Commit Message",
    "properties": {
      "additionalProp1": "xxx",
      "additionalProp2": "yyy",
      "additionalProp3": "zzz"
    },
    "signedOffBy": "signedOffByName <signedOffBy@example.com>"
  },
  "operations": [
    {
      "type": "PUT",
      "key": {
        "elements": [
          "table1"
        ]
      },
      "content": {
        "type": "ICEBERG_TABLE",
        "id": "10df6e9b-890f-491e-821f-02dfeed3a847",
        "metadataLocation": "/path/to/metadata/",
        "snapshotId": 1,
        "schemaId": 2,
        "specId": 3,
        "sortOrderId": 4
      }
    }
  ]
}

merge = {
  "fromHash": "be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c",
  "fromRefName": "test-branch3",
  "defaultKeyMergeMode": "NORMAL",
  "keyMergeModes": [
    {
      "key": {
        "elements": [
          "table1"
        ], 
      },
      "mergeBehavior": "FORCE"
    }
  ],
  "dryRun": False,
  "fetchAdditionalInfo": False,
  "returnConflictAsResult": True
}