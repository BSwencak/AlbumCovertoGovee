import os
from dotenv import load_dotenv
from govee import GoveeClient, Colors



load_dotenv()

GOVEE_API_KEY = os.getenv("GOVEE_API_KEY")

if not GOVEE_API_KEY:
    raise ValueError("GOVEE_API_KEY not found. Make sure it's in your .env file.")


# Initialize your client with your API key
client = GoveeClient(api_key=GOVEE_API_KEY, prefer_lan=True)

# Fetch and discover all connected devices
devices = client.discover_devices()

# Print the list of your devices
#for device in devices:
#    print(f"Device Name: {device.name}, Device ID: {device.id}")




device = client.get_device("PSU Bedroom")  # Change to your device ID
#client.set_color(device,color=Colors.RED,color_temp=3000) 
#client.set_color(device, (97, 35, 204)) 
client.power(device, True)  # Turn on the device
#client.set_brightness(device, 10)  # Set brightness to 100%



    