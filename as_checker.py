as_number = int(input("Ingrese el número de AS de BGP: "))

if 64512 <= as_number <= 65534:
    print("El AS ingresado es PRIVADO.")
elif 1 <= as_number <= 64495:
    print("El AS ingresado es PÚBLICO.")
else:
    print("El número ingresado no corresponde a un rango válido de BGP.")