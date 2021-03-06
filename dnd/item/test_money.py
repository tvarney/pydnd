
import pytest

from dnd.item import money


def test_parse_coin_spec_valid():
    """Test valid coin specs"""
    cs = money.parse_coin_spec("4pp 3gp 2sp 1cp")
    assert cs == (1, 2, 3, 4)

    cs = money.parse_coin_spec("1 pp 2 gp 3 sp 4 cp")
    assert cs == (4, 3, 2, 1)


def test_parse_coin_spec_negative():
    with pytest.raises(ValueError):
        money.parse_coin_spec("-1 cp")


def test_parse_coin_spec_bad_coin_type():
    with pytest.raises(ValueError):
        money.parse_coin_spec("1 dollar")


def test_parse_coin_spec_no_coin_type():
    with pytest.raises(ValueError):
        money.parse_coin_spec("1 cp 2")


def test_parse_coin_spec_empty():
    with pytest.raises(ValueError):
        money.parse_coin_spec("   ")


def test_money_init_dict_pp():
    m = money.Money({'pp': 10})
    assert (m.pp, m.gp, m.sp, m.cp) == (10, 0, 0, 0)


def test_money_init_dict_pp_negative():
    with pytest.raises(ValueError):
        money.Money({'pp': -1})


def test_money_init_dict_pp_bad_type():
    with pytest.raises(ValueError):
        money.Money({'pp': "h"})


def test_money_init_dict_gp():
    m = money.Money({'gp': 10})
    assert (m.pp, m.gp, m.sp, m.cp) == (0, 10, 0, 0)


def test_money_init_dict_gp_overflow():
    m = money.Money({'gp': 101})
    assert (m.pp, m.gp, m.sp, m.cp) == (1, 1, 0, 0)


def test_money_init_dict_gp_negative():
    with pytest.raises(ValueError):
        money.Money({'gp': -1})


def test_money_init_dict_gp_bad_type():
    with pytest.raises(ValueError):
        money.Money({'gp': "h"})


def test_money_init_dict_sp():
    m = money.Money({'sp': 10})
    assert (m.pp, m.gp, m.sp, m.cp) == (0, 0, 10, 0)


def test_money_init_dict_sp_overflow():
    m = money.Money({'sp': 101})
    assert (m.pp, m.gp, m.sp, m.cp) == (0, 1, 1, 0)


def test_money_init_dict_sp_negative():
    with pytest.raises(ValueError):
        money.Money({'sp': -1})


def test_money_init_dict_sp_bad_type():
    with pytest.raises(ValueError):
        money.Money({'sp': "h"})


def test_money_init_dict_cp():
    m = money.Money({'cp': 10})
    assert(m.pp, m.gp, m.sp, m.cp) == (0, 0, 0, 10)


def test_money_init_dict_cp_overflow():
    m = money.Money({'cp': 101})
    assert (m.pp, m.gp, m.sp, m.cp) == (0, 0, 1, 1)


def test_money_init_dict_cp_negative():
    with pytest.raises(ValueError):
        money.Money({'cp': -1})


def test_money_init_dict_bad_type_cp():
    with pytest.raises(ValueError):
        money.Money({'cp': "h"})


def test_money_init_dict_all():
    m = money.Money({'cp': 50, 'sp': 50, 'gp': 50, 'pp': 50})
    assert (m.pp, m.gp, m.sp, m.cp) == (50, 50, 50, 50)


def test_money_init_dict_all_overflow():
    m = money.Money({'cp': 101, 'sp': 101, 'gp': 101, 'pp': 101})
    assert (m.pp, m.gp, m.sp, m.cp) == (102, 2, 2, 1)


def test_money_init_dict_all_negative():
    with pytest.raises(ValueError):
        money.Money({'pp': -1, 'gp': -1, 'sp': -1, 'cp': -1})
    # Valid borrow
    m = money.Money({'pp': 1, 'gp': 0, 'sp': 0, 'cp': -1})
    assert (m.pp, m.gp, m.sp, m.cp) == (0, 99, 99, 99)


def test_money_init_dict_extra_keys():
    with pytest.raises(KeyError):
        money.Money({'something': "else"})


def test_money_init_numeric():
    m = money.Money(1.01)
    assert (m.pp, m.gp, m.sp, m.cp) == (0, 0, 1, 1)


def test_money_init_numeric_large():
    m = money.Money(10101.01)
    assert (m.pp, m.gp, m.sp, m.cp) == (1, 1, 1, 1)


def test_money_init_numeric_negative():
    with pytest.raises(ValueError):
        money.Money(-10000)
    with pytest.raises(ValueError):
        money.Money(-100)
    with pytest.raises(ValueError):
        money.Money(-1)
    with pytest.raises(ValueError):
        money.Money(-0.01)
    with pytest.raises(ValueError):
        money.Money(-0.001)
