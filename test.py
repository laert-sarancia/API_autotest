import main
from constants import Authorization, Work

disk = main.YaDisk(client_id=Authorization.client_id,
                   client_secret=Authorization.client_secret,
                   token=Authorization.token,
                   user="testuser",
                   pas="pass",
                   )


def test0():
    response = disk.create_folder(Work.folder1)
    assert response.status_code == 201


def test1():
    response = disk.upload(Work.file1)
    assert response.status_code == 200


if __name__ == '__main__':
    test0()
