# function for get integer from dict
def Int_From_Dict(key, dict):
    if key in dict:
        return dict[key]
    else:
        return -1

# function for get string from dict
def Str_From_Dict(key, dict):
    if key in dict:
        return dict[key]
    else:
        return "None"