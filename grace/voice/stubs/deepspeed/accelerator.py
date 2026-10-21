def get_accelerator():
    class A:
        def communication_backend_name(self): return "gloo"
    return A()
