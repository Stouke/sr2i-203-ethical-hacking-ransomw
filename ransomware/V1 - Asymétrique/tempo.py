import base64
with open('public.pem', 'rb') as f:
    public = f.read()
print(base64.b64encode(public))

