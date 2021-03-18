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

- Install flask
