"""Provides interface for the HPSS client and file functionality

From hpss_types.h

enum hpss_authn_mech_t {
    hpss_authn_mech_invalid = 0,
    hpss_authn_mech_krb5 = 1,
    hpss_authn_mech_unix = 2,
    hpss_authn_mech_gsi  = 3,
    hpss_authn_mech_spkm = 4
};

enum hpss_rpc_cred_type_t {
    hpss_rpc_cred_server = 1,
    hpss_rpc_cred_client,
    hpss_rpc_cred_both
};

enum hpss_rpc_auth_type_t {
    hpss_rpc_auth_type_invalid = 0,
    hpss_rpc_auth_type_none    = 1,
    hpss_rpc_auth_type_keytab  = 2,
    hpss_rpc_auth_type_keyfile = 3,
    hpss_rpc_auth_type_key     = 4,
    hpss_rpc_auth_type_passwd  = 5
};
"""

from ctypes import cdll, c_void_p, create_string_buffer, c_char_p, cast
import doctest

# c extension import not picked up by pylint, so disabling
# pylint: disable=import-error
# pylint: disable=no-name-in-module
import pacifica._archiveinterface as _archiveinterface
# pylint: enable=import-error
# pylint: disable=no-name-in-module


HPSS_AUTHN_MECH_INVALID = 0
HPSS_AUTHN_MECH_KRB5 = 1
HPSS_AUTHN_MECH_UNIX = 2
HPSS_AUTHN_MECH_GSI = 3
HPSS_AUTHN_MECH_SPKM = 4

HPSS_RPC_CRED_SERVER = 1
HPSS_RPC_CRED_CLIENT = 2
HPSS_RPC_CRED_BOTH = 3

HPSS_RPC_AUTH_TYPE_INVALID = 0
HPSS_RPC_AUTH_TYPE_NONE = 1
HPSS_RPC_AUTH_TYPE_KEYTAB = 2
HPSS_RPC_AUTH_TYPE_KEYFILE = 3
HPSS_RPC_AUTH_TYPE_KEY = 4
HPSS_RPC_AUTH_TYPE_PASSWD = 5

class HPSSClientError(Exception):
    """
    HPSSClientError - basic exception class for this module.

    >>> HPSSClientError()
    HPSSClientError()
    """
    pass

class HPSSCommon(object):
    """ Class for handling common hpss methods,
    such as pinging the core server.
    """
    def __init__(self, accept_latency=5):
        self._accept_latency = accept_latency
        self._latency = None

    def ping_core(self):
        """Ping the Core server to see if its still active"""

        #Define acceptable latency in seconds
        acceptable_latency = self._accept_latency
        latency_tuple = _archiveinterface.hpss_ping_core()
        # Get the latency
        latency = self.parse_latency(latency_tuple)


        if latency > acceptable_latency:
            raise HPSSClientError("The archive core server is slow to respond"+
                                  " Latency is: "+ str(latency) + " second(s)")

    def parse_latency(self, latency_tuple):
        """
        Parses the tuple returned by the c extension into
        the correct latency
        """
        # Get the latency
        # LatencyTuple[0] = time the core server responded
        # LatencyTuple[1] = microseconds relative to core server
        # LatencyTuple[2] = time before pinging core server
        # LatencyTuple[3] = microseconds relative before ping

        lat_seconds = float(latency_tuple[0])
        lat_microseconds = (float(latency_tuple[1])/1000000)
        response_time = lat_seconds + lat_microseconds
        before_ping_seconds = float(latency_tuple[2])
        before_ping_microseconds = (float(latency_tuple[3])/1000000)
        before_ping_time = before_ping_seconds + before_ping_microseconds
        latency = response_time - before_ping_time
        self._latency = latency
        return latency
       


