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
    # Nome do item,  caminho, nivel do link, existe subitem (True/False), visível no menu, possue link dinâmico (True/False).

    col = ( ('Home', 'home', 0, False, True, False),
            ('Clima', 'clima', 0, True, True, False),
            ('Mapa Estações', 'mapaestacoes', 1, False, True, False),
            ('Foco Incêndio' , 'mapafocoincendio' , 1 , False , True, False),
            ('Normais', 'normais', 1, False, True, False),
            ('Grafico Normais', 'grafnormais', 2, False, False, False),
            ('Automáticas', 'automaticas', 1, False, True, False),
            ('Grafico Linhas', 'grafautomatica', 2, False, False, False),
            ('Grafico Total', 'grafautomaticatotal', 2, False, False, False),
            ('Impacto', 'impacto', 0, True, True, False),
            ('Empresas', 'lst_empresa', 1, False, True, False),
            ('Projetos', 'projetos', 1, False, True, False),
            ('Perfil Projeto', 'perfil_projeto', 2, False, False, True),
            ('Equipe', 'admin_grupo', 3, False, False, True),
            ('Questionario', 'questionario', 3, False, False, True),
            ('Quadro AIA', 'quadro', 1, False, False, True),
            ('Gabarito', 'gabarito', 2, False, False, True),
            ('Editar Area', 'editar_area', 3, False, False, True),
            ('Criar Area', 'criar_area', 3, False, False, True),
            ('Editar Impacto', 'editar_impacto_projeto', 3, False, False, True),
            ('Criar Impacto', 'criar_impacto_projeto', 3, False, False, True),
            ('Editar Diagnostico', 'editar_diagnostico', 3, False, False, True),
            ('Criar Diagnostico', 'criar_diagnostico', 3, False, False, True),
            ('Ver Impacto', 'ver_impacto', 3, False, False, True),
            ('Camada', 'camada', 0, True, True, False),
            ('Lista de Locais', 'local', 1, False, True, False),
            ('Criar Local', 'criar', 2, False, False, False),
            ('Editar Local', 'editar', 2, False, False, True),
          )

    def _breadgrumb(self, _path):
        """
        Gera html contendo o breadgrumb a partir do path
        :param _path: caminho da pagina
        :return: expressão html para criar o breadgrumb
        """

        campos = [item for item in _path.split('/') if item != '']
        key ='class ="active"'

        path = '/'
        html = ''
        nivel = 0
        titulo = ''
        for i, item in enumerate(campos):
            reg = [it for it in self.col if it[1] == item and it[2] == nivel]
            if not reg:
                continue
            registro = reg[0]

            path += '{0}/'.format(registro[1])

            if len(campos) >= nivel+1 or nivel == 2:
                titulo = registro[0]
                if (len(campos)-2) == i:
                    key ='class="active"'
                else:
                    key = ''

            if registro[5]:
                markup = '<li {0}><a>{2}</a></li>'
            else:
                markup = '<li {0}><a href="{1}">{2}</a></li>'

            html += markup.format(key, path, registro[0])

            nivel += 1

        return html, titulo

    def _menu(self):
        """
        Gera html para montar o menu
        :return: Html contendo menu e submenu
        """

        markup_normal = '<li class="active"><a href="{0}">{1}</a></li>'
        markup_grupo0 = '<li class="dropdown"><a href="{0}" class="dropdown-toggle" data-toggle="dropdown">{1}<b class="caret"></b></a><ul class="dropdown-menu">$$$</ul></li>'
        markup_grupo1 = '<li><a href="{0}">{1}</a></li>'

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
                path0 = url
            else:
                if item[2] == 1:
                    url = path0 + '{0}/'.format(item[1])

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

        return html


    def __init__(self, path):
        """
        Constroi o cabeçalho da página
        :param path: path da página
        :return: bloco html contendo o cabeçalho
        """
        html, titulo = self._breadgrumb(path)
        self.context = {'menu' : self._menu(), 'pagetitle': titulo, 'pagebreadgrumb' : html }


