using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RPA.UIPathAdapter
{
    public class RPARemoteObj
    {
        public string selector { get; set; }

        public string method { get; set; }

        public Dictionary<string, object> args { get; set; }

        public Dictionary<string, object> attrs { get; set; }
    }
}
