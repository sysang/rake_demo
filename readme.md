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
