import sexpdata
import httplib
import sys
import os
import urlparse
import ssl

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

def download_archive(host, directory):
    url_bits = urlparse.urlparse(host)
    h = httplib.HTTPConnection(url_bits.netloc)
    if url_bits.scheme == "https":
        insecure_context = ssl._create_unverified_context()
        h = httplib.HTTPSConnection(url_bits.netloc,context=insecure_context)

    h.request("GET", "/packages/archive-contents")
    response = h.getresponse()
    if response.status == 200:
        print url_bits.netloc + " archive-contents retrieved"
        body = response.read()

        try:
            os.makedirs(directory)
        except:
            pass
        with open(directory + "/archive-contents", "w") as fd:
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
                    with open(directory + "/" + package_url, "w") as fd:
                        fd.write(body)
            except:
                print package_name.value(), " had an error", sys.exc_info()
                h = httplib.HTTPConnection(url_bits.netloc)
                if url_bits.scheme == "https":
                    insecure_context = ssl._create_unverified_context()
                    h = httplib.HTTPSConnection(url_bits.netloc,context=insecure_context)

config = {
    "http://elpa.gnu.org": "elpa",
    "https://melpa.org": "melpa"
}

if __name__ == "__main__":
    for host, directory in config.items():
        download_archive(host, directory)

# End
