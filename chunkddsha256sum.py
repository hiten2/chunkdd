import hashlib
import os
import sys

def chunkddsha256sum(dir):
    buflen = 64 * 1024 * 1024
    bytes_read = 0
    i = 0
    path = os.path.join(dir, '0')
    sha256 = hashlib.sha256()

    while os.path.exists(path):
        print "reading from chunk %u" % i
        
        with open(path, "rb") as fp:
            chunk = fp.read(buflen)

            while chunk:
                sha256.update(chunk)
                bytes_read += len(chunk)
                chunk = fp.read(buflen)

                print "read %u bytes" % bytes_read
        i += 1
        path = os.path.join(dir, str(i))
    return sha256.hexdigest()

if __name__ == "__main__":
    print chunkddsha256sum(sys.argv[1])
