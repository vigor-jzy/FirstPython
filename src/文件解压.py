import zipfile
import os
import shutil

# 解压文件
def un_zip(file_name):
 # """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    extract_path = os.path.dirname(file_name) + "\\"
    if os.path.isdir(extract_path):
        pass
    else:
        os.mkdir(extract_path)
    for names in zip_file.namelist():
        zip_file.extract(names, extract_path)
        if names.endswith(".zip"):

            # 打开压缩包
            new_file = zipfile.ZipFile(extract_path + names);

            # 便利压缩文件
            for nf_names in new_file.namelist():

                if nf_names.endswith("简体&英文.ass"):

                    # 解压文件
                    new_file.extract(nf_names, extract_path)

                    # 移动文件到压缩包根目录
                    moveAndDeleteFile(extract_path, nf_names)
                    print("内部压缩文件：" + nf_names);
                    pass
            pass
            new_file.close()
            shutil.rmtree(os.path.dirname(extract_path + nf_names))

        elif names.endswith("简体&英文.ass"):

            # 解压文件到指定目录
            zip_file.extract(names, extract_path)

            # 移动文件到压缩包根目录
            moveAndDeleteFile(extract_path, names)

            print("外部压缩文件" + names);
            pass
        #os.removedirs(os.path.dirname(extract_path + names))
        shutil.rmtree(os.path.dirname(extract_path + names))
    zip_file.close()

# 移动解压后的文件到压缩包根目录
def moveAndDeleteFile(extract_path, zip_names):
    chkpath = extract_path + os.path.basename(zip_names)
    if os.path.isfile(chkpath):
        os.remove(chkpath)
        pass
    shutil.move(extract_path + zip_names, extract_path)

un_zip("E:\\Movie\\The.Capture.S01\\1.zip")