#!/usr/bin/env python
# encoding: utf-8
# PYTHON_ARGCOMPLETE_OK

# from __future__ imports must occur at the beginning of the file
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import sys
import os

# https://packaging.python.org/single_source_version/
__title__ = 'bypy'
__version__ = '1.3.5'
__author__ = 'Hou Tianze'
__license__ = 'MIT'
__desc__ ='Python client for Baidu Yun (Personal Cloud Storage) 百度云/百度网盘 Python 客户端'
__url__ = 'https://github.com/houtianze/bypy'

### return (error) codes
# they are put at the top because:
# 1. they have zero dependencies
# 2. can be referred in any abort later, e.g. return error on import faliures
ENoError = 0 # plain old OK, fine, no error.
EIncorrectPythonVersion = 1
#EApiNotConfigured = 10 # Deprecated: ApiKey, SecretKey and AppPcsPath not properly configured
EArgument = 10 # invalid program command argument
EAbort = 20 # aborted
EException = 30 # unhandled exception occured
EParameter = 40 # invalid parameter passed to ByPy
EInvalidJson = 50
EHashMismatch = 60 # MD5 hashes of the local file and remote file don't match each other
EFileWrite = 70
EFileTooBig = 80 # file too big to upload
EFailToCreateLocalDir = 90
EFailToCreateLocalFile = 100
EFailToDeleteDir = 110
EFailToDeleteFile = 120
EFileNotFound = 130
EMaxRetry = 140
ERequestFailed = 150 # request failed
ECacheNotLoaded = 160
EMigrationFailed = 170
EDownloadCerts = 180
EUserRejected = 190 # user's decision
EFatal = -1 # No way to continue
# internal errors
IEMD5NotFound = 31079 # File md5 not found, you should use upload API to upload the whole file.
IESuperfileCreationFailed = 31081 # superfile create failed (HTTP 404)
# Undocumented, see #308 , https://paste.ubuntu.com/23672323/
IEBlockMissInSuperFile2 = 31363 # block miss in superfile2 (HTTP 403)
IETaskNotFound = 36016 # Task was not found

DownloaderAria2 = 'aria2'
Downloaders = [DownloaderAria2]
DownloaderDefaultArgs = {
	DownloaderAria2 : "-c -k10M -x4 -s4  --file-allocation=none"
}

PipBinaryName = 'pip' + str(sys.version_info[0])
PipInstallCommand = PipBinaryName + ' install requests'
PipUpgradeCommand = PipBinaryName + ' install -U requests'

#### Definitions that are real world constants
OneK = 1024
OneM = OneK * OneK
OneG = OneM * OneK
OneT = OneG * OneK
OneP = OneT * OneK
OneE = OneP * OneK
OneZ = OneE * OneK
OneY = OneZ * OneK
SIPrefixNames = [ '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y' ]

SIPrefixTimes = {
	'K' : OneK,
	'M' : OneM,
	'G' : OneG,
	'T' : OneT,
	'E' : OneE,
	'Z' : OneZ,
	'Y' : OneY }

#### Baidu PCS constants
# ==== NOTE ====
# I use server auth, because it's the only possible method to protect the SecretKey.
# If you want to perform local authorization using 'Device' method instead, you just need:
# - Paste your own ApiKey and SecretKey. (An non-NONE or non-empty SecretKey means using local auth
# - Change the AppPcsPath to your own App's directory at Baidu PCS
# Then you are good to go
ApiKey = 'q8WE4EpCsau1oS0MplgMKNBn' # replace with your own ApiKey if you use your own appid
SecretKey = '' # replace with your own SecretKey if you use your own appid
# NOTE: no trailing '/'
AppPcsPath = '/apps/bypy' # change this to the App's directory you specified when creating the app
AppPcsPathLen = len(AppPcsPath)

## Baidu PCS URLs etc.
OpenApiUrl = "https://openapi.baidu.com"
OpenApiVersion = "2.0"
OAuthUrl = OpenApiUrl + "/oauth/" + OpenApiVersion
ServerAuthUrl = OAuthUrl + "/authorize"
DeviceAuthUrl = OAuthUrl + "/device/code"
TokenUrl = OAuthUrl + "/token"
PcsDomain = 'pcs.baidu.com'
RestApiPath = '/rest/2.0/pcs/'
PcsUrl = 'https://' + PcsDomain + RestApiPath
CPcsUrl = 'https://c.pcs.baidu.com/rest/2.0/pcs/'
DPcsUrl = 'https://d.pcs.baidu.com/rest/2.0/pcs/'

