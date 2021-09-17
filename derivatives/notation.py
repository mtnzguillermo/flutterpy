
import numpy as np
import sympy as sym

from ._notation_definition import notation_settings

class Notation():

    def __init__(self, name, relations):

        self.name = name
        self.relations = relations

        self.base_derivs = []
        for letter in 'dlm':
            for number in range(1,7):
                self.base_derivs.append(letter+str(number))
                
    def convert(self,fd_in):

        # Initialize the output set of derivatives
        fd_out = {}

        for deriv in self.relations:

            # Initialize the corresponding derivative in the output set
            fd_out[deriv] = {'values':[], 'Ured':[]}

            # Take the formula defining this derivative
            formula = self.relations[deriv]

            # Check which base derivatives are in the formula
            base_derivs_needed = []
            for base_deriv in self.base_derivs:
                if  formula.has(sym.sympify(base_deriv)):
                    base_derivs_needed.append(base_deriv)

            # Obtain Ured (x-axis) data
            Ureds = fd_in[base_derivs_needed[0]]['Ured']
            
            # Check that the Ureds of the needed derivatives are identical
            if len(base_derivs_needed) > 1:
                for base_deriv in base_derivs_needed[1:]:
                    if fd_in[base_deriv]['Ured'] != Ureds:
                        msg = "The derivative '" + deriv + "' requires values from "
                        msg += 'several base derivatives (' + str(base_derivs_needed)[1:-1]
                        msg += ') which do not have the same U_red values (x-axis data). '
                        msg += 'It is thus impossible to convert the data into the '
                        msg += "'" + self.name + "' notation without losing information."
                        raise Exception(msg)

            # Calculate the values for each Ured
            for index, Ured in enumerate(Ureds):

                # Substitute the formula and evaluate
                deriv_value = formula.subs(sym.sympify('Ured'), Ured)
                for base_deriv in base_derivs_needed:
                    value = fd_in[base_deriv]['values'][index]
                    deriv_value = deriv_value.subs(sym.sympify(base_deriv), value)
                deriv_value = deriv_value.evalf()
                
                # Convert to standard python complex (if it is a complex number)
                if deriv_value.has(sym.I):
                    deriv_value = complex(deriv_value)

                # Fill the values of the new derivative
                fd_out[deriv]['values'].append(deriv_value)
            
            # Fill the Ured data
            fd_out[deriv]['Ured'] = Ureds

        return fd_out
    
    def deconvert(self,fd_in):

        # TODO: implement inverse convert

        fd_out = fd_in

        return fd_out

    def _check_set_notation(self,fd_set):

        # TODO: Method to check if the imputed dictionary fits
        # with the notation of the corresponding instance

        pass


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


def _check_notation_key(notation_key):

    if notation_key not in available_notations and notation_key != 'base':
        msg = "The notation '" + notation_key + "' is not among the available ones. "
        msg += 'Choose one of the following: ' + str(list(available_notations.keys()))[1:-1] + '.'
        raise Exception(msg)


available_notations = {}
for notation in notation_settings:
    available_notations[notation['name']] = Notation(notation['name'],notation['relations'])
