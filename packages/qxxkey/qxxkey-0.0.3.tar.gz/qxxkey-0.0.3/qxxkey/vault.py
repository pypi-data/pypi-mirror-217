class Vault:
    def __init__(self, alias):
        import os
        import json

        self.alias = alias
        self.cwd = os.getcwd()

        # get appdata direcotry weather it is windows or linux or mac
        if os.name == "nt":
            self.appdata = os.getenv("APPDATA")
        else:
            print("This machine is not natively supported. The local appdata directory will be used. If you want this to change please open an issue on github.")
            self.appdata = self.cwd

        self.vault_path = os.path.join(self.appdata, "qxxkey", "vaults", self.alias + ".json")

        if not os.path.exists(self.vault_path):
            self.new()
        else:
            with open(self.vault_path, "r") as f:
                self.vault = json.load(f)
    
    def new(self):
        import os

        if not os.path.exists(os.path.join(self.appdata, "qxxkey")):
            os.mkdir(os.path.join(self.appdata, "qxxkey"))
        
        if not os.path.exists(os.path.join(self.appdata, "qxxkey", "vaults")):
            os.mkdir(os.path.join(self.appdata, "qxxkey", "vaults"))
        
        self.vault = {}
        self.save()

    def save(self):
        import json

        with open(self.vault_path, "w") as f:
            json.dump(self.vault, f)

    def get(self, key):
        return self.vault[key]
    
    def set(self, key, value):
        self.vault[key] = value
        self.save()
    
    def delete(self, key):
        del self.vault[key]
        self.save()

    def list(self):
        return self.vault.keys()
    
