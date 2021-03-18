## [Memory error when installing pytorch](https://discuss.pytorch.org/t/memory-error-when-installing-pytorch/8027/6)

    # create swap file of 512 MB
    dd if=/dev/zero of=/swapfile bs=1024 count=524288
    # modify permissions
    chown root:root /swapfile
    chmod 0600 /swapfile
    # setup swap area
    mkswap /swapfile
    # turn swap on
    swapon /swapfile

## Package Dependencies

- nginx installation, https://nginx.org/en/linux_packages.html#Ubuntu
- pip install --user flask
- pip install --user gunicorn
- pip install --user torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
- pip install --user keybert
-
- pip install pytextrank
- python -m spacy download nl_core_news_sm
