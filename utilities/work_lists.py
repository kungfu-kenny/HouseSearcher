
def make_list_sublists(value_list:list, value_len:int) -> list:
    """
    Function which is dedicated to make sublists of the existing list
    Input:  value_list = list values of the value
            value_len = length which is currently used
    Output: we developed values of the     
    """
    return [value_list[i:i+value_len] for i in range(0, len(value_list), value_len)]
    
def make_list_transpose(value_list:list) -> list:
    """
    Function which is dedicated to transpose the list values
    Input:  value_list = list which is required to transpose
    Output: we developed transposed list
    """
    return map(list, zip(*value_list))