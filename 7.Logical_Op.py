Unit = input("Temperature in Farenheit or Celcius: ")

temperature = float(input("Enter Temperature: "))

if Unit == "C":
    temperature = round((9*temperature)/5 + 32, 2)
    print(f"The temperature in Farenheit: {temperature}F")

elif Unit == "F":
    temperature = round((temperature-32) * 5 / 9, 2)
    print(f"The temperature in Celcius: {temperature}C")

else:
    print(f"{Unit} is an invalid measure.")

    sunny = None

if Unit == "C" and temperature >= 77:
    print("The weather is sunny.")

elif Unit == "F" and temperature >= 25:
    print("The weather is sunny.")

else:
    print("The Weather is cloudy.")