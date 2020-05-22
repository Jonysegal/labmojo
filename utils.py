

def remove_objects(pi, remove_list, key_name):
    """
    Remove the scholarly objects from PI payload - for Detail
    """
    num_to_remove = len(pi[key_name])
    if num_to_remove:
        x = 0
        while x < num_to_remove:
            pi[key_name][x] = pi[key_name][x].__dict__
            for item in remove_list:
                try:
                    del pi[key_name][x][item]
                except:
                    pass
            x += 1
    return pi



def remove_scholarly_objects(pi, remove_list, key_name):
    """
    Remove the scholarly objects from PI payload - for Match
    """
    num_to_remove = len(pi['scholarly'][key_name])
    if num_to_remove:
        x = 0
        while x < num_to_remove:
            pi['scholarly'][key_name][x] = pi['scholarly'][key_name][x].__dict__
            for item in remove_list:
                try:
                    del pi['scholarly'][key_name][x][item]
                except:
                    pass
            x += 1
    return pi


def clean_result_before_save(pi):
    # Master List to remove from everywhere
    try:
        remove_list = ['nav' , '_sections', '_filled']

        for x in remove_list:
            if x in pi:
                del pi[x]

            if 'scholarly' in pi:
                if x in pi['scholarly']:
                    del pi['scholarly'][x]

        # Sections that contain Scholarly Objects
        fields = ['coauthors', 'publications']
        for field in fields:
            if 'scholarly' in pi:
                pi = remove_scholarly_objects(pi, remove_list, field)
            else:
                pi = remove_objects(pi, remove_list, field)
        return pi
    except:
        # Ignore the errors for now - this is a nice to have step
        pass
    return pi
