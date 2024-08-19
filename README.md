# ReservaApp

ReservaApp is a software designed in Python and Flet to efficiently manage reservations. Its intuitive interface facilitates both the registration and the consultation of reservations.

## Main Features

### 1. Registrar Reserva

The **Register Reservation** option allows users to quickly and easily register new reservations. The process includes:

- **Identification or Name**: Users can enter the customer's identification or name. Based on the input, an autocomplete window displays relevant suggestions using pre-existing data.

- **Intelligent Autocomplete**: The system pulls data from the `usuarios.xlsx` file, which contains the necessary information to auto-complete data, optimizing time and reducing errors.

### 2. Consultar Reservas

The **Consult Reservations** option provides an interface to search and review existing reservations. It is possible to access the details of each reservation and mark whether it was taken or not.

Reservations are saved in the `reservas.xlsx`

### 3. Administrar

The Manage option allows you to:

- Generate a report in an Excel file.
- Open the Excel file directly from the interface.
This section is available to all users without additional permissions.

## Requirements

- Python 3.11.9
- Libraries listed in `requirements.txt`

## Installation

Clone this repository:

```bash
- git clone https://github.com/GumeeR/Reservation-system
- cd Reservation-system
```

Install the dependencies:
```bash
pip install -r requirements.txt
```
## Execution
Run the application from the main.py file, either from Visual Studio Code or via the console using the following command:
```bash
flet run main.py
```
## Icon

To add an icon on the startup interface, place an image in the assets folder with the following name and extension:

`logo.png`
