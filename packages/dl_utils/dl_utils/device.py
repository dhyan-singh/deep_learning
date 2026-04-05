import torch


def get_device():
    # 1. CUDA (Nvidia GPU)
    if torch.cuda.is_available():
        return torch.device("cuda")

    # 2. TPU (Updated for latest torch_xla)
    try:
        import torch_xla.core.xla_model as xm
        import torch_xla

        # The modern way to get the XLA device
        tpu_device = torch_xla.device()
        print("Selected Device: TPU (XLA)")
        return tpu_device
    except (ImportError, RuntimeError):
        pass

    # 3. MPS (Mac GPU)
    if torch.backends.mps.is_available():
        return torch.device("mps")

    # 4. Default
    return torch.device("cpu")
