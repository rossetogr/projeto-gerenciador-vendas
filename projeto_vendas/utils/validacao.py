def get_float_input(prompt, min_value=0.0):
    """Lê um float do usuário, garantindo que é um número válido e maior ou igual a min_value."""
    while True:
        try:
            value = float(input(prompt).replace(',', '.'))
            if value < min_value:
                print(f"O valor deve ser maior ou igual a {min_value:.2f}.")
            else:
                return value
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def get_int_input(prompt, min_value=1):
    """Lê um inteiro do usuário, garantindo que é um número válido e maior ou igual a min_value."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"O valor deve ser maior ou igual a {min_value}.")
            else:
                return value
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")