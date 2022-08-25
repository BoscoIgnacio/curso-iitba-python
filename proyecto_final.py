from scipy import signal as sg
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### definimos la abreviatura para femenino (f), masculino(m)
def sex_abbr_to_text(sex_abbr):
    if sex_abbr.lower() == 'f':
        return 'Femenino'
    elif sex_abbr.lower() == 'm':
        return 'Masculino'
    else:
        raise ValueError(f"{sex_abbr} no es un sexo reconocido.")

### definimos función para determinar la actividad del paciente
def act_patient(x, sex):
    if sex == "m":
        if 60 > x and x < 90:
            return "El paciente esta en reposo"
        elif x >= 90:
            return "El paciente esta realizando actividad fisica"
        elif x <= 60:
            return "El paciente esta durmiendo"
    elif sex == "f":
        if 70 > x and x < 100:
            return "La paciente esta en reposo"
        elif x >= 100:
            return "La paciente esta realizando actividad fisica"
        elif x <= 70:
            return "La paciente esta durmiendo"
    else:
        raise ValueError

### lectura del electrocardiograma
dataFrame = pd.read_excel("electrocardiograma.xlsx", usecols=[1, 2])
signal = np.array(dataFrame['señal'])
time = list(dataFrame['tiempo'])

### buscamos los picos de señal con find_peaks
peaks = sg.find_peaks(signal, height=1)

### calculo de frecuencia cardiaca del paciente(hr = heart rate)
hr = 60 * len(peaks[0]) / max(time)

### input de sexo del paciente
while True:
    sex = input('Ingrese sexo, Masculino (M) o Femenino (F):').lower()
    if sex not in ('m', 'f'):
        print('Error. Ingrese M o F')
    else:
        break

### graficamos
plt.plot(time, signal, label='Señal')
plt.plot(list(map(lambda index: time[index], peaks[0])), peaks[1]['peak_heights'], 'x', label='Picos')
plt.title(f"Frecuencia cardiaca: {int(hr)} latidos por minuto")
plt.xlabel(f"Tiempo en segundos\nSexo del paciente: {sex_abbr_to_text(sex)}")
plt.ylabel('Señal en eV')
plt.grid()
plt.legend()
plt.show()

### ejecutamos la funcion
state = act_patient(hr, sex)

### guardamos en un .txt
with open("Resultados electrocardiograma.txt","w+") as f:
    f.write(f"Sexo del paciente: {sex_abbr_to_text(sex)}\nFrecuencia Cardiaca: {int(hr)}\n{state}\n")
### end of code