from client import NessieV2Client
from test_objects import operations, merge

# from test_operation import operations

config = { 
          "endpoint": "http://0.0.0.0:19120/api/v2",
          "verify": False,
          "default_branch": "main",
          "auth": {
              "type": "none",
              "timeout": 10
          }
        }

client = NessieV2Client(config)

## Test get_config
print("-------- get_config()---------------")
# print(client.get_config())
print("------------------------------------")

## Test get_all_references
print("-------- get_all_references()---------------")
# print(client.get_all_references())
print("------------------------------------")

## Test create_reference
print("-------- create_reference()---------------")
# print(client.create_reference("test-branch4"))
print("------------------------------------")

## Test Get Hash
print("-------- get_hash()---------------")
# print(client.get_hash("test-branch3"))
print("------------------------------------")

## Test create_reference
print("-------- create_reference()(TAG)---------------")
# print(client.create_reference(name="test-tag",ref_type="TAG", source_reference={'type': 'BRANCH', 'name': 'test-branch3', 'hash': 'be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c'}))
print("------------------------------------")

## Test create_commit
print("-------- create_commit()---------------")
# print(client.create_commit(operations=operations, branch="test-branch3"))
print("------------------------------------")

## Test create_merge
print("-------- create_merge()---------------")
print(client.create_merge(branch="main", merge=merge))
print("------------------------------------")

## Test get_diff
print("-------- get_diff()---------------")
# print(client.get_diff(from_ref="test-branch3", to_ref="main"))
print("------------------------------------")

## Test get_reference_details()
print("-------- get_reference_details()---------------")
# print(client.get_reference_details(ref="test-branch3",fetch="ALL"))
print("------------------------------------")

## Test delete_reference
print("-------- delete_reference()---------------")
# print(client.delete_reference("test-branch2"))
print("------------------------------------")

## Test get_several_contents
print("-------- get_several_contents()---------------")
# print(client.get_several_contents("test-branch3", keys=["table1"]))
print("------------------------------------")

## Test get_multiple_contents_post
print("-------- get_multiple_contents_post()---------------")
# print(client.get_multiple_contents_post("test-branch3", keys=["table1"], with_doc=True))
print("------------------------------------")

## Test get_contents
print("-------- get_content()---------------")
# print(client.get_content(ref="test-branch3", key="table1", with_doc=False))
print("------------------------------------")

## Test get_entries
print("-------- get_entries()---------------")
# print(client.get_entries("test-branch3"))
print("------------------------------------")

## Test get_commit_log
print("-------- get_commit_log()---------------")
# print(client.get_commit_log("test-branch3"))
print("------------------------------------")