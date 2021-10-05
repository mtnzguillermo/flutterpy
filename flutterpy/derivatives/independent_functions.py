
import numpy as np


def complex2real_notation(fd_complex):

    fd_real = {'H1':{'values':[],'U_red':[]},
        'H2':{'values':[],'U_red':[]},
        'H3':{'values':[],'U_red':[]},
        'H4':{'values':[],'U_red':[]},
        'A1':{'values':[],'U_red':[]},
        'A2':{'values':[],'U_red':[]},
        'A3':{'values':[],'U_red':[]},
        'A4':{'values':[],'U_red':[]}}
    
    for letter_1 in 'ha':

        if letter_1 == 'a':
            factor_1 = 0.5
            deriv_letter = 'A'
        else:
            factor_1 = 1
            deriv_letter = 'H'

        for letter_2 in 'ha':
            
            if letter_2 == 'a':
                factor_2 = 0.5
                deriv_numbers = [2,3]
            else:
                factor_2 = 1
                deriv_numbers = [1,4]

            for input_value, k in zip(fd_complex['c_'+letter_1+letter_2]['values'], fd_complex['c_'+letter_1+letter_2]['k']):

                U_red = np.pi / k

                output_values = np.array([np.imag(input_value), np.real(input_value)]) * np.pi * 0.5 * factor_1 * factor_2

                for output_value, deriv_number in zip(output_values, deriv_numbers):
                    fd_real[deriv_letter+str(deriv_number)]['values'].append(output_value)
                    fd_real[deriv_letter+str(deriv_number)]['U_red'].append(U_red)
    
    return fd_real
                

def real2complex_notation(fd_real):
    pass


if __name__ == '__main__':
    fd_complex = {'c_aa':{'values':[2.4-0.36j],'k':[0.5]},
        'c_ah':{'values':[0.0071+1.2j],'k':[0.5]},
        'c_ha':{'values':[-3.6-0.45j],'k':[0.5]},
        'c_hh':{'values':[0.063-1.6j],'k':[0.5]}}

    fd_real = complex2real_notation(fd_complex)
    print(fd_real)