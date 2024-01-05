using System.IO;
using System.Windows;

namespace FrontBot;

struct FileSystemObject(string name, List<string> children) {
    public string Name { get; } = name;
    public List<string> Children { get; set; } = children;
}

public partial class MainWindow : Window {
    public MainWindow() {
        InitializeComponent();
        LoadData();
    }

    void LoadData() {
        var rootDirectory = new DirectoryInfo("Tests");
        foreach (var directory in rootDirectory.GetDirectories()) {
            List<string> files = [];

            foreach (var file in directory.GetFiles("*.csv")) {
                files.Add(Path.GetFileNameWithoutExtension(file.Name));
            }

            PruebasTreeView.Items.Add(new FileSystemObject(directory.Name, files));
        }

        rootDirectory = new DirectoryInfo("InstructionSets");
        foreach (var directory in rootDirectory.GetDirectories()) {
            List<string> files = [];

            foreach (var file in directory.GetFiles("*.json")) {
                files.Add(Path.GetFileNameWithoutExtension(file.Name));
            }

            InstructionSetsTreeView.Items.Add(new FileSystemObject(directory.Name, files));
        }

        var webBrowsers = Enum.GetNames(typeof(WebBrowser));
        ExploradorComboBox.ItemsSource = webBrowsers;
    }

    void EjecutarButtonClick(object sender, RoutedEventArgs e) {
        string explorador = ExploradorComboBox.SelectedItem?.ToString() ?? string.Empty;
        int repeticiones = int.Parse(RepeticionesInput.Text);
        int frecuencia = int.Parse(FrecuenciaInput.Text);
        int paralelo = int.Parse(ProcesosInput.Text);

        // Etc.
    }
}