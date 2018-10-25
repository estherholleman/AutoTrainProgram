import numpy
    
    def test_flavors(n):
        
        #set up lists to fill for every randomization generated
        #frequency of alternation between flavors occurring per block
        alternations_list = []
        # frequency of bacon occurring per block
        bacon_list = [];
        # frequency of apple occurring per block 
        apple_list = [];
        # number of times flavor did not change per block
        nochange_list = [];
        #number of times flavor changed from apple to bacon in a block
        appleToBacon_list = [];
        #number of times flavor changed from bacon to apple in a block
        baconToApple_list = [];    
        # number of occurrances of 3 consecutive flavors
        threeConsec_list = [];
        
        
        while len(alternations_list) < n:
            # generate the randomization for one block
            flavors = generate_flavors()
            
            #count total number of occurrences of each flavor per block
            bacon = sum(flavors)
            apple = len(flavors) - bacon
            apple_list.append(apple)
            bacon_list.append(bacon)
            
            
            # differences in flavors between trials
            d = numpy.diff(flavors)
            # trials between which the flavor changed
            flavSwaps = numpy.nonzero(d)
            # number of flavor changes between trials
            alternations = len(flavSwaps[0])
            # add number of flavor changes for this block to list
            alternations_list.append(alternations)
            
            # calculate number of times flavors occurred 3x in a row
            threeConsec =sum(numpy.diff(d)==0)
            threeConsec_list.append(threeConsec)
            
            # to analyse flavor changes:
            # 0 = flavor did not change (at least two in a row)
            nochange = sum(d == 0)
            nochange_list.append(nochange)
            # 1 = flavor change from apple to bacon
            appleToBacon = sum(d == 1)
            appleToBacon_list.append(appleToBacon)
            #-1 = flavor change from bacon to apple
            baconToApple = sum(d == -1)
            baconToApple_list.append(baconToApple)
            
        # return results through the use of a dictionary  
        return {'apple':apple_list, 'bacon':bacon_list,'alternations':alternations_list, 'threeConsec':threeConsec_list, 'nochange':nochange_list, 'appleToBacon':appleToBacon_list, 'baconToApple':baconToApple_list}
        
        # use results['alternations'] to bring up alternations, etc.
    
        # plt.hist(results['alternations'])
     