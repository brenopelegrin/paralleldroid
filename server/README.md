# Documentation of the backend server

## Devices
## Tasks
### Sending file to task

```
curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@<yourfile>.<yourfile_extension>" <server_ip>:<server_port>/task/<task_id>/upload
```