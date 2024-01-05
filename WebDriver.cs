using System.IO;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Edge;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Support.UI;
using SeleniumExtras.WaitHelpers;

namespace FrontBot;

public static class WebDriver {
    const int WaitTime = 20;

    public static IWebDriver NuevaPrueba(Prueba prueba) {
        IWebDriver driver;
        string executable;
        var options = new ChromeOptions();

        switch (prueba.Explorador) {
            case WebBrowser.Chrome:
                driver = new ChromeDriver(options);
                options.AddArgument("start-maximized");
                options.AddExcludedArgument("enable-logging");

                if (prueba.Oculto)
                    options.AddArgument("--headless");

                executable = (Environment.OSVersion.Platform) switch {
                    PlatformID.Win32NT => "include/ChromeDriver.exe",
                    PlatformID.Unix => "include/ChromeDriver",
                    _ => throw new ArgumentOutOfRangeException()
                };

                break;

            case WebBrowser.Firefox:
                driver = new FirefoxDriver();
                var firefoxOptions = new FirefoxOptions();
                firefoxOptions.AddArgument("start-maximized");

                if (prueba.Oculto)
                    firefoxOptions.AddArgument("--headless");

                executable = (Environment.OSVersion.Platform) switch {
                    PlatformID.Win32NT => "include/GeckoDriver.exe",
                    PlatformID.Unix => "include/GeckoDriver",
                    _ => throw new ArgumentOutOfRangeException()
                };
                break;

            case WebBrowser.Edge:
                driver = new EdgeDriver();
                var edgeOptions = new EdgeOptions();
                edgeOptions.AddArgument("start-maximized");

                if (prueba.Oculto)
                    edgeOptions.AddArgument("--headless");


                executable = (Environment.OSVersion.Platform) switch {
                    PlatformID.Win32NT => "include/msedgedriver.exe",
                    PlatformID.Unix => "include/msedgedriver",
                    _ => throw new ArgumentOutOfRangeException()
                };

                break;

            default:
                throw new ArgumentOutOfRangeException();
        }

        return new Driver(driver, options, executable, prueba.Web);
    }

    public class Driver : ChromeDriver {
        readonly InstructionSet _instSet;
        int _contadorCapturas;

        public Driver(IWebDriver driver, ChromeOptions options, string executable, string setPath)
            : base(options) {
            _instSet = new InstructionSet(setPath);
            _contadorCapturas = 1;
        }

        public void Action(string name, params string[] args) {
            var inst = _instSet[name];
            var curArg = 0;

            for (var i = 0; i < inst.XPath.Count; i++) {
                var path = inst.XPath[i].Replace("%", args[curArg++], (StringComparison)1); // StringComparison????
                new WebDriverWait(this, TimeSpan.FromSeconds(WaitTime))
                    .Until(ExpectedConditions.ElementExists(By.XPath(path)));

                var element = FindElement(By.XPath(path));
                ((IJavaScriptExecutor)this).ExecuteScript("arguments[0].scrollIntoView(true);", element);

                switch (inst.Action[i]) {
                    case WebAction.Click:
                        new WebDriverWait(this, TimeSpan.FromSeconds(WaitTime))
                            .Until(ExpectedConditions.ElementToBeClickable(element)).Click();
                        break;

                    case WebAction.Input:
                        new WebDriverWait(this, TimeSpan.FromSeconds(WaitTime))
                            .Until(ExpectedConditions.ElementToBeClickable(element)).SendKeys(args[curArg++]);
                        break;

                    default:
                        throw new ArgumentOutOfRangeException();
                }
            }
        }

        public void LogScreenshot(string log, string? evento = null) {
            if (!Directory.Exists(log)) {
                Directory.CreateDirectory(log);
            }

            var nombreCaptura = _contadorCapturas.ToString().PadLeft(2, '0');
            var path = evento == null
                ? $"{log}/captura{nombreCaptura}{_contadorCapturas}.png"
                : $"{log}/Caso {evento}.png";

            var element = FindElement(By.ClassName("nav-tabs-body"));
            var requiredHeight = (long)ExecuteScript("return document.body.parentNode.scrollHeight");
            Manage().Window.Size = new System.Drawing.Size(1080, (int)(requiredHeight * 2));
            ((ITakesScreenshot)element).GetScreenshot().SaveAsFile(path);

            _contadorCapturas++;
        }

        public void Link(string url) {
            Thread.Sleep(2000);
            Navigate().GoToUrl(url);
        }
    }
}