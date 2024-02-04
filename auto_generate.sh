#!/bin/bash

# 检查 original_bin 目录是否存在
if [ ! -d "original_bin" ]; then
    echo "Directory original_bin does not exist."
    exit 1
fi

# 切换到 original_bin 目录
cd original_bin

# 解压所有 .tar 文件
for tarfile in *.tar
do
    # 获取不带扩展名的文件名
    filename="${tarfile%.*}"

    # 解压 tar 文件
    tar -xf "$tarfile"
done

# 在处理完所有的 tar 文件后，查找并处理所有的 .grf 文件
find . -name "*.grf" -type f -exec ../yagl -d {} \;

# 如果 original_bin 目录下直接存在 sprites 目录，处理这个目录
if [ -d "sprites" ]; then
    rsync -a sprites/ ../sprites/
    rm -r sprites
fi

# 遍历所有子目录
for dir in */
do
    # 检查 sprites 目录是否存在
    if [ ! -d "${dir}sprites" ]; then
        echo "Directory ${dir}sprites does not exist."
        continue
    fi

    # 使用 rsync 命令将生成的 sprites 文件夹同步到父目录
    rsync -a "${dir}sprites/" ../sprites/
    rm -r "${dir}sprites"
done

# 使用 rsync 命令将 original_bin 目录中的所有内容同步到 bin 目录中
rm -r *.tar
rsync -a * ../bin/

# 删除除了指定文件之外的所有文件和目录
rm -r *.grf
rm -r */