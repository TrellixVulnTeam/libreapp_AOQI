import glob
import urllib.request
import shutil
import os
from pathlib import Path
import tarfile
import json


FILES_TO_DOWNLOAD = [
    {
        "url": 'https://files.pythonhosted.org/packages/97/ae/93aeb6ba65cf976a23e735e9d32b0d1ffa2797c418f7161300be2ec1f1dd/pydicom-1.2.0-py2.py3-none-any.whl',
        "hash": '2132a9b15a927a1c35a757c0bdef30c373c89cc999cf901633dcd0e8bdd22e84',
        "location": 'wheels',
        "extract": False
    },
    {
        "url": 'https://files.pythonhosted.org/packages/a0/35/dd97fbb48d4e6b5ae97307497e31e46691adc2feedb6279d29fc1c8ad9c1/ipykernel-5.1.1-py3-none-any.whl',
        "hash": '346189536b88859937b5f4848a6fd85d1ad0729f01724a411de5cae9b618819c',
        "location": 'wheels',
        "extract": False
    },
    {
        "url": 'https://github.com/iodide-project/pyodide/releases/download/0.13.0/pyodide-build-0.13.0.tar.bz2',
        "hash": 'd8bb9ec31c87d80bcc4ed9f1477289b679b03ba4a082ebddde88f9416a92376a',
        "location": '.',
        "extract": True
    }
]


# TODO call this function on `yarn bootstrap`
def main():
    for item in FILES_TO_DOWNLOAD:
        filepath, _ = urllib.request.urlretrieve(item['url'])
        # print(headers)
        # TODO check hash
        filename = item['url'].split('/')[-1]

        Path(item['location']).mkdir(exist_ok=True)
        new_location = os.path.abspath(
            os.path.join(item['location'], filename))

        shutil.move(filepath, new_location)

        if item['extract']:
            with tarfile.open(new_location, 'r:bz2') as tar:
                assert new_location.endswith('.tar.bz2')
                extract_dir = Path(new_location[:-8])
                extract_dir.mkdir(exist_ok=True)
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
                    
                
                safe_extract(tar, path=extract_dir)

    index_wheels()


def index_wheels():
    """Create a json index of all the downloaded wheels
    """
    # TODO create index
    # TODO hash index
    # TODO save index with hash appended to filename

    with open('wheels/index.json', 'w') as a_file:
        json.dump([
            "pydicom-1.2.0-py2.py3-none-any.whl",
            "ipykernel-5.1.1-py3-none-any.whl"
        ], a_file)


if __name__ == "__main__":
    main()
