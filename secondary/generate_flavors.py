import numpy
    

def generate_flavors(choices = ['apple', 'bacon']):
    in_row = 1
    p_x= randint(0, len(choices)-1)
    choices_list = [p_x]
    
    
    while len(choices_list) < 20:
        x = randint(0, len(choices)-1)
        if p_x == x:
            if in_row <3:
                in_row +=1
                choices_list.append(x)
                p_x = x
            else:
                continue
        else:
            choices_list.append(x)
            p_x = x
            in_row = 1
    
        # check for number of alternations in a row
        if len(choices_list) > 19:
            d = numpy.diff(choices_list)
            flavChange = numpy.nonzero(d)
            nflavChange = len(flavChange[0])
            
            if nflavChange > 10:
                in_row = 1
                p_x= randint(0, len(choices)-1)
                choices_list = [p_x]
                    

    return choices_list 