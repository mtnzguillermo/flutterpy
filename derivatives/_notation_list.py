

notation_list = [
    {
        'name':'real',
        'relations':{
            'convert':{
                'H1':'(Ured/2/pi)*l3',    'H2':'(Ured/2/pi)*l5',  'H3':'(Ured/2/pi)**2*l6',
                'H4':'(Ured/2/pi)**2*l4', 'H5':'(Ured/2/pi)*l1',  'H6':'(Ured/2/pi)**2*l2',
                'A1':'(Ured/2/pi)*m3',    'A2':'(Ured/2/pi)*m5',  'A3':'(Ured/2/pi)**2*m6',
                'A4':'(Ured/2/pi)**2*m4', 'A5':'(Ured/2/pi)*m1',  'A6':'(Ured/2/pi)**2*m2',
                'P1':'(Ured/2/pi)*d1',    'P2':'(Ured/2/pi)*d5',  'P3':'(Ured/2/pi)**2*d6',
                'P4':'(Ured/2/pi)**2*d2', 'P5':'(Ured/2/pi)*d3',  'P6':'(Ured/2/pi)**2*d4'
            },
            'deconvert':{
                'd1':'(2*pi/Ured)*P1',    'd2':'(2*pi/Ured)**2*P4', 'd3':'(2*pi/Ured)*P5',
                'd4':'(2*pi/Ured)**2*P6', 'd5':'(2*pi/Ured)*P2',    'd6':'(2*pi/Ured)**2*P3',
                'l1':'(2*pi/Ured)*H5',    'l2':'(2*pi/Ured)**2*H6', 'l3':'(2*pi/Ured)*H1',
                'l4':'(2*pi/Ured)**2*H4', 'l5':'(2*pi/Ured)*H2',    'l6':'(2*pi/Ured)**2*H3',
                'm1':'(2*pi/Ured)*A5',    'm2':'(2*pi/Ured)**2*A6', 'm3':'(2*pi/Ured)*A1',
                'm4':'(2*pi/Ured)**2*A4', 'm5':'(2*pi/Ured)*A2',    'm6':'(2*pi/Ured)**2*A3'
            }
        }
    }
]