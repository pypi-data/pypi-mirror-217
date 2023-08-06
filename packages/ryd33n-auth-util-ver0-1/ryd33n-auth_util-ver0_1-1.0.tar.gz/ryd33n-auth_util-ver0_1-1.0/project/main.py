class User:
    """
    class User for init None Get from :class: `AuthUser`

    :param login: Логін користувача
    :type login: str
    :param password: Пароль Користувача
    :type passsword: str
    """

    def __init__(self, login,
                 password):
        """Initialized Method
        """
        self.login = login
        self.password = password

    def check_data(self, login, password):
        """
        Method Check Data

        :param login: Логін на який перевіряємо
        :type login: str
        :param password: Пароль на який перевіряємо
        :type: str

        :return: True Якщо це логін і пароль цього користувача
        :rtype: bool
        """
        pass
