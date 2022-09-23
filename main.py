import requests
from bs4 import BeautifulSoup
from constants import Authorization, Work


class YaDisk:
    def __init__(self, client_id: str, client_secret: str, token: str = None, user: str = None, pas: str = None):
        self.session = requests.Session()
        self.auth_url = Authorization.auth_url
        self.direct_url = Work.direct_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth = (client_id, client_secret)
        if user:
            self.user = user
        else:
            self.user = input("Login:")
        if user:
            self.pas = pas
        else:
            self.pas = input("Password:")
        if token:
            self.token = token
        else:
            self.token = self.get_token()
        self.session.auth = (self.user, self.pas)

    def get_code(self):
        print("Gets code")
        response = self.session.get(f"{self.auth_url}authorize?response_type=code&client_id={self.client_id}")
        print(f"{self.auth_url}/authorize?response_type=code&client_id={self.client_id}")
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            print(soup.h1)

            return soup.h1.text
        else:
            raise Exception(f"Response status code = {response.status_code}")

    def get_token(self):
        print("Gets token")
        data = {
            'grant_type': 'authorization_code',
            'code': 5430877,  #self.get_code(),
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        url1 = f"{self.auth_url}/token"
        loging = self.session.post(url1, data=data)
        print(url1)
        print(loging.status_code)
        print(loging.text)
        return loging

    @staticmethod
    def save_response(response):
        with open("result.html", "w+") as f:
            f.write(response.text)

    def create_folder(self, folder: str):
        print(f"{self.direct_url}?path={folder}")
        response = self.session.put(f"{self.direct_url}?path={folder}",
                                    headers={'Authorization': f'Basic {self.token}'})
        print(response.status_code)  # 201
        return response

    def upload(self, path: str):
        print(f"{self.direct_url}/upload?path={path}")
        response = self.session.get(f"{self.direct_url}/upload?path={path}",
                                    headers={'Authorization': f'Bearer {self.token}'})
        print(response.status_code)  # 200
        d_resp = dict(response.text)
        if d_resp["method"] == "PUT":
            response1 = self.session.put(f"{d_resp['href']}",
                                         headers={'Authorization': f'Bearer {self.token}'})
        else:
            response1 = self.session.get(f"{d_resp['href']}",
                                         headers={'Authorization': f'Bearer {self.token}'})  # TODO add exception
        print(response1.status_code)  # 201
        return response1

    def download(self, path: str):
        response = self.session.get(f"{self.direct_url}/download?path={path}",
                                    headers={'Authorization': f'Bearer {self.token}'})
        print(response.status_code)  # 200
        d_resp = dict(response.text)
        response1 = self.session.get(f"{d_resp['href']}",
                                     headers={'Authorization': f'Bearer {self.token}'})  # TODO add exception
        print(response1.status_code)  # 200
        return response1

    def delete(self, path, permanently: bool = True):
        if permanently:
            perm = "&permanently=true"
        else:
            perm = ""
        response = self.session.get(f"{self.direct_url}/download?path={path}{perm}",
                                    headers={'Authorization': f'Bearer {self.token}'})
        print(response.status_code)  # 202
        return response


if __name__ == '__main__':
    disk = YaDisk(
        Authorization.client_id,
        Authorization.client_secret,
        Authorization.token,
    )

    disk.create_folder(Work.folder1)
    # disk.delete(f"{Work.folder1}/{Work.file1}")

    # disk.upload(f"{Work.folder1}/{Work.file1}")
    #
    # disk.download(f"{Work.folder1}/{Work.file1}")
    # disk.delete(f"{Work.folder1}/{Work.file1}")
    # disk.upload(f"{Work.folder1}/{Work.file2}")
