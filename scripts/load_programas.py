

from impacto.models import  Programa



def run():
    col = [	[1,	"Programa de Controle e Monitoramento de Processos Erosivos;"],
        [2,	"Programa de Recuperação de Áreas Degradadas – PRAD;"],
        [3,	"Subprograma de Recuperação e Manejo de Áreas de Preservação; Permanente (APP); "],
        [4,	"Programa de Gestão de Recursos Hídricos (Subprograma de Gestão dos efluentes Líquidos Subprograma de Monitoramento da Qualidade das águas Superficiais e Subterrâneas) ; " ],
        [5,	"Programa de Gerenciamento de Resíduos Sólidos e de Combustíveis Óleos e Graxas (PGRS);"],
        [6,	"Programa de Gestão Ambiental do Empreendimento;" ],
        [7,	"Plano de Gerenciamento de Risco e Plano de Atendimento a Emergência Ambiental " ],
        [8,	"Programa de Gestão e Monitoramento da Qualidade do Ar; " ],
        [9,	"Programa de Gestão e Monitoramento dos Níveis de Ruído " ],
        [10,"Programa de Manutenção de Máquinas, Equipamentos e Veículos; " ],
        [11,"Plano de Fechamento de Mina; " ],
        [12,"Vistoria Permanente das áreas de Intervenção; " ],
        [13,"Fiscalização/Vigilância; " ],
        [14,"Programa de Monitoramento de Fauna - Avifauna, Herpetofauna, Ictiofauna, Mastofauna, Quiropterofauna, Limnologia;" ],
        [15,"Programa Monitoramento de Limnologia; " ],
        [16,"Programa de Compensação Ambiental; " ],
        [17,"Passagens direcionadas para a Fauna em acessos com manchas de Habitat;" ],
        [18,"Programa de Educação Ambiental; " ],
        [19,"Programa Operacional para Supressão (POS); " ],
        [20,"Programa de Afugentamento e Resgate de Fauna; " ],
        [21,"Programa de Enriquecimento de Entorno; " ],
        [22,"Programa de Resgate e Monitoramento de Flora; " ],
        [23,"Programa de Resgate de Ictiofauna; " ],
        [24,"Projeto Técnico para Reconstituição da Flora (PTRF); " ],
        [25,"Programa de Comunicação Social;" ],
        [26,"Programa de Capacitação para o Desenvolvimento Sustentável;" ],
        [27,"Programa de Monitoramento de Indicadores Socioeconômicos;" ],
        [28,"Programa de Desenvolvimento Econômico Regional Integrado;" ],
        [29,"Programa de Capacitação de Fornecedores Locais;" ],
        [30,"Programa de Negociação e Assistência Fundiária;" ],
        [31,"Programa de Minimização da Pressão sobre a Infraestrutura e Serviços Públicos;" ],
        [32,"Programa de Saúde Ambiental;" ],
        [33,"Programa de Trafegabilidade e Sinalização Viária; " ],
        [34,"Programa de Incentivo às Vocações Locais;" ],
        [35,"Programa de Apoio à Gestão Territorial;" ],
        [36,"Programa de Prospecção e Resgate Arqueológico e Sub-programa de Educação Patrimonial." ],
    ]


	

    for item in col:
        reg = Programa(descricao=item[1])
        reg.save()