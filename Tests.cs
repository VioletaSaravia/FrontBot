using NUnit.Framework;
namespace FrontBot;

[TestFixture]
public class Tests {
    [Test]
    public void TestInstructionSetLoad() {
        var ml = new InstructionSet("instructions/mercadolibre.json");
        Assert.That("/html/body/header/div/div[5]/div/ul/li[2]/a[contains(text(), %)]",
            Is.EqualTo(ml["barra_superior"].XPath[0]));
        Assert.That(WebAction.Input, Is.EqualTo(ml["busqueda"].Action[0]));
        Assert.That(WebAction.Click, Is.EqualTo(ml["busqueda"].Action[1]));
    }

    [Test]
    public void TestParamCount() {
        var ml = new InstructionSet("instructions/mercadolibre.json");
        Assert.That(1, Is.EqualTo(ml["barra_superior"].ParamCount));
        Assert.That(1, Is.EqualTo(ml["busqueda"].ParamCount));
    }
}
