import string
import random
import Prefix
import Suffix
import Error_Handling

class RandomNameGenerator:

    def __init__(self,length,IsMultiple=None, Name_Count=None,With_Numbers=None,With_Prefix=None,With_Suffix=None):
        # Creating variables containing parameters
        self.name_length = length
        self.Multiple = IsMultiple
        self.Count = Name_Count
        self.WithNumbers = With_Numbers
        self.Prefix = With_Prefix
        self.Suffix = With_Suffix

    def generate_name(self):

        abc = string.ascii_lowercase + string.ascii_uppercase
        
        name = ''.join(random.choice(abc) for _ in range(self.name_length))
        return name

    def generate_names(self):
        
        if self.Multiple:
            abc = string.ascii_lowercase + string.ascii_uppercase
            Names = []

            for _ in range(self.Count):
                Names.append(self.generate_name())
            return ' '.join(str(name) for name in Names)
        
    def generate_name_with_numbers(self):
        
        if self.WithNumbers:
            abc = string.ascii_lowercase + string.ascii_uppercase
            numbers = '0123456789'

            name = ''.join(random.choice(abc + numbers) for _ in range(self.name_length))

            return name

    def generate_name_prefix(self,prefix):
        
        if self.Prefix:

            result = self.generate_name()

            return Prefix.Run(result,prefix)
        
    def generate_name_suffix(self,suffix):
        
        if self.Suffix:

            result = self.generate_name()

            return Suffix.Run(result,suffix)
        
    def generate_name_w_suff_pref(self,prefix,suffix):

        if self.Suffix and self.Prefix:
            
            result = self.generate_name()

            return Suffix.Run(Prefix.Run(result,prefix),suffix)
        
    def generate_name_with_format(self,String):
        """Uses N for a random number and L for a random letter."""

        L = string.ascii_lowercase + string.ascii_uppercase
        N = "0123456789"

        for letter in String:

            if letter.upper() == "L":

                letter = ''.join(random.choice(L))

            elif letter.upper() == "N":

                letter = ''.join(random.choice(N))
            
            print(letter) 