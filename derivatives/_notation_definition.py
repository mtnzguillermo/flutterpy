
import sympy as sym

pi = sym.pi
i = sym.I
j = sym.I

d1, d2, d3, d4, d5, d6 = sym.symbols('d1 d2 d3 d4 d5 d6')
l1, l2, l3, l4, l5, l6 = sym.symbols('l1 l2 l3 l4 l5 l6')
m1, m2, m3, m4, m5, m6 = sym.symbols('m1 m2 m3 m4 m5 m6')
Ured = sym.symbols('Ured')

notation_settings = [
    {
        'name':'scanlan',
        'relations':{
            'H1': (Ured/2/pi)*l3,     'H2': (Ured/2/pi)*l5,  'H3': (Ured/2/pi)**2*l6,
            'H4': (Ured/2/pi)**2*l4,  'H5': (Ured/2/pi)*l1,  'H6': (Ured/2/pi)**2*l2,
            'A1': (Ured/2/pi)*m3,     'A2': (Ured/2/pi)*m5,  'A3': (Ured/2/pi)**2*m6,
            'A4': (Ured/2/pi)**2*m4,  'A5': (Ured/2/pi)*m1,  'A6': (Ured/2/pi)**2*m2,
            'P1': (Ured/2/pi)*d1,     'P2': (Ured/2/pi)*d5,  'P3': (Ured/2/pi)**2*d6,
            'P4': (Ured/2/pi)**2*d2,  'P5': (Ured/2/pi)*d3,  'P6': (Ured/2/pi)**2*d4
        }
    },
    {
        'name':'classic',
        'relations':{
            'H1': (Ured/2/pi)*l3/2,     'H2': (Ured/2/pi)*l5/2,  'H3': (Ured/2/pi)**2*l6/2,
            'H4': (Ured/2/pi)**2*l4/2,  'H5': (Ured/2/pi)*l1/2,  'H6': (Ured/2/pi)**2*l2/2,
            'A1': (Ured/2/pi)*m3/2,     'A2': (Ured/2/pi)*m5/2,  'A3': (Ured/2/pi)**2*m6/2,
            'A4': (Ured/2/pi)**2*m4/2,  'A5': (Ured/2/pi)*m1/2,  'A6': (Ured/2/pi)**2*m2/2,
            'P1': (Ured/2/pi)*d1/2,     'P2': (Ured/2/pi)*d5/2,  'P3': (Ured/2/pi)**2*d6/2,
            'P4': (Ured/2/pi)**2*d2/2,  'P5': (Ured/2/pi)*d3/2,  'P6': (Ured/2/pi)**2*d4/2
        }
    }
]