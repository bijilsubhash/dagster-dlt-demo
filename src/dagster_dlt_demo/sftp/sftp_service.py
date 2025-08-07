import paramiko
from dagster_dlt_demo.common.utils.logging_util import Logger

logger = Logger(__name__)


class SFTPClient:
    def __init__(self, hostName: str, port: int, userName: str, password: str):
        self.hostName = hostName
        self.port = port
        self.userName = userName
        self.password = password

    def connect(self) -> paramiko.SFTPClient:
        self.SSH_Client = paramiko.SSHClient()
        self.SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.SSH_Client.connect(
                hostname=self.hostName,
                port=self.port,
                username=self.userName,
                password=self.password,
                look_for_keys=False,
                allow_agent=False,
            )
            sftp_client = self.SSH_Client.open_sftp()
            logger.info("SFTP channel opened successfully")
            return sftp_client
        except paramiko.AuthenticationException as e:
            logger.error(
                f"Authentication failed for {self.userName}@{self.hostName}: {e}"
            )
            raise
        except paramiko.SSHException as e:
            logger.error(f"SSH error connecting to {self.hostName}: {e}")
            raise
        except Exception as e:
            logger.error(f"Connection error to {self.hostName}: {e}")
            raise

    def close(self) -> None:
        self.SSH_Client.close()

    def put(
        self, sftp_client: paramiko.SFTPClient, localFilePath: str, remoteFilePath: str
    ) -> None:
        try:
            sftp_client.put(localFilePath, remoteFilePath)
            logger.info(f"Uploaded {localFilePath} to {remoteFilePath}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

    def get_latest(
        self,
        sftp_client: paramiko.SFTPClient,
        remotePath: str = ".",
        filename_pattern: str = "",
        last_st_mtime: int = None,
    ):
        try:
            import stat

            # First: Find directory with latest mtime
            dirs_iter = sftp_client.listdir_iter(remotePath, read_aheads=50)
            latest_dir = 0
            latest_dir_mtime = 0

            for item_attr in dirs_iter:
                if int(item_attr.filename) > latest_dir:
                    latest_dir = int(item_attr.filename)

            if not latest_dir:
                logger.info(f"No directories found in {remotePath}")
                return None

            # Second: Within that directory, look for files matching filename pattern
            dir_path = f"{remotePath.rstrip('/')}/{latest_dir}"
            files_iter = sftp_client.listdir_iter(dir_path, read_aheads=50)
            matching_file = None
            file_mtime = 0

            for file_attr in files_iter:
                if stat.S_ISREG(file_attr.st_mode):
                    if filename_pattern and filename_pattern in file_attr.filename:
                        if file_attr.st_mtime > file_mtime:
                            file_mtime = file_attr.st_mtime
                            matching_file = file_attr

            if matching_file:
                result = {
                    "file_mtime": file_mtime,
                    "file": matching_file,
                    "dir_name": latest_dir,
                }
                logger.info(
                    f"Found file '{matching_file.filename}' in dir '{latest_dir}' - dir_mtime: {latest_dir_mtime}, file_mtime: {file_mtime}"
                )
                return result
            else:
                logger.info(
                    f"No files matching '{filename_pattern}' found in latest directory '{latest_dir.filename}'"
                )
                return None

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
