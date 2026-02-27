import importlib
mod = importlib.import_module('math')
func = getattr(mod, 'sqrt')
print(func(25)) # 5.0