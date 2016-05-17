

class SiteMap(object):


    def __index__(self):

        self.data = []

        self.data.append(0, 'Home',          '/home/')
        self.data.append(1, 'Muda Senha',    '/mudasenha/')
        self.data.append(2, 'Sair',          '/mudasenha/')


    def bread_grumb(self, path):

        return '/home/'




