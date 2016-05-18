"""
Classe para automatizar construção do sitemap e do breadgrumb
Terravision Geotecnologia e Geoinformação
16/05/2016
Wilson Beirigo Duarte
"""

class sitemap(object):
    """
    Rotina de montagem automática de sitmap e breadgrumb
    """

    # lista de registros
    # Cada novo registro deve ser cadastrado na lista abaixo para aparecer no menu
    # (Nome do item,  caminho, existe subitem (True/False)

    col = ( ('Home', 'home', 0, False, True),
            ('Clima', 'clima', 0, True, True),
            ('Mapa Estações', 'mapaestacoes', 1, False, True),
            ('Normais', 'normais', 1, False, True),
            ('Grafico Normais', 'grafnormais', 1, False, False),
            ('Automáticas', 'automaticas', 1, False, True),
            ('Grafico Linhas', 'graflinha', 2, False, False),
            ('Grafico Total', 'grafautomaticatotal', 2, False, False)

          )

    def _breadgrumb(self, _path):
        """
        Gera html contendo o breadgrumb a partir do path
        :param _path: caminho da pagina
        :return: expressão html para criar o breadgrumb
        """

        campos = [item for item in _path.split('/') if item != '']
        markup =  '<li {2} ><a href="{0}/">{1}</a></li>'

        path = '/'
        html = ''
        nivel = 0
        titulo = ''
        for item in campos:
            registro = [it  for it in self.col if it[1]== item and it[2] == nivel][0]
            if _path == path:
                key ='class ="active"'
                titulo = item[0]
            else:
                key = ''
            print(path, _path)
            html += markup.format(path, registro[0], key)
            nivel +=1

        return html, titulo

    def _menu(self):
        """
        Gera html para montar o menu
        :return: Html contendo menu e submenu
        """

        markup_normal = '<li class="active"><a href="{0}">{1}</a></li>'
        markup_grupo0 = '<li class="dropdown"><a href="{0}" class="dropdown-toggle" data-toggle="dropdown">{1}<b class="caret"></b></a>$$$</li>'
        markup_grupo1 = '<ul class="dropdown-menu"><li><a href="{0}">{1}</a></li></ul>'

        html = ''
        ingrupo = False
        marcador = ''
        for item in self.col:

            if not item[4]:
                continue

            if item[2] == 0:

                # se for novo item grava os submenus
                if ingrupo:
                    html = html.replace('$$$', marcador)
                    marcador = ''
                    ingrupo = False

                url = '/{0}/'.format(item[1])
            else:
                url += '{0}/'.format(item[1])

            if item[3]:
                html += markup_grupo0.format(url, item[0])
                ingrupo = True
            else:
                if ingrupo:
                    marcador += markup_grupo1.format(url, item[0])
                else:
                    html += markup_normal.format(url, item[0])

        #Se ao terminar o loop ainda estiver em submenu
        if ingrupo:
            html = html.replace('$$$', marcador)
            marcador = ''
            ingrupo = False

        return html


    def __init__(self, path):
        """
        Constroi o cabeçalho da página
        :param path: path da página
        :return: bloco html contendo o cabeçalho
        """
        html, titulo = self._breadgrumb(path)
        self.html = {'menu' : self._menu(), 'pagetitle': titulo, 'pagebreadgrumb' : html }


