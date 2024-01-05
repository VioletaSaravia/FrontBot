using System.Diagnostics;
using System.IO;
using Newtonsoft.Json;

namespace FrontBot;

public enum WebBrowser {
    Chrome,
    Firefox,
    Edge
}

public enum WebAction {
    Click,
    Input
}

public class Instruction {
    public List<string> XPath { get; set; }
    public List<WebAction> Action { get; set; }
    public int ParamCount { get; set; }

    public Instruction(List<string> xPath, List<WebAction> action) {
        XPath = xPath;
        Action = action;

        foreach (var i in xPath) {
            ParamCount += i.Split('%').Length - 1;
        }

        ParamCount += action.Count(x => x == WebAction.Input);
    }
}

public class InstructionSet {
    readonly Dictionary<string, Instruction> _data;

    public InstructionSet(string path) {
        var jsonString = File.ReadAllText(path);
        var jsonData = JsonConvert.DeserializeObject<Dictionary<string, List<List<string>>>>(jsonString);
        Debug.Assert(jsonData != null, nameof(jsonData) + " != null");

        var result = new Dictionary<string, Instruction>();

        foreach (var (name, values) in jsonData) {
            var xpaths = new List<string>();
            var actions = new List<WebAction>();

            foreach (var pair in values) {
                xpaths.Add(pair[0]);

                switch (pair[1]) {
                    case "click":
                        actions.Add(WebAction.Click);
                        break;
                    case "input":
                        actions.Add(WebAction.Input);
                        break;
                    default:
                        throw new ArgumentException($"action doesn't exist: {pair[1]}");
                }
            }

            result[name] = new Instruction(xpaths, actions);
        }

        _data = result;
    }

    public Instruction this[string name] => _data[name];
}

public class Prueba(bool oculto, WebBrowser explorador, string web) {
    public bool Oculto = oculto;
    public WebBrowser Explorador = explorador;
    public string Web = web;
}

