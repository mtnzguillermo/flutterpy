
import numpy as np
import warnings

import utilities.sinusoidal_utilities as util


# Main object to manage flutter derivatives data
class FlutterDerivatives():

    def __init__(self, default_notation='real'):

        # Notation default settings
        # 'real' notation --> Scanlan's notation (H1, H2, A1, A2...)
        # 'complex' notation --> Starossek's notation (c_hh, c_ha...)
        self.available_notations = ['real', 'complex']
        self._check_notation(default_notation)
        self.default_notation = default_notation
        
        # Initializing dictionaries with the derivatives' data
        self.reset_all_derivatives()


    ########## USER METHODS

    def reset_all_derivatives(self):

        # Dictionary to store all derivative values, in all notations
        self.flutter_deriv = {'real':{}, 'complex':{}}
        
        # Creating/Overwriting derivatives dictionary (real notation)
        self.flutter_deriv['real'] = {}
        for letter in ['H', 'A', 'P']:
            for number in range(1,7):
                self.flutter_deriv['real'][letter+str(number)] = {'values':[], 'Ured':[]}

        # Creating/Overwriting derivatives dictionary (complex notation)
        self.flutter_deriv['complex'] = {}
        for letter_1 in ['h', 'a', 'p']:
            for letter_2 in ['h', 'a', 'p']:
                self.flutter_deriv['complex']['c_'+letter_1+letter_2] = {'values':[],'k':[]}


    def reset_derivative(self, deriv):

        # Check that the derivative's name is among the available ones
        self._check_derivative_name(deriv)
        
        # Clean the derivative data
        # TODO: clean associated derivatives in other notations
        # Maybe the derivatives need to be cleaned by pairs (H1-H4, A2-A3...)
        # If not, it is not possible to clean complex notation derivatives
        if deriv in list(self.flutter_deriv['real'].keys()):
            self.flutter_deriv['real'][deriv] = {'values':[], 'Ured':[]}
        elif deriv in list(self.flutter_deriv['complex'].keys()):
            self.flutter_deriv['complex'][deriv] = {'values':[],'k':[]}

    
    def reset_from_dictionary(self, dict):

        # TODO: Function to start a FlutterDerivatives object
        # from a self.flutter_deriv-type dictionary.
        # Necessary to check right format in input dictionary.

        pass

    
    def set_default_notation(self, new_notation):
        
        # Change output default notation
        self._check_notation(new_notation)
        self.default_notation = new_notation

    
    def set_default_parameters(self, U=None, B=None, delta_t=None, air_dens=None):

        # TODO: check input format
        # Maybe also use **kwargs instead

        if U != None:
            self.U = U
        
        if B != None:
            self.B = B
        
        if delta_t != None:
            self.delta_t = delta_t

        if air_dens != None:
            self.air_dens = air_dens

    
    def calculate_derivatives_from_forced_motion(self, **kwargs):
        
        # Start checking simulation parameters
        # TODO: consider simply changing the kwargs dictionary with the filled parameters
        sim_params = self._fill_with_default_simulation_parameters(**kwargs)

        # Check that the parameters have frequency data.
        # If yes, add it to the sim_params dictionary
        # I not, add 'None' to the dictionary
        sim_params['omega'] = self._check_frequency_input(**kwargs)

        # Check that the right motion and force time series have been provided
        provided_motion, provided_forces = self._check_motion_force_input(**kwargs)

        # Calculating derivatives pair by pair (with the motion and one force)
        for provided_force in provided_forces:
            self._calculate_derivative_pair_from_forced_motion(sim_params, provided_motion, provided_force, kwargs)


    def get_all_derivatives(self, notation=None):

        # If not provided, take the default value
        notation = self._fill_with_default_notation(notation)
        
        # Return a dictionary with all the derivative data
        return self.flutter_deriv[notation]


    def get_derivative(self, deriv):

        # Check if input is among the available ones
        self._check_derivative_name(deriv)
        
        # Return a small dictionary with only data from one derivative
        if deriv in self.flutter_deriv['real'].keys():
            return self.flutter_deriv['real'][deriv]
        elif deriv in self.flutter_deriv['complex'].keys():
            return self.flutter_deriv['complex'][deriv]
    

    def get_all_fitted_functions(self, degree=3, notation=None, fixed_start=True):

        # If not provided, take the default value
        notation = self._fill_with_default_notation(notation)

        # Use get_fitted_function to fit each single derivative
        functions = {}
        for deriv in self.flutter_deriv[notation]:
            functions[deriv] = self.get_fitted_function(deriv, degree=degree, fixed_start=fixed_start)
        # TODO: Think about returning only non-empty derivatives
        
        return functions
    

    def get_fitted_function(self, deriv, degree=3, fixed_start=True):

        # Check that the derivative name is among the available ones
        self._check_derivative_name(deriv)

        # The polynomials need to be fit in the real notation
        # (complex notation does not have polynomial shape)
        # Thus, if the required derivative is in complex notation
        # it is necessary to get the associated real derivatives
        if deriv in self.flutter_deriv['complex']:
            derivs_to_fit = self._get_related_derivatives(deriv)['real']
        else:
            derivs_to_fit = [deriv]

        # If a complex derivative is asked, two real derivatives must be fitted
        params = []
        for deriv_to_fit in derivs_to_fit:

            # Get derivative points in real notation
            x_data = self.flutter_deriv['real'][deriv_to_fit]['Ured']
            y_data = self.flutter_deriv['real'][deriv_to_fit]['values']

            # Check that there is calculated data in the derivative
            if len(x_data) > degree:

                # Fit the polynomial
                params.append(np.polyfit(x_data, y_data, degree))
            
            elif len(x_data) == 0:
                # TODO: The warnings only raise the first time they are called, not again after it
                msg = 'There are no calculated values for the specified derivative. '
                msg += 'Returning a "None" value instead of the fitted function.'
                warnings.warn(msg)

                return None
            
            else:
                # TODO: The warnings only raise the first time they are called, not again after it
                msg = 'There are not enough calculated values in this derivative. '
                msg += 'Returning a "None" value instead of the fitted function.'
                warnings.warn(msg)

                return None
        
        # The functions are calculated depending on the notation of the input derivative
        # If the derivative is real, the function represents a simple polynomial
        if deriv in self.flutter_deriv['real']:

            def real_fitted_function(ured):
                out = 0
                for exp, param in zip(reversed(range(degree+1)), params[0]):
                    out += param*ured**exp
                return out

            output = real_fitted_function

        # If the derivative is complex, it is necessary to translate the polynomials
        # of both associated real derivatives into a single complex function.
        elif deriv in self.flutter_deriv['complex']:
            
            def complex_fitted_function(k):
                
                # Calculation of the values of the associated real derivatives
                # The same polynomial, but changing U_red by pi/k
                real_derivs = []
                for param_set in params:
                    real_deriv = 0
                    print(param_set)
                    for exp, param in enumerate(param_set):
                        print(param, exp)
                        real_deriv += param*(k/np.pi)**exp
                    real_deriv *= (np.pi/k)**degree
                    real_derivs.append(real_deriv)

                # Calculation of the complex derivative with both real derivatives
                complex_deriv = 2/np.pi*(real_derivs[1] + 1j* real_derivs[0])

                # Depending on which derivative is, the relation between complex and
                # real derivatives can be twice or four times the base one
                deriv_split = deriv.split('_')
                for letter in deriv_split[1]:
                    if letter == 'a':
                        complex_deriv *= 2
                
                return complex_deriv
                
            output = complex_fitted_function

        return output


    ##### INTERNAL METHODS

    def _check_derivative_name(self, deriv):

        # Listing all available derivative names
        real_deriv_names = list(self.flutter_deriv['real'].keys())
        complex_deriv_names = list(self.flutter_deriv['complex'].keys())
        
        # Raise exception if the input is not among the available ones
        if deriv not in real_deriv_names and deriv not in complex_deriv_names:
            msg = 'Derivative name not recognised. '
            msg += 'It should be one of the following:\n'
            msg += str(real_deriv_names+complex_deriv_names)
            raise Exception(msg)


    def _check_notation(self, notation):
        
        # Raise exception if the input is not among the available ones
        if notation not in self.available_notations:
            msg = 'The requested notation is not among the available ones.'
            msg += ' Please select one of these: ' + str(self.available_notations)
            raise Exception(msg)


    def _check_motion_force_input(self, **kwargs):

        # Check that only one motion is provided
        motion_names = {'heave', 'pitch', 'sway'}
        provided_motion = motion_names.intersection(kwargs)
        if len(provided_motion) == 0:
            msg = 'No motion time series provided. '
            msg += 'Please provide one of the following variables: '
            msg += str(motion_names)
            raise Exception(msg)
        elif len(provided_motion) > 1:
            # TODO: This 'elif' would need to be suppressed if the function
            # is adapted to calculate from multi-direction simulations
            msg = 'Too many motion time series provided. '
            msg += 'Please provide only the excited motion time series.'
            raise Exception(msg)

        # Check that at least one force is provided
        force_names = {'lift', 'moment', 'drag'}
        provided_forces = force_names.intersection(kwargs)
        if len(provided_forces) == 0:
            msg = 'No force time series provided. '
            msg += 'Please provide at least one of the following variables: '
            msg += str(force_names)
            raise Exception(msg)

        # TODO: check that all time series have the same length

        return list(provided_motion)[0], list(provided_forces)


    def _check_frequency_input(self, **kwargs):
        
        # Inputs in **kwargs that would give frequency data
        possible_frequency_inputs = {'omega', 'frequency'}
        provided_inputs = possible_frequency_inputs.intersection(kwargs)

        # If only one is given, calculate omega (the angular frequency),
        # which will be the one used later.
        if len(provided_inputs) == 1:
            provided_input = list(provided_inputs)[0]
            if provided_input == 'omega':
                omega = kwargs['omega']
            elif provided_input == 'frequency':
                omega = kwargs['frequency']*2*np.pi

        # If none was given, raise exception and ask for frequency data
        elif len(provided_inputs) == 0:
            msg = 'No motion frequency was provided. '
            msg += 'The frequency will be estimated from the motion time series instead. '
            msg += 'However, the following results may be compromised, '
            msg += 'even if the motion frequency is below the nyquist frequency.'
            warnings.warn(msg)
            omega = None
        
        # If more than one were given, raise exception
        # to avoid incoherences between them
        else:
            msg = 'More than one frequency inputs were given. '
            msg += 'In order to avoid contradictions provide '
            msg += 'only one of the following inputs: '
            msg += str(possible_frequency_inputs)
            raise Exception(msg)
        
        # Return the omega value, it will be used later
        return omega


    def _fill_with_default_notation(self,notation):

        # Use default notation if none was provied
        if notation == None:
            notation = self.default_notation
        # If not, check the input notation
        else:
            self._check_notation(notation)

        return notation


    def _fill_with_default_simulation_parameters(self, **kwargs):
        
        # Preparation of the error message
        msg = 'The variable "{}" has no default value. It is necessary '
        msg += 'to provide a particular one when calling the function.'

        # Check if there is a provided value
        # If not, check if there is at least a default value
        if 'U' in kwargs:
            U = kwargs['U']
        else:
            if getattr(self, 'U', None) != None:
                U = self.U
            else:
                raise Exception(msg.format('U'))

        if 'B' in kwargs:
            B = kwargs['B']
        else:
            if getattr(self, 'B', None) != None:
                B = self.B
            else:
                raise Exception(msg.format('B'))

        if 'delta_t' in kwargs:
            delta_t = kwargs['delta_t']
        else:
            if getattr(self, 'delta_t', None) != None:
                delta_t = self.delta_t
            else:
                raise Exception(msg.format('delta_t'))

        if 'air_dens' in kwargs:
            air_dens = kwargs['air_dens']
        else:
            if getattr(self, 'air_dens', None) != None:
                air_dens = self.air_dens
            else:
                raise Exception(msg.format('air_dens'))
        
        # Return input parameters filled with default values when necessary
        sim_params = {'U':U, 'B':B, 'delta_t':delta_t, 'air_dens':air_dens}
        return(sim_params)
        

    def _calculate_derivative_pair_from_forced_motion(self, sim_params, m_name, f_name, data):

        # Extract the corresponding motion and force time-series
        motion = data[m_name]
        force = data[f_name]

        # Create the time time-series
        # It is just necessary to respect the time step
        # (the absolute value is not important, it will be shifted later). 
        time = [i*sim_params['delta_t'] for i in range(len(motion))]

        # Calculate the amplitude and phase of the motion
        if sim_params['omega'] == None:
            motion_ampl, phi, omega = util.extract_sinusoidal_parameters(time, motion)
        else:
            omega = sim_params['omega']
            motion_ampl, phi = util.extract_sinusoidal_parameters(time, motion, omega=omega)

        # Shift time series to ensure that the motion has no phase
        # (just a pure sinusoidal).
        time_lag = phi/omega
        time += time_lag

        # Fit the sine+cosine function
        # force = a + b*cos(omega*t) + c*sin(omega*t)
        a, b, c = util.extract_sinusoidal_parameters(time, force, omega=omega, function='sin_cos')

        # Get the names of the derivatives asociated
        # with this particular motion and force directions
        derivs_to_calc = self._get_derivatives_to_calculate(m_name, f_name)

        # Calculation of the flutter derivatives
        # COMPLEX NOTATION
        #      parameter            factor_0                factor_1    factor_2
        # H1       b     *   2/(dens*B^2*omega^2*ampl)   *     1      *    1
        # H4       c     *   2/(dens*B^2*omega^2*ampl)   *     1      *    1
        # A1       b     *   2/(dens*B^2*omega^2*ampl)   *     1      *   1/B
        # A4       c     *   2/(dens*B^2*omega^2*ampl)   *     1      *   1/B
        # H2       b     *   2/(dens*B^2*omega^2*ampl)   *    1/B     *    1
        # H3       c     *   2/(dens*B^2*omega^2*ampl)   *    1/B     *    1
        # A2       b     *   2/(dens*B^2*omega^2*ampl)   *    1/B     *   1/B
        # A3       c     *   2/(dens*B^2*omega^2*ampl)   *    1/B     *   1/B
        # REAL NOTATION
        #      parameter                factor_0               factor_1    factor_2
        # H1     c+b*i   *   4/(dens*B^2*omega^2*ampl*pi)   *     1      *    1
        # A1     c+b*i   *   4/(dens*B^2*omega^2*ampl*pi)   *     1      *   2/B
        # H2     c+b*i   *   4/(dens*B^2*omega^2*ampl*pi)   *    2/B     *    1
        # A2     c+b*i   *   4/(dens*B^2*omega^2*ampl*pi)   *    2/B     *   2/B
        f0_real = 2/(sim_params['air_dens']*omega**2*sim_params['B']**2*motion_ampl)
        f0_complex = 2*f0_real/np.pi
        if m_name == 'pitch':
            f1_real = 1/sim_params['B']
            f1_complex = 2*f1_real
        else:
            f1_real = 1
            f1_complex = 1
        if f_name == 'moment':
            f2_real = 1/sim_params['B']
            f2_complex = 2*f2_real
        else:
            f2_real = 1
            f2_complex = 1
        
        # Calculating and saving derivative values
        self.flutter_deriv['real'][derivs_to_calc['real'][0]]['values'].append(b*f0_real*f1_real*f2_real)
        self.flutter_deriv['real'][derivs_to_calc['real'][1]]['values'].append(c*f0_real*f1_real*f2_real)
        self.flutter_deriv['complex'][derivs_to_calc['complex']]['values'].append(complex(c,b)*f0_complex*f1_complex*f2_complex)

        # Calculating 'x-axis' values (the derivatives depend on them)
        freq = omega/2/np.pi
        Ured = sim_params['U']/freq/sim_params['B']
        k = omega*sim_params['B']/2/sim_params['U']

        # Saving 'x-axis' data
        self.flutter_deriv['real'][derivs_to_calc['real'][0]]['Ured'].append(Ured)
        self.flutter_deriv['real'][derivs_to_calc['real'][1]]['Ured'].append(Ured)
        self.flutter_deriv['complex'][derivs_to_calc['complex']]['k'].append(k)


    def _get_derivatives_to_calculate(self, m_name, f_name):
        # Each combination between motion (heave, pitch, sway) and
        # force (lift, moment, drag) has some derivatives associated
        # This function returns the corresponding derivative names

        if m_name == 'heave':
            real_indexes = [1,4]
            complex_letter_2 = 'h'
        elif m_name == 'pitch':
            real_indexes = [2,3]
            complex_letter_2 = 'a'
        elif m_name == 'sway':
            real_indexes = [5,6]
            complex_letter_2 = 'p'

        if f_name == 'lift':
            real_letter = 'H'
            complex_letter_1 = 'h'
        elif f_name == 'moment':
            real_letter = 'A'
            complex_letter_1 = 'a'
        elif f_name == 'drag':
            real_letter = 'P'
            if m_name == 'heave':
                real_indexes = [5,6]
            elif m_name == 'sway':
                real_indexes = [1,4]
            complex_letter_1 = 'p'
        
        # Bulding and returning dictionary with the derivative names
        derivs_to_calc = {}
        derivs_to_calc['real'] = [real_letter+str(real_indexes[0]), real_letter+str(real_indexes[1])]
        derivs_to_calc['complex'] = 'c_' + complex_letter_1 + complex_letter_2

        return derivs_to_calc


    def _get_related_derivatives(self, deriv):
        # This function returns a dictionary with all associated derivatives
        # in the different notations

        # Getting the associated motion and force
        # The procedure changes depending on the notation of the derivative
        if deriv in self.flutter_deriv['real']:
            # TODO: make the function work with real derivs as input
            pass

        if deriv in self.flutter_deriv['complex']:
            split_deriv = deriv.split('_')
            for letter_1, force in zip(['h','a','p'], ['lift','moment','drag']):
                if letter_1 == split_deriv[1][0]:
                    f_name = force
            for letter_2, motion in zip(['h','a','p'], ['heave','pitch','sway']):
                if letter_2 == split_deriv[1][1]:
                    m_name = motion
        
        # Calculating all derivatives associated with this force-motion combination
        related_derivs = self._get_derivatives_to_calculate(m_name, f_name)

        return related_derivs
            