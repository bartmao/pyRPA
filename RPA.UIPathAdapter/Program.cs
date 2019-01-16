using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using UiPath.Core;

namespace RPA.UIPathAdapter
{
    class Program
    {
        static void Main(string[] args)
        {
            var srv = new RPCServer();
            try
            {
                srv.Start();
            }
            finally
            {
                srv.Stop();
            }
        }
    }

    class RPCServer
    {
        private HttpListener listener;
        public void Start()
        {
            Global.Init();

            listener = new HttpListener();
            listener.Prefixes.Add("http://localhost/RPA.UIPath/");
            listener.Start();
            Console.WriteLine("Start listening...");

            while (true)
            {
                Console.WriteLine("Receving Request...");
                var ctx = listener.GetContext();
                Console.WriteLine("Received Request...");

                ExecuteResult result;
                using (var reader = new StreamReader(ctx.Request.InputStream))
                {
                    var req = reader.ReadToEnd();
                    Console.WriteLine(req);
                    var executeContext = JsonHelper.DeserializeJsonToObject<RPARemoteObj>(req);
                    if (executeContext != null)
                    {
                        try
                        {
                            var e = new MyUIElement(executeContext);
                            result = e.Execute();
                        }
                        catch (SelectorNotFoundException ex)
                        {
                            result = new ExecuteResult(0x1, "Element Not Found");
                        }
                        catch (Exception ex)
                        {
                            result = new ExecuteResult(0x2, "Failed Execution: " + ex.Message);
                        }
                    }
                    else
                    {
                        result = new ExecuteResult(-1, "Invalid Remote Object");
                    }
                }

                using (var writer = new StreamWriter(ctx.Response.OutputStream))
                {
                    writer.Write(JsonHelper.SerializeObject(result));
                    writer.Flush();
                }
            }
        }

        public void Stop()
        {
            if (listener.IsListening)
                listener.Stop();
        }
    }


}
