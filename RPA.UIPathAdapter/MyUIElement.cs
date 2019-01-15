using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UiPath.Core;
using UiPath.Core.Activities;

namespace RPA.UIPathAdapter
{
    public class MyUIElement
    {
        private UiElement node;
        private RPARemoteObj context;

        public MyUIElement(RPARemoteObj context)
        {
            this.context = context;
            node = new UiElement(SelectorStrategy.DEFAULT);
            node.Timeout = 3000;
            node.WaitForReadyLevel = WaitForReady.INTERACTIVE;
            var selector = context.selector;
            if (!string.IsNullOrEmpty(selector))
            {
                Selector filter = new Selector(selector);
                FindScope scope = filter.IsTopLevel() ? FindScope.FIND_TOP_LEVELS : FindScope.FIND_DESCENDANTS;
                node = node.FindFirst(scope, filter);
            }
        }

        public ExecuteResult Execute()
        {
            ModifyAttributes();
            var method = context.method;
            var m = GetType().GetMethods().FirstOrDefault(mm => mm.Name.ToLower() == method);
            if (m != null)
                return (ExecuteResult)m.Invoke(this, new object[] { });
            else
                return new ExecuteResult(1, "Not supported method");
        }

        public void ModifyAttributes()
        {
            var props = node.GetType().GetProperties();
            foreach (var attr in context.attrs)
            {
                var p = props.FirstOrDefault(pp => pp.Name.ToLower() == attr.Key);
                if (p != null)
                {
                    try
                    {
                        if (attr.Value is long || attr.Value is Enum)
                            p.SetValue(node, (int)(long)attr.Value);
                        else
                            p.SetValue(node, attr.Value);
                    }
                    catch (Exception)
                    {
                        Console.WriteLine("Failed to set value for attribute {0}", attr.Key);
                    }
                }
                else
                {
                    Console.WriteLine("Attribute {0} not found", attr.Key);
                }
            }
        }

        public ExecuteResult Click()
        {
            var args = context.args;
            var type = (ClickType)(long)args["type"];
            var button = (MouseButton)(long)args["button"];
            var method = (InputMethod)(long)args["method"];
            if (button == MouseButton.BTN_RIGHT && method == InputMethod.API)
                method = InputMethod.WINDOW_MESSAGES;
            node.Click((ClickType)type, (MouseButton)button, (InputMethod)method);
            return new ExecuteResult(0);
        }

        public ExecuteResult Highlight()
        {
            var args = context.args;
            var seconds = (int)(long)args["seconds"];
            var colorName = args["color"];
            var color = Color.Red;
            var pColor = typeof(Color).GetProperties().FirstOrDefault(c => c.Name.ToLower() == colorName.ToString());
            if (pColor != null)
                color = Color.FromName(pColor.Name);
            node.Highlight(new TimeSpan(0, 0, seconds), color);
            return new ExecuteResult(0);
        }

        public ExecuteResult TypeText()
        {
            var args = context.args;
            var text = args["text"].ToString();
            var method = (InputMethod)(long)args["method"];
            node.WriteText(text, method);
            return new ExecuteResult(0);
        }

        public ExecuteResult SendHotkey()
        {
            var args = context.args;
            var key = (KeyModifiers)(long)args["modifiers"];
            var text = args["key"].ToString();
            var isSpecial = args["isSpecial"].ToString() != "0";
            var outText = ComposeText(key, text, isSpecial);
            Console.WriteLine("Output Command: " + outText);
            node.WriteText(outText, InputMethod.WINDOW_MESSAGES);
            return new ExecuteResult(0);
        }

        public ExecuteResult GetText()
        {
            var val = node.Get("Text");
            return new ExecuteResult(0, value: val);
        }

        private string ComposeText(KeyModifiers keyModifiers, string keyVariable, bool isSpecial)
        {
            string text = "";
            string text2 = "";
            keyModifiers.ComposeAsText(out text, out text2);
            string text3 = keyVariable;
            if (isSpecial)
            {
                text3 = "[k(" + text3 + ")]";
            }
            if (!string.IsNullOrWhiteSpace(text))
            {
                text3 = string.Concat(new string[]
                {
                    "[",
                    text,
                    "]",
                    text3,
                    "[",
                    text2,
                    "]"
                });
            }
            return text3;
        }

        private void ComposeAsText(KeyModifiers keyModifiers, out string beginText, out string endText)
        {
            string empty;
            beginText = (empty = string.Empty);
            endText = empty;
            if (keyModifiers.HasFlag(KeyModifiers.Alt))
            {
                beginText += "d(alt)";
                endText = "u(alt)" + endText;
            }
            if (keyModifiers.HasFlag(KeyModifiers.Ctrl))
            {
                beginText += "d(ctrl)";
                endText = "u(ctrl)" + endText;
            }
            if (keyModifiers.HasFlag(KeyModifiers.Shift))
            {
                beginText += "d(shift)";
                endText = "u(shift)" + endText;
            }
            if (keyModifiers.HasFlag(KeyModifiers.Win))
            {
                beginText += "d(lwin)";
                endText = "u(lwin)" + endText;
            }
        }
    }
}
