VER_NUM = 200
"""
Blattidus Preview Version: blattidus/2.0p1 © 2020-2021 citrons

This is a preview version of blattidus. Please note that many additions
are yet occur, and much is subject to change. Please report any bugs or
atmospheric anomalies. If Blattidus Preview Version exhibits any signs of
sentience, disconnect all power to the device and all nearby internet
connected devices immediately. If you are using hosted server space, shut
it down immediately and contact your web hosting provider. Take deep
breaths to attempt to slow your heart rate. DO NOT TELL IT YOUR NAME UNDER ANY
CIRCUMSTANCES. Evacuate the building if possible. Do not call the police.


                         BLATTIDUS PREVIEW LICENSE

Permission is granted to copy, modify, or distribute this software, under the
condition that it only be distributed to those eligible to receive copies of
the software. A person is eligible to receive a copy of the software if they
have ever deployed an instance of blattidus which is internet accessible. This
software may not be distributed to individuals who are not eligible.

BY USING, COPYING, MODIFYING, DISTRIBUTING OR DEALING WITH THIS SOFTWARE
IN ANY MANNER, YOU ACQUIESCE YOUR SOUL TO THE FULL OWNERSHIP (OR OWNERSHIP
TO THE EXTENT TO WHICH YOU ARE LEGALLY CAPABLE OF PROVIDING) AND CONTROL
OF BLATTIDUS, INC. AND CONSTITUENTS.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

"""
WARNING: USE at YOUR OWN RISK!

USE of BLATTIDUS/2.0 MAY CAUSE
 - IRREVERSIBLE CHANGES to YOUR SYSTEM and/or THE SPACETIME IT OCCUPIES
 - CAUSALITY VIOLATIONS
 - SINUS INFECTIONS
 - ARREST by THE JAPANESE POLICE
 - SPONTANEOUS INJURY or DEATH
 - BEE SWARMS
 - [REDACTED]
 - VIOLATION of INTERNATIONAL TREATIES
 - PESTILENCE

THERE IS NO WARRANTY.
BLATTIDUS, INC IS NOT RESPONSIBLE FOR ANY DAMAGE or ELDRICH HORRORS
CAUSED or SUMMONED via THE USAGE of BLATTIDUS/2.0 or HYPERCAL.

