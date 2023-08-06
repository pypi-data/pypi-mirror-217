import dvc.api
from dvc.api import DVCFileSystem
import boto3
import os
from git import Repo,rmtree


repo_dir="tah_data_repo"


def get_file(file_system,file_name,local_file_name):
    file_system.get_file(file_name,local_file_name)

def get_dir(file_system,dir_path,local_dir_name):
    file_system.get(dir_path,local_dir_name,recursive=True)
    rmtree(repo_dir)


def init_fs(Repo_url,branch):

    repo = Repo.clone_from(Repo_url,repo_dir)

    git_ = repo.git

    git_.checkout(branch)

    file_system = DVCFileSystem(repo_dir)

    return file_system
    