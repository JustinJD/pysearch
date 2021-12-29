import os
import re
import psutil
import datetime
import time
import argparse


class pySearch:
    def __init__(self, path: str, key_word: str, key_type: str = 'End', mode: str = 'multilayer', log: bool = True,
                 wildcard: bool = True):
        """
        Global Variables
        """
        self.path = path
        self.key_word = key_word
        self.key_type = key_type
        self.mode = mode
        self.log = log
        self.wildcard = wildcard
        self.count = 0
        self.disk_info = self._get_disk_info()
        self.results = []

    def execute(self):
        mode = self.mode
        start_time = time.time()
        if mode == 'monolayer' and self.log:
            self._search_current_layer(self.path)
            self._create_log()
        elif mode == 'multilayer' and self.log:
            self._drill_down()
            self._create_log()
        elif mode == 'monolayer':
            self._search_current_layer(self.path)
        elif mode == 'multilayer':
            self._drill_down()
        end_time = time.time()
        print('(%.2f seconds)' % (end_time - start_time))

    @staticmethod
    def _get_disk_info():
        disk_info = psutil.disk_partitions()
        disk_part = []
        for x in disk_info:
            x = x[1].replace('\\', '/')
            disk_part.append(x)
        return disk_part

    def _create_log(self):
        name = datetime.datetime.now()
        name = str(name)[0:-7]
        name = name.replace('-', '')
        name = name.replace(' ', '')
        name = name.replace(':', '')
        name = 'log' + name + '.txt'
        if self.log is True:
            with open('./%s' % name, 'w') as f:
                for x in self.results:
                    f.write(x + '\n')

    def _search_current_layer(self, path=None):
        path = path.rstrip('/') + '/'
        dir_list = os.listdir(path)
        data = []
        for x in dir_list:
            name_split = os.path.splitext(x)
            value = os.path.isdir(path + x)
            if self.key_type == 'Head':
                key_word = name_split[0]
            elif self.key_type == 'End':
                key_word = name_split[1]
            elif self.key_type == 'Full':
                key_word = x
            else:
                key_word = x
            if self.wildcard is False:
                if key_word == self.key_word:
                    self.count += 1
                    print(path + x)
                    self.results.append(path + x)
                elif value:
                    data.append(path + x)
                else:
                    pass
            elif self.wildcard is True:
                ###
                keys = self.key_word.split('%')
                if len(keys) == 1:
                    raise Exception('Looks like you have turned on the wildcard(%) option but you have not used any wildcard in your keyword')
                keys2 = []
                for y in keys:
                    if y != '':
                        pattern = re.compile(r'\W')
                        result = pattern.finditer(y)
                        z = list(y)
                        for i in result:
                            z[i.span()[0]] = r'\%s' % i.group()
                        y = ''.join(z)
                        keys2.append(y)
                    else:
                        keys2.append(y)
                # 上面的部分用来处理关键字中的特殊字符
                keys = keys2
                extract = key_word
                count = 0
                if value:
                    data.append(path + x)
                else:
                    if len(keys) == 1:
                        if key_word == self.key_word:
                            self.count += 1
                            print(path + x)
                            self.results.append(path + x)
                        elif value:
                            data.append(path + x)
                        else:
                            pass
                    elif keys[0] == '' and keys[count - 1] == '':
                        keys.pop(0)
                        keys.pop()
                        count = len(keys)
                        result = []
                        for y in range(count):
                            if y == 0 or y == count - 1:
                                pattern = re.compile(r'\B%s' % keys[y])
                                result = pattern.findall(extract)
                            else:
                                pattern = re.compile(r'%s' % keys[y])
                                result = pattern.findall(extract)
                            if result:
                                extract = key_word.split(keys[y])
                                extract = key_word.replace(extract[0] + keys[y], '')
                            else:
                                result = []
                                break
                        if result:
                            self.count += 1
                            print(path + x)
                            self.results.append(path + x)
                    elif keys[0] == '' and keys[count - 1] != '':
                        keys.pop(0)
                        count = len(keys)
                        result = []
                        for y in range(count):
                            if count == 1:
                                pattern = re.compile(r'%s$' % keys[y])
                                result = pattern.findall(extract)
                            elif y == 0:
                                pattern = re.compile(r'\B%s' % keys[y])
                                result = pattern.findall(extract)
                            elif y == count - 1:
                                pattern = re.compile(r'%s$' % keys[y])
                                result = pattern.findall(extract)
                            else:
                                pattern = re.compile(r'%s' % keys[y])
                                result = pattern.findall(extract)
                            if result:
                                extract = key_word.split(keys[y])
                                extract = key_word.replace(extract[0] + keys[y], '')
                            else:
                                result = []
                                break
                        if result:
                            self.count += 1
                            print(path + x)
                            self.results.append(path + x)
                    elif keys[0] != '' and keys[count - 1] == '':
                        keys.pop()
                        count = len(keys)
                        result = []
                        for y in range(count):
                            if count == 1:
                                pattern = re.compile(r'^%s' % keys[y])
                                result = pattern.findall(extract)
                            elif y == 0:
                                pattern = re.compile(r'^%s' % keys[y])
                                result = pattern.findall(extract)
                            elif y == count - 1:
                                pattern = re.compile(r'\B%s' % keys[y])
                                result = pattern.findall(extract)
                            else:
                                pattern = re.compile(r'%s' % keys[y])
                                result = pattern.findall(extract)
                            if result:
                                extract = key_word.split(keys[y])
                                extract = key_word.replace(extract[0] + keys[y], '')
                            else:
                                result = []
                                break
                        if result:
                            self.count += 1
                            print(path + x)
                            self.results.append(path + x)
                    elif keys[0] != '' and keys[count - 1] != '':
                        count = len(keys)
                        result = []
                        for y in range(count):
                            if y == 0:
                                pattern = re.compile(r'^%s' % keys[y])
                                result = pattern.findall(extract)
                            elif y == count - 1:
                                pattern = re.compile(r'%s$' % keys[y])
                                result = pattern.findall(extract)
                            else:
                                pattern = re.compile(r'%s' % keys[y])
                                result = pattern.findall(extract)
                            if result:
                                extract = key_word.split(keys[y])
                                extract = key_word.replace(extract[0] + keys[y], '')
                            else:
                                result = []
                                break
                        if result:
                            self.count += 1
                            print(path + x)
                            self.results.append(path + x)
        if self.mode == 'monolayer':
            print('Fount %d results!!!' % self.count)
        return data

    def _drill_down(self, data=None):
        if data is None:
            if self.path == '.*':
                data = self.disk_info
            else:
                data = [self.path]
        data2 = None
        for x in data:
            try:
                data2 = self._search_current_layer(x)
                if len(data2) != 0:
                    data3 = data2
                    data2 = self._drill_down(data3)
            except PermissionError:
                """
                print('"%s" is not a machine-readable path' % x)
                """
        if data == [self.path] or data == self.disk_info:  # 此步骤用来判断递归函数是否回到最顶层的函数体
            print('Fount %d results!!!' % self.count)
        return data2


parser = argparse.ArgumentParser(prog='pysearch',
                                 description='This is a tool written by Python to'
                                             ' help you search files on your device.',
                                 usage='pysearch [options] [path] [keyword]')
parser.add_argument('path', help='the path where the search process starts', type=str)
parser.add_argument('key_word', help='the keyword used to match results', type=str)
parser.add_argument('-p', '--part', default='Full', type=str, choices=['Head', 'End', 'Full'], help='Portion of the file name, which determines with which part of the file name to match. Its default value is "Full"')
parser.add_argument('-m', '--mode', default='multilayer', type=str, choices=['monolayer', 'multilayer'], help='Search mode, which determines the depth of the search. Its default value is "multilayer"')
parser.add_argument('-l', '--log', action='store_true', help='Return a log of the results')
parser.add_argument('-w', '--wildcard', action='store_true', help='Use wildcard to help you match the results')
args = parser.parse_args()
Search = pySearch(path=args.path, key_word=args.key_word, key_type=args.part, mode=args.mode, log=args.log,
                  wildcard=args.wildcard)
Search.execute()
