import ssl

cert_file = '../Certificates/cert.pem'

cert_dict = ssl._ssl._test_decode_cert(cert_file)

for subject in cert_dict['subject']:
    if subject[0][0] == 'commonName':
        print(f'Common Name (CN): {subject[0][1]}')