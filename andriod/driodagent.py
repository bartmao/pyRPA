from common import configs, trace
import subprocess
import threading
import re
import xml.etree.ElementTree


class DriodAgent(object):
    isRunning = False
    adbPath = configs['adb']
    isDumping = False
    pListen = None

    def start(self, filter=None):
        '''
        start listening of the events, which is used to refresh layout of dump
        '''
        self.isRunning = True
        self.filter = filter
        t = threading.Thread(target=self.loop, name='listenEvents')
        t.start()

    def stop(self):
        if(self.pListen):
            self.pListen.kill()
        self.isRunning = False

    def execute(self, selector, method='click'):
        ele, pos = self.readelement(selector)
        if(ele is None):
            raise Exception('No element found: ' + selector)
        if(method == 'click'):
            self.click(pos)

    def click(self, pos):
        cmd = ['adb', 'shell', 'input', 'tap']
        cmd.extend(map(str, pos))
        subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         cwd=configs['adb'], shell=True)

    def readelement(self, selector):
        sel = DriodSelector(selector)
        r = xml.etree.ElementTree.parse('window_dump.xml').getroot()
        #ele = r.find('.//node[@class="android.widget.TextView"][@text="通讯录"]')
        xpath = './/node' + \
            ''.join(list(map(lambda k: "[@%s=\"%s\"]" %
                             (k, sel.attrs[k]), sel.attrs.keys())))
        print(xpath)
        ele = r.find(xpath)
        #ele = r.find('.//node')
        if(ele is None):
            return None, None
        b = ele.attrib['bounds']
        g = re.match('\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]', b)
        ltx = int(b[g.regs[1][0]:g.regs[1][1]])
        lty = int(b[g.regs[2][0]:g.regs[2][1]])
        rbx = int(b[g.regs[3][0]:g.regs[3][1]])
        rby = int(b[g.regs[4][0]:g.regs[4][1]])
        print(b)
        return ele, [(ltx+rbx)/2, (lty+rby)/2]

    def loop(self):
        pListen = subprocess.Popen(['adb', 'shell', 'uiautomator', 'events'],
                                   stdout=subprocess.PIPE, cwd=DriodAgent.adbPath, shell=True)

        while self.isRunning:
            trace('reading line.....')
            line = pListen.stdout.readline()
            if(line):
                # trace(line)
                if(not str(line)):
                    break
                evt = EventObj(line)
                if(not self.filter or self.filter(evt)):
                    self.dump()
            else:
                break
        trace('stop listening')

    def dump(self):
        if(not DriodAgent.isDumping):
            DriodAgent.isDumping = True
            trace('dumping layout')
            subprocess.call([self.adbPath + '\\adb', 'shell',
                             'uiautomator', 'dump'], shell=True)
            subprocess.call([self.adbPath + '\\adb', 'pull',
                             '/sdcard/window_dump.xml', '.'], shell=True)
            DriodAgent.isDumping = False


class EventObj(object):
    eventtype = None
    packagename = None
    classname = None
    text = None
    contentdescription = None

    def __init__(self, eobj):
        self.obj = eobj
        line = str(eobj)
        g = re.match(
            '.*EventType: (.+?);.*PackageName:(.+?);.*ClassName:(.+?);.*Text: \\[(.*?)\\];.*ContentDescription:(.*?).*;', str(self.obj))
        self.eventtype = line[g.regs[1][0]:g.regs[1][1]]
        self.packagename = line[g.regs[2][0]:g.regs[2][1]]
        self.classname = line[g.regs[3][0]:g.regs[3][1]]
        self.text = bytes.fromhex(
            line[g.regs[4][0]:g.regs[4][1]].replace('\\x', '')).decode('utf-8')
        self.contentdescription = line[g.regs[5][0]:g.regs[5][1]]
        print(self.eventtype, self.packagename, self.classname,
              self.text, self.contentdescription)


class DriodSelector(object):
    attrs = {}

    def __init__(self, selector):
        pairs = re.findall(r'\s(.+?)=[\'|"](.*?)[\'|"]', selector)
        for p in pairs:
            self.attrs[p[0]] = p[1]


class DriodElement(object):
    xmlnode = None
    centerpos = None
    bound = None
