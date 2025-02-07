import urllib.request

external_ip : str

def init():
    global external_ip
    external_ip = urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')
    print("Client IP:", external_ip)
