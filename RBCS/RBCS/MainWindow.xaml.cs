using System;
using System.Diagnostics;
using System.IO;
using System.Windows;

namespace BarcodeApp
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void StartScanner_Click(object sender, RoutedEventArgs e)
        {
            string pythonScriptPath = @"C:\Users\Senior\source\repos\RBCS\RBCS\RPBR\Restroom-Pass-Barcode-Reader\RPBCR.py"; // Adjust this to your Python script path // you can find this by opening cmd and typing "where python" and copy the path.
            string pythonExePath = @"C:\Users\Senior\AppData\Local\Microsoft\WindowsApps\python.exe"; // Adjust this to your Python executable path

            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = pythonExePath,
                Arguments = pythonScriptPath,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            Process process = new Process
            {
                StartInfo = startInfo
            };

            process.OutputDataReceived += (s, ea) =>
            {
                if (!string.IsNullOrEmpty(ea.Data))
                {
                    Dispatcher.Invoke(() =>
                    {
                        OutputList.Items.Add(ea.Data);
                    });
                }
            };

            process.ErrorDataReceived += (s, ea) =>
            {
                if (!string.IsNullOrEmpty(ea.Data))
                {
                    Dispatcher.Invoke(() =>
                    {
                        OutputList.Items.Add($"Error: {ea.Data}");
                    });
                }
            };

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
        }
    }
}
