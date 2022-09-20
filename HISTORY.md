# Release history

### 0.4.1
* Improve `pynamodb_list_result` class.

### 0.4.0
* Model type factory for dynamic table use now supports `Indexes` 
  (global or local). Previously if you had e.g. GSI in your model, 
  you would get a "Missing Meta" error.

### 0.3.0
* Expose `validate_permissions` method.

### 0.2.0
* Add model type factory to allow dynamic `table_name` and `region` specification.

### 0.1.0
* Add transformer functions to transform returned results.
* P.S. still not a stable version.

### 0.0.6
* Add documentation.

### 0.0.5
* Add Fernet and KMS attribute tests.

### 0.0.4
* Add Dynamo and Pynamo encoders tests.

### 0.0.3
* Add tests to test PermissionModel base class.

### 0.0.2
* Improve `pynamodb_list_result` class.

### 0.0.1
* Initial build.
