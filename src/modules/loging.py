colors = {
    "info" : ["\u001b[0m","\u001b[32m","\u001b[32m\u001b[1m"],
    "info_msg" : ["\u001b[0m","\u001b[32m","\u001b[32m\u001b[1m"],
    
    "warn" : ["\u001b[33m","\u001b[33m\u001b[1m","\u001b[43m\u001b[1m"],
    "warn_msg" : ["\u001b[33m","\u001b[33m\u001b[1m","\u001b[43m\u001b[1m"],
    
    "error" : ["\u001b[31m","\u001b[31m\u001b[1m", "\u001b[41m\u001b[1m"],
    "error_msg" : ["\u001b[31m","\u001b[31m\u001b[1m", "\u001b[41m\u001b[1m"],
    
}

class Logging():    
    def __init__(self, TAG) -> None:
        self.tag = TAG
    
    def Info(self, msg, level=1):
        print(f'{colors["info"][level]}[I] {self.tag} -> \u001b[0m{colors["info_msg"][level]}{msg}\u001b[0m')
    
    def Warn(self, msg, level=1):
        print(f'{colors["warn"][level]}[W] {self.tag} -> \u001b[0m{colors["warn_msg"][level]}{msg}\u001b[0m')
        
    def Error(self, msg, level=1):
        print(f'{colors["error"][level]}[E] {self.tag} -> \u001b[0m{colors["error_msg"][level]}{msg}\u001b[0m')
  


# Example
if __name__ == '__main__':
    Log = Logging("Test")
    Log.Info("hello", 0)
    Log.Info("hello")
    Log.Info("hello", 2)
    print()
    Log.Warn("hello", 0)
    Log.Warn("hello")
    Log.Warn("hello", 2)
    print()
    Log.Error("hello", 0)
    Log.Error("hello")
    Log.Error("hello", 2)
    print()
    Log.Error("no numbers is created")
    Log.Info("please make shure that u are connected to...")
    Log.Warn("disabling logs, it will no log any more")