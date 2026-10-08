import tkinter
import pygame
import requests
from datetime import datetime

# wow whoever made this must be real talented

pygame.mixer.init()

pygame.mixer.music.load("weathermusic.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(1)


window = tkinter.Tk()
window.title("Weather")
window.geometry("500x500")
window.resizable(False, False)
window.attributes("-topmost", True)

bg_image = tkinter.PhotoImage(file="background.png")

canvas = tkinter.Canvas(window, width=500, height=500)
canvas.place(x=0, y=0)
canvas_bg = canvas.create_image(0, 0, anchor="nw", image=bg_image)


# current weather
current_label = canvas.create_text(20, 20, anchor="nw", text="", fill="black", font=("Arial", 15), justify="left")

#hourly weather

hourly_label = canvas.create_text(20, 110, anchor="nw", text="", fill="black", font=("Arial", 10), justify="left")

# api stuff
url = "https://api.open-meteo.com/v1/forecast"
paramS = {
    "latitude": "REPLACE ME",
    "longitude": "REPLACE ME",
    "current_weather": True,
    "daily": "weather_code",
    "hourly": (
        "temperature_2m,apparent_temperature,"
        "precipitation_probability,precipitation,"
        "rain,showers,snowfall,snow_depth"
        
        ),
    "timezone":"auto"
    }

def weather_update():
    try:
        response=requests.get(url, params=paramS, timeout=10)
        data = response.json()
        
        current = data["current_weather"]
        current_text = (
            f"Temperature: {current['temperature']}*C \n"
            f"Feels like: {current['temperature']}*C \n"
            f"Windspeed: {current['windspeed']} km/h \n"
            f"Weather Code: {current['weathercode']}"
            
        )
        canvas.itemconfig(current_label, text=current_text)
        
        
        hourly = data["hourly"]
        hourly_text = ""
        
        for i in range(24):
            time = datetime.fromisoformat(hourly["time"][i]).strftime("%a %H:%M")
            temp = hourly["temperature_2m"][i]
            feels = hourly["apparent_temperature"][i]
            rain = hourly["precipitation_probability"][i]
            
            hourly_text += f"{time} | {temp}*C (feels {feels}*C) | Rain {rain}% \n"
        
        canvas.itemconfig(hourly_label, text=hourly_text)
        
    except Exception as e:
        canvas.itemconfig(current_label, text="Failed to fetch weather data.")
        canvas.itemconfig(hourly_label, text=str(e))
    
    window.after(600000, weather_update)

weather_update()

window.mainloop()
