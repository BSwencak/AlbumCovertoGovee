from govee import GoveeClient

def init_govee(api_key):
    return GoveeClient(api_key=api_key, prefer_lan=True)

def get_devices(client):
    return client.discover_devices()

def set_color(client, device_id, rgb):
    device = client.get_device(device_id)
    client.set_color(device, rgb)

def power(client, device_id, state):
    device = client.get_device(device_id)
    client.power(device, state)

def set_brightness(client, device_id, value):
    device = client.get_device(device_id)
    client.set_brightness(device, value)
