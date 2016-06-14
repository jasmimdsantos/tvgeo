from impacto.models import  Impacto, Meio


source = """1	Alteração das propriedades físicas do solo
1	Indução e intensificação de processos erosivos e movimentos de massa
1	Aumento do assoreamento de cursos d'água por sedimentos inertes
1	Redução da disponibilidade hídrica para a produção industrial
1	Redução da disponibilidade hídrica para a produção agrícola
1	Redução da disponibilidade hídrica para comunidades tradicionais
1	Redução da disponibilidade hídrica para as comunidades locais
1	Alteração das propriedades químicas do solo
1	Contaminação do solo por óleos, graxas e derivados de petróleo
1	Contaminação do solo por elementos radioativos
1	Contaminação do solo por metais pesados
1	Contaminação por metais pesados
1	Alterações na qualidade das águas superficiais por metais pesados
1	Alterações na qualidade das águas superficiais por bactérias
1	Alterações na qualidade das águas superficiais por sedimentos
1	Alterações na qualidade das águas subterrâneas por metais pesados
1	Alterações na qualidade das águas subterrâneas por bactérias
1	Alterações na qualidade das águas subterrâneas por elementos radioativos
1	Alterações na qualidade das águas subterrâneas por óleos, graxas e derivados de petróleo
1	Alteração dos níveis de ruído
1	Alteração da qualidade do ar por fumaça preta e aerossóis
1	Alteração da qualidade do ar por gases tóxicos de alta periculosidade
1	Alteração da qualidade do ar por gases nocivos a saúde
1	Alteração da qualidade do ar por particulados em suspensão (PTS, PM10 e PM2,5)
1	Alteração das propriedades físicas do solo (estrutura, compactação, desagregação)
1	Indução e intensificação de processos erosivos e movimentos de massa (voçorocas, ravinamentos, erosões laminares)
1	Assoreamento de cursos d'água por sedimentos não tóxicos (inertes)
1	Alteração da dinâmica hídrica superficial (alteração de fluxo, de direção, de vazão, velocidade de escoamento)
1	Rebaixamento do nível freático
1	Redução da disponibilidade hídrica
1	Alteração das propriedades químicas do solo
1	Alteração da qualidade do ar
1	Alteração dos níveis de ruído
1	Incremento na geração de vibrações
1	Alteração dos padrões naturais da dinâmica hídrica superficial
1	Interferências ou mudanças no nível freático
1	Aumento do consumo de água
1	Aumento da disponibilidade hídrica
1	Alteração das propriedades químicas do solo
1	Alterações na qualidade das águas superficiais
1	Alterações na qualidade das águas subterrâneas
1	Alterações na circulação atmosférica local
1	Alteração da qualidade do ar
1	Alteração da dispersão atual de poluentes atmosféricos
1	Alteração das temperaturas locais
1	Mudanças no regime dos ventos locais
1	Mudanças no regime da umidade relativa do ar
1	Mudanças no regime de precipitação
1	Alteração da composição química da atmosfera local
1	Diminuição dos gases de efeito estufa
1	Aumento na geração de gases de efeito estufa
1	Alteração do micro clima local
1	Alteração nos níveis atuais de ruído
2	Redução da cobertura vegetal nativa, devido à supressão da vegetação
2	Perda de indivíduos da flora, devido à supressão da vegetação
2	Fragmentação da vegetação nativa, devido à supressão da vegetação
2	Intervenção em vegetação em APP, devido à supressão da vegetação
2	Perda de indivíduos da fauna terrestre, devido à supressão da vegetação e atividades correlacionadas
2	Perda e/ou alteração de hábitat, devido à supressão da vegetação e atividades correlacionadas
2	Alteração na composição e/ou na estrutura das comunidades faunísticas, devido à supressão da vegetação e atividades correlacionadas
2	Dispersão forçada de indivíduos da fauna, devido à supressão da vegetação, abertura de acessos e tráfego intenso de maquinário
2	Perda de indivíduos da fauna por atropelamento, devido ao tráfego intenso de maquinário
2	Interferência na atividade acústica da fauna, devido à abertura de acessos e tráfego intenso de maquinário
2	Estímulo às atividades de caça e apanha, devido à presença constante de pessoas (operários e comunidade local)
2	Perda de indivíduos da fauna aquática, devido à intervenção em cursos d'água
2	Perda e/ou alteração de hábitat, devido à intervenção em cursos d'água
2	Alteração na composição e/ou na estrutura das comunidades faunísticas, devido à intervenção em cursos d'água
2	Redução da cobertura vegetal nativa, devido à supressão da vegetação
2	Perda de indivíduos da flora, devido à supressão da vegetação
2	Fragmentação da vegetação nativa, devido à supressão da vegetação
2	Intervenção em vegetação em APP, devido à supressão da vegetação
2	Perda de indivíduos da fauna terrestre, devido à supressão da vegetação e atividades correlacionadas
2	Perda e/ou alteração de hábitat, devido à supressão da vegetação e atividades correlacionadas
2	Alteração na composição e/ou na estrutura das comunidades faunísticas, devido à supressão da vegetação e atividades correlacionadas
2	Perda e/ou alteração de hábitat, devido à evolução da cava
2	Alteração na composição e/ou na estrutura das comunidades faunísticas, devido à evolução da cava
2	Perda de indivíduos da fauna por atropelamento, devido ao tráfego intenso de maquinário
2	Dispersão forçada de indivíduos da fauna, devido ao tráfego intenso de maquinário
2	Interferência na atividade acústica da fauna, devido ao tráfego intenso de maquinário
2	Estímulo às atividades de caça e apanha, devido à presença constante de pessoas (operários e comunidade local)
2	Aumento da diversidade da fauna local
2	Melhoria do sistema ecológico local
2	Aumento da diversidade florística local
2	Conexão de corredores ecológicos anteriormente fragmentados
2	Perda de indivíduos da fauna aquática, devido à intervenção em cursos d'água
2	Perda e/ou alteração de hábitat, devido à intervenção em cursos d'água
2	Alteração na composição e/ou na estrutura das comunidades faunísticas, devido à intervenção em cursos d'água
2	Alteração na dinâmica ecológica das comunidades aquática, terrestre e edáfica, devido às atividades de desmontagem e fechamento das estruturas
2	Estímulo às atividades de caça e apanha, devido às atividades de desmontagem e fechamento das estruturas
3	Aumento da Geração de Expectativas
3	Alteração da Paisagem
3	Alteração dos modos de vida
3	Desestruturação de laços de reciprocidade
3	Aumento da geração de tensões sociais
3	Remoção populacional compulsória
3	Aumento dos casos de vulnerabilidade infantil
3	Aumento dos casos de vulnerabilidade social
3	Aumento da geração de empregos
3	Aumento nos casos de violência social
3	Aumento e geração de incômodos (Aspectos físicos)
3	Incremento nos casos de prostituição, violência contra mulheres e homossexuais
3	Diminuição de áreas agricultáveis
3	Mudança na cultura e religião local
3	Incremento da produção de ortifulticultura
3	Incremento da produção de fontes energéticas renováveis
3	Incremento da produção energética
3	Incremento da produção de grãos
3	Incremento da produção pecuária
3	Incremento da arrecadação pública
3	Mudança nos modos de vida tradicional
3	Incremento da circulação de bens e serviços
3	Incremento da pressão sobre infraestrutura
3	Aumento da valorização imobiliária
3	Incremento dos fluxos migratórios
3	Supressão de patrimônio arqueológico
3	Incremento da pressão sobre sistema viário
3	Aumento dos problemas de saúde ocupacional
3	Aumento nos casos de saúde pública
3	Aumento dos casos de doenças respiratórias
3	Aumento nos caos de doenças mentais
3	Aumento dos casos de doenças tropicais (arboviroses)
3	Alteração da dinâmica socioeconômica regional
3	Indução do aumento das atividades informais
3	Indução do aumento das atividades comerciais
3	Indução do aumento das atividades industriais
3	Indução do aumento da produtividade agrícola
3	Dificuldade de acesso das vias locais em função de cercamento
3	Alteração do cotidiano das famílias e comunidades de entorno
3	Geração de incômodos adversos (ar, poeira, ruído, vibração)
3	Aumento da pressão sobre o sistema educacional local ( demanda por vagas nas unidades escolares)
3	Interferência sobre a culinária local
3	Melhoria no sistema educacional local (investimentos, cursos e treinamentos)
3	Interferência sobre a atividade de caça
3	Interferência sobre a atividade pesqueira local
3	Incremento da arrecadação pública
3	Incremento da circulação de bens e serviços
3	Incremento da pressão sobre infraestrutura
3	Incremento da pressão sobre sistema viário
3	Aumento da poluição do ar e pneumoconioses (doenças pulmonares)
3	Aumento do número de sindicatos e ou associações de classe
3	Aumento da demanda por aparatos de segurança pública e ou privada
3	Aumento de associações de bairros ou de representantes locais
3	Surgimento de áreas para recreação social
3	Aumento dos níveis de desemprego formal na região
3	Redução dos postos de trabalho
"""

for item in source.split('\n'):
    reg = item.split('\t')
    id_meio = int(reg[0])
    obj_meio = Meio.objects.get(id=id_meio)
    registro = Impacto(conceito='--', meio_FK=obj_meio , descricao= reg[1])
    registro.save()


