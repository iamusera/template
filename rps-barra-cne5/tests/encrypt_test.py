import unittest
from application import app
from application.common.utils.encrypt import encrypt, decrypt
from flask import current_app

class MyTestCase(unittest.TestCase):
    def test_something(self):
        aim = 'abcd'
        print(f'原始字符:{aim}')
        base_en = "S0FJWVVEU1NQTE04ODg4OA=="
        print(f'密钥:{base_en}')
        r = encrypt(aim, base_en)
        print(f'加密:{r}')
        s = decrypt(r, base_en)
        print(f'解密:{s}')
        self.assertEqual(s, aim)  # add assertion here


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
    unittest.main()
