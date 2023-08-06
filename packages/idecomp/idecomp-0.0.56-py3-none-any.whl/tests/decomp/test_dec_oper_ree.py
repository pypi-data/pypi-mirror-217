from idecomp.decomp.dec_oper_ree import DecOperRee

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.dec_oper_ree import MockDecOperRee


def test_atributos_encontrados_dec_oper_ree():
    m: MagicMock = mock_open(read_data="".join(MockDecOperRee))
    with patch("builtins.open", m):
        rel = DecOperRee.read("./tests/mocks/arquivos/dec_oper_ree.py")
        assert rel.versao == "31.14"
        assert rel.tabela.at[0, "periodo"] == 1
        assert rel.tabela.at[0, "no"] == 1
        assert rel.tabela.at[0, "cenario"] == 1
        assert rel.tabela.at[0, "indice_ree"] == 1
        assert rel.tabela.at[0, "nome_ree"] == "SUDESTE"
        assert rel.tabela.at[0, "indice_submercado"] == 1
        assert rel.tabela.at[0, "ena_MWmes"] == 1667.5
        assert rel.tabela.at[0, "earm_inicial_MWmes"] == 10387.50
        assert rel.tabela.at[0, "earm_inicial_percentual"] == 20.65
        assert rel.tabela.at[0, "earm_final_MWmes"] == 10956.67
        assert rel.tabela.at[0, "earm_final_percentual"] == 21.78
        assert rel.tabela.at[0, "earm_maximo_MWmes"] == 50314.5


def test_eq_dec_oper_ree():
    m: MagicMock = mock_open(read_data="".join(MockDecOperRee))
    with patch("builtins.open", m):
        rel1 = DecOperRee.read("./tests/mocks/arquivos/dec_oper_ree.py")
        rel2 = DecOperRee.read("./tests/mocks/arquivos/dec_oper_ree.py")
        assert rel1 == rel2


def test_neq_dec_oper_ree():
    m: MagicMock = mock_open(read_data="".join(MockDecOperRee))
    with patch("builtins.open", m):
        rel1 = DecOperRee.read("./tests/mocks/arquivos/dec_oper_ree.py")
        rel2 = DecOperRee.read("./tests/mocks/arquivos/dec_oper_ree.py")
        rel1.tabela.iloc[0, 0] = -1
        assert rel1 != rel2
