## [Memory error when installing pytorch](https://discuss.pytorch.org/t/memory-error-when-installing-pytorch/8027/6)

    # create swap file of 512 MB
    dd if=/dev/zero of=/swapfile bs=1024 count=2097152
    # modify permissions
    chown root:root /swapfile
    chmod 0600 /swapfile
    # setup swap area
    mkswap /swapfile
    # turn swap on
    swapon /swapfile
    # vi /etc/fstab
    /swapfile   swap    swap    sw  0   0

## Performance optimization for vm

- https://askubuntu.com/questions/259739/kswapd0-is-taking-a-lot-of-cpu  
- https://serverfault.com/questions/696156/kswapd-often-uses-100-cpu-when-swap-is-in-use/696185#696185  
- Edit /etc/default/grub and add the following kernel parameters to the GRUB_CMDLINE_LINUX_DEFAULT line  
> elevator=noop - https://lonesysadmin.net/2013/12/06/use-elevator-noop-for-linux-virtual-machines/  
> zswap.enabled=1 - https://www.addictivetips.com/ubuntu-linux-tips/enable-zswap-on-linux/  
> transparent_hugepage=madvise - https://www.golinuxcloud.com/check-transparent-hugepage-status-rhel-centos/  

- update-grub2  
- Edit /etc/sysctl.conf and append the following:  
> vm.swappiness=25  
> vm.vfs_cache_pressure=50 # safer than periodically dropping caches  

## Package Dependencies

- nginx installation, https://nginx.org/en/linux_packages.html#Ubuntu
- pip install flask
- pip install gunicorn
- pip install supervisor
- pip install torch==1.7.0+cpu torchvision==0.8.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
- pip install keybert
- python -m nltk.downloader stopwords
- cd path/to/project && python keywords_extraction/algorithms.py
- pip install pytextrank
- python -m spacy download nl_core_news_md
- ln -s /path/to/project/keywords_extraction/syntax_iterators.py /usr/local/lib/python3.7/dist-packages/spacy/lang/nl/syntax_iterators.py
- edit /usr/local/lib/python3.7/dist-packages/spacy/lang/nl/__init__.py
