#!/usr/bin/env zsh
# Ideally ran like this.
# ./build.sh; conda deactivate; conda activate botsy
# or
# conda deactivate; ./build.sh; conda activate botsy

conda init zsh
# source /Users/jfurr/.zshrc
# conda deactivate

base_dir=~/miniconda3/envs/botsy
rm -rf ~/miniconda3/envs/botsy
yes | conda create -p $base_dir python=3.8
# conda activate botsy

$base_dir/bin/pip install poetry --no-cache

exit

# To build
# poetry build

# clear poetry cache
yes | $base_dir/bin/poetry cache clear --all .

# Install localy
$base_dir/bin/poetry install --only main --no-cache
# $base_dir/bin/poetry install --only converse,dev

$base_dir/bin/poetry show


echo "To activate botsy run:"
echo "conda deactivate; conda activate botsy"

# upload to testpypi
# poetry publish --repository testpypi

# Install from testpy
# pip install --index-url https://test.pypi.org/simple/ --upgrade botsy

# upload to pypi
# poetry publish