class HPSSFile(HPSSCommon):
    """class that represents the hpss file struct and its methods"""
    def __init__(self, filepath, mode, hpsslib):
        HPSSCommon.__init__(self)
        self.closed = True
        self._hpsslib = hpsslib
        self._filepath = filepath
        hpss_fopen = self._hpsslib.hpss_Fopen
        hpss_fopen.restype = c_void_p

        self._hpssfile = hpss_fopen(filepath, mode)
        if self._hpssfile < 0:
            raise HPSSClientError("Failed Opening File")
        self.closed = False

    def status(self):
        """
        Get the status of a file if it is on tape or disk
        Found the documentation for this in the hpss programmers reference
        section 2.3.6.2.8 "Get Extanded Attributes"
        """
        self.ping_core()

        mtime = ""
        ctime = ""
        bytes_per_level = ""
        filesize = ""
        try:
            mtime = _archiveinterface.hpss_mtime(self._filepath)
            ctime = _archiveinterface.hpss_ctime(self._filepath)
            bytes_per_level = _archiveinterface.hpss_status(self._filepath)
            filesize = _archiveinterface.hpss_filesize(self._filepath)
            status = HPSSStatus(mtime, ctime, bytes_per_level, filesize)

        except Exception as ex:
            #Push the excpetion up the chain to the response
            raise HPSSClientError("Error using c extension for hpss status"+
                                  " exception: (%s)\n"%ex)

        return status

    def stage(self):
        """
        Stage an hpss file so that it moves to disk
        doesnt need to return anything.  will throw
        exception on error however
        """
        self.ping_core()

        try:
            _archiveinterface.hpss_stage(self._filepath)

        except Exception as ex:
            #Push the excpetion up the chain to the response
            raise HPSSClientError("Error using c extension for hpss stage"+
                                  " exception: (%s)\n"%ex)

    def read(self, blksize):
        """Read a file with the the hpss Fread"""
        self.ping_core()

        buf = create_string_buffer('\000'*blksize)
        rcode = self._hpsslib.hpss_Fread(buf, 1, blksize, self._hpssfile)
        if rcode < 0:
            raise HPSSClientError("Failed During HPSS Fread,"+
                                  "return value is (%d)"%(rcode))
        return buf.value

    def write(self, blk):
        """Write a block to a hpss file"""
        self.ping_core()
        blk_char_p = cast(blk, c_char_p)
        rcode = self._hpsslib.hpss_Fwrite(blk_char_p, 1,
                                          len(blk), self._hpssfile)
        if rcode != len(blk):
            raise HPSSClientError("Short write!")

    def close(self):
        """Close an hpss file"""
        if self.closed:
            return
        self.ping_core()
        self.flush()
        rcode = self._hpsslib.hpss_Fclose(self._hpssfile)
        if rcode < 0:
            raise HPSSClientError("Failed to close(%d)"%(rcode))

        self._hpssfile = None
        self.closed = True

    def flush(self):
        """Flush an hpss file"""
        if self.closed:
            return
        self.ping_core()
        rcode = self._hpsslib.hpss_Fflush(self._hpssfile)
        if rcode < 0:
            raise HPSSClientError(
                "Failed to flush buffer with error code(%d)"%(rcode))

    def seek(self, offset_in, whence):
        """Find a specific location in an hpss file"""
        self.ping_core()
        rcode = self._hpsslib.hpss_Fseek(self._hpssfile, offset_in, whence)
        if rcode < 0:
            raise HPSSClientError("Failed to seek with error code(%d)"%(rcode))

    def tell(self):
        """Get the location of seek in a file"""
        self.ping_core()
        rcode = self._hpsslib.hpss_Ftell()
        if rcode < 0:
            raise HPSSClientError("Failed fTell with error code(%d)"%(rcode))
        else:
            return rcode

    def set_mod_time(self, mod_time):
        """sets the last modified time on the file"""
        self.ping_core()
        try:
            _archiveinterface.hpss_utime(self._filepath, float(mod_time))

        except Exception as ex:
            #Push the excpetion up the chain to the response
            raise HPSSClientError("Error using c extension for hpss utime"+
                                  " exception: (%s)\n"%ex)


class HPSSClient(HPSSCommon):
    """
    Write the block to the file
    Testing conencting to hpss client, writing, and reading a file

    >>> user_name = "svc-myemsldev"
    >>> auth_path = "/var/hpss/etc/hpss.unix.keytab"
    >>> hpssclient = HPSSClient(user=user_name, auth=auth_path)
    >>> myfile = hpssclient.open("/myemsl-dev/bundle/test.txt", "w")
    >>> myfile.ping_core()
    >>> myfile.write('bar')
    >>> myfile.close()
    >>> myfile = hpssclient.open("/myemsl-dev/bundle/test.txt", "r")
    >>> myfile.read(20)
    'bar'
    >>> type(myfile.status())
    <class '__main__.HPSSStatus'>
    >>> myfile.stage()
    >>> myfile.close()
    """
    def __init__(self, library="/opt/hpss/lib/libhpss.so",
                 user="hpss", auth="/var/hpss/etc/hpss.unix.keytab"):
        HPSSCommon.__init__(self)
        self._hpsslib = cdll.LoadLibrary(library)
        rcode = self._hpsslib.hpss_SetLoginCred(user, HPSS_AUTHN_MECH_UNIX,
                                                HPSS_RPC_CRED_CLIENT,
                                                HPSS_RPC_AUTH_TYPE_KEYTAB, auth)

        if rcode != 0:
            raise HPSSClientError("Could Not Authenticate(%d)"%(rcode))

    def open(self, filename, mode):
        """Open an hpss file"""
        self.ping_core()
        return HPSSFile(filename, mode, self._hpsslib)

    def gethpsslib(self):
        """get the HPSS client libraries"""
        return self._hpsslib

class HPSSStatus(object):
    """Class for handling hpss status pieces
    needs mtime,ctime, bytes per level array
    >>> status = HPSSStatus(42, 33, [33,36,22], 36)
    >>> type(status)
    <class '__main__.HPSSStatus'>
    >>> status.file_storage_media
    'tape'
    """
    _disk = "disk"
    _tape = "tape"
    _error = "error"
    def __init__(self, mtime, ctime, bytes_per_level, filesize):
        self.mtime = mtime
        self.ctime = ctime
        self.bytes_per_level = bytes_per_level
        self.filesize = filesize
        self._defined_levels = self.define_levels()
        self.file_storage_media = self.find_file_storage_media()


    def find_file_storage_media(self):
        """Set if file is on disk or tape"""
        level_array = self._defined_levels
        level = 0
        for num_bytes in self.bytes_per_level:
            if num_bytes == self.filesize:
                break
            level += 1

        return level_array[level]

    def define_levels(self):
        """Sets up what each level definition means"""
        #This defines what hpss integer levels really mean
        #handle error if on level 4 or 5 since those are suppose to be null
        #UPDATE LEVEL NAMES AS NEEDED
        type_per_level = [self._disk, self._tape, self._tape,
                          self._error, self._error]
        return type_per_level



if __name__ == "__main__":
    doctest.testmod(verbose=True)
