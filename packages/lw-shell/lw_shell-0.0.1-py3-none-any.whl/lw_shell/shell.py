import subprocess

'''
统一处理shell交互命令
'''


def shell(cmd):
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = str(ret.stderr.read(), encoding='utf-8')
    out = str(ret.stdout.read(), encoding='utf-8')
    return ShellResult(len(err) == 0, out, err)


class ShellResult:
    isSuccess = False
    content = ""
    errorMsg = ""

    def __init__(self, isSuccess=False, content="", errorMsg=""):
        self.isSuccess = isSuccess
        self.content = content
        self.errorMsg = errorMsg
