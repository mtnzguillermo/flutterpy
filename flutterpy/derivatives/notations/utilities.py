
from flutterpy.derivatives.notations.notation import _check_notation_key, available_notations

def notation2notation(fd_in, notation_in, notation_out):
    
    fd_base = notation2base(fd_in, notation_in)
    fd_out = base2notation(fd_base, notation_out)

    return fd_out


def notation2base(fd_in, notation_in):

    _check_notation_key(notation_in)
    
    fd_out = available_notations[notation_in].deconvert(fd_in)
    
    return fd_out


def base2notation(fd_in, notation_out):

    _check_notation_key(notation_out)
    
    fd_out = available_notations[notation_out].convert(fd_in)
    
    return fd_out

'''
if __name__ == '__main__':
    fd_complex = {'c_aa':{'values':[2.4-0.36j],'k':[0.5]},
        'c_ah':{'values':[0.0071+1.2j],'k':[0.5]},
        'c_ha':{'values':[-3.6-0.45j],'k':[0.5]},
        'c_hh':{'values':[0.063-1.6j],'k':[0.5]}}

    fd_real = complex2real_notation(fd_complex)
    print(fd_real)
'''