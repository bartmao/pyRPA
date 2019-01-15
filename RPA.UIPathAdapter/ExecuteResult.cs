using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RPA.UIPathAdapter
{
    public class ExecuteResult
    {
        public string message;
        public int stat;
        public object value;

        public ExecuteResult(int stat, string msg = null, object value = null)
        {
            this.stat= stat;
            message = msg;
            this.value = value;
        }
    }
}
