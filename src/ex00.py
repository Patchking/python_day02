

class key():
    def __init__(self):
        self.passphrase = "zax2rulez"
    def __len__(self):
        return 1337
    def __getitem__(self, index):
        return 3
    def __gt__(self, num):
        return True
    def __str__(self):
        return "GeneralTsoKeycard"
    
def main():
    Key = key()

    try:
        assert(len(Key) == 1337)
        assert(Key[404] == 3)
        assert(Key > 9000)
        assert(Key.passphrase == "zax2rulez")
        assert(str(Key) == "GeneralTsoKeycard")
        print("Test completed successfully")
    except:
        print("Error occured while check")
    

if __name__ == "__main__":
    main()
    

