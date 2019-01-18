from common import configs, trace
from rpa import UIElement, ExecutionResult
import subprocess
import threading
import re
import xml.etree.ElementTree
import os.path

class DroidAdapter(object):
    isRunning = False
    adbPath = configs['adb']
    isDumping = False
    pListen = None
    __locker = threading.Lock()

    def start(self, filter=None):
        '''
        start listening of the events, which is used to refresh layout of dump
        '''
        self.isRunning = True
        self.filter = filter
        #t = threading.Thread(target=self.loop, name='listenEvents')
        #t.start()

    def stop(self):
        if(self.pListen):
            self.pListen.kill()
        self.isRunning = False

    def execute(self, obj):
        selector = obj['selector']
        method = obj['method']
        args = obj['args']
        ele = None
        if(selector):
            ele = self.readelement(selector)
            if(ele is None):
                raise Exception('No element found: ' + selector)
        r = ExecutionResult()
        if(method == 'click'):
            self.click(ele.centerpos)
        elif(method == 'typetext'):
            self.typetext(args['text'])
        elif(method == 'gettext'):
            r.value = self.gettext(ele)
        elif(method == 'start'):
            self.startapp(args)
        return r

    def startapp(self, args):
        app = args['app']
        if(app == 'contacts'):
            subprocess.call('adb shell am start -a android.intent.action.VIEW content://contacts/people', stdout=subprocess.PIPE,
                        cwd=configs['adb'], shell=True)
            

    def click(self, pos):
        trace('performing click @[%s, %s]' % (pos[0], pos[1]))
        cmd = ['adb', 'shell', 'input', 'tap']
        cmd.extend(map(str, pos))
        subprocess.call(cmd, stdout=subprocess.PIPE,
                        cwd=configs['adb'], shell=True)

    def gettext(self, ele):
        trace('performing gettext')
        return ele.xmlnode.attrib['text']

    def typetext(self, txt):
        # Not support Unicode currently
        trace('performing typing')
        txt = txt.replace(' ', '%s')
        cmd = ['adb', 'shell', 'input', 'text']
        cmd.append(txt)
        subprocess.call(cmd, stdout=subprocess.PIPE,
                        cwd=configs['adb'], shell=True)

    def readelement(self, selector):
        #if(not os.path.isfile('window_dump.xml')):
        if(selector):
            self.dump()

        sel = DriodSelector(selector)
        r = xml.etree.ElementTree.parse('window_dump.xml').getroot()
        xpath = './/node' + \
            ''.join(list(map(lambda k: "[@%s=\"%s\"]" %
                             (k, sel.attrs[k]), sel.attrs.keys())))
        print(xpath)
        node = r.find(xpath)
        if(node is None):
            return None
        ele = NativeDroidElement(node)
        return ele

    def loop(self):
        trace('start listening...')
        pListen = subprocess.Popen(['adb', 'shell', 'uiautomator', 'events'],
                                   stdout=subprocess.PIPE, cwd=DroidAdapter.adbPath, shell=True)

        while self.isRunning:
            trace('waiting for new events...')
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
        if(not DroidAdapter.isDumping):
            DroidAdapter.isDumping = True
            DroidAdapter.__locker.acquire()
            try:
                trace('dumping layout')
                p = subprocess.Popen([self.adbPath + '\\adb', 'shell',
                                'uiautomator', 'dump'], shell=True)
                p.wait()
                p = subprocess.Popen([self.adbPath + '\\adb', 'pull',
                                '/sdcard/window_dump.xml', '.'], shell=True, cwd='.')
                p.wait()
            finally:
                DroidAdapter.__locker.release()
                DroidAdapter.isDumping = False


class EventObj(object):
    eventtype = None
    packagename = None
    classname = None
    text = None
    contentdescription = None

    def __init__(self, eobj):
        self.obj = eobj
        line = str(eobj)
        trace(line)
        g = re.match(
            '.*EventType: (.+?);.*PackageName:(.+?);.*ClassName:(.+?);.*Text: \\[(.*?)\\];.*ContentDescription:(.*?).*;', str(self.obj))
        self.eventtype = line[g.regs[1][0]:g.regs[1][1]]
        self.packagename = line[g.regs[2][0]:g.regs[2][1]]
        self.classname = line[g.regs[3][0]:g.regs[3][1]]
        self.text = line[g.regs[4][0]:g.regs[4][1]]
        if(self.text.startswith('[\\x')):
            self.text = self.text.replace('\\x', '')
            self.text = bytes.fromhex(self.text).decode('utf-8')
        self.contentdescription = line[g.regs[5][0]:g.regs[5][1]]
        print(self.eventtype, self.packagename, self.classname,
              self.text, self.contentdescription)


class DriodSelector(object):
    attrs = {}

    def __init__(self, selector):
        pairs = re.findall(r'\s(.+?)=[\'|"](.*?)[\'|"]', selector)
        for p in pairs:
            self.attrs[p[0]] = p[1]


class NativeDroidElement(object):
    xmlnode = None
    centerpos = [0, 0]

    def __init__(self, node):
        self.xmlnode = node
        b = node.attrib['bounds']
        g = re.match('\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]', b)
        ltx = int(b[g.regs[1][0]:g.regs[1][1]])
        lty = int(b[g.regs[2][0]:g.regs[2][1]])
        rbx = int(b[g.regs[3][0]:g.regs[3][1]])
        rby = int(b[g.regs[4][0]:g.regs[4][1]])
        self.centerpos = [(ltx+rbx)/2, (lty+rby)/2]


class DroidElement(UIElement):
    __adapter = None

    @staticmethod
    def setAgent(adapter):
        DroidElement.__adapter = adapter

    def execute(self, obj):
        return self.__adapter.execute(obj)

    def start(self, app):
        return locals()