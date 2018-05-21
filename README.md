# NetworkTools
本人自己开发的网络工具库

# 功能说明：
实现一系列IP地址，IP网段，IP范围的合并网段，并且是最小范围的合并。何为最小合并，例如：192.168.10.1，192.168.10.2，192.168.10.3，192.168.10.4，这四个IP
地址进行最小合并，得到的答案应该是：192.168.10.1， 192.168.10.2/31，192.168.10.4，而不能合并为192.168.10.0/30，192.168.10.4；也不能是
192.168.10.0/29。因为192.168.10.0/30包含了不存在192.168.10.0这个IP，192.168.10.0/29 包含了192.168.10.0， 192.168.10.5-192.168.10.7这些IP地址。
所以，最小合并的意思在于，只含有给定的IP地址，不能多也不能少。

# 使用范围：
某些情况网络设备上需要配置一些ACL，由于ACL控制需要严格限定访问IP，但是ACL资源有限，使用最小合并成一些最小的IP网段，可以在有效减少ACL资源的同时，保证最小访问权限。

# 使用方法：
test.text中填写需要合并的IP地址，IP网段，IP范围。使用如下命令，进行合并

    python combineIp.py test.text
    
测试例子结果如下：

    *********
    *********
    *********
    10.10.10.24/29
    10.10.10.32/30
    10.10.10.36/32
    20.20.20.20/30
    192.168.10.1/32
    192.168.10.2/31
    192.168.10.4/32
