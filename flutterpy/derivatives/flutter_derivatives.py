
import numpy as np
import warnings

import flutterpy.derivatives.sinusoidal_utilities as util
import flutterpy.derivatives.notations.notation as ntt


# Main object to manage flutter derivatives data
class FlutterDerivatives():

    def __init__(self, default_notation='scanlan'):

        # Notation default settings
        ntt._check_notation_key(default_notation)
        self.default_notation = default_notation
        
        # Initializing dictionary with the derivatives' data
        self.reset_all_derivatives()

        # Other class variables needed
        self.sim_param_keys = ['U', 'B', 'delta_t', 'fluid_dens']
        self.default_sim_params = {}


    ########## USER METHODS

    def reset_all_derivatives(self):

        # Dictionary to store all derivative values, in all notations
        self.fd_data = {}
        
        # Creating/Overwriting derivatives dictionary (base notation)
        for letter in 'dlm':
            for number in range(1,7):
                self.fd_data[letter+str(number)] = {'values':[], 'Ured':[]}


    def reset_derivative(self, deriv):

        # Check that the derivative's name is among the available ones
        self._check_derivative_name(deriv)
        
        # Clean the derivative data
        self.fd_data[deriv] = {'values':[], 'Ured':[]}

        # TODO: Think about ways to clean the deerivatives.
        #   - Maybe it is necessary to clean its pair.
        #   - Would be cool to erase from other notations' keys


    def reset_from_dictionary(self, dict):

        # TODO: Function to start a FlutterDerivatives object
        # from a self.fd_data-type dictionary.
        # Necessary to check right format in input dictionary.

        pass

    
    def set_default_notation(self, new_notation):
        
        # Change output default notation
        ntt._check_notation_key(new_notation)
        self.default_notation = new_notation

    
    def set_default_parameters(self, **kwargs):

        # TODO: check input format

        for param in self.sim_param_keys:
            if param in kwargs:
                self.default_sim_params[param] = kwargs[param]

    
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
        if notation == 'base':
            return self.fd_data
        else:
            fd_data_converted = ntt.base2notation(self.fd_data,notation)
            return fd_data_converted


    def get_derivative(self, deriv):

        # TODO: Possibility to extract derivatives in the current notation

        # Check if input is among the available ones
        self._check_derivative_name(deriv)
        
        # Return a small dictionary with only data from one derivative
        return self.fd_data[deriv]
    

    def get_all_fitted_functions(self, degree=3, notation=None, fixed_start=True):

        # TODO
        
        pass
    

    def get_fitted_function(self, deriv, degree=3, fixed_start=True):

        # TODO
        
        pass



    ##### INTERNAL METHODS

    def _check_derivative_name(self, deriv):

        # TODO: include the current default notation
        
        # Raise exception if the input is not among the base derivatives
        if deriv not in self.fd_data:
            msg = 'Derivative name not recognised. '
            msg += 'It should be one of the following:\n'
            msg += str(list(self.fd_data.keys()))[1:-1]
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
            ntt._check_notation_key(notation)

        return notation


    def _fill_with_default_simulation_parameters(self, **kwargs):
        
        # Preparation of the error message
        msg = 'The variable "{}" has no default value. It is necessary '
        msg += 'to provide a particular one when calling the function.'

        # Initialize the dictionary which will be returned
        sim_params = {}

        # Check if there is a provided value
        # If not, check if there is at least a default value
        for param in self.sim_param_keys:
            if param in kwargs:
                sim_params[param] = kwargs[param]
            else:
                if param in self.default_sim_params:
                    sim_params[param] = self.default_sim_params[param]
                else:
                    raise Exception(msg.format(param))
        
        # Return input parameters filled with default values when necessary
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
        _, b, c = util.extract_sinusoidal_parameters(time, force, omega=omega, function='sin_cos')

        # Get the names of the derivatives asociated
        # with this particular motion and force directions
        derivs_to_calc = self._get_derivatives_to_calculate(m_name, f_name)

        # Calculation of the flutter derivatives
        #       parameter             factor_0             factor_1      factor_2
        # l3    b*U/omega   *    2/(dens*U^2*B*ampl)   *      1      *      1
        # l4       c*B      *    2/(dens*U^2*B*ampl)   *      1      *      1
        # l5    b*U/omega   *    2/(dens*U^2*B*ampl)   *      1      *     1/B
        # l6       c*B      *    2/(dens*U^2*B*ampl)   *      1      *     1/B
        # m3    b*U/omega   *    2/(dens*U^2*B*ampl)   *     1/B     *      1
        # m4       c*B      *    2/(dens*U^2*B*ampl)   *     1/B     *      1
        # m5    b*U/omega   *    2/(dens*U^2*B*ampl)   *     1/B     *     1/B
        # m6       c*B      *    2/(dens*U^2*B*ampl)   *     1/B     *     1/B
        f0 = 2/(sim_params['fluid_dens']*sim_params['U']**2*sim_params['B']**2*motion_ampl)
        if m_name == 'pitch':
            f1= 1/sim_params['B']
        else:
            f1 = 1
        if f_name == 'moment':
            f2 = 1/sim_params['B']
        else:
            f2 = 1
        
        # Calculating and saving derivative values
        self.fd_data[derivs_to_calc[0]]['values'].append(b*sim_params['U']/omega * f0 * f1 * f2)
        self.fd_data[derivs_to_calc[1]]['values'].append(c*sim_params['B'] * f0 * f1 * f2)

        # Calculating 'x-axis' values (the derivatives depend on them)
        freq = omega/2/np.pi
        Ured = sim_params['U']/freq/sim_params['B']

        # Saving 'x-axis' data
        self.fd_data[derivs_to_calc[0]]['Ured'].append(Ured)
        self.fd_data[derivs_to_calc[1]]['Ured'].append(Ured)


    def _get_derivatives_to_calculate(self, m_name, f_name):
        # Each combination between motion (heave, pitch, sway) and
        # force (lift, moment, drag) has some derivatives associated
        # This function returns the corresponding derivative names

        if m_name == 'heave':
            numbers = [3,4]
        elif m_name == 'pitch':
            numbers = [5,6]
        elif m_name == 'sway':
            numbers = [1,2]

        if f_name == 'lift':
            letter = 'l'
        elif f_name == 'moment':
            letter = 'm'
        elif f_name == 'drag':
            letter = 'd'
        
        # Bulding and returning dictionary with the derivative names
        derivs_to_calc = [letter+str(numbers[0]), letter+str(numbers[1])]

        return derivs_to_calc
            