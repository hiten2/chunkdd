import os
import sys

def chunkdd(src, dest, max_chunk_size = 4 * 1024 * 1024 * 1024):
    max_chunk_size = int(max_chunk_size)
    buflen = min(16 * 1024 * 1024, max_chunk_size)
    chunk_size = max_chunk_size - (max_chunk_size % buflen)
    i = 0
    size = 0
    os.makedirs(dest)

    with open(src, "rb") as src_fp:
        src_fp.seek(0, os.SEEK_END)
        size = src_fp.tell()
        one_percent = 100.0 / size
        src_fp.seek(0, os.SEEK_SET)
        chunk = src_fp.read(buflen)
        
        while chunk:
            with open(os.path.join(dest, str(i)), "wb") as dest_fp:
                bytes_copied = 0
                print "writing to chunk %u" % i
                
                while chunk and bytes_copied < chunk_size:
                    dest_fp.write(chunk)
                    dest_fp.flush()
                    os.fdatasync(dest_fp.fileno())
                    
                    bytes_copied += buflen
                    chunk = src_fp.read(buflen)
                    print "%u / %u bytes copied (%f %% done)" % (
                        bytes_copied + (chunk_size * i), size,
                        (bytes_copied + (chunk_size * i)) * one_percent)
            i += 1

def unchunkdd(src, dest):
    buflen = 16 * 1024 * 1024
    chunk_size = 0
    i = 0

    with open(dest, "wb") as dest_fp:
        src_path = os.path.join(src, str(i))

        while os.path.exists(src_path):
            with open(src_path, "rb") as src_fp:
                bytes_copied = 0
                chunk = src_fp.read(buflen)
                print "reading from chunk %u" % i

                while chunk:
                    dest_fp.write(chunk)
                    dest_fp.flush()
                    os.fdatasync(dest_fp.fileno())

                    bytes_copied += len(chunk)
                    chunk = src_fp.read(buflen)
                    print "%u bytes copied" % \
                          (bytes_copied + (chunk_size * i))
                chunk_size = bytes_copied
            i += 1
            src_path = os.path.join(src, str(i))

if __name__ == "__main__":
    src = sys.argv[1]
    
    if os.path.isdir(src):
        unchunkdd(*sys.argv[1:])
    else:
        chunkdd(*sys.argv[1:])
