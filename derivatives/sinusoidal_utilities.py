
import numpy as np
from scipy.optimize import curve_fit
from scipy.fft import fft


def sin_func(t, A, phi, omega):
    return A*np.sin(omega*t+phi)


def sin_cos_func(t, a, b, c, omega):
    return a + b*np.cos(omega*t) + c*np.sin(omega*t)


def extract_sinusoidal_parameters(x, y, omega=None, function='phase'):

    if omega == None:

        omega_guess = GuessFrequency(np.array(x), np.array(y))*2*np.pi

        if function == 'phase':
            params, cov = curve_fit(sin_func, x, y, p0=[1,0,omega_guess], bounds=([0, -np.pi, 0], [np.inf, np.pi, np.inf]))

        elif function == 'sin_cos':
            params, cov = curve_fit(sin_cos_func, x, y, p0=[0,1,1,omega_guess], bounds=([-np.inf, 0, 0], [np.inf, np.inf, np.inf]))

        print('Freq guess: '+str(omega_guess/2/np.pi))
        print('Freq final: '+str(params[-1]/2/np.pi))

    else:

        if function == 'phase':
            def custom_func(t, A, phi):
                return A*np.sin(omega*t+phi)

        elif function == 'sin_cos':
            def custom_func(t, a, b, c):
                return a + b*np.cos(omega*t) + c*np.sin(omega*t)

        params, cov = curve_fit(custom_func, x, y)

    return params


def GuessFrequency(time, motion):

    # Generating frequency spectrum
    spectrum = fft(motion)

    # Calculating frequency domain
    N = len(time)-1
    time_step = (time[-1]-time[0]) / N
    freq_domain = np.linspace(0.0, 1.0/(time_step), N+1)

    # Getting maximum value of the spectrum (main frequency)
    main_freqs = freq_domain[np.abs(spectrum)==max(np.abs(spectrum))]

    # Only the first frequency, the second one is mirrored respect to the Nyquist frequency
    return(main_freqs[0])