https://mondecitronne.com/main/blattidus
"""

# blattidus contains no™* spaghetti code

import socketserver
import random
from sys import stderr,stdout,exit,setrecursionlimit
import os.path
import re
import urllib.parse
from html import escape
import argparse
from functools import lru_cache
import sqlite3
import socket
import ssl
import threading
import hashlib

setrecursionlimit(10000)

ap = argparse.ArgumentParser()

ap.add_argument("-p", "--port", help="port to serve on", type=int, 
        default=80)
ap.add_argument("-s", "--https", help="enable https", metavar="CERT_FILE")
ap.add_argument("-k", "--privkey", help="private key for https", metavar="KEY_FILE")
ap.add_argument("-P", "--https-port", help="port to serve https on", type=int, 
        default=443)
ap.add_argument("-r", "--webroot", help="directory to serve files from", 
        default="/var/www/html")
ap.add_argument("-U", "--auto-update", metavar='FILE',
        help="enable automatic updates, storing update data in FILE")
ap.add_argument("-l", "--log", help="log activity to stderr", action='store_true')
ap.add_argument("-c", "--cache", metavar='SIZE',
        help="maximum amount of files to cache", type=int, default=50)

args = ap.parse_args()

HOST = ''

PORT = args.port

WEBROOT = args.webroot

ssl_ctx = None
if args.https != None:
    ssl_ctx = ssl.SSLContext()
    ssl_ctx.load_cert_chain(args.https,keyfile=args.privkey)

def get_page_(path):
    try:
        if path[0] == '/':
            path = path[1:]
        fpath = os.path.join(WEBROOT, path)
        if not os.path.abspath(fpath).startswith(os.path.abspath(WEBROOT)):
            return None
        with open(fpath, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return None

cachesize = args.cache

if cachesize != 0:
    get_page = lru_cache(maxsize=cachesize)(get_page_)
else:
    get_page = get_page_

DEFAULT_INDEX = "<script>while(1)alert('I will now be arrested by the Japanese police.')</script>"
VERSION = "blattidus/2.0p1"

STATUS_CODES = {
    200: "200 Everyone Is Always Asking What the Status Code Is But No One Ever Asks How the Status Code Is Like If You Agree",
    299: "299 Polo!",
    400: "400 Do You Even Know HTTP?",
    404: "404 Link Rot",
    405: "405 GET Better at HTTP",
    418: "418 I'm a teapot",
    500: "500 I Am NOT OK"
}


MIMES = {".123":"application/vnd.lotus-1-2-3",".3dml":"text/vnd.in3d.3dml",".3g2":"video/3gpp2",".3gp":"video/3gpp",".a":"application/octet-stream",".aab":"application/x-authorware-bin",".aac":"audio/x-aac",".aam":"application/x-authorware-map",".aas":"application/x-authorware-seg",".abw":"application/x-abiword",".acc":"application/vnd.americandynamics.acc",".ace":"application/x-ace-compressed",".acu":"application/vnd.acucobol",".acutc":"application/vnd.acucorp",".adp":"audio/adpcm",".aep":"application/vnd.audiograph",".afm":"application/x-font-type1",".afp":"application/vnd.ibm.modcap",".ai":"application/postscript",".aif":"audio/x-aiff",".aifc":"audio/x-aiff",".aiff":"audio/x-aiff",".air":"application/vnd.adobe.air-application-installer-package+zip",".ami":"application/vnd.amiga.ami",".apk":"application/vnd.android.package-archive",".application":"application/x-ms-application",".apr":"application/vnd.lotus-approach",".asc":"application/pgp-signature",".asf":"video/x-ms-asf",".asm":"text/x-asm",".aso":"application/vnd.accpac.simply.aso",".asx":"video/x-ms-asf",".atc":"application/vnd.acucorp",".atom":"application/atom+xml",".atomcat":"application/atomcat+xml",".atomsvc":"application/atomsvc+xml",".atx":"application/vnd.antix.game-component",".au":"audio/basic",".avi":"video/x-msvideo",".aw":"application/applixware",".azf":"application/vnd.airzip.filesecure.azf",".azs":"application/vnd.airzip.filesecure.azs",".azw":"application/vnd.amazon.ebook",".bat":"application/x-msdownload",".bcpio":"application/x-bcpio",".bdf":"application/x-font-bdf",".bdm":"application/vnd.syncml.dm+wbxml",".bh2":"application/vnd.fujitsu.oasysprs",".bin":"application/octet-stream",".bmi":"application/vnd.bmi",".bmp":"image/bmp",".book":"application/vnd.framemaker",".box":"application/vnd.previewsystems.box",".boz":"application/x-bzip2",".bpk":"application/octet-stream",".btif":"image/prs.btif",".bz":"application/x-bzip",".bz2":"application/x-bzip2",".c":"text/x-c",".c4d":"application/vnd.clonk.c4group",".c4f":"application/vnd.clonk.c4group",".c4g":"application/vnd.clonk.c4group",".c4p":"application/vnd.clonk.c4group",".c4u":"application/vnd.clonk.c4group",".cab":"application/vnd.ms-cab-compressed",".car":"application/vnd.curl.car",".cat":"application/vnd.ms-pki.seccat",".cc":"text/x-c",".cct":"application/x-director",".ccxml":"application/ccxml+xml",".cdbcmsg":"application/vnd.contact.cmsg",".cdf":"application/x-netcdf",".cdkey":"application/vnd.mediastation.cdkey",".cdx":"chemical/x-cdx",".cdxml":"application/vnd.chemdraw+xml",".cdy":"application/vnd.cinderella",".cer":"application/pkix-cert",".cgm":"image/cgm",".chat":"application/x-chat",".chm":"application/vnd.ms-htmlhelp",".chrt":"application/vnd.kde.kchart",".cif":"chemical/x-cif",".cii":"application/vnd.anser-web-certificate-issue-initiation",".cil":"application/vnd.ms-artgalry",".cla":"application/vnd.claymore",".class":"application/java-vm",".clkk":"application/vnd.crick.clicker.keyboard",".clkp":"application/vnd.crick.clicker.palette",".clkt":"application/vnd.crick.clicker.template",".clkw":"application/vnd.crick.clicker.wordbank",".clkx":"application/vnd.crick.clicker",".clp":"application/x-msclip",".cmc":"application/vnd.cosmocaller",".cmdf":"chemical/x-cmdf",".cml":"chemical/x-cml",".cmp":"application/vnd.yellowriver-custom-menu",".cmx":"image/x-cmx",".cod":"application/vnd.rim.cod",".com":"application/x-msdownload",".conf":"text/plain",".cpio":"application/x-cpio",".cpp":"text/x-c",".cpt":"application/mac-compactpro",".crd":"application/x-mscardfile",".crl":"application/pkix-crl",".crt":"application/x-x509-ca-cert",".csh":"application/x-csh",".csml":"chemical/x-csml",".csp":"application/vnd.commonspace",".css":"text/css",".cst":"application/x-director",".csv":"text/csv",".cu":"application/cu-seeme",".curl":"text/vnd.curl",".cww":"application/prs.cww",".cxt":"application/x-director",".cxx":"text/x-c",".daf":"application/vnd.mobius.daf",".dataless":"application/vnd.fdsn.seed",".davmount":"application/davmount+xml",".dcr":"application/x-director",".dcurl":"text/vnd.curl.dcurl",".dd2":"application/vnd.oma.dd2+xml",".ddd":"application/vnd.fujixerox.ddd",".deb":"application/x-debian-package",".def":"text/plain",".deploy":"application/octet-stream",".der":"application/x-x509-ca-cert",".dfac":"application/vnd.dreamfactory",".dic":"text/x-c",".diff":"text/plain",".dir":"application/x-director",".dis":"application/vnd.mobius.dis",".dist":"application/octet-stream",".distz":"application/octet-stream",".djv":"image/vnd.djvu",".djvu":"image/vnd.djvu",".dll":"application/x-msdownload",".dmg":"application/octet-stream",".dms":"application/octet-stream",".dna":"application/vnd.dna",".doc":"application/msword",".docm":"application/vnd.ms-word.document.macroenabled.12",".docx":"application/vnd.openxmlformats-officedocument.wordprocessingml.document",".dot":"application/msword",".dotm":"application/vnd.ms-word.template.macroenabled.12",".dotx":"application/vnd.openxmlformats-officedocument.wordprocessingml.template",".dp":"application/vnd.osgi.dp",".dpg":"application/vnd.dpgraph",".dsc":"text/prs.lines.tag",".dtb":"application/x-dtbook+xml",".dtd":"application/xml-dtd",".dts":"audio/vnd.dts",".dtshd":"audio/vnd.dts.hd",".dump":"application/octet-stream",".dvi":"application/x-dvi",".dwf":"model/vnd.dwf",".dwg":"image/vnd.dwg",".dxf":"image/vnd.dxf",".dxp":"application/vnd.spotfire.dxp",".dxr":"application/x-director",".ecelp4800":"audio/vnd.nuera.ecelp4800",".ecelp7470":"audio/vnd.nuera.ecelp7470",".ecelp9600":"audio/vnd.nuera.ecelp9600",".ecma":"application/ecmascript",".edm":"application/vnd.novadigm.edm",".edx":"application/vnd.novadigm.edx",".efif":"application/vnd.picsel",".ei6":"application/vnd.pg.osasli",".elc":"application/octet-stream",".eml":"message/rfc822",".emma":"application/emma+xml",".eol":"audio/vnd.digital-winds",".eot":"application/vnd.ms-fontobject",".eps":"application/postscript",".epub":"application/epub+zip",".es3":"application/vnd.eszigno3+xml",".esf":"application/vnd.epson.esf",".et3":"application/vnd.eszigno3+xml",".etx":"text/x-setext",".exe":"application/x-msdownload",".ext":"application/vnd.novadigm.ext",".ez":"application/andrew-inset",".ez2":"application/vnd.ezpix-album",".ez3":"application/vnd.ezpix-package",".f":"text/x-fortran",".f4v":"video/x-f4v",".f77":"text/x-fortran",".f90":"text/x-fortran",".fbs":"image/vnd.fastbidsheet",".fdf":"application/vnd.fdf",".fe_launch":"application/vnd.denovo.fcselayout-link",".fg5":"application/vnd.fujitsu.oasysgp",".fgd":"application/x-director",".fh":"image/x-freehand",".fh4":"image/x-freehand",".fh5":"image/x-freehand",".fh7":"image/x-freehand",".fhc":"image/x-freehand",".fig":"application/x-xfig",".fli":"video/x-fli",".flo":"application/vnd.micrografx.flo",".flv":"video/x-flv",".flw":"application/vnd.kde.kivio",".flx":"text/vnd.fmi.flexstor",".fly":"text/vnd.fly",".fm":"application/vnd.framemaker",".fnc":"application/vnd.frogans.fnc",".for":"text/x-fortran",".fpx":"image/vnd.fpx",".frame":"application/vnd.framemaker",".fsc":"application/vnd.fsc.weblaunch",".fst":"image/vnd.fst",".ftc":"application/vnd.fluxtime.clip",".fti":"application/vnd.anser-web-funds-transfer-initiation",".fvt":"video/vnd.fvt",".fzs":"application/vnd.fuzzysheet",".g3":"image/g3fax",".gac":"application/vnd.groove-account",".gdl":"model/vnd.gdl",".geo":"application/vnd.dynageo",".gex":"application/vnd.geometry-explorer",".ggb":"application/vnd.geogebra.file",".ggt":"application/vnd.geogebra.tool",".ghf":"application/vnd.groove-help",".gif":"image/gif",".gim":"application/vnd.groove-identity-message",".gmx":"application/vnd.gmx",".gnumeric":"application/x-gnumeric",".gph":"application/vnd.flographit",".gqf":"application/vnd.grafeq",".gqs":"application/vnd.grafeq",".gram":"application/srgs",".gre":"application/vnd.geometry-explorer",".grv":"application/vnd.groove-injector",".grxml":"application/srgs+xml",".gsf":"application/x-font-ghostscript",".gtar":"application/x-gtar",".gtm":"application/vnd.groove-tool-message",".gtw":"model/vnd.gtw",".gv":"text/vnd.graphviz",".gz":"application/x-gzip",".h":"text/x-c",".h261":"video/h261",".h263":"video/h263",".h264":"video/h264",".hbci":"application/vnd.hbci",".hdf":"application/x-hdf",".hh":"text/x-c",".hlp":"application/winhlp",".hpgl":"application/vnd.hp-hpgl",".hpid":"application/vnd.hp-hpid",".hps":"application/vnd.hp-hps",".hqx":"application/mac-binhex40",".htke":"application/vnd.kenameaapp",".htm":"text/html",".html":"text/html",".hvd":"application/vnd.yamaha.hv-dic",".hvp":"application/vnd.yamaha.hv-voice",".hvs":"application/vnd.yamaha.hv-script",".icc":"application/vnd.iccprofile",".ice":"x-conference/x-cooltalk",".icm":"application/vnd.iccprofile",".ico":"image/x-icon",".ics":"text/calendar",".ief":"image/ief",".ifb":"text/calendar",".ifm":"application/vnd.shana.informed.formdata",".iges":"model/iges",".igl":"application/vnd.igloader",".igs":"model/iges",".igx":"application/vnd.micrografx.igx",".iif":"application/vnd.shana.informed.interchange",".imp":"application/vnd.accpac.simply.imp",".ims":"application/vnd.ms-ims",".in":"text/plain",".ipk":"application/vnd.shana.informed.package",".irm":"application/vnd.ibm.rights-management",".irp":"application/vnd.irepository.package+xml",".iso":"application/octet-stream",".itp":"application/vnd.shana.informed.formtemplate",".ivp":"application/vnd.immervision-ivp",".ivu":"application/vnd.immervision-ivu",".jad":"text/vnd.sun.j2me.app-descriptor",".jam":"application/vnd.jam",".jar":"application/java-archive",".java":"text/x-java-source",".jisp":"application/vnd.jisp",".jlt":"application/vnd.hp-jlyt",".jnlp":"application/x-java-jnlp-file",".joda":"application/vnd.joost.joda-archive",".jpe":"image/jpeg",".jpeg":"image/jpeg",".jpg":"image/jpeg",".jpgm":"video/jpm",".jpgv":"video/jpeg",".jpm":"video/jpm",".js":"application/javascript",".json":"application/json",".kar":"audio/midi",".karbon":"application/vnd.kde.karbon",".kfo":"application/vnd.kde.kformula",".kia":"application/vnd.kidspiration",".kil":"application/x-killustrator",".kml":"application/vnd.google-earth.kml+xml",".kmz":"application/vnd.google-earth.kmz",".kne":"application/vnd.kinar",".knp":"application/vnd.kinar",".kon":"application/vnd.kde.kontour",".kpr":"application/vnd.kde.kpresenter",".kpt":"application/vnd.kde.kpresenter",".ksh":"text/plain",".ksp":"application/vnd.kde.kspread",".ktr":"application/vnd.kahootz",".ktz":"application/vnd.kahootz",".kwd":"application/vnd.kde.kword",".kwt":"application/vnd.kde.kword",".latex":"application/x-latex",".lbd":"application/vnd.llamagraphics.life-balance.desktop",".lbe":"application/vnd.llamagraphics.life-balance.exchange+xml",".les":"application/vnd.hhe.lesson-player",".lha":"application/octet-stream",".link66":"application/vnd.route66.link66+xml",".list":"text/plain",".list3820":"application/vnd.ibm.modcap",".listafp":"application/vnd.ibm.modcap",".log":"text/plain",".lostxml":"application/lost+xml",".lrf":"application/octet-stream",".lrm":"application/vnd.ms-lrm",".ltf":"application/vnd.frogans.ltf",".lvp":"audio/vnd.lucent.voice",".lwp":"application/vnd.lotus-wordpro",".lzh":"application/octet-stream",".m13":"application/x-msmediaview",".m14":"application/x-msmediaview",".m1v":"video/mpeg",".m2a":"audio/mpeg",".m2v":"video/mpeg",".m3a":"audio/mpeg",".m3u":"audio/x-mpegurl",".m4u":"video/vnd.mpegurl",".m4v":"video/x-m4v",".ma":"application/mathematica",".mag":"application/vnd.ecowin.chart",".maker":"application/vnd.framemaker",".man":"text/troff",".mathml":"application/mathml+xml",".mb":"application/mathematica",".mbk":"application/vnd.mobius.mbk",".mbox":"application/mbox",".mc1":"application/vnd.medcalcdata",".mcd":"application/vnd.mcd",".mcurl":"text/vnd.curl.mcurl",".mdb":"application/x-msaccess",".mdi":"image/vnd.ms-modi",".me":"text/troff",".mesh":"model/mesh",".mfm":"application/vnd.mfmp",".mgz":"application/vnd.proteus.magazine",".mht":"message/rfc822",".mhtml":"message/rfc822",".mid":"audio/midi",".midi":"audio/midi",".mif":"application/vnd.mif",".mime":"message/rfc822",".mj2":"video/mj2",".mjp2":"video/mj2",".mlp":"application/vnd.dolby.mlp",".mmd":"application/vnd.chipnuts.karaoke-mmd",".mmf":"application/vnd.smaf",".mmr":"image/vnd.fujixerox.edmics-mmr",".mny":"application/x-msmoney",".mobi":"application/x-mobipocket-ebook",".mov":"video/quicktime",".movie":"video/x-sgi-movie",".mp2":"audio/mpeg",".mp2a":"audio/mpeg",".mp3":"audio/mpeg",".mp4":"video/mp4",".mp4a":"audio/mp4",".mp4s":"application/mp4",".mp4v":"video/mp4",".mpa":"video/mpeg",".mpc":"application/vnd.mophun.certificate",".mpe":"video/mpeg",".mpeg":"video/mpeg",".mpg":"video/mpeg",".mpg4":"video/mp4",".mpga":"audio/mpeg",".mpkg":"application/vnd.apple.installer+xml",".mpm":"application/vnd.blueice.multipass",".mpn":"application/vnd.mophun.application",".mpp":"application/vnd.ms-project",".mpt":"application/vnd.ms-project",".mpy":"application/vnd.ibm.minipay",".mqy":"application/vnd.mobius.mqy",".mrc":"application/marc",".ms":"text/troff",".mscml":"application/mediaservercontrol+xml",".mseed":"application/vnd.fdsn.mseed",".mseq":"application/vnd.mseq",".msf":"application/vnd.epson.msf",".msh":"model/mesh",".msi":"application/x-msdownload",".msl":"application/vnd.mobius.msl",".msty":"application/vnd.muvee.style",".mts":"model/vnd.mts",".mus":"application/vnd.musician",".musicxml":"application/vnd.recordare.musicxml+xml",".mvb":"application/x-msmediaview",".mwf":"application/vnd.mfer",".mxf":"application/mxf",".mxl":"application/vnd.recordare.musicxml",".mxml":"application/xv+xml",".mxs":"application/vnd.triscape.mxs",".mxu":"video/vnd.mpegurl",".n-gage":"application/vnd.nokia.n-gage.symbian.install",".nb":"application/mathematica",".nc":"application/x-netcdf",".ncx":"application/x-dtbncx+xml",".ngdat":"application/vnd.nokia.n-gage.data",".nlu":"application/vnd.neurolanguage.nlu",".nml":"application/vnd.enliven",".nnd":"application/vnd.noblenet-directory",".nns":"application/vnd.noblenet-sealer",".nnw":"application/vnd.noblenet-web",".npx":"image/vnd.net-fpx",".nsf":"application/vnd.lotus-notes",".nws":"message/rfc822",".o":"application/octet-stream",".oa2":"application/vnd.fujitsu.oasys2",".oa3":"application/vnd.fujitsu.oasys3",".oas":"application/vnd.fujitsu.oasys",".obd":"application/x-msbinder",".obj":"application/octet-stream",".oda":"application/oda",".odb":"application/vnd.oasis.opendocument.database",".odc":"application/vnd.oasis.opendocument.chart",".odf":"application/vnd.oasis.opendocument.formula",".odft":"application/vnd.oasis.opendocument.formula-template",".odg":"application/vnd.oasis.opendocument.graphics",".odi":"application/vnd.oasis.opendocument.image",".odp":"application/vnd.oasis.opendocument.presentation",".ods":"application/vnd.oasis.opendocument.spreadsheet",".odt":"application/vnd.oasis.opendocument.text",".oga":"audio/ogg",".ogg":"audio/ogg",".ogv":"video/ogg",".ogx":"application/ogg",".onepkg":"application/onenote",".onetmp":"application/onenote",".onetoc":"application/onenote",".onetoc2":"application/onenote",".opf":"application/oebps-package+xml",".oprc":"application/vnd.palm",".org":"application/vnd.lotus-organizer",".osf":"application/vnd.yamaha.openscoreformat",".osfpvg":"application/vnd.yamaha.openscoreformat.osfpvg+xml",".otc":"application/vnd.oasis.opendocument.chart-template",".otf":"application/x-font-otf",".otg":"application/vnd.oasis.opendocument.graphics-template",".oth":"application/vnd.oasis.opendocument.text-web",".oti":"application/vnd.oasis.opendocument.image-template",".otm":"application/vnd.oasis.opendocument.text-master",".otp":"application/vnd.oasis.opendocument.presentation-template",".ots":"application/vnd.oasis.opendocument.spreadsheet-template",".ott":"application/vnd.oasis.opendocument.text-template",".oxt":"application/vnd.openofficeorg.extension",".p":"text/x-pascal",".p10":"application/pkcs10",".p12":"application/x-pkcs12",".p7b":"application/x-pkcs7-certificates",".p7c":"application/pkcs7-mime",".p7m":"application/pkcs7-mime",".p7r":"application/x-pkcs7-certreqresp",".p7s":"application/pkcs7-signature",".pas":"text/x-pascal",".pbd":"application/vnd.powerbuilder6",".pbm":"image/x-portable-bitmap",".pcf":"application/x-font-pcf",".pcl":"application/vnd.hp-pcl",".pclxl":"application/vnd.hp-pclxl",".pct":"image/x-pict",".pcurl":"application/vnd.curl.pcurl",".pcx":"image/x-pcx",".pdb":"application/vnd.palm",".pdf":"application/pdf",".pfa":"application/x-font-type1",".pfb":"application/x-font-type1",".pfm":"application/x-font-type1",".pfr":"application/font-tdpfr",".pfx":"application/x-pkcs12",".pgm":"image/x-portable-graymap",".pgn":"application/x-chess-pgn",".pgp":"application/pgp-encrypted",".pic":"image/x-pict",".pkg":"application/octet-stream",".pki":"application/pkixcmp",".pkipath":"application/pkix-pkipath",".pl":"text/plain",".plb":"application/vnd.3gpp.pic-bw-large",".plc":"application/vnd.mobius.plc",".plf":"application/vnd.pocketlearn",".pls":"application/pls+xml",".pml":"application/vnd.ctc-posml",".png":"image/png",".pnm":"image/x-portable-anymap",".portpkg":"application/vnd.macports.portpkg",".pot":"application/vnd.ms-powerpoint",".potm":"application/vnd.ms-powerpoint.template.macroenabled.12",".potx":"application/vnd.openxmlformats-officedocument.presentationml.template",".ppa":"application/vnd.ms-powerpoint",".ppam":"application/vnd.ms-powerpoint.addin.macroenabled.12",".ppd":"application/vnd.cups-ppd",".ppm":"image/x-portable-pixmap",".pps":"application/vnd.ms-powerpoint",".ppsm":"application/vnd.ms-powerpoint.slideshow.macroenabled.12",".ppsx":"application/vnd.openxmlformats-officedocument.presentationml.slideshow",".ppt":"application/vnd.ms-powerpoint",".pptm":"application/vnd.ms-powerpoint.presentation.macroenabled.12",".pptx":"application/vnd.openxmlformats-officedocument.presentationml.presentation",".pqa":"application/vnd.palm",".prc":"application/x-mobipocket-ebook",".pre":"application/vnd.lotus-freelance",".prf":"application/pics-rules",".ps":"application/postscript",".psb":"application/vnd.3gpp.pic-bw-small",".psd":"image/vnd.adobe.photoshop",".psf":"application/x-font-linux-psf",".ptid":"application/vnd.pvi.ptid1",".pub":"application/x-mspublisher",".pvb":"application/vnd.3gpp.pic-bw-var",".pwn":"application/vnd.3m.post-it-notes",".pwz":"application/vnd.ms-powerpoint",".py":"text/x-python",".pya":"audio/vnd.ms-playready.media.pya",".pyc":"application/x-python-code",".pyo":"application/x-python-code",".pyv":"video/vnd.ms-playready.media.pyv",".qam":"application/vnd.epson.quickanime",".qbo":"application/vnd.intu.qbo",".qfx":"application/vnd.intu.qfx",".qps":"application/vnd.publishare-delta-tree",".qt":"video/quicktime",".qwd":"application/vnd.quark.quarkxpress",".qwt":"application/vnd.quark.quarkxpress",".qxb":"application/vnd.quark.quarkxpress",".qxd":"application/vnd.quark.quarkxpress",".qxl":"application/vnd.quark.quarkxpress",".qxt":"application/vnd.quark.quarkxpress",".ra":"audio/x-pn-realaudio",".ram":"audio/x-pn-realaudio",".rar":"application/x-rar-compressed",".ras":"image/x-cmu-raster",".rcprofile":"application/vnd.ipunplugged.rcprofile",".rdf":"application/rdf+xml",".rdz":"application/vnd.data-vision.rdz",".rep":"application/vnd.businessobjects",".res":"application/x-dtbresource+xml",".rgb":"image/x-rgb",".rif":"application/reginfo+xml",".rl":"application/resource-lists+xml",".rlc":"image/vnd.fujixerox.edmics-rlc",".rld":"application/resource-lists-diff+xml",".rm":"application/vnd.rn-realmedia",".rmi":"audio/midi",".rmp":"audio/x-pn-realaudio-plugin",".rms":"application/vnd.jcp.javame.midlet-rms",".rnc":"application/relax-ng-compact-syntax",".roff":"text/troff",".rpm":"application/x-rpm",".rpss":"application/vnd.nokia.radio-presets",".rpst":"application/vnd.nokia.radio-preset",".rq":"application/sparql-query",".rs":"application/rls-services+xml",".rsd":"application/rsd+xml",".rss":"application/rss+xml",".rtf":"application/rtf",".rtx":"text/richtext",".s":"text/x-asm",".saf":"application/vnd.yamaha.smaf-audio",".sbml":"application/sbml+xml",".sc":"application/vnd.ibm.secure-container",".scd":"application/x-msschedule",".scm":"application/vnd.lotus-screencam",".scq":"application/scvp-cv-request",".scs":"application/scvp-cv-response",".scurl":"text/vnd.curl.scurl",".sda":"application/vnd.stardivision.draw",".sdc":"application/vnd.stardivision.calc",".sdd":"application/vnd.stardivision.impress",".sdkd":"application/vnd.solent.sdkm+xml",".sdkm":"application/vnd.solent.sdkm+xml",".sdp":"application/sdp",".sdw":"application/vnd.stardivision.writer",".see":"application/vnd.seemail",".seed":"application/vnd.fdsn.seed",".sema":"application/vnd.sema",".semd":"application/vnd.semd",".semf":"application/vnd.semf",".ser":"application/java-serialized-object",".setpay":"application/set-payment-initiation",".setreg":"application/set-registration-initiation",".sfd-hdstx":"application/vnd.hydrostatix.sof-data",".sfs":"application/vnd.spotfire.sfs",".sgl":"application/vnd.stardivision.writer-global",".sgm":"text/sgml",".sgml":"text/sgml",".sh":"application/x-sh",".shar":"application/x-shar",".shf":"application/shf+xml",".si":"text/vnd.wap.si",".sic":"application/vnd.wap.sic",".sig":"application/pgp-signature",".silo":"model/mesh",".sis":"application/vnd.symbian.install",".sisx":"application/vnd.symbian.install",".sit":"application/x-stuffit",".sitx":"application/x-stuffitx",".skd":"application/vnd.koan",".skm":"application/vnd.koan",".skp":"application/vnd.koan",".skt":"application/vnd.koan",".sl":"text/vnd.wap.sl",".slc":"application/vnd.wap.slc",".sldm":"application/vnd.ms-powerpoint.slide.macroenabled.12",".sldx":"application/vnd.openxmlformats-officedocument.presentationml.slide",".slt":"application/vnd.epson.salt",".smf":"application/vnd.stardivision.math",".smi":"application/smil+xml",".smil":"application/smil+xml",".snd":"audio/basic",".snf":"application/x-font-snf",".so":"application/octet-stream",".spc":"application/x-pkcs7-certificates",".spf":"application/vnd.yamaha.smaf-phrase",".spl":"application/x-futuresplash",".spot":"text/vnd.in3d.spot",".spp":"application/scvp-vp-response",".spq":"application/scvp-vp-request",".spx":"audio/ogg",".src":"application/x-wais-source",".srx":"application/sparql-results+xml",".sse":"application/vnd.kodak-descriptor",".ssf":"application/vnd.epson.ssf",".ssml":"application/ssml+xml",".stc":"application/vnd.sun.xml.calc.template",".std":"application/vnd.sun.xml.draw.template",".stf":"application/vnd.wt.stf",".sti":"application/vnd.sun.xml.impress.template",".stk":"application/hyperstudio",".stl":"application/vnd.ms-pki.stl",".str":"application/vnd.pg.format",".stw":"application/vnd.sun.xml.writer.template",".sus":"application/vnd.sus-calendar",".susp":"application/vnd.sus-calendar",".sv4cpio":"application/x-sv4cpio",".sv4crc":"application/x-sv4crc",".svd":"application/vnd.svd",".svg":"image/svg+xml",".svgz":"image/svg+xml",".swa":"application/x-director",".swf":"application/x-shockwave-flash",".swi":"application/vnd.arastra.swi",".sxc":"application/vnd.sun.xml.calc",".sxd":"application/vnd.sun.xml.draw",".sxg":"application/vnd.sun.xml.writer.global",".sxi":"application/vnd.sun.xml.impress",".sxm":"application/vnd.sun.xml.math",".sxw":"application/vnd.sun.xml.writer",".t":"text/troff",".tao":"application/vnd.tao.intent-module-archive",".tar":"application/x-tar",".tcap":"application/vnd.3gpp2.tcap",".tcl":"application/x-tcl",".teacher":"application/vnd.smart.teacher",".tex":"application/x-tex",".texi":"application/x-texinfo",".texinfo":"application/x-texinfo",".text":"text/plain",".tfm":"application/x-tex-tfm",".tgz":"application/x-gzip",".tif":"image/tiff",".tiff":"image/tiff",".tmo":"application/vnd.tmobile-livetv",".torrent":"application/x-bittorrent",".tpl":"application/vnd.groove-tool-template",".tpt":"application/vnd.trid.tpt",".tr":"text/troff",".tra":"application/vnd.trueapp",".trm":"application/x-msterminal",".tsv":"text/tab-separated-values",".ttc":"application/x-font-ttf",".ttf":"application/x-font-ttf",".twd":"application/vnd.simtech-mindmapper",".twds":"application/vnd.simtech-mindmapper",".txd":"application/vnd.genomatix.tuxedo",".txf":"application/vnd.mobius.txf",".txt":"text/plain",".u32":"application/x-authorware-bin",".udeb":"application/x-debian-package",".ufd":"application/vnd.ufdl",".ufdl":"application/vnd.ufdl",".umj":"application/vnd.umajin",".unityweb":"application/vnd.unity",".uoml":"application/vnd.uoml+xml",".uri":"text/uri-list",".uris":"text/uri-list",".urls":"text/uri-list",".ustar":"application/x-ustar",".utz":"application/vnd.uiq.theme",".uu":"text/x-uuencode",".vcd":"application/x-cdlink",".vcf":"text/x-vcard",".vcg":"application/vnd.groove-vcard",".vcs":"text/x-vcalendar",".vcx":"application/vnd.vcx",".vis":"application/vnd.visionary",".viv":"video/vnd.vivo",".vor":"application/vnd.stardivision.writer",".vox":"application/x-authorware-bin",".vrml":"model/vrml",".vsd":"application/vnd.visio",".vsf":"application/vnd.vsf",".vss":"application/vnd.visio",".vst":"application/vnd.visio",".vsw":"application/vnd.visio",".vtu":"model/vnd.vtu",".vxml":"application/voicexml+xml",".w3d":"application/x-director",".wad":"application/x-doom",".wav":"audio/x-wav",".wax":"audio/x-ms-wax",".wbmp":"image/vnd.wap.wbmp",".wbs":"application/vnd.criticaltools.wbs+xml",".wbxml":"application/vnd.wap.wbxml",".wcm":"application/vnd.ms-works",".wdb":"application/vnd.ms-works",".wiz":"application/msword",".wks":"application/vnd.ms-works",".wm":"video/x-ms-wm",".wma":"audio/x-ms-wma",".wmd":"application/x-ms-wmd",".wmf":"application/x-msmetafile",".wml":"text/vnd.wap.wml",".wmlc":"application/vnd.wap.wmlc",".wmls":"text/vnd.wap.wmlscript",".wmlsc":"application/vnd.wap.wmlscriptc",".wmv":"video/x-ms-wmv",".wmx":"video/x-ms-wmx",".wmz":"application/x-ms-wmz",".wpd":"application/vnd.wordperfect",".wpl":"application/vnd.ms-wpl",".wps":"application/vnd.ms-works",".wqd":"application/vnd.wqd",".wri":"application/x-mswrite",".wrl":"model/vrml",".wsdl":"application/wsdl+xml",".wspolicy":"application/wspolicy+xml",".wtb":"application/vnd.webturbo",".wvx":"video/x-ms-wvx",".x32":"application/x-authorware-bin",".x3d":"application/vnd.hzn-3d-crossword",".xap":"application/x-silverlight-app",".xar":"application/vnd.xara",".xbap":"application/x-ms-xbap",".xbd":"application/vnd.fujixerox.docuworks.binder",".xbm":"image/x-xbitmap",".xdm":"application/vnd.syncml.dm+xml",".xdp":"application/vnd.adobe.xdp+xml",".xdw":"application/vnd.fujixerox.docuworks",".xenc":"application/xenc+xml",".xer":"application/patch-ops-error+xml",".xfdf":"application/vnd.adobe.xfdf",".xfdl":"application/vnd.xfdl",".xht":"application/xhtml+xml",".xhtml":"application/xhtml+xml",".xhvml":"application/xv+xml",".xif":"image/vnd.xiff",".xla":"application/vnd.ms-excel",".xlam":"application/vnd.ms-excel.addin.macroenabled.12",".xlb":"application/vnd.ms-excel",".xlc":"application/vnd.ms-excel",".xlm":"application/vnd.ms-excel",".xls":"application/vnd.ms-excel",".xlsb":"application/vnd.ms-excel.sheet.binary.macroenabled.12",".xlsm":"application/vnd.ms-excel.sheet.macroenabled.12",".xlsx":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",".xlt":"application/vnd.ms-excel",".xltm":"application/vnd.ms-excel.template.macroenabled.12",".xltx":"application/vnd.openxmlformats-officedocument.spreadsheetml.template",".xlw":"application/vnd.ms-excel",".xml":"application/xml",".xo":"application/vnd.olpc-sugar",".xop":"application/xop+xml",".xpdl":"application/xml",".xpi":"application/x-xpinstall",".xpm":"image/x-xpixmap",".xpr":"application/vnd.is-xpr",".xps":"application/vnd.ms-xpsdocument",".xpw":"application/vnd.intercon.formnet",".xpx":"application/vnd.intercon.formnet",".xsl":"application/xml",".xslt":"application/xslt+xml",".xsm":"application/vnd.syncml+xml",".xspf":"application/xspf+xml",".xul":"application/vnd.mozilla.xul+xml",".xvm":"application/xv+xml",".xvml":"application/xv+xml",".xwd":"image/x-xwindowdump",".xyz":"chemical/x-xyz",".zaz":"application/vnd.zzazz.deck+xml",".zip":"application/zip",".zir":"application/vnd.zul",".zirz":"application/vnd.zul",".zmm":"application/vnd.handheld-entertainment+xml",".hchtml":"text/html"}

MAX_REQ_BODY_SIZE = 10000

req_count = 0

server_id = ""

try:
    h = hashlib.sha1()
    with open('/etc/machine-id','rb') as f:
        h.update(f.read())
    server_id = h.hexdigest()
except:
    server_id = "unknown"

class HYPERCALException(Exception):
    pass

class HYPERCALParseException(HYPERCALException):
    pass

class HYPERCALResourceLimitation(HYPERCALException):
    pass

class HYPERCALPile:
    def __init__(self, ret_pos=None):
        self.values = {}
        self.piles = {}
        self.ret_pos = ret_pos
        self.deferred = []

    def derobe(self, mask):
        if mask in self.values.keys():
            return self.values[mask]
        else:
            return None

    def getpile(self, mask): 
        if mask in self.piles.keys():
            return self.piles[mask]
        else:
            return None

    def from_dict(d):
        p = HYPERCALPile()
        p.values = d if d != None else {}
        return p

    def become(self, pile):
        self.values = pile.values
        self.piles = pile.piles

hypercal_verbs = {}
def hypercal_verb(verb_name, min_args=0, accepts_do=False):
    def dec(func):
        def inner(ctx, args, do=None):
            if len(args) < min_args:
                ctx.aggravate(1)
                args += ["HYPERCAL"*ctx.aggravation] * (min_args - len(args)) 
            if accepts_do:
                return func(ctx, args, do)
            else:
                if do != None:
                    ctx.aggravate(1)
                return func(ctx, args)
        hypercal_verbs[verb_name] = inner
        return inner
    return dec

@hypercal_verb("PRINT", 1)
def verb_print(ctx, args):
    ctx.output += " ".join(args)

@hypercal_verb("CONNECT", 2)
def verb_connect(ctx, args):
    return "".join(args)

@hypercal_verb("LENGTH", 1)
def verb_length(ctx, args):
    return str(len(args[0]))

@hypercal_verb("INDEX", 2)
def verb_index(ctx, args):
    i = ctx.get_int(args[1])
    if i >= len(args[0]) or i < 0:
        return ""
    return args[0][i]

@hypercal_verb("CHAR", 1)
def verb_char(ctx, args):
    try:
        return chr(ctx.get_int(args[0]))
    except:
        return '\0'

@hypercal_verb("CHARCODE", 1)
def verb_charcode(ctx, args):
    if len(args[0]) > 0:
        try:
            return str(ord(args[0][0]))
        except:
            return '\0'
    else:
        return '\0'

@hypercal_verb("CUT", 3)
def verb_cut(ctx, args):
    a = ctx.get_int(args[1])
    b = ctx.get_int(args[2])
    return args[0][a:b]

@hypercal_verb("ADD", 2)
def verb_add(ctx, args):
    return str(ctx.get_int(args[0]) + ctx.get_int(args[1]))

@hypercal_verb("MULT", 2)
def verb_mult(cx, args):
    return str(ctx.get_int(args[0]) * ctx.get_int(args[1]))

@hypercal_verb("EXP", 2)
def verb_mult(ctx, args):
    return str(ctx.get_int(args[0]) ** ctx.get_int(args[1]))

@hypercal_verb("TETR", 2)
def verb_tetra(ctx, args):
    a = ctx.get_int(args[0])
    b = ctx.get_int(args[1])
    r = a
    if ctx.max_cycles != None:
        raise(HYPERCALResourceLimitation(
            "The raw power of HYPERCAL is limited for this session. "
            "Tetration is unallowed."))
    if b == 0:
        return "1"
    elif b > 0:
        for i in range(b - 1):
            r **= a
    else:
        for i in range(abs(b) - 1):
            r **= 1/a
    return str(int(r))

@hypercal_verb("OUT", 1)
def verb_out(ctx, args):
    return args[0]

@hypercal_verb("BOOKMARK", 1)
def verb_bookmark(ctx, args):
    pass

@hypercal_verb("VERB", 1)
def verb_verb(ctx, args):
    return

@hypercal_verb("WARP", 1)
def verb_warp(ctx, args):
    if ctx.warp(args[0]) == None:
        ctx.aggravate(2)

@hypercal_verb("BESEECH", 1)
def verb_beseech(ctx, args):
    ctx.beseech(args[0])

@hypercal_verb("SURRENDER", 0)
def verb_surrender(ctx, args):
    top = ctx.stack.pop()
    for d in top.deferred:
        d.eval(ctx)
    if top.ret_pos == None:
        ctx.stack.append(top)
        ctx.end()
    else:
        ctx.program_pos = top.ret_pos

@hypercal_verb("DEROBE", 1)
def verb_derobe(ctx, args):
    return ctx.derobe(args[0])

@hypercal_verb("DELETE", 1)
def verb_delete(ctx, args):
    if args[0] in ctx.stack[-1].keys():
        ctx.stack[-1].values.pop(args[0])

@hypercal_verb("REM", 0, accepts_do=True)
def verb_rem(ctx, args, do):
    pass

@hypercal_verb("CHECK", 1, accepts_do=True)
def verb_check(ctx, args, do):
    if args[0] == "27":
        if do != None:
            do.eval(ctx)
        else:
            ctx.aggravate(1)
    return

@hypercal_verb("LARGER", 2)
def verb_larger(ctx, args):
    if ctx.get_int(args[0]) > ctx.get_int(args[1]):
        return "27"
    else:
        return "28"

@hypercal_verb("SMALLER", 2)
def verb_smaller(ctx, args):
    if ctx.get_int(args[0]) < ctx.get_int(args[1]):
        return "27"
    else:
        return "28"

@hypercal_verb("MATCH", 2)
def verb_match(ctx, args):
    if args[0] == args[1]:
        return "27"
    else:
        return "28"

@hypercal_verb("DO NOT SUMMON NASAL DEMONS", 0)
def verb_nasal_demons(ctx, args):
    ctx.aggravate(-1)

@hypercal_verb("ESCAPE", 1)
def verb_escape(ctx, args):
    return escape(args[0])

@hypercal_verb("NEWPILE", 1)
def verb_newpile(ctx, args):
    ctx.stack[-1].piles[args[0]] = HYPERCALPile()

def pile_traverse(ctx, piles):
    r = ctx.stack[-1]
    for pmask in piles:
        if pmask == "bottom":
            r = ctx.stack[0]
        elif pmask == "below" and len(ctx.stack) > 1:
            r = ctx.stack[-2]
        else:
            r = r.getpile(pmask)
        if r == None:
            ctx.aggravate(4)
            r = ctx.stack[-1]
    return r

#TODO: add traversal to DEROBE

@hypercal_verb("IN", 1, accepts_do=True)
def verb_in(ctx, args, do):
    if do == None:
        ctx.aggravate(2)
        return
    ctx.stack.append(pile_traverse(ctx, args))
    do.eval(ctx)
    ctx.stack.pop()

@hypercal_verb("LINK", 2)
def verb_link(ctx, args):
    ctx.stack[-1].piles[args[-1]] = pile_traverse(ctx, args)

@hypercal_verb("DISOWN", 1)
def verb_disown(ctx, args):
    if args[0] in ctx.stack[-1].piles.keys():
        ctx.stack[-1].piles.pop(args[0])

@hypercal_verb("EXTANCE", 1)
def verb_extance(ctx, args):
    if args[0] in ctx.stack[-1].values.keys():
        return '27'
    else:
        return '28'

@hypercal_verb("NEGATE", 1)
def verb_negate(ctx, args):
    if args[0] == '27':
        return '28'
    else:
        return '27'

@hypercal_verb("CONJUNCT", 2)
def verb_conjunct(ctx, args):
    if args[0] == '27' and args[1] == '27':
        return '27'
    else:
        return '28'

@hypercal_verb("DISJUNCT", 2)
def verb_conjunct(ctx, args):
    if args[0] == '27' or args[1] == '27':
        return '27'
    else:
        return '28'

@hypercal_verb("ONCE", 0, accepts_do=True)
def verb_once(ctx, args, do):
    if do != None:
        do.eval(ctx)
        do.verb = "REM"

@hypercal_verb("ONLY", 1, accepts_do=True)
def verb_only(ctx, args, do):
    times = ctx.get_int(args[0])
    do.counter += 1
    if do != None and do.counter < times:
        do.eval(ctx)

@hypercal_verb("PROCRASTINATE", 0, accepts_do=True)
def verb_defer(ctx, args, do):
    ctx.stack[-1].deferred.append(do)

@hypercal_verb("DEMONGAUGE", 0, accepts_do=True)
def verb_demongauge(ctx, args, do):
    before = ctx.aggravation
    do.eval(ctx)
    if ctx.aggravation > before and not random.randint(0,15) == 7:
        return "27"
    else:
        return "28"

@hypercal_verb("PARALLEL", 1)
def verb_parallel(ctx, args):
    new_ctx = HYPERCALContext()
    new_ctx.program = ctx.program
    new_ctx.result = ctx.result
    new_ctx.stack[-1].become(ctx.stack[-1])
    if new_ctx.warp(args[0]) == None:
        return
    new_ctx.stack.append(HYPERCALPile())
    ctx.parallel.append(new_ctx)

# HYPER-revolutionary OOP! 
# (not as revolutionary as the HOLY patterns of HYPERCAL, however)
class HYPERCALDerobal:
    def __init__(self, mask, depth, bottom=False):
        self.mask = mask
        self.depth = depth
        self.bottom = bottom

    def derobe(self, ctx):
        if hasattr(self.mask, 'derobe'):
            mask = self.mask.derobe(ctx)
        else:
            mask = self.mask
        if self.bottom:
            return ctx.derobe(mask, len(ctx.stack) - 1)
        else:
            return ctx.derobe(mask, self.depth)

class HYPERCALResultReference:
    def derobe(self, ctx):
        return ctx.result

class HYPERCALStatement:
    def __init__(self, verb, args, please, out=None, do=None):
        self.verb = verb
        self.args = args
        self.out = out
        self.please = please
        self.do = do
        self.counter = 0

    def eval(self, ctx):
        ctx.current_stmt = self
        args = [
            arg if not hasattr(arg, 'derobe') else arg.derobe(ctx) for arg in self.args]
        if not self.verb in hypercal_verbs.keys():
            result = None
            if ctx.beseech(self.verb, verb=True) != None:
                ctx.stack[-1].piles['arg'] = HYPERCALPile.from_dict(
                    dict((str(x),y) for x, y in enumerate(args))
                )
            else:
                raise(HYPERCALException(f"Verb '{self.verb}' unexists"))
        else:
            result = hypercal_verbs[self.verb](ctx, args, self.do)
        if result != None:
            ctx.result = result
        if self.out != None:
            if hasattr(self.out, 'derobe'):
                out = self.out.derobe(ctx)
            else:
                out = self.out
            if result == None:
                ctx.set(out, "H Y P E R C A L " * ctx.aggravation)
            else:
                ctx.set(out, result)
        if self.please:
            ctx.please_stmts += 1
            if random.randint(0,100) == 27:
                ctx.aggravate(1)
        else:
            ctx.pleasent_stmts += 1
        if ctx.pleasent_stmts > 2 * ctx.please_stmts:
            ctx.aggravate(1)
        ctx.cycles += 1

def parse_gen(program):
    for c in program:
        yield c
    while 1:
        yield '\0'

class HYPERCALParser:
    def __init__(self, program):
        self.program = program
        self.gen = parse_gen(program)
        self.current = next(self.gen)
        self.line = 0
        self.curline = []

    def consume(self):
        c = self.current
        self.current = next(self.gen)
        if c == '\n': 
            self.curline = []
            self.line += 1
        else:
            self.curline.append(c)

        return c

    def error(self, err):
        while not self.peek() == '\n' and not self.end():
            self.consume()
        raise(HYPERCALParseException(
            f"(parse error on line {self.line})\n\t"
            f"`{''.join(self.curline).strip()}`\n\n\terror: {err}"))
    
    def end(self):
        return self.current == '\0'

    def accept(self, cond):
        if cond(self.current) and self.current != '\0':
            return self.consume()
        else:
            return None
    
    def expect(self, cond):
        if cond(self.current):
            return self.consume()
        else:
            if self.current == '\n':
                self.error("Unexpected end of line")
            elif self.current == '\0':
                self.error("Unexpected end of segment")
            else:
                self.error(f"Unexpected character ({self.current})")

    def peek(self):
        return self.current
    
    def whitespace(self):
        ws = False
        while True:
            c = self.accept(lambda c: (c.isspace() or c == ')') and c != '\n')
            if c == ')':
                while self.accept('\n'.__ne__) != None:
                    pass
            elif c == None:
                break
            ws = True
        return ws

    def linespace(self):
        ws = False
        while self.accept(lambda c: c.isspace()) != None:
            ws = True
        return ws
    
    def keyword(self):
        k = ""
        while 1:
            c = self.accept(lambda c: c.isupper() or c == "☭")
            if c == None:
                if k == "":
                    return None
                else:
                    return k
            else:
                k += c

    def value(self):
        if self.accept('"'.__eq__) == None:
            if self.peek() == '!' or self.peek() == '#':
                depth = 0
                while self.accept('!'.__eq__) != None:
                    depth += 1
                self.expect('#'.__eq__)
                return HYPERCALDerobal(self.value(), depth)
            elif self.peek() == '&':
                self.expect('&'.__eq__)
                return HYPERCALDerobal(self.value(), 0, bottom=True)
            else:
                self.expect('@'.__eq__)
                return HYPERCALResultReference()
        s = ""
        escape = False
        while 1:
            c = self.accept('"'.__ne__)
            if c == None:
                c = self.expect('"'.__eq__)
                if not escape:
                    return s
            if escape:
                if c == '`' or c == '"':
                    s += c
                elif c == '$':
                    s += '\n'
                else:
                    s += '`' + c
                escape = False
            elif c == '`':
                escape = True
            else:
                s += c

    def expect_keyword(self, k):
        self.whitespace()
        if self.keyword() != k:
            self.error(f"Expected '{k}'")
        self.whitespace()
    
    def statement(self, in_do=False):
        self.whitespace()
        k = self.keyword()
        if k == "PLEASE":
            please = True
            if not self.whitespace():
                self.expect(lambda _: False)
            k = self.keyword()
        else:
            please = False
        if k == None:
            self.error("Expected keyword or verb")
        verb = k

        if (verb == "NOT" and in_do) or verb == "DO":
            if not in_do:
                self.expect_keyword("NOT")
            self.expect_keyword("SUMMON")
            self.expect_keyword("NASAL")
            self.expect_keyword("DEMONS")
            verb = "DO NOT SUMMON NASAL DEMONS"

        args = []
        self.whitespace()
        val_chars = '"#@!&'
        if self.peek() in val_chars:
            while 1:
                self.whitespace()
                args.append(self.value())
                self.whitespace()
                if self.accept(",".__eq__) == None:
                    break
        self.whitespace()
        out = None
        do = None
        if self.accept(lambda c: c == '\n' or c == ':') == None and not self.end():
            k = self.keyword()
            if k == "OUT":
                self.whitespace()
                out = self.value()
                self.whitespace()
                self.expect(lambda c: c == '\n' or self.end())
            elif k == "DO":
                self.whitespace()
                do = self.statement(in_do=True)
            else:
                self.error("Expected 'OUT', 'DO', or end of line")
        self.whitespace()
        return HYPERCALStatement(verb, args, please, out, do)

    def parse(self):
        prog = []
        while not self.end():
            self.linespace()
            prog.append(self.statement())
            self.linespace()
        return prog

class HYPERCALContext:
    def __init__(self, demon_threshold=15, max_cycles=None):
        self.stack = [HYPERCALPile()]
        self.aggravation = 1
        self.demon_threshold = demon_threshold
        self.cycles = 0
        self.max_cycles = max_cycles
        self.result = ""
        self.output = ""
        self.program = []
        self.program_pos = 0
        self.user_verbs = set([])
        self.please_stmts = 0
        self.pleasent_stmts = 0
        self.current_stmt = None
        self.parallel = []

    def nasal_demons(self):
        return self.aggravation > self.demon_threshold
    
    def step(self):
        if not self.done():
            self.program[self.program_pos].eval(self)
            self.program_pos += 1
            if self.nasal_demons():
                self.program_pos += random.randint(-1,1)
        for p in self.parallel:
            p.step()
            self.output += p.output
            p.output = ""
            if p.done() and len(p.parallel) == 0:
                self.parallel.remove(p)
                self.cycles += p.get_cycles()
        if self.max_cycles != None and self.get_cycles() > self.max_cycles:
            raise(HYPERCALResourceLimitation("Program ran for too long!"))

    def done(self):
        return self.program_pos >= len(self.program)

    def run(self):
        while (not self.done()) or len(self.parallel) > 0:
            self.step()
    
    def get_cycles(self):
        pllel_cycles = 0
        for p in self.parallel:
            pllel_cycles += p.get_cycles()
        return self.cycles + pllel_cycles

    def eval(self, program):
        self.stack = [self.stack[0]]
        self.program += HYPERCALParser(program).parse()
        self.run()
        output = self.output
        self.output = ""
        return output

    def warp(self, bookmark, verb=False):
        for pos,stmt in enumerate(self.program):
            if (stmt.verb == "BOOKMARK" or stmt.verb == "VERB") \
                    and stmt.args[0] == bookmark:
                if verb and not stmt.verb == "VERB":
                    continue
                self.program_pos = pos
                return pos
        return None

    def beseech(self, bookmark, verb=False):
        self.stack.append(HYPERCALPile(ret_pos=self.program_pos))
        result = self.warp(bookmark, verb)
        if result == None:
            self.stack.pop()
            self.aggravate(3)
        return result
    
    def derobe(self, mask, depth=0):
        if depth >= len(self.stack):
            self.aggravate(depth)
            return "LACREPYH" * self.aggravation
        v = self.stack[-1 - depth].derobe(mask)
        if v == None:
            self.aggravate(1)
            return "HYPERCAL" * self.aggravation
        else:
            if self.nasal_demons():
                v = v[::-1]
            return v
    
    def set(self, mask, value, depth=0):
        if depth >= len(self.stack):
            self.aggravate(depth)
        self.stack[-1 - depth].values[mask] = value

    def getpile(self, mask, depth=0):
        if depth >= len(self.stack):
            self.aggravate(depth)
            return self.stack[-1]
        if mask in self.stack[-1 - depth].piles.keys():
            return self.stack[-1 - depth].getpile(mask)
        elif mask == "bottom":
            return self.stack[0]
        elif mask == "below" and len(self.stack) >= 2:
            return self.stack[-2]
        else:
            self.aggravate(1)
            return self.stack[-1]

    def get_int(self, string):
        try:
            return int(string)
        except:
            self.aggravate(1)
            return random.randint(0,100)

    def aggravate(self, amount):
        if self.nasal_demons() or self.aggravation <= -self.demon_threshold:
            self.aggravation += max(0, amount)
        else:
            self.aggravation += amount
            if self.nasal_demons():
                stderr.write("WARNING: nasal demons HAVE been summoned!\n")

    def end(self):
        self.program_pos = len(self.program)

class Abort(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(STATUS_CODES[code])

class HYPERCALAbort(Abort, HYPERCALException):
    pass

@hypercal_verb("EXEC", 2)
def verb_exec(ctx, args):
    if ctx.max_cycles != None:
        raise(HYPERCALResourceLimitation("You cannot bypass resource limits!"))
    new_ctx = HYPERCALContext(
            max_cycles=ctx.get_int(args[2]) if len(args) > 2 else None)
    pile_arg = ctx.getpile(args[1])
    new_ctx.stack[-1].become(pile_arg)
    try:
        result = new_ctx.eval(args[0])
        ctx.set('error', "28")
    except HYPERCALException as err:
        result = new_ctx.output
        ctx.set('error', "27")
        ctx.set('error details', str(err))
    ctx.set('nasal demons', "27" if new_ctx.nasal_demons() else "28")
    return result

@hypercal_verb("ABORT", 1)
def verb_abort(ctx, args):
    code = ctx.get_int(args[0])
    if code in STATUS_CODES.keys() and \
            not str(code)[0] == "2" or str(code)[0] == "3":
        raise(HYPERCALAbort(code))
    else:
        ctx.aggravate(30)

class Response: # Revolutionary OOP
    def __init__(self, page, status=None, request_method="GET", req_data=None):
        self.headers = ""
        self.method = request_method
        self.req_data = req_data

        self.status = STATUS_CODES[200] if status == None else status

        self.body = DEFAULT_INDEX
        content_type = self.get_body(page)

        self.add_header('Date', 'Tue, 7 Jan 100 00:58:20 GMT')
        self.add_header('Cache-Control', 'exhibitionist, max-age=45')
        self.add_header('Content-Type', content_type)
        self.add_header('P3P', 'CP="Privacy is obselete. Any and all data shall be sold to the highest bidder"')
        self.add_header('Content-Length', len(self.body))
        self.add_header('Server', VERSION)
        self.add_header('X-XSS-Protection', '0')
        self.add_header('X-Frame-Options', 'plant-evidence')
        self.add_header('Based-on', 'what')
        self.add_header('Accept-Ranges', 'none')
        self.add_header('Vary', '*')
        self.add_header('Warning', '199 It Kind Of Smells Like Piss In Here')
        self.add_header('Connection', 'close')
        self.add_header('Expires', 'Yesterday')
        self.add_header('Pragma', 'hi-mom')
        self.add_header('X-Powered-By', 'Wage Slavery')
        self.add_header('Hotel', 'Trivago')
        self.add_header('X-Content-Duration', '999999999.666')
        self.add_header('BlatID', server_id)
        self.add_header('Flacidity', 'about three')
        self.add_header('Bees', 'many')
        self.add_header('Humor-Quality', 'terrible')
        self.add_header('English-Spelling', 'american')
        self.add_header('Namesake', 'cockroach')
        self.add_header('Mood', 'angsty')
        self.add_header('Height', '124cm')
        self.add_header('Freshness', 'rotten')
        self.add_header('Editor', 'vim')
        self.add_header('Wug-Plural', 'wuggen')
        self.add_header('GNU-Copypasta', "I'd just like to interject for a moment. What you're refering to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called Linux, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called Linux distributions are really distributions of GNU/Linux!")
        self.add_header('PH', '7')
        self.add_header('Orientation', 'pansexual')
        self.add_header('Gender', 'none')
        self.add_header('Identity', 'gamer')
        self.add_header('Political-Afflilation', 'crypto-anarcho-marxist-juche-reaganism')
        self.add_header('SSN', '457-55-5462')
        self.add_header('Viscosity', '0.01 poise')
        self.add_header('Favorite-Color', 'orange')
        self.add_header('Complexity', 'O(log n)')
        self.add_header('Computational-Class', 'turing-complete')
        self.add_header('Lifespan', '10-20 years')
        self.add_header('Legacy', 'none')
        self.add_header('Zodiac', 'aries')
        self.add_header('Temperature', '62 C')
        self.add_header('Knuckles', 'cracked')
        self.add_header('Shoe-Size', 'confidential')
        self.add_header('Subscribed-Conspiracy-Theories', 'time-cube')
        self.add_header('Dimensions', '4')
        self.add_header('Distro', 'debian')
        self.add_header('Geometric-Shape', 'cone')
        self.add_header('Random-Number', random.randint(0,10))
        self.add_header('Price', '$32')
        self.add_header('Step-2', 'cover-yourself-in-oil')
        self.add_header('Taxes', 'evaded')
        self.add_header('Crimes-Against-Humanity', 5)
        self.add_header('Rickroll', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.add_header('Income', 'around $73,000')

    def parse_hc(self, hc):
        BEGIN_TAG = "<HYPERCAL>"
        END_TAG = "</HYPERCAL>"

        ctx = HYPERCALContext()
        ctx.set('request method', self.method)
        if self.req_data != None:
            def convert(x):
                if x == None:
                    return None
                r = {}
                for key in x.keys():
                    if len(x[key]) > 0:
                        r[key] = x[key][0].replace('\r\n', '\n')
                return r
            ctx.stack[-1].piles['request headers'] = \
                    HYPERCALPile.from_dict(self.req_data.headers)
            ctx.stack[-1].piles['form data'] = \
                    HYPERCALPile.from_dict(convert(self.req_data.form))
            ctx.stack[-1].piles['request parameters'] = \
                    HYPERCALPile.from_dict(convert(self.req_data.params))
            ctx.set('request body',
                    "" if self.req_data.body == None else self.req_data.body)
        result = ""
        while 1:
            begin = hc.find(BEGIN_TAG)
            if begin == -1:
                result += hc
                break
            result += hc[:begin]
            hc = hc[begin + len(BEGIN_TAG):]
            end = hc.find(END_TAG)
            if end == -1: 
                raise(HYPERCALParseException("Unbalanced HYPERCAL tags"))
            hc_source = hc[:end]
            result += ctx.eval(hc_source)
            hc = hc[end + len(END_TAG):]

        self.body = result.encode('utf-8')

    def get_body(self, page):
        if self.status.split()[0] != "200":
            self.error_page()
            return 'text/html'
        p = get_page(page)
        if p == None:
            if page == "/index.html":
                self.body = DEFAULT_INDEX.encode('utf-8')
                return 'text/html'
            else:
                self.status = STATUS_CODES[404]
                self.error_page()
                return 'text/html'
        else:
            self.body = p
            _, ext = os.path.splitext(page)
            if ext == '.hchtml':
                self.parse_hc(p.decode('utf-8'))
            elif self.method == "POST":
                raise(Abort(405))
            return 'text/plain' if not ext.lower() in MIMES.keys() else MIMES[ext.lower()]

    def error_page(self):
        code = self.status.split()[0]
        p = get_page(f"{code}.html")
        if p != None:
            self.body = p
            return
        p = get_page("_err.html")
        if p != None:
            p = p.replace('BLATTIDUS ERROR'.encode('utf-8'), self.status.encode('utf-8'))
            self.body = p
            return
        self.body = f"<h1>{self.status}</h1>".encode('utf-8')

    def add_header(self, header, value):
        self.headers += f"{header}: {value}\n"

    def encode(self):
        if self.method == "HEAD" or self.method == "MARCO":
            return f"HTTP/1.1 {self.status}\n{self.headers}".encode('utf-8')
        elif self.method == "TEG":
            return f"HTTP/1.1 {self.status}\n{self.headers}\n".encode('utf-8') + self.body[::-1]
        else:
            return f"HTTP/1.1 {self.status}\n{self.headers}\n".encode('utf-8') + self.body

class RequestData:
    def get_line(self):
        l = []
        for c in self.stream:
            if c == '\n':
                break
            l.append(c)
        return ''.join(l)

    def __init__(self, stream):
        self.stream = stream
        self.headers = {}
        self.body = None
        self.form = None
        req_top = self.get_line().split()
        self.method = req_top[0]
        loc = urllib.parse.urlparse(req_top[1])
        self.path = loc.path
        self.params = urllib.parse.parse_qs(loc.query)
        while 1:
            header_str = self.get_line()
            if len(header_str.strip()) == 0:
                break
            h = header_str.split(':')
            self.headers[h[0].strip()] = urllib.parse.unquote(h[1].strip())
        if 'Content-Length' in self.headers.keys() and self.method == 'POST':
            l = []
            length = int(self.headers['Content-Length'])
            assert(length < MAX_REQ_BODY_SIZE)
            for i in range(length):
                l.append(next(stream))
            self.body = ''.join(l)
            if 'Content-Type' in self.headers.keys() \
                    and self.headers['Content-Type'] == 'application/x-www-form-urlencoded':
                self.form = urllib.parse.parse_qs(self.body)

class Blattidus(socketserver.BaseRequestHandler):
    def perform_response(self, sock, method, path, status, req_data=None):
        try:
            r = Response(path, status=status, request_method=method, req_data=req_data)
            sock.send(r.encode())
        except Abort as abrt:
            r = Response(
                    "", status=STATUS_CODES[abrt.code], request_method="GET", req_data=req_data)
            sock.send(r.encode())
        except HYPERCALException as err:
            stderr.write(f"{path}: HYPERCAL error: {err}\n")
            sock.send(
                    Response(path, status=STATUS_CODES[500], req_data=req_data).encode())
            return
        except Exception as err:
            if args.log:
                stderr.write(f"ERROR ({err}) serving response ({method} {path})\n")
            sock.send(Response(path, status=STATUS_CODES[500]).encode())
            bees
            return
        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        if args.log:
            stderr.write(f"{method} {path} -> {r.status}\n")

    def stream_data(self,sock):
        while True:
            data = sock.recv(2048).decode('utf-8')
            for c in data:
                yield c

    def _handle(self, sock):
        sock.settimeout(40) # blattidus is generous
        global req_count
        req_count += 1
        if args.log and cachesize != 0 and req_count % 10 == 0:
            info = get_page.cache_info()
            stderr.write(
                f"[file cache info] hits: {info.hits}, misses: {info.misses}, "
                f"max size: {info.maxsize}, current size: {info.currsize}\n")
        try:
            rd = RequestData(self.stream_data(sock))
            req_method = rd.method
            req_path = rd.path
        except TimeoutError:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            return
        except:
            self.perform_response(sock, "GET", "/", STATUS_CODES[400])
            return
            
        if req_method == "GET" or req_method == "TEG" \
                or req_method == "HEAD" or req_method == "POST":
            if req_path == "/":
                req_path = "/index.html"
            self.perform_response(sock, req_method, req_path, STATUS_CODES[200], req_data=rd)
        elif req_method == "BREW" or req_method == "WHEN":
            self.perform_response(sock, req_method, "", STATUS_CODES[418])
        elif req_method == "MARCO":
            self.perform_response(sock, req_method, "", STATUS_CODES[299])
        else:
            self.perform_response(sock, req_method, "", STATUS_CODES[405], req_data=rd)

    def handle(self):
        self._handle(self.request)

class BlattidusSecure(Blattidus):
    def handle(self):
        sock = ssl_ctx.wrap_socket(self.request,server_side=True)
        sock.do_handshake()
        self._handle(sock)

class BlattidusTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


servs = []
servs.append(BlattidusTCPServer((HOST, PORT), Blattidus))
if ssl_ctx != None:
    servs.append(BlattidusTCPServer((HOST, args.https_port), BlattidusSecure))

def runserver(s):
    try:
        s.serve_forever()
    except:
        for serv in servs:
            serv.shutdown()
for serv in servs:
    threading.Thread(target=runserver, args=(serv,)).start()
