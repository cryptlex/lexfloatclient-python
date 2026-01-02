import requests
import zipfile
import platform
import subprocess
import os
import shutil
import io
tmp_dir = "./tmp"
lexfloatclient_libs_version = "v4.13.0"


class FileInfo(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


def download(url, files):
    print (url)
    result = requests.get(url, stream=True)
    zip = zipfile.ZipFile(io.BytesIO(result.content))
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    zip.extractall(tmp_dir)
    for file in files:
        shutil.copyfile(tmp_dir + "/" + file.src, file.dest)


def main():
    print("Downloading LexFloatClient library ...")

    base_url = 'https://dl.cryptlex.com/downloads/'
    base_path = './cryptlex/lexfloatclient/libs'

    files = [
        FileInfo('libs/clang/x86_64/libLexFloatClient.dylib',
                      base_path + '/macos/x86_64/libLexFloatClient.dylib'),
        FileInfo('libs/clang/arm64/libLexFloatClient.dylib',
                 base_path + '/macos/arm64/libLexFloatClient.dylib')
                      ]
    url = '/LexFloatClient-Mac.zip'
    download(base_url + lexfloatclient_libs_version + url, files)

    files = [
        FileInfo('libs/vc14/x86/LexFloatClient.dll',
                 base_path + '/win32/x86/LexFloatClient.dll'),
        FileInfo('libs/vc14/x64/LexFloatClient.dll',
                 base_path + '/win32/x86_64/LexFloatClient.dll'),
        FileInfo('libs/vc17/arm64/LexFloatClient.dll',
                 base_path + '/win32/arm64/LexFloatClient.dll')
    ]
    url = '/LexFloatClient-Win.zip'
    download(base_url + lexfloatclient_libs_version + url, files)

    files = [
        FileInfo('libs/gcc/amd64/libLexFloatClient.so', base_path +
                 '/linux/gcc/x86_64/libLexFloatClient.so'),
        FileInfo('libs/gcc/i386/libLexFloatClient.so', base_path +
                 '/linux/gcc/x86/libLexFloatClient.so'),
        FileInfo('libs/gcc/arm64/libLexFloatClient.so', base_path +
                 '/linux/gcc/arm64/libLexFloatClient.so'),
        FileInfo('libs/musl/amd64/libLexFloatClient.so', base_path +
                 '/linux/musl/x86_64/libLexFloatClient.so'),
    ]
    url = '/LexFloatClient-Linux.zip'
    download(base_url + lexfloatclient_libs_version + url, files)

    print("LexFloatClient library successfully downloaded!")
    shutil.rmtree(tmp_dir)


main()
