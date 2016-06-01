from impacto.models import Quadro, QuadroItem
import xlrd


class GetTableFromExcel(object):
    def __init__(self, url):
        self.tabela = []
        workbook = xlrd.open_workbook(url)
        quadros = workbook.sheet_by_index(0)
        quadros_item = workbook.sheet_by_index(1)

        for quadro_lin in range(quadros.nrows):
            quadro_id = quadros.cell(quadro_lin, 0).value
            quadro_desc = quadros.cell(quadro_lin, 1).value
            quadro_FK = Quadro(ordem=quadro_id, descricao=quadro_desc)
            quadro_FK.save()

            for quadro_id_lin in range(quadros_item.nrows):
                quadro_item_id = quadros_item.cell(quadro_id_lin, 0).value
                if quadro_item_id == quadro_id:
                    quadro_item_desc = quadros_item.cell(quadro_id_lin, 2).value

                    if quadros_item.cell_type(quadro_id_lin, 1) == xlrd.XL_CELL_EMPTY:
                        quadro_item_classe = ''
                    else:
                        quadro_item_classe = quadros_item.cell(quadro_id_lin, 1).value

                    if quadros_item.cell_type(quadro_id_lin, 3) == xlrd.XL_CELL_EMPTY:
                        quadro_item_desc1 = ''
                    else:
                        quadro_item_desc1 = quadros_item.cell(quadro_id_lin, 3).value

                    if quadros_item.cell_type(quadro_id_lin, 4) == xlrd.XL_CELL_EMPTY:
                        quadro_item_escala = ''
                    else:
                        quadro_item_escala = quadros_item.cell(quadro_id_lin, 4).value

                    quadro_item_FK = QuadroItem(quadro_FK=quadro_FK,
                                                classe= quadro_item_classe,
                                                descricao=quadro_item_desc,
                                                descricao1=quadro_item_desc1,
                                                escala=quadro_item_escala)
                    quadro_item_FK.save()

def run():
    GetTableFromExcel("planilha.xlsx")

