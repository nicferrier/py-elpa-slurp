import sexpdata
import httplib
import sys
import os

class ExtensionError(Exception):
    pass

def version_string(version):
    return ".".join([str(item) for item in version])

def type_to_extension(type):
    if type == "single":
        return ".el"
    elif type == "tar":
        return ".tar"
    else:
        raise ExtensionError(type)

def download_archive():
    h = httplib.HTTPConnection("elpa.gnu.org")
    h.request("GET", "/packages/archive-contents")
    response = h.getresponse()
    if response.status == 200:
        body = response.read()

        try:
            os.makedirs("downloads")
        except:
            pass
        with open("downloads/archive-contents", "w") as fd:
            fd.write(body)
            
        packages = sexpdata.loads(body)[2:]
        for [package_name, _, struct] in packages:
            try:
                [version, depends_sexp, description, type, attributes_sexp] = struct.value()
                package_url = package_name.value() \
                              + "-" + version_string(version) \
                              + type_to_extension(type.value())
                h.request("GET", "/packages/" + package_url)
                down_response = h.getresponse()
                if down_response.status == 200:
                    body = down_response.read()
                    with open("downloads/" + package_url, "w") as fd:
                        fd.write(body)
            except:
                print package_name.value(), " had an error", sys.exc_info()
                h = httplib.HTTPConnection("elpa.gnu.org")

if __name__ == "__main__":
    download_archive()

# End
