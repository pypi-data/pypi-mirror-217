from unittest.mock import MagicMock

# Mocking the requests library
requests = MagicMock()

# Mocking the get() function
requests.get = MagicMock()
requests.get.return_value = MagicMock(status_code=200, text="Mocked response")
requests.get.return_value.json.return_value = {"key": "value"}
requests.get.return_value.ok = True

# Mocking the post() function
requests.post = MagicMock()
requests.post.return_value = MagicMock(status_code=201, text="Created")
requests.post.return_value.json.return_value = {"key": "value"}
requests.post.return_value.ok = True

# Mocking the put() function
requests.put = MagicMock()
requests.put.return_value = MagicMock(status_code=204, text="No Content")
requests.put.return_value.json.return_value = None
requests.put.return_value.ok = True

# Mocking the delete() function
requests.delete = MagicMock()
requests.delete.return_value = MagicMock(status_code=204, text="No Content")
requests.delete.return_value.json.return_value = None
requests.delete.return_value.ok = True

# Mocking the patch() function
requests.patch = MagicMock()
requests.patch.return_value = MagicMock(status_code=200, text="Updated")
requests.patch.return_value.json.return_value = {"key": "value"}
requests.patch.return_value.ok = True

# Mocking the head() function
requests.head = MagicMock()
requests.head.return_value = MagicMock(status_code=200, text="OK")
requests.head.return_value.json.return_value = None
requests.head.return_value.ok = True

# Mocking the options() function
requests.options = MagicMock()
requests.options.return_value = MagicMock(status_code=200, text="OK")
requests.options.return_value.json.return_value = None
requests.options.return_value.ok = True
