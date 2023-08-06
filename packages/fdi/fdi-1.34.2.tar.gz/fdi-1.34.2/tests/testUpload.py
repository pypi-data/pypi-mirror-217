 
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

url = 'http://123.56.102.90:31702/csdb/v1/storage/upload?path=/grmtest/svom.products.grm.burst.EVT'
headers = {
    'X-CSDB-AUTOINDEX': '1',
    'X-CSDB-HASHCOMPARE': '0',
    'Accept': '*/*',
    'X-AUTH-TOKEN': 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJpaGVwdGVzdCIsInVzZXJJZCI6IjM2MzMiLCJuYW1lIjoiemhlbmdzaiIsImV4cCI6MTY4ODk3NDMzNX0.pnWmMYCAIsxo8JVObf-OYL3yOVBBF9-OxQfOAw-th0u37kwrB1UF_tpOSGlu3aZPD-mlSRKj-YjmlLDuAfGsIzb0pWxA9ERMedesDBdGLPOlb5qStvz-0PtYtotf37hI648Ty-zmOuaBMYqxl45VRd311jTbnFRSA-KqJVwe0tU'
}

multipart_data = MultipartEncoder(fields={'file': ('C:\\Users\\WJ\\Desktop\\gbg_evt_230427_15_v00.fits', open('C:\\Users\\WJ\\Desktop\\gbg_evt_230427_15_v00.fits', 'rb'), 'application/octet-stream')})
headers['Content-type'] = multipart_data.content_type
with requests.post(url, headers=headers, data=multipart_data) as response:
    print(response.text)


