class Function :
    """For define a function into the class"""
    def __init__ (self, Name:str, Arguments:str, Do:str) :
        self.data = ({
            "Name":Name, "Args":Arguments, "Do":Do
            })
    
    def ToSet (self) :
        """Returning As A Set"""
        return self.data
    
class Create :
    def __init__(self, Null=None) :
        self.functions = []
        self.classes = []
        self.libraries = []

    def Import (self, thing:str, from_:str|None=None) :
        self.libraries.append ([thing, from_])
    
    def Function (self, Name:str, Arguments:str, Do:str) :
        self.functions.append ({
            "Name":Name, "Args":Arguments, "Do":Do
            })
    
    def Class (self, Name:str, Super:str | None, Functions:list) :
        self.classes.append ({
            "Name":Name, "Super":Super, "Functions":Functions
            })
    
    def Result (self) :
        chars = ""
        funs = self.functions
        cls = self.classes
        mdls = self.libraries
        for i in mdls :
            if i[1] == None :
                chars += "import %s\n"%(i[0])
            else :
                chars += "from %s import %s\n"%(i[1], i[0])
        for i in funs :
            chars += "def %s (%s) :\n"%(i["Name"], i["Args"])
            do = i["Do"].splitlines ()
            for h in do :
                chars += "    %s\n"%(h)
        for i in cls :
            if i["Super"] == None :
                chars += "class %s :\n"%(i["Name"])
            else :
                chars += "class %s (%s) :\n"%(i["Name"], i["Super"])
            for c in i["Functions"] :
                j = c.ToSet ()
                chars += "    def %s (%s) :\n"%(j["Name"], j["Args"])
                do = j["Do"].splitlines ()
                for h in do :
                    chars += "        %s\n"%(h)
        return chars