## Baidu PCS constants
MinRapidUploadFileSize = 256 * OneK
MaxSliceSize = 2 * OneG
MaxSlicePieces = 1024

### Auth servers
GaeUrl = 'https://bypyoauth.appspot.com'
OpenShiftUrl = 'https://bypy-tianze.rhcloud.com'
HerokuUrl = 'https://bypyoauth.herokuapp.com'
GaeRedirectUrl = GaeUrl + '/auth'
GaeRefreshUrl = GaeUrl + '/refresh'
OpenShiftRedirectUrl = OpenShiftUrl + '/auth'
OpenShiftRefreshUrl = OpenShiftUrl + '/refresh'
HerokuRedirectUrl = HerokuUrl + '/auth'
HerokuRefreshUrl = HerokuUrl + '/refresh'
AuthServerList = [
	# url, rety?, message
	(OpenShiftRedirectUrl, False, "Authorizing/refreshing with the OpenShift server ..."),
	(HerokuRedirectUrl, True, "OpenShift server failed, authorizing/refreshing with the Heroku server ..."),
	(GaeRedirectUrl, False, "Heroku server failed. Last resort: authorizing/refreshing with the GAE server ..."),
]
RefreshServerList = AuthServerList

### public static properties
HelpMarker = "Usage:"

### ByPy config constants
## directories, for setting, cache, etc
HomeDir = os.path.expanduser('~')
# os.path.join() may not handle unicode well
ConfigDir = HomeDir + os.sep + '.bypy'
TokenFileName = 'bypy.json'
TokenFilePath = ConfigDir + os.sep + TokenFileName
SettingFileName= 'bypy.setting.json'
SettingFilePath= ConfigDir + os.sep + SettingFileName
HashCacheFileName = 'bypy.hashcache.json'
HashCachePath = ConfigDir + os.sep + HashCacheFileName
PickleFileName = 'bypy.pickle'
PicklePath = ConfigDir + os.sep + PickleFileName
# ProgressPath saves the MD5s of uploaded slices, for upload resuming
# format:
# {
# 	abspath: [slice_size, [slice1md5, slice2md5, ...]],
# }
#
ProgressFileName = 'bypy.parts.json'
ProgressPath = ConfigDir + os.sep + ProgressFileName
ByPyCertsFileName = 'bypy.cacerts.pem'
OldByPyCertsPath = ConfigDir + os.sep + ByPyCertsFileName
# Old setting locations, should be moved to ~/.bypy to be clean
OldTokenFilePath = HomeDir + os.sep + '.bypy.json'
OldPicklePath = HomeDir + os.sep + '.bypy.pickle'
RemoteTempDir = AppPcsPath + '/.bypytemp'
SettingKey_OverwriteRemoteTempDir = 'overwriteRemoteTempDir'

## default config values
PrintFlushPeriodInSec = 5.0
# TODO: Does the following User-Agent emulation help?
UserAgent = None # According to xslidian, User-Agent affects download.
#UserAgent = 'Mozilla/5.0'
#UserAgent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"
#UserAgent = 'netdisk;5.2.7.2;PC;PC-Windows;6.2.9200;WindowsBaiduYunGuanJia'
DefaultSliceInMB = 20
DefaultSliceSize = 20 * OneM
DefaultDlChunkSize = 20 * OneM
RetryDelayInSec = 10
CacheSavePeriodInSec = 10 * 60.0
# share retries
ShareRapidUploadRetries = 3
DefaultResumeDlRevertCount = 1

## program switches
CleanOptionShort= '-c'
CleanOptionLong= '--clean'
DisableSslCheckOption = '--disable-ssl-check'
CaCertsOption = '--cacerts'

# vim: tabstop=4 noexpandtab shiftwidth=4 softtabstop=4 ff=unix fileencoding=utf-8
