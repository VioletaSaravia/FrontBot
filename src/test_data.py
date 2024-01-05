import src.data as test


def test_instruction_set_load():
    ml = test.init_instruction_set('instructions/mercadolibre.json')
    assert (ml["barra_superior"].xpath[0] == "/html/body/header/div/div[5]/div/ul/li[2]/a[contains(text(), %)]")
    assert (ml["busqueda"].action[0] == test.WebAction.input)
    assert (ml["busqueda"].action[1] == test.WebAction.click)


def test_param_count():
    ml = test.init_instruction_set('instructions/mercadolibre.json')
    assert (ml["barra_superior"].param_count == 1)
    assert (ml["busqueda"].param_count == 1)
