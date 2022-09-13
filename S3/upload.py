import os
import boto3

s3 = boto3.resource("s3", region_name="us-west-1")
#s3 = boto3.client("s3", region_name="us-west-1")


def get_directory_paths():
    path_file = open('local_path.txt', 'r')
    return path_file.readlines()

def upload():
    try:
        bucket_name = "style-engine"
        bucket = s3.Bucket(bucket_name)

        #response = s3.list_objects_v2(Bucket=bucket_name)

        for path in paths:
            for path, subdirs, files in os.walk(path):
                #_path = path.replace("\\","/")
                directory_name = path.split('/')
                #s3.li
                obj = s3.Object(bucket_name, directory_name[-2] + '/' +directory_name[-1])
                for file in files:
                    bucket.upload_file(os.path.join(path, file), bucket_name+'/'+directory_name[-2] + '/'
                                                                                 +directory_name[-1]+file)

    except Exception as err:
        print(err)

if __name__ == '__main__':
    paths = get_directory_paths()
    upload()