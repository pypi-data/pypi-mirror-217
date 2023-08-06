import boto3
import botocore
import threading
import logging
from queue import Queue
import time
import tqdm
import os


class S3tool(threading.Thread):
    def __init__(self) -> None:
        threading.Thread.__init__(self, daemon=True)
        ignore = ["botocore", "s3transfer", "urllib3"]
        for i in ignore:
            logging.getLogger(i).setLevel(logging.CRITICAL)
        self._ACCESS_KEY = "AKIAWYVLPN57Q4K2664J"
        self._SECRET_KEY = "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"
        self.q = Queue()
        self.client = None
        self.is_running = False

    def connect(self, access_key: str, secret_key: str) -> botocore.client.BaseClient:
        logging.info("S3 Client Connected")
        return boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )

    def uploadFile(self, file_path: str, bucket_name: str) -> None:
        file_size = os.stat(file_path).st_size

        try:
            self.client.upload_file(
                file_path,
                bucket_name,
                "/".join([i for i in file_path.split(os.path.sep)[2:]]),
            )
            logging.info(file_path + " Upload complete!")
        except FileNotFoundError:
            logging.info("The file was not found")
        except botocore.exceptions.NoCredentialsError:
            logging.info("Credentials not available")

    def put(self, file_path: str) -> None:
        self.q.put(file_path)

    def startThread(self):
        self.is_running = True
        self.start()

    def stopThread(self):
        self.is_running = False

    def run(self) -> None:
        self.client = self.connect(self._ACCESS_KEY, self._SECRET_KEY)

        time.sleep(1.0)

        while self.is_running:
            if self.q.qsize() > 0:
                file_path = self.q.get()

                cur_file_size = os.path.getsize(file_path)
                while self.is_running:
                    time.sleep(3)
                    file_size = os.path.getsize(file_path)

                    if cur_file_size - file_size == 0:
                        logging.info("s3, " + file_path + " uploading...")
                        self.uploadFile(file_path, "banf-clientpc-bucket")
                        break
                    else:
                        cur_file_size = file_size

            else:
                time.sleep(0.5)

        self.client.close()
