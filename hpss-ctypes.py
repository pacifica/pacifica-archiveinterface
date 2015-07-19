#!/usr/bin/python

from ctypes import cdll, c_void_p, create_string_buffer, c_char_p, cast

"""
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
HPSS_AUTHN_MECH_INVALID    = 0
HPSS_AUTHN_MECH_KRB5       = 1
HPSS_AUTHN_MECH_UNIX       = 2
HPSS_AUTHN_MECH_GSI        = 3
HPSS_AUTHN_MECH_SPKM       = 4

HPSS_RPC_CRED_SERVER       = 1
HPSS_RPC_CRED_CLIENT       = 2
HPSS_RPC_CRED_BOTH         = 3

HPSS_RPC_AUTH_TYPE_INVALID = 0
HPSS_RPC_AUTH_TYPE_NONE    = 1
HPSS_RPC_AUTH_TYPE_KEYTAB  = 2
HPSS_RPC_AUTH_TYPE_KEYFILE = 3
HPSS_RPC_AUTH_TYPE_KEY     = 4
HPSS_RPC_AUTH_TYPE_PASSWD  = 5

class HPSSClientError(Exception):
  """
  HPSSClientError - basic exception class for this module.

  >>> HPSSClientError()
  HPSSClientError()
  """
  pass

class HPSSFile(object):
  def __init__(self, file, mode, hpsslib):
    self._hpsslib = hpsslib
    hpss_Fopen = self._hpsslib.hpss_Fopen
    hpss_Fopen.restype = c_void_p
    self._hpssfile = hpss_Fopen(file, mode)
    self.closed = False

  def read(self, blksize):
    buf = create_string_buffer('\000'*blksize)
    rc = self._hpsslib.hpss_Fread(buf, 1, blksize, self._hpssfile)
    return buf.value

  def write(self, blk):
    blk_char_p = cast(blk, c_char_p)
    rc = self._hpsslib.hpss_Fwrite(blk_char_p, 1, len(blk), self._hpssfile)
    if rc != len(blk):
        raise HPSSClientError("Short write!")

  def close(self):
    rc = self._hpsslib.hpss_Fclose(self._hpssfile)
    if rc < 0:
        raise HPSSClientError("Failed to close(%d)"%(rc))
    self._hpssfile = 0
    self.closed = True

  def __del__(self):
    if not self.closed:
      self.close()
    

#  >>> myfile = hpssclient.open("/myemsldev/test.txt", "w")
#  >>> myfile.write('foo')
#  >>> myfile.close()
class HPSSClient(object):
  """
  Write the block to the file

  >>> hpssclient = HPSSClient(user="svc-myemsldev", auth="/home/dmlb2000/svc-myemsldev.keytab")
  >>> myfile = hpssclient.open("/myemsldev/test.txt", "w")
  >>> myfile.write('bar')
  >>> myfile.close()
  >>> myfile = hpssclient.open("/myemsldev/test.txt", "r")
  >>> myfile.read(20)
  'bar'
  >>> myfile.close()
  """
  def __init__(self, library="/opt/hpss/lib/libhpss.so", user="hpss", auth="/var/hpss/etc/hpss.unix.keytab"):
    self._hpsslib = cdll.LoadLibrary(library)
    rc = self._hpsslib.hpss_SetLoginCred(user, HPSS_AUTHN_MECH_UNIX, HPSS_RPC_CRED_CLIENT, HPSS_RPC_AUTH_TYPE_KEYTAB, auth)
    if rc < 0:
        raise HPSSClientError("Could Not Authenticate(%d)"%(rc))
    rc = self._hpsslib.hpss_Chdir("/")
    if rc < 0:
        raise HPSSClientError("Could not chdir(%d)"%(rc))

  def open(self, file, mode):
    return HPSSFile(file, mode, self._hpsslib)

if __name__ == "__main__":
  import doctest
  doctest.testmod(verbose=True)
