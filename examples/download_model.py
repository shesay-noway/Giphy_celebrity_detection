import logging
import os
import tarfile
import urllib.request


s3_bucker_dir = 'https://s3.amazonaws.com/giphy-public/models/celeb-detection/'
archive_name = 'resources.tar.gz'


def download():
    archive = urllib.request.urlopen(s3_bucker_dir + archive_name)
    with open(archive_name, 'wb') as f:
        f.write(archive.read())
    with tarfile.open(archive_name, "r:gz") as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar)
    os.remove(archive_name)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)

    if not os.path.isdir(archive_name.split('.tar.gz')[0]):
        logging.info('Starting to download archive from S3')
        download()
        logging.info('Done')
    else:
        logging.info('Resources directory already exists')
