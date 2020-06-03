from cloud_kernel.db import CLOUD_KERNEL_SESSION, invokeglobalsession

if __name__ == "__main__":
    invokeglobalsession()
    print(CLOUD_KERNEL_SESSION)
