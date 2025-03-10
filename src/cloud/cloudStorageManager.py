from typing import Protocol
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class CloudStorageManager(Protocol):
    def create_diroctory(self, dir_name:str):...
    def upload_file(self):...
    def download_file(self):...
    def delete_directory(self):...


class AzureStorageManager:
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def create_directory(self, container_name):
        """Create a new container in the storage account."""
        container_client = self.blob_service_client.create_container(container_name)
        print(f"Container '{container_name}' created.")
        return container_client

    def delete_directory(self, container_name):
        """Delete a container from the storage account."""
        self.blob_service_client.delete_container(container_name)
        print(f"Container '{container_name}' deleted.")

    def upload_file(self, container_name, blob_name, file_path):
        """Upload a file to a blob in the specified container."""
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"Blob '{blob_name}' uploaded to container '{container_name}'.")

    def download_file(self, container_name, blob_name, download_path):
        """Download a blob to a local file."""
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        print(f"Blob '{blob_name}' downloaded to '{download_path}'.")

    def list_files(self, container_name):
        """List all blobs in a container."""
        container_client = self.blob_service_client.get_container_client(container_name)
        blobs_list = container_client.list_blobs()
        print(f"Blobs in container '{container_name}':")
        for blob in blobs_list:
            print(blob.name)

    def delete_file(self, container_name, blob_name):
        """Delete a blob from a container."""
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()
        print(f"Blob '{blob_name}' deleted from container '{container_name}'.")

# Example usage
if __name__ == "__main__":
    # Replace with your Azure Storage connection string
    connection_string = "your_connection_string_here"

    storage_manager = AzureStorageManager(connection_string)

    # Create a new container
    storage_manager.create_directory("mycontainer")

    # Upload a file to the container
    storage_manager.upload_file("mycontainer", "myblob", "path/to/local/file.txt")

    # List blobs in the container
    storage_manager.list_files("mycontainer")

    # Download a blob from the container
    storage_manager.download_file("mycontainer", "myblob", "path/to/download/file.txt")

    # Delete a blob from the container
    storage_manager.delete_file("mycontainer", "myblob")

    # Delete the container
    storage_manager.delete_directory("mycontainer")