using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UiPath;

namespace RPA.UIPathAdapter
{
    public static class Global
    {
        private static int isInitialized = 0;

        public static void Init() {
            if (Interlocked.CompareExchange(ref isInitialized, 1, 0) == 0) {
                var sysPath = ConfigurationManager.AppSettings["UIPathActFolder"];
                if (string.IsNullOrEmpty(sysPath) || !Directory.Exists(sysPath))
                    throw new Exception("Provide the correct UIPath folder path first");
                //var sysPath = "C:\\Users\\bmao002\\.nuget\\packages\\uipath\\9.0.6877.24355\\build\\UiPath";
                Environment.SetEnvironmentVariable("UIPATH_RUNTIME", sysPath);
                var factory = UiFactory.Instance;
                Console.WriteLine(factory.NativeLibrariesFolder);
                var tp = Assembly.GetAssembly(typeof(ActivationScope)).GetType("UiPath.ActivationContext").GetField("hActCtx", BindingFlags.Static | BindingFlags.GetField | BindingFlags.NonPublic).GetValue(null);
                Console.WriteLine("The activation code is: " + tp);
            }
        }
    }
}
