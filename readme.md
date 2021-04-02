## Memory error when installing pytorch

    # https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-18-04
    # Step 1 – Checking the System for Swap Information
    swapon --show
    free -h
    # Step 2 – Checking Available Space on the Hard Drive Partition
    df -h
    # Step 3 – Creating a Swap File
    fallocate -l 2G /swapfile
    # Step 4 – Enabling the Swap File
    chmod 600 /swapfile
    ls -lh /swapfile
    mkswap /swapfile
    swapon /swapfile
    # Step 5 – Making the Swap File Permanent
    cp /etc/fstab /etc/fstab.bak
    echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
    # Step 6 – Tuning your Swap Settings
    nano /etc/sysctl.conf
    vm.swappiness=15
    vm.vfs_cache_pressure=50

## Performance optimization for vm

    # https://serverfault.com/questions/696156/kswapd-often-uses-100-cpu-when-swap-is-in-use
    # Edit /etc/default/grub and add the following kernel parameters to the GRUB_CMDLINE_LINUX_DEFAULT line:
    elevator=noop - https://lonesysadmin.net/2013/12/06/use-elevator-noop-for-linux-virtual-machines/  
    zswap.enabled=1 - https://www.addictivetips.com/ubuntu-linux-tips/enable-zswap-on-linux/  
    transparent_hugepage=madvise - https://www.golinuxcloud.com/check-transparent-hugepage-status-rhel-centos/  

    # update-grub2  

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
