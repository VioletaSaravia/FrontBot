import src.data as test


def test_instruction_set_load():
    ml = test.load_instruction_set('instructions/mercadolibre.json')
    assert (ml["barra_superior"].xpath[0] == "/html/body/header/div/div[5]/div/ul/li[2]/a[contains(text(), %)]")
    assert (ml["busqueda"].action[0] == test.Action.input)
    assert (ml["busqueda"].action[1] == test.Action.click)
